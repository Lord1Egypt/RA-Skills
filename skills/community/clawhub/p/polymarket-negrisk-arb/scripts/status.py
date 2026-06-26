#!/usr/bin/env python3
"""Portfolio status for NegRisk Arbitrage Trader."""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    from simmer_sdk import SimmerClient
except ImportError:
    print("❌ simmer-sdk not installed. Run: pip install simmer-sdk")
    sys.exit(1)

LEDGER_FILE = Path(__file__).parent.parent / "negrisk_ledger.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--positions", action="store_true", help="Show open positions")
    args = parser.parse_args()

    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("❌ SIMMER_API_KEY not set")
        sys.exit(1)

    client = SimmerClient(api_key=api_key)

    # Portfolio
    try:
        portfolio = client.get_portfolio()
        print(f"\n💼 Portfolio")
        print(f"{'='*40}")
        print(f"  USDC Balance:  ${portfolio.get('balance_usdc', 0):.2f}")
        print(f"  SIM Balance:   {portfolio.get('sim_balance', 0):.0f} $SIM")
        print(f"  Positions:     {portfolio.get('positions_count', 0)}")
        print(f"  Total PnL:     ${portfolio.get('pnl_total', 0):.2f}")
    except Exception as e:
        print(f"❌ Portfolio fetch failed: {e}")

    # NegRisk positions
    if args.positions:
        try:
            data = client.get_positions()
            negrisk_positions = [
                p for p in data.get("positions", [])
                if "negrisk-arb" in str(p.get("source", ""))
            ]

            if negrisk_positions:
                print(f"\n🔢 NegRisk Arbitrage Positions ({len(negrisk_positions)})")
                print(f"{'='*40}")
                for p in negrisk_positions:
                    pnl = p.get("pnl", 0)
                    pnl_str = f"+${pnl:.2f}" if pnl >= 0 else f"-${abs(pnl):.2f}"
                    print(f"  {p['question'][:45]:45s} {pnl_str}")
            else:
                print(f"\n  No NegRisk positions found.")
        except Exception as e:
            print(f"❌ Positions fetch failed: {e}")

    # Ledger summary
    if LEDGER_FILE.exists():
        try:
            ledger = json.loads(LEDGER_FILE.read_text())
            trades = ledger.get("trades", [])
            if trades:
                total_cost = sum(t.get("cost", 0) for t in trades)
                total_expected = sum(t.get("expected_profit", 0) for t in trades)
                print(f"\n📒 Ledger Summary")
                print(f"{'='*40}")
                print(f"  Total events:    {len(trades)}")
                print(f"  Total invested:  ${total_cost:.2f}")
                print(f"  Expected profit: ${total_expected:.2f}")
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                today_spend = ledger.get("daily_spend", {}).get(today, 0)
                print(f"  Today's spend:   ${today_spend:.2f}")
        except Exception:
            pass


if __name__ == "__main__":
    main()
