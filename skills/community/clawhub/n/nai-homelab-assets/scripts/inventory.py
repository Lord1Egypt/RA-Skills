#!/usr/bin/env python3
"""List homelab assets with optional filters."""

import argparse
import json
import os
import sys
from datetime import datetime, date


INVENTORY_PATH = os.environ.get(
    "HOMELAB_ASSETS_PATH",
    os.path.expanduser("~/.openclaw/workspace/homelab-assets/inventory.json"),
)

VALID_TYPES = ["server", "switch", "router", "ups", "drive", "cable", "accessory", "other"]
VALID_STATUSES = ["active", "retired", "sold", "rma"]


def load_inventory(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def days_until(date_str):
    """Return days until a date string (YYYY-MM-DD). Negative = already past."""
    if not date_str:
        return None
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - date.today()).days
    except ValueError:
        return None


def apply_filters(assets, args):
    filtered = assets
    if args.type:
        filtered = [a for a in filtered if a.get("type") == args.type]
    if args.status:
        filtered = [a for a in filtered if a.get("status") == args.status]
    if args.location:
        loc = args.location.lower()
        filtered = [a for a in filtered if loc in a.get("location", "").lower()]
    if args.warranty_expiring is not None:
        result = []
        for a in filtered:
            d = days_until(a.get("warranty_expiry"))
            if d is not None and 0 <= d <= args.warranty_expiring:
                result.append(a)
        filtered = result
    return filtered


def truncate(s, length):
    s = str(s) if s is not None else ""
    return s if len(s) <= length else s[: length - 1] + "…"


def print_table(assets):
    if not assets:
        print("No assets found.")
        return

    # Column widths
    cols = {
        "name": max(len("Name"), max(len(a.get("name", "")) for a in assets)),
        "type": max(len("Type"), max(len(a.get("type", "")) for a in assets)),
        "brand_model": max(len("Brand/Model"), max(len(f"{a.get('brand','')} {a.get('model','')}".strip()) for a in assets)),
        "status": max(len("Status"), max(len(a.get("status", "")) for a in assets)),
        "price": len("Price"),
        "location": max(len("Location"), max(len(a.get("location", "")) for a in assets)),
        "warranty": len("Warranty"),
        "watts": len("Watts"),
    }
    # Cap some columns
    cols["name"] = min(cols["name"], 30)
    cols["brand_model"] = min(cols["brand_model"], 28)
    cols["location"] = min(cols["location"], 22)

    def row(name, type_, bm, status, price, location, warranty, watts):
        return (
            f"{name:<{cols['name']}}  "
            f"{type_:<{cols['type']}}  "
            f"{bm:<{cols['brand_model']}}  "
            f"{status:<{cols['status']}}  "
            f"{price:>{cols['price']}}  "
            f"{location:<{cols['location']}}  "
            f"{warranty:<{cols['warranty']}}  "
            f"{watts:<{cols['watts']}}"
        )

    header = row("Name", "Type", "Brand/Model", "Status", "Price", "Location", "Warranty", "Watts")
    divider = "-" * len(header)
    print(header)
    print(divider)

    for a in assets:
        bm = f"{a.get('brand', '')} {a.get('model', '')}".strip()
        price = f"${a['purchase_price']:.2f}" if a.get("purchase_price") is not None else "—"
        watts = f"{a['power_watts']}W" if a.get("power_watts") is not None else "—"

        warranty = "—"
        if a.get("warranty_expiry"):
            d = days_until(a["warranty_expiry"])
            if d is None:
                warranty = a["warranty_expiry"]
            elif d < 0:
                warranty = f"Expired"
            elif d == 0:
                warranty = "Expires today"
            else:
                warranty = f"{d}d left"

        print(row(
            truncate(a.get("name", ""), cols["name"]),
            truncate(a.get("type", ""), cols["type"]),
            truncate(bm, cols["brand_model"]),
            truncate(a.get("status", ""), cols["status"]),
            price,
            truncate(a.get("location", ""), cols["location"]),
            warranty,
            watts,
        ))

    print(divider)
    total_price = sum(a["purchase_price"] for a in assets if a.get("purchase_price") is not None)
    total_watts = sum(a["power_watts"] for a in assets if a.get("power_watts") is not None)
    print(f"Total: {len(assets)} assets  |  Investment: ${total_price:.2f}  |  Power: {total_watts:.1f}W")


def main():
    parser = argparse.ArgumentParser(description="List homelab assets with optional filters.")
    parser.add_argument("--type", choices=VALID_TYPES, help="Filter by asset type")
    parser.add_argument("--status", choices=VALID_STATUSES, help="Filter by status")
    parser.add_argument("--location", help="Filter by location (substring match)")
    parser.add_argument(
        "--warranty-expiring",
        type=int,
        metavar="DAYS",
        help="Show only assets with warranty expiring within N days",
    )
    parser.add_argument(
        "--output",
        choices=["table", "json"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--inventory",
        default=INVENTORY_PATH,
        help=f"Path to inventory JSON (default: {INVENTORY_PATH})",
    )
    args = parser.parse_args()

    inventory = load_inventory(args.inventory)
    if not inventory:
        print("No inventory found. Use add_asset.py to add your first asset.")
        return

    filtered = apply_filters(inventory, args)

    if args.output == "json":
        print(json.dumps(filtered, indent=2))
    else:
        print_table(filtered)


if __name__ == "__main__":
    main()
