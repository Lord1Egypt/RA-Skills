#!/usr/bin/env python3
"""
monitor-positions.py — Check all tracked positions for maturity and generate alerts.

Usage:
  python3 monitor-positions.py [--positions-file data/positions.json] [--alert-hours 24]

Reads positions.json and for each active position:
  - Reports days remaining to maturity
  - Flags positions that have matured or will mature within --alert-hours
  - Fetches current market data from Pendle API for mark-to-market
  - Outputs a summary report
"""

import argparse, json, os, sys, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

API_BASE = "https://api-v2.pendle.finance/core"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  ⚠ API fetch failed: {e}", file=sys.stderr)
        return None


def fetch_market_data(chain_id, market_address):
    url = f"{API_BASE}/v2/{chain_id}/markets/{market_address}"
    return fetch_json(url)


def load_positions(path):
    p = Path(path)
    if not p.exists():
        return []
    with open(p) as f:
        return json.load(f)


def main():
    p = argparse.ArgumentParser(description="Monitor Pendle PT positions")
    p.add_argument("--positions-file", default="data/positions.json")
    p.add_argument("--alert-hours", type=int, default=24,
                   help="Alert if maturity within N hours")
    args = p.parse_args()

    positions = load_positions(args.positions_file)
    if not positions:
        print("No positions found.")
        return

    now = datetime.now(timezone.utc)
    alert_threshold = now + timedelta(hours=args.alert_hours)

    active = [p for p in positions if p.get("status") == "active"]
    matured_pending = []
    maturing_soon = []
    healthy = []

    total_deployed = 0
    total_expected_yield = 0

    print(f"=== Pendle PT Position Monitor ===")
    print(f"    Checked at: {now.isoformat()}")
    print(f"    Active positions: {len(active)}")
    print()

    for pos in active:
        mat_str = pos.get("maturity_date", "")
        if not mat_str:
            continue

        maturity = datetime.fromisoformat(mat_str.replace("Z", "+00:00"))
        days_left = (maturity - now).total_seconds() / 86400
        deposit = pos.get("deposit_amount_usd", 0)
        expected = pos.get("expected_value_at_maturity_usd", deposit)
        apy = pos.get("effective_apy_at_entry", 0)

        total_deployed += deposit
        total_expected_yield += (expected - deposit)

        elapsed_days = (now - datetime.fromisoformat(
            pos["entry_date"].replace("Z", "+00:00")
        )).total_seconds() / 86400
        total_hold_days = pos.get("days_to_maturity_at_entry", max(elapsed_days, 1))
        progress_pct = min(elapsed_days / total_hold_days * 100, 100) if total_hold_days > 0 else 0
        accrued_yield = (expected - deposit) * min(elapsed_days / total_hold_days, 1.0) if total_hold_days > 0 else 0

        entry = {
            "id": pos["id"],
            "market": pos.get("market_name", pos.get("market_address", "?")),
            "chain": pos.get("chain", "?"),
            "deposit_usd": deposit,
            "apy": apy,
            "days_left": round(days_left, 1),
            "maturity": mat_str,
            "progress_pct": round(progress_pct, 1),
            "accrued_yield_usd": round(accrued_yield, 2),
            "expected_total_yield_usd": round(expected - deposit, 2),
        }

        if maturity <= now:
            matured_pending.append(entry)
        elif maturity <= alert_threshold:
            maturing_soon.append(entry)
        else:
            healthy.append(entry)

    # --- Report ---
    if matured_pending:
        print("🔴 MATURED — Ready to redeem/roll:")
        for e in matured_pending:
            print(f"  • {e['market']} ({e['chain']})")
            print(f"    Deposited: ${e['deposit_usd']:,.2f} | APY: {e['apy']*100:.1f}%")
            print(f"    Matured: {e['maturity']}")
            print(f"    Expected yield: ${e['expected_total_yield_usd']:,.2f}")
            print()

    if maturing_soon:
        print(f"🟡 MATURING within {args.alert_hours}h:")
        for e in maturing_soon:
            print(f"  • {e['market']} ({e['chain']})")
            print(f"    Deposited: ${e['deposit_usd']:,.2f} | APY: {e['apy']*100:.1f}%")
            print(f"    Matures in: {e['days_left']} days ({e['maturity']})")
            print(f"    Accrued yield: ${e['accrued_yield_usd']:,.2f} / ${e['expected_total_yield_usd']:,.2f}")
            print()

    if healthy:
        print("🟢 ACTIVE — Holding:")
        for e in healthy:
            print(f"  • {e['market']} ({e['chain']})")
            print(f"    Deposited: ${e['deposit_usd']:,.2f} | APY: {e['apy']*100:.1f}%")
            print(f"    Days left: {e['days_left']} | Progress: {e['progress_pct']}%")
            print(f"    Accrued yield: ${e['accrued_yield_usd']:,.2f} / ${e['expected_total_yield_usd']:,.2f}")
            print()

    # --- Aggregate ---
    print("--- Aggregate ---")
    print(f"  Total deployed:        ${total_deployed:,.2f}")
    print(f"  Total expected yield:  ${total_expected_yield:,.2f}")
    if total_deployed > 0:
        wavg_apy = sum(
            p.get("effective_apy_at_entry", 0) * p.get("deposit_amount_usd", 0)
            for p in active
        ) / total_deployed
        print(f"  Weighted avg APY:      {wavg_apy*100:.2f}%")
    print(f"  Positions to redeem:   {len(matured_pending)}")
    print(f"  Positions maturing soon: {len(maturing_soon)}")

    # --- Rollover history ---
    all_rollovers = []
    for pos in positions:
        for ro in pos.get("rollover_history", []):
            all_rollovers.append(ro)
    if all_rollovers:
        total_realized = sum(r.get("realized_yield_usd", 0) for r in all_rollovers)
        print(f"\n--- Rollover History ---")
        print(f"  Total rollovers:       {len(all_rollovers)}")
        print(f"  Total realized yield:  ${total_realized:,.2f}")
        for ro in all_rollovers[-5:]:
            print(f"  • {ro.get('from_market','?')} → {ro.get('to_market','?')}")
            print(f"    Date: {ro.get('rollover_date','?')} | Yield: ${ro.get('realized_yield_usd',0):,.2f}")


if __name__ == "__main__":
    main()
