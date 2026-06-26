#!/usr/bin/env python3
"""
Fetch order book data from Polymarket CLOB API using the polymarket CLI.

Replaces direct urllib HTTP calls with `polymarket clob book` subprocess calls.
Analysis logic (slippage, capacity, positioning) is preserved unchanged.

Usage:
    python fetch_orderbook_cli.py <token_id> [--slippage 0.02]
    python fetch_orderbook_cli.py <token_id_1> <token_id_2> ...
"""

import argparse
import json
import subprocess
import sys


def fetch_book(token_id: str) -> dict:
    """Fetch order book via polymarket CLI."""
    result = subprocess.run(
        ["polymarket", "clob", "book", token_id, "-o", "json"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        raise RuntimeError(f"CLI error: {result.stderr.strip()}")
    return json.loads(result.stdout)


def parse_float(val, default=0.0):
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def analyze_side(orders: list, side: str) -> dict:
    """Analyze one side (bids or asks) of the order book."""
    if not orders:
        return {"best_price": 0, "total_size": 0, "num_levels": 0, "depth": []}

    depth = []
    cumulative_size = 0
    cumulative_cost = 0

    for order in orders:
        price = parse_float(order.get("price"))
        size = parse_float(order.get("size"))
        if price <= 0 or size <= 0:
            continue
        cumulative_size += size
        cumulative_cost += price * size
        depth.append({
            "price": round(price, 4),
            "size": round(size, 2),
            "cumulative_size": round(cumulative_size, 2),
            "cumulative_cost": round(cumulative_cost, 2),
        })

    best_price = depth[0]["price"] if depth else 0

    return {
        "best_price": best_price,
        "total_size": round(cumulative_size, 2),
        "num_levels": len(depth),
        "depth": depth,
    }


def compute_max_order(depth: list, slippage: float, side: str) -> dict:
    """
    Compute maximum order size executable within a given slippage tolerance.
    For BUY: slippage = (execution_price - best_ask) / best_ask
    For SELL: slippage = (best_bid - execution_price) / best_bid
    """
    if not depth:
        return {"max_size": 0, "avg_price": 0, "worst_price": 0}

    best = depth[0]["price"]
    if best <= 0:
        return {"max_size": 0, "avg_price": 0, "worst_price": 0}

    max_size = 0
    total_cost = 0
    worst_price = best

    for level in depth:
        price = level["price"]
        size = level["size"]

        if side == "buy":
            price_impact = (price - best) / best if best > 0 else 0
        else:
            price_impact = (best - price) / best if best > 0 else 0

        if price_impact > slippage:
            break

        max_size += size
        total_cost += price * size
        worst_price = price

    avg_price = total_cost / max_size if max_size > 0 else 0

    return {
        "max_size": round(max_size, 2),
        "max_cost_usd": round(total_cost, 2),
        "avg_price": round(avg_price, 4),
        "worst_price": round(worst_price, 4),
    }


def analyze_orderbook(token_id: str, slippage: float) -> dict:
    print(f"[INFO] Fetching order book for token {token_id[:16]}... (via CLI)", file=sys.stderr)
    book = fetch_book(token_id)

    bids_raw = book.get("bids", [])
    asks_raw = book.get("asks", [])

    bids_sorted = sorted(bids_raw, key=lambda o: parse_float(o.get("price")), reverse=True)
    asks_sorted = sorted(asks_raw, key=lambda o: parse_float(o.get("price")))

    bids = analyze_side(bids_sorted, "bid")
    asks = analyze_side(asks_sorted, "ask")

    spread = round(asks["best_price"] - bids["best_price"], 4) if asks["best_price"] > 0 and bids["best_price"] > 0 else None
    spread_pct = round(spread / asks["best_price"] * 100, 2) if spread and asks["best_price"] > 0 else None
    midpoint = round((asks["best_price"] + bids["best_price"]) / 2, 4) if asks["best_price"] > 0 and bids["best_price"] > 0 else None

    buy_capacity = compute_max_order(asks["depth"], slippage, "buy")
    sell_capacity = compute_max_order(bids["depth"], slippage, "sell")

    return {
        "token_id": token_id,
        "midpoint": midpoint,
        "spread": spread,
        "spread_pct": spread_pct,
        "bids": {
            "best_price": bids["best_price"],
            "total_size": bids["total_size"],
            "num_levels": bids["num_levels"],
        },
        "asks": {
            "best_price": asks["best_price"],
            "total_size": asks["total_size"],
            "num_levels": asks["num_levels"],
        },
        "buy_capacity": {
            "slippage_tolerance": slippage,
            **buy_capacity,
        },
        "sell_capacity": {
            "slippage_tolerance": slippage,
            **sell_capacity,
        },
        "position_recommendation": position_recommendation(buy_capacity, sell_capacity, midpoint),
    }


def position_recommendation(buy_cap: dict, sell_cap: dict, midpoint: float) -> dict:
    buy_max = buy_cap.get("max_cost_usd", 0)
    sell_max = sell_cap.get("max_cost_usd", 0)
    capacity = min(buy_max, sell_max)

    if capacity >= 5000:
        tier = "high"
        suggested = "$1000-5000"
    elif capacity >= 1000:
        tier = "medium"
        suggested = "$200-1000"
    elif capacity >= 200:
        tier = "low"
        suggested = "$50-200"
    else:
        tier = "very_low"
        suggested = "<$50 (caution: thin liquidity)"

    return {
        "liquidity_tier": tier,
        "suggested_position_range": suggested,
        "two_way_capacity_usd": round(capacity, 2),
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch and analyze Polymarket order books (CLI version)")
    parser.add_argument("token_ids", nargs="+", help="CLOB token ID(s) to analyze")
    parser.add_argument("--slippage", type=float, default=0.02, help="Max slippage tolerance (default: 0.02 = 2%%)")
    parser.add_argument("--output", type=str, default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    results = []
    for tid in args.token_ids:
        try:
            analysis = analyze_orderbook(tid, args.slippage)
            results.append(analysis)
        except Exception as e:
            print(f"[ERROR] Failed to analyze {tid}: {e}", file=sys.stderr)
            results.append({"token_id": tid, "error": str(e)})

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
