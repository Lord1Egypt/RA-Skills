"""Ensure installation probes use the correct completion mode for each version."""
import unittest
from pathlib import Path
from runtime_acceptance import build_card_instructions, build_resume_prompt


class FormalAcceptanceModeTests(unittest.TestCase):
    def test_formal_card(self):
        text = build_card_instructions("2.0.3", "run", "team", Path("run"), "command")
        self.assertIn("formal_delivery_complete", text)
        self.assertNotIn("candidate_pipeline_complete", text)
        self.assertIn("不传 --candidate-acceptance", text)

    def test_candidate_card(self):
        text = build_card_instructions("2.0.3-candidate.1", "run", "team", Path("run"), "command")
        self.assertIn("candidate_pipeline_complete", text)
        self.assertNotIn("formal_delivery_complete", text)

    def test_formal_resume(self):
        text = build_resume_prompt("2.0.3", Path("run"))
        self.assertIn("completion-receipt.json", text)
        self.assertNotIn("--candidate-acceptance", text)
        self.assertNotIn("candidate_pipeline_complete", text)

    def test_review_identity_includes_required_legacy_boundary(self):
        from artifact_contract import native_receipt_identity
        identity = native_receipt_identity("review_result", "2.0.3")
        self.assertEqual(identity["created_by_team_version"], "2.0.3")
        self.assertIn("legacy_compatibility", identity)


if __name__ == "__main__":
    unittest.main()
