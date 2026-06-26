#!/usr/bin/env python3
"""
Quick status for MTF Momentum skill.
Shows active positions and recent signals.
"""

import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

SIMMER_API_URL = os.environ.get("SIMMER_API_URL", "https://api.simmer.markets")
TRADE_SOURCE = "sdk:sol-mtf-momentum"
ASSET = "SOL"


def main():
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("❌ SIMMER_API_KEY not set")
        sys.exit(1)

    try:
        from simmer_sdk import SimmerClient
        client = SimmerClient(api_key=api_key, venue=os.environ.get("TRADING_VENUE", "sim"))

        # Portfolio
        portfolio = client.get_portfolio()
        balance = portfolio.get("balance_usdc", 0) if portfolio else 0

        # Positions
        from dataclasses import asdict
        positions = [asdict(p) for p in client.get_positions()]
        my_positions = [p for p in positions if TRADE_SOURCE in (p.get("sources") or [])]

        active = [p for p in my_positions if p.get("status") == "active"]
        resolved = [p for p in my_positions if p.get("status") == "resolved"]

        total_pnl = sum(p.get("pnl", 0) for p in my_positions)

        print()
        print(f"⚡ {ASSET} 5m MTF MOMENTUM STATUS")
        print("=" * 45)
        print(f"  Balance:           ${balance:.2f}")
        print(f"  Active positions:  {len(active)}")
        print(f"  Resolved:          {len(resolved)}")
        print(f"  Total PnL:         ${total_pnl:+.2f}")
        print("=" * 45)

        if active:
            print(f"\n  📊 Active Positions:")
            for p in active:
                q = (p.get("question") or "")[:50]
                pnl = p.get("pnl", 0)
                price = p.get("current_price", 0)
                print(f"    {q}...")
                print(f"      Price: {price:.2f} | PnL: ${pnl:+.2f}")

        if resolved:
            wins = sum(1 for p in resolved if (p.get("pnl") or 0) > 0)
            losses = len(resolved) - wins
            wr = wins / len(resolved) * 100 if resolved else 0
            print(f"\n  📈 Win Rate: {wr:.0f}% ({wins}W / {losses}L)")

        print()

    except ImportError:
        print("❌ simmer-sdk not installed. Run: pip install simmer-sdk")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
