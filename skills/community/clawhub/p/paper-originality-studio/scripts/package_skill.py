#!/usr/bin/env python3
"""Validate and package a skill directory into a .skill archive."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import sys
import zipfile

REQUIRED = [
    "SKILL.md",
    "README.md",
    "SELF_CHECK.md",
    "tests/smoke-test.md",
]

HIGH_RISK_PATTERNS = [
    r"curl\s+[^|\n]+\|\s*(bash|sh)",
    r"wget\s+[^|\n]+\|\s*(bash|sh)",
    r"base64\s+-d\s*\|\s*(bash|sh)",
]

PLACEHOLDER_PATTERNS = [
    r"\bTODO:",
    r"\bFIXME:",
    r"<your[_ -]?[a-z]",
    r"lorem ipsum",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_skill(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")

    if not (root / "scripts").exists():
        errors.append("Missing scripts/ directory")
    if not (root / "resources").exists():
        errors.append("Missing resources/ directory")
    if not (root / "examples").exists():
        errors.append("Missing examples/ directory")

    scripts = list((root / "scripts").glob("*")) if (root / "scripts").exists() else []
    resources = list((root / "resources").glob("*")) if (root / "resources").exists() else []
    if not scripts:
        errors.append("scripts/ must contain at least one file")
    if not resources:
        errors.append("resources/ must contain at least one file")

    skill_md = root / "SKILL.md"
    if skill_md.exists():
        text = read_text(skill_md)
        if not text.startswith("---\n"):
            errors.append("SKILL.md must start with YAML frontmatter")
        matches = re.findall(r"^name:\s*(.+)$", text, flags=re.M)
        if not matches:
            errors.append("SKILL.md missing required frontmatter field: name")
        else:
            name = matches[0].strip()
            if name != root.name:
                errors.append(f"Skill name '{name}' does not match folder name '{root.name}'")
        if not re.findall(r"^description:\s*(.+)$", text, flags=re.M):
            errors.append("SKILL.md missing required frontmatter field: description")

    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for pattern in HIGH_RISK_PATTERNS:
            if re.search(pattern, text, flags=re.I):
                errors.append(f"High-risk command pattern found in {path.relative_to(root)}: {pattern}")
        if path.name != "package_skill.py":
            for pattern in PLACEHOLDER_PATTERNS:
                if re.search(pattern, text, flags=re.I):
                    errors.append(f"Placeholder content found in {path.relative_to(root)}: {pattern}")

    return errors


def package_skill(root: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{root.name}.skill"
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue
            if path.name == ".DS_Store":
                continue
            arcname = f"{root.name}/{path.relative_to(root).as_posix()}"
            zf.write(path, arcname)
    return out_path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate and package a skill directory.")
    parser.add_argument("skill_dir", help="Path to skill directory.")
    parser.add_argument("out_dir", nargs="?", default="dist", help="Output directory (default: dist)")
    args = parser.parse_args(argv)

    root = Path(args.skill_dir).resolve()
    out_dir = Path(args.out_dir).resolve()

    if not root.exists() or not root.is_dir():
        print(f"[error] Skill directory not found: {root}", file=sys.stderr)
        return 1

    errors = validate_skill(root)
    if errors:
        print("[error] Validation failed:", file=sys.stderr)
        for item in errors:
            print(f" - {item}", file=sys.stderr)
        return 2

    out_path = package_skill(root, out_dir)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
