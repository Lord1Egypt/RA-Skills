"""Tests for scripts/build_runtime_prompt.py."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from build_runtime_prompt import agent_entries, build, list_agents  # noqa: E402


class BuildRuntimePromptTests(unittest.TestCase):
    def test_list_agents_includes_required_agents(self):
        listing = list_agents(ROOT_DIR)
        for agent_id in ["generic", "codex", "claude", "openclaw", "hermes", "workbuddy", "qoder-work", "trae"]:
            self.assertIn(agent_id, listing)

    def test_build_generic_prompt_includes_contract_and_adapter(self):
        prompt = build(ROOT_DIR, agent="generic")
        self.assertIn("# Oh My Teacher - Bundled Runtime Prompt", prompt)
        self.assertIn("Agent: generic", prompt)
        self.assertIn("agents/generic.yaml", prompt)
        self.assertIn("agent-adapter-contract.md", prompt)
        self.assertIn("agent-optimization.md", prompt)
        self.assertIn("agent-inventory.md", prompt)
        self.assertIn("staged-review-workflow.md", prompt)
        self.assertIn("focus-feedback-iteration.md", prompt)
        self.assertIn("opt-in-reminders.md", prompt)
        self.assertIn("Optimization profiles: prompt-agent", prompt)
        self.assertIn("SKILL.md", prompt)

    def test_build_all_registered_agents(self):
        for agent_id, entry in agent_entries(ROOT_DIR).items():
            with self.subTest(agent_id=agent_id):
                prompt = build(ROOT_DIR, agent=agent_id)
                self.assertIn(f"Agent: {agent_id}", prompt)
                self.assertIn(entry["adapter_path"], prompt)
                self.assertIn("Follow SKILL.md", prompt)
                self.assertIn("agent-adapter-contract.md", prompt)
                self.assertIn("agent-optimization.md", prompt)
                self.assertIn("staged-review-workflow.md", prompt)
                self.assertIn("focus-feedback-iteration.md", prompt)
                self.assertIn("opt-in-reminders.md", prompt)
                self.assertIn("Optimization profiles:", prompt)
                self.assertIn("Best path:", prompt)
                self.assertIn("Quality Gates", prompt)

    def test_cli_unknown_agent_fails(self):
        script = SCRIPT_DIR / "build_runtime_prompt.py"
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, str(script), "--root", str(ROOT_DIR), "--agent", "missing-agent"],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR),
            env=env,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown agent", result.stderr)

    def test_cli_output_file(self):
        script = SCRIPT_DIR / "build_runtime_prompt.py"
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "prompt.md"
            result = subprocess.run(
                [sys.executable, str(script), "--root", str(ROOT_DIR), "--agent", "trae", "--output", str(output)],
                capture_output=True,
                text=True,
                cwd=str(ROOT_DIR),
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            text = output.read_text(encoding="utf-8")
            self.assertIn("Agent: trae", text)
            self.assertIn("agents/trae.yaml", text)


if __name__ == "__main__":
    unittest.main()
