from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parent.parent


class SavedProfilesTests(unittest.TestCase):
    def test_save_list_and_load_saved_profile_via_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env = {"PYTHONPATH": "src"}

            save_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "intelligence_desk_brief",
                    "save-profile",
                    "--fixture",
                    "--local-state-dir",
                    temp_dir,
                    "--profile-name",
                    "semis-core",
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            saved_profile = json.loads(save_result.stdout)
            self.assertEqual(saved_profile["profile_id"], "semis-core")
            self.assertEqual(saved_profile["workspace_id"], "demo-workspace")

            list_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "intelligence_desk_brief",
                    "list-profiles",
                    "--workspace-id",
                    "demo-workspace",
                    "--local-state-dir",
                    temp_dir,
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            listed_profiles = json.loads(list_result.stdout)
            self.assertEqual(len(listed_profiles), 1)
            self.assertEqual(listed_profiles[0]["profile_name"], "semis-core")

            create_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "intelligence_desk_brief",
                    "create-brief",
                    "--saved-profile",
                    "semis-core",
                    "--workspace-id",
                    "demo-workspace",
                    "--local-state-dir",
                    temp_dir,
                    "--as-of-date",
                    "2026-03-25",
                    "--output-format",
                    "json",
                ],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            payload = json.loads(create_result.stdout)
            self.assertEqual(payload["profile_id"], "semis-core")
            self.assertEqual(payload["profile_name"], "semis-core")
            self.assertEqual(payload["brief_id"], "portfolio-risk-desk-semis-core-2026-03-25")


if __name__ == "__main__":
    unittest.main()
