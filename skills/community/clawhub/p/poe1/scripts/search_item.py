#!/usr/bin/env python3
"""
Search for items across all item types.

Usage:
    python search_item.py --league Settlers --query "Mirror"
    python search_item.py --league Settlers --query "Headhunter" --min-price 100
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed


BASE_URL = "https://poe.ninja/api/data"

ITEM_TYPES = [
    ("currencyoverview", "Currency"),
    ("currencyoverview", "Fragment"),
    ("itemoverview", "Oil"),
    ("itemoverview", "Incubator"),
    ("itemoverview", "Scarab"),
    ("itemoverview", "Fossil"),
    ("itemoverview", "Resonator"),
    ("itemoverview", "Essence"),
    ("itemoverview", "DivinationCard"),
    ("itemoverview", "SkillGem"),
    ("itemoverview", "BaseType"),
    ("itemoverview", "HelmetEnchant"),
    ("itemoverview", "UniqueMap"),
    ("itemoverview", "Map"),
    ("itemoverview", "UniqueJewel"),
    ("itemoverview", "UniqueFlask"),
    ("itemoverview", "UniqueWeapon"),
    ("itemoverview", "UniqueArmour"),
    ("itemoverview", "UniqueAccessory"),
    ("itemoverview", "Beast"),
    ("itemoverview", "Vial"),
    ("itemoverview", "DeliriumOrb"),
    ("itemoverview", "Omen"),
    ("itemoverview", "UniqueRelic"),
    ("itemoverview", "ClusterJewel"),
    ("itemoverview", "BlightedMap"),
    ("itemoverview", "BlightRavagedMap"),
    ("itemoverview", "Invitation"),
    ("itemoverview", "Memory"),
    ("itemoverview", "Coffin"),
    ("itemoverview", "AllflameEmber"),
]


def fetch_data(league: str, endpoint: str, item_type: str) -> tuple:
    """Fetch data from a specific endpoint."""
    url = f"{BASE_URL}/{endpoint}?league={league}&type={item_type}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QClaw-PoeNinja/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return (item_type, json.loads(response.read().decode("utf-8")))
    except Exception:
        return (item_type, None)


def search_items(league: str, query: str, min_price: float = 0) -> list:
    """Search for items across all types."""
    results = []
    query_lower = query.lower()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_data, league, endpoint, item_type): item_type
            for endpoint, item_type in ITEM_TYPES
        }

        for future in as_completed(futures):
            item_type, data = future.result()

            if not data:
                continue

            lines = data.get("lines", [])

            for line in lines:
                # Get name based on data type
                name = line.get("name") or line.get("currencyTypeName", "")
                if not name:
                    continue

                if query_lower not in name.lower():
                    continue

                # Get price
                chaos_value = line.get("chaosValue") or line.get("chaosEquivalent", 0)

                if chaos_value < min_price:
                    continue

                results.append({
                    "name": name,
                    "type": item_type,
                    "chaosValue": chaos_value,
                    "divineValue": line.get("divineValue", 0),
                    "change": line.get("sparkline", {}).get("totalChange", 0) or
                              line.get("paySparkLine", {}).get("totalChange", 0),
                    "listings": line.get("listingCount", 0) or
                               line.get("pay", {}).get("listingCount", 0)
                })

    return sorted(results, key=lambda x: x["chaosValue"], reverse=True)


def format_number(num: float) -> str:
    """Format number with appropriate precision."""
    if num >= 1000:
        return f"{num:,.0f}"
    elif num >= 1:
        return f"{num:.2f}"
    else:
        return f"{num:.4f}"


def main():
    parser = argparse.ArgumentParser(description="Search items across all types")
    parser.add_argument("--league", required=True, help="League name")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--min-price", type=float, default=0, help="Minimum chaos price")
    parser.add_argument("--limit", type=int, default=30, help="Maximum results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    print(f"Searching for '{args.query}' in {args.league}...")
    results = search_items(args.league, args.query, args.min_price)

    if args.json:
        print(json.dumps(results[:args.limit], indent=2))
        return

    if not results:
        print("No items found.")
        return

    print(f"\nFound {len(results)} items (showing top {min(args.limit, len(results))}):\n")
    print(f"{'Item Name':<35} {'Type':<18} {'Chaos':>12} {'Divine':>8}")
    print("-" * 75)

    for item in results[:args.limit]:
        name = item["name"][:33] + ".." if len(item["name"]) > 35 else item["name"]
        print(f"{name:<35} {item['type']:<18} {format_number(item['chaosValue']):>12} {item['divineValue']:>8.2f}")


if __name__ == "__main__":
    main()
