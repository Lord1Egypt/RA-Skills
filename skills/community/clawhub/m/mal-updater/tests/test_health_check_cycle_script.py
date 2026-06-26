from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from mal_updater.config import ensure_directories, load_config
from mal_updater.db import bootstrap_database, connect


class HealthCheckCycleScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]
        self.script_path = self.repo_root / "scripts" / "run_health_check_cycle.sh"

    def _prepare_temp_repo(self, temp_root: Path) -> Path:
        repo_root = temp_root / "repo"
        repo_root.mkdir()
        shutil.copytree(self.repo_root / "src", repo_root / "src")
        shutil.copytree(self.repo_root / "scripts", repo_root / "scripts")
        shutil.copytree(self.repo_root / "ops", repo_root / "ops")
        return repo_root

    def _write_fake_systemctl(self, bin_dir: Path) -> Path:
        systemctl_path = bin_dir / "systemctl"
        systemctl_path.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "if [[ \"${1:-}\" == \"--user\" ]]; then\n"
            "  shift\n"
            "fi\n"
            "cmd=\"${1:-}\"\n"
            "shift || true\n"
            "case \"$cmd\" in\n"
            "  daemon-reload)\n"
            "    exit 0\n"
            "    ;;\n"
            "  enable|restart|status|is-enabled|is-active|show)\n"
            "    exit 0\n"
            "    ;;\n"
            "  *)\n"
            "    echo \"unsupported fake systemctl command: $cmd\" >&2\n"
            "    exit 1\n"
            "    ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        systemctl_path.chmod(systemctl_path.stat().st_mode | stat.S_IXUSR)
        return systemctl_path

    def test_auto_remediation_can_run_direct_install_script_commands(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            repo_root = self._prepare_temp_repo(temp_root)
            config = load_config(repo_root)
            ensure_directories(config)
            bootstrap_database(config.db_path)

            (config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (config.secrets_dir / "crunchyroll_password.txt").write_text("secret\n", encoding="utf-8")
            (config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            (config.secrets_dir / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
            (config.secrets_dir / "mal_refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")
            crunchyroll_state = config.state_dir / "crunchyroll" / "default"
            crunchyroll_state.mkdir(parents=True, exist_ok=True)
            (crunchyroll_state / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
            (crunchyroll_state / "device_id.txt").write_text("device-id\n", encoding="utf-8")
            (crunchyroll_state / "sync_boundary.json").write_text("{}\n", encoding="utf-8")

            with connect(config.db_path) as conn:
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", "series-1", "Example Show", "Example Show", 1, "{}"),
                )
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", "series-1", 1001, 0.99, "auto_exact", 1, None),
                )
                conn.execute(
                    "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                    ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 1}, sort_keys=True)),
                )
                conn.commit()

            bin_dir = temp_root / "bin"
            bin_dir.mkdir()
            self._write_fake_systemctl(bin_dir)
            xdg_config_home = temp_root / "xdg-config"

            result = subprocess.run(
                [str(repo_root / "scripts" / "run_health_check_cycle.sh")],
                cwd=repo_root,
                text=True,
                capture_output=True,
                check=False,
                env={
                    **os.environ,
                    "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", ""),
                    "XDG_CONFIG_HOME": str(xdg_config_home),
                    "MAL_UPDATER_HEALTH_AUTO_RUN_RECOMMENDED": "1",
                    "MAL_UPDATER_HEALTH_AUTO_RUN_REASON_CODES": "install_user_systemd_service",
                },
            )

            self.assertEqual(0, result.returncode, msg=result.stderr)
            self.assertIn("auto_remediation_reason_code=install_user_systemd_service", result.stdout)
            self.assertIn("auto_remediation_command=", result.stdout)
            self.assertNotIn("auto_remediation_action=skipped_not_allowlisted", result.stdout)


if __name__ == "__main__":
    unittest.main()
