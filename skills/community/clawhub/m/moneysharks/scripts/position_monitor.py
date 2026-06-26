#!/usr/bin/env python3
"""
Position monitor — detects closed positions (SL/TP hit) and records outcomes.
Compares last known positions in state.json against live exchange positions.
When a position disappears, queries income history for realised PnL.

usage: position_monitor.py <config.json> <state.json> <trades.json>

Output (stdout JSON):
  {
    "ok": bool,
    "closed_positions": [...],
    "updated_trades": int
  }
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_json(args: list, stdin_obj=None) -> dict:
    proc = subprocess.run(
        args,
        input=(json.dumps(stdin_obj).encode() if stdin_obj is not None else None),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=30, check=False,
    )
    if proc.returncode not in (0, 1):
        return {"ok": False, "error": proc.stderr.decode()[:300]}
    return json.loads(proc.stdout.decode())


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: position_monitor.py <config.json> <state.json> <trades.json>", file=sys.stderr)
        return 2

    base = Path(__file__).resolve().parent
    config_path = Path(sys.argv[1])
    state_path = Path(sys.argv[2])
    trades_path = Path(sys.argv[3])
    ts = datetime.now(timezone.utc).isoformat()

    config = json.loads(config_path.read_text())
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    trades = json.loads(trades_path.read_text()) if trades_path.exists() else []

    # Get previously known open positions from state
    prev_positions = state.get("known_open_positions", {})
    # e.g. {"BTCUSDT": {"side": "BUY", "quantity": 0.001, "entry_price": 85000, "opened_at": "..."}}

    if not prev_positions:
        # Nothing to monitor
        print(json.dumps({"ok": True, "closed_positions": [], "updated_trades": 0}))
        return 0

    # Fetch live positions from exchange
    live_bundle = run_json([sys.executable, str(base / "aster_readonly_client.py"), "account"])
    if not live_bundle.get("positions"):
        live_bundle["positions"] = []

    # Build set of currently open symbols
    live_open = {}
    for p in live_bundle.get("positions", []):
        sym = p.get("symbol", "")
        amt = float(p.get("positionAmt", 0))
        if abs(amt) > 0:
            live_open[sym] = {
                "side": "BUY" if amt > 0 else "SELL",
                "quantity": abs(amt),
                "entry_price": float(p.get("entryPrice", 0)),
                "unrealised_pnl": float(p.get("unRealizedProfit", 0)),
            }

    # Detect closed positions
    closed_positions = []
    for symbol, prev in list(prev_positions.items()):
        if symbol not in live_open:
            # Position was closed (SL, TP, or manual)
            # Try to get realised PnL from income history
            realised_pnl = 0.0
            close_reason = "unknown"
            try:
                income = run_json([
                    sys.executable, str(base / "aster_readonly_client.py"), "account", symbol
                ])
                # Check open orders — if SL/TP orders are also gone, they were triggered
                open_orders = income.get("orders", [])
                sl_exists = any(o.get("type") == "STOP_MARKET" for o in open_orders)
                tp_exists = any(o.get("type") == "TAKE_PROFIT_MARKET" for o in open_orders)

                if not sl_exists and not tp_exists:
                    close_reason = "sl_or_tp_hit"
                elif sl_exists and not tp_exists:
                    close_reason = "take_profit_hit"
                elif tp_exists and not sl_exists:
                    close_reason = "stop_loss_hit"
            except Exception:
                pass

            # Query income history for this symbol to get realised PnL
            try:
                sys.path.insert(0, str(base))
                from aster_readonly_client import get_income_history
                incomes = get_income_history(symbol, limit=20)
                # Sum recent REALIZED_PNL entries
                for inc in incomes:
                    if inc.get("incomeType") == "REALIZED_PNL":
                        realised_pnl += float(inc.get("income", 0))
            except Exception:
                pass

            outcome = "win" if realised_pnl > 0 else ("loss" if realised_pnl < 0 else "breakeven")
            entry_price = float(prev.get("entry_price", 0))

            closed_record = {
                "symbol": symbol,
                "side": prev.get("side"),
                "quantity": prev.get("quantity"),
                "entry_price": entry_price,
                "realised_pnl": realised_pnl,
                "outcome": outcome,
                "close_reason": close_reason,
                "closed_at": ts,
                "opened_at": prev.get("opened_at", ""),
            }
            closed_positions.append(closed_record)

            # Update the most recent matching trade journal entry with outcome
            for i in range(len(trades) - 1, -1, -1):
                t = trades[i]
                if (t.get("symbol") == symbol
                        and t.get("decision") in ("long", "short")
                        and t.get("status") in ("live_executed", "paper_executed")
                        and "outcome" not in t):
                    trades[i]["outcome"] = outcome
                    trades[i]["realised_pnl"] = realised_pnl
                    trades[i]["close_reason"] = close_reason
                    trades[i]["closed_at"] = ts
                    # Add lesson tags based on outcome
                    tags = []
                    if close_reason == "stop_loss_hit":
                        tags.append("stopped-out")
                    elif close_reason == "take_profit_hit":
                        tags.append("target-hit")
                    if realised_pnl > 0:
                        tags.append("profitable")
                    else:
                        tags.append("loss-trade")
                    # Regime from features if available
                    f1h = t.get("features_1h", {})
                    if f1h.get("trend") == "up":
                        tags.append("uptrend")
                    elif f1h.get("trend") == "down":
                        tags.append("downtrend")
                    if f1h.get("high_volatility"):
                        tags.append("high-volatility")
                    trades[i]["lesson_tags"] = tags
                    trades[i]["regime"] = f1h.get("trend", "unknown")
                    break

            # Remove from known positions
            del prev_positions[symbol]

    # Update state with current open positions
    state["known_open_positions"] = {}
    for sym, pos in live_open.items():
        if sym in prev_positions:
            # Still open — keep original opened_at
            state["known_open_positions"][sym] = prev_positions[sym]
        else:
            # New position we didn't track before
            state["known_open_positions"][sym] = {
                "side": pos["side"],
                "quantity": pos["quantity"],
                "entry_price": pos["entry_price"],
                "opened_at": ts,
            }

    # Update daily loss counter
    for cp in closed_positions:
        if cp["realised_pnl"] < 0:
            state["daily_loss"] = float(state.get("daily_loss", 0)) + abs(cp["realised_pnl"])

    # Save
    state_path.write_text(json.dumps(state, indent=2))
    if trades:
        trades_path.write_text(json.dumps(trades, indent=2))

    print(json.dumps({
        "ok": True,
        "closed_positions": closed_positions,
        "updated_trades": len(closed_positions),
        "current_open": list(live_open.keys()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
