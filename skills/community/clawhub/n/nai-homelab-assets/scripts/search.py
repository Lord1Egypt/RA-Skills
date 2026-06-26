#!/usr/bin/env python3
"""Fuzzy (substring) search across all homelab asset fields."""

import argparse
import json
import os
import sys


INVENTORY_PATH = os.environ.get(
    "HOMELAB_ASSETS_PATH",
    os.path.expanduser("~/.openclaw/workspace/homelab-assets/inventory.json"),
)


def load_inventory(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def search_assets(assets, query):
    q = query.lower()
    results = []
    for a in assets:
        searchable = " ".join(str(v) for v in [
            a.get("name", ""),
            a.get("brand", ""),
            a.get("model", ""),
            a.get("type", ""),
            a.get("location", ""),
            a.get("notes", ""),
            a.get("serial", ""),
            a.get("status", ""),
        ]).lower()
        if q in searchable:
            results.append(a)
    return results


def print_results(results, query):
    if not results:
        print(f"No assets found matching '{query}'.")
        return

    print(f"Found {len(results)} result(s) for '{query}':\n")
    for a in results:
        bm = f"{a.get('brand', '')} {a.get('model', '')}".strip()
        price = f"${a['purchase_price']:.2f}" if a.get("purchase_price") is not None else "—"
        watts = f"{a['power_watts']}W" if a.get("power_watts") is not None else "—"
        print(f"  [{a['id'][:8]}...]  {a['name']}")
        print(f"    Type:     {a.get('type', '—')}")
        if bm:
            print(f"    Model:    {bm}")
        print(f"    Status:   {a.get('status', '—')}")
        if a.get("location"):
            print(f"    Location: {a['location']}")
        if a.get("purchase_date"):
            print(f"    Purchased: {a['purchase_date']}  ({price})")
        if a.get("warranty_expiry"):
            print(f"    Warranty:  expires {a['warranty_expiry']}")
        if a.get("serial"):
            print(f"    Serial:   {a['serial']}")
        print(f"    Power:    {watts}")
        if a.get("notes"):
            print(f"    Notes:    {a['notes']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Search homelab assets by any field (case-insensitive substring match)."
    )
    parser.add_argument("query", help="Search term")
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--inventory",
        default=INVENTORY_PATH,
        help=f"Path to inventory JSON (default: {INVENTORY_PATH})",
    )
    args = parser.parse_args()

    inventory = load_inventory(args.inventory)
    if not inventory:
        print("No inventory found. Use add_asset.py to add assets first.")
        sys.exit(0)

    results = search_assets(inventory, args.query)

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        print_results(results, args.query)


if __name__ == "__main__":
    main()
