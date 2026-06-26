from __future__ import annotations

import unittest

from property_advisor.models import PreflightCheck, PreflightReport, SearchRequest
from property_advisor.orchestrator import PropertyAdvisorOrchestrator


class FakeOKClient:
    def __init__(self, listings, details):
        self._listings = listings
        self._details = details
        self.search_calls = []
        self.detail_calls = []

    def doctor(self, *, run_browser_smoke: bool = True):
        return PreflightReport(
            ok=True,
            skill_root="/fake/ok-core-skill",
            selected_runner="uv",
            checks=[PreflightCheck(name="doctor", ok=True, message="ok")],
        )

    def search_property(self, **kwargs):
        self.search_calls.append(kwargs)
        return [dict(item) for item in self._listings]

    def browse_property(self, **kwargs):
        return self.search_property(**kwargs)

    def get_listing_detail(self, *, url: str):
        self.detail_calls.append(url)
        return dict(self._details[url])


class FakeMapClient:
    def __init__(self, report):
        self.report = report
        self.calls = []

    def doctor(self):
        return {"status": "ok"}

    def analyze_batch(self, *, listings, destination: str = "", city: str = ""):
        self.calls.append({"listings": listings, "destination": destination, "city": city})
        return self.report


class FailingSearchClient(FakeOKClient):
    source_name = "gt-core-skill"
    runtime_mode = "bridge"

    def search_property(self, **kwargs):
        raise RuntimeError("页面加载超时")


