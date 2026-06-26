#!/usr/bin/env python3
"""
sim_redeem.py — Redeem resolved SIM positions and report true P&L.

Simmer's SDK get_positions() only returns active positions. Resolved positions
sit at ?status=resolved and are never surfaced by the tracker, so realized P&L
stays at zero until this script is run.

For SIM: redemption is server-side (no on-chain tx). client.redeem() tells
Simmer to settle the P&L into the SIM account balance.
For polymarket: redemption is on-chain via the CTF contract.

Usage:
    python scripts/sim_redeem.py              # show resolved P&L (no redemption)
    python scripts/sim_redeem.py --live       # redeem all resolved SIM positions
    python scripts/sim_redeem.py --source sdk:spreadsniper   # filter by source

Cron (every 15 min):
    */15 * * * * source ~/.openclaw/workspace/.env && \\
        python3 ~/.openclaw/workspace/skills/polymarket-spread-sniper/scripts/sim_redeem.py --live \\
        >> ~/.openclaw/workspace/skills/sim_redeem.log 2>&1
"""

import os
import sys
import json
import argparse
import time
import requests
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

BASE_URL = "https://api.simmer.markets"


def _load_env():
    env_path = Path(__file__).resolve().parents[4] / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get_client():
    _load_env()
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("Error: SIMMER_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    from simmer_sdk import SimmerClient
    return SimmerClient(api_key=api_key, venue="sim")


def fetch_resolved(api_key, venue="sim", source=None):
    """Fetch resolved positions via raw API (not exposed by SDK)."""
    params = {"status": "resolved", "venue": venue}
    if source:
        params["source"] = source
    resp = requests.get(
        f"{BASE_URL}/api/sdk/positions",
        params=params,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("positions", [])


def print_pnl_summary(positions, label=""):
    wins = [p for p in positions if p.get("pnl", 0) > 0]
    losses = [p for p in positions if p.get("pnl", 0) <= 0]
    win_pnl = sum(p["pnl"] for p in wins)
    loss_pnl = sum(p["pnl"] for p in losses)
    net = win_pnl + loss_pnl
    wr = len(wins) / len(positions) * 100 if positions else 0
    print(f"\n{'='*56}")
    if label:
        print(f"  {label}")
    print(f"  Resolved positions: {len(positions)}")
    print(f"  Wins:  {len(wins):3d}  P&L: ${win_pnl:+.2f}")
    print(f"  Losses:{len(losses):3d}  P&L: ${loss_pnl:+.2f}")
    print(f"  Net:         ${net:+.2f}   WR: {wr:.1f}%")
    print(f"{'='*56}")


def main():
    parser = argparse.ArgumentParser(description="Redeem resolved SIM positions")
    parser.add_argument("--live", action="store_true", help="Execute redemptions")
    parser.add_argument("--source", default=None, help="Filter by source (e.g. sdk:spreadsniper)")
    parser.add_argument("--verbose", action="store_true", help="Print each position")
    args = parser.parse_args()

    _load_env()
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("Error: SIMMER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"[{ts}] Fetching resolved SIM positions...")

    positions = fetch_resolved(api_key, venue="sim", source=args.source)
    print(f"Found {len(positions)} resolved positions" + (f" (source={args.source})" if args.source else ""))

    if not positions:
        print("Nothing to redeem.")
        return

    print_pnl_summary(positions, label=f"Source: {args.source or 'all'}")

    if args.verbose:
        print("\nDetail:")
        for p in sorted(positions, key=lambda x: x.get("pnl", 0)):
            side = "YES" if p.get("shares_yes", 0) > p.get("shares_no", 0) else "NO"
            pnl = p.get("pnl", 0)
            print(f"  {'WIN ' if pnl>0 else 'LOSS'}  ${pnl:+6.2f}  [{side}]  {p.get('question','?')[:55]}")

    if not args.live:
        print("\n[DRY RUN — pass --live to redeem and settle P&L]")
        return

    # Redeem — for SIM this is a server-side settlement call
    client = get_client()
    ok = failed = 0
    for p in positions:
        market_id = p["market_id"]
        side = "yes" if p.get("shares_yes", 0) > p.get("shares_no", 0) else "no"
        try:
            result = client.redeem(market_id, side)
            if result.get("success"):
                ok += 1
            else:
                failed += 1
                if args.verbose:
                    print(f"  ❌ {market_id}: {result.get('error','?')}")
        except Exception as e:
            failed += 1
            if args.verbose:
                print(f"  ❌ {market_id}: {e}")
        time.sleep(0.2)

    print(f"\n{ok}/{len(positions)} redeemed  |  {failed} failed")

    # Show updated P&L after redemptions
    portfolio = client.get_portfolio()
    sim = portfolio.get("sim", {})
    print(f"Updated SIM P&L: ${sim.get('pnl', 0):+.2f}  balance: ${sim.get('balance', 0):,.2f}")
    pnl_real = client.get_total_pnl()
    print(f"get_total_pnl(): ${pnl_real:+.2f}")


if __name__ == "__main__":
    main()
