#!/usr/bin/env python3
"""
nft-floor-price-monitor: Monitor NFT collection floor prices
Usage: uv run python scripts/floor_monitor.py --collection bored-ape-yacht-club --target 80 --discord
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime, timezone


# ── API Endpoints ──────────────────────────────────────────────────────────────

# OpenSea API v2 (REST)
OPENSEA_V2_COLLECTION = "https://api.opensea.io/api/v2/collections/{slug}"

# OpenSea API v1 (fallback)
OPENSEA_V1_COLLECTION = "https://api.opensea.io/api/v1/collection/{slug}"

# CoinGecko simple crypto price (for ETH/USD conversion reference)
COINGECKO_SIMPLE_PRICE = "https://api.coingecko.com/api/v3/simple/price"

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg: str):
    print(f"[{datetime.now(timezone.utc):%H:%M:%S}] {msg}", file=sys.stderr)


def fetch_json(url: str, headers=None, params=None, timeout=15) -> dict | None:
    try:
        resp = requests.get(url, headers=headers or {}, params=params or {}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log(f"Fetch error for {url}: {e}")
        return None


def get_floor_price_opensea_v2(slug: str, api_key: str = "") -> float | None:
    """Get floor price from OpenSea API v2."""
    url = OPENSEA_V2_COLLECTION.format(slug=slug)
    headers = {"Accept": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    data = fetch_json(url, headers=headers)
    if not data:
        return None
    # v2 response structure: { "collection": { "floor_price": number } }
    coll = data.get("collection", {})
    return coll.get("floor_price") or coll.get("floor_price_v2")


def get_floor_price_opensea_v1(slug: str) -> float | None:
    """Get floor price from OpenSea API v1."""
    url = OPENSEA_V1_COLLECTION.format(slug=slug)
    headers = {"Accept": "application/json"}
    data = fetch_json(url, headers=headers)
    if not data:
        return None
    # v1 response: { "collection": { "stats": { "floor_price": number } } }
    stats = data.get("collection", {}).get("stats", {})
    return stats.get("floor_price")


def get_eth_price_in_currency(currency: str = "usd") -> float:
    """Get current ETH price in given currency. Defaults to 1 (ETH native = 1 ETH)."""
    params = {"ids": "ethereum", "vs_currencies": currency}
    data = fetch_json(COINGECKO_SIMPLE_PRICE, params=params)
    if not data:
        return 1.0
    eth_data = data.get("ethereum", {})
    price = eth_data.get(currency, 1.0)
    return price if price else 1.0


def get_floor_price(collection_slug: str) -> dict:
    """Get floor price from OpenSea v2 + v1, return best estimate in ETH."""
    results = {}
    api_key = os.getenv("OPENSEA_API_KEY", "")

    # OpenSea v2 (preferred)
    os_price = get_floor_price_opensea_v2(collection_slug, api_key)
    if os_price is not None:
        results["opensea_v2"] = os_price

    time.sleep(0.7)

    # OpenSea v1 (fallback)
    os_price_v1 = get_floor_price_opensea_v1(collection_slug)
    if os_price_v1 is not None:
        results["opensea_v1"] = os_price_v1

    # Pick the best (non-null)
    for source in ["opensea_v2", "opensea_v1"]:
        if source in results and results[source]:
            return {
                "floor_price": results[source],
                "source": source,
                "all_sources": results,
            }

    return {"floor_price": None, "source": None, "all_sources": results}


def check_alert(floor_price: float, target: float, direction: str) -> bool:
    if floor_price is None:
        return False
    if direction == "below":
        return floor_price <= target
    else:
        return floor_price >= target


def send_discord_alert(collection_slug: str, floor_price: float, target: float,
                       direction: str, webhook_url: str = ""):
    """Send Discord embed alert via webhook."""
    if not webhook_url:
        webhook_url = DISCORD_WEBHOOK_URL
    if not webhook_url:
        log("No Discord webhook URL set. Skipping DM.")
        return False

    emoji = "📉" if direction == "below" else "📈"
    direction_text = "dropped to or below" if direction == "below" else "risen to or above"
    color = 0x00AE86 if direction == "below" else 0xFF4444

    payload = {
        "embeds": [{
            "title": f"{emoji} NFT Floor Alert: {collection_slug}",
            "description": f"**{collection_slug.upper()}** floor has {direction_text} your target!\n\n"
                           f"**Target:** {target} ETH\n"
                           f"**Current Floor:** {floor_price} ETH",
            "color": color,
            "footer": {
                "text": "NFT Floor Monitor • OpenClaw"
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }]
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        resp.raise_for_status()
        log("Discord alert sent successfully.")
        return True
    except Exception as e:
        log(f"Discord alert error: {e}")
        return False


def compare_collections(slugs: list) -> list:
    """Get floor prices for multiple collections."""
    results = []
    for slug in slugs:
        log(f"Fetching floor for {slug}...")
        data = get_floor_price(slug)
        results.append({
            "collection": slug,
            "floor_price": data["floor_price"],
            "source": data["source"],
        })
        time.sleep(1.0)  # Respect rate limits
    return results


def build_report(collection_slug: str, floor_price: float, source: str,
                 target: float = None, direction: str = "below") -> str:
    """Build a formatted text report."""
    if floor_price is None:
        return f"""
