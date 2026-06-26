from __future__ import annotations

from datetime import date
import unittest

from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload
from intelligence_desk_brief.orchestrator import PortfolioRiskDesk
from intelligence_desk_brief.config import AppConfig


class RendererTests(unittest.TestCase):
    def test_fixture_markdown_contains_required_sections(self) -> None:
        runtime = PortfolioRiskDesk(AppConfig())
        request = CreateBriefRequest.from_dict(load_demo_request_payload())

        _, markdown = runtime.create_brief(request, as_of_date=date(2026, 3, 25))

        self.assertIn("# Portfolio Risk Desk - 2026-03-25", markdown)
        self.assertIn("## 0) User focus", markdown)
        self.assertIn("## 2) Current exposure map", markdown)
        self.assertIn("## 3) What changed since last brief", markdown)
        self.assertIn("## 5) Scenario analysis", markdown)
        self.assertIn("## 8) Evidence and sources", markdown)
        self.assertIn("## 9) Audit trail", markdown)
        self.assertIn("Delivery status: inline_returned", markdown)


if __name__ == "__main__":
    unittest.main()
