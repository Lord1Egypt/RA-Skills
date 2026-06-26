from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.exposure_mapping import build_exposure_outputs
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.source_taxonomy import classify_evidence


def _fixture_inputs() -> tuple[CreateBriefRequest, list[dict[str, object]]]:
    request = CreateBriefRequest.from_dict(load_demo_request_payload())
    normalized = normalize_evidence(load_mock_evidence(), request)
    ranked = rank_evidence(request, normalized)
    return request, classify_evidence(ranked, request)


class ExposureMappingTests(unittest.TestCase):
    def test_exposure_map_is_built_from_ranked_evidence(self) -> None:
        request, evidence = _fixture_inputs()
        current_exposure_map, dominant_factors = build_exposure_outputs(request, evidence)

        self.assertGreaterEqual(len(current_exposure_map), 3)
        self.assertEqual(current_exposure_map[0]["name"], "AI infrastructure concentration")
        self.assertEqual(len(dominant_factors), 6)

    def test_dominant_factors_keep_template_coverage(self) -> None:
        request, evidence = _fixture_inputs()
        _, dominant_factors = build_exposure_outputs(request, evidence)
        by_factor = {item["factor"]: item for item in dominant_factors}

        self.assertEqual(by_factor["AI capex and infrastructure sensitivity"]["stance"], "strengthened")
        self.assertIn(
            "Policy-sensitive evidence",
            by_factor["China, regulation, or policy exposure"]["impact_summary"],
        )


if __name__ == "__main__":
    unittest.main()
