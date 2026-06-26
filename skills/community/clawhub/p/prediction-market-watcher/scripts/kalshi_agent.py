#!/usr/bin/env python3
"""
kalshi_agent.py — Main Kalshi trading agent for Quirk/Katie

Usage:
  python3 kalshi_agent.py --status          # Portfolio + risk summary
  python3 kalshi_agent.py --scan            # Scan markets, show top opportunities
  python3 kalshi_agent.py --run             # Scan + auto-place bets (live mode)
  python3 kalshi_agent.py --demo            # Same but demo account
  python3 kalshi_agent.py --positions       # Show open positions
  python3 kalshi_agent.py --history         # Recent fills/settlements

Requires env vars or config:
  KALSHI_KEY_ID       — API key ID from Kalshi account settings
  KALSHI_KEY_FILE     — Path to RSA private key .key file
"""

import argparse
import json
import os
import sys
from datetime import datetime

from kalshi_client import KalshiClient
from analyzer import rank_markets, format_market_report, score_market
from risk import get_state, can_bet, size_bet, record_bet, risk_summary, daily_remaining_cents

# ── Config ────────────────────────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def get_client(demo: bool = False) -> KalshiClient:
    cfg = load_config()
    key_id = os.environ.get("KALSHI_KEY_ID") or cfg.get("key_id")
    key_file = os.environ.get("KALSHI_KEY_FILE") or cfg.get("key_file")

    if not key_id or not key_file:
        print("❌ Missing credentials.")
        print("   Set KALSHI_KEY_ID and KALSHI_KEY_FILE env vars,")
        print("   or create kalshi-agent/config.json with {key_id, key_file}")
        sys.exit(1)

    if not os.path.exists(key_file):
        print(f"❌ Key file not found: {key_file}")
        sys.exit(1)

    return KalshiClient(key_id=key_id, private_key_path=key_file, demo=demo)


# ── Commands ──────────────────────────────────────────────────────────────

