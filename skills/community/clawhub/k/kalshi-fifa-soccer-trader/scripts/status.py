#!/usr/bin/env python3
"""Check Kalshi FIFA soccer positions and portfolio balance."""

import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from soccer_trader import get_client, get_portfolio, get_positions, TRADE_SOURCE

def main():
    parser = argparse.ArgumentParser(description="Kalshi FIFA Soccer Trader — Status")
    parser.add_argument("--positions", action="store_true", help="Show open positions")
    parser.add_argument("--pnl",       action="store_true", help="Show P&L summary")
    parser.add_argument("--all",       action="store_true", help="Show all positions (not just this skill's)")
    args = parser.parse_args()

    portfolio = get_portfolio()
    balance = portfolio.get("balance_usd") or portfolio.get("usdc_balance") or 0
    print(f"\nBalance: ${balance:.2f} USDC")

    if args.positions or args.pnl or not any(vars(args).values()):
        positions = get_positions()
        mine = [p for p in positions if p.get("source") == TRADE_SOURCE] if not args.all else positions
        print(f"\nOpen positions ({'all' if args.all else 'this skill'}): {len(mine)}")
        for p in mine:
            market_id = p.get("market_id") or p.get("id") or "?"
            shares    = p.get("shares") or p.get("quantity") or 0
            avg_price = p.get("avg_price") or p.get("entry_price") or 0
            cur_price = p.get("current_price") or p.get("yes_price") or 0
            pnl       = (cur_price - avg_price) * shares
            print(f"  {market_id[:40]:<40}  {shares:6.1f}sh  avg={avg_price:.2f}  cur={cur_price:.2f}  P&L={pnl:+.2f}")

if __name__ == "__main__":
    main()
