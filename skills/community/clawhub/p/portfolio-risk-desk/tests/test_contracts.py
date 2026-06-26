from __future__ import annotations

import unittest

from intelligence_desk_brief.contracts import (
    ContractValidationError,
    CreateBriefRequest,
    CreateBriefResponse,
    WriteBriefToNotionInput,
    WriteBriefToNotionOutput,
)
from intelligence_desk_brief.fixtures import load_demo_request_payload
from intelligence_desk_brief.orchestrator import PortfolioRiskDesk, create_brief
from intelligence_desk_brief.config import AppConfig


class ContractTests(unittest.TestCase):
    def test_valid_fixture_payload_round_trips_through_contract(self) -> None:
        request = CreateBriefRequest.from_dict(load_demo_request_payload())
        brief, _ = create_brief(request)
        validated = CreateBriefResponse.from_dict(brief.to_dict())

        self.assertEqual(validated.delivery_status.value, "inline_returned")
        self.assertEqual(validated.workspace_id, "demo-workspace")
        self.assertEqual(validated.profile_name, "semiconductor-core")
        self.assertEqual(validated.scenario_analysis[0].confidence_level, "medium")
        self.assertIn("dominant_factors", validated.audit_trail)
        self.assertTrue(validated.audit_trail["scenarios"])

    def test_missing_themes_fails_fast(self) -> None:
        payload = load_demo_request_payload()
        payload["themes"] = []

        with self.assertRaises(ContractValidationError):
            CreateBriefRequest.from_dict(payload)

    def test_scenarios_require_confidence_level(self) -> None:
        request = CreateBriefRequest.from_dict(load_demo_request_payload())
        brief, _ = create_brief(request)
        payload = brief.to_dict()
        del payload["scenario_analysis"][0]["confidence_level"]

        with self.assertRaises(ContractValidationError):
            CreateBriefResponse.from_dict(payload)

    def test_write_brief_to_notion_contract_requires_workspace_id(self) -> None:
        with self.assertRaises(ContractValidationError):
            WriteBriefToNotionInput.from_dict(
                {
                    "brief_payload": {"brief_id": "test"},
                    "parent_page_id": "page-123",
                }
            )

    def test_notion_handoff_round_trips_with_delivery_metadata(self) -> None:
        runtime = PortfolioRiskDesk(AppConfig(notion_parent_page_id="demo-parent"))
        request = CreateBriefRequest.from_dict(
            {
                **load_demo_request_payload(),
                "delivery_target": "notion",
            }
        )
        brief, _ = runtime.create_brief(request)
        validated = CreateBriefResponse.from_dict(brief.to_dict())

        self.assertEqual(validated.delivery_status.value, "handoff_recorded")
        self.assertEqual(validated.delivery_metadata["workspace_id"], "demo-workspace")
        self.assertEqual(validated.delivery_metadata["section_count"], 11)
        self.assertEqual(validated.delivery_metadata["integration_target"], "openclaw_notion_handoff")
        self.assertGreater(validated.delivery_metadata["audit_section_count"], 0)

        handoff_output = WriteBriefToNotionOutput.from_dict(
            {
                "notion_page_id": "openclaw-handoff",
                "url": "https://openclaw.local/notion-handoff",
                "status": "accepted",
                "delivery_metadata": {"workspace_id": "demo-workspace"},
            }
        )
        self.assertEqual(handoff_output.status.value, "accepted")

    def test_direct_handoff_request_preserves_structured_payload(self) -> None:
        runtime = PortfolioRiskDesk(AppConfig(notion_parent_page_id="demo-parent"))
        result = runtime.write_brief_to_notion(
            WriteBriefToNotionInput.from_dict(
                {
                    "brief_payload": {"brief_id": "brief-123"},
                    "parent_page_id": "demo-parent",
                    "workspace_id": "demo-workspace",
                    "brief_title": "Portfolio Risk Desk - 2026-03-25",
                    "delivery_payload": {
                        "handoff_version": "v1",
                        "integration_target": "openclaw_notion_handoff",
                        "ordered_sections": [{"id": "summary", "title": "Summary", "content": "Test"}],
                        "audit_bundle": {"scenarios": [{"claim": "Scenario"}]},
                        "failure_semantics": {"fallback_delivery_status": "failed"},
                    },
                }
            )
        )
        self.assertEqual(result.status.value, "accepted")
        self.assertEqual(result.delivery_metadata["section_count"], 1)
        self.assertEqual(result.delivery_metadata["handoff_version"], "v1")
        self.assertEqual(result.delivery_metadata["fallback_delivery_status"], "failed")


if __name__ == "__main__":
    unittest.main()
