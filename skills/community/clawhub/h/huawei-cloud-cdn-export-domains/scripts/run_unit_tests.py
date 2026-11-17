#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the skill's offline unit tests (mocked hcloud; no credentials, no network).

This is the executor-friendly entrypoint declared in templates/test-vars.json so
the standard test executor can run the offline suite as
``python3 scripts/run_unit_tests.py`` (a ``python3 scripts/...`` command the
executor resolves against the skill root). It is cwd-independent: the tests are
discovered relative to this file's skill root.

Exit code: 0 when every test passes, 1 otherwise.
"""

import os
import sys
import unittest

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(SKILL_ROOT, "tests")


def main():
    if not os.path.isdir(TESTS_DIR):
        sys.stderr.write("未找到离线单元测试目录: %s\n" % TESTS_DIR)
        return 1
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())