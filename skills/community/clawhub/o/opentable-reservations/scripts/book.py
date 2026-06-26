#!/usr/bin/env python3
"""
Build an OpenTable reservation confirmation link.

The actual reservation is completed by the user on OpenTable — this script
just produces the deep link that pre-fills the booking details page. No
account auth, no cards, nothing that could accidentally commit the user to
something they didn't approve.

Usage:
    python3 book.py --rid 123456 --date-time 2026-04-12T19:00 --party 2 \\
        --name "Carbone" --url-path carbone-new-york
"""
from __future__ import annotations

import argparse
import json
import sys
from urllib.parse import quote


def build_confirm_url(rid: str, date_time: str, party: int) -> str:
    return (
        "https://www.opentable.com/booking/details"
        f"?rid={quote(rid)}"
        f"&datetime={quote(date_time)}"
        f"&covers={party}"
    )


def build_profile_url(rid: str, url_path: str) -> str:
    if url_path:
        return f"https://www.opentable.com/r/{quote(url_path, safe='')}"
    return f"https://www.opentable.com/restaurant/profile/{quote(rid)}"


def main() -> int:
    p = argparse.ArgumentParser(description="Build OpenTable booking deep link")
    p.add_argument("--rid",        required=True, help="OpenTable restaurant id")
    p.add_argument("--date-time",  required=True, help="YYYY-MM-DDTHH:MM (local)")
    p.add_argument("--party",      type=int, required=True)
    p.add_argument("--name",       default="", help="Restaurant name (for display)")
    p.add_argument("--url-path",   default="", help="OpenTable slug if known (e.g. 'carbone-new-york')")
    args = p.parse_args()

    payload = {
        "restaurant":  args.name or f"rid {args.rid}",
        "date_time":   args.date_time,
        "party":       args.party,
        "confirm_url": build_confirm_url(args.rid, args.date_time, args.party),
        "profile_url": build_profile_url(args.rid, args.url_path),
    }
    print(json.dumps(payload, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
