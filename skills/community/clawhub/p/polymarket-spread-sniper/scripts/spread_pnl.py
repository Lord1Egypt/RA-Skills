#!/usr/bin/env python3
"""
Spread Sniper P&L tracker.

Queries Simmer SIM venue for spread sniper positions and portfolio stats.
Appends a snapshot to spread_pnl.log on each run (used by cron).

Usage:
    python scripts/spread_pnl.py              # snapshot + print summary
    python scripts/spread_pnl.py --positions  # show open positions detail
    python scripts/spread_pnl.py --history    # print log history
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

SKILL_SOURCE = "sdk:spreadsniper"
LOG_FILE = Path(__file__).parent.parent.parent / "spread_pnl.log"


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


def fetch_resolved_pnl(api_key):
    """Fetch resolved spreadsniper positions via raw API for true realized P&L."""
    try:
        resp = requests.get(
            "https://api.simmer.markets/api/sdk/positions",
            params={"status": "resolved", "venue": "sim", "source": SKILL_SOURCE},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15,
        )
        resp.raise_for_status()
        positions = resp.json().get("positions", [])
        total = sum(p.get("pnl", 0) for p in positions)
        wins = len([p for p in positions if p.get("pnl", 0) > 0])
        return round(total, 2), len(positions), wins
    except Exception:
        return None, 0, 0


def get_stats(client):
    _load_env()
    api_key = os.environ.get("SIMMER_API_KEY", "")

    portfolio = client.get_portfolio()
    positions = client.get_positions(source=SKILL_SOURCE)  # active only

    sim = portfolio.get("sim", {})
    sim_pnl = sim.get("pnl", 0.0)
    sim_balance = sim.get("balance", 0.0)
    redeemable_count = portfolio.get("redeemable_count", 0)

    open_positions = []
    for p in positions:
        side = "NO" if p.shares_no > p.shares_yes else "YES"
        shares = p.shares_no if side == "NO" else p.shares_yes
        open_positions.append({
            "market_id": p.market_id,
            "question": p.question,
            "side": side,
            "shares": round(shares, 2),
            "avg_cost": round(p.avg_cost, 4) if p.avg_cost is not None else None,
            "current_price": round(p.current_price, 4) if p.current_price is not None else None,
            "cost_basis": round(p.cost_basis, 2) if p.cost_basis is not None else None,
            "current_value": round(p.current_value, 2),
            "pnl": round(p.pnl, 2),
            "status": p.status,
        })

    total_open_cost = sum(p["cost_basis"] or 0 for p in open_positions)
    total_open_value = sum(p["current_value"] for p in open_positions)
    unrealized_pnl = total_open_value - total_open_cost

    # True realized P&L from resolved positions (raw API — SDK misses these)
    realized_pnl, resolved_count, resolved_wins = fetch_resolved_pnl(api_key)

    return {
        "ts": datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "sim_balance": round(sim_balance, 2),
        "sim_pnl_total": round(sim_pnl, 2),
        "realized_pnl": realized_pnl,
        "unrealized_pnl": round(unrealized_pnl, 2),
        "redeemable_count": redeemable_count,
        "resolved_count": resolved_count,
        "resolved_wins": resolved_wins,
        "open_count": len(open_positions),
        "open_cost": round(total_open_cost, 2),
        "positions": open_positions,
    }


def print_summary(stats):
    resolved_count = stats.get("resolved_count", 0)
    resolved_wins  = stats.get("resolved_wins", 0)
    wr = f"{resolved_wins}/{resolved_count} WR={resolved_wins/resolved_count*100:.0f}%" if resolved_count else "n/a"
    realized = stats["realized_pnl"]
    realized_str = f"${realized:+.2f}" if realized is not None else "n/a (fetch failed)"
    print(f"\n{'='*56}")
    print(f"  SPREAD SNIPER P&L  ({stats['ts']})")
    print(f"{'='*56}")
    print(f"  SIM balance:       ${stats['sim_balance']:,.2f}")
    print(f"  SIM total P&L:     ${stats['sim_pnl_total']:+.2f}  (all sources)")
    print(f"  ── spreadsniper ──────────────────────────")
    print(f"  Realized P&L:      {realized_str}  ({wr}  {resolved_count} resolved)")
    print(f"  Unrealized P&L:    ${stats['unrealized_pnl']:+.2f}")
    print(f"  Open positions:    {stats['open_count']}  (${stats['open_cost']:.2f} at cost)")
    print(f"{'='*56}")


def print_positions(stats):
    print_summary(stats)
    if not stats["positions"]:
        print("  No open positions.")
        return
    print(f"\n  OPEN POSITIONS")
    print(f"  {'-'*50}")
    for p in stats["positions"]:
        avg_cost = p["avg_cost"] or 0.0
        cur_price = p["current_price"] or 0.0
        move = cur_price - avg_cost
        print(f"  [{p['side']}] {p['question'][:52]}")
        print(f"       {p['shares']} sh | entry={avg_cost:.3f} now={cur_price:.3f} move={move:+.3f}")
        print(f"       cost=${p['cost_basis']:.2f} | value=${p['current_value']:.2f} | pnl=${p['pnl']:+.2f}")


def append_log(stats):
    snapshot = {k: v for k, v in stats.items() if k != "positions"}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(snapshot) + "\n")


def print_history():
    if not LOG_FILE.exists():
        print("No log file yet.")
        return
    lines = LOG_FILE.read_text().strip().splitlines()
    if not lines:
        print("Log is empty.")
        return
    print(f"\n{'='*72}")
    print(f"  SPREAD SNIPER HISTORY  ({len(lines)} snapshots)")
    print(f"{'='*72}")
    print(f"  {'Timestamp':<22} {'Total P&L':>10} {'Realized':>10} {'Unrealized':>11} {'Open':>5} {'Rdm':>5}")
    print(f"  {'-'*66}")
    for line in lines:
        try:
            s = json.loads(line)
            rdm = s.get("redeemable_count", "-")
            print(f"  {s['ts']:<22} ${s['sim_pnl_total']:>+9.2f} ${s['realized_pnl']:>+9.2f} ${s['unrealized_pnl']:>+10.2f} {s['open_count']:>5} {rdm:>5}")
        except Exception:
            continue


def main():
    parser = argparse.ArgumentParser(description="Spread Sniper P&L tracker")
    parser.add_argument("--positions", action="store_true", help="Show open positions detail")
    parser.add_argument("--history", action="store_true", help="Print log history")
    parser.add_argument("--no-log", dest="no_log", action="store_true", help="Skip appending to log")
    args = parser.parse_args()

    if args.history:
        print_history()
        return

    client = get_client()
    stats = get_stats(client)

    if args.positions:
        print_positions(stats)
    else:
        print_summary(stats)

    if not args.no_log:
        append_log(stats)


if __name__ == "__main__":
    main()
