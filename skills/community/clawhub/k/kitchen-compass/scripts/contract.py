#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Iterable

SECTION_ORDER = [
    "## Snapshot",
    "## Ingredients",
    "## Instructions",
    "## House Tweaks / Change Log",
    "## Planning Notes",
    "## Notes",
]

SNAPSHOT_FIELDS = [
    ("Source", "source"),
    ("Status", "status"),
    ("Meal Type", "meal_type"),
    ("Structural Role", "structural_role"),
    ("Core Protein / Main Ingredient", "core_protein"),
    ("Serves", "serves"),
    ("Time", "time"),
    ("Cooking Effort", "cooking_effort"),
    ("Ingredient Friction", "ingredient_friction"),
    ("Cost", "cost"),
    ("Serving Profile", "serving_profile"),
    ("Diet Modes", "diet_modes"),
    ("Context / Occasion", "context_occasion"),
    ("Flexibility", "flexibility"),
    ("Pair With", "pair_with"),
    ("Tags", "tags"),
]

SNAPSHOT_LABELS = [label for label, _ in SNAPSHOT_FIELDS]
SNAPSHOT_TO_KEY = {label: key for label, key in SNAPSHOT_FIELDS}
FIELD_ORDER = [key for _, key in SNAPSHOT_FIELDS]

LIST_FIELDS = {
    "meal_type",
    "structural_role",
    "diet_modes",
    "context_occasion",
    "pair_with",
    "tags",
}

REQUIRED_FIELDS = {
    "source",
    "status",
    "meal_type",
    "structural_role",
    "core_protein",
    "serves",
    "time",
    "cooking_effort",
    "ingredient_friction",
    "cost",
    "serving_profile",
    "flexibility",
}

ENUM_CHOICES = {
    "status": ("trusted", "testing", "aspirational"),
    "meal_type": ("dinner", "side", "breakfast-brunch", "snack", "appetizer-party", "dessert", "component"),
    "structural_role": ("full-meal", "base", "component", "pairing", "filler-meal"),
    "cooking_effort": ("easy", "moderate", "involved"),
    "ingredient_friction": ("low", "medium", "high"),
    "cost": ("cheap", "medium", "expensive"),
    "serving_profile": ("small-table", "family-table", "crowd-friendly"),
    "flexibility": ("rigid", "some-flex", "forgiving"),
}
ENUM_VALUES = {key: set(values) for key, values in ENUM_CHOICES.items()}

ACTIVE_ENGINE_MEAL_TYPES = ("dinner", "side")
REQUIRED_PLANNING_LABELS = {"Composition"}
COMPOSITION_VALUES = ("self-contained", "wants-side", "needs-protein-pairing", "flexible")
COMPOSITION_VALUE_SET = set(COMPOSITION_VALUES)
COMPOSITION_NORMALIZATION_ALIASES = {
    "needs-protein": "needs-protein-pairing",
    "needs-protein-pairing": "needs-protein-pairing",
    "needs-protein-paired": "needs-protein-pairing",
    "needs-side": "wants-side",
    "wants-side": "wants-side",
    "side-needed": "wants-side",
    "self-contained": "self-contained",
    "mostly-self-contained": "self-contained",
    "standalone": "self-contained",
    "flexible": "flexible",
}

PAIR_WITH_KIND_CHOICES = ("protein", "side", "support", "general")
PAIR_WITH_KIND_ALIASES = {
    "protein": "protein",
    "side": "side",
    "support": "support",
    "general": "general",
    "condiment": "support",
}
ALLOWED_PAIR_WITH_PREFIXES = set(PAIR_WITH_KIND_ALIASES)
HISTORY_EVENT_TYPES = ("planned", "made")
INVENTORY_SCHEMA_VERSION = 1
INVENTORY_LOCATIONS = ("freezer", "fridge", "pantry", "other")
INVENTORY_KINDS = ("protein", "produce", "prepared", "other")
INVENTORY_PRIORITIES = ("normal", "prefer-soon", "low")
WEEKLY_DEAL_BRIEF_SCHEMA_VERSION = 1
WEEKLY_DEAL_SOURCE_TYPES = ("circular-url", "retailer-page", "pdf", "app-share", "manual-note")
WEEKLY_DEAL_STORE_STATUSES = ("active", "inactive")
WEEKLY_DEAL_ENTRY_ROLES = ("major-protein", "supporting-ingredient", "side", "other")
WEEKLY_DEAL_DISCOUNT_BASES = ("source-exposed", "computed")
WEEKLY_DEAL_DISPLAY_CATEGORIES = ("meat", "starch", "dairy", "fruit-veg", "beverages", "misc")

LABELED_BULLET_RE = re.compile(r"- \*\*(.+?):\*\*\s*(.*)")
NON_WORD_RE = re.compile(r"[^a-z0-9]+")


def split_list(value: str) -> list[str]:
    if not value.strip():
        return []
    return [part.strip() for part in value.split(",") if part.strip()]



def slugify(text: str) -> str:
    return NON_WORD_RE.sub("-", text.lower()).strip("-")



def extract_block(text: str, start_heading: str, end_heading: str | None = None) -> str:
    if start_heading not in text:
        return ""
    after = text.split(start_heading, 1)[1]
    if end_heading and end_heading in after:
        return after.split(end_heading, 1)[0]
    next_section = re.search(r"\n## ", after)
    if next_section:
        return after[: next_section.start()]
    return after



def iter_non_empty_lines(block: str) -> Iterable[str]:
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if line:
            yield line



def parse_labeled_bullet(line: str) -> tuple[str, str] | None:
    match = LABELED_BULLET_RE.match(line)
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()



def parse_snapshot_block(block: str) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    errors: list[str] = []
    seen_labels: set[str] = set()

    for line in iter_non_empty_lines(block):
        parsed = parse_labeled_bullet(line)
        if not parsed:
            errors.append(f"unexpected Snapshot line: {line}")
            continue
        label, value = parsed
        if label not in SNAPSHOT_TO_KEY:
            errors.append(f"unexpected Snapshot label: {label}")
            continue
        if label in seen_labels:
            errors.append(f"duplicate Snapshot label: {label}")
            continue
        seen_labels.add(label)
        fields[SNAPSHOT_TO_KEY[label]] = value

    for label in SNAPSHOT_LABELS:
        if label not in seen_labels:
            errors.append(f"missing Snapshot label: {label}")

    return fields, errors



def snapshot_fields_with_defaults(fields: dict[str, str]) -> dict[str, str | list[str]]:
    normalized: dict[str, str | list[str]] = {}
    for key in FIELD_ORDER:
        raw = fields.get(key, "")
        normalized[key] = split_list(raw) if key in LIST_FIELDS else raw
    return normalized



def parse_planning_notes_block(block: str) -> tuple[dict[str, str], list[str]]:
    notes: dict[str, str] = {}
    errors: list[str] = []

    for line in iter_non_empty_lines(block):
        parsed = parse_labeled_bullet(line)
        if not parsed:
            continue
        label, value = parsed
        if label in notes:
            errors.append(f"duplicate Planning Notes label: {label}")
            continue
        notes[label] = value

    for label in REQUIRED_PLANNING_LABELS:
        if label not in notes:
            errors.append(f"missing Planning Notes label: {label}")

    return notes, errors
