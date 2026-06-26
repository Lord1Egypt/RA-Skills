#!/usr/bin/env python3
"""
Fetch current prices and settlement status for all positions in a portfolio.

Reads portfolio.json, queries Polymarket APIs for each position and pending order,
and outputs updated price/status data.

Usage:
    python fetch_prices.py ~/polymarket-reports/portfolio.json
    python fetch_prices.py ~/polymarket-reports/portfolio.json --output prices.json
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GAMMA_API = "https://gamma-api.polymarket.com"
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


def fetch_midpoint(token_id: str) -> float | None:
    try:
        data = fetch_with_retry(f"{CLOB_API}/midpoint?token_id={token_id}")
        mid = data.get("mid")
        if mid is not None:
            return float(mid)
    except Exception as e:
        print(f"[WARN] Midpoint fetch failed for {token_id[:20]}...: {e}", file=sys.stderr)
    return None


def fetch_market_by_slug(event_slug: str) -> dict | None:
    try:
        url = f"{GAMMA_API}/events/slug/{event_slug}"
        data = fetch_with_retry(url)
        return data
    except Exception as e:
        print(f"[WARN] Event fetch failed for {event_slug}: {e}", file=sys.stderr)
    return None


def resolve_clob_token_ids(event_slug: str) -> tuple[str, str] | None:
    """Resolve event slug to (yes_token_id, no_token_id)."""
    event = fetch_market_by_slug(event_slug)
    if not event:
        return None
    markets = event.get("markets", [])
    if not markets:
        return None
    market = markets[0]
    ids_raw = market.get("clobTokenIds", "")
    if isinstance(ids_raw, str):
        try:
            ids_raw = json.loads(ids_raw)
        except (json.JSONDecodeError, TypeError):
            return None
    if isinstance(ids_raw, list) and len(ids_raw) >= 2:
        return (ids_raw[0], ids_raw[1])
    return None


def check_market_status(event_slug: str) -> dict:
    """Check if a market is closed/settled."""
    event = fetch_market_by_slug(event_slug)
    if not event:
        return {"closed": None, "outcome_prices": []}

    markets = event.get("markets", [])
    if not markets:
        return {"closed": None, "outcome_prices": []}

    market = markets[0]
    closed = market.get("closed", False)

    outcome_prices_raw = market.get("outcomePrices", "")
    if isinstance(outcome_prices_raw, str):
        try:
            outcome_prices_raw = json.loads(outcome_prices_raw)
        except (json.JSONDecodeError, TypeError):
            outcome_prices_raw = []

    prices = []
    for p in outcome_prices_raw:
        try:
            prices.append(float(p))
        except (ValueError, TypeError):
            prices.append(0.0)

    end_date = market.get("endDate", "")

    return {
        "closed": closed,
        "outcome_prices": prices,
        "end_date": end_date,
        "market_id": market.get("id", ""),
    }


def process_positions(positions: list) -> list[dict]:
    results = []
    for pos in positions:
        token_id = pos.get("clob_token_id", "")
        event_slug = pos.get("event_slug", "")
        pos_id = pos.get("id", "")

        print(f"[INFO] Checking position {pos_id}: {pos.get('question', '')[:50]}...", file=sys.stderr)

        current_price = None
        if token_id:
            current_price = fetch_midpoint(token_id)

        status = {"closed": None, "outcome_prices": []}
        if event_slug:
            status = check_market_status(event_slug)

        entry_price = pos.get("entry_price", 0)
        shares = pos.get("shares", 0)
        cost_basis = pos.get("cost_basis", entry_price * shares)
        current_value = (current_price or entry_price) * shares

        is_settled = False
        exit_price = None
        actual_result = None
        if status.get("closed"):
            prices = status.get("outcome_prices", [])
            if prices and (max(prices) >= 0.95 or min(prices) <= 0.05):
                is_settled = True
                direction = pos.get("direction", "Yes")
                if direction == "Yes":
                    exit_price = prices[0] if prices else 0
                else:
                    exit_price = prices[1] if len(prices) > 1 else 0

                if exit_price >= 0.95:
                    exit_price = 1.0
                    actual_result = direction
                else:
                    exit_price = 0.0
                    actual_result = "No" if direction == "Yes" else "Yes"

        result = {
            "position_id": pos_id,
            "current_price": current_price,
            "current_value": round(current_value, 2) if current_price else None,
            "unrealized_pnl": round(current_value - cost_basis, 2) if current_price else None,
            "is_settled": is_settled,
            "exit_price": exit_price,
            "actual_result": actual_result,
            "market_closed": status.get("closed"),
            "market_id": status.get("market_id", ""),
        }
        results.append(result)

        time.sleep(0.3)

    return results


def process_pending_orders(orders: list) -> list[dict]:
    results = []
    for order in orders:
        token_id = order.get("clob_token_id", "")
        order_id = order.get("id", "")

        print(f"[INFO] Checking order {order_id}...", file=sys.stderr)

        current_price = None
        if token_id:
            current_price = fetch_midpoint(token_id)

        limit_price = order.get("limit_price", 0)
        should_fill = False
        if current_price is not None and limit_price > 0:
            if current_price <= limit_price:
                should_fill = True

        results.append({
            "order_id": order_id,
            "current_price": current_price,
            "limit_price": limit_price,
            "should_fill": should_fill,
        })

        time.sleep(0.3)

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch prices for portfolio positions")
    parser.add_argument("portfolio", help="Path to portfolio.json")
    parser.add_argument("--output", type=str, default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    path = Path(args.portfolio).expanduser()
    if not path.exists():
        print(f"[ERROR] Portfolio not found: {path}", file=sys.stderr)
        sys.exit(1)

    portfolio = json.loads(path.read_text(encoding="utf-8"))
    positions = portfolio.get("positions", [])
    pending = portfolio.get("pending_orders", [])

    print(f"[INFO] Processing {len(positions)} positions, {len(pending)} pending orders", file=sys.stderr)

    position_results = process_positions(positions)
    order_results = process_pending_orders(pending)

    output = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "positions": position_results,
        "pending_orders": order_results,
        "positions_count": len(position_results),
        "settled_count": sum(1 for p in position_results if p["is_settled"]),
        "orders_to_fill": sum(1 for o in order_results if o["should_fill"]),
    }

    json_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(json_str, encoding="utf-8")
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
