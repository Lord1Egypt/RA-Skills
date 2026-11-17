#!/usr/bin/env python3
"""
perp-basis-scanner: spot vs. perpetual/futures basis scanner across
Binance, Bybit, OKX, and Deribit public REST endpoints (no API key required).

Basis = (perp_price - spot_price) / spot_price
Annualized basis assumes 3x 8-hour funding periods/day (365 days), which is
a rough approximation, not a funding-payment forecast.

Usage:
    python3 basis_scanner.py scan BTC ETH SOL
    python3 basis_scanner.py scan BTC --json
    python3 basis_scanner.py watch BTC ETH --interval 30
"""
import argparse
import json
import sys
import time
import urllib.request
import urllib.error

TIMEOUT = 8


def http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "perp-basis-scanner/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode())


def safe_get(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, KeyError, TypeError) as e:
        return {"error": str(e)}


def binance_pair(symbol: str):
    pair = f"{symbol}USDT"
    spot = http_get(f"https://api.binance.com/api/v3/ticker/price?symbol={pair}")
    perp = http_get(f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={pair}")
    spot_px = float(spot["price"])
    perp_px = float(perp["markPrice"])
    funding_rate = float(perp["lastFundingRate"])
    return {
        "exchange": "binance",
        "spot": spot_px,
        "perp": perp_px,
        "funding_rate_8h_pct": funding_rate * 100,
    }


def bybit_pair(symbol: str):
    pair = f"{symbol}USDT"
    spot = http_get(f"https://api.bybit.com/v5/market/tickers?category=spot&symbol={pair}")
    perp = http_get(f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={pair}")
    spot_px = float(spot["result"]["list"][0]["lastPrice"])
    perp_item = perp["result"]["list"][0]
    perp_px = float(perp_item["markPrice"])
    funding_rate = float(perp_item.get("fundingRate", 0) or 0)
    return {
        "exchange": "bybit",
        "spot": spot_px,
        "perp": perp_px,
        "funding_rate_8h_pct": funding_rate * 100,
    }


def okx_pair(symbol: str):
    spot = http_get(f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT")
    swap = http_get(f"https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT-SWAP")
    funding = http_get(f"https://www.okx.com/api/v5/public/funding-rate?instId={symbol}-USDT-SWAP")
    spot_px = float(spot["data"][0]["last"])
    perp_px = float(swap["data"][0]["last"])
    funding_rate = float(funding["data"][0]["fundingRate"]) if funding.get("data") else 0.0
    return {
        "exchange": "okx",
        "spot": spot_px,
        "perp": perp_px,
        "funding_rate_8h_pct": funding_rate * 100,
    }


def deribit_pair(symbol: str):
    # Deribit only lists BTC/ETH/SOL perpetuals against USDC/USD index.
    index = http_get(f"https://www.deribit.com/api/v2/public/get_index_price?index_name={symbol.lower()}_usd")
    ticker = http_get(f"https://www.deribit.com/api/v2/public/ticker?instrument_name={symbol}-PERPETUAL")
    spot_px = float(index["result"]["index_price"])
    perp_px = float(ticker["result"]["mark_price"])
    funding_rate = float(ticker["result"].get("current_funding", 0) or 0)
    return {
        "exchange": "deribit",
        "spot": spot_px,
        "perp": perp_px,
        # Deribit's current_funding is an 8h-equivalent rate already in decimal form.
        "funding_rate_8h_pct": funding_rate * 100,
    }


FETCHERS = {
    "binance": binance_pair,
    "bybit": bybit_pair,
    "okx": okx_pair,
    "deribit": deribit_pair,
}


def compute_basis(row):
    if "error" in row:
        return row
    basis_pct = (row["perp"] - row["spot"]) / row["spot"] * 100
    annualized_pct = basis_pct * 3 * 365 / 1  # rough: treat basis as if captured daily via funding-like decay
    row["basis_pct"] = round(basis_pct, 4)
    row["annualized_basis_pct_approx"] = round(annualized_pct, 2)
    return row


def scan(symbols, exchanges):
    results = {}
    for symbol in symbols:
        results[symbol] = []
        for ex in exchanges:
            row = safe_get(FETCHERS[ex], symbol)
            if "error" not in row:
                row = compute_basis(row)
            results[symbol].append(row)
    return results


def print_table(results):
    print(f"{'symbol':<6} {'exchange':<9} {'spot':>12} {'perp':>12} {'basis %':>9} {'ann. %':>9} {'fund 8h %':>10}")
    print("-" * 74)
    for symbol, rows in results.items():
        for row in rows:
            if "error" in row:
                print(f"{symbol:<6} {'?':<9} {'error: ' + row['error'][:40]}")
                continue
            print(
                f"{symbol:<6} {row['exchange']:<9} {row['spot']:>12,.2f} {row['perp']:>12,.2f} "
                f"{row['basis_pct']:>9.3f} {row['annualized_basis_pct_approx']:>9.1f} "
                f"{row['funding_rate_8h_pct']:>10.4f}"
            )
    print()
    print("Note: annualized basis is a rough approximation (basis_pct * 3 * 365), not a")
    print("funding-payment forecast. Always re-check live order books before sizing a trade.")


def main():
    parser = argparse.ArgumentParser(description="Spot vs perpetual basis scanner")
    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="One-shot scan")
    scan_p.add_argument("symbols", nargs="+", help="Base symbols, e.g. BTC ETH SOL")
    scan_p.add_argument("--exchanges", default="binance,bybit,okx,deribit")
    scan_p.add_argument("--json", action="store_true")

    watch_p = sub.add_parser("watch", help="Repeated scan on an interval")
    watch_p.add_argument("symbols", nargs="+")
    watch_p.add_argument("--exchanges", default="binance,bybit,okx,deribit")
    watch_p.add_argument("--interval", type=int, default=30)
    watch_p.add_argument("--json", action="store_true")

    args = parser.parse_args()
    exchanges = [e.strip() for e in args.exchanges.split(",") if e.strip() in FETCHERS]
    symbols = [s.upper() for s in args.symbols]

    if args.command == "scan":
        results = scan(symbols, exchanges)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_table(results)
    elif args.command == "watch":
        try:
            while True:
                results = scan(symbols, exchanges)
                if args.json:
                    print(json.dumps(results))
                else:
                    print(f"\n=== {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
                    print_table(results)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
