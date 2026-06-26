#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "privacy-protector" / "scripts" / "detect_local.py"


class TestDetectLocalConfig(unittest.TestCase):
    def _run_cli(self, args):
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH)] + args,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
        )

    def test_allowlist_file_suppresses_email_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            allowlist_file = Path(tmpdir) / "allowlist.json"
            allowlist_file.write_text(
                json.dumps(
                    [
                        {
                            "type": "email",
                            "kind": "exact",
                            "value": "alice@example.com",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = self._run_cli(
                [
                    "--input",
                    "Email: alice@example.com",
                    "--allowlist-file",
                    str(allowlist_file),
                    "--json",
                ]
            )

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["scoringMethod"], "heuristic-v1")
            self.assertEqual(payload["detectorVersion"], "local-rules-v1")
            email_items = [item for item in payload["items"] if item["type"] == "email"]
            self.assertEqual(email_items, [])

    def test_blocklist_file_forces_detection(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            blocklist_file = Path(tmpdir) / "blocklist.json"
            blocklist_file.write_text(
                json.dumps(
                    [
                        {
                            "type": "name",
                            "kind": "exact",
                            "value": "Phoenix",
                        }
                    ]
                ),
                encoding="utf-8",
            )

            result = self._run_cli(
                [
                    "--input",
                    "Project codename Phoenix is approved",
                    "--blocklist-file",
                    str(blocklist_file),
                    "--json",
                ]
            )

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            name_items = [item for item in payload["items"] if item["type"] == "name"]
            self.assertGreaterEqual(len(name_items), 1)
            self.assertTrue(name_items[0]["forcedBlocklist"])
            self.assertIn("detectionScore", name_items[0])
            self.assertIn("scoreThreshold", name_items[0])
            self.assertIn("scoreReasons", name_items[0])

    def test_thresholds_file_overrides_email_threshold(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            thresholds_file = Path(tmpdir) / "thresholds.json"
            thresholds_file.write_text(json.dumps({"email": 0.99}), encoding="utf-8")

            result = self._run_cli(
                [
                    "--input",
                    "Email: alice@example.com",
                    "--thresholds-file",
                    str(thresholds_file),
                    "--json",
                ]
            )

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            email_items = [item for item in payload["items"] if item["type"] == "email"]
            self.assertEqual(email_items, [])

    def test_invalid_blocklist_type_returns_error(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            blocklist_file = Path(tmpdir) / "blocklist-invalid.json"
            blocklist_file.write_text(
                json.dumps([{"type": "*", "kind": "exact", "value": "foo"}]),
                encoding="utf-8",
            )

            result = self._run_cli(
                [
                    "--input",
                    "foo",
                    "--blocklist-file",
                    str(blocklist_file),
                ]
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("blocklist rule requires explicit type", result.stderr)

    def test_explain_flag_prints_scoring_details_to_stderr(self):
        result = self._run_cli(
            [
                "--input",
                "Email: alice@example.com",
                "--explain",
            ]
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("scoringMethod: heuristic-v1", result.stderr)
        self.assertIn("detectorVersion: local-rules-v1", result.stderr)
        self.assertIn("score=", result.stderr)


if __name__ == "__main__":
    unittest.main()
