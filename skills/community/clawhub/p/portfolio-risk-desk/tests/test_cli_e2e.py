from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parent.parent


class CliE2ETests(unittest.TestCase):
    def _run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "intelligence_desk_brief",
                *args,
            ],
            cwd=REPO_ROOT,
            env={"PYTHONPATH": "src"},
            capture_output=True,
            text=True,
            check=True,
        )

    def test_create_brief_fixture_json_output(self) -> None:
        result = self._run_cli(
            "create-brief",
            "--fixture",
            "--as-of-date",
            "2026-03-25",
            "--output-format",
            "json",
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["brief_id"], "portfolio-risk-desk-semiconductor-core-2026-03-25")
        self.assertEqual(payload["delivery_status"], "inline_returned")
        self.assertEqual(payload["workspace_id"], "demo-workspace")
        self.assertEqual(payload["scenario_analysis"][0]["confidence_level"], "medium")

    def test_run_demo_happy_json_output(self) -> None:
        result = self._run_cli("run-demo", "--mode", "happy", "--output-format", "json")

        payload = json.loads(result.stdout)
        self.assertEqual(payload["delivery_status"], "handoff_recorded")
        self.assertTrue(payload["dominant_factors"])
        self.assertTrue(payload["scenario_analysis"])

    def test_run_benchmarks_json_output(self) -> None:
        result = self._run_cli("run-benchmarks", "--output-format", "json")

        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 2)
        results = {item["name"]: item for item in payload}
        self.assertEqual(results["good_build_fixture"]["score"], 5)
        self.assertLess(results["degraded_build_sparse"]["score"], results["good_build_fixture"]["score"])


if __name__ == "__main__":
    unittest.main()
