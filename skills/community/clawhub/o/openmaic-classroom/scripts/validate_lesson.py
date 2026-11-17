#!/usr/bin/env python3
"""Validate the portable OpenMAIC-inspired classroom JSON package."""
import json
import sys
from pathlib import Path


def validate(data):
    errors = []
    required_text = ("title", "audience")
    for key in required_text:
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key}: must be a non-empty string")
    duration = data.get("duration_minutes")
    if not isinstance(duration, int) or isinstance(duration, bool) or duration <= 0:
        errors.append("duration_minutes: must be a positive integer")
    for key in ("assumptions", "objectives", "agenda", "slides", "activities", "quiz", "homework"):
        if not isinstance(data.get(key), list):
            errors.append(f"{key}: must be an array")
    for index, item in enumerate(data.get("agenda", [])):
        if not isinstance(item, dict):
            errors.append(f"agenda[{index}]: must be an object")
            continue
        for key in ("title", "teacher_action", "learner_action", "check"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"agenda[{index}].{key}: must be a non-empty string")
        minutes = item.get("minutes")
        if not isinstance(minutes, int) or isinstance(minutes, bool) or minutes <= 0:
            errors.append(f"agenda[{index}].minutes: must be a positive integer")
    if isinstance(duration, int) and not isinstance(duration, bool) and all(
        isinstance(item, dict) and isinstance(item.get("minutes"), int) and not isinstance(item.get("minutes"), bool)
        for item in data.get("agenda", [])
    ):
        total = sum(item["minutes"] for item in data.get("agenda", []))
        if total != duration:
            errors.append(f"agenda minutes total {total}, expected duration_minutes {duration}")
    for section, fields in {
        "slides": ("title", "key_point", "teacher_notes"),
        "activities": ("title", "mode", "instructions", "expected_observation", "fallback"),
        "quiz": ("question", "answer", "explanation", "next_step"),
    }.items():
        for index, item in enumerate(data.get(section, [])):
            if not isinstance(item, dict):
                errors.append(f"{section}[{index}]: must be an object")
                continue
            for key in fields:
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"{section}[{index}].{key}: must be a non-empty string")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_lesson.py <lesson.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read valid UTF-8 JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("Top-level JSON value must be an object", file=sys.stderr)
        return 1
    errors = validate(data)
    if errors:
        print("Classroom package has errors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {data['title']} ({data['duration_minutes']} minutes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
