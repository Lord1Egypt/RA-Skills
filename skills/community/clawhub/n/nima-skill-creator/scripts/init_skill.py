#!/usr/bin/env python3
"""Initialize a skill folder with a clean starter structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from generate_openai_yaml import write_openai_yaml

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = """---
name: {skill_name}
description: Explain what this skill does and when to use it. Include concrete trigger scenarios.
---

# {skill_title}

Start with the shortest set of instructions that lets another agent succeed.

## Quick Flow

1. Confirm the task shape.
2. Load only the references needed for this request.
3. Run any bundled scripts or apply the relevant assets.
4. Validate the result before finishing.

## Main Procedure

Replace this section with the real workflow for the skill.

## Resources

- `references/...` for detailed guidance that should load on demand
- `scripts/...` for deterministic automation
- `assets/...` for templates or starter files
"""

EXAMPLE_SCRIPT = """#!/usr/bin/env python3
\"\"\"Example helper for {skill_name}. Replace or delete.\"\"\"

def main() -> None:
    print("Example helper for {skill_name}")


if __name__ == "__main__":
    main()
"""

EXAMPLE_REFERENCE = """# Reference Notes

Replace this file with domain guidance that should only load on demand.
"""

EXAMPLE_ASSET = """Replace this placeholder with a real template, starter file, or asset."""


def normalize_skill_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def title_case_skill_name(skill_name: str) -> str:
    return " ".join(part.capitalize() for part in skill_name.split("-") if part)


def parse_resources(raw_resources: str) -> list[str]:
    if not raw_resources:
        return []
    resources = []
    seen = set()
    for item in raw_resources.split(","):
        item = item.strip()
        if not item or item in seen:
            continue
        if item not in ALLOWED_RESOURCES:
            allowed = ", ".join(sorted(ALLOWED_RESOURCES))
            raise ValueError(f"Unknown resource '{item}'. Allowed values: {allowed}")
        resources.append(item)
        seen.add(item)
    return resources


def write_examples(skill_dir: Path, skill_name: str, resources: list[str]) -> None:
    if "scripts" in resources:
        path = skill_dir / "scripts" / "example.py"
        path.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8")
        path.chmod(0o755)
    if "references" in resources:
        path = skill_dir / "references" / "reference.md"
        path.write_text(EXAMPLE_REFERENCE, encoding="utf-8")
    if "assets" in resources:
        path = skill_dir / "assets" / "placeholder.txt"
        path.write_text(EXAMPLE_ASSET, encoding="utf-8")


def init_skill(
    skill_name: str,
    output_dir: Path,
    resources: list[str],
    include_examples: bool,
    interface_overrides: list[str],
) -> Path:
    normalized = normalize_skill_name(skill_name)
    if not normalized:
        raise ValueError("Skill name becomes empty after normalization.")
    if normalized != skill_name:
        print(f"[INFO] Normalized skill name to '{normalized}'")
    if len(normalized) > MAX_SKILL_NAME_LENGTH:
        raise ValueError(
            f"Skill name is too long ({len(normalized)}). Maximum is {MAX_SKILL_NAME_LENGTH}."
        )

    skill_dir = output_dir.expanduser().resolve() / normalized
    if skill_dir.exists():
        raise FileExistsError(f"Skill directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(
            skill_name=normalized,
            skill_title=title_case_skill_name(normalized),
        ),
        encoding="utf-8",
    )

    for resource in resources:
        (skill_dir / resource).mkdir()

    if include_examples:
        write_examples(skill_dir, normalized, resources)

    write_openai_yaml(skill_dir, normalized, interface_overrides)
    return skill_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a new skill folder.")
    parser.add_argument("skill_name", help="Skill name, ideally lowercase hyphen-case")
    parser.add_argument("--path", required=True, help="Parent directory for the skill folder")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated resource directories to create: scripts,references,assets",
    )
    parser.add_argument(
        "--examples",
        action="store_true",
        help="Create example files inside the selected resource directories",
    )
    parser.add_argument(
        "--interface",
        action="append",
        default=[],
        help="Optional interface override in key=value format",
    )
    args = parser.parse_args()

    try:
        resources = parse_resources(args.resources)
        skill_dir = init_skill(
            args.skill_name,
            Path(args.path),
            resources,
            args.examples,
            args.interface,
        )
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1

    print(f"[OK] Created skill at {skill_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
