import concurrent.futures
import json
import tempfile
import unittest
from pathlib import Path

from dispatch_hook import reserve
from run_journal import Journal


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.identity = dict(run_id="test", client_scope="test-client", team_version="2.0.3", host="workbuddy", team_name="omni-ecom-test")
        (self.root / "team-bootstrap.json").write_text(json.dumps(self.identity), encoding="utf-8")
        journal = Journal(self.root / "run-journal.sqlite")
        journal.create("test", "test-client", "2.0.3", "diagnosis")
        journal.close()

    def event(self, role="data-analyst", attempt="a1"):
        card = self.root / "task-cards" / "analysis" / f"{role}-{attempt}.json"
        card.parent.mkdir(parents=True, exist_ok=True)
        card.write_text(json.dumps(dict(self.identity, agent_id=role, attempt_id=attempt)), encoding="utf-8")
        return dict(tool_name="Agent", session_id="test-session", tool_input=dict(team_name="omni-ecom-test", subagent_type=role, prompt=f"读取任务卡：{card}。"))

    def test_duplicate_and_other_roles(self):
        event = self.event()
        self.assertEqual(reserve(event), "reserved_not_started")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            reserve(event)
        self.assertEqual(reserve(self.event("platform-ops")), "reserved_not_started")

    def test_parallel_exactly_one(self):
        event = self.event()
        def call(_):
            try:
                return reserve(event)
            except ValueError:
                return "blocked"
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(call, range(16)))
        self.assertEqual(results.count("reserved_not_started"), 1)

    def test_retry_cannot_bypass(self):
        with self.assertRaisesRegex(ValueError, "terminal_failure"):
            reserve(self.event(attempt="a2"))

    def test_unrelated_untouched(self):
        self.assertEqual(reserve(dict(tool_name="Agent", tool_input=dict(prompt="unrelated task"))), "unrelated")

    def test_role_mismatch(self):
        event = self.event()
        event["tool_input"]["subagent_type"] = "platform-ops"
        with self.assertRaisesRegex(ValueError, "role_mismatch"):
            reserve(event)

    def test_missing_card_blocks(self):
        with self.assertRaisesRegex(ValueError, "one_existing_task_card"):
            reserve(dict(tool_name="Agent", tool_input=dict(team_name="omni-ecom-test")))

    def test_reservation_not_host_evidence(self):
        reserve(self.event())
        journal = Journal(self.root / "run-journal.sqlite", read_only=True)
        try:
            self.assertEqual(journal.events("test", "test-client"), [])
        finally:
            journal.close()


if __name__ == "__main__":
    unittest.main()
