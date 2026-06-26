#!/usr/bin/env python3

from __future__ import annotations

import argparse
import pathlib
import sys
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib
from datetime import datetime


SCHEMAS = {
    "learning_candidates": {
        "required_keys": {
            "target_class",
            "schema_version",
            "updated_at",
            "candidate_status",
        },
        "enum": {
            "candidate_status": {"candidate", "discarded", "promoted"},
        },
        "required_headings": {"## Candidates"},
    },
    "proactive_state": {
        "required_keys": {
            "target_class",
            "schema_version",
            "updated_at",
            "state_mode",
            "current_objective",
            "current_blocker",
            "next_move",
        },
        "enum": {
            "state_mode": {"combined", "split-slice"},
        },
        "required_headings": {"## Current Task State", "## Durable Boundaries"},
    },
    "working_buffer": {
        "required_keys": {
            "target_class",
            "schema_version",
            "updated_at",
            "task_ref",
            "buffer_status",
        },
        "enum": {
            "buffer_status": {"active", "stale", "cleared"},
        },
        "required_headings": {"## Breadcrumbs"},
    },
    "reusable_lessons": {
        "required_keys": {
            "target_class",
            "schema_version",
            "updated_at",
            "scope",
        },
        "enum": {
            "scope": {"global", "domain", "project"},
        },
        "required_headings": {"## Lessons"},
    },
}


def extract_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("+++\n"):
        raise ValueError("missing TOML frontmatter start delimiter")

    end = text.find("\n+++\n", 4)
    if end == -1:
        raise ValueError("missing TOML frontmatter end delimiter")

    raw = text[4:end]
    body = text[end + 5 :]
    return tomllib.loads(raw), body


def validate_updated_at(value: object) -> str | None:
    if not isinstance(value, str):
        return "updated_at must be a string"

    normalized = value.replace("Z", "+00:00")
    try:
        datetime.fromisoformat(normalized)
    except ValueError:
        return "updated_at must be ISO-8601, e.g. 2026-03-31T00:00:00Z"
    return None


def validate_file(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    try:
        frontmatter, body = extract_frontmatter(text)
    except Exception as exc:  # noqa: BLE001
        return [f"{path}: {exc}"]

    target_class = frontmatter.get("target_class")
    if target_class not in SCHEMAS:
        return [f"{path}: unknown target_class {target_class!r}"]

    schema = SCHEMAS[target_class]

    missing = sorted(schema["required_keys"] - frontmatter.keys())
    for key in missing:
        errors.append(f"{path}: missing required key {key!r}")

    updated_at_error = validate_updated_at(frontmatter.get("updated_at"))
    if updated_at_error:
        errors.append(f"{path}: {updated_at_error}")

    for key, values in schema["enum"].items():
        if key in frontmatter and frontmatter[key] not in values:
            allowed = ", ".join(sorted(values))
            errors.append(f"{path}: {key} must be one of [{allowed}]")

    for heading in sorted(schema["required_headings"]):
        if heading not in body:
            errors.append(f"{path}: missing required heading {heading!r}")

    if frontmatter.get("target_class") == "proactive_state":
        if frontmatter.get("state_mode") == "combined" and "## Current Task State" not in body:
            errors.append(f"{path}: combined proactive_state must include current task state section")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate memory-governor TOML frontmatter files.")
    parser.add_argument("paths", nargs="+", help="Markdown files to validate")
    args = parser.parse_args()

    errors: list[str] = []
    for raw_path in args.paths:
        path = pathlib.Path(raw_path)
        if not path.exists():
            errors.append(f"{path}: file does not exist")
            continue
        errors.extend(validate_file(path))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    for raw_path in args.paths:
        print(f"OK {raw_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
