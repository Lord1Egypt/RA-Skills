#!/usr/bin/env python3
"""
Fetch current positions for one or more wallet addresses from the Polymarket
Data API.

Usage:
    python fetch_positions.py <address> [<address2> ...]
    python fetch_positions.py 0x1234... --min-size 10 --output positions.json
"""

import argparse
import http.client
import json
import sys
import time
import urllib.request
import urllib.parse

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


def fetch_positions(address: str, limit: int = 500, min_size: float = 0) -> list:
    """Fetch all open positions for a wallet address."""
    all_positions = []
    offset = 0

    while True:
        params = {
            "user": address,
            "limit": str(min(limit, 500)),
            "offset": str(offset),
            "sortBy": "CURRENT",
            "sortDirection": "DESC",
        }
        if min_size > 0:
            params["sizeThreshold"] = str(min_size)

        qs = urllib.parse.urlencode(params)
        url = f"{DATA_API}/positions?{qs}"
        data = fetch_with_retry(url)

        if not data:
            break

        all_positions.extend(data)
        if len(data) < limit:
            break
        offset += limit

    return all_positions


def normalize_position(pos: dict) -> dict:
    """Extract key fields from a raw position record."""
    def pf(val, default=0.0):
        try:
            return float(val)
        except (ValueError, TypeError):
            return default

    return {
        "market_id": pos.get("conditionId", pos.get("market", "")),
        "asset_id": pos.get("assetId", pos.get("asset", "")),
        "title": pos.get("title", ""),
        "outcome": pos.get("outcome", ""),
        "size": pf(pos.get("size", pos.get("currentValue"))),
        "avg_price": pf(pos.get("avgPrice")),
        "current_value": pf(pos.get("currentValue")),
        "initial_value": pf(pos.get("initialValue")),
        "cash_pnl": pf(pos.get("cashPnl")),
        "percent_pnl": pf(pos.get("percentPnl")),
        "cur_price": pf(pos.get("curPrice")),
        "event_slug": pos.get("eventSlug", ""),
        "event_title": pos.get("eventTitle", ""),
        "end_date": pos.get("endDate", ""),
        "redeemable": pos.get("redeemable", False),
        "mergeable": pos.get("mergeable", False),
        "raw": pos,
    }


def fetch_all_positions(addresses: list[str], min_size: float = 0) -> dict:
    """Fetch positions for multiple addresses. Returns {address: [positions]}."""
    result = {}
    for addr in addresses:
        print(f"[INFO] Fetching positions for {addr[:10]}...", file=sys.stderr)
        raw = fetch_positions(addr, min_size=min_size)
        positions = [normalize_position(p) for p in raw]
        active = [p for p in positions if not p["redeemable"]]
        result[addr] = active
        print(f"[INFO]   {len(active)} active positions ({len(raw)} total)", file=sys.stderr)
    return result


def get_monitored_markets(positions_by_addr: dict) -> dict:
    """Build a deduplicated dict of markets from positions: {condition_id: market_info}."""
    markets = {}
    for addr, positions in positions_by_addr.items():
        for pos in positions:
            mid = pos["market_id"]
            if mid and mid not in markets:
                markets[mid] = {
                    "condition_id": mid,
                    "asset_id": pos["asset_id"],
                    "title": pos["title"],
                    "event_slug": pos["event_slug"],
                    "event_title": pos["event_title"],
                    "end_date": pos["end_date"],
                }
    return markets


def main():
    parser = argparse.ArgumentParser(description="Fetch Polymarket positions for wallet addresses")
    parser.add_argument("addresses", nargs="+", help="Wallet address(es) to query")
    parser.add_argument("--min-size", type=float, default=0, help="Minimum token size filter")
    parser.add_argument("--output", type=str, default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    positions_by_addr = fetch_all_positions(args.addresses, min_size=args.min_size)
    markets = get_monitored_markets(positions_by_addr)

    output = {
        "positions": {addr: ps for addr, ps in positions_by_addr.items()},
        "monitored_markets": markets,
        "total_positions": sum(len(ps) for ps in positions_by_addr.values()),
        "total_markets": len(markets),
    }

    # Strip raw field for cleaner output
    for addr in output["positions"]:
        for p in output["positions"][addr]:
            p.pop("raw", None)

    json_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w") as f:
            f.write(json_str)
        print(f"[INFO] Output written to {args.output}", file=sys.stderr)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
