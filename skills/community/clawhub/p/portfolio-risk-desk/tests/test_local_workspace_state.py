from __future__ import annotations

from datetime import date
import tempfile
import unittest

from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload
from intelligence_desk_brief.orchestrator import PortfolioRiskDesk


class LocalWorkspaceStateTests(unittest.TestCase):
    def test_local_state_dir_makes_second_run_memory_aware(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = PortfolioRiskDesk(AppConfig(local_state_dir=temp_dir))
            request = CreateBriefRequest.from_dict(load_demo_request_payload())

            first_brief, _ = runtime.create_brief(request, as_of_date=date(2026, 3, 25))
            second_brief, _ = runtime.create_brief(request, as_of_date=date(2026, 3, 26))

            self.assertEqual(first_brief.delivery_status.value, "inline_returned")
            self.assertEqual(
                second_brief.user_focus.comparison_baseline,
                "Most recent brief for this portfolio and theme set.",
            )
            self.assertIn("Since the last brief", second_brief.summary)


if __name__ == "__main__":
    unittest.main()
