#!/usr/bin/env python3
"""Load, normalize, and validate the unified fingering-plan JSON format."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
HAND_DEFAULT_PLACEMENT = {"RH": "above", "LH": "below"}
HAND_SIZES = {"XXS", "XS", "S", "M", "L", "XL", "XXL"}
COORDINATE_UNITS = {"pdf_point", "pixel_top_left"}
MAX_PLAN_BYTES = 64 * 1024 * 1024
MAX_PLAN_NOTES = 250_000
MAX_PLAN_PAGES = 2_000


def load_plan(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"plan not found: {path}")
    if path.stat().st_size > MAX_PLAN_BYTES:
        raise ValueError("plan exceeds 64 MiB safety limit")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("plan root must be a JSON object")
    normalize_plan(data)
    return data


def save_plan(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def finite_number(value: Any, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def normalize_plan(data: dict[str, Any]) -> None:
    data.setdefault("schema_version", SCHEMA_VERSION)
    if str(data["schema_version"]) != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {data['schema_version']}")
    source = data.setdefault("source", {})
    if not isinstance(source, dict):
        raise ValueError("source must be an object")
    source.setdefault("type", "musicxml")
    settings = data.setdefault("settings", {})
    if not isinstance(settings, dict):
        raise ValueError("settings must be an object")
    settings.setdefault("hand_size", "M")
    settings.setdefault("lookahead", 0)
    pages = data.setdefault("pages", [])
    notes = data.setdefault("notes", [])
    if not isinstance(pages, list) or not isinstance(notes, list):
        raise ValueError("pages and notes must be arrays")
    if len(pages) > MAX_PLAN_PAGES or len(notes) > MAX_PLAN_NOTES:
        raise ValueError("plan exceeds page or note count safety limit")
    for note in notes:
        if isinstance(note, dict):
            hand = str(note.get("hand", "")).upper()
            note["hand"] = hand
            if hand in HAND_DEFAULT_PLACEMENT:
                note.setdefault("placement", HAND_DEFAULT_PLACEMENT[hand])
            note.setdefault("locked", note.get("source") == "existing")
            note.setdefault("source", "existing" if note.get("locked") else "unassigned")


def page_map(plan: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for index, page in enumerate(plan.get("pages", [])):
        if not isinstance(page, dict):
            raise ValueError(f"pages[{index}] must be an object")
        number = int(page.get("page", index + 1))
        if number in result:
            raise ValueError(f"duplicate page number: {number}")
        result[number] = page
    return result


def note_sort_key(note: dict[str, Any]) -> tuple[Any, ...]:
    return (
        str(note.get("part", "")),
        int(note.get("measure_index", 0)),
        finite_number(note.get("onset", 0), "onset"),
        int(note.get("staff", 0)),
        str(note.get("voice", "")),
        int(note.get("event_index", 0)),
        int(note.get("chord_row", 0)),
        int(note.get("pitch_midi", 0)),
    )
