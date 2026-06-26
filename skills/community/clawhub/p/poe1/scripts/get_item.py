#!/usr/bin/env python3
"""
Query poe.ninja item data.

Usage:
    python get_item.py --league Settlers --type UniqueWeapon
    python get_item.py --league Settlers --type SkillGem --search "Enlighten"
    python get_item.py --league Settlers --type DivinationCard --json
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Optional


BASE_URL = "https://poe.ninja/api/data/itemoverview"

ITEM_TYPES = [
    "Oil", "Incubator", "Scarab", "Fossil", "Resonator", "Essence",
    "DivinationCard", "SkillGem", "BaseType", "HelmetEnchant", "UniqueMap",
    "Map", "UniqueJewel", "UniqueFlask", "UniqueWeapon", "UniqueArmour",
    "UniqueAccessory", "Beast", "Vial", "DeliriumOrb", "Omen", "UniqueRelic",
    "ClusterJewel", "BlightedMap", "BlightRavagedMap", "Invitation", "Memory",
    "Coffin", "AllflameEmber"
]


def fetch_items(league: str, item_type: str) -> dict:
    """Fetch item data from poe.ninja API."""
    url = f"{BASE_URL}?league={league}&type={item_type}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "QClaw-PoeNinja/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)


def format_number(num: float) -> str:
    """Format number with appropriate precision."""
    if num >= 1000:
        return f"{num:,.0f}"
    elif num >= 1:
        return f"{num:.2f}"
    else:
        return f"{num:.4f}"


def print_item_table(data: dict, search: Optional[str] = None, limit: int = 20):
    """Print item data in a formatted table."""
    lines = data.get("lines", [])

    # Filter by search term
    if search:
        search_lower = search.lower()
        lines = [l for l in lines if search_lower in l.get("name", "").lower()]

    if not lines:
        print("No items found.")
        return

    # Sort by chaos value (highest first)
    lines = sorted(lines, key=lambda x: x.get("chaosValue", 0), reverse=True)

    # Limit results
    lines = lines[:limit]

    # Print header
    print(f"{'Item Name':<40} {'Chaos':>10} {'Divine':>8} {'Change':>8} {'Listings':>10}")
    print("-" * 78)

    for line in lines:
        name = line.get("name", "Unknown")
        chaos = line.get("chaosValue", 0)
        divine = line.get("divineValue", 0)
        change = line.get("sparkline", {}).get("totalChange", 0)
        listings = line.get("listingCount", 0)

        # Truncate long names
        name_display = name[:38] + ".." if len(name) > 40 else name

        # Format change
        change_str = f"{change:+.1f}%" if change else "N/A"

        print(f"{name_display:<40} {format_number(chaos):>10} {divine:>8.2f} {change_str:>8} {listings:>10}")


def main():
    parser = argparse.ArgumentParser(description="Query poe.ninja item prices")
    parser.add_argument("--league", required=True, help="League name (e.g., Settlers, Standard)")
    parser.add_argument("--type", required=True, choices=ITEM_TYPES,
                       help="Item type to query")
    parser.add_argument("--search", help="Filter by item name")
    parser.add_argument("--limit", type=int, default=20, help="Maximum items to display (default: 20)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    data = fetch_items(args.league, args.type)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"\n{args.type} Prices - {args.league} League\n")
        print_item_table(data, args.search, args.limit)


if __name__ == "__main__":
    main()
