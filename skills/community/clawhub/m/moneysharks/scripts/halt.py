#!/usr/bin/env python3
"""
MoneySharks emergency halt.
Immediately sets halt=true and circuit_breaker=true in state.json.
Optionally cancels all resting orders for configured symbols.
Journals the halt event.

usage: halt.py <config.json> [--data-dir <dir>] [--cancel-orders] [--flatten] [--reason "text"]

--cancel-orders   Cancel all open orders for each allowed symbol
--flatten         Close all open positions at market price (USE WITH CAUTION)
--reason "text"   Optional reason string for the halt journal entry
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", file=sys.stderr)


def run_json(args: list, stdin_obj=None) -> dict:
    try:
        proc = subprocess.run(
            args,
            input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            check=False,
        )
        return json.loads(proc.stdout.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return {"halt": False, "circuit_breaker": False, "consecutive_errors": 0, "daily_loss": 0.0}


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2))


def append_journal(trades_path: Path, entry: dict) -> None:
    trades = []
    if trades_path.exists():
        try:
            trades = json.loads(trades_path.read_text())
        except Exception:
            trades = []
    trades.append(entry)
    trades_path.write_text(json.dumps(trades, indent=2))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: halt.py <config.json> [--data-dir <dir>] [--cancel-orders] [--flatten] [--reason 'text']",
              file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config_path = Path(sys.argv[1])
    cancel_orders = "--cancel-orders" in sys.argv
    flatten = "--flatten" in sys.argv

    reason = "manual_halt"
    if "--reason" in sys.argv:
        idx = sys.argv.index("--reason")
        if idx + 1 < len(sys.argv):
            reason = sys.argv[idx + 1]

    data_dir = config_path.parent
    if "--data-dir" in sys.argv:
        idx = sys.argv.index("--data-dir")
        data_dir = Path(sys.argv[idx + 1])

    state_path = data_dir / "state.json"
    trades_path = data_dir / "trades.json"
    ts = datetime.now(timezone.utc).isoformat()

    # ── Load config ──
    config = {}
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
        except Exception:
            pass

    allowed_symbols = config.get("allowed_symbols", [])
    cancel_on_halt = config.get("execution", {}).get("cancel_on_halt", True)

    # ── Set halt state ──
    state = load_state(state_path)
    state["halt"] = True
    state["circuit_breaker"] = True
    state["halt_reason"] = reason
    state["halt_ts"] = ts
    save_state(state_path, state)
    log(f"✓ halt=true set in state.json")

    # ── Cancel orders ──
    cancelled = []
    cancel_errors = []
    if cancel_orders or cancel_on_halt:
        api_key = os.getenv("ASTER_API_KEY", "")
        api_secret = os.getenv("ASTER_API_SECRET", "")
        if api_key and api_secret:
            for symbol in allowed_symbols:
                log(f"  cancelling orders for {symbol} ...")
                result = run_json([sys.executable, str(base / "aster_readonly_client.py"), "cancel_all", symbol])
                if result.get("code") == 200 or not result.get("ok") is False:
                    cancelled.append(symbol)
                    log(f"  ✓ {symbol} orders cancelled")
                else:
                    cancel_errors.append({"symbol": symbol, "error": str(result)})
                    log(f"  ✗ {symbol} cancel failed: {result}")
        else:
            log("  ⚠ No credentials — cannot cancel orders")

    # ── Flatten positions (only if explicitly requested) ──
    flattened = []
    flatten_errors = []
    if flatten:
        api_key = os.getenv("ASTER_API_KEY", "")
        api_secret = os.getenv("ASTER_API_SECRET", "")
        if api_key and api_secret:
            log("  fetching open positions to flatten ...")
            sys.path.insert(0, str(base))
            try:
                import aster_readonly_client as aster
                positions = aster.get_positions()
                for p in positions:
                    amt = float(p.get("positionAmt", 0))
                    if abs(amt) > 0:
                        symbol = p.get("symbol", "")
                        side = "BUY" if amt > 0 else "SELL"
                        log(f"  closing {symbol} {side} qty={abs(amt)} ...")
                        close_result = aster.close_position_market(symbol, side, abs(amt))
                        flattened.append({"symbol": symbol, "side": side, "qty": abs(amt)})
                        log(f"  ✓ {symbol} position closed")
            except Exception as e:
                flatten_errors.append(str(e))
                log(f"  ✗ flatten error: {e}")
        else:
            log("  ⚠ No credentials — cannot flatten positions")

    # ── Journal halt event ──
    halt_journal = {
        "ts": ts,
        "type": "halt_event",
        "decision": "halt",
        "status": "halted",
        "reason": reason,
        "cancel_orders": cancel_orders or cancel_on_halt,
        "cancelled_symbols": cancelled,
        "cancel_errors": cancel_errors,
        "flatten_requested": flatten,
        "flattened": flattened,
        "flatten_errors": flatten_errors,
    }
    append_journal(trades_path, halt_journal)
    log("✓ halt event journaled")

    result = {
        "ok": True,
        "status": "halted",
        "ts": ts,
        "reason": reason,
        "halt": True,
        "circuit_breaker": True,
        "cancelled": cancelled,
        "cancel_errors": cancel_errors,
        "flattened": flattened,
        "flatten_errors": flatten_errors,
    }

    print(json.dumps(result, indent=2))
    print(f"\n🛑 MoneySharks HALTED at {ts}", file=sys.stderr)
    print(f"   Reason: {reason}", file=sys.stderr)
    if cancelled:
        print(f"   Orders cancelled for: {', '.join(cancelled)}", file=sys.stderr)
    if flattened:
        print(f"   Positions closed: {len(flattened)}", file=sys.stderr)
    print(f"\n   To resume: python3 scripts/resume.py {config_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
