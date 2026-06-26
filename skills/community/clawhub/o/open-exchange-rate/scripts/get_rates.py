#!/usr/bin/env python3
import requests
import argparse
import json

def get_latest_rates(base_currency="USD"):
    url = f"https://open.er-api.com/v6/latest/{base_currency}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to get rates (status code {response.status_code})")
        return None
    
    data = response.json()
    if data["result"] != "success":
        print(f"Error: {data.get('error-type', 'Unknown error')}")
        return None
    
    return data

def main():
    parser = argparse.ArgumentParser(description="Get latest exchange rates")
    parser.add_argument("--base", default="USD", help="Base currency code (default: USD)")
    args = parser.parse_args()
    
    data = get_latest_rates(args.base)
    if not data:
        return
    
    print(f"Latest exchange rates (base: {data['base_code']})")
    print(f"Last updated: {data['time_last_update_utc']}")
    print("\nRates:")
    for currency, rate in sorted(data["rates"].items()):
        print(f"1 {data['base_code']} = {rate:.4f} {currency}")

if __name__ == "__main__":
    main()
