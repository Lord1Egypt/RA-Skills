from __future__ import annotations

import unittest

from intelligence_desk_brief.benchmarks import run_quality_benchmarks
from intelligence_desk_brief.demo import run_demo


class DemoAndBenchmarkTests(unittest.TestCase):
    def test_happy_demo_includes_judge_ready_sections(self) -> None:
        result = run_demo("happy")

        self.assertIn("Portfolio Risk Desk", result.markdown)
        self.assertTrue(result.payload["dominant_factors"])
        self.assertTrue(result.payload["scenario_analysis"])
        self.assertEqual(result.payload["delivery_status"], "handoff_recorded")

    def test_failure_demo_still_returns_useful_brief(self) -> None:
        result = run_demo("provider_failure")

        self.assertTrue(result.payload["risk_map_changes"])
        self.assertTrue(result.payload["uncertainty_notes"])
        self.assertTrue(any("degraded" in note.lower() or "uncertainty" in note.lower() for note in result.operator_notes))

    def test_benchmarks_distinguish_good_and_degraded_builds(self) -> None:
        results = {result.name: result for result in run_quality_benchmarks()}

        self.assertGreater(results["good_build_fixture"].score, results["degraded_build_sparse"].score)
        self.assertTrue(results["good_build_fixture"].checks["delta_usefulness"])
        self.assertFalse(results["degraded_build_sparse"].checks["delta_usefulness"])


if __name__ == "__main__":
    unittest.main()
