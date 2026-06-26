#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_hotels, load_trips, load_preferences
from lib.scoring import score_hotel

def main():
    parser = argparse.ArgumentParser(description="Shortlist best-fit hotels")
    parser.add_argument("--trip_id", required=True)
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()

    trips = load_trips().get("trips", {})
    trip = trips.get(args.trip_id)
    if not trip:
        print(f"Trip not found: {args.trip_id}")
        sys.exit(1)

    hotels = [h for h in load_hotels().get("hotels", {}).values() if h.get("trip_id") == args.trip_id]
    prefs = load_preferences().get("preferences", {})

    if not hotels:
        print("No hotels found for this trip.")
        return

    ranked = sorted(
        [(score_hotel(h, trip=trip, preferences=prefs), h) for h in hotels],
        key=lambda x: x[0],
        reverse=True
    )[:args.top]

    print(f"Top {len(ranked)} hotel choice(s) for {trip['destination']}")
    print()

    labels = ["Top Pick", "Backup", "Backup"]
    for i, (score, hotel) in enumerate(ranked):
        label = labels[i] if i < len(labels) else "Option"
        print(f"{label} — {hotel['name']} ({hotel['id']})")
        print(f"  Score: {score}")
        print(f"  Area: {hotel.get('area') or 'n/a'}")
        if hotel.get("nightly_price") is not None:
            print(f"  Nightly price: {hotel['nightly_price']}")
        print()

if __name__ == "__main__":
    main()
