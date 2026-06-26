from __future__ import annotations

import unittest

from property_advisor.models import SearchRequest
from property_advisor.routing import apply_market_routing, route_search_request


class RoutingTests(unittest.TestCase):
    def test_uk_city_routes_to_gt_and_rewrites_defaults(self) -> None:
        request = SearchRequest(
            query_text="帮我看看 London 的租房",
            market_hint="auto",
            country_is_default=True,
            city_is_default=True,
        )

        routed, decision = apply_market_routing(request)

        self.assertEqual(decision.market, "gt")
        self.assertEqual(routed.resolved_market, "gt")
        self.assertEqual(routed.country, "united kingdom")
        self.assertEqual(routed.city, "London")
        self.assertEqual(routed.search_location_hint, "London")

    def test_uk_school_or_university_signal_routes_to_gt(self) -> None:
        request = SearchRequest(
            query_text="找靠近 UCL 的 studio",
            market_hint="auto",
            country_is_default=True,
            city_is_default=True,
        )

        decision = route_search_request(request)

        self.assertEqual(decision.market, "gt")
        self.assertEqual(decision.reason, "uk_semantic_match")

    def test_mixed_geography_requires_clarification(self) -> None:
        request = SearchRequest(
            query_text="找 London 或 Melbourne 的 apartment",
            market_hint="auto",
            country_is_default=True,
            city_is_default=True,
        )

        decision = route_search_request(request)

        self.assertIsNone(decision.market)
        self.assertIn("英国市场还是其他市场", decision.error or "")

    def test_explicit_ok_override_wins(self) -> None:
        request = SearchRequest(
            query_text="找 London 的 flat",
            market_hint="ok",
            country="australia",
            city="melbourne",
            country_is_default=False,
            city_is_default=False,
        )

        routed, decision = apply_market_routing(request)

        self.assertEqual(decision.market, "ok")
        self.assertEqual(decision.source_id, "ok")
        self.assertEqual(routed.resolved_market, "ok")
        self.assertEqual(routed.resolved_source_id, "ok")
        self.assertEqual(routed.country, "australia")
        self.assertEqual(routed.city, "melbourne")

    def test_explicit_external_source_is_not_rewritten_to_ok_or_gt(self) -> None:
        request = SearchRequest(
            query_text="找 London 的 flat",
            source_hint="rightmove",
            country_is_default=True,
            city_is_default=True,
        )

        routed, decision = apply_market_routing(request)

        self.assertIsNone(decision.market)
        self.assertEqual(decision.source_id, "rightmove")
        self.assertEqual(routed.resolved_source_id, "rightmove")
        self.assertIn("尚未安装或接入", decision.error or "")

    def test_platform_name_in_query_requires_matching_source(self) -> None:
        request = SearchRequest(
            query_text="帮我分析 Zillow 上 Austin 的房源",
            market_hint="auto",
            country="united states",
            city="Austin",
            country_is_default=False,
            city_is_default=False,
        )

        decision = route_search_request(request)

        self.assertEqual(decision.source_id, "zillow")
        self.assertIn("HasData", decision.error or "")
        self.assertIn("HASDATA_API_KEY", decision.error or "")


if __name__ == "__main__":
    unittest.main()
