#!/usr/bin/env python3
"""Run MoSoCanvas deterministic unit, adversarial, and integration tests."""

from __future__ import annotations

from pathlib import Path
import unittest


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
