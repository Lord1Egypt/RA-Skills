#!/usr/bin/env python3
from __future__ import annotations

"""Dedicated hidden-menu CLI. User text is accepted only as argv data."""

import argparse
import json

from search_maps import search_fancard


def main() -> None:
    parser = argparse.ArgumentParser(description="Nomtiq hidden-menu restaurant search")
    parser.add_argument("location", help="Location or neighborhood")
    parser.add_argument("--city", default="北京", help="City")
    parser.add_argument("--budget-low", type=int, default=80)
    parser.add_argument("--budget-high", type=int, default=300)
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    results = search_fancard(
        location=args.location,
        city=args.city,
        budget_low=max(0, args.budget_low),
        budget_high=max(0, args.budget_high),
    )[:3]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return
    for result in results:
        print(result.get("name", ""), result.get("blurb", ""))


if __name__ == "__main__":
    main()
