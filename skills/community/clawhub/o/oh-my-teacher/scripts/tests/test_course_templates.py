"""Tests for scripts/course_templates.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent


class CourseTemplateCliTests(unittest.TestCase):
    def _run(self, args: list[str]) -> subprocess.CompletedProcess:
        script = SCRIPT_DIR / "course_templates.py"
        return subprocess.run(
            [sys.executable, str(script)] + args,
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
        )

    def test_list_includes_common_templates(self):
        result = self._run(["list"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("advanced-math", result.stdout)
        self.assertIn("programming-c-cpp", result.stdout)
        self.assertIn("digital-logic", result.stdout)
        self.assertIn("marxism-basic-principles", result.stdout)

    def test_show_template_outputs_snapshot(self):
        result = self._run(["show", "advanced-math"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("## Current Course Snapshot", result.stdout)
        self.assertIn("高等数学", result.stdout)

    def test_apply_template_writes_snapshot_and_active_slug(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self._run(["--workspace", tmp, "apply", "advanced-math", "--active"])
            self.assertEqual(result.returncode, 0, result.stderr)
            snapshot = Path(tmp) / ".oh-my-teacher" / "snapshots" / "高等数学.md"
            active = Path(tmp) / ".oh-my-teacher" / "snapshots" / "_active"
            state = Path(tmp) / ".oh-my-teacher" / "state.json"
            self.assertTrue(snapshot.exists())
            self.assertEqual(active.read_text(encoding="utf-8"), "高等数学")
            self.assertIn("advanced-math", snapshot.read_text(encoding="utf-8"))
            self.assertTrue(state.exists())

    def test_unknown_template_fails(self):
        result = self._run(["show", "missing-template"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
