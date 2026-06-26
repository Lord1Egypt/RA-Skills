#!/usr/bin/env python3
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_hotels

def main():
    parser = argparse.ArgumentParser(description="Check if hotel is ready to book")
    parser.add_argument("--hotel_id", required=True)
    args = parser.parse_args()

    hotels = load_hotels().get("hotels", {})
    hotel = hotels.get(args.hotel_id)
    if not hotel:
        print(f"Hotel not found: {args.hotel_id}")
        sys.exit(1)

    missing = []
    if hotel.get("nightly_price") is None:
        missing.append("nightly_price")
    if not hotel.get("area"):
        missing.append("area")
    if not hotel.get("refund_policy"):
        missing.append("refund_policy")

    if missing:
        print(f"Not booking-ready: {hotel['name']}")
        print(f"Missing: {', '.join(missing)}")
    else:
        print(f"✓ Booking-ready: {hotel['name']}")
        print(f"  Refund policy: {hotel['refund_policy']}")
        print(f"  Area: {hotel['area']}")
        print(f"  Nightly price: {hotel['nightly_price']}")

if __name__ == "__main__":
    main()
