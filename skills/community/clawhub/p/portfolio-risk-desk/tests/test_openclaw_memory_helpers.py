from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.memory import (
    BRIEF_STATE_PREFIX,
    build_memory_recall_args,
    build_memory_store_entries,
    memory_context_from_recalled_memories,
)
from intelligence_desk_brief.normalization import normalize_evidence
from intelligence_desk_brief.orchestrator import create_brief
from intelligence_desk_brief.ranking import rank_evidence


class OpenClawMemoryHelpersTests(unittest.TestCase):
    def test_build_memory_recall_args_is_portfolio_aware(self) -> None:
        request = CreateBriefRequest.from_dict(load_demo_request_payload())

        recall_args = build_memory_recall_args(request)

        self.assertIn("NVDA", recall_args["query"])
        self.assertIn("demo-workspace", recall_args["query"])
        self.assertIn("AI infrastructure", recall_args["query"])
        self.assertEqual(recall_args["limit"], 5)
        self.assertEqual(recall_args["workspace_id"], "demo-workspace")

    def test_build_memory_store_entries_emits_profile_and_brief_state(self) -> None:
        request = CreateBriefRequest.from_dict(load_demo_request_payload())
        brief, _ = create_brief(request)
        normalized = normalize_evidence(load_mock_evidence(), request)
        ranked = rank_evidence(request, normalized)

        entries = build_memory_store_entries(request, brief, ranked)

        self.assertEqual(len(entries), 2)
        self.assertTrue(any("portfolio-risk-desk" in entry["tags"] for entry in entries))
        self.assertTrue(any("demo-workspace" in entry["tags"] for entry in entries))
        self.assertTrue(any(entry["text"].startswith(BRIEF_STATE_PREFIX) for entry in entries))

    def test_memory_context_can_be_reconstructed_from_recalled_memories(self) -> None:
        request = CreateBriefRequest.from_dict(load_demo_request_payload())
        brief, _ = create_brief(request)
        normalized = normalize_evidence(load_mock_evidence(), request)
        ranked = rank_evidence(request, normalized)
        entries = build_memory_store_entries(request, brief, ranked)

        recalled_context = memory_context_from_recalled_memories(
            [{"text": entries[1]["text"]}]
        )

        self.assertFalse(recalled_context.first_run)
        self.assertEqual(
            recalled_context.comparison_baseline,
            "Most recent brief for this portfolio and theme set.",
        )
        self.assertTrue(recalled_context.prior_dominant_factors)
        self.assertTrue(recalled_context.repeated_evidence_fingerprints)


if __name__ == "__main__":
    unittest.main()
