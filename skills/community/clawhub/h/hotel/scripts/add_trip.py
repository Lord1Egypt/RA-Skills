#!/usr/bin/env python3
import argparse
import os
import sys
import uuid
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_trips, save_trips

def nights_between(check_in, check_out):
    d1 = datetime.fromisoformat(check_in)
    d2 = datetime.fromisoformat(check_out)
    return max(1, (d2 - d1).days)

def main():
    parser = argparse.ArgumentParser(description="Add a new trip")
    parser.add_argument("--destination", required=True)
    parser.add_argument("--check_in", required=True, help="YYYY-MM-DD")
    parser.add_argument("--check_out", required=True, help="YYYY-MM-DD")
    parser.add_argument("--budget_total", type=float)
    parser.add_argument("--purpose", default="general")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    trip_id = f"TRP-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    trip = {
        "id": trip_id,
        "destination": args.destination,
        "check_in": args.check_in,
        "check_out": args.check_out,
        "nights": nights_between(args.check_in, args.check_out),
        "budget_total": args.budget_total,
        "purpose": args.purpose,
        "notes": args.notes,
        "created_at": now,
        "updated_at": now
    }

    data = load_trips()
    data["trips"][trip_id] = trip
    save_trips(data)

    print(f"✓ Trip added: {trip_id}")
    print(f"  {args.destination} | {args.check_in} -> {args.check_out}")
    print(f"  Nights: {trip['nights']}")

if __name__ == "__main__":
    main()
