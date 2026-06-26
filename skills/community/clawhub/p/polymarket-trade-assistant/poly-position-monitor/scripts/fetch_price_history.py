#!/usr/bin/env python3
"""
Fetch price history from the Polymarket CLOB API and compute relative price
changes over multiple time windows (5m, 15m, 60m, 240m).

Usage:
    python fetch_price_history.py <token_id> [<token_id2> ...]
    python fetch_price_history.py <token_id> --windows 5,15,60,240
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta

CLOB_API = "https://clob.polymarket.com"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "poly-position-monitor/1.0",
}

DEFAULT_WINDOWS = [5, 15, 60, 240]


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


def fetch_price_history(token_id: str, interval: str = "6h",
                        fidelity: int = 1) -> list[dict]:
    """Fetch price history points. Returns list of {t: unix_ts, p: price}."""
    params = {
        "market": token_id,
        "interval": interval,
        "fidelity": str(fidelity),
    }
    qs = urllib.parse.urlencode(params)
    url = f"{CLOB_API}/prices-history?{qs}"
    data = fetch_with_retry(url)

    if isinstance(data, dict):
        return data.get("history", [])
    if isinstance(data, list):
        return data
    return []


def compute_price_changes(history: list[dict],
                          windows: list[int] = None) -> dict:
    """
    Compute relative price changes over specified windows (in minutes).

    Returns:
        {
            "current_price": float,
            "current_time": int,
            "changes": {
                "5m": {"price_then": float, "price_now": float, "change_pct": float, "window_min": int},
                "15m": {...},
                ...
            }
        }
    """
    if windows is None:
        windows = DEFAULT_WINDOWS

    if not history:
        return {"current_price": None, "current_time": None, "changes": {}}

    sorted_history = sorted(history, key=lambda x: x.get("t", 0))

    current = sorted_history[-1]
    current_price = float(current.get("p", 0))
    current_time = int(current.get("t", 0))

    changes = {}
    for window in windows:
        target_time = current_time - (window * 60)
        closest = _find_closest_point(sorted_history, target_time)
        if closest is None:
            changes[f"{window}m"] = {
                "price_then": None,
                "price_now": current_price,
                "change_pct": None,
                "window_min": window,
            }
            continue

        price_then = float(closest.get("p", 0))
        if price_then > 0:
            change_pct = (current_price / price_then) - 1.0
        else:
            change_pct = None

        changes[f"{window}m"] = {
            "price_then": price_then,
            "price_now": current_price,
            "change_pct": change_pct,
            "window_min": window,
            "time_then": int(closest.get("t", 0)),
        }

    return {
        "current_price": current_price,
        "current_time": current_time,
        "changes": changes,
    }


def _find_closest_point(sorted_history: list[dict], target_time: int) -> dict | None:
    """Binary-search for the data point closest to target_time."""
    if not sorted_history:
        return None

    lo, hi = 0, len(sorted_history) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_history[mid].get("t", 0) < target_time:
            lo = mid + 1
        else:
            hi = mid

    best = sorted_history[lo]
    if lo > 0:
        prev = sorted_history[lo - 1]
        if abs(prev.get("t", 0) - target_time) < abs(best.get("t", 0) - target_time):
            best = prev

    # Reject if the closest point is more than 2x the smallest window away
    if abs(best.get("t", 0) - target_time) > 600:
        return best  # still return but might be stale
    return best


def check_thresholds(price_data: dict, thresholds: dict) -> list[dict]:
    """
    Check price changes against thresholds.

    Args:
        price_data: output from compute_price_changes()
        thresholds: {"5m": 0.03, "15m": 0.15, "60m": 0.10, "240m": 0.20}

    Returns: list of breached threshold dicts
    """
    breaches = []
    changes = price_data.get("changes", {})

    for window_key, threshold in thresholds.items():
        change_info = changes.get(window_key)
        if not change_info or change_info.get("change_pct") is None:
            continue

        change_pct = change_info["change_pct"]
        if abs(change_pct) >= threshold:
            breaches.append({
                "window": window_key,
                "change_pct": change_pct,
                "threshold": threshold,
                "price_then": change_info["price_then"],
                "price_now": change_info["price_now"],
            })

    return breaches


def fetch_and_analyze(token_id: str, windows: list[int] = None,
                      thresholds: dict = None) -> dict:
    """Convenience: fetch history, compute changes, check thresholds."""
    history = fetch_price_history(token_id)
    price_data = compute_price_changes(history, windows)

    result = {
        "token_id": token_id,
        **price_data,
    }

    if thresholds:
        result["breaches"] = check_thresholds(price_data, thresholds)
    else:
        result["breaches"] = []

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch price history and compute changes")
    parser.add_argument("token_ids", nargs="+", help="CLOB token ID(s)")
    parser.add_argument("--windows", type=str, default="5,15,60,240",
                        help="Comma-separated window sizes in minutes (default: 5,15,60,240)")
    parser.add_argument("--interval", type=str, default="6h",
                        help="History interval (default: 6h)")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    windows = [int(w) for w in args.windows.split(",")]

    results = []
    for tid in args.token_ids:
        print(f"[INFO] Fetching price history for {tid[:16]}...", file=sys.stderr)
        history = fetch_price_history(tid, interval=args.interval)
        price_data = compute_price_changes(history, windows)
        results.append({"token_id": tid, **price_data})

    output = results[0] if len(results) == 1 else results
    json_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
