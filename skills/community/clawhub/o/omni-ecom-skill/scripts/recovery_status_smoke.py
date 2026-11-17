import json
import tempfile
import unittest
from pathlib import Path
from workbuddy_recovery_status import inspect


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.run = self.root / "run"; self.run.mkdir()
        self.session = "00000000-0000-0000-0000-000000000001"
        (self.run / "team-bootstrap.json").write_text(json.dumps(dict(team_name="omni-ecom-test", run_id="run-test")), encoding="utf-8")
        team = self.root / ".codebuddy/teams/omni-ecom-test"; team.mkdir(parents=True)
        (team / "config.json").write_text(json.dumps(dict(name="omni-ecom-test", leadSessionId=self.session)), encoding="utf-8")
        folder = self.root / ".codebuddy/projects/test"; folder.mkdir(parents=True)
        self.trace = folder / (self.session + ".jsonl")

    def write_events(self, events):
        self.trace.write_text("\n".join(json.dumps(x) for x in events), encoding="utf-8")

    def call(self, call_id, success):
        return [dict(type="function_call", name="Agent", callId=call_id, arguments=json.dumps(dict(team_name="omni-ecom-test", subagent_type="data-analyst"))), dict(type="function_call_result", name="Agent", callId=call_id, output=dict(text=(f"Spawned successfully. task_id: agent-{call_id}" if success else "dispatch_duplicate_blocked")))]

    def test_native_id_preserved_without_claiming_completion(self):
        self.write_events(self.call("one", True) + self.call("blocked", False))
        result = inspect(self.run, self.root)
        self.assertEqual(result["members"]["data-analyst"]["native_task_ids"], ["agent-one"])
        self.assertFalse(result["members"]["data-analyst"]["valid_return_file"])
        self.assertEqual(result["duplicate_native_launches"], {})
        self.assertFalse((self.run / "run-journal.sqlite").exists())

    def test_duplicate_actual_spawns_exposed(self):
        self.write_events(self.call("one", True) + self.call("two", True))
        self.assertEqual(inspect(self.run, self.root)["duplicate_native_launches"]["data-analyst"], ["agent-one", "agent-two"])

    def test_missing_trace_not_fabricated(self):
        with self.assertRaisesRegex(ValueError, "trace_missing"):
            inspect(self.run, self.root)


if __name__ == "__main__": unittest.main()
