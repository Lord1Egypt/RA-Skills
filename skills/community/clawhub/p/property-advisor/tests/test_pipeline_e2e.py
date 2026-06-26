from __future__ import annotations

import json
import unittest
from pathlib import Path

from property_advisor import PropertyAdvisorOrchestrator, PublicOsmMapClient, SearchRequest
from property_advisor.models import PreflightCheck, PreflightReport

ROOT = Path(__file__).resolve().parents[1]
MAP_FIXTURES = ROOT / "public-osm-map-context-skill" / "tests" / "fixtures"
EXPECTED_TABLE = ROOT / "tests" / "fixtures" / "expected_candidate_table.md"


class FixtureOKClient:
    def __init__(self) -> None:
        payload = json.loads((MAP_FIXTURES / "melbourne_listings.json").read_text(encoding="utf-8"))
        self.listings = payload["listings"]
        self.details = {
            "https://example.test/archive": {
                **self.listings[0],
                "description": "1 bedroom apartment with study near Montague Street tram stop.",
                "images": [
                    "https://example.test/archive.jpg",
                    "https://example.test/archive2.jpg",
                ],
            },
            "https://example.test/southbank": {
                **self.listings[1],
                "description": "1 bedroom apartment in Southbank with light description only.",
                "images": [
                    "https://example.test/southbank.jpg",
                ],
            },
        }

    def doctor(self, *, run_browser_smoke: bool = True):
        return PreflightReport(
            ok=True,
            skill_root="/fixture/ok-core-skill",
            selected_runner="fixture",
            checks=[PreflightCheck(name="fixture", ok=True, message="fixture ok client")],
        )

    def search_property(self, **kwargs):
        return [dict(item) for item in self.listings]

    def browse_property(self, **kwargs):
        return self.search_property(**kwargs)

    def get_listing_detail(self, *, url: str):
        return dict(self.details[url])


class PipelineE2ETests(unittest.TestCase):
    def test_fixture_pipeline_renders_full_candidate_table(self) -> None:
        orchestrator = PropertyAdvisorOrchestrator(
            FixtureOKClient(),
            PublicOsmMapClient(fixture_dir=MAP_FIXTURES / "osm"),
        )

        report = orchestrator.search(
            SearchRequest(
                keyword="southbank apartment",
                country="australia",
                city="melbourne",
                destination="Melbourne CBD VIC",
                max_results=2,
                detail_limit=2,
                budget_max=3500,
                bedrooms=1,
            )
        )

        self.assertFalse(report.errors)
        self.assertEqual(report.summary["map_status"], "ok")
        self.assertEqual(report.summary["visible_candidates"], 2)
        self.assertEqual(len(report.candidate_rows), 2)
        self.assertTrue(all(set(row.to_display_row().keys()) == {"候选房源", "状态", "价格", "位置", "已满足", "缺失/未知", "淘汰原因/风险", "房源链接"} for row in report.candidate_rows))
        self.assertIn("transport_access", report.candidate_rows[0].map_assessment)
        self.assertIn("daily_convenience", report.candidate_rows[0].map_assessment)
        self.assertIn("environment_risk", report.candidate_rows[0].map_assessment)
        self.assertIn("area_maturity", report.candidate_rows[0].map_assessment)
        expected_table = EXPECTED_TABLE.read_text(encoding="utf-8").strip()
        self.assertEqual(report.rendered_table.strip(), expected_table)


if __name__ == "__main__":
    unittest.main()
