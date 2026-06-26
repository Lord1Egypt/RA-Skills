#!/usr/bin/env python3
"""Validate a skill folder for common structural issues."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64


def extract_frontmatter(content: str) -> str:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter.")
    return match.group(1)


def parse_simple_yaml(frontmatter: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md not found."]

    content = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter = parse_simple_yaml(extract_frontmatter(content))
    except Exception as exc:
        return [str(exc)]

    allowed_keys = {"name", "description"}
    extra_keys = sorted(set(frontmatter) - allowed_keys)
    if extra_keys:
        errors.append(f"Unexpected frontmatter keys: {', '.join(extra_keys)}")

    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()

    if not name:
        errors.append("Frontmatter 'name' is required.")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("Frontmatter 'name' must be lowercase hyphen-case.")
    elif len(name) > MAX_SKILL_NAME_LENGTH:
        errors.append(f"Frontmatter 'name' exceeds {MAX_SKILL_NAME_LENGTH} characters.")

    if not description:
        errors.append("Frontmatter 'description' is required.")
    elif len(description) > 1024:
        errors.append("Frontmatter 'description' exceeds 1024 characters.")

    if "README.md" in {p.name for p in skill_dir.iterdir() if p.is_file()}:
        errors.append("Auxiliary README.md found in skill root. Remove non-essential docs.")
    if "PROJECT.md" in {p.name for p in skill_dir.iterdir() if p.is_file()}:
        errors.append("Auxiliary PROJECT.md found in skill root. Remove non-essential docs.")

    script_dir = skill_dir / "scripts"
    if script_dir.is_dir():
        for path in script_dir.glob("*.py"):
            first = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:3]
            joined = "\n".join(first)
            if "Usage" in joined and "#!" not in joined:
                errors.append(f"{path.name} looks like prose, not an executable script.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a skill folder.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] Not a directory: {skill_dir}")
        return 1

    errors = validate_skill(skill_dir)
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    print("[OK] Skill is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
