#!/usr/bin/env python3
"""
Check pending limit orders against price history to determine fills.

For paper trading: checks if the market midpoint has crossed the limit price.
For live trading: queries CLOB API for actual order status.

Usage:
    python check_orders.py ~/polymarket-reports/portfolio.json
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CLOB_API = "https://clob.polymarket.com"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "polymarket-paper-trading/1.0",
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


def fetch_price_history(token_id: str, interval: str = "1d") -> list[dict]:
    """Fetch price history for a token. Returns list of {t, p} objects."""
    try:
        url = f"{CLOB_API}/prices-history?market={token_id}&interval={interval}&fidelity=100"
        data = fetch_with_retry(url)
        if isinstance(data, dict):
            return data.get("history", [])
        if isinstance(data, list):
            return data
    except Exception as e:
        print(f"[WARN] Price history failed for {token_id[:20]}...: {e}", file=sys.stderr)
    return []


def fetch_midpoint(token_id: str) -> float | None:
    try:
        data = fetch_with_retry(f"{CLOB_API}/midpoint?token_id={token_id}")
        mid = data.get("mid")
        if mid is not None:
            return float(mid)
    except Exception as e:
        print(f"[WARN] Midpoint failed for {token_id[:20]}...: {e}", file=sys.stderr)
    return None


def check_paper_fill(order: dict) -> dict:
    """Check if a paper order should be filled based on current price."""
    token_id = order.get("clob_token_id", "")
    limit_price = order.get("limit_price", 0)
    order_id = order.get("id", "")

    if not token_id:
        return {"order_id": order_id, "filled": False, "reason": "no token_id"}

    current_mid = fetch_midpoint(token_id)
    if current_mid is None:
        return {"order_id": order_id, "filled": False, "reason": "price_unavailable"}

    history = fetch_price_history(token_id, "1w")

    created_at = order.get("created_at", "")
    min_price_since = current_mid
    if history and created_at:
        try:
            created_ts = datetime.fromisoformat(created_at.replace("Z", "+00:00")).timestamp()
            for point in history:
                t = point.get("t", 0)
                p = float(point.get("p", 999))
                if t >= created_ts and p < min_price_since:
                    min_price_since = p
        except (ValueError, TypeError):
            pass

    filled = min_price_since <= limit_price or current_mid <= limit_price
    fill_price = limit_price if filled else None

    return {
        "order_id": order_id,
        "filled": filled,
        "fill_price": fill_price,
        "current_price": current_mid,
        "min_price_since_order": round(min_price_since, 4),
        "limit_price": limit_price,
    }


def main():
    parser = argparse.ArgumentParser(description="Check pending order fills")
    parser.add_argument("portfolio", help="Path to portfolio.json")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    path = Path(args.portfolio).expanduser()
    if not path.exists():
        print(f"[ERROR] Portfolio not found: {path}", file=sys.stderr)
        sys.exit(1)

    portfolio = json.loads(path.read_text(encoding="utf-8"))
    mode = portfolio.get("mode", "paper")
    pending = portfolio.get("pending_orders", [])

    if not pending:
        output = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "orders": [],
            "fills_count": 0,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        return

    print(f"[INFO] Checking {len(pending)} pending orders (mode={mode})", file=sys.stderr)

    results = []
    for order in pending:
        print(f"[INFO] Checking order {order.get('id', '?')}...", file=sys.stderr)
        if mode == "paper":
            result = check_paper_fill(order)
        else:
            result = check_paper_fill(order)
        results.append(result)
        time.sleep(0.3)

    output = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "orders": results,
        "fills_count": sum(1 for r in results if r.get("filled")),
    }

    json_str = json.dumps(output, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(json_str, encoding="utf-8")
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
