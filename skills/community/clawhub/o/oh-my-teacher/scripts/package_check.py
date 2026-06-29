#!/usr/bin/env python3
"""Run all Oh My Teacher skill validation checks in one command.

This is a convenience entry point that runs:
  1. validate_skill.py  — structural checks, command registration, stale references
  2. All unit tests under scripts/tests/

Usage:
    python scripts/package_check.py
    python scripts/package_check.py --root /path/to/skill
"""

from __future__ import annotations

import argparse
import os
import py_compile
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def clean_pycache(root: Path) -> None:
    for path in root.rglob("__pycache__"):
        if path.is_dir():
            import shutil
            shutil.rmtree(path)


def check_utf8_and_long_lines(root: Path) -> int:
    failures = 0
    suffixes = {".py", ".md", ".yml", ".yaml", ".json"}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in {".git", "__pycache__"} for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            failures += 1
            print(f"UTF-8 check FAILED: {path}: {exc}", file=sys.stderr)
            continue
        long_lines = [i for i, line in enumerate(text.splitlines(), 1) if len(line) > 500]
        if long_lines:
            failures += 1
            print(f"Long-line check FAILED: {path}: {long_lines[:5]}", file=sys.stderr)
    return failures


def check_py_compile(root: Path) -> int:
    failures = 0
    for path in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            failures += 1
            print(f"py_compile FAILED: {path}: {exc}", file=sys.stderr)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all Oh My Teacher skill checks.")
    parser.add_argument("--root", default=str(SCRIPT_DIR.parent), help="Skill root directory.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    failures = 0
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    clean_pycache(root)

    # Step 1: validate_skill.py
    validate_script = SCRIPT_DIR / "validate_skill.py"
    print("=== Running validate_skill.py ===")
    result = subprocess.run(
        [sys.executable, str(validate_script), "--root", str(root)],
        cwd=str(root),
        env=env,
    )
    if result.returncode != 0:
        failures += 1
        print("validate_skill.py FAILED.", file=sys.stderr)
    else:
        print("validate_skill.py PASSED.")

    # Step 2: unit tests
    print("\n=== Running unit tests ===")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(SCRIPT_DIR / "tests"), "-v"],
        cwd=str(SCRIPT_DIR),
        env=env,
    )
    if result.returncode != 0:
        failures += 1
        print("Unit tests FAILED.", file=sys.stderr)
    else:
        print("Unit tests PASSED.")

    # Step 3: Python compile
    print("\n=== Running py_compile ===")
    compile_failures = check_py_compile(root)
    failures += compile_failures
    print("py_compile PASSED." if compile_failures == 0 else "py_compile FAILED.", file=sys.stderr if compile_failures else sys.stdout)

    # Step 4: UTF-8 and long lines
    print("\n=== Running UTF-8 and long-line checks ===")
    text_failures = check_utf8_and_long_lines(root)
    failures += text_failures
    print("Text checks PASSED." if text_failures == 0 else "Text checks FAILED.", file=sys.stderr if text_failures else sys.stdout)

    # Summary
    print(f"\n=== Summary: {4 - min(failures, 4)}/4 check groups passed ===")
    if failures:
        print("Some checks failed. See output above for details.", file=sys.stderr)
        return 1
    clean_pycache(root)
    print("All checks passed. Skill package is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
