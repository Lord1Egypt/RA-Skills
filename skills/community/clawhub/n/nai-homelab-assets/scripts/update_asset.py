#!/usr/bin/env python3
"""Update an existing asset's details in the homelab inventory."""

import argparse
import json
import os
import sys
from datetime import datetime


INVENTORY_PATH = os.environ.get(
    "HOMELAB_ASSETS_PATH",
    os.path.expanduser("~/.openclaw/workspace/homelab-assets/inventory.json"),
)

VALID_STATUSES = ["active", "retired", "sold", "rma"]


def load_inventory(path):
    if not os.path.exists(path):
        print(f"Error: Inventory not found at {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r") as f:
        return json.load(f)


def save_inventory(path, assets):
    with open(path, "w") as f:
        json.dump(assets, f, indent=2)


def find_by_id(assets, asset_id):
    for a in assets:
        if a["id"] == asset_id:
            return a
    return None


def find_by_search(assets, query):
    q = query.lower()
    matches = [
        a for a in assets
        if q in a.get("name", "").lower()
        or q in a.get("brand", "").lower()
        or q in a.get("model", "").lower()
        or q in a.get("location", "").lower()
    ]
    return matches


def main():
    parser = argparse.ArgumentParser(
        description="Update an existing asset in the homelab inventory."
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--id", help="Asset UUID to update")
    target.add_argument("--search", help="Search term to find asset by name/brand/model")

    parser.add_argument(
        "--status",
        choices=VALID_STATUSES,
        help=f"New status: {', '.join(VALID_STATUSES)}",
    )
    parser.add_argument("--location", help="New physical location")
    parser.add_argument("--notes", help="New/replacement notes")
    parser.add_argument("--power-watts", type=float, help="Updated power draw in watts")
    parser.add_argument(
        "--inventory",
        default=INVENTORY_PATH,
        help=f"Path to inventory JSON (default: {INVENTORY_PATH})",
    )
    args = parser.parse_args()

    # Require at least one field to update
    update_fields = {
        k: v for k, v in {
            "status": args.status,
            "location": args.location,
            "notes": args.notes,
            "power_watts": args.power_watts,
        }.items()
        if v is not None
    }

    if not update_fields:
        print("Error: Provide at least one field to update (--status, --location, --notes, --power-watts).", file=sys.stderr)
        sys.exit(1)

    inventory = load_inventory(args.inventory)

    if args.id:
        asset = find_by_id(inventory, args.id)
        if not asset:
            print(f"Error: No asset found with ID '{args.id}'", file=sys.stderr)
            sys.exit(1)
        targets = [asset]
    else:
        targets = find_by_search(inventory, args.search)
        if not targets:
            print(f"Error: No assets found matching '{args.search}'", file=sys.stderr)
            sys.exit(1)
        if len(targets) > 1:
            print(f"Found {len(targets)} matching assets:")
            for t in targets:
                print(f"  [{t['id'][:8]}...] {t['name']} — {t.get('brand', '')} {t.get('model', '')}".strip())
            print("\nUse --id to target a specific asset.", file=sys.stderr)
            sys.exit(1)

    asset = targets[0]
    old_vals = {k: asset.get(k) for k in update_fields}

    for field, value in update_fields.items():
        asset[field] = value
    asset["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    save_inventory(args.inventory, inventory)

    print(f"✅ Updated: {asset['name']} ({asset['id'][:8]}...)")
    for field, new_val in update_fields.items():
        old_val = old_vals[field]
        display_field = field.replace("_", "-")
        print(f"   {display_field}: {old_val!r} → {new_val!r}")


if __name__ == "__main__":
    main()
