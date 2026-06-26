#!/usr/bin/env python3
"""跨所套利计算器"""
import json
import sys
import urllib.request
import urllib.error

COIN_SYMBOLS = {
    'btc': 'bitcoin', 'eth': 'ethereum', 'usdt': 'tether',
    'sol': 'solana', 'bnb': 'binancecoin', 'xrp': 'ripple',
    'ada': 'cardano', 'doge': 'dogecoin', 'dot': 'polkadot',
    'matic': 'matic-network'
}

def fetch_price(coin_id):
    """Fetch price from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            return data.get(coin_id, {}).get('usd', 0)
    except:
        return 0

def check_binance(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return float(json.loads(r.read()).get('price', 0))
    except:
        return 0

def check_okx(symbol):
    url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            return float(data['data'][0]['last'])
    except:
        return 0

def check_bybit(symbol):
    url = f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}USDT"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
            return float(data['result']['list'][0]['lastPrice'])
    except:
        return 0

def check_arbitrage(coin):
    symbol = coin.upper()
    prices = {
        'Binance': check_binance(symbol),
        'OKX': check_okx(symbol),
        'Bybit': check_bybit(symbol)
    }
    
    valid = {k: v for k, v in prices.items() if v > 0}
    if len(valid) < 2:
        print(f"  ⚠️ {symbol}: 数据不足 | {prices}")
        return
    
    best = max(valid, key=valid.get)
    worst = min(valid, key=valid.get)
    spread = valid[best] - valid[worst]
    spread_pct = (spread / valid[worst]) * 100 if valid[worst] > 0 else 0
    
    if spread_pct > 0.1:
        arrow = "🔴"
    elif spread_pct > 0.01:
        arrow = "🟡"
    else:
        arrow = "🟢"
    
    print(f"  {arrow} {symbol}: 价差 {spread_pct:.3f}% | ${spread:.4f}")
    print(f"     最高: {best} (${valid[best]:,.2f}) | 最低: {worst} (${valid[worst]:,.2f})")

def main():
    coins = sys.argv[1:] if len(sys.argv) > 1 else ['btc', 'eth', 'sol', 'bnb']
    
    print("🏦 跨所套利扫描")
    print(f"{'─'*45}")
    for c in coins:
        check_arbitrage(c)
    
    print(f"\n💡 价差>0.1%有套利空间 | 需扣除手续费(0.1%)和滑点")
    print("💡 不包含转账时间和Gas费")

if __name__ == '__main__':
    main()
