#!/usr/bin/env python3
"""Checks for the fail-early runtime dependency report."""

import unittest
from unittest.mock import patch

import runtime_dependency_guard as guard


class RuntimeDependencyGuardSmoke(unittest.TestCase):
    def test_current_test_runtime_is_ready(self):
        result = guard.inspect_dependencies()
        self.assertEqual(result["status"], "runtime_dependencies_ready")
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["incompatible"], [])
        self.assertEqual(set(result["installed"]), set(guard.DEPENDENCIES))

    def test_missing_component_is_named_and_blocks(self):
        original = guard.importlib.util.find_spec
        with patch.object(guard.importlib.util, "find_spec",
                          side_effect=lambda name: None if name == "pymupdf" else original(name)):
            result = guard.inspect_dependencies()
        self.assertEqual(result["status"], "runtime_dependencies_missing")
        self.assertIn("PyMuPDF", result["missing"])

    def test_incompatible_version_is_named_and_blocks(self):
        original = guard.importlib.metadata.version
        with patch.object(guard.importlib.metadata, "version",
                          side_effect=lambda name: "3.7.9" if name == "matplotlib" else original(name)):
            result = guard.inspect_dependencies()
        self.assertEqual(result["status"], "runtime_dependencies_incompatible")
        self.assertEqual(result["incompatible"][0]["dependency"], "matplotlib")

    def test_numeric_version_bounds_are_not_lexical(self):
        self.assertTrue(guard.in_range("3.11.1", "3.8", "4"))
        self.assertFalse(guard.in_range("3.7.10", "3.8", "4"))


if __name__ == "__main__":
    unittest.main()
