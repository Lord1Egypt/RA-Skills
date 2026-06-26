#!/usr/bin/env python3
"""
Fetch trade outcomes from Aster DEX and update trades.json with realised PnL.

For LIVE trades: queries /fapi/v1/income (REALIZED_PNL) from Aster and matches
income records to open journal entries by symbol and time.

For PAPER trades: estimates outcome from current mark price vs stop/take-profit
levels recorded at entry time.

This script must run before review_trades.py to ensure outcome/realised_pnl
fields are populated. Called by autonomous_runner.py post-trade review and by
the autonomous_review cron job.

usage: fetch_trade_outcomes.py <trades.json> [--data-dir <dir>] [--paper]
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
            timeout=30,
            check=False,
        )
        return json.loads(proc.stdout.decode())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def ts_to_ms(ts_str: str) -> int:
    """Convert ISO-8601 timestamp string to milliseconds."""
    try:
        dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    except Exception:
        return 0


def classify_outcome(pnl: float) -> str:
    if pnl > 0:
        return "win"
    elif pnl < 0:
        return "loss"
    return "breakeven"


def estimate_paper_outcome(trade: dict) -> dict | None:
    """
    Estimate paper trade outcome from current price vs SL/TP levels.
    Returns dict with outcome + estimated_pnl, or None if undetermined.
    """
    order = trade.get("order") or {}
    side = order.get("side")
    stop_loss = float(order.get("stop_loss") or 0)
    take_profit = float(order.get("take_profit") or 0)
    entry_price = float(order.get("entry_price") or 0)
    quantity = float(order.get("quantity") or 0)

    if not side or not stop_loss or not take_profit or not entry_price:
        return None

    # Fetch current market price for the symbol
    base = Path(__file__).resolve().parent
    ticker = run_json([sys.executable, str(base / "aster_readonly_client.py"), "market", trade.get("symbol", "")])
    if not ticker or ticker.get("ok") is False:
        return None

    try:
        current_price = float(ticker.get("ticker", {}).get("price", 0))
    except Exception:
        return None

    if not current_price:
        return None

    is_long = side.upper() == "BUY"

    if is_long:
        if current_price >= take_profit:
            pnl = (take_profit - entry_price) * quantity
            return {"outcome": "win", "realised_pnl": round(pnl, 6), "exit_price": take_profit, "exit_reason": "tp_hit"}
        elif current_price <= stop_loss:
            pnl = (stop_loss - entry_price) * quantity
            return {"outcome": "loss", "realised_pnl": round(pnl, 6), "exit_price": stop_loss, "exit_reason": "sl_hit"}
    else:  # SHORT
        if current_price <= take_profit:
            pnl = (entry_price - take_profit) * quantity
            return {"outcome": "win", "realised_pnl": round(pnl, 6), "exit_price": take_profit, "exit_reason": "tp_hit"}
        elif current_price >= stop_loss:
            pnl = (entry_price - stop_loss) * quantity
            return {"outcome": "loss", "realised_pnl": round(pnl, 6), "exit_price": stop_loss, "exit_reason": "sl_hit"}

    # Position still appears open
    unrealised = ((current_price - entry_price) * quantity) if is_long else ((entry_price - current_price) * quantity)
    return {
        "outcome": None,  # still open
        "unrealised_pnl_estimate": round(unrealised, 6),
        "current_price": current_price,
    }


def fetch_income_for_symbol(symbol: str, start_ms: int, limit: int = 200) -> list:
    """
    Fetch income history (REALIZED_PNL) from Aster for a symbol after start_ms.
    Uses aster_readonly_client CLI.
    """
    base = Path(__file__).resolve().parent
    # We'll import aster_readonly_client directly since we need its private API
    sys.path.insert(0, str(base))
    try:
        import aster_readonly_client as aster
        records = aster._get(
            "/fapi/v1/income",
            {"symbol": symbol, "incomeType": "REALIZED_PNL", "startTime": start_ms, "limit": limit},
            private=True,
        )
        return records if isinstance(records, list) else []
    except Exception as e:
        log(f"  income fetch failed for {symbol}: {e}")
        return []


def update_live_trade(trade: dict, income_records: list) -> bool:
    """
    Try to match a live trade to an income record.
    income_records: filtered list for this symbol after trade entry.
    Mutates trade dict in-place. Returns True if updated.
    """
    if not income_records:
        return False

    entry_ts_ms = ts_to_ms(trade.get("ts", ""))

    # Find income records that occurred after the trade entry, sorted by time
    candidates = sorted(
        [r for r in income_records if int(r.get("time", 0)) >= entry_ts_ms],
        key=lambda r: int(r.get("time", 0)),
    )

    if not candidates:
        return False

    # Take the most recent REALIZED_PNL that occurred after our entry
    # This is a heuristic — works well when only one concurrent trade per symbol
    record = candidates[-1]
    pnl = float(record.get("income", 0))
    trade["outcome"] = classify_outcome(pnl)
    trade["realised_pnl"] = pnl
    trade["outcome_ts"] = datetime.fromtimestamp(
        int(record.get("time", 0)) / 1000, tz=timezone.utc
    ).isoformat()
    trade["lesson_tags"] = []

    # Auto-tag lessons
    order = trade.get("order") or {}
    entry_price = float(order.get("entry_price") or 0)
    stop_loss = float(order.get("stop_loss") or 0)
    take_profit = float(order.get("take_profit") or 0)
    quantity = float(order.get("quantity") or 0)

    if pnl < 0 and entry_price and stop_loss and quantity:
        expected_loss = abs(entry_price - stop_loss) * quantity
        if abs(pnl) > expected_loss * 1.1:
            trade["lesson_tags"].append("slippage_on_stop")

    if trade.get("outcome") == "loss":
        confidence = float(trade.get("confidence", 0))
        if confidence > 0.7:
            trade["lesson_tags"].append("high_confidence_loss")
        regime = trade.get("market", {})
        f1h = trade.get("features_1h", {})
        if f1h.get("high_volatility"):
            trade["lesson_tags"].append("volatile_regime_loss")

    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch_trade_outcomes.py <trades.json> [--paper]", file=sys.stderr)
        return 2

    trades_path = Path(sys.argv[1])
    paper_mode = "--paper" in sys.argv

    if not trades_path.exists():
        log(f"trades.json not found: {trades_path}")
        print(json.dumps({"ok": False, "error": "trades_not_found"}))
        return 1

    trades = json.loads(trades_path.read_text())
    if not isinstance(trades, list):
        log("Invalid trades.json: expected list")
        print(json.dumps({"ok": False, "error": "invalid_trades_format"}))
        return 1

    updated_count = 0
    skipped_count = 0
    paper_updated = 0

    # ── Group open live trades by symbol for batch income fetch ──
    live_open = [
        t for t in trades
        if t.get("status") == "live_executed"
        and t.get("decision") in ("long", "short")
        and not t.get("outcome")
    ]

    symbols_needing_fetch = list(set(t.get("symbol") for t in live_open if t.get("symbol")))

    # ── Fetch income records per symbol ──
    income_by_symbol: dict[str, list] = {}
    for symbol in symbols_needing_fetch:
        # Find oldest unresolved trade for this symbol to set lookback start
        sym_trades = [t for t in live_open if t.get("symbol") == symbol]
        oldest_ts = min((ts_to_ms(t.get("ts", "")) for t in sym_trades if t.get("ts")), default=0)
        if oldest_ts > 0:
            log(f"  fetching income for {symbol} since {oldest_ts}")
            income_by_symbol[symbol] = fetch_income_for_symbol(symbol, oldest_ts)
            log(f"  {len(income_by_symbol[symbol])} income records found for {symbol}")
        else:
            income_by_symbol[symbol] = []

    # ── Update live trades ──
    for trade in trades:
        if (
            trade.get("status") == "live_executed"
            and trade.get("decision") in ("long", "short")
            and not trade.get("outcome")
        ):
            symbol = trade.get("symbol")
            records = income_by_symbol.get(symbol, [])
            if update_live_trade(trade, records):
                updated_count += 1
                log(f"  [{symbol}] outcome={trade['outcome']} pnl={trade['realised_pnl']:.4f}")
            else:
                skipped_count += 1

    # ── Update paper trades (estimate from current price) ──
    if paper_mode:
        for trade in trades:
            if (
                trade.get("status") == "paper_executed"
                and trade.get("decision") in ("long", "short")
                and not trade.get("outcome")
            ):
                result = estimate_paper_outcome(trade)
                if result and result.get("outcome"):
                    trade["outcome"] = result["outcome"]
                    trade["realised_pnl"] = result.get("realised_pnl", 0)
                    trade["exit_price"] = result.get("exit_price")
                    trade["exit_reason"] = result.get("exit_reason")
                    trade["lesson_tags"] = trade.get("lesson_tags") or []
                    paper_updated += 1
                elif result and result.get("unrealised_pnl_estimate") is not None:
                    trade["unrealised_pnl_estimate"] = result["unrealised_pnl_estimate"]
                    trade["current_price_at_review"] = result.get("current_price")

    # ── Save updated trades ──
    if updated_count > 0 or paper_updated > 0:
        trades_path.write_text(json.dumps(trades, indent=2))
        log(f"trades.json updated: {updated_count} live + {paper_updated} paper outcomes resolved")

    result = {
        "ok": True,
        "live_updated": updated_count,
        "live_skipped": skipped_count,
        "paper_updated": paper_updated,
        "total_trades": len(trades),
        "symbols_fetched": list(income_by_symbol.keys()),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
