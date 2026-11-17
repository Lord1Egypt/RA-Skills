#!/usr/bin/env python3
"""sync-ide-folders.py — mirror canonical scripts + templates into IDE adapter dirs.

Adapter dirs receive byte-identical scripts + templates from the canonical top-level.
SKILL.md is NOT synced (each IDE has its own frontmatter shape).

Usage:
  python scripts/sync-ide-folders.py            # sync all IDE dirs
  python scripts/sync-ide-folders.py --verify   # exit nonzero on drift, no writes
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANONICAL_SCRIPTS = "scripts"
CANONICAL_TEMPLATES = "templates"

# Adapter dirs that should receive scripts + templates mirrors.
ADAPTERS = [
    ".codex/skills/plan-it",
    ".cursor/skills/plan-it",
    ".codebuddy/skills/plan-it",
    ".factory/skills/plan-it",
    ".mastracode/skills/plan-it",
    ".opencode/skills/plan-it",
    ".hermes/skills/plan-it",
    ".continue/skills/plan-it",
    ".gemini/skills/plan-it",
    ".kiro/skills/plan-it",
    ".pi/skills/plan-it",
    # canonical English skill bundle also gets the same scripts + templates
    "skills/plan-it",
]

SCRIPTS_MANIFEST = [
    "plan-hook.py",
    "init-plan.sh",
    "init-plan.ps1",
    "render-plan.sh",
    "render-plan.ps1",
    "attest-plan.sh",
    "attest-plan.ps1",
    "bump-version.py",
    "sync-ide-folders.py",
    "session-catchup.py",
    "export-markdown.py",
]


def _copy_or_verify(src: Path, dst: Path, verify_only: bool) -> tuple[bool, str | None]:
    """Return (changed, reason). reason is None on success."""
    if not src.exists():
        return False, f"missing source {src}"
    if not dst.exists():
        if verify_only:
            return True, f"missing dest {dst}"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True, None
    if filecmp.cmp(src, dst, shallow=False):
        return False, None
    if verify_only:
        return True, f"drift: {dst}"
    shutil.copy2(src, dst)
    return True, None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="check only; nonzero on drift")
    args = parser.parse_args(argv)

    src_scripts = ROOT / CANONICAL_SCRIPTS
    src_templates = ROOT / CANONICAL_TEMPLATES

    drift = []
    changes = []
    for adapter_rel in ADAPTERS:
        adapter = ROOT / adapter_rel
        # sync scripts
        adapter_scripts = adapter / "scripts"
        for script_name in SCRIPTS_MANIFEST:
            src = src_scripts / script_name
            dst = adapter_scripts / script_name
            changed, reason = _copy_or_verify(src, dst, args.verify)
            if reason and "missing source" in reason:
                continue
            if reason:
                drift.append(reason)
            elif changed:
                changes.append(str(dst))
        # sync templates
        if src_templates.exists():
            adapter_templates = adapter / "templates"
            for tpl in sorted(src_templates.glob("*.html")):
                dst = adapter_templates / tpl.name
                changed, reason = _copy_or_verify(tpl, dst, args.verify)
                if reason:
                    drift.append(reason)
                elif changed:
                    changes.append(str(dst))

    if args.verify:
        if drift:
            print(f"[sync] DRIFT detected ({len(drift)} entries):")
            for d in drift:
                print(f"  {d}")
            return 1
        print("[sync] OK, no drift")
        return 0

    if changes:
        print(f"[sync] updated {len(changes)} files:")
        for c in changes:
            print(f"  {c}")
    else:
        print("[sync] OK, nothing to update")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
