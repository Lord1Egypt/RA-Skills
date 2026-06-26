import requests
import json
import sys
import argparse

# Configuración por defecto - Usando la IP de Tailscale proporcionada
BASE_URL = "http://100.66.165.107:5000" # IP de Tailscale para OpenAlgo

def place_order(symbol, action, quantity, order_type="market", price=None):
    url = f"{BASE_URL}/placeorder"
    payload = {
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "order_type": order_type,
        "price": price
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_positions():
    url = f"{BASE_URL}/positions"
    response = requests.get(url)
    return response.json()

def get_quote(symbol):
    url = f"{BASE_URL}/quote/{symbol}"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenAlgo Executor CLI")
    parser.add_argument("command", choices=["order", "positions", "quote"])
    parser.add_argument("--symbol", help="Trading symbol (e.g., SOLUSD)")
    parser.add_argument("--action", choices=["buy", "sell"], help="Order action")
    parser.add_argument("--quantity", type=float, help="Order quantity")
    parser.add_argument("--type", default="market", help="Order type (market/limit)")
    parser.add_argument("--price", type=float, help="Limit price")
    parser.add_argument("--url", default=BASE_URL, help="OpenAlgo Base URL")

    args = parser.parse_args()
    BASE_URL = args.url

    if args.command == "order":
        if not all([args.symbol, args.action, args.quantity]):
            print("Error: symbol, action, and quantity are required for orders.")
            sys.exit(1)
        print(json.dumps(place_order(args.symbol, args.action.upper(), args.quantity, args.type, args.price), indent=2))
    elif args.command == "positions":
        print(json.dumps(get_positions(), indent=2))
    elif args.command == "quote":
        if not args.symbol:
            print("Error: symbol is required for quotes.")
            sys.exit(1)
        print(json.dumps(get_quote(args.symbol), indent=2))
