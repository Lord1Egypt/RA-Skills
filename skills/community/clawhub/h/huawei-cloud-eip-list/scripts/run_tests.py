#!/usr/bin/env python3
"""Run the offline unit test suite for the EIP list skill.

Executable entry point used by templates/test-vars.json so the test pipeline
gets a real script path (`python3 scripts/run_tests.py`) instead of relying on
`python3 -m unittest ...` being interpreted from the skill root. The tests are
fully offline (hcloud calls are mocked) and need no AK/SK.
"""

import os
import sys
import unittest

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(SKILL_ROOT, "tests")


def main():
    if SKILL_ROOT not in sys.path:
        sys.path.insert(0, SKILL_ROOT)
    suite = unittest.TestLoader().discover(TESTS_DIR, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())