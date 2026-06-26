import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
MANAGER = SKILL_ROOT / "scripts" / "handoff_manager.py"


class HandoffManagerTests(unittest.TestCase):
    def run_manager(self, *args, cwd=None, input_text=None, expect=0):
        proc = subprocess.run(
            [sys.executable, str(MANAGER), *args],
            cwd=cwd,
            input=input_text,
            text=True,
            capture_output=True,
        )
        self.assertEqual(
            proc.returncode,
            expect,
            msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
        )
        return proc

    def create_payload(self):
        return {
            "task_name": "Unit Test Handoff",
            "current_goal": "Verify manager behavior.",
            "completed_this_turn": ["Created test handoff."],
            "current_test_results": ["unittest running"],
            "key_files": ["scripts/handoff_manager.py - manager entrypoint"],
            "unfinished_items": ["finish assertions"],
            "next_actions": ["run full test suite"],
            "commands_and_verification": ["python -m unittest - expected pass"],
            "decisions_and_constraints": ["keep skill lightweight"],
            "known_risks": {"high": "none", "medium": "none", "low": "test fixture only"},
        }

    def test_create_update_recover_and_active_pointer(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.dumps(self.create_payload())
            created = self.run_manager(
                "create",
                "--workspace",
                tmp,
                "--task",
                "Unit Test Handoff",
                "--input-json",
                "-",
                input_text=payload,
            )
            created_json = json.loads(created.stdout)
            self.assertTrue(created_json["valid"])
            handoff = Path(created_json["path"])
            active = Path(created_json["active"])
            self.assertTrue(handoff.exists())
            self.assertTrue(active.exists())
            self.assertIn(str(handoff.resolve()), active.read_text(encoding="utf-8"))

            recovered = self.run_manager("recover", "--workspace", tmp)
            recovered_json = json.loads(recovered.stdout)
            self.assertTrue(recovered_json["found"])
            self.assertTrue(recovered_json["valid"])
            self.assertEqual(Path(recovered_json["path"]), handoff)

            updated = self.run_manager(
                "update",
                "--workspace",
                tmp,
                "--task",
                "Unit Test Handoff",
                "--event",
                "context_compaction",
                "--compaction-count",
                "3",
                "--completed",
                "Updated active handoff.",
            )
            updated_json = json.loads(updated.stdout)
            self.assertTrue(updated_json["valid"])
            self.assertEqual(updated_json["path"], str(handoff.resolve()))
            self.assertEqual(updated_json["recommendation"], "restart_advisable")

    def test_recover_without_handoff_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = self.run_manager("recover", "--workspace", tmp, expect=1)
            payload = json.loads(proc.stdout)
            self.assertFalse(payload["found"])
            self.assertIn("No handoff found", payload["errors"])

    def test_validate_rejects_secret_and_placeholder(self):
        with tempfile.TemporaryDirectory() as tmp:
            created = self.run_manager(
                "create",
                "--workspace",
                tmp,
                "--task",
                "Secret Test",
                "--completed",
                "created fixture",
            )
            handoff = Path(json.loads(created.stdout)["path"])
            handoff.write_text(
                handoff.read_text(encoding="utf-8")
                + "\nAPI_KEY=abcdef1234567890\nTemplate leftover: [path]\n",
                encoding="utf-8",
            )
            proc = self.run_manager("validate", str(handoff), expect=1)
            self.assertIn("Possible secret", proc.stdout)
            self.assertIn("Template placeholder still present", proc.stdout)

    def test_absolute_script_path_from_different_cwd(self):
        with tempfile.TemporaryDirectory() as tmp:
            other_cwd = Path(tmp) / "other"
            other_cwd.mkdir()
            proc = subprocess.run(
                [
                    sys.executable,
                    str(MANAGER.resolve()),
                    "create",
                    "--workspace",
                    tmp,
                    "--task",
                    "Absolute Path Test",
                    "--completed",
                    "absolute invocation",
                ],
                cwd=other_cwd,
                text=True,
                capture_output=True,
            )
            self.assertEqual(proc.returncode, 0, msg=f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
            self.assertTrue(json.loads(proc.stdout)["valid"])

    def test_payload_markdown_is_sanitized(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = self.create_payload()
            payload["next_actions"] = ["first line\n## Injected Heading\n```python\nprint('x')\n```"]
            proc = self.run_manager(
                "create",
                "--workspace",
                tmp,
                "--task",
                "Markdown Sanitize",
                "--input-json",
                "-",
                input_text=json.dumps(payload),
            )
            handoff = Path(json.loads(proc.stdout)["path"])
            text = handoff.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"(?m)^## Injected Heading", text))
            self.assertNotIn("```python", text)


if __name__ == "__main__":
    unittest.main()
