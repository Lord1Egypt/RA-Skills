#!/usr/bin/env python3
"""
MoneySharks autonomous runner — main 24/7 entry point.
Called by cron every N minutes. Runs one full cycle across all configured symbols.

usage: autonomous_runner.py <config.json> [--data-dir <dir>]

Expects:
  - ASTER_API_KEY and ASTER_API_SECRET in environment
  - config.json with mode=autonomous_live and autonomous_live_consent=true
  - data dir for state.json and trades.json (default: same dir as config)

Outputs a summary JSON to stdout. Logs verbose output to stderr.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure scripts dir is in path for direct aster_readonly_client imports
_BASE = Path(__file__).resolve().parent
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))


def log(msg: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", file=sys.stderr)


def run_json(args: list, stdin_obj=None, check: bool = False) -> dict:
    try:
        proc = subprocess.run(
            args,
            input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60,
            check=False,
        )
        if proc.returncode not in (0, 1) and check:
            raise RuntimeError(f"exit {proc.returncode}: {proc.stderr.decode()[:300]}")
        return json.loads(proc.stdout.decode())
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    return {
        "halt": False,
        "circuit_breaker": False,
        "daily_loss": 0.0,
        "consecutive_errors": 0,
        "last_run": None,
        "account": {"equity": 0, "available_margin": 0, "daily_pnl": 0},
        "metrics": {},
    }


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2))


def run_post_trade_review(base: Path, config_path: Path, trades_path: Path, state_path: Path) -> dict:
    """Fetch outcomes → review_trades → update_metrics. The full self-learning cycle."""
    if not trades_path.exists():
        return {}
    try:
        config = json.loads(config_path.read_text())
        mode = config.get("mode", "paper")

        # ── Step 1: Fetch and reconcile trade outcomes from Aster ──
        fetch_args = [sys.executable, str(base / "fetch_trade_outcomes.py"), str(trades_path)]
        if mode == "paper":
            fetch_args.append("--paper")
        fetch_result = run_json(fetch_args)
        if fetch_result.get("live_updated", 0) + fetch_result.get("paper_updated", 0) > 0:
            log(f"Outcomes resolved: live={fetch_result.get('live_updated',0)} paper={fetch_result.get('paper_updated',0)}")

        # ── Step 2: Review trades ──
        trades = json.loads(trades_path.read_text())
        review = run_json([sys.executable, str(base / "review_trades.py")], trades)

        # ── Step 3: Update metrics with learning adaptations ──
        state = load_state(state_path)
        metrics = run_json([sys.executable, str(base / "update_metrics.py")], {
            "metrics": state.get("metrics", {}),
            "review": review,
            "config": config,
        })
        state["metrics"] = metrics
        save_state(state_path, state)
        return review
    except Exception as e:
        return {"error": str(e)}


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: autonomous_runner.py <config.json> [--data-dir <dir>]", file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config_path = Path(sys.argv[1])

    # Parse --data-dir
    data_dir = config_path.parent
    if "--data-dir" in sys.argv:
        idx = sys.argv.index("--data-dir")
        data_dir = Path(sys.argv[idx + 1])
    data_dir.mkdir(parents=True, exist_ok=True)

    state_path = data_dir / "state.json"
    trades_path = data_dir / "trades.json"
    ts_start = datetime.now(timezone.utc).isoformat()

    log(f"MoneySharks autonomous runner starting — config={config_path}")

    # ── Load config ──
    if not config_path.exists():
        log(f"ERROR: config not found: {config_path}")
        print(json.dumps({"ok": False, "error": "config_not_found", "ts": ts_start}))
        return 1

    config = json.loads(config_path.read_text())
    mode = config.get("mode", "paper")

    # ── Validate config ──
    validate_result = run_json(
        [sys.executable, str(base / "validate_config.py")],
        config,
    )
    if not validate_result.get("ok", True):
        log(f"Config validation failed: {validate_result.get('errors', [])}")
        print(json.dumps({"ok": False, "error": "config_invalid", "details": validate_result, "ts": ts_start}))
        return 1

    # ── Consent guard ──
    if mode == "autonomous_live":
        if not config.get("autonomous_live_consent"):
            log("BLOCKED: autonomous_live_consent not set. Run onboarding first.")
            print(json.dumps({
                "ok": False,
                "error": "no_autonomous_consent",
                "message": "autonomous_live_consent must be true in config. Run onboarding and type ACCEPT.",
                "ts": ts_start,
            }))
            return 1

    # ── Credential check ──
    api_key = os.getenv("ASTER_API_KEY", "")
    api_secret = os.getenv("ASTER_API_SECRET", "")
    if not api_key or not api_secret:
        log("ERROR: ASTER_API_KEY or ASTER_API_SECRET not set in environment.")
        print(json.dumps({"ok": False, "error": "missing_credentials", "ts": ts_start}))
        return 1

    # ── Load state ──
    state = load_state(state_path)

    # ── Hard halt check ──
    if state.get("halt"):
        log("Agent is halted. No cycles will run. Use 'halt moneysharks' to clear halt or update state.json.")
        print(json.dumps({"ok": False, "status": "halted", "ts": ts_start}))
        return 0

    # ── Circuit breaker ──
    consecutive_errors = int(state.get("consecutive_errors", 0))
    if state.get("circuit_breaker") or consecutive_errors >= 5:
        log(f"Circuit breaker active (consecutive_errors={consecutive_errors}). Skipping cycle.")
        print(json.dumps({"ok": False, "status": "circuit_breaker", "consecutive_errors": consecutive_errors, "ts": ts_start}))
        return 0

    # ── Reset daily loss at UTC midnight ──
    last_run = state.get("last_run", "")
    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    last_run_date = last_run[:10] if last_run else ""
    if now_date != last_run_date:
        log(f"New day ({now_date}), resetting daily_loss counter.")
        state["daily_loss"] = 0.0

    # ── Position monitoring — detect closed positions before scanning ──
    allowed_symbols = config.get("allowed_symbols", [])
    if not allowed_symbols:
        log("No allowed_symbols in config. Nothing to trade.")
        print(json.dumps({"ok": False, "error": "no_symbols", "ts": ts_start}))
        return 1

    known_positions = state.get("known_open_positions", {})
    if known_positions:
        log(f"Checking {len(known_positions)} known open position(s) for closes …")
        monitor_result = run_json([
            sys.executable, str(base / "position_monitor.py"),
            str(config_path), str(state_path), str(trades_path),
        ])
        closed_count = len(monitor_result.get("closed_positions", []))
        if closed_count > 0:
            log(f"  → {closed_count} position(s) closed since last cycle.")
            for cp in monitor_result.get("closed_positions", []):
                log(f"    {cp['symbol']}: {cp['outcome']} ({cp['close_reason']}) PnL={cp.get('realised_pnl', 0):.2f}")
            # Reload state after monitor updated it
            state = load_state(state_path)

    results = {}
    cycle_errors = 0

    for symbol in allowed_symbols:
        log(f"  [{symbol}] running trade loop …")
        result = run_json([
            sys.executable, str(base / "trade_loop.py"),
            str(config_path), symbol, str(state_path), str(trades_path)
        ])
        results[symbol] = result
        if result.get("ok") is False and result.get("status") not in ("halted", "daily_loss_limit_hit"):
            cycle_errors += 1
            log(f"  [{symbol}] ⚠ error: {result.get('error') or result.get('status')}")
        else:
            log(f"  [{symbol}] decision={result.get('decision')} status={result.get('status')} confidence={result.get('confidence', 0):.2f}")

        # Small delay between symbols to avoid rate limits
        if len(allowed_symbols) > 1:
            time.sleep(0.5)

    # ── Trailing stop management for open positions ──
    state = load_state(state_path)  # reload after trade loops
    known_open = state.get("known_open_positions", {})
    if known_open and mode == "autonomous_live":
        for sym, pos_info in list(known_open.items()):
            if pos_info.get("stop_loss") and pos_info.get("entry_price"):
                try:
                    # Get current price
                    ticker = run_json([
                        sys.executable, str(base / "aster_readonly_client.py"), "market", sym
                    ])
                    cur_price = float(ticker.get("ticker", {}).get("price", 0))
                    if cur_price <= 0:
                        continue

                    # Get ATR from latest features
                    klines = run_json([
                        sys.executable, str(base / "aster_readonly_client.py"), "klines", sym, "1h", "50"
                    ])
                    feats = run_json(
                        [sys.executable, str(base / "compute_features.py")],
                        {"klines": klines},
                    )
                    atr_val = feats.get("atr14", 0) or 0

                    trail_result = run_json(
                        [sys.executable, str(base / "trailing_stop.py")],
                        {
                            "symbol": sym,
                            "side": pos_info["side"],
                            "entry_price": pos_info["entry_price"],
                            "current_price": cur_price,
                            "current_stop_loss": pos_info["stop_loss"],
                            "atr": atr_val,
                        },
                    )

                    if trail_result.get("moved") and trail_result.get("new_stop_loss"):
                        new_sl = trail_result["new_stop_loss"]
                        log(f"  [{sym}] trailing stop: {pos_info['stop_loss']:.2f} → {new_sl:.2f} ({trail_result['reason']})")
                        # Cancel old SL and place new one
                        try:
                            import aster_readonly_client as aster
                            # Cancel all existing stop orders for this symbol
                            orders = aster.get_open_orders(sym)
                            for o in orders:
                                if o.get("type") == "STOP_MARKET":
                                    aster.cancel_order(sym, int(o["orderId"]))
                            # Place new SL
                            close_side = "SELL" if pos_info["side"] == "BUY" else "BUY"
                            aster.place_order(
                                symbol=sym, side=close_side,
                                quantity=pos_info["quantity"],
                                order_type="STOP_MARKET",
                                stop_price=new_sl,
                                reduce_only=True,
                            )
                            # Update state
                            known_open[sym]["stop_loss"] = new_sl
                        except Exception as e:
                            log(f"  [{sym}] trailing stop update failed: {e}")
                except Exception as e:
                    log(f"  [{sym}] trailing stop check error: {e}")
            time.sleep(0.3)
        state["known_open_positions"] = known_open
        save_state(state_path, state)

    # ── Update state ──
    state = load_state(state_path)  # reload (trade_loop may have updated it)
    state["last_run"] = ts_start
    if cycle_errors > 0:
        state["consecutive_errors"] = int(state.get("consecutive_errors", 0)) + cycle_errors
    else:
        state["consecutive_errors"] = 0
    if state.get("consecutive_errors", 0) >= 5:
        state["circuit_breaker"] = True
        log("CIRCUIT BREAKER TRIPPED: too many consecutive errors.")

    save_state(state_path, state)

    # ── Post-trade review (every 30 cycles or on each run in debug) ──
    # In production the cron review job handles this; we run a lightweight check here too.
    trade_count = state.get("metrics", {}).get("last_review_trade_count", 0)
    current_trades = []
    if trades_path.exists():
        try:
            current_trades = json.loads(trades_path.read_text())
        except Exception:
            pass
    if len(current_trades) - trade_count >= 5:
        log("Running post-trade review …")
        run_post_trade_review(base, config_path, trades_path, state_path)

    summary = {
        "ok": True,
        "ts": ts_start,
        "mode": mode,
        "symbols_scanned": allowed_symbols,
        "results": results,
        "consecutive_errors": state.get("consecutive_errors", 0),
        "circuit_breaker": state.get("circuit_breaker", False),
        "halt": state.get("halt", False),
    }
    print(json.dumps(summary, indent=2))
    log("Cycle complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
