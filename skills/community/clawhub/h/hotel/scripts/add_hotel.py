#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_hotels, save_hotels, load_trips

def parse_csv(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def main():
    parser = argparse.ArgumentParser(description="Add hotel candidate")
    parser.add_argument("--trip_id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--nightly_price", type=float)
    parser.add_argument("--area")
    parser.add_argument("--amenities")
    parser.add_argument("--refund_policy", choices=["flexible", "moderate", "strict"], default="moderate")
    parser.add_argument("--walkability", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    trips = load_trips().get("trips", {})
    if args.trip_id not in trips:
        print(f"Trip not found: {args.trip_id}")
        sys.exit(1)

    hotel_id = f"HOT-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    hotel = {
        "id": hotel_id,
        "trip_id": args.trip_id,
        "name": args.name,
        "nightly_price": args.nightly_price,
        "area": args.area,
        "amenities": parse_csv(args.amenities),
        "refund_policy": args.refund_policy,
        "walkability": args.walkability,
        "notes": args.notes,
        "created_at": now,
        "updated_at": now
    }

    data = load_hotels()
    data["hotels"][hotel_id] = hotel
    save_hotels(data)

    print(f"✓ Hotel added: {hotel_id}")
    print(f"  {args.name}")
    print(f"  Trip: {args.trip_id}")

if __name__ == "__main__":
    main()
