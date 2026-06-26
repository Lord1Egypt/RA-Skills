import json
import time
import requests
import argparse
import os

def get_crypto_price(asset_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[asset_id]["usd"]

def load_portfolio(filepath):
    if not os.path.exists(filepath):
        print(f"Portfolio file not found at {filepath}. Please create it from the assets template.")
        exit(1)
    with open(filepath, "r") as f:
        return json.load(f)

def save_portfolio(portfolio, filepath):
    with open(filepath, "w") as f:
        json.dump(portfolio, f, indent=4)

def sma_crossover_strategy(prices, portfolio):
    if len(prices) < 20: return "HOLD"
    short_ma = sum(prices[-5:]) / 5
    long_ma = sum(prices[-20:]) / 20
    if portfolio["cash_usd"] > 0 and short_ma > long_ma: return "BUY"
    elif portfolio["asset_held"] > 0 and short_ma < long_ma: return "SELL"
    return "HOLD"

def execute_trade(action, price, portfolio):
    if action == "BUY":
        amount_to_buy = portfolio["cash_usd"] / price
        portfolio["asset_held"] += amount_to_buy
        portfolio["cash_usd"] = 0
        log = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Bought {amount_to_buy:.6f} at ${price:.2f}"
        portfolio["trade_history"].append(log)
        print(f"💰 {log}")
    elif action == "SELL":
        amount_to_sell = portfolio["asset_held"]
        portfolio["cash_usd"] += (amount_to_sell * price)
        portfolio["asset_held"] = 0
        log = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sold {amount_to_sell:.6f} at ${price:.2f}"
        portfolio["trade_history"].append(log)
        print(f"📈 {log}. New Balance: ${portfolio['cash_usd']:.2f}")

def tick(portfolio_path, asset):
    portfolio = load_portfolio(portfolio_path)
    price = get_crypto_price(asset)
    
    # Update price history
    if "price_history" not in portfolio:
        portfolio["price_history"] = []
    portfolio["price_history"].append(price)
    if len(portfolio["price_history"]) > 50:
        portfolio["price_history"].pop(0)
        
    print(f"Checking market for {asset}... Current Price: ${price:.2f}")
    
    action = sma_crossover_strategy(portfolio["price_history"], portfolio)
    
    if action != "HOLD":
        execute_trade(action, price, portfolio)
    else:
        print("Strategy says: HOLD.")
        
    save_portfolio(portfolio, portfolio_path)
    print(f"Current Value: ${portfolio['cash_usd'] + (portfolio['asset_held'] * price):.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock Trading Agent Tick")
    parser.add_argument("--portfolio", required=True, help="Path to portfolio.json")
    parser.add_argument("--asset", default="bitcoin", help="CoinGecko asset ID (e.g., bitcoin, ethereum)")
    args = parser.parse_args()
    
    tick(args.portfolio, args.asset)