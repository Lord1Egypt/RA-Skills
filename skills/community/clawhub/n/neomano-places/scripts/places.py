#!/usr/bin/env python3
"""Search Google Places (New) text queries.

Requires GOOGLE_PLACES_API_KEY.
Outputs JSON by default.
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

BASE_URL = "https://places.googleapis.com"
API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "").strip()

FIELDS = [
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.rating",
    "places.userRatingCount",
    "places.types",
    "places.googleMapsUri",
    "places.websiteUri",
]


def request_json(path, payload=None):
    if not API_KEY:
        raise SystemExit("ERROR: missing GOOGLE_PLACES_API_KEY")
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, method="POST")
    req.add_header("X-Goog-Api-Key", API_KEY)
    req.add_header("X-Goog-FieldMask", ",".join(FIELDS))
    req.add_header("Content-Type", "application/json; charset=utf-8")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lng", type=float)
    ap.add_argument("--radius-m", type=int, default=5000)
    ap.add_argument("--open-now", action="store_true")
    ap.add_argument("--min-rating", type=float)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    payload = {
        "textQuery": args.query,
        "maxResultCount": args.limit,
    }
    if args.lat is not None and args.lng is not None:
        payload["locationBias"] = {
            "circle": {
                "center": {"latitude": args.lat, "longitude": args.lng},
                "radius": args.radius_m,
            }
        }
    if args.open_now:
        payload["openNow"] = True
    if args.min_rating is not None:
        payload["minRating"] = args.min_rating

    res = request_json("/v1/places:searchText", payload)
    places = res.get("places", [])
    if args.json:
        print(json.dumps(places, ensure_ascii=False, indent=2))
        return 0

    for i, p in enumerate(places, 1):
        name = p.get("displayName", {}).get("text", "")
        addr = p.get("formattedAddress", "")
        rating = p.get("rating")
        cnt = p.get("userRatingCount")
        print(f"{i}. {name}")
        if addr:
            print(f"   {addr}")
        if rating is not None:
            print(f"   rating: {rating} ({cnt or 0} reviews)")
        if p.get("googleMapsUri"):
            print(f"   maps: {p['googleMapsUri']}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
