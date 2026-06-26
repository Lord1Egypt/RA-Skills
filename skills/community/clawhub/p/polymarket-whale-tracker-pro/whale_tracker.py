#!/usr/bin/env python3
"""
Polymarket Whale Tracker
=========================
Tracks top traders' open positions via Polygon on-chain data
and the Polymarket Data API.

Usage:
    python3 whale_tracker.py                    # Show top traders + positions
    python3 whale_tracker.py --watch            # Watch for new positions every 5min
    python3 whale_tracker.py --addr 0xABC...    # Track a specific address
"""

import requests
import json
import argparse
import time
from datetime import datetime

DATA_API  = "https://data-api.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"

KNOWN_WHALES = [
    # Add wallet addresses here as you discover good traders
    # {"name": "Whale1", "address": "0x..."},
]

def get_user_positions(address, min_size=10):
    """Fetch open positions for a wallet address."""
    try:
        r = requests.get(f"{DATA_API}/positions", params={
            "user": address,
            "sizeThreshold": min_size,
            "limit": 50,
        }, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data if isinstance(data, list) else data.get("data", [])
    except Exception as e:
        print(f"  Error fetching positions for {address}: {e}")
    return []

def get_user_trades(address, limit=20):
    """Fetch recent trades for a wallet."""
    try:
        r = requests.get(f"{DATA_API}/activity", params={
            "user": address,
            "limit": limit,
        }, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data if isinstance(data, list) else data.get("data", [])
    except Exception as e:
        pass
    return []

def get_leaderboard_addresses(limit=20, period="MONTH"):
    """Fetch top traders from the Data API leaderboard."""
    attempts = [
        f"/v1/leaderboard?timePeriod={period}&limit={limit}",
        f"/v1/leaderboard?timePeriod=ALL&limit={limit}",
        f"/v1/leaderboard?limit={limit}",
    ]
    for path in attempts:
        try:
            r = requests.get(f"{DATA_API}{path}", timeout=8)
            if r.status_code == 200:
                data = r.json()
                rows = data if isinstance(data, list) else data.get("data", [])
                if rows:
                    return rows, path
        except Exception:
            continue
    return [], None

def get_market_info(condition_id):
    """Look up market question from condition ID."""
    try:
        r = requests.get(f"{GAMMA_API}/markets", params={
            "conditionId": condition_id,
            "limit": 1
        }, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data:
                return data[0].get("question", condition_id)[:65]
    except Exception:
        pass
    return condition_id[:40]

def display_positions(name, address, positions):
    if not positions:
        print(f"  No open positions found.")
        return

    print(f"\n  {'Outcome':<8} {'Size':>10} {'Avg Price':>10} {'Curr Price':>10} {'PnL':>10}  Market")
    print(f"  {'-------':<8} {'----':>10} {'---------':>10} {'----------':>10} {'---':>10}  ------")
    for p in sorted(positions, key=lambda x: abs(float(x.get("size", 0) or 0)), reverse=True)[:15]:
        try:
            outcome = p.get("outcome", "?")[:6]
            size = float(p.get("size") or p.get("currentValue") or 0)
            avg_price = float(p.get("avgPrice") or p.get("averagePrice") or 0)
            curr_price = float(p.get("curPrice") or p.get("currentPrice") or p.get("price") or 0)
            pnl = (curr_price - avg_price) * size if avg_price and curr_price else 0
            market = p.get("title") or p.get("market") or p.get("conditionId", "")[:50]
            if not market or len(market) < 10:
                market = get_market_info(str(p.get("conditionId", "")))
            print(f"  {outcome:<8} {size:>10.2f} {avg_price:>10.3f} {curr_price:>10.3f} {pnl:>+10.2f}  {str(market)[:55]}")
        except Exception:
            continue

def main():
    parser = argparse.ArgumentParser(description="Polymarket Whale Tracker")
    parser.add_argument("--addr", help="Specific wallet address to track")
    parser.add_argument("--watch", action="store_true", help="Watch mode (refresh every 5 min)")
    parser.add_argument("--min-size", type=float, default=10, help="Min position size to show")
    args = parser.parse_args()

    def run():
        print("=" * 65)
        print("🐋  POLYMARKET WHALE TRACKER")
        print(f"    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 65)

        if args.addr:
            # Track a specific address
            print(f"\n📍 Tracking: {args.addr}")
            positions = get_user_positions(args.addr, min_size=args.min_size)
            trades = get_user_trades(args.addr)
            display_positions("Custom", args.addr, positions)

            if trades:
                print(f"\n  Recent trades:")
                for t in trades[:5]:
                    side = t.get("side", "?")
                    size = float(t.get("size") or 0)
                    price = float(t.get("price") or 0)
                    market = t.get("title") or t.get("market", "")[:50]
                    ts = t.get("timestamp") or t.get("createdAt", "")[:16]
                    print(f"  [{ts}] {side:>4} {size:.2f} @ {price:.3f}  {market}")
        else:
            # Try leaderboard first
            print("\n📊 Fetching top traders...")
            leaders, endpoint = get_leaderboard_addresses()

            if leaders:
                print(f"  Source: {DATA_API}{endpoint}")
                print(f"  Found {len(leaders)} traders\n")

                for i, w in enumerate(leaders[:10], 1):
                    name = (w.get("userName") or w.get("name") or w.get("pseudonym") or
                            w.get("proxyWallet") or w.get("address") or "?")[:25]
                    address = (w.get("proxyWallet") or w.get("address") or "")
                    pnl = float(w.get("pnl") or w.get("profit") or 0)
                    vol = float(w.get("vol") or w.get("volume") or 0)

                    print(f"\n{'━'*55}")
                    print(f"  #{i} {name}  |  PnL: ${pnl:+,.2f}  |  Vol: ${vol:,.2f}")
                    if address:
                        print(f"  Address: {address}")
                        print(f"  → https://polymarket.com/profile/{address}")
                        positions = get_user_positions(address, min_size=args.min_size)
                        display_positions(name, address, positions)
                    else:
                        print("  (no address in API response)")

            elif KNOWN_WHALES:
                print("  Leaderboard API unavailable — using known whale list\n")
                for whale in KNOWN_WHALES:
                    print(f"\n{'━'*55}")
                    print(f"  🐋 {whale['name']} | {whale['address']}")
                    positions = get_user_positions(whale["address"], min_size=args.min_size)
                    display_positions(whale["name"], whale["address"], positions)
            else:
                print("\n  ⚠️  No leaderboard data + no known whale addresses.")
                print("  Options:")
                print("  1. Visit https://polymarket.com/leaderboard")
                print("  2. Copy wallet addresses, add to KNOWN_WHALES in this file")
                print("  3. Run: python3 whale_tracker.py --addr 0xYOUR_ADDRESS")

        print("\n" + "=" * 65)

    if args.watch:
        print("👁️  Watch mode — refreshing every 5 minutes. Ctrl+C to stop.\n")
        while True:
            run()
            print(f"\n  💤 Next refresh in 5 min...\n")
            time.sleep(300)
    else:
        run()

if __name__ == "__main__":
    main()
