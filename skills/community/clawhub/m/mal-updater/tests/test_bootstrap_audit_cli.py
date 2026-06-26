from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.cli import main as cli_main


class BootstrapAuditCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True)

    def _run_bootstrap_audit_raw(self, *args: str) -> tuple[int, str]:
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "bootstrap-audit",
            *args,
        ]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=io.StringIO) as stdout,
            patch.dict("os.environ", {"XDG_CONFIG_HOME": str(self.project_root / ".config")}, clear=False),
        ):
            exit_code = cli_main()
        return exit_code, stdout.getvalue()

    def test_bootstrap_audit_json_exposes_provider_readiness_and_recommended_commands(self) -> None:
        exit_code, stdout = self._run_bootstrap_audit_raw()
        payload = json.loads(stdout)

        self.assertEqual(0, exit_code)
        self.assertIn("providers", payload)
        self.assertIn("summary", payload)
        self.assertIn("recommended_commands", payload)
        self.assertFalse(payload["providers"]["crunchyroll"]["ready"])
        self.assertIn("credentials", payload["providers"]["crunchyroll"]["missing"])
        self.assertIn("session", payload["providers"]["crunchyroll"]["missing"])
        self.assertFalse(payload["providers"]["hidive"]["ready"])
        self.assertEqual(2, payload["summary"]["provider_count"])
        self.assertGreaterEqual(payload["summary"]["actionable_command_count"], 1)
        commands = [item["command"] for item in payload["recommended_commands"] if item.get("command")]
        self.assertIn("PYTHONPATH=src python3 -m mal_updater.cli mal-auth-login", commands)
        self.assertIn(
            "PYTHONPATH=src python3 -m mal_updater.cli provider-auth-login --provider crunchyroll",
            commands,
        )

    def test_bootstrap_audit_summary_reports_provider_missing_state_and_next_commands(self) -> None:
        secrets_dir = self.project_root / ".MAL-Updater" / "secrets"
        secrets_dir.mkdir(parents=True, exist_ok=True)
        (secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (secrets_dir / "crunchyroll_password.txt").write_text("top-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.project_root / ".MAL-Updater" / "state" / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")

        exit_code, stdout = self._run_bootstrap_audit_raw("--summary")

        self.assertEqual(0, exit_code)
        self.assertIn("provider_crunchyroll_ready=False", stdout)
        self.assertIn("provider_crunchyroll_missing=session", stdout)
        self.assertIn(
            "next_command=PYTHONPATH=src python3 -m mal_updater.cli provider-auth-login --provider crunchyroll",
            stdout,
        )
        self.assertIn("blocking_step_count=", stdout)
        self.assertIn("nonblocking_step_count=", stdout)


if __name__ == "__main__":
    unittest.main()
