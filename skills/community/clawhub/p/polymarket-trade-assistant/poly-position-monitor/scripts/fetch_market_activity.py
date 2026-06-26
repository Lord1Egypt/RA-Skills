#!/usr/bin/env python3
"""
Fetch market trading activity from the Polymarket Data API.

Two main functions:
1. Fetch recent trades for a market — compute volume metrics
2. Check if watched addresses have traded on specific markets

Usage:
    python fetch_market_activity.py trades --market <condition_id> [--limit 200]
    python fetch_market_activity.py whale --address <addr> --market <condition_id>
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

DATA_API = "https://data-api.polymarket.com"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "poly-position-monitor/1.0",
}


def fetch_with_retry(url: str, max_retries: int = 3, backoff: float = 1.0):
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError,
                http.client.IncompleteRead,
                http.client.RemoteDisconnected,
                TimeoutError,
                ConnectionResetError) as e:
            if attempt < max_retries - 1:
                wait = backoff * (2 ** attempt)
                print(f"[WARN] Retry {attempt + 1}/{max_retries}: {e}", file=sys.stderr)
                time.sleep(wait)
            else:
                raise


# ---------------------------------------------------------------------------
# Market trades
# ---------------------------------------------------------------------------

def fetch_market_trades(condition_id: str, limit: int = 200,
                        since_ts: int = None) -> list:
    """Fetch recent trades for a market."""
    params = {
        "market": condition_id,
        "limit": str(min(limit, 10000)),
    }
    if since_ts:
        params["start"] = str(since_ts)

    qs = urllib.parse.urlencode(params)
    url = f"{DATA_API}/trades?{qs}"
    data = fetch_with_retry(url)
    return data if isinstance(data, list) else []


def compute_volume_metrics(trades: list, interval_minutes: int = 60) -> dict:
    """
    Compute volume metrics from a list of trades.

    Returns:
        {
            "total_trades": int,
            "total_volume_usd": float,
            "buy_volume": float,
            "sell_volume": float,
            "interval_trades": int,        # trades in the last interval_minutes
            "interval_volume_usd": float,
            "largest_trade_usd": float,
            "largest_trade": dict | None,
        }
    """
    if not trades:
        return {
            "total_trades": 0, "total_volume_usd": 0,
            "buy_volume": 0, "sell_volume": 0,
            "interval_trades": 0, "interval_volume_usd": 0,
            "largest_trade_usd": 0, "largest_trade": None,
        }

    now = time.time()
    cutoff = now - (interval_minutes * 60)

    total_volume = 0
    buy_volume = 0
    sell_volume = 0
    interval_trades = 0
    interval_volume = 0
    largest_usd = 0
    largest_trade = None

    for t in trades:
        price = _pf(t.get("price"))
        size = _pf(t.get("size", t.get("amount")))
        usd = price * size
        total_volume += usd

        side = (t.get("side") or "").upper()
        if side == "BUY":
            buy_volume += usd
        else:
            sell_volume += usd

        trade_ts = _parse_trade_time(t)
        if trade_ts and trade_ts >= cutoff:
            interval_trades += 1
            interval_volume += usd

        if usd > largest_usd:
            largest_usd = usd
            largest_trade = {
                "side": side,
                "price": price,
                "size": size,
                "usd": round(usd, 2),
                "time": t.get("timestamp", t.get("createdAt", "")),
            }

    return {
        "total_trades": len(trades),
        "total_volume_usd": round(total_volume, 2),
        "buy_volume": round(buy_volume, 2),
        "sell_volume": round(sell_volume, 2),
        "interval_trades": interval_trades,
        "interval_volume_usd": round(interval_volume, 2),
        "largest_trade_usd": round(largest_usd, 2),
        "largest_trade": largest_trade,
    }


def check_volume_anomaly(current_volume: float, rolling_avg: float,
                         spike_ratio: float = 2.0,
                         drop_ratio: float = 0.3) -> dict | None:
    """
    Check if current volume is anomalous vs rolling average.

    Returns anomaly dict or None.
    """
    if rolling_avg <= 0:
        return None

    ratio = current_volume / rolling_avg

    if ratio >= spike_ratio:
        return {
            "type": "spike",
            "ratio": round(ratio, 2),
            "current": current_volume,
            "average": rolling_avg,
        }
    elif ratio <= drop_ratio and rolling_avg > 10:
        return {
            "type": "drop",
            "ratio": round(ratio, 2),
            "current": current_volume,
            "average": rolling_avg,
        }
    return None


# ---------------------------------------------------------------------------
# Whale / watched address activity
# ---------------------------------------------------------------------------

def fetch_address_activity(address: str, condition_id: str = None,
                           since_ts: int = None,
                           limit: int = 100) -> list:
    """Fetch recent activity for a specific address, optionally on a market."""
    params = {
        "user": address,
        "limit": str(min(limit, 500)),
        "type": "TRADE",
    }
    if condition_id:
        params["market"] = condition_id
    if since_ts:
        params["start"] = str(since_ts)

    qs = urllib.parse.urlencode(params)
    url = f"{DATA_API}/activity?{qs}"
    data = fetch_with_retry(url)
    return data if isinstance(data, list) else []


def check_whale_activity(watched_addresses: list[dict],
                         condition_ids: list[str],
                         since_ts: int = None) -> list[dict]:
    """
    Check if any watched addresses have traded on the given markets.

    Args:
        watched_addresses: [{"address": "0x...", "label": "Whale1"}, ...]
        condition_ids: list of market condition IDs to check
        since_ts: only report trades after this unix timestamp

    Returns: list of whale trade dicts
    """
    whale_trades = []

    for watcher in watched_addresses:
        addr = watcher["address"]
        label = watcher.get("label", addr[:10])

        for cid in condition_ids:
            activities = fetch_address_activity(addr, condition_id=cid, since_ts=since_ts)
            for act in activities:
                whale_trades.append({
                    "address": addr,
                    "label": label,
                    "condition_id": cid,
                    "side": act.get("side", ""),
                    "size": _pf(act.get("size", act.get("amount"))),
                    "price": _pf(act.get("price")),
                    "usd": round(
                        _pf(act.get("size", act.get("amount"))) *
                        _pf(act.get("price")), 2
                    ),
                    "title": act.get("title", ""),
                    "outcome": act.get("outcome", ""),
                    "timestamp": act.get("timestamp", act.get("createdAt", "")),
                })
            time.sleep(0.2)  # rate limit courtesy

    return whale_trades


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pf(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def _parse_trade_time(trade: dict) -> float | None:
    """Try to extract a unix timestamp from a trade record."""
    for key in ("timestamp", "createdAt", "created_at", "t"):
        val = trade.get(key)
        if val is None:
            continue
        if isinstance(val, (int, float)) and val > 1e9:
            return float(val)
        if isinstance(val, str):
            try:
                dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                return dt.timestamp()
            except (ValueError, TypeError):
                pass
            try:
                return float(val)
            except ValueError:
                pass
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch Polymarket market activity")
    sub = parser.add_subparsers(dest="command")

    trades_p = sub.add_parser("trades", help="Fetch trades for a market")
    trades_p.add_argument("--market", required=True, help="Condition ID")
    trades_p.add_argument("--limit", type=int, default=200)
    trades_p.add_argument("--output", type=str, default=None)

    whale_p = sub.add_parser("whale", help="Check whale activity on a market")
    whale_p.add_argument("--address", required=True, help="Watched address")
    whale_p.add_argument("--label", default=None, help="Label for the address")
    whale_p.add_argument("--market", required=True, help="Condition ID")
    whale_p.add_argument("--output", type=str, default=None)

    args = parser.parse_args()

    if args.command == "trades":
        trades = fetch_market_trades(args.market, limit=args.limit)
        metrics = compute_volume_metrics(trades)
        result = {"condition_id": args.market, "metrics": metrics}
    elif args.command == "whale":
        label = args.label or args.address[:10]
        watched = [{"address": args.address, "label": label}]
        whale_trades = check_whale_activity(watched, [args.market])
        result = {"whale_trades": whale_trades, "count": len(whale_trades)}
    else:
        parser.print_help()
        sys.exit(1)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
