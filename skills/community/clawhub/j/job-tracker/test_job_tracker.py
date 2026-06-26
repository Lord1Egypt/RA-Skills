import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class JobTrackerTests(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(__file__).parent
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_arg = ["--base-dir", self.temp_dir.name]

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, *args):
        result = subprocess.run(
            [sys.executable, str(self.base_dir / "scripts" / "job_tracker.py"), *self.base_arg, *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_add_and_list_application(self):
        self.run_cli(
            "add",
            "--company",
            "Example Corp",
            "--role",
            "AI Engineer",
            "--status",
            "applied",
            "--next-follow-up",
            "2026-03-30",
            "--contact-name",
            "Priya",
        )
        listing = self.run_cli("list", "--status", "applied")
        self.assertEqual(len(listing["applications"]), 1)
        self.assertEqual(listing["applications"][0]["company"], "Example Corp")

    def test_due_and_summary(self):
        self.run_cli(
            "add",
            "--company",
            "Contoso",
            "--role",
            "ML Engineer",
            "--status",
            "applied",
            "--next-follow-up",
            "2026-03-25",
        )
        self.run_cli(
            "update",
            "--id",
            "1",
            "--status",
            "interview",
            "--next-follow-up",
            "2026-03-26",
            "--note",
            "Interview booked",
        )
        due = self.run_cli("due", "--on", "2026-03-23", "--window", "7")
        summary = self.run_cli("summary")
        self.assertEqual(len(due["applications"]), 1)
        self.assertEqual(summary["totalApplications"], 1)
        self.assertEqual(summary["byStatus"][0]["status"], "interview")


if __name__ == "__main__":
    unittest.main()
