#!/usr/bin/env python3
import requests

def get_currency_list():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to get currencies (status code {response.status_code})")
        return None
    
    data = response.json()
    if data["result"] != "success":
        print(f"Error: {data.get('error-type', 'Unknown error')}")
        return None
    
    return list(data["rates"].keys())

def main():
    currencies = get_currency_list()
    if not currencies:
        return
    
    print("Available currency codes:")
    print("------------------------")
    for i, currency in enumerate(sorted(currencies), 1):
        print(f"{i:3d}. {currency}")
    
    print(f"\nTotal: {len(currencies)} currencies available")

if __name__ == "__main__":
    main()
