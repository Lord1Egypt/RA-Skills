from __future__ import annotations

import json
from unittest.mock import patch
import unittest
from urllib.error import URLError

from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.retrieval import LiveRetrievalAdapter


class _FakeResponse:
    def __init__(self, payload: list[dict[str, object]]):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        del exc_type, exc, tb


class Order2LiveEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = CreateBriefRequest.from_dict(load_demo_request_payload())
        self.config = AppConfig(
            apify_api_token="token",
            apify_task_id="primary-task",
            apify_x_task_id="x-task",
            enable_live_providers=True,
            enable_x_signals=True,
        )

    def test_live_retrieval_collects_primary_and_x_items(self) -> None:
        adapter = LiveRetrievalAdapter(self.config)

        responses = [
            _FakeResponse(
                [
                    {
                        "query": '"NVDA" earnings OR "investor relations" OR guidance',
                        "position": 1,
                        "title": "NVIDIA Announces Earnings Release Date",
                        "url": "https://investor.nvidia.com/news/default.aspx",
                        "description": "Investor relations update for NVDA earnings timing.",
                        "date": "Mar 25, 2026",
                        "searchUrl": "https://google.com/search?q=nvda",
                    }
                ]
            ),
            _FakeResponse(
                [
                    {
                        "id": "x-1",
                        "url": "https://x.com/nvidia/status/1",
                        "twitterUrl": "https://twitter.com/nvidia/status/1",
                        "full_text": "NVIDIA posts an update on AI infrastructure demand.",
                        "created_at": "Tue Feb 28 20:28:53 +0000 2023",
                        "author": {
                            "screen_name": "nvidia",
                            "verified": True,
                            "followers_count": 1000000,
                        },
                        "searchTerm": '("NVDA" OR "$NVDA") lang:en -is:retweet',
                    }
                ]
            ),
        ]

        with (
            patch.object(adapter, "_build_primary_inputs", return_value=[{"query": "NVDA earnings"}]),
            patch("intelligence_desk_brief.retrieval.urlopen", side_effect=responses),
        ):
            items = adapter.collect(self.request)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["provider"], "apify")
        self.assertEqual(items[0]["source_type"], "google_search_result")
        self.assertEqual(items[0]["affected_names"], ["NVDA"])
        self.assertEqual(items[1]["source_type"], "x_post")
        self.assertEqual(items[1]["affected_names"], ["NVDA"])

    def test_task_ids_allow_owner_slash_name_input(self) -> None:
        adapter = LiveRetrievalAdapter(self.config)

        self.assertEqual(
            adapter._normalize_task_id("compassionate_rye/web-search-task"),
            "compassionate_rye~web-search-task",
        )
        self.assertEqual(
            adapter._normalize_task_id("compassionate_rye~web-search-task"),
            "compassionate_rye~web-search-task",
        )

    def test_missing_task_ids_can_bootstrap_from_apify_token(self) -> None:
        config = AppConfig(
            apify_api_token="token",
            enable_live_providers=True,
            enable_x_signals=True,
        )
        with patch(
            "intelligence_desk_brief.retrieval.ensure_apify_tasks",
            return_value=[
                {"env_var": "APIFY_TASK_ID", "task_id": "bootstrapped-primary"},
                {"env_var": "APIFY_X_TASK_ID", "task_id": "bootstrapped-x"},
            ],
        ):
            adapter = LiveRetrievalAdapter(config)

        self.assertEqual(adapter._apify_task_id, "bootstrapped-primary")
        self.assertEqual(adapter._apify_x_task_id, "bootstrapped-x")

    def test_partial_failure_returns_notice_and_keeps_run_alive(self) -> None:
        adapter = LiveRetrievalAdapter(self.config)

        with (
            patch.object(adapter, "_build_primary_inputs", return_value=[{"query": "NVDA earnings"}]),
            patch(
                "intelligence_desk_brief.retrieval.urlopen",
                side_effect=URLError("upstream timeout"),
            ),
        ):
            items = adapter.collect(self.request)

        self.assertEqual(len(items), 2)
        self.assertTrue(all(item["item_type"] == "retrieval_notice" for item in items))
        self.assertTrue(all(item["retrieval_status"] == "failed" for item in items))

    def test_retry_can_recover_from_transient_failure(self) -> None:
        adapter = LiveRetrievalAdapter(AppConfig(
            apify_api_token="token",
            apify_task_id="primary-task",
            apify_x_task_id="x-task",
            enable_live_providers=True,
            enable_x_signals=False,
            apify_retry_attempts=2,
        ))

        with (
            patch.object(adapter, "_build_primary_inputs", return_value=[{"query": "NVDA earnings"}]),
            patch(
                "intelligence_desk_brief.retrieval.urlopen",
                side_effect=[
                    URLError("temporary timeout"),
                    _FakeResponse(
                        [
                            {
                                "query": '"NVDA" earnings OR "investor relations" OR guidance',
                                "position": 1,
                                "title": "NVIDIA Announces Earnings Release Date",
                                "url": "https://investor.nvidia.com/news/default.aspx",
                                "description": "Investor relations update for NVDA earnings timing.",
                                "date": "Mar 25, 2026",
                            }
                        ]
                    ),
                ],
            ),
        ):
            items = adapter.collect(self.request)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["item_type"], "evidence")

    def test_no_results_payload_becomes_notice_instead_of_fake_evidence(self) -> None:
        adapter = LiveRetrievalAdapter(self.config)

        with (
            patch.object(adapter, "_build_primary_inputs", return_value=[{"query": "NVDA earnings"}]),
            patch(
                "intelligence_desk_brief.retrieval.urlopen",
                return_value=_FakeResponse([{"noResults": True}]),
            ),
        ):
            items = adapter.collect(self.request)

        self.assertEqual(len(items), 2)
        self.assertTrue(all(item["item_type"] == "retrieval_notice" for item in items))
        self.assertTrue(all(item["retrieval_status"] == "empty" for item in items))

    def test_normalization_and_ranking_demote_failed_or_x_items(self) -> None:
        raw_items = [
            {
                "id": "primary-1",
                "item_type": "evidence",
                "category": "company",
                "factor": "AI capex and infrastructure sensitivity",
                "affected_names": ["NVDA", "TSM", "ASML"],
                "source_title": "Cloud capex callout",
                "url": "https://example.com/cloud",
                "published_at": "2026-03-25T10:00:00+00:00",
                "fact": "Demand remains firm.",
                "interpretation": "High-signal direct evidence.",
                "why_it_matters": "Touches multiple core holdings.",
                "watchpoint": "Next hyperscaler print",
                "confidence_level": "high",
                "signal_strength": "high",
                "retrieval_status": "success",
                "provider": "apify",
                "source_type": "earnings_material",
            },
            {
                "id": "x-1",
                "item_type": "evidence",
                "category": "x_signals",
                "factor": "AI capex and infrastructure sensitivity",
                "affected_names": ["NVDA"],
                "source_title": "X official signal",
                "url": "https://x.com/example/status/1",
                "published_at": "2026-03-25T11:00:00+00:00",
                "fact": "Short official comment.",
                "interpretation": "Supplementary context only.",
                "why_it_matters": "Potentially useful but should not dominate.",
                "watchpoint": "Look for primary-source confirmation",
                "confidence_level": "low",
                "signal_strength": "medium",
                "retrieval_status": "success",
                "provider": "apify",
                "source_type": "x_official",
            },
            {
                "id": "notice-1",
                "item_type": "retrieval_notice",
                "category": "retrieval_status",
                "source_title": "Primary retrieval failed",
                "url": "https://example.com/error",
                "published_at": "2026-03-25T11:30:00+00:00",
                "fact": "One lane failed",
                "interpretation": "Partial evidence only.",
                "confidence_level": "low",
                "signal_strength": "low",
                "retrieval_status": "failed",
                "provider": "apify",
                "source_type": "primary_web",
            },
        ]

        normalized = normalize_evidence(raw_items, self.request)
        ranked = rank_evidence(self.request, normalized)

        self.assertEqual(normalized[0]["direct_relevance"], 3)
        self.assertTrue(normalized[1]["is_x_signal"])
        self.assertTrue(normalized[2]["low_quality"])
        self.assertGreater(ranked[0]["ranking"]["score"], ranked[-1]["ranking"]["score"])
        self.assertEqual(ranked[0]["id"], "primary-1")


if __name__ == "__main__":
    unittest.main()
