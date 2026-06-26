from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.source_taxonomy import classify_evidence


def _classified_fixture_evidence() -> list[dict[str, object]]:
    request = CreateBriefRequest.from_dict(load_demo_request_payload())
    normalized = normalize_evidence(load_mock_evidence(), request)
    ranked = rank_evidence(request, normalized)
    return classify_evidence(ranked, request)


class SourceTaxonomyTests(unittest.TestCase):
    def test_fixture_evidence_gets_lane_classification(self) -> None:
        items = _classified_fixture_evidence()
        lanes = {item["id"]: item["source_lane"] for item in items if item["item_type"] == "evidence"}

        self.assertEqual(lanes["company-nvda-earnings-01"], "earnings_primary")
        self.assertEqual(lanes["policy-china-01"], "policy")
        self.assertEqual(lanes["peer-memory-01"], "competitor")
        self.assertEqual(lanes["investor-letter-01"], "curated_analysis")
        self.assertEqual(lanes["x-commentary-01"], "x_commentary")

    def test_fixture_evidence_gets_quality_and_corroboration_metadata(self) -> None:
        items = _classified_fixture_evidence()
        by_id = {item["id"]: item for item in items if item["item_type"] == "evidence"}

        self.assertEqual(by_id["company-nvda-earnings-01"]["source_quality"], "high")
        self.assertEqual(by_id["x-commentary-01"]["source_quality"], "low")
        self.assertEqual(by_id["company-nvda-earnings-01"]["corroboration_status"], "corroborated")


if __name__ == "__main__":
    unittest.main()
