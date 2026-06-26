#!/usr/bin/env python3
"""Drawdown-triggered DCA-the-dip helper for the 70/20/10 strategy.

Compares current total equity against the all-time high (ATH) seen across
~/.aeon/okx/snapshots/*.json and emits a recommendation: when drawdown from
ATH crosses the threshold, recommend deploying a slice of the user's
reserve allocation as an additional buy proposal.

This script does NOT place any orders — it only observes and recommends.
The agent reads the output and (if status == 'trigger') calls
okx_propose_trade.py with the recommended quote size, then asks the user
to YES it.

Idempotency: state lives at ~/.aeon/okx/dca_dip_state.json so we don't
re-fire on every scheduled run during the same drawdown event. A trigger
re-arms when the drawdown has deepened by --rearm-pct since the last
trigger, OR when equity recovers to >=(1 - rearm_pct) * ATH.

Args:
    --reserve-usdt   Total reserve allocation, in USDT. Required.
    --threshold-pct  Drawdown level that fires a trigger. Default 0.30.
    --max-triggers   Maximum buys to deploy from the reserve. Default 3
                     (each trigger uses reserve / (max_triggers - used)).
    --rearm-pct      Drawdown delta needed to re-fire after a previous
                     trigger. Default 0.05 (5 percentage points).
    --instId         Asset to buy on dip. Default BTC-USDT.

Output (stdout, human-readable + a final structured line for the agent):
    Status:        no_trigger | trigger | exhausted
    ATH equity:    <usd>      (and when last seen)
    Current:       <usd>
    Drawdown:      <pct>
    Triggers used: N / max
    [if trigger] Recommended buy: <quote_sz_usdt> on <instId>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from _okx_client import account_api, env_summary

ROOT = Path(os.path.expanduser("~/.aeon/okx"))
SNAPSHOT_DIR = ROOT / "snapshots"
STATE_FILE = ROOT / "dca_dip_state.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _current_equity_usd() -> float:
    """Read OKX total equity (USD-est)."""
    bal = account_api().get_account_balance()
    if bal.get("code") != "0":
        raise RuntimeError(f"OKX balance error: {bal.get('msg')!r}")
    data = bal.get("data") or [{}]
    return float(data[0].get("totalEq") or 0)


def _historical_ath() -> tuple[float, str | None]:
    """Scan stored snapshots and return (max equity, iso of that snapshot)."""
    if not SNAPSHOT_DIR.exists():
        return 0.0, None
    best = 0.0
    best_iso: str | None = None
    for path in sorted(SNAPSHOT_DIR.glob("*.json")):
        try:
            snap = json.loads(path.read_text())
        except Exception:
            continue
        eq = float(snap.get("total_equity_usd") or 0)
        if eq > best:
            best = eq
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
    p.add_argument("--reserve-usdt", type=float, required=True,
                   help="Total reserve allocation in USDT (the '10%' bucket)")
    p.add_argument("--threshold-pct", type=float, default=0.30,
                   help="Drawdown level (0..1) to fire a trigger. Default 0.30 = 30%%.")
    p.add_argument("--max-triggers", type=int, default=3,
                   help="How many dip-buys to deploy from the reserve. Default 3.")
    p.add_argument("--rearm-pct", type=float, default=0.05,
                   help="Additional drawdown needed to re-fire after a prior trigger.")
    p.add_argument("--instId", default="BTC-USDT",
                   help="Asset to buy on dip. Default BTC-USDT.")
    p.add_argument("--record-trigger", action="store_true",
                   help="Internal: persist this trigger as fired. Use only after the agent's "
                        "user-confirmed YES has produced a successful execute.")
    args = p.parse_args()

    if args.reserve_usdt <= 0:
        print("--reserve-usdt must be positive", file=sys.stderr)
        return 2
    if not 0 < args.threshold_pct < 1:
        print("--threshold-pct must be in (0, 1)", file=sys.stderr)
        return 2
    if args.max_triggers < 1:
        print("--max-triggers must be >= 1", file=sys.stderr)
        return 2

    try:
        current = _current_equity_usd()
    except Exception as e:
        print(f"Could not read current equity: {e}", file=sys.stderr)
        return 1

    snap_ath, snap_iso = _historical_ath()
    state = _load_state()
    stored_ath = float(state.get("ath_usd") or 0)

    # ATH = max(stored, snapshot ATH, current). Refresh stored.
    ath = max(stored_ath, snap_ath, current)
    ath_iso = state.get("ath_seen_iso") or snap_iso or _now_iso()
    if current > stored_ath and current >= snap_ath:
        ath_iso = _now_iso()
    state["ath_usd"] = ath
    state["ath_seen_iso"] = ath_iso

    drawdown_pct = (ath - current) / ath if ath > 0 else 0.0
    triggers: list[dict] = state.get("triggers") or []

    # Re-arm: if equity recovered to within rearm_pct of ATH, clear the trigger
    # log so a fresh drawdown event starts a clean cycle.
    if drawdown_pct < args.rearm_pct and triggers:
        triggers = []
        state["triggers"] = triggers

    print(env_summary())
    print(f"ATH equity:    ${ath:.2f}  (seen {ath_iso})")
    print(f"Current:       ${current:.2f}")
    print(f"Drawdown:      {drawdown_pct*100:.2f}% (threshold {args.threshold_pct*100:.1f}%)")
    print(f"Triggers used: {len(triggers)} / {args.max_triggers}")

    if drawdown_pct < args.threshold_pct:
        print("Status:        no_trigger")
        _save_state(state)
        return 0

    if len(triggers) >= args.max_triggers:
        print("Status:        exhausted")
        print(f"NOTE: reserve allocation fully deployed across {args.max_triggers} dip-buy(s).")
        _save_state(state)
        return 0

    # Already fired since the drawdown last deepened?
    last_dd = float(triggers[-1].get("drawdown_pct") or 0) if triggers else 0.0
    if last_dd > 0 and (drawdown_pct - last_dd) < args.rearm_pct:
        print("Status:        no_trigger")
        print(f"NOTE: already fired at {last_dd*100:.2f}% drawdown; needs +{args.rearm_pct*100:.1f}% to re-arm.")
        _save_state(state)
        return 0

    remaining = args.max_triggers - len(triggers)
    used_already_usdt = sum(float(t.get("size_usdt") or 0) for t in triggers)
    remaining_reserve = max(0.0, args.reserve_usdt - used_already_usdt)
    if remaining_reserve <= 0:
        print("Status:        exhausted")
        _save_state(state)
        return 0
    size_usdt = round(remaining_reserve / remaining, 2)

    print(f"Status:        trigger")
    print(f"Recommended buy: ${size_usdt:.2f} of {args.instId}")
    print()
    print(f"To act on this, the agent should call:")
    print(f"  okx_propose_trade.py --instId {args.instId} --side buy --quote-sz {size_usdt}")
    print(f"After the user confirms with YES and the trade executes, persist the trigger:")
    print(f"  okx_dca_dip.py --reserve-usdt {args.reserve_usdt} --threshold-pct {args.threshold_pct} "
          f"--max-triggers {args.max_triggers} --record-trigger")

    if args.record_trigger:
        triggers.append({
            "ts_iso": _now_iso(),
            "drawdown_pct": round(drawdown_pct, 6),
            "ath_usd": round(ath, 4),
            "size_usdt": size_usdt,
            "instId": args.instId,
        })
        state["triggers"] = triggers
        print(f"\nRecorded trigger {len(triggers)}/{args.max_triggers}.")

    _save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
