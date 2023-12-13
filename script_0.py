#Import Libraries
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError 
import csv

headers = {
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
	}
url = 'https://www.walmart.com.mx/search?q=alimento+'
count=1
#Create top_items as empty list
all_items = []
while count<=23:
	count+=1
	#error handling
	try:
		response = requests.get(url)
	except HTTPError as error:
	 	print(error)
	except URLError as error:
	 	print('The server could not be found!')
	else:
		response = requests.get(url, headers=headers)
		# Parsing the HTML 
		soup = BeautifulSoup(response.content, 'html.parser')
		  
		s = soup.find_all("div",{"role":"group"})
		
		for link in s:
			url_1="https://www.walmart.com.mx"+link.a.attrs['href']
			response1 = requests.get(url_1, headers=headers)
			# Parsing the HTML 
			soup = BeautifulSoup(response1.content, 'html.parser')
			t = soup.find("h1")
			r= soup.find("span",{"class":"f7 rating-number"})
			p=soup.find("div",{"class":"mr1 mr2-xl b black green lh-copy f5 f4-l"})

			if t is None:
				title1 ="N/A"
			else:
				title1=t.text.strip()

			if r is None:
				rating1="N/A"
			else:
				rating2=r.get_text()
				rating1=rating2[1:-1]
				
			if p is None:
				price1 = "N/A"
			else:
				price2 = p.get_text().strip()
				price1=price2[1:]
			all_items.append({"Item": title1,"Priceb($)": price1,"Rating": rating1,"Link": url_1})
			keys = all_items[0].keys()

			with open('data3.csv', 'w', newline='') as output_file:
			    dict_writer = csv.DictWriter(output_file, keys)
			    dict_writer.writeheader()
			    dict_writer.writerows(all_items)
			print(count)
	
	url=f"https://www.walmart.com.mx/search?q=alimento+para+perro+o+alimento+p%2Fperro&page={count}"