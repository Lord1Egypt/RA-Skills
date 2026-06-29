"""Tests for scripts/verify_math.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

import verify_math  # noqa: E402


class VerifyMathTests(unittest.TestCase):
    def test_missing_sympy_returns_unverified_status(self):
        with patch.object(verify_math, "HAS_SYMPY", False):
            with patch.object(sys, "argv", ["verify_math.py", "x", "x"]):
                self.assertEqual(verify_math.main(), 2)


if __name__ == "__main__":
    unittest.main()
