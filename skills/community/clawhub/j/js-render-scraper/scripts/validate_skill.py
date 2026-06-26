#!/usr/bin/env python3
"""
Quick validation script for js-render-scraper skill
Validates SKILL.md frontmatter and structure
"""

import os
import sys
import re
from pathlib import Path


def validate_frontmatter(skill_path: Path) -> tuple[bool, list[str]]:
    """Validate SKILL.md frontmatter"""
    errors = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, ["SKILL.md not found"]

    content = skill_md.read_text(encoding="utf-8")

    # Check frontmatter exists at start
    if not content.strip().startswith("---"):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return False, errors

    # Extract frontmatter
    parts = content.split("---")
    if len(parts) < 3:
        errors.append("Invalid frontmatter structure")
        return False, errors

    frontmatter = parts[1]

    # Check required fields
    if "name:" not in frontmatter:
        errors.append("Missing 'name:' in frontmatter")

    if "description:" not in frontmatter:
        errors.append("Missing 'description:' in frontmatter")

    # Validate name format
    name_match = re.search(r"name:\s*([a-z0-9-]+)", frontmatter)
    if name_match:
        name = name_match.group(1)
        if name != skill_path.name:
            errors.append(f"Name mismatch: frontmatter '{name}' != folder '{skill_path.name}'")

    # Check no markdown title before frontmatter
    before_frontmatter = content.split("---")[0].strip()
    if before_frontmatter.startswith("#"):
        errors.append("Markdown title (#) found before frontmatter")

    return len(errors) == 0, errors


def validate_meta(skill_path: Path) -> tuple[bool, list[str]]:
    """Validate _meta.json"""
    errors = []
    meta_file = skill_path / "_meta.json"

    if not meta_file.exists():
        return False, ["_meta.json not found"]

    try:
        import json
        meta = json.loads(meta_file.read_text(encoding="utf-8"))

        if "id" not in meta:
            errors.append("Missing 'id' in _meta.json")

        if "version" not in meta:
            errors.append("Missing 'version' in _meta.json")

        # Validate id is a number
        if "id" in meta:
            try:
                int(meta["id"])
            except ValueError:
                errors.append("'id' must be a valid integer")

    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in _meta.json: {e}")
    except Exception as e:
        errors.append(f"Error reading _meta.json: {e}")

    return len(errors) == 0, errors


def validate_structure(skill_path: Path) -> tuple[bool, list[str]]:
    """Validate overall skill structure"""
    errors = []

    # Check skill directory name
    if not re.match(r'^[a-z0-9-]+$', skill_path.name):
        errors.append(f"Invalid folder name '{skill_path.name}'. Use lowercase, numbers, and hyphens only")

    # Check for unintended files
    forbidden = [".pyc", "__pycache__", ".env", ".git"]
    for item in skill_path.rglob("*"):
        if item.is_file():
            for f in forbidden:
                if f in str(item):
                    errors.append(f"Found forbidden file pattern: {item}")

    return len(errors) == 0, errors


def main():
    skill_path = Path(__file__).parent.parent

    print(f"Validating skill at: {skill_path}")
    print("-" * 50)

    all_errors = []

    # Run validations
    checks = [
        ("Frontmatter", validate_frontmatter),
        ("_meta.json", validate_meta),
        ("Structure", validate_structure),
    ]

    for name, validator in checks:
        valid, errors = validator(skill_path)
        if valid:
            print(f"✓ {name}: PASS")
        else:
            print(f"✗ {name}: FAIL")
            for err in errors:
                print(f"  - {err}")
                all_errors.append(err)

    print("-" * 50)

    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s) found")
        sys.exit(1)
    else:
        print("VALIDATION PASSED: All checks successful")
        sys.exit(0)


if __name__ == "__main__":
    main()
