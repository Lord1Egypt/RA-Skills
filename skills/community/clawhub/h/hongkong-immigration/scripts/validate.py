#!/usr/bin/env python3
"""Validate the standalone Hong Kong immigration skill without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = ROOT / "SKILL.md"
EVALS_FILE = ROOT / "evals" / "evals.json"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
LOCAL_PATH_RE = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\\\Users\\\\)")
SECRET_RE = re.compile(r"\b(?:clh_|gh[opsu]_|sk-[A-Za-z0-9_-]{16})[A-Za-z0-9_-]+")


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("SKILL.md is missing opening front matter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("SKILL.md is missing closing front matter delimiter") from error

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            raise ValueError(f"invalid front matter line: {line}")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def main() -> int:
    errors = 0
    if not SKILL_FILE.is_file():
        fail("SKILL.md is missing")
        return 1

    text = SKILL_FILE.read_text(encoding="utf-8")
    try:
        fields = parse_front_matter(text)
    except ValueError as error:
        fail(str(error))
        return 1

    if fields.get("name") != "hongkong-immigration":
        fail("front matter name must be hongkong-immigration")
        errors += 1

    description = fields.get("description", "")
    if not description or len(description) > 1024 or "\n" in description:
        fail("description must be one non-empty line no longer than 1024 characters")
        errors += 1

    if len(text.splitlines()) > 500:
        fail("SKILL.md exceeds 500 lines")
        errors += 1

    for markdown_file in sorted(ROOT.rglob("*.md")):
        content = markdown_file.read_text(encoding="utf-8")
        relative = markdown_file.relative_to(ROOT)
        if re.search(r"\bTODO\b", content):
            fail(f"{relative} contains TODO")
            errors += 1
        if LOCAL_PATH_RE.search(content):
            fail(f"{relative} contains an absolute local path")
            errors += 1
        if SECRET_RE.search(content):
            fail(f"{relative} appears to contain a secret")
            errors += 1
        for target in LINK_RE.findall(content):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if path and not (markdown_file.parent / path).exists():
                fail(f"{relative} has broken relative link: {target}")
                errors += 1

    try:
        evals = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"invalid evals/evals.json: {error}")
        errors += 1
    else:
        if evals.get("skill_name") != fields.get("name"):
            fail("eval skill_name does not match front matter name")
            errors += 1
        items = evals.get("evals")
        if not isinstance(items, list) or not items:
            fail("evals must contain a non-empty evals list")
            errors += 1
        else:
            ids = [item.get("id") for item in items if isinstance(item, dict)]
            if len(ids) != len(set(ids)):
                fail("eval IDs must be unique")
                errors += 1
            for item in items:
                if not isinstance(item, dict) or not item.get("prompt") or not item.get("expected_output"):
                    fail("every eval needs prompt and expected_output")
                    errors += 1

    if errors:
        return 1
    print("Validated hongkong-immigration skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
