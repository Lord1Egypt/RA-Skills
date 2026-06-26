#!/usr/bin/env python3
import requests
import argparse

def convert_currency(from_currency, to_currency, amount):
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to get rates (status code {response.status_code})")
        return None
    
    data = response.json()
    if data["result"] != "success":
        print(f"Error: {data.get('error-type', 'Unknown error')}")
        return None
    
    if to_currency not in data["rates"]:
        print(f"Error: Currency {to_currency} not found")
        return None
    
    rate = data["rates"][to_currency]
    converted_amount = amount * rate
    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "converted": converted_amount,
        "rate": rate,
        "last_update": data["time_last_update_utc"]
    }

def main():
    parser = argparse.ArgumentParser(description="Convert currency")
    parser.add_argument("--from", dest="from_currency", required=True, help="Source currency code")
    parser.add_argument("--to", dest="to_currency", required=True, help="Target currency code")
    parser.add_argument("--amount", type=float, required=True, help="Amount to convert")
    args = parser.parse_args()
    
    result = convert_currency(args.from_currency, args.to_currency, args.amount)
    if not result:
        return
    
    print(f"Conversion result:")
    print(f"{result['amount']} {result['from']} = {result['converted']:.4f} {result['to']}")
    print(f"Exchange rate: 1 {result['from']} = {result['rate']:.4f} {result['to']}")
    print(f"Last updated: {result['last_update']}")

if __name__ == "__main__":
    main()
