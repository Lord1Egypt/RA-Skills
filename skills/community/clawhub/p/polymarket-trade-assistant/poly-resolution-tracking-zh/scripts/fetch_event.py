#!/usr/bin/env python3
"""
Fetch a single Polymarket event by slug or URL.

Retrieves event metadata and all sub-markets (prices, outcomes, liquidity, description).

Usage:
    python fetch_event.py <slug_or_url>
    python fetch_event.py which-company-has-the-best-ai-model-end-of-february
    python fetch_event.py https://polymarket.com/event/which-company-has-the-best-ai-model-end-of-february
"""

import argparse
import http.client
import json
import re
import sys
import time
import urllib.request
import urllib.parse

GAMMA_API = "https://gamma-api.polymarket.com"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "poly-resolution-tracking/1.0",
}


def fetch_with_retry(url: str, headers: dict, max_retries: int = 3, backoff: float = 1.0):
    """Fetch a URL with exponential-backoff retry on transient errors."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError,
                http.client.IncompleteRead,
                http.client.RemoteDisconnected,
                TimeoutError,
                ConnectionResetError) as e:
            if attempt < max_retries - 1:
                wait = backoff * (2 ** attempt)
                print(f"[WARN] Retry {attempt + 1}/{max_retries} for {url[:80]}... ({e})", file=sys.stderr)
                time.sleep(wait)
            else:
                raise


def parse_float(val, default=0.0):
    if val is None:
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def parse_json_string(val):
    """Parse a value that may be a JSON-encoded string."""
    if isinstance(val, str):
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return []
    return val if val else []


def extract_slug(input_str: str) -> str:
    """Extract event slug from a URL or return as-is if already a slug."""
    url_match = re.match(r'https?://(?:www\.)?polymarket\.com/event/([^/?#]+)', input_str)
    if url_match:
        return url_match.group(1)
    return input_str.strip().strip('/')


def extract_market_info(m: dict, event_slug: str = "", event_title: str = "") -> dict:
    """Extract and normalize fields from a raw market dict."""
    outcomes = parse_json_string(m.get("outcomes", ""))
    outcome_prices = parse_json_string(m.get("outcomePrices", ""))
    clob_token_ids = parse_json_string(m.get("clobTokenIds", ""))
    prices = [parse_float(p) for p in outcome_prices] if outcome_prices else []

    slug_for_url = event_slug or m.get("slug", "")
    market_url = f"https://polymarket.com/event/{slug_for_url}" if slug_for_url else ""

    return {
        "id": m.get("id"),
        "condition_id": m.get("conditionId", ""),
        "slug": m.get("slug", ""),
        "event_slug": event_slug,
        "event_title": event_title,
        "url": market_url,
        "question": m.get("question", ""),
        "description": m.get("description") or "",
        "outcomes": outcomes,
        "outcome_prices": prices,
        "clob_token_ids": clob_token_ids,
        "liquidity": parse_float(m.get("liquidityNum", m.get("liquidity"))),
        "volume_24hr": parse_float(m.get("volume24hr")),
        "volume_total": parse_float(m.get("volumeNum", m.get("volume"))),
        "best_bid": parse_float(m.get("bestBid")),
        "best_ask": parse_float(m.get("bestAsk")),
        "spread": parse_float(m.get("spread")),
        "last_trade_price": parse_float(m.get("lastTradePrice")),
        "end_date": m.get("endDate", ""),
        "active": m.get("active", False),
        "closed": m.get("closed", False),
    }


def fetch_event(slug: str) -> dict:
    """Fetch event data from Gamma API by slug."""
    url = f"{GAMMA_API}/events?slug={urllib.parse.quote(slug)}"
    events = fetch_with_retry(url, HEADERS)

    if not events:
        print(f"[ERROR] No event found for slug: {slug}", file=sys.stderr)
        sys.exit(1)

    event = events[0]
    event_slug = event.get("slug", "")
    event_title = event.get("title", "")

    raw_markets = event.get("markets", [])
    markets = [extract_market_info(m, event_slug, event_title) for m in raw_markets]

    # Sort by price (highest first for multi-outcome)
    markets.sort(key=lambda x: max(x["outcome_prices"]) if x["outcome_prices"] else 0, reverse=True)

    return {
        "event_id": event.get("id", ""),
        "slug": event_slug,
        "title": event_title,
        "description": event.get("description", ""),
        "url": f"https://polymarket.com/event/{event_slug}" if event_slug else "",
        "start_date": event.get("startDate", ""),
        "end_date": event.get("endDate", ""),
        "liquidity": parse_float(event.get("liquidityNum", event.get("liquidity"))),
        "volume": parse_float(event.get("volumeNum", event.get("volume"))),
        "markets_count": len(markets),
        "markets": markets,
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch a Polymarket event by slug or URL")
    parser.add_argument("slug", help="Event slug or full Polymarket URL")
    parser.add_argument("--output", type=str, default=None, help="Output file path (default: stdout)")
    args = parser.parse_args()

    slug = extract_slug(args.slug)
    print(f"[INFO] Fetching event: {slug}", file=sys.stderr)

    result = fetch_event(slug)
    print(f"[INFO] Found event: {result['title']}", file=sys.stderr)
    print(f"[INFO] Sub-markets: {result['markets_count']}", file=sys.stderr)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
