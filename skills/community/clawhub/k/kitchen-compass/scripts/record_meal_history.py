#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

from contract import HISTORY_EVENT_TYPES
from paths import KitchenCompassPaths, append_jsonl, resolve_data_root, write_atomic


def load_catalog(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing catalog: {path}. Run build_recipe_query_index.py first.")
    return json.loads(path.read_text())


def recipe_lookup(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {recipe["slug"]: recipe for recipe in payload.get("recipes", [])}


def normalize_recipe_slug(raw: str, payload: dict[str, Any]) -> str:
    recipes = recipe_lookup(payload)
    candidate = raw.strip().lower()
    if candidate in recipes:
        return candidate

    title_match = {recipe["title"].lower(): recipe["slug"] for recipe in payload.get("recipes", [])}
    if candidate in title_match:
        return title_match[candidate]

    raise SystemExit(f"Unknown recipe '{raw}'. Use a known slug from the query catalog.")


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        events.append(json.loads(line))
    return events


def append_event(path: Path, event: dict[str, Any]) -> None:
    append_jsonl(path, event)


def event_key(event: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        event.get("date", ""),
        event.get("recipe_slug", ""),
        event.get("meal_slot", ""),
        event.get("event_type", ""),
    )


def find_duplicate_index(events: list[dict[str, Any]], event: dict[str, Any]) -> int | None:
    key = event_key(event)
    for idx, existing in enumerate(events):
        if event_key(existing) == key:
            return idx
    return None


def rewrite_events(path: Path, events: list[dict[str, Any]]) -> None:
    body = "".join(json.dumps(e, sort_keys=True) + "\n" for e in events)
    write_atomic(path, body)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record simple Kitchen Compass meal history events.")
    parser.add_argument("--data-root", help="Household data root. Defaults to ./kitchen-compass-data, except when run from the installed skill root it defaults to ../kitchen-compass-data so household data stays outside the skill.")
    parser.add_argument("--verbose", action="store_true", help="Print the resolved data root to stderr.")
    parser.add_argument("--history-file", help="Override the history JSONL path.")
    parser.add_argument("--event-type", choices=list(HISTORY_EVENT_TYPES))
    parser.add_argument("--recipe", help="Recipe slug or exact title from the Kitchen Compass catalog.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--meal-slot", default="dinner")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--notes", default="")
    parser.add_argument("--show", action="store_true", help="Show recent events instead of appending a new one.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--quiet", action="store_true", help="Print a one-line confirmation instead of the full event JSON.")
    parser.add_argument("--silent", action="store_true", help="Suppress all stdout output.")
    duplicate_group = parser.add_mutually_exclusive_group()
    duplicate_group.add_argument("--allow-duplicate", action="store_true", help="Append even if an event with the same (date, recipe, meal_slot, event_type) already exists.")
    duplicate_group.add_argument("--replace", action="store_true", help="If a duplicate exists, rewrite the file so the new event replaces it.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    paths = KitchenCompassPaths.from_root(resolve_data_root(args.data_root, verbose=args.verbose))
    if args.history_file:
        history_path = Path(args.history_file).expanduser().resolve()
        try:
            history_path.relative_to(paths.data_root)
        except ValueError:
            raise SystemExit(
                f"--history-file must be inside --data-root ({paths.data_root}); got {history_path}"
            )
    else:
        history_path = paths.history_file

    if args.show:
        events = read_events(history_path)
        for event in events[-args.limit :]:
            print(json.dumps(event, indent=2, sort_keys=True))
        return

    if not args.event_type or not args.recipe:
        raise SystemExit("--event-type and --recipe are required unless using --show")

    payload = load_catalog(paths.generated_query_dir / "recipe-catalog.json")
    recipe_slug = normalize_recipe_slug(args.recipe, payload)
    event = {
        "date": args.date,
        "event_type": args.event_type,
        "meal_slot": args.meal_slot,
        "recipe_slug": recipe_slug,
        "source": args.source,
    }
    if args.notes:
        event["notes"] = args.notes

    events = read_events(history_path)
    duplicate_idx = find_duplicate_index(events, event)
    if duplicate_idx is not None and not args.allow_duplicate and not args.replace:
        print(
            f"[kitchen-compass] duplicate history event ({event['date']}, {event['recipe_slug']}, "
            f"{event['meal_slot']}, {event['event_type']}); skipping. Pass --allow-duplicate or --replace to override.",
            file=__import__('sys').stderr,
        )
        return

    if duplicate_idx is not None and args.replace:
        events[duplicate_idx] = event
        rewrite_events(history_path, events)
        verb = "replaced"
    else:
        append_event(history_path, event)
        verb = "recorded"

    if args.silent:
        return
    if args.quiet:
        print(f"{verb} history event: {event['date']} {event['recipe_slug']} ({event['event_type']})")
        return
    print(json.dumps(event, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
