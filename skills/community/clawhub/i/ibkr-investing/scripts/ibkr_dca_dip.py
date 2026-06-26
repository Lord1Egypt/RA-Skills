#!/usr/bin/env python3
"""Drawdown-triggered DCA-the-dip helper for the IBKR reserve allocation.

Mirrors okx_dca_dip.py: compares current NAV against the all-time high seen
across ~/.aeon/ibkr/snapshots/*.json. When drawdown crosses --threshold-pct,
recommends deploying a slice of the reserve as an additional buy proposal on
the configured target symbol (default VOO).

Does NOT place any orders — only observes and prints a recommendation.
The agent reads the output and (if status == 'trigger') calls
ibkr_propose_trade.py with the recommended size, then waits for user YES.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from _audit import append as audit_append
from _ibkr_client import connect, env_summary

ROOT = Path(os.path.expanduser("~/.aeon/ibkr"))
SNAPSHOT_DIR = ROOT / "snapshots"
STATE_FILE = ROOT / "dca_dip_state.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _current_nav() -> float:
    ib = connect()
    try:
        for av in ib.accountValues():
            if av.tag == "NetLiquidation" and av.currency == "BASE":
                return float(av.value)
    finally:
        ib.disconnect()
    raise RuntimeError("Could not read NAV from IBKR")


def _historical_ath() -> tuple[float, str | None]:
    if not SNAPSHOT_DIR.exists():
        return 0.0, None
    best = 0.0
    best_iso: str | None = None
    for path in sorted(SNAPSHOT_DIR.glob("*.json")):
        try:
            snap = json.loads(path.read_text())
        except Exception:
            continue
        nav = float((snap.get("account") or {}).get("nav") or 0)
        if nav > best:
            best = nav
            best_iso = snap.get("timestamp") or snap.get("date_utc")
    return best, best_iso


def _load_state() -> dict:
    if not STATE_FILE.exists():
        return {"ath_usd": 0.0, "ath_seen_iso": None, "triggers": []}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {"ath_usd": 0.0, "ath_seen_iso": None, "triggers": []}


def _save_state(state: dict) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))
    os.chmod(STATE_FILE, 0o600)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--reserve-usd", type=float, required=True)
    p.add_argument("--threshold-pct", type=float, default=0.30)
    p.add_argument("--max-triggers", type=int, default=3)
    p.add_argument("--rearm-pct", type=float, default=0.05)
    p.add_argument("--symbol", default="VOO", help="Target symbol for the dip-buy. Default VOO.")
    p.add_argument("--record-trigger", action="store_true",
                   help="Internal: persist this trigger as fired. Use only after the user-confirmed YES has produced a successful execute.")
    args = p.parse_args()

    if args.reserve_usd <= 0:
        print("--reserve-usd must be positive", file=sys.stderr)
        return 2

    try:
        current = _current_nav()
    except Exception as e:
        print(f"Could not read NAV: {e}", file=sys.stderr)
        return 1

    snap_ath, snap_iso = _historical_ath()
    state = _load_state()
    stored_ath = float(state.get("ath_usd") or 0)

    ath = max(stored_ath, snap_ath, current)
    ath_iso = state.get("ath_seen_iso") or snap_iso or _now_iso()
    if current > stored_ath and current >= snap_ath:
        ath_iso = _now_iso()
    state["ath_usd"] = ath
    state["ath_seen_iso"] = ath_iso

    drawdown_pct = (ath - current) / ath if ath > 0 else 0.0
    triggers: list[dict] = state.get("triggers") or []

    if drawdown_pct < args.rearm_pct and triggers:
        triggers = []
        state["triggers"] = triggers

    print(env_summary())
    print(f"ATH NAV:       ${ath:.2f}  (seen {ath_iso})")
    print(f"Current:       ${current:.2f}")
    print(f"Drawdown:      {drawdown_pct*100:.2f}% (threshold {args.threshold_pct*100:.1f}%)")
    print(f"Triggers used: {len(triggers)} / {args.max_triggers}")

    if drawdown_pct < args.threshold_pct:
        print("Status:        no_trigger")
        _save_state(state)
        return 0

    if len(triggers) >= args.max_triggers:
        print("Status:        exhausted")
        _save_state(state)
        return 0

    last_dd = float(triggers[-1].get("drawdown_pct") or 0) if triggers else 0.0
    if last_dd > 0 and (drawdown_pct - last_dd) < args.rearm_pct:
        print("Status:        no_trigger")
        print(f"NOTE: already fired at {last_dd*100:.2f}% drawdown; needs +{args.rearm_pct*100:.1f}% to re-arm.")
        _save_state(state)
        return 0

    remaining = args.max_triggers - len(triggers)
    used_already = sum(float(t.get("size_usd") or 0) for t in triggers)
    remaining_reserve = max(0.0, args.reserve_usd - used_already)
    if remaining_reserve <= 0:
        print("Status:        exhausted")
        _save_state(state)
        return 0
    size_usd = round(remaining_reserve / remaining, 2)

    print(f"Status:        trigger")
    print(f"Recommended buy: ${size_usd:.2f} of {args.symbol}")
    print()
    print(f"To act on this, the agent should call:")
    print(f"  ibkr_propose_trade.py --symbol {args.symbol} --side BUY --quote-sz {size_usd}")
    print(f"After user YES + execute, persist with --record-trigger.")

    audit_append(
        "drawdown_trigger",
        symbol=args.symbol,
        size_usd=size_usd,
        drawdown_pct=round(drawdown_pct, 6),
        ath=round(ath, 4),
        recorded=bool(args.record_trigger),
    )

    if args.record_trigger:
        triggers.append({
            "ts_iso": _now_iso(),
            "drawdown_pct": round(drawdown_pct, 6),
            "ath_usd": round(ath, 4),
            "size_usd": size_usd,
            "symbol": args.symbol,
        })
        state["triggers"] = triggers
        print(f"\nRecorded trigger {len(triggers)}/{args.max_triggers}.")

    _save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
