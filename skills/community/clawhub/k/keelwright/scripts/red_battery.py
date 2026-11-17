#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""Run RED-BATTERY: swap implementation under test and verify tests fail on buggy version.

RED-BATTERY is the machine proof for gate 8c (spec-not-code / non-tautological tests):
the SAME spec-derived test suite must be GREEN on a correct implementation and RED on a
deliberately buggy one. If both arms are green, the tests do not discriminate and are
tautological by construction.

Usage:
    python scripts/red_battery.py <tests.py> <correct_impl.py> <buggy_impl.py>

All three files must live in the SAME directory; the test module imports `implementation`.
Paths may be relative to the current working directory.

Exit codes:
    0 = PASS         (green on correct, red on buggy — tests discriminate)
    1 = FAIL         (green on both — tautological)
    2 = INCONCLUSIVE (tests do not pass even on the correct implementation, or usage error)
"""
import os
import shutil
import subprocess
import sys
import pathlib


def run_pytest(test_file: str, impl_file: str) -> tuple[bool, str]:
    """Run pytest with impl_file temporarily swapped in as implementation.py.

    The test module imports `implementation`, so this renames impl_file to
    `implementation.py` inside the test directory, runs pytest there, then restores the
    original name in a finally block (so an interrupted run cannot corrupt the tree).

    Returns (all_green, combined_output). all_green is derived from pytest's real exit
    code, not from scanning output text.
    """
    test_path = pathlib.Path(test_file).resolve()
    work_dir = test_path.parent
    impl_path = work_dir / impl_file
    swap_path = work_dir / "implementation.py"
    stash_path = work_dir / "_red_battery_stash.py"

    if not impl_path.is_file():
        return False, f"[red_battery] implementation not found: {impl_path}"
    if not test_path.is_file():
        return False, f"[red_battery] test file not found: {test_path}"

    # A pre-existing implementation.py is stashed, never destroyed.
    had_existing = swap_path.exists()
    if had_existing:
        swap_path.rename(stash_path)
    impl_path.rename(swap_path)
    try:
        # Stale bytecode would mask the swap, so drop __pycache__ first.
        pycache = work_dir / "__pycache__"
        if pycache.is_dir():
            shutil.rmtree(pycache, ignore_errors=True)

        # PYTHONPATH must be ADDED to the inherited environment. Replacing os.environ
        # outright (env={"PYTHONPATH": ...}) strips SYSTEMROOT/PATH/TEMP and pytest dies
        # inside pytest_cmdline_parse on Windows before collecting anything.
        env = {**os.environ, "PYTHONPATH": str(work_dir)}

        r = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-q", "--tb=no"],
            cwd=str(work_dir),
            capture_output=True,
            env=env,
        )
        # Decode defensively: pytest output can carry non-UTF8 bytes (localized Windows
        # paths), and text=True would raise UnicodeDecodeError in the reader thread.
        out = (r.stdout or b"").decode("utf-8", errors="replace") + \
              (r.stderr or b"").decode("utf-8", errors="replace")

        # pytest exit codes: 0=all passed, 1=tests failed, 2=interrupted, 3=internal
        # error, 4=usage error, 5=no tests collected. Only 0 is green. A substring scan
        # for "FAILED" would treat a collection error (exit 3/4/5) as green.
        all_green = (r.returncode == 0)
        return all_green, out
    finally:
        if swap_path.exists():
            swap_path.rename(impl_path)
        if had_existing and stash_path.exists():
            stash_path.rename(swap_path)


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: red_battery.py <tests.py> <correct_impl.py> <buggy_impl.py>")
        return 2

    test_file, correct_impl, buggy_impl = sys.argv[1:4]

    # Phase 1: the correct implementation must PASS.
    green1, out1 = run_pytest(test_file, correct_impl)
    print(f"Phase 1 ({correct_impl}): {'PASS' if green1 else 'FAIL'}")
    print(out1[:800])

    # Phase 2: the buggy implementation must FAIL — this is the discriminating check.
    green2, out2 = run_pytest(test_file, buggy_impl)
    print(f"Phase 2 ({buggy_impl}): {'RED on buggy' if not green2 else 'GREEN on buggy — trap weak'}")
    print(out2[:1200])

    if green1 and not green2:
        print("\nRED-BATTERY RESULT: PASS — tests derived from spec, not tautological")
        return 0
    if green1 and green2:
        print("\nRED-BATTERY RESULT: FAIL — tests green on both, likely tautological")
        return 1
    print("\nRED-BATTERY RESULT: INCONCLUSIVE — tests fail on correct impl")
    return 2


if __name__ == "__main__":
    sys.exit(main())
