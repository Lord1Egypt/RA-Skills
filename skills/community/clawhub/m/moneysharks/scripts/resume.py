#!/usr/bin/env python3
"""
Resume MoneySharks from halt.
Clears halt=false, circuit_breaker=false, consecutive_errors=0 in state.json.
Optionally switches mode (default: paper for safety).
Optionally runs a reconcile cycle before first execution.

usage: resume.py <config.json> [--data-dir <dir>] [--mode paper|live|autonomous_live] [--run-now]

--mode             Mode to resume in (default: paper — safer; specify autonomous_live to resume live)
--run-now          Run one full cycle immediately after resuming
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", file=sys.stderr)


def run_json(args: list) -> dict:
    try:
        proc = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=False
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
    return {}


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
        print("usage: resume.py <config.json> [--data-dir <dir>] [--mode paper|live|autonomous_live] [--run-now]",
              file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config_path = Path(sys.argv[1])
    run_now = "--run-now" in sys.argv
    VALID_MODES = {"paper", "live", "autonomous_live", "approval"}

    resume_mode = "paper"  # default to paper for safety
    if "--mode" in sys.argv:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            resume_mode = sys.argv[idx + 1]
            if resume_mode not in VALID_MODES:
                print(f"ERROR: invalid mode '{resume_mode}'. Must be one of {VALID_MODES}", file=sys.stderr)
                return 1

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

    # ── Warn if resuming into autonomous_live ──
    if resume_mode == "autonomous_live":
        if not config.get("autonomous_live_consent"):
            print(
                "ERROR: Cannot resume in autonomous_live mode — autonomous_live_consent is not set in config.json.\n"
                "Run onboarding.py to re-consent, or use --mode paper to resume safely.",
                file=sys.stderr,
            )
            return 1
        log("⚠ Resuming in autonomous_live mode — live orders WILL be placed.")

    # ── Clear halt state ──
    state = load_state(state_path)
    prev_halt_reason = state.get("halt_reason", "unknown")
    state["halt"] = False
    state["circuit_breaker"] = False
    state["consecutive_errors"] = 0
    state["resume_ts"] = ts
    state["resume_mode"] = resume_mode
    state.pop("halt_reason", None)
    state.pop("halt_ts", None)
    save_state(state_path, state)
    log(f"✓ halt cleared (was: {prev_halt_reason})")

    # ── Update config mode if changed ──
    if config.get("mode") != resume_mode:
        config["mode"] = resume_mode
        if resume_mode != "autonomous_live":
            config["autonomous_live_consent"] = False
        config_path.write_text(json.dumps(config, indent=2))
        log(f"✓ config.json mode updated to: {resume_mode}")

    # ── Journal resume event ──
    resume_journal = {
        "ts": ts,
        "type": "resume_event",
        "decision": "resume",
        "status": "resumed",
        "mode": resume_mode,
        "prev_halt_reason": prev_halt_reason,
    }
    append_journal(trades_path, resume_journal)
    log("✓ resume event journaled")

    # ── Reconcile state from Aster before first cycle ──
    api_key = os.getenv("ASTER_API_KEY", "")
    api_secret = os.getenv("ASTER_API_SECRET", "")
    reconcile_result = {}
    if api_key and api_secret:
        log("  reconciling state from Aster ...")
        allowed_symbols = config.get("allowed_symbols", [])
        symbol = allowed_symbols[0] if allowed_symbols else None
        bundle = run_json([sys.executable, str(base / "aster_readonly_client.py"), "account"] +
                         ([symbol] if symbol else []))
        if not bundle.get("ok") is False:
            account = bundle.get("account", {})
            positions = bundle.get("positions", [])
            orders = bundle.get("orders", [])
            sys.path.insert(0, str(base))
            try:
                import aster_readonly_client as aster
                reconcile_result = {
                    "equity": float(account.get("totalWalletBalance") or 0),
                    "available_margin": float(account.get("availableBalance") or 0),
                    "positions": len([p for p in positions if abs(float(p.get("positionAmt", 0))) > 0]),
                    "orders": len(orders),
                }
                state = load_state(state_path)
                state["account"] = {
                    "equity": reconcile_result["equity"],
                    "available_margin": reconcile_result["available_margin"],
                }
                save_state(state_path, state)
                log(f"  ✓ reconciled: equity={reconcile_result['equity']:.2f}, "
                    f"positions={reconcile_result['positions']}")
            except Exception as e:
                log(f"  ⚠ reconcile import error: {e}")
        else:
            log("  ⚠ Could not reach Aster for reconciliation")

    # ── Run cycle now if requested ──
    run_result = {}
    if run_now:
        log("Running first cycle now ...")
        run_result = run_json([sys.executable, str(base / "autonomous_runner.py"), str(config_path),
                               "--data-dir", str(data_dir)])
        if run_result.get("ok"):
            log("✓ First cycle complete")
        else:
            log(f"⚠ First cycle returned: {run_result.get('error') or run_result.get('status')}")

    result = {
        "ok": True,
        "status": "resumed",
        "mode": resume_mode,
        "ts": ts,
        "halt": False,
        "circuit_breaker": False,
        "consecutive_errors": 0,
        "reconcile": reconcile_result,
        "first_cycle": run_result if run_now else None,
    }

    print(json.dumps(result, indent=2))
    print(f"\n✅ MoneySharks RESUMED at {ts}", file=sys.stderr)
    print(f"   Mode: {resume_mode}", file=sys.stderr)
    if reconcile_result:
        print(f"   Account equity: ${reconcile_result.get('equity', 0):.2f}", file=sys.stderr)
        print(f"   Open positions: {reconcile_result.get('positions', 0)}", file=sys.stderr)
    if resume_mode == "autonomous_live":
        print(f"\n   ⚠ Live mode active — cron will execute trades autonomously.", file=sys.stderr)
    else:
        print(f"\n   Mode is '{resume_mode}' — no live orders until you switch to autonomous_live.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
