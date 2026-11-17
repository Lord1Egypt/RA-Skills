#!/usr/bin/env python3
"""Update an existing place entry without hand-editing Markdown."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from notion_common import resolve_db  # noqa: E402
from travel_model import (  # noqa: E402
    clean_list,
    dedupe_text_list,
    normalize_city_name,
    parse_frontmatter_file,
    today_iso,
    yaml_coordinates,
    yaml_list,
    yaml_scalar,
)


FRONTMATTER_ORDER = (
    "id",
    "type",
    "status",
    "name",
    "aliases",
    "city",
    "province",
    "address",
    "coordinates",
    "tags",
    "source",
    "evidence",
    "phone",
    "website",
    "priority",
    "last_verified",
    "created_at",
    "updated_at",
)


def yaml_value(value: Any, indent: int = 2) -> list[str]:
    prefix = " " * indent
    if isinstance(value, list):
        if not value:
            return ["[]"]
        lines: list[str] = []
        for item in value:
            if isinstance(item, dict):
                first = True
                for key, inner in item.items():
                    marker = "- " if first else "  "
                    lines.append(f"{prefix}{marker}{key}: {yaml_scalar(inner)}")
                    first = False
            else:
                lines.append(f"{prefix}- {yaml_scalar(item)}")
        return [""] + lines
    if isinstance(value, dict):
        if set(value) == {"lat", "lng"}:
            return [yaml_coordinates(value)]
        if not value:
            return ["{}"]
        return [""] + [f"{prefix}{key}: {yaml_scalar(inner)}" for key, inner in value.items()]
    return [yaml_scalar(value)]


def render_frontmatter(data: dict[str, Any]) -> str:
    keys = [key for key in FRONTMATTER_ORDER if key in data]
    keys.extend(key for key in data if key not in keys)
    lines = ["---"]
    for key in keys:
        rendered = yaml_value(data.get(key))
        if len(rendered) == 1 and not rendered[0].startswith("\n"):
            lines.append(f"{key}: {rendered[0]}")
        else:
            value = rendered[0]
            if value.startswith("\n"):
                lines.append(f"{key}:{value}")
            elif value == "":
                lines.append(f"{key}:")
                lines.extend(rendered[1:])
            else:
                lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def replace_frontmatter(text: str, data: dict[str, Any]) -> str:
    if not text.startswith("---\n"):
        raise ValueError("target file has no frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("target file has unterminated frontmatter")
    body_start = text.find("\n", end + 4)
    body = text[body_start + 1:] if body_start != -1 else ""
    return render_frontmatter(data) + "\n" + body.lstrip("\n")


def append_to_section(body: str, title: str, additions: list[str]) -> str:
    if not additions:
        return body
    marker = f"## {title}"
    block = "\n".join(f"- {item}" for item in additions)
    if marker not in body:
        return body.rstrip() + f"\n\n{marker}\n\n{block}\n"
    start = body.index(marker)
    next_start = body.find("\n## ", start + len(marker))
    if next_start == -1:
        return body.rstrip() + "\n" + block + "\n"
    return body[:next_start].rstrip() + "\n" + block + "\n" + body[next_start:]


def update_body(text: str, notes: list[str]) -> str:
    end = text.find("\n---", 4)
    body_start = text.find("\n", end + 4)
    frontmatter_text = text[:body_start + 1]
    body = text[body_start + 1:]
    return frontmatter_text + append_to_section(body, "Notes", notes)


def find_place(db: Path, place_id: str | None, name: str | None, city: str | None) -> Path:
    places = sorted((db / "places").glob("*.md"))
    matches: list[Path] = []
    target_city = normalize_city_name(city)
    for path in places:
        data, _, errors = parse_frontmatter_file(path)
        if errors:
            continue
        if place_id and data.get("id") == place_id:
            return path
        if name and str(data.get("name") or "") == name:
            if not target_city or normalize_city_name(data.get("city")) == target_city:
                matches.append(path)
    if not matches:
        raise ValueError("No matching place found.")
    if len(matches) > 1:
        raise ValueError("Multiple matching places found; use --id.")
    return matches[0]


def run_validate(db: Path) -> int:
    return subprocess.run([sys.executable, str(SCRIPT_DIR / "validate_db.py"), str(db)]).returncode


def update_place(args: argparse.Namespace) -> Path:
    db = resolve_db(args.db)
    target = find_place(db, args.id, args.name, args.city)
    text = target.read_text(encoding="utf-8")
    data, _, errors = parse_frontmatter_file(target)
    if errors:
        raise ValueError("; ".join(errors))

    if args.tag:
        data["tags"] = dedupe_text_list([*clean_list(data.get("tags")), *args.tag])
    if args.source:
        data["source"] = dedupe_text_list([*clean_list(data.get("source")), *args.source])
    if args.evidence:
        data["evidence"] = [*clean_list(data.get("evidence")), *args.evidence]
    for field in ("address", "province", "phone", "website"):
        value = getattr(args, field)
        if value is not None:
            data[field] = value
    data["updated_at"] = today_iso()
    if args.last_verified:
        data["last_verified"] = args.last_verified

    updated = replace_frontmatter(text, data)
    updated = update_body(updated, args.note)
    if args.dry_run:
        print(updated)
        return target

    target.write_text(updated, encoding="utf-8")
    print(f"Updated {target}")
    rc = run_validate(db)
    if rc != 0:
        raise SystemExit(rc)
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=None)
    parser.add_argument("--id", default=None)
    parser.add_argument("--name", default=None)
    parser.add_argument("--city", default=None)
    parser.add_argument("--tag", action="append", default=[])
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--address", default=None)
    parser.add_argument("--province", default=None)
    parser.add_argument("--phone", default=None)
    parser.add_argument("--website", default=None)
    parser.add_argument("--last-verified", default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.id and not args.name:
        print("Use --id, or --name with optional --city.")
        return 1
    try:
        update_place(args)
    except ValueError as exc:
        print(f"Cannot update place: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
