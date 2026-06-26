from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.readthroughs import build_driver_readthroughs
from intelligence_desk_brief.source_taxonomy import classify_evidence


def _fixture_inputs() -> tuple[CreateBriefRequest, list[dict[str, object]]]:
    request = CreateBriefRequest.from_dict(load_demo_request_payload())
    normalized = normalize_evidence(load_mock_evidence(), request)
    ranked = rank_evidence(request, normalized)
    return request, classify_evidence(ranked, request)


class DriverReadthroughTests(unittest.TestCase):
    def test_readthroughs_prioritize_portfolio_relevant_non_x_evidence(self) -> None:
        request, evidence = _fixture_inputs()
        drivers = build_driver_readthroughs(request, evidence)

        self.assertTrue(drivers)
        self.assertNotIn("x_commentary", drivers[0]["evidence_quality"])
        self.assertIn("AI capex", drivers[0]["driver"])

    def test_policy_or_competitor_readthroughs_are_included(self) -> None:
        request, evidence = _fixture_inputs()
        drivers = build_driver_readthroughs(request, evidence)
        qualities = {driver["evidence_quality"] for driver in drivers}

        self.assertTrue(any("policy" in quality or "competitor" in quality for quality in qualities))


if __name__ == "__main__":
    unittest.main()
