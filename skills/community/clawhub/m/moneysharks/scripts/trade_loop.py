#!/usr/bin/env python3
"""
Single-symbol trade loop for MoneySharks.
Called by autonomous_runner.py for each allowed symbol.
Runs one full decision cycle: scan → risk → execute → journal.

Production features:
  - Cooldown enforcement after position close
  - Duplicate position guard (one position per symbol)
  - Learning metrics feedback (confidence_multiplier, effective_leverage_cap)
  - Daily loss tracking on position close
  - Proper sys.path for aster_readonly_client imports

usage: trade_loop.py <config.json> <symbol> <state.json> <trades.json>
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Add scripts dir to sys.path for aster_readonly_client imports
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))


def run_json(args: list, stdin_obj=None, check: bool = True) -> dict:
    proc = subprocess.run(
        args,
        input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode not in (0, 1):
        raise RuntimeError(f"subprocess error ({proc.returncode}): {proc.stderr.decode()[:400]}")
    return json.loads(proc.stdout.decode())


def append_journal(trades_path: Path, entry: dict) -> None:
    trades = []
    if trades_path.exists():
        try:
            trades = json.loads(trades_path.read_text())
        except Exception:
            trades = []
    trades.append(entry)
    trades_path.write_text(json.dumps(trades, indent=2))


def load_state(state_path: Path) -> dict:
    if state_path.exists():
        try:
            return json.loads(state_path.read_text())
        except Exception:
            pass
    return {
        "account": {"equity": 0, "available_margin": 0, "daily_pnl": 0},
        "positions": [],
        "orders": [],
        "metrics": {"last_review_trade_count": 0},
        "circuit_breaker": False,
        "halt": False,
        "daily_loss": 0.0,
        "last_scan": None,
        "known_open_positions": {},
        "last_close_ts": {},
    }


def save_state(state_path: Path, state: dict) -> None:
    state_path.write_text(json.dumps(state, indent=2))


def main() -> int:
    if len(sys.argv) < 5:
        print("usage: trade_loop.py <config.json> <symbol> <state.json> <trades.json>", file=sys.stderr)
        return 2

    base = BASE_DIR
    config_path = Path(sys.argv[1])
    symbol = sys.argv[2]
    state_path = Path(sys.argv[3])
    trades_path = Path(sys.argv[4])

    config = json.loads(config_path.read_text())
    state = load_state(state_path)
    mode = config.get("mode", "paper")
    ts = datetime.now(timezone.utc).isoformat()

    # ── Halt / circuit breaker check ──
    if state.get("halt") or state.get("circuit_breaker"):
        status = "halted" if state.get("halt") else "circuit_breaker_active"
        print(json.dumps({"symbol": symbol, "decision": "wait", "status": status, "ts": ts}))
        return 0

    # ── Daily loss check ──
    daily_loss = float(state.get("daily_loss", 0))
    max_daily_loss = float(config.get("max_daily_loss", 0))
    if max_daily_loss > 0 and daily_loss >= max_daily_loss:
        print(json.dumps({"symbol": symbol, "decision": "wait", "status": "daily_loss_limit_hit", "ts": ts}))
        return 0

    # ── Cooldown check ── prevent rapid re-entry after position close
    cooldown_sec = int(config.get("cooldown_after_close_sec", 120))
    last_close_ts = state.get("last_close_ts", {}).get(symbol, "")
    if last_close_ts and cooldown_sec > 0:
        try:
            last_close_dt = datetime.fromisoformat(last_close_ts.replace("Z", "+00:00"))
            now_dt = datetime.now(timezone.utc)
            elapsed = (now_dt - last_close_dt).total_seconds()
            if elapsed < cooldown_sec:
                remaining = int(cooldown_sec - elapsed)
                print(json.dumps({
                    "symbol": symbol, "decision": "wait",
                    "status": "cooldown_active", "remaining_sec": remaining, "ts": ts
                }))
                return 0
        except (ValueError, TypeError):
            pass

    # ── Duplicate position guard ── skip entry if already positioned
    known_positions = state.get("known_open_positions", {})
    has_existing = symbol in known_positions

    # ── 1. Market scan ──
    try:
        scan = run_json([sys.executable, str(base / "market_scan_from_aster.py"), str(config_path), symbol])
    except Exception as e:
        print(json.dumps({"symbol": symbol, "decision": "wait", "status": "scan_error", "error": str(e), "ts": ts}))
        return 1

    if not scan.get("signal"):
        print(json.dumps({"symbol": symbol, "decision": "wait", "status": "scan_empty", "ts": ts}))
        return 0

    signal = scan["signal"]
    confidence = float(scan.get("confidence", 0))
    order_params = scan.get("order")
    existing_position = scan.get("existing_position")
    account = scan.get("account", {})
    equity = float(account.get("equity", 0))

    # ── Learning feedback ── apply confidence_multiplier and effective_leverage_cap from metrics
    metrics = state.get("metrics", {})
    conf_multiplier = float(metrics.get("confidence_multiplier", 1.0))
    effective_lev_cap = metrics.get("effective_leverage_cap")
    recommended_min_conf = float(metrics.get("recommended_min_confidence", 0.55))

    # Adjust confidence by learning multiplier
    adjusted_confidence = confidence * conf_multiplier

    # If learning says raise the bar, respect it
    if signal in ("long", "short") and adjusted_confidence < recommended_min_conf:
        journal_entry = {
            "ts": ts, "symbol": symbol, "mode": mode, "decision": "wait",
            "signal": signal, "confidence": confidence,
            "adjusted_confidence": adjusted_confidence,
            "status": "below_learning_threshold",
            "note": f"Raw confidence {confidence:.2f} × multiplier {conf_multiplier:.2f} = {adjusted_confidence:.2f} < threshold {recommended_min_conf:.2f}",
        }
        append_journal(trades_path, journal_entry)
        print(json.dumps({
            "symbol": symbol, "decision": "wait", "status": "below_learning_threshold",
            "confidence": confidence, "adjusted_confidence": adjusted_confidence, "ts": ts
        }))
        return 0

    # Cap leverage at effective_leverage_cap from learning
    if order_params and effective_lev_cap is not None:
        order_lev = int(order_params.get("leverage", 1))
        capped_lev = min(order_lev, int(effective_lev_cap))
        if capped_lev != order_lev:
            order_params["leverage"] = capped_lev
            # Recalculate quantity for new leverage
            if order_params.get("entry_price") and order_params.get("stop_loss"):
                risk_pct = float(config.get("risk_pct_per_trade", 0.01))
                entry_p = float(order_params["entry_price"])
                stop_p = float(order_params["stop_loss"])
                stop_dist_pct = abs(entry_p - stop_p) / entry_p if entry_p else 0
                risk_usd = equity * risk_pct
                notional = risk_usd / stop_dist_pct if stop_dist_pct > 0 else 0
                max_notional = float(config.get("max_notional_per_trade", 0))
                if max_notional and notional > max_notional:
                    notional = max_notional
                order_params["quantity"] = notional / entry_p if entry_p else 0
                order_params["notional"] = notional

    # ── Duplicate position guard for new entries ──
    if signal in ("long", "short") and has_existing and not existing_position:
        # State says we have a position but exchange scan didn't find it
        # — position may have closed. Let position_monitor handle it.
        pass
    elif signal in ("long", "short") and existing_position:
        # Already in a position on this symbol — don't stack
        journal_entry = {
            "ts": ts, "symbol": symbol, "mode": mode, "decision": "hold",
            "signal": signal, "confidence": confidence,
            "status": "duplicate_position_guard",
            "note": f"Already positioned {existing_position.get('side')} on {symbol}",
        }
        append_journal(trades_path, journal_entry)
        print(json.dumps({
            "symbol": symbol, "decision": "hold", "status": "duplicate_position_guard",
            "confidence": confidence, "ts": ts
        }))
        return 0

    # ── 2. Risk checks ──
    risk_payload = {
        "daily_loss_hit": daily_loss >= max_daily_loss if max_daily_loss else False,
        "exposure_after_trade": float(account.get("total_exposure", 0)) + float((order_params or {}).get("notional", 0)),
        "max_total_exposure": float(config.get("max_total_exposure", 0)),
        "notional": float((order_params or {}).get("notional", 0)),
        "max_notional_per_trade": float(config.get("max_notional_per_trade", 0)),
        "available_margin": float(account.get("available_margin", 0)),
        "required_margin": float((order_params or {}).get("notional", 0)) / max(int((order_params or {}).get("leverage", 1)), 1),
    }
    risk = run_json([sys.executable, str(base / "risk_checks.py")], risk_payload)
    risk_ok = risk.get("ok", False)

    if not risk_ok and signal in ("long", "short"):
        journal_entry = {
            "ts": ts, "symbol": symbol, "mode": mode, "decision": "wait",
            "signal": signal, "confidence": confidence,
            "status": "blocked_by_risk", "risk_failures": risk.get("failures", []),
        }
        append_journal(trades_path, journal_entry)
        print(json.dumps({"symbol": symbol, "decision": "wait", "status": "risk_blocked",
                          "failures": risk.get("failures", []), "ts": ts}))
        return 0

    # ── 3. Execute by mode ──
    exec_result = None
    final_decision = signal
    status = "journaled"

    if signal in ("long", "short") and order_params:
        side = order_params["side"]
        quantity = float(order_params.get("quantity", 0))
        leverage = int(order_params.get("leverage", 1))
        stop_loss = float(order_params["stop_loss"])
        take_profit = float(order_params["take_profit"])
        entry_price = float(order_params["entry_price"])
        notional = float(order_params.get("notional", 0))

        if quantity <= 0:
            final_decision = "wait"
            status = "zero_quantity"

        elif mode == "paper":
            # Simulate
            exec_result = {
                "ok": True, "status": "PAPER_SIMULATED",
                "symbol": symbol, "side": side, "quantity": quantity,
                "leverage": leverage, "stop_loss": stop_loss, "take_profit": take_profit,
                "entry_price": entry_price, "notional": notional,
                "simulated": True,
            }
            status = "paper_executed"

        elif mode == "autonomous_live":
            exec_input = {
                "mode": "autonomous_live",
                "require_human_approval": False,
                "symbol": symbol, "side": side, "quantity": quantity,
                "leverage": leverage, "entry_price": entry_price,
                "stop_loss": stop_loss, "take_profit": take_profit,
                "reason": scan.get("signal_reason", ""),
                "confidence": adjusted_confidence,
            }
            exec_result = run_json(
                [sys.executable, str(base / "live_execution_adapter.py")],
                exec_input,
                check=False,
            )
            status = "live_executed" if exec_result.get("ok") else "execution_error"

            # Track opened position in state
            if exec_result.get("ok"):
                state.setdefault("known_open_positions", {})[symbol] = {
                    "side": side,
                    "quantity": quantity,
                    "entry_price": entry_price,
                    "leverage": leverage,
                    "stop_loss": stop_loss,
                    "take_profit": take_profit,
                    "opened_at": ts,
                }

        elif mode == "live":
            # Per-trade approval required in live mode; emit proposal
            exec_result = {
                "ok": False, "status": "PENDING_APPROVAL",
                "symbol": symbol, "side": side, "quantity": quantity,
                "leverage": leverage, "stop_loss": stop_loss, "take_profit": take_profit,
                "entry_price": entry_price, "confidence": adjusted_confidence,
                "reason": scan.get("signal_reason", ""),
            }
            status = "proposal_emitted"

    elif signal in ("close", "hold") and existing_position:
        if signal == "close" and mode == "autonomous_live":
            try:
                from aster_readonly_client import close_position_market
                pos = existing_position
                close_r = close_position_market(pos["symbol"], pos["side"], pos["quantity"])
                exec_result = {"ok": True, "status": "POSITION_CLOSED", "api_result": close_r}
                status = "position_closed"

                # Update state: remove from known positions, set cooldown
                state.get("known_open_positions", {}).pop(symbol, None)
                state.setdefault("last_close_ts", {})[symbol] = ts

                # Get realised PnL from the close
                try:
                    from aster_readonly_client import get_income_history
                    incomes = get_income_history(symbol, limit=5)
                    rpnl = sum(float(i.get("income", 0)) for i in incomes
                               if i.get("incomeType") == "REALIZED_PNL")
                    exec_result["realised_pnl"] = rpnl
                    if rpnl < 0:
                        state["daily_loss"] = float(state.get("daily_loss", 0)) + abs(rpnl)
                except Exception:
                    pass

            except Exception as e:
                exec_result = {"ok": False, "status": "CLOSE_ERROR", "error": str(e)}
                status = "close_error"
        elif signal == "close" and mode == "paper":
            exec_result = {"ok": True, "status": "PAPER_CLOSE", "note": "Simulated position close."}
            status = "paper_closed"
            state.setdefault("last_close_ts", {})[symbol] = ts
        else:
            exec_result = {"ok": True, "status": "HOLD", "note": "Holding existing position."}
            status = "hold"

    # ── 4. Determine regime from features ──
    f1h = scan.get("features_1h", {})
    regime = "unknown"
    if f1h.get("trend") == "up" and not f1h.get("high_volatility"):
        regime = "trending_up"
    elif f1h.get("trend") == "down" and not f1h.get("high_volatility"):
        regime = "trending_down"
    elif f1h.get("high_volatility"):
        regime = "high_volatility"
    elif f1h.get("trend") == "neutral":
        regime = "ranging"

    # ── 5. Journal ──
    journal_entry = {
        "ts": ts,
        "symbol": symbol,
        "mode": mode,
        "decision": final_decision,
        "signal": signal,
        "signal_reason": scan.get("signal_reason", ""),
        "confidence": confidence,
        "adjusted_confidence": adjusted_confidence,
        "regime": regime,
        "confluence": scan.get("confluence", {}),
        "order": order_params,
        "existing_position": existing_position,
        "exec_result": exec_result,
        "status": status,
        "market": scan.get("market"),
        "features_1h": {
            k: f1h.get(k)
            for k in ("rsi14", "ema20", "ema50", "atr14", "volume_ratio", "trend", "momentum", "funding_rate")
        } if f1h else {},
    }
    append_journal(trades_path, journal_entry)

    # ── 6. Update state ──
    state["last_scan"] = ts
    state["account"] = {
        "equity": equity,
        "available_margin": float(account.get("available_margin", 0)),
        "daily_pnl": float(state.get("account", {}).get("daily_pnl", 0)),
    }
    save_state(state_path, state)

    print(json.dumps({
        "symbol": symbol, "decision": final_decision, "status": status,
        "confidence": confidence, "adjusted_confidence": adjusted_confidence,
        "mode": mode, "regime": regime, "ts": ts,
        "exec_ok": exec_result.get("ok") if exec_result else None,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
