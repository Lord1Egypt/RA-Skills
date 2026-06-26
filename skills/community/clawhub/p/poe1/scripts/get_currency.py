#!/usr/bin/env python3
"""
Query poe.ninja currency data.

Usage:
    python get_currency.py --league Settlers
    python get_currency.py --league Settlers --search "divine"
    python get_currency.py --league Settlers --type Fragment
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Optional


BASE_URL = "https://poe.ninja/api/data/currencyoverview"


def fetch_currency(league: str, currency_type: str = "Currency") -> dict:
    """Fetch currency data from poe.ninja API."""
    url = f"{BASE_URL}?league={league}&type={currency_type}"

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
        return f"{num:.6f}"


def print_currency_table(data: dict, search: Optional[str] = None):
    """Print currency data in a formatted table."""
    lines = data.get("lines", [])
    currency_details = {d["id"]: d for d in data.get("currencyDetails", [])}

    # Filter by search term
    if search:
        search_lower = search.lower()
        lines = [l for l in lines if search_lower in l.get("currencyTypeName", "").lower()]

    if not lines:
        print("No currency found.")
        return

    # Print header
    print(f"{'Currency':<30} {'Chaos Value':>12} {'Change':>8} {'Listings':>10}")
    print("-" * 62)

    for line in lines:
        name = line.get("currencyTypeName", "Unknown")
        chaos_eq = line.get("chaosEquivalent", 0)
        change = line.get("paySparkLine", {}).get("totalChange", 0)
        listings = line.get("pay", {}).get("listingCount", 0)

        # Format change with color indicator
        change_str = f"{change:+.1f}%" if change else "N/A"

        print(f"{name:<30} {format_number(chaos_eq):>12} {change_str:>8} {listings:>10}")


def main():
    parser = argparse.ArgumentParser(description="Query poe.ninja currency prices")
    parser.add_argument("--league", required=True, help="League name (e.g., Settlers, Standard)")
    parser.add_argument("--type", default="Currency", choices=["Currency", "Fragment"],
                       help="Currency type (default: Currency)")
    parser.add_argument("--search", help="Filter by currency name")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    data = fetch_currency(args.league, args.type)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"\n{args.type} Prices - {args.league} League\n")
        print_currency_table(data, args.search)


if __name__ == "__main__":
    main()
