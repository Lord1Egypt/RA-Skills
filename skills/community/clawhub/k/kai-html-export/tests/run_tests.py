#!/usr/bin/env python3
"""
kai-html-export test runner.

Usage:
    python tests/run_tests.py              # run all tests
    python tests/run_tests.py --pptx       # PPTX tests only
    python tests/run_tests.py --png        # screenshot tests only
    python tests/run_tests.py -v           # verbose (show each test name)

Requires: pip install pytest Pillow python-pptx
"""

import subprocess
import sys
import argparse
from pathlib import Path

TESTS_DIR = Path(__file__).parent

SUITES = {
    "pptx":       TESTS_DIR / "test_pptx.py",
    "screenshot": TESTS_DIR / "test_screenshot.py",
    "share":      TESTS_DIR / "test_share_deploy.py",
}


def check_deps():
    missing = []
    for pkg in ["pytest", "PIL", "pptx"]:
        try:
            __import__(pkg)
        except ImportError:
            name = {"PIL": "Pillow", "pptx": "python-pptx"}.get(pkg, pkg)
            missing.append(name)
    if missing:
        print(f"Missing test dependencies. Install with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)


def run(files: list[Path], verbose: bool) -> int:
    args = [sys.executable, "-m", "pytest", "--tb=short"]
    if verbose:
        args.append("-v")
    args += [str(f) for f in files]
    result = subprocess.run(args)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pptx",       action="store_true", help="Run PPTX tests only")
    parser.add_argument("--png",        action="store_true", help="Run screenshot tests only")
    parser.add_argument("--share",      action="store_true", help="Run share-helper tests only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    check_deps()

    if args.pptx:
        files = [SUITES["pptx"]]
    elif args.png:
        files = [SUITES["screenshot"]]
    elif args.share:
        files = [SUITES["share"]]
    else:
        files = list(SUITES.values())

    sys.exit(run(files, args.verbose))


if __name__ == "__main__":
    main()
