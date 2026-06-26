#!/usr/bin/env python3
"""Daily account snapshot.

Persists `~/.aeon/okx/snapshots/<UTC-date>.json` with:
  - timestamp + UTC date
  - total equity (USD-est)
  - per-currency balances (equity, available, frozen, USD-est, spot UPL)
  - per-instrument tickers
  - per-instrument 24h fills summary (count, buy/sell vol, avgs, net USDT, fees)
  - per-instrument pending-order count
  - active grid strategies summary
  - delta vs the most recent prior snapshot (equity change, per-asset deltas)
  - per-instrument price moves: vs yesterday close, vs 1-week-ago, vs 1-year-ago
    (v0.3.1+; pulls daily OHLCV via OKX history-candles, ~2 API calls/instrument)

Designed as the body of a scheduled morning Telegram digest:

  schedule_create  schedule="0 9 * * *"  task="Run okx_snapshot.py"  notify=true

Defaults the watched instrument list from `OKX_ALLOWED_SYMBOLS` plus active
grid strategies. Override with one or more `--instId` flags. Pass
`--no-price-history` to skip the historical-price lookup if you want a faster
ad-hoc summary.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from _okx_client import account_api, env_summary, market_api, trade_api
from _pending import list_strategies

SNAPSHOT_DIR = Path(os.path.expanduser("~/.aeon/okx/snapshots"))


def _resolve_inst_ids(cli_inst_ids: list[str]) -> list[str]:
    if cli_inst_ids:
        return list(dict.fromkeys(cli_inst_ids))
    seen: list[str] = []
    raw = os.environ.get("OKX_ALLOWED_SYMBOLS", "").strip()
    if raw:
        for s in raw.split(","):
            s = s.strip()
            if s and s not in seen:
                seen.append(s)
    for strat in list_strategies():
        s = strat.get("instId")
        if s and s not in seen:
            seen.append(s)
    return seen


def _fetch_24h_fills(api, inst_id: str) -> list[dict]:
    """Walk /trade/fills backwards via `after=<billId>` until we cross the 24h
    boundary or run out of pages. Caps at 50 pages (5000 fills) for safety."""
    cutoff_ms = int((time.time() - 24 * 3600) * 1000)
    out: list[dict] = []
    after = ""
    for _ in range(50):
        kwargs = {"instId": inst_id, "limit": "100"}
        if after:
            kwargs["after"] = after
        resp = api.get_fills(**kwargs)
        if resp.get("code") != "0":
            break
        page = resp.get("data") or []
        if not page:
            break
        recent = [f for f in page if int(f.get("ts") or f.get("fillTime") or 0) >= cutoff_ms]
        out.extend(recent)
        # Stop when this page already crossed the cutoff or was undersized.
        if len(recent) < len(page) or len(page) < 100:
            break
        after = page[-1].get("billId", "")
        if not after:
            break
    return out


def _summarise_fills(fills: list[dict]) -> dict:
    buy_vol = 0.0
    sell_vol = 0.0
    buy_val = 0.0
    sell_val = 0.0
    fees = 0.0
    buy_count = 0
    sell_count = 0
    for f in fills:
        try:
            px = float(f.get("fillPx") or 0)
            sz = float(f.get("fillSz") or 0)
            fees += float(f.get("fee") or 0)
        except ValueError:
            continue
        if f.get("side") == "buy":
            buy_count += 1
            buy_vol += sz
            buy_val += px * sz
        else:
            sell_count += 1
            sell_vol += sz
            sell_val += px * sz
    return {
        "fills": len(fills),
        "buy_count": buy_count,
        "sell_count": sell_count,
        "buy_vol": round(buy_vol, 8),
        "buy_val_usdt": round(buy_val, 4),
        "buy_avg": round(buy_val / buy_vol, 4) if buy_vol > 0 else 0.0,
        "sell_vol": round(sell_vol, 8),
        "sell_val_usdt": round(sell_val, 4),
        "sell_avg": round(sell_val / sell_vol, 4) if sell_vol > 0 else 0.0,
        "net_usdt": round(sell_val - buy_val, 4),
        "fees": round(fees, 6),
    }


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


def _fetch_daily_closes(api, inst_id: str, days_needed: int = 380) -> list[tuple[int, float]]:
    """Return up to days_needed daily candles as (ts_ms, close), newest first.

    Uses /market/candles (max 300 recent) plus /market/history-candles
    (paginated via `after=<oldest_ts>`) to reach the year-back range.
    Returns whatever it could fetch; callers tolerate gaps gracefully.
    """
    out: list[tuple[int, float]] = []

    # First page: most recent ~300 days from /market/candles.
    try:
        resp = api.get_candlesticks(instId=inst_id, bar="1D", limit="300")
    except Exception:
        return out
    if resp.get("code") == "0" and resp.get("data"):
        for c in resp["data"]:
            try:
                out.append((int(c[0]), float(c[4])))
            except (ValueError, IndexError):
                continue

    # Subsequent pages: older data via /market/history-candles.
    pages = 0
    while len(out) < days_needed and pages < 5 and out:
        oldest_ts = out[-1][0]
        try:
            resp = api.get_history_candlesticks(
                instId=inst_id, bar="1D", limit="100", after=str(oldest_ts)
            )
        except Exception:
            break
        if resp.get("code") != "0":
            break
        page = resp.get("data") or []
        if not page:
            break
        for c in page:
            try:
                out.append((int(c[0]), float(c[4])))
            except (ValueError, IndexError):
                continue
        pages += 1

    return out


def _close_n_days_ago(closes: list[tuple[int, float]], days_back: int, tolerance_days: int = 2) -> float | None:
    """Pick the close nearest to `days_back` days from now.
    Returns None if no candle within `tolerance_days` of the target."""
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


def _price_changes(api, inst_id: str, current_px: float) -> dict:
    """Compute current price + 1D / 1W / 1Y changes vs daily closes."""
    closes = _fetch_daily_closes(api, inst_id, days_needed=380)
    yesterday = _close_n_days_ago(closes, 1)
    week_ago = _close_n_days_ago(closes, 7)
    year_ago = _close_n_days_ago(closes, 365, tolerance_days=4)

    def pct(prev: float | None) -> float | None:
        if prev is None or prev <= 0:
            return None
        return (current_px - prev) / prev

    return {
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
    p.add_argument("--instId", action="append", default=[], help="Instrument to include (repeatable). Defaults from OKX_ALLOWED_SYMBOLS + active strategies.")
    p.add_argument("--no-write", action="store_true", help="Print summary only; do not persist a snapshot file.")
    p.add_argument("--no-price-history", action="store_true", help="Skip the 1D/1W/1Y price-change lookup. Saves ~2 API calls per instrument.")
    args = p.parse_args()

    acct = account_api()
    trd = trade_api()
    mkt = market_api()

    inst_ids = _resolve_inst_ids(args.instId)

    # 1. Balances
    bal = acct.get_account_balance()
    if bal.get("code") != "0":
        print(f"Balance error: {bal.get('msg')!r}", file=sys.stderr)
        return 1
    bal_summary = (bal.get("data") or [{}])[0]
    total_equity_usd = float(bal_summary.get("totalEq") or 0)
    assets: dict[str, dict] = {}
    for d in bal_summary.get("details") or []:
        try:
            eq = float(d.get("eq") or 0)
        except ValueError:
            continue
        if eq <= 0:
            continue
        assets[d.get("ccy", "?")] = {
            "equity": round(eq, 8),
            "available": float(d.get("availBal") or 0),
            "frozen": float(d.get("frozenBal") or 0),
            "usd_est": float(d.get("eqUsd") or 0),
            "spot_upl": float(d.get("spotUpl") or 0),
            "spot_upl_ratio": float(d.get("spotUplRatio") or 0),
        }

    # 2. Tickers
    prices: dict[str, float] = {}
    for inst_id in inst_ids:
        t = mkt.get_ticker(instId=inst_id)
        if t.get("code") == "0" and t.get("data"):
            try:
                prices[inst_id] = float(t["data"][0]["last"])
            except (KeyError, ValueError):
                pass

    # 3. 24h fills per instrument
    trading_summary: dict[str, dict] = {}
    for inst_id in inst_ids:
        fills = _fetch_24h_fills(trd, inst_id)
        trading_summary[inst_id] = _summarise_fills(fills)

    # 4. Pending orders count per instrument
    pending_counts: dict[str, int] = {}
    for inst_id in inst_ids:
        pend = trd.get_order_list(instId=inst_id)
        if pend.get("code") == "0":
            pending_counts[inst_id] = len(pend.get("data") or [])

    # 4b. Price-change history per instrument (1D / 1W / 1Y vs current).
    price_changes: dict[str, dict] = {}
    if not args.no_price_history:
        for inst_id in inst_ids:
            cur = prices.get(inst_id)
            if cur is None:
                continue
            try:
                price_changes[inst_id] = _price_changes(mkt, inst_id, cur)
            except Exception:
                # Don't let one instrument's history failure abort the snapshot.
                continue

    # 5. Active strategies
    strategies = list_strategies()
    strategy_summary = [
        {
            "id": s.get("id"),
            "kind": s.get("kind"),
            "instId": s.get("instId"),
            "active_orders": len(s.get("active_orders") or []),
            "fills": len([h for h in (s.get("history") or []) if h.get("event") is None]),
            "halted": s.get("halted", False),
            "halt_reason": s.get("halt_reason"),
            "rescales_used": s.get("rescales_used", 0),
        }
        for s in strategies
    ]

    # 6. Build the snapshot record + delta vs previous.
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    snapshot = {
        "timestamp": now.isoformat(),
        "date_utc": today_str,
        "env": "DEMO" if env_summary().endswith("flag=1)") else "LIVE",
        "total_equity_usd": round(total_equity_usd, 4),
        "assets": assets,
        "prices": prices,
        "price_changes": price_changes,
        "trading_summary_24h": trading_summary,
        "pending_orders": pending_counts,
        "strategies": strategy_summary,
    }
    prev = _previous_snapshot(today_str)
    delta = None
    if prev:
        prev_eq = float(prev.get("total_equity_usd") or 0)
        equity_change = round(total_equity_usd - prev_eq, 4)
        equity_change_pct = round((equity_change / prev_eq) * 100, 4) if prev_eq > 0 else 0.0
        asset_changes: dict[str, dict] = {}
        for ccy, cur in assets.items():
            prev_a = (prev.get("assets") or {}).get(ccy)
            if not prev_a:
                continue
            asset_changes[ccy] = {
                "equity_change": round(cur["equity"] - float(prev_a.get("equity") or 0), 8),
                "usd_change": round(cur["usd_est"] - float(prev_a.get("usd_est") or 0), 4),
            }
        delta = {
            "prev_date": prev.get("date_utc"),
            "equity_change_usd": equity_change,
            "equity_change_pct": equity_change_pct,
            "asset_changes": asset_changes,
        }
        snapshot["delta"] = delta

    # 7. Persist (unless --no-write).
    if not args.no_write:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        path = SNAPSHOT_DIR / f"{today_str}.json"
        path.write_text(json.dumps(snapshot, indent=2))

    # 8. Print human summary.
    print(env_summary())
    print(f"Snapshot {today_str}  total equity ~${total_equity_usd:.2f}")
    if delta:
        sign = "+" if delta["equity_change_usd"] >= 0 else ""
        pct_sign = "+" if delta["equity_change_pct"] >= 0 else ""
        print(f"  vs {delta['prev_date']}: {sign}${delta['equity_change_usd']:.2f} ({pct_sign}{delta['equity_change_pct']:.2f}%)")
    print()
    print("Balances:")
    for ccy, a in sorted(assets.items(), key=lambda kv: -kv[1]["usd_est"]):
        upl = f"  upl=${a['spot_upl']:+.2f}" if a["spot_upl"] else ""
        print(f"  {ccy:<6} {a['equity']:>14}  ~${a['usd_est']:.2f}{upl}")
    if price_changes:
        print()
        print("Price moves:")
        for inst_id, pc in price_changes.items():
            cur = pc.get("current") or 0.0
            parts = [f"  {inst_id:<14} ${cur:>12,.2f}"]
            for label, key in (("1D", "change_pct_1d"), ("1W", "change_pct_7d"), ("1Y", "change_pct_365d")):
                pct = pc.get(key)
                if pct is None:
                    parts.append(f"   {label}      n/a")
                else:
                    sign = "+" if pct >= 0 else ""
                    parts.append(f"   {label} {sign}{pct*100:>6.2f}%")
            print("".join(parts))

    if trading_summary:
        print()
        print("24h fills:")
        for inst_id, s in trading_summary.items():
            if s["fills"] == 0:
                continue
            net_sign = "+" if s["net_usdt"] >= 0 else ""
            print(
                f"  {inst_id:<14} {s['fills']:>3} fills  "
                f"buy={s['buy_count']}@{s['buy_avg'] or '-'}  sell={s['sell_count']}@{s['sell_avg'] or '-'}  "
                f"net={net_sign}${s['net_usdt']:.2f}  fees={s['fees']:.4f}"
            )
    if pending_counts:
        print()
        print("Pending orders: " + ", ".join(f"{k}={v}" for k, v in pending_counts.items()))
    if strategy_summary:
        print()
        print(f"Active strategies ({len(strategy_summary)}):")
        for s in strategy_summary:
            flags = " HALTED" if s["halted"] else ""
            print(
                f"  {s['id']:<22} {s['instId']:<14} active_orders={s['active_orders']}  "
                f"fills={s['fills']}  rescales={s['rescales_used']}{flags}"
            )
    if not args.no_write:
        print()
        print(f"Saved {SNAPSHOT_DIR}/{today_str}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
