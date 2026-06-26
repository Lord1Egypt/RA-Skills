#!/usr/bin/env python3
"""Generate agents/openai.yaml for a skill folder."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALLOWED_INTERFACE_KEYS = {
    "display_name",
    "short_description",
    "icon_small",
    "icon_large",
    "brand_color",
    "default_prompt",
}

MAX_SHORT_DESCRIPTION = 64
MIN_SHORT_DESCRIPTION = 25


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def read_skill_name(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter.")
    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if not name_match:
        raise ValueError("Frontmatter is missing 'name'.")
    return name_match.group(1).strip().strip("\"'")


def format_display_name(skill_name: str) -> str:
    return " ".join(part.capitalize() for part in skill_name.split("-") if part)


def generate_short_description(display_name: str) -> str:
    value = f"Help with {display_name} workflows"
    if len(value) > MAX_SHORT_DESCRIPTION:
        value = f"{display_name} workflow helper"
    if len(value) > MAX_SHORT_DESCRIPTION:
        value = value[:MAX_SHORT_DESCRIPTION].rstrip()
    if len(value) < MIN_SHORT_DESCRIPTION:
        value = f"{value} tasks"
    return value[:MAX_SHORT_DESCRIPTION].rstrip()


def parse_overrides(items: list[str]) -> tuple[dict[str, str], list[str]]:
    values: dict[str, str] = {}
    order: list[str] = []
    for item in items:
        if "=" not in item:
            raise ValueError(f"Invalid override '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key not in ALLOWED_INTERFACE_KEYS:
            allowed = ", ".join(sorted(ALLOWED_INTERFACE_KEYS))
            raise ValueError(f"Unknown interface key '{key}'. Allowed: {allowed}")
        values[key] = value
        if key not in ("display_name", "short_description") and key not in order:
            order.append(key)
    return values, order


def write_openai_yaml(skill_dir: Path, skill_name: str, raw_overrides: list[str]) -> Path:
    overrides, extra_order = parse_overrides(raw_overrides)
    display_name = overrides.get("display_name") or format_display_name(skill_name)
    short_description = overrides.get("short_description") or generate_short_description(display_name)
    if not (MIN_SHORT_DESCRIPTION <= len(short_description) <= MAX_SHORT_DESCRIPTION):
        raise ValueError(
            f"short_description must be {MIN_SHORT_DESCRIPTION}-{MAX_SHORT_DESCRIPTION} characters."
        )

    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    path = agents_dir / "openai.yaml"

    lines = [
        "interface:",
        f"  display_name: {yaml_quote(display_name)}",
        f"  short_description: {yaml_quote(short_description)}",
    ]
    for key in extra_order:
        lines.append(f"  {key}: {yaml_quote(overrides[key])}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Created {path}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate agents/openai.yaml for a skill.")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument("--name", help="Skill name override")
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Optional interface override in key=value format",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"[ERROR] Not a directory: {skill_dir}")
        return 1

    try:
        skill_name = args.name or read_skill_name(skill_dir)
        write_openai_yaml(skill_dir, skill_name, args.interface)
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
