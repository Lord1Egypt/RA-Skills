#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dev.py —— one entry point for every local gate.

Why this exists
---------------
The checks a contributor must run are four separate commands with four sets of
flags that nobody remembers. This script is the single source of truth for
them; `Makefile` is a thin proxy so `make test` also works where make exists.
Windows contributors (no make) call this directly.

    python scripts/dev.py all          # everything CI runs, locally
    python scripts/dev.py test         # pytest
    python scripts/dev.py hygiene      # CRLF / mojibake / junk / line budget
    python scripts/dev.py refs         # release files reference release files
    python scripts/dev.py lint         # byte-compile + ruff (if installed)
    python scripts/dev.py scaffold --name "书名" --root ../my-novel

Exit code is the first failing gate's exit code, 0 when all pass.

This file writes LF endings only.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

# Files exempt from the 500-line budget. Mirrors .pre-commit-config.yaml and
# .github/workflows/ci.yml — change all three together.
LINE_BUDGET_ALLOW = "README FOR AI.md,CHANGELOG.md,LICENSE,LICENSES/CC-BY-NC-SA-4.0.txt"


def run(cmd: list, label: str) -> int:
    print(f"\n--- {label} ---")
    print("$ " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
    proc = subprocess.run(cmd, cwd=str(ROOT))
    if proc.returncode == 0:
        print(f"[ok] {label}")
    else:
        print(f"[FAIL] {label} (exit {proc.returncode})")
    return proc.returncode


def cmd_test(_args) -> int:
    return run([sys.executable, "-m", "pytest"], "pytest")


def cmd_hygiene(_args) -> int:
    return run(
        [sys.executable, str(SCRIPTS / "scan_hygiene.py"),
         "--root", ".", "--max-lines", "500",
         "--allow", LINE_BUDGET_ALLOW,
         "--fail-on", "crlf,junk,mojibake"],
        "file hygiene",
    )


def cmd_refs(_args) -> int:
    return run(
        [sys.executable, str(SCRIPTS / "check_refs.py"),
         "--root", ".", "--fail-on", "NONRELEASE"],
        "reference integrity",
    )


def cmd_lint(_args) -> int:
    code = run([sys.executable, "-m", "compileall", "-q", "scripts", "tests"], "byte-compile")
    if code:
        return code
    if shutil.which("ruff"):
        return run([sys.executable, "-m", "ruff", "check", "scripts", "tests"], "ruff")
    print("\n--- ruff ---\n[skip] ruff not installed (pip install -r requirements-dev.txt)")
    return 0


def cmd_scaffold(args) -> int:
    return run(
        [sys.executable, str(SCRIPTS / "init_subproject.py"),
         "--name", args.name, "--root", args.root],
        "subproject scaffold",
    )


def cmd_all(args) -> int:
    for fn in (cmd_hygiene, cmd_refs, cmd_lint, cmd_test):
        code = fn(args)
        if code:
            return code
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Local development gates.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("test", help="run the pytest suite")
    sub.add_parser("hygiene", help="CRLF / mojibake / junk / line budget")
    sub.add_parser("refs", help="release files must reference release files")
    sub.add_parser("lint", help="byte-compile and ruff")
    sub.add_parser("all", help="hygiene + refs + lint + test")

    sc = sub.add_parser("scaffold", help="create a new novel subproject")
    sc.add_argument("--name", required=True)
    sc.add_argument("--root", default=".")

    args = ap.parse_args(argv)

    handlers = {
        "test": cmd_test,
        "hygiene": cmd_hygiene,
        "refs": cmd_refs,
        "lint": cmd_lint,
        "scaffold": cmd_scaffold,
        "all": cmd_all,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
