#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_hotels, load_trips, load_preferences
from lib.scoring import score_hotel

def main():
    parser = argparse.ArgumentParser(description="Compare hotels for a trip")
    parser.add_argument("--trip_id", required=True)
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
    )

    print(f"Hotel comparison for {trip['destination']} ({trip['check_in']} -> {trip['check_out']})")
    print()

    for score, hotel in ranked:
        print(f"- {hotel['id']} | {hotel['name']} | score={score}")
        if hotel.get("nightly_price") is not None:
            print(f"  Nightly price: {hotel['nightly_price']}")
        print(f"  Area: {hotel.get('area') or 'n/a'}")
        print(f"  Refund: {hotel.get('refund_policy')}")
        print(f"  Amenities: {', '.join(hotel.get('amenities', [])) or 'none'}")
        print()

if __name__ == "__main__":
    main()
