from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.scenario_engine import build_scenarios
from intelligence_desk_brief.source_taxonomy import classify_evidence


def _fixture_inputs() -> tuple[CreateBriefRequest, list[dict[str, object]]]:
    request = CreateBriefRequest.from_dict(load_demo_request_payload())
    normalized = normalize_evidence(load_mock_evidence(), request)
    ranked = rank_evidence(request, normalized)
    return request, classify_evidence(ranked, request)


class ScenarioEngineTests(unittest.TestCase):
    def test_fixture_scenarios_include_confidence_evidence_and_falsifiers(self) -> None:
        request, evidence = _fixture_inputs()
        scenarios = build_scenarios(request, evidence)

        self.assertEqual(len(scenarios), 2)
        self.assertTrue(all(item.confidence_level in {"low", "medium", "high"} for item in scenarios))
        self.assertTrue(all(item.supporting_evidence for item in scenarios))
        self.assertTrue(all(item.falsifiers for item in scenarios))

    def test_rates_scenario_uses_rates_evidence(self) -> None:
        request, evidence = _fixture_inputs()
        scenarios = build_scenarios(request, evidence)
        rates_scenario = scenarios[0]

        self.assertIn("Rates move higher again", rates_scenario.scenario)
        self.assertTrue(
            any("Fed minutes" in source["title"] for source in rates_scenario.supporting_evidence)
        )


if __name__ == "__main__":
    unittest.main()
