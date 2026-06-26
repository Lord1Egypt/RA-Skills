from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.ranking import rank_evidence
from intelligence_desk_brief.scenario_engine import build_scenarios
from intelligence_desk_brief.signal_noise import build_signal_vs_noise
from intelligence_desk_brief.source_taxonomy import classify_evidence


def _fixture_inputs() -> tuple[CreateBriefRequest, list[dict[str, object]]]:
    request = CreateBriefRequest.from_dict(load_demo_request_payload())
    normalized = normalize_evidence(load_mock_evidence(), request)
    ranked = rank_evidence(request, normalized)
    return request, classify_evidence(ranked, request)


class SignalNoiseTests(unittest.TestCase):
    def test_primary_earnings_evidence_beats_x_commentary(self) -> None:
        request, evidence = _fixture_inputs()
        scenarios = build_scenarios(request, evidence)
        buckets = build_signal_vs_noise(evidence, scenarios)
        by_title = {item["title"]: item["bucket"] for item in buckets}

        self.assertEqual(
            by_title["NVIDIA reports another AI-led beat and raises data center outlook"],
            "high_signal",
        )
        self.assertEqual(
            by_title["X thread warns that semiconductor digestion risk is spreading faster than reported"],
            "noise",
        )


if __name__ == "__main__":
    unittest.main()
