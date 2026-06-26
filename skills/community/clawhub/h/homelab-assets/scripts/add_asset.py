#!/usr/bin/env python3
"""Add a new hardware asset to the homelab inventory."""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, date


INVENTORY_PATH = os.environ.get(
    "HOMELAB_ASSETS_PATH",
    os.path.expanduser("~/.openclaw/workspace/homelab-assets/inventory.json"),
)

VALID_TYPES = ["server", "switch", "router", "ups", "drive", "cable", "accessory", "other"]


def load_inventory(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_inventory(path, assets):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(assets, f, indent=2)


def parse_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'. Use YYYY-MM-DD format.")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new hardware asset to the homelab inventory."
    )
    parser.add_argument("--name", required=True, help="Asset name (e.g. 'Raspberry Pi 4')")
    parser.add_argument(
        "--type",
        required=True,
        choices=VALID_TYPES,
        help=f"Asset type: {', '.join(VALID_TYPES)}",
    )
    parser.add_argument("--brand", default="", help="Brand/manufacturer")
    parser.add_argument("--model", default="", help="Model name or number")
    parser.add_argument("--purchase-date", type=parse_date, help="Purchase date (YYYY-MM-DD)")
    parser.add_argument("--purchase-price", type=float, help="Purchase price in USD")
    parser.add_argument("--warranty-months", type=int, help="Warranty duration in months")
    parser.add_argument("--power-watts", type=float, help="Estimated power draw in watts")
    parser.add_argument("--location", default="", help="Physical location (e.g. 'Rack Shelf 2')")
    parser.add_argument("--notes", default="", help="Additional notes")
    parser.add_argument("--serial", default="", help="Serial number")
    parser.add_argument(
        "--inventory",
        default=INVENTORY_PATH,
        help=f"Path to inventory JSON (default: {INVENTORY_PATH})",
    )
    args = parser.parse_args()

    # Compute warranty expiry
    warranty_expiry = None
    if args.purchase_date and args.warranty_months:
        pd = datetime.strptime(args.purchase_date, "%Y-%m-%d")
        year = pd.year + (pd.month - 1 + args.warranty_months) // 12
        month = (pd.month - 1 + args.warranty_months) % 12 + 1
        try:
            warranty_expiry = date(year, month, pd.day).strftime("%Y-%m-%d")
        except ValueError:
            # Handle end-of-month edge cases
            import calendar
            last_day = calendar.monthrange(year, month)[1]
            warranty_expiry = date(year, month, min(pd.day, last_day)).strftime("%Y-%m-%d")

    asset = {
        "id": str(uuid.uuid4()),
        "name": args.name,
        "type": args.type,
        "brand": args.brand,
        "model": args.model,
        "serial": args.serial,
        "purchase_date": args.purchase_date or "",
        "purchase_price": args.purchase_price,
        "warranty_months": args.warranty_months,
        "warranty_expiry": warranty_expiry,
        "power_watts": args.power_watts,
        "location": args.location,
        "status": "active",
        "notes": args.notes,
        "added_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }

    inventory = load_inventory(args.inventory)
    inventory.append(asset)
    save_inventory(args.inventory, inventory)

    print(f"✅ Added: {asset['name']}")
    print(f"   ID:       {asset['id']}")
    print(f"   Type:     {asset['type']}")
    if asset["brand"] or asset["model"]:
        bm = f"{asset['brand']} {asset['model']}".strip()
        print(f"   Model:    {bm}")
    if asset["purchase_price"] is not None:
        print(f"   Price:    ${asset['purchase_price']:.2f}")
    if asset["warranty_expiry"]:
        print(f"   Warranty: expires {asset['warranty_expiry']}")
    if asset["location"]:
        print(f"   Location: {asset['location']}")
    print(f"   Saved to: {args.inventory}")


if __name__ == "__main__":
    main()