========================================
      NFT FLOOR REPORT: {collection_slug}
========================================
  Status: Could not fetch floor price
  Tip: Check the collection slug is correct
  Example slugs: bored-ape-yacht-club,
                 mutant-ape-yacht-club,
                 doodles
========================================"""

    report = f"""
========================================
      NFT FLOOR REPORT: {collection_slug}
========================================
  Collection:       {collection_slug}
  Floor Price:       {floor_price} ETH
  Source:            {source.upper() if source else 'N/A'}
========================================"""

    if target:
        triggered = check_alert(floor_price, target, direction)
        status = "🚨 TRIGGERED" if triggered else "✅ Safe"
        report += f"""
  Alert Target:      {target} ETH ({direction})
  Alert Status:       {status}
========================================"""

    return report.strip()


def main():
    parser = argparse.ArgumentParser(description="NFT Floor Price Monitor")
    parser.add_argument("--collection", required=True,
                        help="Collection slug (e.g. bored-ape-yacht-club)")
    parser.add_argument("--target", type=float, help="Target floor price in ETH for alert")
    parser.add_argument("--direction", choices=["above", "below"], default="below",
                        help="Direction to trigger alert (default: below)")
    parser.add_argument("--discord", action="store_true",
                        help="Send Discord DM alert when triggered")
    parser.add_argument("--discord-webhook", default="",
                        help="Discord webhook URL (or set DISCORD_WEBHOOK_URL env var)")
    parser.add_argument("--compare", type=int, const=3, nargs="?", metavar="N",
                        help="Compare N collections (pass --collections list)")
    parser.add_argument("--collections", default="",
                        help="Comma-separated list of collection slugs for --compare")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format")
    args = parser.parse_args()

    # ── Compare mode ────────────────────────────────────────────────────────────
    if args.compare:
        slugs_raw = args.collections or input(
            "Enter collection slugs (comma-separated): ")
        slugs = [s.strip() for s in slugs_raw.split(",") if s.strip()][:args.compare]
        if not slugs:
            print("ERROR: No collections provided for comparison.", file=sys.stderr)
            sys.exit(1)

        results = compare_collections(slugs)
        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            print("\n========================================")
            print("       NFT FLOOR COMPARISON")
            print("========================================")
            for r in results:
                fp = r["floor_price"]
                emoji = "✅" if fp else "❌"
                print(f"  {emoji} {r['collection']}: {fp} ETH ({r['source'] or 'N/A'})")
            print("========================================")
        sys.exit(0)

    # ── Single collection ────────────────────────────────────────────────────────
    collection = args.collection
    log(f"Fetching floor for: {collection}")

    data = get_floor_price(collection)
    floor_price = data["floor_price"]
    source = data["source"]

    # Check alert
    triggered = False
    if args.target and floor_price is not None:
        triggered = check_alert(floor_price, args.target, args.direction)

    # Output
    if args.output == "json":
        result = {
            "collection": collection,
            "floor_price": floor_price,
            "source": source,
            "all_sources": data.get("all_sources"),
            "target": args.target,
            "direction": args.direction,
            "alert_triggered": triggered,
        }
        print(json.dumps(result, indent=2))
    else:
        report = build_report(collection, floor_price, source or "N/A",
                              args.target, args.direction)
        print(report)
        print()
        if triggered:
            print("🚨 ALERT TRIGGERED!")
        else:
            print("✅ No alert triggered.")

    # Send Discord alert if triggered
    if triggered and args.discord:
        webhook = args.discord_webhook or DISCORD_WEBHOOK_URL
        if webhook:
            send_discord_alert(collection, floor_price, args.target,
                               args.direction, webhook)
        else:
            log("WARNING: --discord set but no webhook URL. Set DISCORD_WEBHOOK_URL env var.")


if __name__ == "__main__":
    main()
