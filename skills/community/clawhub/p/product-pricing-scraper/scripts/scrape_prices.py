#!/usr/bin/env python3
"""Product pricing scraper — extract and compare prices across e-commerce sites."""

import argparse
import json
import re
import sys
import time
import random
from urllib.parse import quote_plus
from datetime import datetime, timezone

# --- Price normalization ---

CURRENCY_MAP = {"$": "USD", "€": "EUR", "£": "GBP", "¥": "JPY", "￥": "CNY", "₹": "INR"}


def parse_price(text: str) -> tuple[float | None, str | None]:
    """Extract numeric price and currency from raw text."""
    if not text:
        return None, None
    text = text.strip()
    currency = "USD"
    for sym, cur in CURRENCY_MAP.items():
        if sym in text:
            currency = cur
            break
    nums = re.findall(r"[\d,]+\.?\d*", text.replace(",", ""))
    if not nums:
        return None, currency
    return float(nums[0]), currency


def normalize_price(raw: str) -> dict:
    price, currency = parse_price(raw)
    return {"price": price, "currency": currency, "raw": raw}


# --- Output ---

def build_output(query: str, results: list[dict]) -> dict:
    prices = [r["price"] for r in results if r.get("price") is not None]
    summary = {}
    if prices:
        lowest_idx = min(range(len(prices)), key=lambda i: prices[i])
        highest_idx = max(range(len(prices)), key=lambda i: prices[i])
        summary = {
            "lowest": {"source": results[lowest_idx]["source"], "price": prices[lowest_idx]},
            "highest": {"source": results[highest_idx]["source"], "price": prices[highest_idx]},
            "average": round(sum(prices) / len(prices), 2),
            "median": round(sorted(prices)[len(prices) // 2], 2),
        }
    return {
        "query": query,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Product pricing scraper")
    parser.add_argument("query", help="Product name or URL to scrape")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    args = parser.parse_args()

    # Placeholder: in practice, use web_fetch or browser tool to scrape
    # This script provides the normalization and output structure
    print(f"[product-pricing-scraper] Query: {args.query}", file=sys.stderr)
    print("[product-pricing-scraper] Use web_fetch or browser tool to scrape, then pipe results here.", file=sys.stderr)

    # Example: read JSON results from stdin
    try:
        results = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        results = []

    output = build_output(args.query, results)

    out_str = json.dumps(output, indent=2, ensure_ascii=False) if args.format == "json" else ""
    if args.output:
        with open(args.output, "w") as f:
            f.write(out_str)
    else:
        print(out_str)


if __name__ == "__main__":
    main()
