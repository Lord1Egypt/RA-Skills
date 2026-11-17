"""Tests for strict WorkBuddy/Codex orchestration routing."""
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import validate
from host_orchestration_guard import ROOT, build_plan, main


class HostOrchestrationTests(unittest.TestCase):
    def setUp(self):
        self.args = dict(run_id="run-host-001", client_scope="synthetic", team_version="2.0.3-candidate.1")

    def test_workbuddy_direct_teamcreate_plan(self):
        caps = ["TeamCreate", "TaskCreate", "TaskList", "TaskUpdate", "Agent", "TaskOutput", "SendMessage"]
        plan = build_plan("workbuddy", caps, **self.args)
        self.assertEqual(plan["bootstrap_mode"], "teamcreate_direct")
        self.assertNotIn("spawn_agent", plan["observed_capabilities"])

    def test_workbuddy_deferred_teamcreate_plan(self):
        caps = ["ToolSearch", "DeferExecuteTool", "TaskCreate", "TaskList", "TaskUpdate", "Agent", "TaskOutput"]
        plan = build_plan("workbuddy", caps, **self.args)
        self.assertEqual(plan["bootstrap_mode"], "teamcreate_deferred")

    def test_workbuddy_missing_teamcreate_path_blocks(self):
        caps = ["TaskCreate", "TaskList", "TaskUpdate", "Agent", "TaskOutput"]
        with self.assertRaisesRegex(ValueError, "workbuddy_teamcreate_unavailable"):
            build_plan("workbuddy", caps, **self.args)

    def test_codex_uses_native_subagents_and_schema(self):
        plan = build_plan("codex", ["spawn_agent", "wait_agent", "send_message"], **self.args)
        self.assertEqual(plan["bootstrap_mode"], "codex_native_subagents")
        self.assertNotIn("TeamCreate", plan["observed_capabilities"])
        schema = json.loads((ROOT / "schemas" / "host-orchestration-plan.schema.json").read_text(encoding="utf-8"))
        validate(plan, schema)

    def test_codex_workbuddy_tool_mix_blocks_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "plan.json"
            code = main(["--host", "codex", "--capability", "spawn_agent", "--capability", "wait_agent",
                         "--capability", "TeamCreate", "--run-id", self.args["run_id"],
                         "--client-scope", self.args["client_scope"], "--team-version", self.args["team_version"],
                         "--output", str(output)])
            self.assertEqual(code, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
