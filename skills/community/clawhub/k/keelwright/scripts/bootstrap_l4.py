#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""
bootstrap_l4.py — keelwright Layer-4 auto-wake.

WHY: keelwright's Phoenix + Autoresearch (cross-session learning, L4) need three
files in the PROJECT ROOT:
  - PROGRESS.md
  - autoresearch-lessons.md
  - phoenix-log.md
Without them L4 is inert. Vibe-coders do not read skill files, so we cannot rely on
the agent "remembering" to create them. This script makes it mandatory: the agent
runs it on first skill load, and the files appear.

WHAT IT DOES:
  - Takes one arg: the project root (directory of the repo / open project).
  - For each of the 3 files, if missing, copies the matching template from the
    skill's references/bootstrap/ dir into the project root.
  - If a file already exists, leaves it alone (never overwrites human/agent work).
  - Prints a short plain-language report of what it did.

USAGE: this is invoked by the agent at skill-load time, not by a human.
"""

import os
import sys
import shutil

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOTSTRAP_DIR = os.path.join(SKILL_ROOT, "references", "bootstrap")

FILES = {
    "PROGRESS.md": "PROGRESS.md.template",
    "autoresearch-lessons.md": "autoresearch-lessons.md.template",
    "phoenix-log.md": "phoenix-log.md.template",
}


def _normalize_path(p: str) -> str:
    """Convert an MSYS/Cygwin-style path (/c/Users/...) to a Windows path
    (C:\\Users\\...) when running under Windows Python, which does not
    understand the former. On non-Windows or already-native paths, return
    the input unchanged."""
    import re
    if os.name == "nt" and re.match(r"^/[a-zA-Z]/(?:\S+)?$", p):
        # /c/foo/bar -> C:/foo/bar
        drive = p[1].upper() + ":"
        rest = p[3:]
        return drive + "/" + rest
    return p


def main() -> int:
    # The project root must be passed EXPLICITLY. Silently falling back to os.getcwd()
    # meant that when the agent invoked this at skill-load time from an arbitrary
    # directory, three files were created in whatever tree the process happened to sit
    # in — a different repo, a home directory, or a system path. Writing outside the
    # intended project is worse than doing nothing, so refuse instead of guessing.
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("[keelwright bootstrap] ERROR: project root argument is required.")
        print("  Usage: python bootstrap_l4.py <project-root>")
        print("  Refusing to guess from the current directory — that risks creating")
        print("  files in an unrelated tree.")
        return 2

    project_root = os.path.abspath(_normalize_path(sys.argv[1]))

    if not os.path.isdir(project_root):
        print(f"[keelwright bootstrap] ERROR: project root not found: {project_root}")
        return 1

    print(f"[keelwright bootstrap] L4 loop-log check in: {project_root}")

    created = []
    skipped = []
    for target, template in FILES.items():
        dest = os.path.join(project_root, target)
        if os.path.exists(dest):
            skipped.append(target)
            continue
        src = os.path.join(BOOTSTRAP_DIR, template)
        if not os.path.exists(src):
            print(f"[keelwright bootstrap] WARNING: template missing: {src}")
            continue
        shutil.copy2(src, dest)
        created.append(target)

    if created:
        print(f"[keelwright bootstrap] CREATED ({len(created)}): {', '.join(created)}")
    if skipped:
        print(f"[keelwright bootstrap] already present ({len(skipped)}): {', '.join(skipped)}")
    if not created and not skipped:
        print("[keelwright bootstrap] nothing done (templates missing?)")

    print("[keelwright bootstrap] L4 is now awake — Phoenix/Autoresearch will learn across sessions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
