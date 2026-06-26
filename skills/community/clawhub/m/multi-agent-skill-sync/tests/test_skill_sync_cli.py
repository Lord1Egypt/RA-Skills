from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "skill_sync.py"


def write_skill(root: Path, name: str, payload: str) -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: fixture\n---\n\n# {name}\n",
        encoding="utf-8",
    )
    (skill_dir / "payload.txt").write_text(payload, encoding="utf-8")
    return skill_dir


class SkillSyncCliTests(unittest.TestCase):
    def run_cli(self, machine_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(machine_root),
                "SKILL_SYNC_AGENTS_ROOT": str(machine_root / "agents"),
                "SKILL_SYNC_CODEX_ROOT": str(machine_root / "codex"),
                "SKILL_SYNC_CLAUDE_ROOT": str(machine_root / "claude"),
                "SKILL_SYNC_OPENCODE_ROOT": str(machine_root / "opencode"),
                "SKILL_SYNC_OPENCLAW_ROOT": str(machine_root / "openclaw"),
                "SKILL_SYNC_BACKUP_ROOT": str(machine_root / "backups"),
            }
        )
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            cwd=str(REPO_ROOT),
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_export_import_apply_restore_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            machine_a = temp_root / "machine-a"
            machine_b = temp_root / "machine-b"
            manifest_path = temp_root / "agent-layout.json"

            for machine_root in (machine_a, machine_b):
                for root_name in ("agents", "codex", "backups"):
                    (machine_root / root_name).mkdir(parents=True, exist_ok=True)

            write_skill(machine_a / "agents", "demo-skill", "canonical\n")
            write_skill(machine_a / "codex", "demo-skill", "canonical\n")

            export_result = self.run_cli(
                machine_a,
                "--adopt-root",
                "agents",
                "--export-manifest",
                str(manifest_path),
                "--format",
                "json",
            )
            exported = json.loads(export_result.stdout)
            self.assertEqual(exported["kind"], "skill-sync-layout")
            self.assertEqual(exported["summary"]["importable_skills"], 1)
            self.assertEqual(exported["skills"][0]["canonical"]["platform"], "agents")
            self.assertEqual(
                exported["skills"][0]["desired_platforms"],
                ["agents", "codex"],
            )

            write_skill(machine_b / "agents", "demo-skill", "canonical\n")
            write_skill(machine_b / "codex", "demo-skill", "legacy-copy\n")

            preview_result = self.run_cli(
                machine_b,
                "--import-manifest",
                str(manifest_path),
                "--format",
                "json",
            )
            preview = json.loads(preview_result.stdout)
            self.assertEqual(len(preview["operations"]), 1)
            self.assertEqual(preview["operations"][0]["action"], "replace_with_symlink")

            apply_result = self.run_cli(
                machine_b,
                "--import-manifest",
                str(manifest_path),
                "--apply",
                "--format",
                "json",
            )
            applied = json.loads(apply_result.stdout)
            run_id = applied["run"]["run_id"]
            codex_skill = machine_b / "codex" / "demo-skill"
            self.assertTrue(codex_skill.is_symlink())
            self.assertEqual(
                codex_skill.resolve(),
                (machine_b / "agents" / "demo-skill").resolve(),
            )
            self.assertTrue((machine_b / "backups" / run_id / "manifest.json").is_file())
            self.assertTrue((machine_b / "backups" / "latest").is_symlink())

            restore_result = self.run_cli(
                machine_b,
                "--restore",
                "latest",
                "--apply",
                "--format",
                "json",
            )
            restored = json.loads(restore_result.stdout)
            self.assertEqual(restored["run_id"], run_id)
            self.assertFalse(codex_skill.is_symlink())
            self.assertEqual((codex_skill / "payload.txt").read_text(encoding="utf-8"), "legacy-copy\n")


if __name__ == "__main__":
    unittest.main()
