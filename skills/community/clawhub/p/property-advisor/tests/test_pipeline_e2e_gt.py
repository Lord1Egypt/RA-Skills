from __future__ import annotations

import unittest

from property_advisor import PropertyAdvisorOrchestrator, SearchRequest
from property_advisor.models import PreflightCheck, PreflightReport


class FakeMapClient:
    def __init__(self, report):
        self.report = report

    def doctor(self):
        return {"status": "ok"}

    def analyze_batch(self, *, listings, destination: str = "", city: str = ""):
        return self.report


class FakeBridgeGTClient:
    source_name = "gt-core-skill"
    runtime_mode = "bridge"
    detail_supported = True

    def __init__(self):
        self._warnings = []
        self.doctor_flags = []

    def doctor(self, *, run_browser_smoke: bool = True):
        self.doctor_flags.append(run_browser_smoke)
        return PreflightReport(
            ok=True,
            skill_root="/fake/gt-core-skill",
            selected_runner="uv",
            checks=[PreflightCheck(name="doctor", ok=True, message="ok")],
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
            detail_supported=self.detail_supported,
            logged_in=False,
            warnings=["Gumtree 当前未登录，但公开搜索与详情抓取仍可用。"],
        )

    def search_property(self, **kwargs):
        return [
            {
                "id": "1511100050",
                "listing_id": "1511100050",
                "title": "HMO Studio Flat",
                "price": None,
                "location": "Heathrow, London",
                "url": "https://www.gumtree.com/p/property-to-rent/hmo-studio-flat/1511100050",
            }
        ]

    def browse_property(self, **kwargs):
        return self.search_property(**kwargs)

    def get_listing_detail(self, *, url: str):
        return {
            "id": "1511100050",
            "listing_id": "1511100050",
            "title": "HMO Studio Flat",
            "price": "£1,000pm",
            "location": "Heathrow, London",
            "url": url,
            "images": ["https://img.gumtree.com/sample/1"],
            "description": "Modern private studio flat.",
            "detail_fetched": True,
            "attributes": {
                "Number Of Bedrooms": "Studio",
                "Property Type": "Flat",
                "Date Available": "31 Mar 2026",
            },
            "bedrooms_text": "Studio",
        }

    def drain_warnings(self):
        warnings = list(self._warnings)
        self._warnings.clear()
        return warnings


class FakeApiGTClient:
    source_name = "gt-core-skill"
    runtime_mode = "api"
    detail_supported = False

    def __init__(self):
        self.doctor_flags = []

    def doctor(self, *, run_browser_smoke: bool = True):
        self.doctor_flags.append(run_browser_smoke)
        return PreflightReport(
            ok=True,
            skill_root="/fake/gt-core-skill-api",
            selected_runner="python3",
            checks=[PreflightCheck(name="doctor", ok=True, message="ok")],
            source_name=self.source_name,
            runtime_mode=self.runtime_mode,
            detail_supported=self.detail_supported,
        )

    def search_property(self, **kwargs):
        return [
            {
                "id": "1511100050",
                "listing_id": "1511100050",
                "title": "API Studio Flat",
                "price": "£1,000",
                "location": "Richmond",
                "url": "https://www.gumtree.com/p/property-to-rent/api-studio-flat/1511100050",
                "image_url": "https://img.gumtree.com/sample/1",
            }
        ]

    def browse_property(self, **kwargs):
        return self.search_property(**kwargs)

    def get_listing_detail(self, *, url: str):
        return {
            "url": url,
            "detail_fetched": False,
            "detail_degraded": True,
            "detail_degraded_reason": "GT 当前运行模式不支持详情补全",
        }

    def drain_warnings(self):
        return []


class GTPipelineE2ETests(unittest.TestCase):
    def test_bridge_gt_pipeline_keeps_table_shape(self) -> None:
        map_report = {
            "status": "ok",
            "listings": [
                {
                    "id": "1511100050",
                    "geo": {"precision": "address", "confidence": "medium"},
                    "verification_links": {"google_maps_manual": "https://maps.test/gt"},
                    "assessments": {
                        "transport_access": {"conclusion": "交通可达性较好。", "evidence": ["附近存在公交与铁路接驳。"]},
                        "daily_convenience": {"conclusion": "生活便利度较好。", "evidence": ["800m 内存在超市和餐饮。"]},
                        "environment_risk": {"conclusion": "环境风险暂未见明显高信号。", "evidence": ["未记录到显著工业干扰。"]},
                        "area_maturity": {"conclusion": "区域成熟度较高。", "evidence": ["常用配套较集中。"]},
                    },
                    "limitations": [],
                }
            ],
        }
        client = FakeBridgeGTClient()
        orchestrator = PropertyAdvisorOrchestrator(client, FakeMapClient(map_report))

        report = orchestrator.search(
            SearchRequest(
                keyword="flat",
                country="united kingdom",
                city="London",
                market_hint="gt",
                resolved_market="gt",
                routing_reason="uk_semantic_match",
                search_location_hint="London",
                budget_max=1200,
            )
        )

        self.assertFalse(report.errors)
        self.assertEqual(client.doctor_flags, [False])
        self.assertEqual(report.selected_source, "gt-core-skill")
        self.assertEqual(report.selected_runtime_mode, "bridge")
        self.assertEqual(set(report.candidate_rows[0].to_display_row().keys()), {"候选房源", "状态", "价格", "位置", "已满足", "缺失/未知", "淘汰原因/风险", "房源链接"})
        self.assertIn("£1,000pm", report.rendered_table)

    def test_api_gt_pipeline_surfaces_detail_degradation(self) -> None:
        map_report = {"status": "degraded", "listings": []}
        client = FakeApiGTClient()
        orchestrator = PropertyAdvisorOrchestrator(client, FakeMapClient(map_report))

        report = orchestrator.search(
            SearchRequest(
                keyword="flat",
                country="united kingdom",
                city="London",
                market_hint="gt",
                resolved_market="gt",
                routing_reason="uk_semantic_match",
                search_location_hint="London",
            )
        )

        self.assertFalse(report.errors)
        self.assertEqual(client.doctor_flags, [False])
        self.assertEqual(report.selected_runtime_mode, "api")
        self.assertIn("GT 当前运行模式不支持详情补全", report.candidate_rows[0].missing_or_unknown)
        self.assertIn("API Studio Flat", report.rendered_table)


if __name__ == "__main__":
    unittest.main()
