"""Recovery never rewrites a1 or re-freezes the report to manufacture approval."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from prepare_workbuddy_acceptance_review import prepare


class ReviewRetryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        identity = dict(run_id="test", client_scope="client", team_version="2.0.3", host="codex")
        (self.root / "host-orchestration-plan.json").write_text(json.dumps(identity), encoding="utf-8")
        (self.root / "report.json").write_text(json.dumps(dict(identity,report_revision="R1")),encoding="utf-8")
        (self.root / "review-manifest.json").write_text(json.dumps(dict(identity, report_revision="R1",manifest_sha256="a" * 64, artifacts=[], sources=[])), encoding="utf-8")
        self.journal = MagicMock()
        self.journal.events.return_value = [dict(kind="member_rejected", payload=dict(role="delivery-review", attempt_id="delivery-review-r1-a1")), dict(kind="model_observation", payload=dict(role="delivery-review"))]
        for target, value in (("Journal", self.journal),):
            patcher = patch("prepare_workbuddy_acceptance_review." + target, return_value=value)
            patcher.start(); self.addCleanup(patcher.stop)
        patcher = patch("prepare_workbuddy_acceptance_review.validate_manifest")
        patcher.start(); self.addCleanup(patcher.stop)
        patcher = patch("prepare_workbuddy_acceptance_review.changed_entries", return_value=([], []))
        self.changes = patcher.start(); self.addCleanup(patcher.stop)

    def test_a2_separate_paths_and_preserves_freeze(self):
        before = (self.root / "review-manifest.json").read_bytes()
        result = prepare(self.root, self.root, "codex", 2)
        self.assertEqual(before, (self.root / "review-manifest.json").read_bytes())
        self.assertIn("a2.return.json", result["wait_command"])
        self.assertIn("--attempt-number 2", result["finalize_command_template"])
        self.assertFalse((self.root / "review-launch-manifest.json").exists())
        self.assertTrue((self.root / "review-launch-manifest-a2.json").exists())
        card = json.loads(Path(result["card_path"]).read_text(encoding="utf-8"))
        self.assertEqual(card["raw_result_identity"]["agent_version"], "2.0.3")
        with self.assertRaisesRegex(ValueError, "already_exists"):
            prepare(self.root, self.root, "codex", 2)

    def test_waiting_or_passed_not_retried(self):
        for state in ("member_started", "member_returned"):
            self.journal.events.return_value = [dict(kind=state, payload=dict(role="delivery-review", attempt_id="delivery-review-r1-a1"))]
            with self.assertRaisesRegex(ValueError, "terminal_a1"):
                prepare(self.root, self.root, "codex", 2)

    def test_changed_report_not_refrozen(self):
        self.changes.return_value = (["report.pdf"], [])
        with self.assertRaisesRegex(ValueError, "frozen_files_changed"):
            prepare(self.root, self.root, "codex", 2)

    def test_third_attempt_not_allowed(self):
        with self.assertRaisesRegex(ValueError, "retry_exhausted"):
            prepare(self.root, self.root, "codex", 3)


if __name__ == "__main__":
    unittest.main()
