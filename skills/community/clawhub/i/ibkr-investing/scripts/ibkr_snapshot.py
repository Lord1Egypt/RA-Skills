#!/usr/bin/env python3
"""IBKR daily account snapshot.

Persists `~/.aeon/ibkr/snapshots/<UTC-date>.json` with:
  - timestamp + UTC date
  - NAV, cash, buying power
  - per-position equity (qty, avg cost, mark, value, UPL)
  - per-instrument 1D/1W/1Y price changes (when --no-price-history not set)
  - delta vs the most recent prior snapshot (NAV change, position changes)

Mirrors okx_snapshot.py so the daily digest looks consistent across the two
skills. Designed as the body of a scheduled morning Telegram digest.

Defaults the watched ticker list from `IBKR_ALLOWED_SYMBOLS` plus the symbols
currently held in your account. Pass --symbol multiple times to override.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from _ibkr_client import connect, env_summary, smart_stock

SNAPSHOT_DIR = Path(os.path.expanduser("~/.aeon/ibkr/snapshots"))


KEY_TAGS = {
    "NetLiquidation": "nav",
    "TotalCashValue": "cash",
    "StockMarketValue": "stock_value",
    "BuyingPower": "buying_power",
    "UnrealizedPnL": "unrealized_pnl",
    "RealizedPnL": "realized_pnl",
    "GrossPositionValue": "gross_position_value",
}


def _resolve_symbols(cli_symbols: list[str], position_symbols: list[str]) -> list[str]:
    if cli_symbols:
        return list(dict.fromkeys(s.upper() for s in cli_symbols))
    seen: list[str] = []
    raw = os.environ.get("IBKR_ALLOWED_SYMBOLS", "").strip()
    if raw:
        for s in raw.split(","):
            s = s.strip().upper()
            if s and s not in seen:
                seen.append(s)
    for s in position_symbols:
        if s and s.upper() not in seen:
            seen.append(s.upper())
    return seen


def _previous_snapshot(today: str) -> dict | None:
    if not SNAPSHOT_DIR.exists():
        return None
    files = sorted(p.name for p in SNAPSHOT_DIR.glob("*.json"))
    files = [f for f in files if f != f"{today}.json"]
    if not files:
        return None
    try:
        return json.loads((SNAPSHOT_DIR / files[-1]).read_text())
    except Exception:
        return None


def _historical_closes(ib, contract, duration: str = "400 D") -> list[tuple[int, float]]:
    """Return up to ~400 daily closes (newest-first). Empty list on failure."""
    try:
        bars = ib.reqHistoricalData(
            contract, endDateTime="", durationStr=duration, barSizeSetting="1 day",
            whatToShow="TRADES", useRTH=True, formatDate=2,
        )
    except Exception:
        return []
    out: list[tuple[int, float]] = []
    for b in bars:
        # `b.date` is a date object (formatDate=2 returns datetime/date); convert to ms epoch.
        try:
            d = b.date
            if hasattr(d, "timestamp"):
                ts_ms = int(d.timestamp() * 1000)
            else:
                from datetime import datetime as _dt
                ts_ms = int(_dt.combine(d, _dt.min.time()).timestamp() * 1000)
            out.append((ts_ms, float(b.close)))
        except Exception:
            continue
    out.sort(key=lambda kv: -kv[0])  # newest-first
    return out


def _close_n_days_ago(closes: list[tuple[int, float]], days_back: int, tolerance_days: int = 4) -> float | None:
    if not closes:
        return None
    target_ts = int((time.time() - days_back * 86400) * 1000)
    best_close: float | None = None
    best_diff = float("inf")
    for ts, close in closes:
        diff = abs(ts - target_ts)
        if diff < best_diff:
            best_diff = diff
            best_close = close
    if best_close is None or best_diff > tolerance_days * 86400 * 1000:
        return None
    return best_close


def _price_changes(ib, symbol: str, contract, current_px: float | None) -> dict:
    closes = _historical_closes(ib, contract)
    yesterday = _close_n_days_ago(closes, 1, tolerance_days=3)
    week_ago = _close_n_days_ago(closes, 7, tolerance_days=3)
    year_ago = _close_n_days_ago(closes, 365, tolerance_days=7)

    def pct(prev: float | None) -> float | None:
        if prev is None or prev <= 0 or current_px is None or current_px <= 0:
            return None
        return (current_px - prev) / prev

    return {
        "symbol": symbol,
        "current": current_px,
        "prev_day_close": yesterday,
        "week_ago_close": week_ago,
        "year_ago_close": year_ago,
        "change_pct_1d": pct(yesterday),
        "change_pct_7d": pct(week_ago),
        "change_pct_365d": pct(year_ago),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", action="append", default=[],
                   help="Ticker to include (repeatable). Defaults from IBKR_ALLOWED_SYMBOLS + held positions.")
    p.add_argument("--no-write", action="store_true")
    p.add_argument("--no-price-history", action="store_true",
                   help="Skip 1D/1W/1Y price-change lookup. Faster.")
    args = p.parse_args()

    ib = connect()
    try:
        # 1. Account values.
        acct: dict[str, float] = {}
        for av in ib.accountValues():
            if av.tag in KEY_TAGS and av.currency == "BASE":
                try:
                    acct[KEY_TAGS[av.tag]] = float(av.value)
                except ValueError:
                    continue

        # 2. Positions with marks.
        ib.reqMarketDataType(4)  # delayed-frozen
        positions = ib.positions()
        position_dump = []
        position_symbols = [pos.contract.symbol for pos in positions]

        marks: dict[str, float] = {}
        if positions:
            tickers = []
            for pos in positions:
                t = ib.reqMktData(pos.contract, "", False, False)
                tickers.append((pos.contract, t))
            ib.sleep(3)
            for c, t in tickers:
                last = t.last if (t.last and t.last == t.last) else t.close
                if last and last == last:
                    marks[c.symbol] = float(last)
                ib.cancelMktData(c)

        for pos in positions:
            sym = pos.contract.symbol
            qty = float(pos.position)
            avg = float(pos.avgCost) if pos.avgCost else 0.0
            mark = marks.get(sym)
            cost = qty * avg
            value = qty * mark if mark else cost
            position_dump.append({
                "symbol": sym,
                "exchange": pos.contract.exchange,
                "currency": pos.contract.currency,
                "qty": qty,
                "avg_cost": round(avg, 4),
                "mark": round(mark, 4) if mark else None,
                "value": round(value, 4),
                "upl": round(value - cost, 4) if mark else None,
            })

        # 3. Resolve watched symbols + price changes.
        symbols = _resolve_symbols(args.symbol, position_symbols)
        price_changes: dict[str, dict] = {}
        if not args.no_price_history and symbols:
            for sym in symbols:
                contract = smart_stock(sym)
                qualified = ib.qualifyContracts(contract)
                if not qualified:
                    continue
                qcontract = qualified[0]
                # Pull latest price from a quick mkt data request (delayed-frozen).
                t = ib.reqMktData(qcontract, "", False, False)
                ib.sleep(1.5)
                cur = t.last if (t.last and t.last == t.last) else t.close
                cur_f = float(cur) if (cur and cur == cur) else None
                ib.cancelMktData(qcontract)
                try:
                    price_changes[sym] = _price_changes(ib, sym, qcontract, cur_f)
                except Exception:
                    continue

        # 4. Build snapshot.
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")
        snapshot = {
            "timestamp": now.isoformat(),
            "date_utc": today_str,
            "env": env_summary(),
            "account": acct,
            "positions": position_dump,
            "price_changes": price_changes,
        }

        prev = _previous_snapshot(today_str)
        delta = None
        if prev:
            prev_nav = float((prev.get("account") or {}).get("nav") or 0)
            cur_nav = float(acct.get("nav") or 0)
            nav_change = round(cur_nav - prev_nav, 4)
            nav_change_pct = round((nav_change / prev_nav) * 100, 4) if prev_nav > 0 else 0.0
            delta = {
                "prev_date": prev.get("date_utc"),
                "nav_change_usd": nav_change,
                "nav_change_pct": nav_change_pct,
            }
            snapshot["delta"] = delta

        # 5. Persist.
        if not args.no_write:
            SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
            (SNAPSHOT_DIR / f"{today_str}.json").write_text(json.dumps(snapshot, indent=2, default=str))

        # 6. Pretty-print.
        print(env_summary())
        nav = acct.get("nav", 0.0)
        print(f"Snapshot {today_str}  NAV ~${nav:,.2f}")
        if delta:
            sign = "+" if delta["nav_change_usd"] >= 0 else ""
            pct_sign = "+" if delta["nav_change_pct"] >= 0 else ""
            print(f"  vs {delta['prev_date']}: {sign}${delta['nav_change_usd']:,.2f} ({pct_sign}{delta['nav_change_pct']:.2f}%)")
        if acct:
            print()
            print("Account:")
            for label, val in acct.items():
                print(f"  {label:<24} ${val:>14,.2f}")

        if position_dump:
            print()
            print(f"Positions ({len(position_dump)}):")
            print(f"  {'Symbol':<10} {'Qty':>10} {'Avg':>10} {'Mark':>10} {'Value':>14} {'UPL':>12}")
            for r in sorted(position_dump, key=lambda x: -(x.get("value") or 0)):
                mark_s = f"{r['mark']:>10.2f}" if r.get("mark") else f"{'—':>10}"
                upl_s = f"{r['upl']:>+12.2f}" if r.get("upl") is not None else f"{'—':>12}"
                print(f"  {r['symbol']:<10} {r['qty']:>10.2f} {r['avg_cost']:>10.2f} {mark_s} {r['value']:>14,.2f} {upl_s}")

        if price_changes:
            print()
            print("Price moves:")
            for sym, pc in price_changes.items():
                cur = pc.get("current") or 0.0
                parts = [f"  {sym:<8} ${cur:>12,.2f}"]
                for label, key in (("1D", "change_pct_1d"), ("1W", "change_pct_7d"), ("1Y", "change_pct_365d")):
                    pct = pc.get(key)
                    if pct is None:
                        parts.append(f"   {label}      n/a")
                    else:
                        sign = "+" if pct >= 0 else ""
                        parts.append(f"   {label} {sign}{pct*100:>6.2f}%")
                print("".join(parts))

        if not args.no_write:
            print()
            print(f"Saved {SNAPSHOT_DIR}/{today_str}.json")
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
