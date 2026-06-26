from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

from planner.common import primary_structural_role, protein_family
from planner.presets import RECENT_WINDOW_DAYS


def parse_date(raw: str) -> date | None:
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def load_history_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line == "[]":
            continue
        event = json.loads(line)
        event_date = parse_date(event.get("date"))
        if event_date is None:
            continue
        event["parsed_date"] = event_date
        events.append(event)
    events.sort(key=lambda item: (item["parsed_date"], item.get("event_type", ""), item.get("recipe_slug", "")))
    return events


def history_event_weight(event: dict[str, Any]) -> float:
    return 1.0 if event.get("event_type") == "made" else 0.7


def build_history_context(events: list[dict[str, Any]], recipes_by_slug: dict[str, dict[str, Any]]) -> dict[str, Any]:
    dinner_events: list[dict[str, Any]] = []
    for event in events:
        if event.get("meal_slot") != "dinner":
            continue
        recipe = recipes_by_slug.get(event.get("recipe_slug", ""))
        if not recipe or "dinner" not in recipe.get("meal_type", []):
            continue
        dinner_events.append({**event, "recipe": recipe, "event_weight": history_event_weight(event)})

    if not dinner_events:
        return {
            "has_history": False,
            "event_count": 0,
            "recent_event_count": 0,
            "last_recipe_dates": {},
            "recent_protein_counts": Counter(),
            "recent_role_counts": Counter(),
            "recent_events": [],
        }

    latest_date = max(event["parsed_date"] for event in dinner_events)
    recent_events = [event for event in dinner_events if (latest_date - event["parsed_date"]).days <= RECENT_WINDOW_DAYS]

    last_recipe_dates: dict[str, date] = {}
    for event in dinner_events:
        last_recipe_dates[event["recipe_slug"]] = event["parsed_date"]

    recent_protein_counts: Counter[str] = Counter()
    recent_role_counts: Counter[str] = Counter()
    for event in recent_events:
        recent_protein_counts[protein_family(event["recipe"])] += event["event_weight"]
        recent_role_counts[primary_structural_role(event["recipe"])] += event["event_weight"]

    return {
        "has_history": True,
        "event_count": len(dinner_events),
        "recent_event_count": len(recent_events),
        "anchor_date": latest_date,
        "last_recipe_dates": last_recipe_dates,
        "recent_protein_counts": recent_protein_counts,
        "recent_role_counts": recent_role_counts,
        "recent_events": [
            {
                "date": event["parsed_date"].isoformat(),
                "event_type": event.get("event_type"),
                "event_weight": event["event_weight"],
                "recipe_slug": event.get("recipe_slug"),
                "title": event["recipe"]["title"],
            }
            for event in recent_events[-8:]
        ],
    }


def history_summary_for_output(history: dict[str, Any]) -> dict[str, Any] | None:
    if not history.get("has_history"):
        return None
    return {
        "anchor_date": history["anchor_date"].isoformat(),
        "event_count": history["event_count"],
        "recent_event_count": history["recent_event_count"],
        "recent_protein_counts": {key: round(value, 2) for key, value in sorted(history["recent_protein_counts"].items())},
        "recent_role_counts": {key: round(value, 2) for key, value in sorted(history["recent_role_counts"].items())},
        "recent_events": history["recent_events"],
    }
