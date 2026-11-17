#!/usr/bin/env python3
"""bump-version.py — parity-locked version bumper for plan-it.

Bumps the version field across the parity-locked file set in one atomic operation.
Designed after planning-with-files v2.37.0 bumper (Issue #151).

Usage:
  python scripts/bump-version.py 0.1.1
  python scripts/bump-version.py 0.1.1 --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Parity-locked file set (15 files).
# Language variants (ar/de/es/zh/zht) removed in v0.1.0 because the bodies
# were not actually translated. They return in v0.2.0 with real translations.
PARITY_FILES = [
    # 12 SKILL.md files (1 canonical + 11 IDE adapters)
    "skills/plan-it/SKILL.md",
    ".codex/skills/plan-it/SKILL.md",
    ".cursor/skills/plan-it/SKILL.md",
    ".codebuddy/skills/plan-it/SKILL.md",
    ".factory/skills/plan-it/SKILL.md",
    ".mastracode/skills/plan-it/SKILL.md",
    ".opencode/skills/plan-it/SKILL.md",
    ".hermes/skills/plan-it/SKILL.md",
    ".continue/skills/plan-it/SKILL.md",
    ".gemini/skills/plan-it/SKILL.md",
    ".kiro/skills/plan-it/SKILL.md",
    ".pi/skills/plan-it/SKILL.md",
    # 3 manifests
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "CITATION.cff",
]

# Intentionally lagging set (reserved for future IDE adapters with separate version schemes).
LAGGING_FILES: list[str] = []

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.]+)?$")
SKILL_VERSION_RE = re.compile(r'^(\s*version:\s*)"[^"]*"\s*$', re.MULTILINE)
JSON_VERSION_RE = re.compile(r'("version"\s*:\s*)"[^"]*"')
CFF_VERSION_RE = re.compile(r'^(version:\s*)"[^"]*"\s*$', re.MULTILINE)


def bump_skill_md(path: Path, new_version: str, dry_run: bool) -> str | None:
    text = path.read_text(encoding="utf-8")
    new_text, n = SKILL_VERSION_RE.subn(rf'\1"{new_version}"', text, count=1)
    if n == 0:
        return None
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return new_version


def bump_json(path: Path, new_version: str, dry_run: bool) -> str | None:
    text = path.read_text(encoding="utf-8")
    new_text, n = JSON_VERSION_RE.subn(rf'\1"{new_version}"', text, count=1)
    if n == 0:
        return None
    # round-trip parse to confirm validity
    try:
        json.loads(new_text)
    except json.JSONDecodeError:
        return None
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return new_version


def bump_cff(path: Path, new_version: str, dry_run: bool) -> str | None:
    text = path.read_text(encoding="utf-8")
    new_text, n = CFF_VERSION_RE.subn(rf'\1"{new_version}"', text, count=1)
    if n == 0:
        return None
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return new_version


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="New semver version, e.g. 0.1.1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if not SEMVER_RE.match(args.version):
        print(f"[bump-version] not a valid semver: {args.version}", file=sys.stderr)
        return 2

    print(f"[bump-version] target: {args.version}")
    if args.dry_run:
        print("[bump-version] dry run, no writes")

    bumped = []
    skipped = []
    for rel in PARITY_FILES:
        path = ROOT / rel
        if not path.exists():
            skipped.append((rel, "missing"))
            continue
        if rel.endswith(".json"):
            ok = bump_json(path, args.version, args.dry_run)
        elif rel.endswith(".cff"):
            ok = bump_cff(path, args.version, args.dry_run)
        else:
            ok = bump_skill_md(path, args.version, args.dry_run)
        if ok:
            bumped.append(rel)
        else:
            skipped.append((rel, "no version field matched"))

    print()
    print(f"[bump-version] bumped {len(bumped)} files:")
    for f in bumped:
        print(f"  {f}")
    if skipped:
        print()
        print(f"[bump-version] skipped {len(skipped)} files:")
        for f, reason in skipped:
            print(f"  {f} ({reason})")
    print()
    print("[bump-version] intentionally lagging (not bumped):")
    for f in LAGGING_FILES:
        present = (ROOT / f).exists()
        marker = "exists" if present else "absent"
        print(f"  {f} ({marker})")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
