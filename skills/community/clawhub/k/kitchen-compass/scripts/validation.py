#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from contract import (
    ALLOWED_PAIR_WITH_PREFIXES,
    COMPOSITION_VALUES,
    COMPOSITION_VALUE_SET,
    ENUM_VALUES,
    LIST_FIELDS,
    REQUIRED_FIELDS,
    SECTION_ORDER,
    extract_block,
    parse_planning_notes_block,
    parse_snapshot_block,
    split_list,
)


def validate_section_order(text: str) -> list[str]:
    errors: list[str] = []
    positions: list[int] = []
    for heading in SECTION_ORDER:
        index = text.find(heading)
        if index == -1:
            errors.append(f"missing section: {heading}")
        positions.append(index)

    present_positions = [position for position in positions if position != -1]
    if len(present_positions) == len(SECTION_ORDER) and present_positions != sorted(present_positions):
        errors.append("section order does not match the canonical contract")
    return errors


def validate_title(text: str) -> list[str]:
    first_non_empty = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_non_empty.startswith("# "):
        return ["recipe must start with a level-1 markdown title like '# Recipe Name'"]
    if len(first_non_empty) <= 2:
        return ["recipe title cannot be empty"]
    return []


def validate_snapshot_values(fields: dict[str, str]) -> list[str]:
    errors: list[str] = []

    for key in REQUIRED_FIELDS:
        raw = fields.get(key, "")
        values = split_list(raw) if key in LIST_FIELDS else [raw.strip()] if raw.strip() else []
        if not values:
            errors.append(f"required field is empty: {key}")

    for key, allowed in ENUM_VALUES.items():
        raw = fields.get(key, "")
        values = split_list(raw) if key in LIST_FIELDS else [raw.strip()] if raw.strip() else []
        for value in values:
            if value not in allowed:
                errors.append(f"invalid {key} value: {value} (allowed: {', '.join(sorted(allowed))})")

    for entry in split_list(fields.get("pair_with", "")):
        if ":" not in entry:
            continue
        prefix = entry.split(":", 1)[0].strip().lower()
        if prefix not in ALLOWED_PAIR_WITH_PREFIXES:
            errors.append(
                f"invalid Pair With prefix: {prefix} (allowed: {', '.join(sorted(ALLOWED_PAIR_WITH_PREFIXES))})"
            )

    return errors


def validate_planning_values(notes: dict[str, str]) -> list[str]:
    errors: list[str] = []
    composition_values = split_list(notes.get("Composition", ""))
    if len(composition_values) != 1:
        errors.append("Composition must contain exactly one value")
        return errors

    composition = composition_values[0]
    if composition not in COMPOSITION_VALUE_SET:
        errors.append(
            f"invalid Composition value: {composition} (allowed: {', '.join(COMPOSITION_VALUES)})"
        )
    return errors


def validate_recipe(path: Path) -> list[str]:
    text = path.read_text()
    errors: list[str] = []
    errors.extend(validate_title(text))
    errors.extend(validate_section_order(text))

    snapshot_fields, snapshot_errors = parse_snapshot_block(extract_block(text, "## Snapshot", "## Ingredients"))
    errors.extend(snapshot_errors)
    errors.extend(validate_snapshot_values(snapshot_fields))

    planning_notes, planning_errors = parse_planning_notes_block(extract_block(text, "## Planning Notes", "## Notes"))
    errors.extend(planning_errors)
    errors.extend(validate_planning_values(planning_notes))
    return errors


def validate_recipe_paths(recipe_paths: list[Path]) -> list[tuple[Path, list[str]]]:
    failures: list[tuple[Path, list[str]]] = []
    for recipe_path in recipe_paths:
        errors = validate_recipe(recipe_path)
        if errors:
            failures.append((recipe_path, errors))
    return failures
