#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""
build_skill.py — ADR-001 layered skill assembler (F46, v1.10.0).

WHY:
- `SKILL.md` in the repo is a layered INDEX (~150-200 lines, ~2-3K tokens).
  This keeps agent context lightweight (Hermes/Cursor/Codex/Cline/OpenClaw).
- Public registries (skills.sh, ClawHub, askill.sh) display SKILL.md as a single page.
  If we published the index alone, discoverability and completeness would drop.
- `build_skill.py` re-assembles the index + all `references/*.md` into `SKILL.full.md`
  or overwrites `SKILL.md` in a release artifact for publication.

USAGE:
    python scripts/build_skill.py [--output SKILL.full.md] [--check]

FLAGS:
    --output PATH   Where to write the assembled skill (default: SKILL.full.md)
    --check         Exit 0 if assembled output matches existing output (CI check)
    --inplace       Overwrite SKILL.md directly (for publication workflows)
"""
import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "SKILL.md"
REFS_DIR = ROOT / "references"


def reassemble_skill(index_text: str, refs_dir: Path) -> str:
    """Read SKILL.md index; inline references where referenced, or append all references at the bottom."""
    out = [index_text]
    out.append("\n\n" + "=" * 80 + "\n")
    out.append("# APPENDIX: Full Reference Modules (Inlined for Registry Display)\n")
    out.append("> **Note for agents:** When loaded in a live coding session, read these modules\n")
    out.append("> on demand via `references/<name>.md`. They are inlined here for web display.\n\n")

    # Walk all .md in references/ sorted (recursive to include bindings/, bootstrap/, etc.)
    # Exclude directories that must never be auto-inlined.
    EXCLUDE_DIRS = {"historical", "internal"}
    ref_files = sorted(refs_dir.rglob("*.md"))
    ref_files = [
        rf for rf in ref_files
        if not any(part in EXCLUDE_DIRS for part in rf.relative_to(ROOT).parts)
    ]
    for rf in ref_files:
        rel_name = rf.relative_to(ROOT)
        out.append(f"\n--- {rel_name} ---\n\n")
        try:
            content = rf.read_text(encoding="utf-8")
            # Strip top header if it duplicates the file name
            out.append(content)
            out.append("\n")
        except Exception as e:
            out.append(f"<!-- Error reading {rel_name}: {e} -->\n")

    return "".join(out)


def main():
    p = argparse.ArgumentParser(description="Assemble layered skill for publication.")
    p.add_argument("--output", "-o", default="SKILL.full.md", help="Output file path")
    p.add_argument("--check", action="store_true", help="Check if output is up-to-date")
    p.add_argument("--inplace", action="store_true", help="Overwrite SKILL.md directly (for publication workflows)")
    args = p.parse_args()

    if not INDEX_PATH.exists():
        print(f"Error: {INDEX_PATH} not found", file=sys.stderr)
        return 1

    # Symlink guard: refuse to operate if SKILL.md is a symlink (MIN-3c)
    if INDEX_PATH.is_symlink():
        print(f"Error: {INDEX_PATH} is a symlink — refusing to operate. Resolve it first.", file=sys.stderr)
        return 1

    # Inplace warning (MIN-3c)
    if args.inplace:
        print("WARNING: --inplace will OVERWRITE the layered index (SKILL.md) with the full assembled doc.")
        print("This is for publication artifacts ONLY. Normal development keeps SKILL.md as the index.")
        print("Type 'YES' to confirm: ", end="", flush=True)
        confirm = sys.stdin.readline().strip()
        if confirm != "YES":
            print("Aborted.")
            return 1

    index_text = INDEX_PATH.read_text(encoding="utf-8")
    assembled = reassemble_skill(index_text, REFS_DIR)

    target_path = INDEX_PATH if args.inplace else Path(args.output)

    if args.check:
        if not target_path.exists():
            print(f"[check] {target_path} does not exist — needs build", file=sys.stderr)
            return 1
        existing = target_path.read_text(encoding="utf-8")
        if existing != assembled:
            print(f"[check] {target_path} is out of date — run `python scripts/build_skill.py`", file=sys.stderr)
            return 1
        print(f"[check] {target_path} is up to date OK")
        return 0

    target_path.write_text(assembled, encoding="utf-8")
    tokens = len(assembled) // 4
    lines = len(assembled.splitlines())
    print(f"[build_skill] wrote {target_path} ({lines} lines, ~{tokens} tokens, {len(assembled)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
