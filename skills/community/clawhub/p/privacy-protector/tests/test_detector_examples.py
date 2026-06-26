#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "privacy-protector" / "scripts" / "detect_local.py"
EXAMPLES_DIR = REPO_ROOT / "privacy-protector" / "examples" / "detect-local"


class TestDetectorExamples(unittest.TestCase):
    def _run_cli(self, args):
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH)] + args,
            capture_output=True,
            text=True,
            env=os.environ.copy(),
        )

    def test_allowlist_example_suppresses_shipped_support_email(self):
        result = self._run_cli(
            [
                "--input",
                "Reach support@example.com for status updates",
                "--allowlist-file",
                str(EXAMPLES_DIR / "allowlist.json"),
                "--json",
            ]
        )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual([item for item in payload["items"] if item["type"] == "email"], [])

    def test_blocklist_example_forces_detection(self):
        result = self._run_cli(
            [
                "--input",
                "Project codename Phoenix is approved",
                "--blocklist-file",
                str(EXAMPLES_DIR / "blocklist.json"),
                "--json",
            ]
        )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        forced_items = [item for item in payload["items"] if item["value"] == "Phoenix"]
        self.assertGreaterEqual(len(forced_items), 1)
        self.assertTrue(forced_items[0]["forcedBlocklist"])

    def test_threshold_example_suppresses_email_detection(self):
        result = self._run_cli(
            [
                "--input",
                "Email: alice@example.com",
                "--thresholds-file",
                str(EXAMPLES_DIR / "thresholds.json"),
                "--json",
            ]
        )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual([item for item in payload["items"] if item["type"] == "email"], [])


if __name__ == "__main__":
    unittest.main()
