"""Tests for scripts/snapshot.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from snapshot import slugify  # noqa: E402


SNAPSHOT = """## Current Course Snapshot
- **Course**: Data Structures / Computer Science
- **Assessment**: coding exam
- **Days left**: 7
- **Level**: shaky
- **Environment**: agent-shell
- **Materials**: notes
- **LaTeX**: not applicable
- **Weak points**: [graphs]
- **Completed**: []
- **Accuracy**: "graphs 4/10"
- **Last action**: /quiz
- **Next recommended**: /fix on graphs
"""


class SnapshotTests(unittest.TestCase):
    def _script(self) -> str:
        return str(SCRIPT_DIR / "snapshot.py")

    def test_slugify(self):
        self.assertEqual(slugify("Data Structures!"), "data-structures")
        self.assertEqual(slugify("  Linear   Algebra  "), "linear-algebra")
        self.assertEqual(slugify("数据结构与算法"), "数据结构与算法")
        self.assertEqual(slugify("操作系统（OS）"), "操作系统os")

    def test_save_load_and_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            save = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "save", "--course", "Data Structures", "--active"],
                input=SNAPSHOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(save.returncode, 0, save.stderr)

            load = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "load", "--active"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(load.returncode, 0, load.stderr)
            self.assertEqual(load.stdout, SNAPSHOT)

            active = Path(tmp) / ".oh-my-teacher" / "snapshots" / "_active"
            self.assertEqual(active.read_text(encoding="utf-8"), "data-structures")

    def test_validate_well_formed_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "save"],
                input=SNAPSHOT,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "validate"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("notes", result.stdout)
            self.assertNotIn("WARNING", result.stderr)

    def test_validate_missing_fields(self):
        minimal = """## Current Course Snapshot
- **Course**: test
- **Assessment**: paper
"""
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "save"],
                input=minimal,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "validate"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("WARNING", result.stderr)

    def test_validate_strict_fails_on_missing(self):
        minimal = """## Current Course Snapshot
- **Course**: test
"""
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "save"],
                input=minimal,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "validate", "--strict"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("WARNING", result.stderr)

    def test_validate_strict_requires_tracking_fields(self):
        missing_tracking = """## Current Course Snapshot
- **Course**: test
- **Assessment**: paper
- **Days left**: unknown
- **Level**: shaky
- **Environment**: plain-chat
- **Materials**: notes
- **Weak points**: []
- **Last action**: /profile
- **Next recommended**: /diagnose
"""
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "save"],
                input=missing_tracking,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "validate", "--strict"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("latex", result.stderr.lower())
            self.assertIn("completed", result.stderr.lower())
            self.assertIn("accuracy", result.stderr.lower())

    def test_validate_no_snapshot_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, self._script(), "--workspace", tmp, "validate"],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