def cmd_status(demo: bool):
    client = get_client(demo)
    state = get_state()

    print("=" * 55)
    print(f"  KALSHI AGENT — {'DEMO' if demo else 'LIVE'} MODE")
    print(f"  {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 55)

    try:
        bal = client.get_balance()
        balance_cents = bal.get("balance", 0)
        pv = bal.get("portfolio_value", 0)
        print(f"\n💰 Account Balance:   ${balance_cents/100:.2f}")
        print(f"📊 Portfolio Value:   ${pv/100:.2f}")
    except Exception as e:
        print(f"⚠️  Balance fetch failed: {e}")

    print(f"\n📋 Risk State:")
    for line in risk_summary(state).splitlines():
        print(f"   {line}")
    print()


def cmd_scan(demo: bool, auto_bet: bool = False):
    client = get_client(demo)
    state = get_state()

    print(f"\n🔍 Scanning Kalshi markets ({'DEMO' if demo else 'LIVE'})...\n")

    # Fetch open markets
    all_markets = []
    try:
        cursor = None
        for _ in range(3):  # max 3 pages
            resp = client.get_markets(status="open", limit=100, cursor=cursor)
            markets = resp.get("markets", [])
            all_markets.extend(markets)
            cursor = resp.get("cursor")
            if not cursor or not markets:
                break
        print(f"   Fetched {len(all_markets)} open markets\n")
    except Exception as e:
        print(f"❌ Failed to fetch markets: {e}")
        return

    if not all_markets:
        print("No open markets found.")
        return

    # Rank them
    top = rank_markets(all_markets, top_n=10)
    print(format_market_report(top))

    if not auto_bet:
        return

    # Auto-bet mode
    print("\n🤖 AUTO-BET MODE — evaluating top opportunities...\n")
    
    try:
        bal = client.get_balance()
        balance_cents = bal.get("balance", 0)
    except Exception as e:
        print(f"❌ Cannot fetch balance: {e}")
        return

    remaining = daily_remaining_cents(state)
    if remaining <= 0:
        print("⛔ Daily budget exhausted. No bets placed.")
        return

    bets_placed = 0
    for market in top[:3]:  # max 3 auto-bets per run
        if market["confidence"] not in ("high", "medium"):
            continue
        if not market.get("recommended_side"):
            continue

        side = market["recommended_side"]
        price = market["recommended_price"]

        if not price or price <= 0:
            continue

        bet_cents = size_bet(
            balance_cents=balance_cents,
            confidence=market["confidence"],
            price_cents=price,
        )

        allowed, reason = can_bet(state, bet_cents, market["confidence"])
        if not allowed:
            print(f"⛔ Skipping {market['ticker']}: {reason}")
            continue

        # Number of contracts we can afford
        contracts = max(1, bet_cents // price)
        actual_cost = contracts * price

        print(f"📌 Placing bet:")
        print(f"   Market: {market['title']}")
        print(f"   Side: {side.upper()} @ {price}¢ × {contracts} contracts = ${actual_cost/100:.2f}")

        try:
            order = client.create_order(
                ticker=market["ticker"],
                side=side,
                action="buy",
                count=contracts,
                limit_price=price,
            )
            order_id = order.get("order", {}).get("order_id", "unknown")
            record_bet(state, market["ticker"], side, actual_cost, order_id)
            print(f"   ✅ Order placed! ID: {order_id}")
            bets_placed += 1
        except Exception as e:
            print(f"   ❌ Order failed: {e}")

    if bets_placed == 0:
        print("No bets placed this run.")
    else:
        print(f"\n✅ {bets_placed} bet(s) placed. Updated risk state saved.")


def cmd_positions(demo: bool):
    client = get_client(demo)
    state = get_state()

    print("\n📊 Open Positions\n")

    # From API
    try:
        resp = client.get_positions()
        positions = resp.get("market_positions", [])
        if not positions:
            print("  No open positions on Kalshi.")
        else:
            for p in positions:
                ticker = p.get("market_ticker", "?")
                pos = p.get("position", 0)
                value = p.get("market_exposure", 0)
                resting = p.get("resting_orders_count", 0)
                print(f"  {ticker}: position={pos}, exposure=${value/100:.2f}, resting={resting}")
    except Exception as e:
        print(f"  ⚠️ API error: {e}")

    # From local state
    local = state.get("open_positions", [])
    if local:
        print(f"\n📋 Local tracked ({len(local)}):")
        for p in local:
            placed = p.get("placed_at", "?")[:10]
            print(f"  [{placed}] {p['ticker']} — {p['side'].upper()} — ${p['amount_cents']/100:.2f} — ID: {p['order_id']}")


def cmd_history(demo: bool):
    client = get_client(demo)

    print("\n📜 Recent Fills\n")
    try:
        resp = client.get_fills(limit=20)
        fills = resp.get("fills", [])
        if not fills:
            print("  No fills yet.")
        else:
            for f in fills:
                ticker = f.get("market_ticker", "?")
                side = f.get("side", "?")
                price = f.get("yes_price" if side == "yes" else "no_price", 0)
                count = f.get("count", 0)
                ts = f.get("created_time", "?")[:10]
                print(f"  [{ts}] {ticker} — {side.upper()} × {count} @ {price}¢")
    except Exception as e:
        print(f"  ⚠️ API error: {e}")


# ── Entry Point ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Quirk's Kalshi Trading Agent")
    parser.add_argument("--status", action="store_true", help="Show portfolio + risk summary")
    parser.add_argument("--scan", action="store_true", help="Scan and rank markets")
    parser.add_argument("--run", action="store_true", help="Scan + auto-place bets (LIVE)")
    parser.add_argument("--positions", action="store_true", help="Show open positions")
    parser.add_argument("--history", action="store_true", help="Show recent fills")
    parser.add_argument("--demo", action="store_true", help="Use demo environment")
    args = parser.parse_args()

    if args.status:
        cmd_status(demo=args.demo)
    elif args.scan:
        cmd_scan(demo=args.demo, auto_bet=False)
    elif args.run:
        cmd_scan(demo=args.demo, auto_bet=True)
    elif args.positions:
        cmd_positions(demo=args.demo)
    elif args.history:
        cmd_history(demo=args.demo)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