class PropertyAdvisorOrchestratorTests(unittest.TestCase):
    def test_hydrates_details_and_uses_map_assessments(self) -> None:
        listings = [
            {
                "id": "l1",
                "title": "The Archive, Southbank",
                "price": "A$786/wk",
                "location": "Southbank VIC",
                "url": "https://example.test/archive",
            },
            {
                "id": "l2",
                "title": "Southbank Apartment",
                "price": "A$645/wk",
                "location": "Southbank VIC",
                "url": "https://example.test/southbank",
            },
        ]
        details = {
            "https://example.test/archive": {
                **listings[0],
                "description": "1 bedroom apartment with parking and tram access.",
                "images": ["https://example.test/archive1.jpg", "https://example.test/archive2.jpg"],
            },
            "https://example.test/southbank": {
                **listings[1],
                "description": "1 bedroom apartment in Southbank.",
                "images": ["https://example.test/southbank1.jpg"],
            },
        }
        map_report = {
            "status": "ok",
            "listings": [
                {
                    "id": "l1",
                    "geo": {"precision": "address", "confidence": "medium"},
                    "verification_links": {"google_maps_manual": "https://maps.test/archive"},
                    "assessments": {
                        "transport_access": {
                            "conclusion": "交通条件已有地址级 OSM 证据，可用于首轮排序。",
                            "evidence": ["到 Stop 126 直线估算约 150-200m。"],
                        },
                        "daily_convenience": {
                            "conclusion": "生活便利度较好。",
                            "evidence": ["800m 范围内记录到超市 3 家。"],
                        },
                        "environment_risk": {
                            "conclusion": "当前未见明显高风险环境信号，但仍不等于实地安静。",
                            "evidence": ["未记录到明显主路、轨道或工业用地信号。"],
                        },
                        "area_maturity": {
                            "conclusion": "区域成熟度较高。",
                            "evidence": ["当前片区公开 OSM 记录到的常用配套总量约 12 项。"],
                        },
                    },
                    "limitations": ["route_time_is_estimated"],
                },
                {
                    "id": "l2",
                    "geo": {"precision": "missing", "confidence": "low"},
                    "verification_links": {"google_maps_manual": "https://maps.test/southbank"},
                    "assessments": {
                        "transport_access": {
                            "conclusion": "自动地图定位失败，交通结论需人工复核。",
                            "evidence": ["未拿到可用经纬度，只能提供手动地图复核链接。"],
                        },
                        "daily_convenience": {
                            "conclusion": "周边生活便利度自动分析失败，需要人工复核。",
                            "evidence": ["未拿到可靠位置或配套数据。"],
                        },
                        "environment_risk": {
                            "conclusion": "环境风险自动分析失败，需要人工复核噪音和工业用地。",
                            "evidence": ["未拿到可靠位置。"],
                        },
                        "area_maturity": {
                            "conclusion": "区域成熟度无法自动判断，需要人工复核。",
                            "evidence": ["缺少可用定位。"],
                        },
                    },
                    "limitations": ["geo_missing"],
                },
            ],
        }
        orchestrator = PropertyAdvisorOrchestrator(FakeOKClient(listings, details), FakeMapClient(map_report))

        report = orchestrator.search(
            SearchRequest(
                keyword="southbank apartment",
                country="australia",
                city="melbourne",
                destination="Melbourne CBD VIC",
                max_results=2,
                detail_limit=2,
                budget_max=3200,
                bedrooms=1,
            )
        )

        self.assertEqual(report.summary["visible_candidates"], 2)
        self.assertEqual(report.summary["detail_hydrated"], 2)
        self.assertIn("selected_source_id", report.summary)
        self.assertEqual(report.candidate_rows[0].listing_url, "https://example.test/archive")
        self.assertEqual(report.candidate_rows[0].status, "推荐")
        self.assertEqual(report.candidate_rows[1].status, "待人工复核")
        self.assertIn("交通条件已有地址级 OSM 证据，可用于首轮排序。", report.candidate_rows[0].satisfied[4])

    def test_ok_gt_searches_warn_that_results_are_not_full_market_coverage(self) -> None:
        listings = [
            {
                "id": "visible",
                "title": "Visible Listing",
                "price": "A$620/wk",
                "location": "Southbank VIC",
                "url": "https://example.test/visible",
            }
        ]
        details = {
            "https://example.test/visible": {
                **listings[0],
                "description": "1 bedroom apartment with photos.",
                "images": ["https://example.test/visible.jpg"],
            }
        }
        orchestrator = PropertyAdvisorOrchestrator(FakeOKClient(listings, details), FakeMapClient({"status": "ok", "listings": []}))

        report = orchestrator.search(SearchRequest(keyword="southbank", resolved_source_id="ok", resolved_market="ok"))

        self.assertTrue(any("不代表已覆盖所有房产平台" in warning for warning in report.warnings))

    def test_search_source_failure_returns_structured_report_not_traceback(self) -> None:
        orchestrator = PropertyAdvisorOrchestrator(FailingSearchClient([], {}), FakeMapClient({"status": "ok", "listings": []}))

        report = orchestrator.search(SearchRequest(keyword="flat", resolved_source_id="gt", resolved_market="gt"))

        self.assertEqual(report.summary["visible_candidates"], 0)
        self.assertEqual(report.selected_source, "gt-core-skill")
        self.assertIn("search failed", report.errors[0])
        self.assertIn("页面加载超时", report.errors[0])

    def test_missing_original_listing_url_is_hidden_from_table(self) -> None:
        listings = [
            {
                "id": "hidden",
                "title": "Missing Link Listing",
                "price": "A$500/wk",
                "location": "Southbank VIC",
            },
            {
                "id": "visible",
                "title": "Visible Listing",
                "price": "A$620/wk",
                "location": "Southbank VIC",
                "url": "https://example.test/visible",
            },
        ]
        details = {
            "https://example.test/visible": {
                **listings[1],
                "description": "1 bedroom apartment with photos.",
                "images": ["https://example.test/visible.jpg"],
            }
        }
        map_report = {
            "status": "partial",
            "listings": [
                {
                    "id": "visible",
                    "geo": {"precision": "area", "confidence": "low"},
                    "verification_links": {"google_maps_manual": "https://maps.test/visible"},
                    "assessments": {
                        "transport_access": {"conclusion": "当前只有区域级位置，交通只能做片区参考，不能作为楼栋级步行距离结论。", "evidence": ["到 Melbourne CBD VIC 只能做区域级直线估算。"]},
                        "daily_convenience": {"conclusion": "区域级配套成熟度可做参考，但不能直接代表房源楼下的便利度。", "evidence": ["800m 范围内记录到超市 2 家。"]},
                        "environment_risk": {"conclusion": "区域级环境风险可做参考，噪音源距离仍需人工复核。", "evidence": ["未记录到明显主路、轨道或工业用地信号。"]},
                        "area_maturity": {"conclusion": "区域成熟度中等。这个结论只能代表片区，不代表具体楼栋。", "evidence": ["当前片区公开 OSM 记录到的常用配套总量约 6 项。"]},
                    },
                    "limitations": ["area_level_location"],
                }
            ],
        }
        orchestrator = PropertyAdvisorOrchestrator(FakeOKClient(listings, details), FakeMapClient(map_report))

        report = orchestrator.search(SearchRequest(keyword="southbank", city="melbourne", country="australia"))

        self.assertEqual(len(report.hidden_candidates), 1)
        self.assertEqual(report.hidden_candidates[0]["candidate_name"], "Missing Link Listing")
        self.assertNotIn("Missing Link Listing", report.rendered_table)
        self.assertIn("Visible Listing", report.rendered_table)

    def test_abnormal_low_price_is_marked_as_elimination_risk(self) -> None:
        listings = [
            {"id": "a", "title": "Candidate A", "price": "A$100/wk", "location": "Southbank VIC", "url": "https://example.test/a"},
            {"id": "b", "title": "Candidate B", "price": "A$700/wk", "location": "Southbank VIC", "url": "https://example.test/b"},
            {"id": "c", "title": "Candidate C", "price": "A$720/wk", "location": "Southbank VIC", "url": "https://example.test/c"},
        ]
        details = {
            "https://example.test/a": {**listings[0], "description": "Studio listing", "images": ["https://example.test/a.jpg"]},
            "https://example.test/b": {**listings[1], "description": "1 bedroom apartment", "images": ["https://example.test/b.jpg"]},
            "https://example.test/c": {**listings[2], "description": "1 bedroom apartment", "images": ["https://example.test/c.jpg"]},
        }
        map_report = {"status": "degraded", "listings": []}
        orchestrator = PropertyAdvisorOrchestrator(FakeOKClient(listings, details), FakeMapClient(map_report))

        report = orchestrator.search(SearchRequest(keyword="southbank", city="melbourne", country="australia"))

        by_id = {row.source_id: row for row in report.candidate_rows}
        self.assertEqual(by_id["a"].status, "淘汰")
        self.assertTrue(any("异常低价" in item or "疑似异常低价" in item for item in by_id["a"].elimination_or_risk))


if __name__ == "__main__":
    unittest.main()
