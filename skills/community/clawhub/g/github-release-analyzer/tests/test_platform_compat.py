from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import state_store  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]


class SkillCompatibilityTests(unittest.TestCase):
    def test_skill_uses_skill_root_relative_paths_without_shell_variables(self) -> None:
        skill_md = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("python3 scripts/run.py prepare", skill_md)
        self.assertIn("python3 scripts/run.py render", skill_md)
        self.assertIn("python3 scripts/run.py commit", skill_md)
        self.assertIn("set the command working directory to", skill_md)
        self.assertIn("Do not run\nthese commands from the OpenClaw workspace root", skill_md)
        self.assertNotIn("$SKILL_DIR", skill_md)
        self.assertNotIn("python3 skills/github-release-analyzer/scripts/run.py", skill_md)

    def test_relative_script_command_runs_from_skill_root(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/run.py", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("{prepare,render,commit}", result.stdout)

    def test_skill_keeps_openclaw_metadata_and_adds_hermes_metadata(self) -> None:
        skill_md = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("openclaw:", skill_md)
        self.assertIn("hermes:", skill_md)
        self.assertIn("github", skill_md)
        self.assertIn("releases", skill_md)


class StateRootCompatibilityTests(unittest.TestCase):
    def test_explicit_state_root_overrides_hermes_home(self) -> None:
        with tempfile.TemporaryDirectory() as explicit_root:
            with tempfile.TemporaryDirectory() as hermes_home:
                with patch.dict(
                    os.environ,
                    {
                        "GITHUB_RELEASE_ANALYZER_STATE_ROOT": explicit_root,
                        "HERMES_HOME": hermes_home,
                    },
                    clear=True,
                ):
                    self.assertEqual(
                        state_store._resolve_state_root(),
                        Path(explicit_root),
                    )

    def test_hermes_home_uses_profile_scoped_state_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.dict(
                os.environ,
                {"HERMES_HOME": temp_dir},
                clear=True,
            ):
                self.assertEqual(
                    state_store._resolve_state_root(),
                    Path(temp_dir) / "state" / "github-release-analyzer",
                )

    def test_openclaw_persistent_path_is_unchanged_without_hermes_home(self) -> None:
        with tempfile.TemporaryDirectory() as temp_home:
            with patch.dict(os.environ, {}, clear=True):
                with patch.object(Path, "home", return_value=Path(temp_home)):
                    self.assertEqual(
                        state_store._resolve_state_root(),
                        Path(temp_home)
                        / ".openclaw"
                        / "state"
                        / "github-release-analyzer",
                    )

    def test_existing_openclaw_legacy_state_is_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as temp_home:
            legacy = (
                Path(temp_home)
                / ".openclaw"
                / "workspace"
                / "state"
                / "github-release-analyzer"
            )
            legacy.mkdir(parents=True)
            (legacy / "owner__repo.json").write_text("{}", encoding="utf-8")

            with patch.dict(os.environ, {}, clear=True):
                with patch.object(Path, "home", return_value=Path(temp_home)):
                    self.assertEqual(state_store._resolve_state_root(), legacy)


if __name__ == "__main__":
    unittest.main()
