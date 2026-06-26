#!/usr/bin/env python3
"""Validate the music-education-research-writer skill package."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

SKILL_NAME = "music-education-research-writer"
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
REQUIRED_FRONTMATTER_KEYS = ("name", "description")
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "references/workflow.md",
    "references/evidence_hierarchy.md",
    "references/social_science_methods.md",
    "references/music_education_ontology.md",
    "references/literature_review_principles.md",
    "references/theory_modeling_guide.md",
    "references/research_gap_taxonomy.md",
    "references/ima_integration.md",
    "templates/literature_review_template.md",
    "templates/theory_model_template.md",
    "templates/research_gap_matrix_template.md",
    "templates/opening_report_argument_template.md",
    "templates/journal_article_outline_template.md",
    "templates/classroom_practice_research_design_template.md",
    "templates/evidence_chain_table_template.md",
    "templates/literature_concept_theory_method_gap_map.md",
    "examples/example_ai_music_education_review.md",
    "examples/example_large_corpus_triage.md",
    "examples/example_theory_model.md",
    "examples/example_research_gap_matrix.md",
    "tests/sample_user_request.md",
    "tests/sample_large_corpus_request.md",
    "tests/sample_corpus_notes.md",
    "tests/expected_output_checklist.md",
    "tests/pre_publish_checklist.md",
    "scripts/validate_skill.py",
    "scripts/package_skill.py",
]

DANGEROUS_PATTERNS: Sequence[Tuple[str, str, Sequence[str]]] = [
    ("remote download command", r"\bcurl\s+(-[A-Za-z]+\s+)*https?://", (".md", ".py", ".sh", ".bash")),
    ("remote download command", r"\bwget\s+(-[A-Za-z]+\s+)*https?://", (".md", ".py", ".sh", ".bash")),
    ("python network fetch", r"requests\.(get|post|put|delete)\s*\(", (".py",)),
    ("python urllib download", r"urllib\.request\.(urlopen|urlretrieve)\s*\(", (".py",)),
    ("shell execution", r"\bos\.system\s*\(", (".py",)),
    ("shell execution", r"\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\(", (".py",)),
    ("credential env access", r"\bos\.(getenv|environ)\s*\(", (".py",)),
    ("credential env access", r"\bos\.environ\[[^\]]+\]", (".py",)),
    ("secret file access", r"\.(aws|ssh)/", (".md", ".py", ".sh", ".bash")),
    ("cookie or browser store access", r"(cookies\.sqlite|Login Data|Local Storage)", (".md", ".py", ".sh", ".bash")),
]


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter.")

    raw_frontmatter = match.group(1)
    body = match.group(2)
    frontmatter: Dict[str, str] = {}

    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t"):
            raise ValueError("Frontmatter cannot contain nested keys.")
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()

    return frontmatter, body


def validate_frontmatter(skill_md: Path, errors: List[str]) -> None:
    content = skill_md.read_text(encoding="utf-8")

    try:
        frontmatter, _body = parse_frontmatter(content)
    except ValueError as exc:
        errors.append(str(exc))
        return

    keys = tuple(frontmatter.keys())
    if keys != REQUIRED_FRONTMATTER_KEYS:
        errors.append(
            "SKILL.md frontmatter must contain only 'name' and 'description' in that order."
        )

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        errors.append("Frontmatter is missing 'name'.")
    elif name != SKILL_NAME:
        errors.append(f"Frontmatter name must be '{SKILL_NAME}'.")
    elif not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append("Frontmatter name must be kebab-case.")
    elif name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append("Frontmatter name cannot start or end with '-' or contain '--'.")
    elif len(name) > MAX_NAME_LENGTH:
        errors.append(f"Frontmatter name exceeds {MAX_NAME_LENGTH} characters.")

    if not description:
        errors.append("Frontmatter is missing 'description'.")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f"Frontmatter description exceeds {MAX_DESCRIPTION_LENGTH} characters.")
    elif "use this skill" not in description.lower():
        errors.append("Frontmatter description must clearly say when to use the skill.")


def validate_required_files(root: Path, errors: List[str]) -> None:
    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        if not path.exists():
            errors.append(f"Missing required file: {relative_path}")


def validate_required_sections(skill_md: Path, errors: List[str]) -> None:
    content = skill_md.read_text(encoding="utf-8")
    required_headings = [
        "## Skill purpose",
        "## When to use this skill",
        "## When not to use this skill",
        "## Core workflow",
        "## Token Efficiency Protocol",
        "## Evidence rules",
        "## Citation integrity rules",
        "## iMA / local corpus integration rules",
        "## Literature review procedure",
        "## Theory and model construction procedure",
        "## Research gap analysis procedure",
        "## Output templates",
        "## Safety and academic integrity constraints",
        "## Examples",
    ]

    for heading in required_headings:
        if heading not in content:
            errors.append(f"SKILL.md is missing required section: {heading}")


def validate_no_symlinks(root: Path, errors: List[str]) -> None:
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlink is not allowed: {path.relative_to(root)}")


def validate_dangerous_patterns(root: Path, errors: List[str]) -> None:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in {"dist", "__pycache__"} for part in path.parts):
            continue
        if path.relative_to(root).as_posix() == "scripts/validate_skill.py":
            continue
        suffix = path.suffix.lower()
        text = path.read_text(encoding="utf-8", errors="ignore")

        for label, pattern, suffixes in DANGEROUS_PATTERNS:
            if suffix not in suffixes:
                continue
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"Dangerous pattern detected in {path.relative_to(root)}: {label}")


def validate_no_placeholder_todos(root: Path, errors: List[str]) -> None:
    for path in root.rglob("*.md"):
        if any(part in {"dist", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "[TODO" in text or "TODO:" in text:
            errors.append(f"Placeholder TODO found in {path.relative_to(root)}")


def validate_skill_root(root: Path) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not root.exists():
        return False, [f"Path does not exist: {root}"]
    if not root.is_dir():
        return False, [f"Path is not a directory: {root}"]

    validate_required_files(root, errors)

    skill_md = root / "SKILL.md"
    if skill_md.exists():
        validate_frontmatter(skill_md, errors)
        validate_required_sections(skill_md, errors)

    validate_no_symlinks(root, errors)
    validate_dangerous_patterns(root, errors)
    validate_no_placeholder_todos(root, errors)

    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the music-education-research-writer package.")
    parser.add_argument("path", nargs="?", default=".", help="Path to the skill root. Defaults to current directory.")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    ok, errors = validate_skill_root(root)

    if ok:
        print("Skill package is valid.")
        return 0

    print("Skill package validation failed:")
    for item in errors:
        print(f"- {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
