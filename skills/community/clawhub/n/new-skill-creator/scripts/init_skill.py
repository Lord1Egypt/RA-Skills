#!/usr/bin/env python3
"""Scaffold a new agent skill directory with SKILL.md template and resource folders."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKILL_MD_TEMPLATE = """\
---
name: {name}
description: TODO: <Action> <object/system> for <main outcome>. Use when you need to <job 1>, <job 2>, <job 3>.
metadata: {{ "openclaw": {{ "emoji": "{emoji}", "requires": {{ }} }} }}
---

# {title}

TODO: One-sentence summary of what this skill does.

## Prerequisites

- TODO: List environment variables, CLI tools, or dependencies.

## Example Prompts

- `TODO: Write a realistic user prompt that should trigger this skill.`
- `TODO: Write another prompt covering a different use case.`
- `TODO: Write a third prompt with casual user language.`

## Workflow

1. TODO: First step.
2. TODO: Second step.
3. TODO: Third step.

## Commands

```sh
# TODO: Add runnable commands using {{baseDir}} paths
# python3 {{baseDir}}/scripts/example.py <input>
```

## Definition of Done

- TODO: Add measurable completion criteria.
- TODO: What files, outputs, or states prove the skill succeeded?

## When Not to Use

- TODO: What should this skill NOT be used for?

## Resources

- TODO: Link to references/ files if applicable.
"""

REFERENCE_PLACEHOLDER = """\
# {title}

TODO: Add reference content for this skill.

This file is loaded into context on demand when the skill needs domain-specific information.
"""

SCRIPT_PLACEHOLDER = """\
#!/usr/bin/env python3
\"\"\"TODO: Describe what this script does.\"\"\"

from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="TODO: Script description.")
    parser.add_argument("input", help="TODO: Input argument description")
    args = parser.parse_args()

    # TODO: Implement script logic

    print(f"Processing: {{args.input}}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""


NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def validate_name(name: str) -> str | None:
    if not name:
        return "name cannot be empty"
    if len(name) > 64:
        return f"name too long ({len(name)} chars, max 64)"
    if "--" in name:
        return "name cannot contain consecutive hyphens"
    if not NAME_PATTERN.match(name):
        return "name must be lowercase letters, digits, and hyphens; no leading/trailing hyphens"
    return None


def name_to_title(name: str) -> str:
    return " ".join(word.capitalize() for word in name.split("-"))


def create_skill(name: str, output_dir: Path, skill_type: str) -> Path:
    skill_dir = output_dir / name
    if skill_dir.exists():
        raise FileExistsError(f"directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True)

    title = name_to_title(name)
    emoji = "🔧"

    skill_md = SKILL_MD_TEMPLATE.format(name=name, title=title, emoji=emoji)
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "domain.md").write_text(
        REFERENCE_PLACEHOLDER.format(title=f"{title} Reference"),
        encoding="utf-8",
    )

    if skill_type in ("script", "asset"):
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "example.py").write_text(SCRIPT_PLACEHOLDER, encoding="utf-8")

    if skill_type == "asset":
        assets_dir = skill_dir / "assets"
        assets_dir.mkdir()
        (assets_dir / ".gitkeep").write_text("", encoding="utf-8")

    return skill_dir


def print_tree(root: Path, prefix: str = "") -> None:
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry.name}")
        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_tree(entry, prefix + extension)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a new agent skill directory."
    )
    parser.add_argument("name", help="Skill name (lowercase-hyphen, e.g. my-skill)")
    parser.add_argument(
        "--path",
        default=".",
        help="Parent directory where the skill folder will be created (default: current dir)",
    )
    parser.add_argument(
        "--type",
        choices=["instruction", "script", "asset"],
        default="instruction",
        help="Skill type: instruction (default), script, or asset",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    name = args.name
    output_dir = Path(args.path).expanduser().resolve()
    skill_type = args.type

    error = validate_name(name)
    if error:
        print(f"error: invalid skill name '{name}': {error}", file=sys.stderr)
        return 1

    if not output_dir.is_dir():
        print(f"error: output directory does not exist: {output_dir}", file=sys.stderr)
        return 1

    try:
        skill_dir = create_skill(name, output_dir, skill_type)
    except FileExistsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Created skill: {skill_dir}")
    print()
    print_tree(skill_dir)
    print()
    print("Next steps:")
    print(f"  1. Edit {skill_dir / 'SKILL.md'} — fill in the TODO placeholders")
    print(f"  2. Replace {skill_dir / 'references' / 'domain.md'} with real reference docs")
    if skill_type in ("script", "asset"):
        print(f"  3. Implement {skill_dir / 'scripts' / 'example.py'} or replace with real scripts")
    print(f"  4. Run skill-test to verify quality")
    print(f"  5. Run skill-seo to optimize discoverability")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
