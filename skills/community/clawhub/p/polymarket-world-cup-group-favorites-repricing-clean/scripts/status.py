#!/usr/bin/env python3
"""
Simmer Account Status

Shows wallet balance, positions, and recent activity.
"""

import argparse
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.stdout.reconfigure(line_buffering=True)
SIMMER_API_BASE = "https://api.simmer.markets"


def api_request(api_key: str, endpoint: str) -> dict:
    url = f"{SIMMER_API_BASE}{endpoint}"
    req = Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    })
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API Error {e.code}: {error_body}")
        sys.exit(1)
    except URLError as e:
        print(f"Connection error: {e.reason}")
        sys.exit(1)


def format_usd(amount: float) -> str:
    return f"${amount:,.2f}"


def main():
    parser = argparse.ArgumentParser(description="Check Simmer account status")
    parser.add_argument("--positions", action="store_true", help="Show detailed positions")
    args = parser.parse_args()

    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("SIMMER_API_KEY environment variable not set")
        sys.exit(1)

    print("Fetching account status...\n")
    portfolio = api_request(api_key, "/api/sdk/portfolio")

    balance = portfolio.get("balance_usdc", 0)
    exposure = portfolio.get("total_exposure", 0)
    positions_count = portfolio.get("positions_count", 0)

    print("=" * 50)
    print("ACCOUNT SUMMARY")
    print("=" * 50)
    print(f"  Available Balance:  {format_usd(balance)}")
    print(f"  Total Exposure:     {format_usd(exposure)}")
    print(f"  Open Positions:     {positions_count}")
    print("=" * 50)

    if args.positions:
        print("\nOPEN POSITIONS")
        print("=" * 50)
        result = api_request(api_key, "/api/sdk/positions")
        positions = result.get("positions", []) if isinstance(result, dict) else result
        if not positions:
            print("  No open positions")
        else:
            for pos in positions:
                question = pos.get("question", "Unknown")
                if len(question) > 50:
                    question = question[:47] + "..."
                shares_yes = pos.get("shares_yes", 0)
                shares_no = pos.get("shares_no", 0)
                pnl = pos.get("pnl", 0)
                if shares_yes > 0:
                    side, shares = "YES", shares_yes
                elif shares_no > 0:
                    side, shares = "NO", shares_no
                else:
                    continue
                print(f"\n  {question}")
                print(f"    {side}: {shares:.2f} shares | PnL: {format_usd(pnl)}")
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
