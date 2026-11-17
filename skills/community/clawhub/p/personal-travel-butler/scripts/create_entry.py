#!/usr/bin/env python3
"""Create a Markdown travel database entry with stable frontmatter."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from travel_model import TYPE_DIRS, entry_id, parse_coordinates, require_valid_city, slugify, yaml_coordinates, yaml_list, yaml_scalar

BODY_TEMPLATES = {
    "place": """## Snapshot

- Why it matters:
- Best for:
- Signature items:
- Reservation:
- Hours:
- Budget:

## Notes

-

## Evidence

-

## Conflicts / Review

-
""",
    "guide": """## Summary


## Extracted Items

-

## Useful For

-

## Evidence

-
""",
    "trip": """## Intent


## Constraints

-

## Draft Plan

-

## Candidates

-
""",
    "preference": """## Preference


## Applies To

-

## Evidence

-
""",
}


def frontmatter(args: argparse.Namespace, entry_id_value: str, today: str) -> str:
    coordinates = parse_coordinates(args.coords)
    coordinates_yaml = f"\ncoordinates:{yaml_coordinates(coordinates)}" if coordinates else f"\ncoordinates: {yaml_coordinates(coordinates)}"
    return f"""---
id: {entry_id_value}
type: {args.type}
status: {args.status}
name: {yaml_scalar(args.name)}
city: {yaml_scalar(args.city)}
{coordinates_yaml.lstrip()}
tags: {yaml_list(args.tags)}
source: []
evidence: {yaml_list(args.evidence)}
priority: {args.priority}
last_verified: null
created_at: {today}
updated_at: {today}
---
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default="../travel-db", help="Path to the travel-db directory.")
    parser.add_argument("--type", choices=sorted(TYPE_DIRS), required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--city", default=None)
    parser.add_argument("--coords", default=None, help="Optional coordinates as LAT,LNG.")
    parser.add_argument("--status", default="active")
    parser.add_argument("--tag", dest="tags", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--priority", type=int, default=3)
    parser.add_argument("--date", default=None, help="Override today's date as YYYY-MM-DD.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= args.priority <= 5:
        raise SystemExit("priority must be between 1 and 5")
    try:
        args.city = require_valid_city(args.city)
        parse_coordinates(args.coords)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    today = args.date or date.today().isoformat()
    db_path = Path(args.db).expanduser().resolve()
    folder = db_path / TYPE_DIRS[args.type]
    eid = entry_id(args.type, args.name, args.city, today)
    city_prefix = f"{slugify(args.city)}-" if args.city else ""
    filename = f"{city_prefix}{slugify(args.name)}-{eid}.md"
    target = folder / filename

    content = frontmatter(args, eid, today) + "\n" + BODY_TEMPLATES[args.type]

    if args.dry_run:
        print(content)
        return 0

    folder.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {target}")
    target.write_text(content, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
