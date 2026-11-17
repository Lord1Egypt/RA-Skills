#!/usr/bin/env python3
"""Smoke tests for ocas-forge."""
import py_compile
import os
import glob
import unittest

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'scripts')


class TestScriptsCompile(unittest.TestCase):
    """All .py scripts must compile."""

    def test_all_py_compile(self):
        failures = []
        for py in sorted(glob.glob(os.path.join(SCRIPTS_DIR, '*.py'))):
            name = os.path.basename(py)
            try:
                py_compile.compile(py, doraise=True)
            except py_compile.PyCompileError as e:
                failures.append(f'{name}: {e}')
        self.assertEqual([], failures)

    def test_scripts_dir_exists(self):
        self.assertTrue(os.path.isdir(SCRIPTS_DIR))


if __name__ == '__main__':
    unittest.main()