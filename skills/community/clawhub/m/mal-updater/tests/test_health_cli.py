from __future__ import annotations

import io
import json
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.cli import main as cli_main
from mal_updater.config import ensure_directories, load_config
from mal_updater.db import bootstrap_database, connect, replace_review_queue_entries


class HealthCheckCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True)
        self.config = load_config(self.project_root)
        ensure_directories(self.config)
        bootstrap_database(self.config.db_path)

    def _run_health_check_raw(self, *args: str) -> tuple[int, str]:
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "health-check",
            *args,
        ]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=io.StringIO) as stdout,
            patch.dict("os.environ", {"XDG_CONFIG_HOME": str(self.project_root / ".config")}, clear=False),
        ):
            exit_code = cli_main()
        return exit_code, stdout.getvalue()

    def _run_health_check(self, *args: str) -> tuple[int, dict[str, object]]:
        exit_code, stdout = self._run_health_check_raw(*args)
        return exit_code, json.loads(stdout)

    def _provision_repo_owned_automation_assets(self) -> None:
        source_dir = self.project_root / "ops" / "systemd-user"
        source_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / "mal-updater.service").write_text(
            "[Unit]\nDescription=mal-updater.service\n\n[Service]\nExecStart=python3 -m mal_updater.cli service-run\n",
            encoding="utf-8",
        )
        scripts_dir = self.project_root / "scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        install_script = scripts_dir / "install_user_systemd_units.sh"
        install_script.write_text("#!/usr/bin/env bash\n", encoding="utf-8")
        install_script.chmod(0o755)

    def _install_repo_owned_automation_assets(self) -> Path:
        self._provision_repo_owned_automation_assets()
        target_dir = self.project_root / ".config" / "systemd" / "user"
        target_dir.mkdir(parents=True, exist_ok=True)
        source_path = self.project_root / "ops" / "systemd-user" / "mal-updater.service"
        (target_dir / source_path.name).write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
        return target_dir

    def test_health_check_flags_missing_auth_and_missing_completed_snapshot(self) -> None:
        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("missing_crunchyroll_credentials", warning_codes)
        self.assertIn("missing_crunchyroll_state", warning_codes)
        self.assertIn("missing_mal_auth_material", warning_codes)
        self.assertIn("no_completed_ingest_snapshot", warning_codes)
        self.assertIsNone(payload["latest_sync_run"])
        self.assertEqual(0, payload["mappings"]["total"])
        self.assertEqual(0, payload["mappings"]["approved"])
        self.assertEqual({}, payload["mappings"]["by_source"])
        self.assertEqual(
            {
                "provider_series_count": 0,
                "approved_mapping_count": 0,
                "unmapped_series_count": 0,
                "total_mapping_count": 0,
                "approved_coverage_ratio": None,
            },
            payload["mappings"]["coverage"],
        )
        self.assertEqual(0.8, payload["mappings"]["coverage_threshold"])
        self.assertEqual([], payload["maintenance"]["recommended_commands"])
        self.assertIsNone(payload["maintenance"]["recommended_command"])
        self.assertIsNone(payload["maintenance"]["recommended_automation_command"])
        self.assertIsNone(payload["review_queue"]["recommended_next"])
        self.assertEqual([], payload["review_queue"]["recommended_worklist"])
        self.assertIsNone(payload["review_queue"]["recommended_apply_worklist"])

    def test_health_check_recommends_crunchyroll_reauth_after_repeated_auth_failures(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "tasks": {
                        "sync_fetch_crunchyroll": {
                            "last_status": "error",
                            "last_error": "HTTP 401 from Crunchyroll",
                            "failure_backoff_reason": "HTTP 401 from Crunchyroll",
                            "failure_backoff_consecutive_failures": 3,
                            "failure_backoff_until": "2026-03-23T09:55:00Z",
                            "failure_backoff_remaining_seconds": 900,
                        }
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("crunchyroll_auth_failures_repeated", warning_codes)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("rebootstrap_crunchyroll_auth_after_failures", maintenance_commands[0]["reason_code"])
        self.assertEqual(["crunchyroll-auth-login"], maintenance_commands[0]["command_args"])
        self.assertFalse(maintenance_commands[0]["automation_safe"])
        self.assertFalse(maintenance_commands[0]["requires_auth_interaction"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual("refresh_ingested_snapshot", payload["maintenance"]["recommended_automation_command"]["reason_code"])

    def test_health_check_recommends_reauth_for_login_failure_without_http_401_marker(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "tasks": {
                        "sync_fetch_crunchyroll": {
                            "last_status": "error",
                            "last_error": "Crunchyroll refresh-token login failed: invalid_grant - refresh token revoked",
                            "failure_backoff_reason": "Crunchyroll refresh-token login failed: invalid_grant - refresh token revoked",
                            "failure_backoff_consecutive_failures": 3,
                        }
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        repeated = next(warning for warning in payload["warnings"] if warning["code"] == "crunchyroll_auth_failures_repeated")
        self.assertEqual("crunchyroll", repeated["provider"])
        self.assertIn("invalid_grant", repeated["reason"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("rebootstrap_crunchyroll_auth_after_failures", maintenance_commands[0]["reason_code"])

    def test_health_check_recommends_reauth_for_missing_refresh_token_residue(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "tasks": {
                        "sync_fetch_crunchyroll": {
                            "last_status": "error",
                            "last_error": "Missing Crunchyroll refresh token at /tmp/cr-token",
                            "failure_backoff_reason": "Missing Crunchyroll refresh token at /tmp/cr-token",
                            "failure_backoff_consecutive_failures": 2,
                        }
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        repeated = next(warning for warning in payload["warnings"] if warning["code"] == "crunchyroll_auth_failures_repeated")
        self.assertIn("Missing Crunchyroll refresh token", repeated["reason"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(["crunchyroll-auth-login"], maintenance_commands[0]["command_args"])

    def test_health_check_uses_provider_session_auth_phase_as_fallback_signal(self) -> None:
        (self.config.secrets_dir / "hidive_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "hidive_password.txt").write_text("super-secret\n", encoding="utf-8")
        hidive_state_root = self.config.state_dir / "hidive" / "default"
        hidive_state_root.mkdir(parents=True, exist_ok=True)
        (hidive_state_root / "authorisation_token.txt").write_text("auth-token\n", encoding="utf-8")
        (hidive_state_root / "refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")
        (hidive_state_root / "session.json").write_text(
            json.dumps(
                {
                    "hidive_phase": "auth_failed",
                    "last_error": "HIDIVE login did not return authorisationToken",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "tasks": {
                        "sync_fetch_hidive": {
                            "last_status": "error",
                            "last_error": "provider snapshot failed after token churn",
                            "failure_backoff_reason": "provider snapshot failed after token churn",
                            "failure_backoff_consecutive_failures": 2,
                        }
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        repeated = next(warning for warning in payload["warnings"] if warning["code"] == "hidive_auth_failures_repeated")
        self.assertEqual("auth_failed", repeated["session_phase"])
        self.assertIn("authorisationToken", repeated["session_last_error"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("rebootstrap_hidive_auth_after_failures", maintenance_commands[0]["reason_code"])
        self.assertEqual(["provider-auth-login", "--provider", "hidive"], maintenance_commands[0]["command_args"])

    def test_health_check_ignores_non_auth_provider_failures(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "tasks": {
                        "sync_fetch_crunchyroll": {
                            "last_status": "error",
                            "last_error": "HTTP 500 from Crunchyroll",
                            "failure_backoff_reason": "HTTP 500 from Crunchyroll",
                            "failure_backoff_consecutive_failures": 3,
                        }
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertNotIn("crunchyroll_auth_failures_repeated", warning_codes)
        maintenance_reason_codes = [command["reason_code"] for command in payload["maintenance"]["recommended_commands"]]
        self.assertNotIn("rebootstrap_crunchyroll_auth_after_failures", maintenance_reason_codes)

    def test_health_check_warns_when_repo_owned_automation_units_are_not_installed(self) -> None:
        self._provision_repo_owned_automation_assets()

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("automation_units_missing", warning_codes)
        automation = payload["automation"]
        self.assertFalse(automation["all_units_installed"])
        self.assertEqual(["mal-updater.service"], automation["missing_units"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("install_user_systemd_service", maintenance_commands[0]["reason_code"])
        self.assertEqual([str(self.project_root / "scripts" / "install_user_systemd_units.sh")], maintenance_commands[0]["command_args"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])

    def test_health_check_warns_when_installed_repo_owned_automation_units_are_outdated(self) -> None:
        target_dir = self._install_repo_owned_automation_assets()
        (target_dir / "mal-updater.service").write_text("[Unit]\nDescription=stale\n", encoding="utf-8")

        exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("automation_units_outdated", warning_codes)
        automation = payload["automation"]
        self.assertTrue(automation["all_units_installed"])
        self.assertFalse(automation["all_units_current"])
        self.assertEqual(["mal-updater.service"], automation["outdated_units"])
        self.assertEqual([], automation["missing_units"])
        self.assertFalse(automation["unit"]["content_matches_repo"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("install_user_systemd_service", maintenance_commands[0]["reason_code"])

    def test_health_check_warns_when_repo_owned_service_is_installed_but_not_enabled(self) -> None:
        self._install_repo_owned_automation_assets()

        def fake_systemctl_run(command: list[str], **kwargs):
            return unittest.mock.Mock(returncode=0, stdout="ActiveState=active\nSubState=running\nUnitFileState=disabled\nResult=success\n", stderr="")

        with patch("mal_updater.cli.subprocess.run", side_effect=fake_systemctl_run):
            exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("automation_service_disabled", warning_codes)
        automation = payload["automation"]
        self.assertEqual(["mal-updater.service"], automation["disabled_services"])
        self.assertFalse(automation["service_enabled"])

    def test_health_check_warns_when_enabled_service_is_not_active_in_runtime(self) -> None:
        self._install_repo_owned_automation_assets()

        def fake_systemctl_run(command: list[str], **kwargs):
            return unittest.mock.Mock(returncode=0, stdout="ActiveState=inactive\nSubState=dead\nUnitFileState=enabled\nResult=success\n", stderr="")

        with patch("mal_updater.cli.subprocess.run", side_effect=fake_systemctl_run):
            exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("automation_service_inactive", warning_codes)
        automation = payload["automation"]
        self.assertEqual(["mal-updater.service"], automation["inactive_services"])
        self.assertFalse(automation["service_active"])

    def test_health_check_parses_systemctl_show_key_value_output_without_assuming_field_order(self) -> None:
        self._install_repo_owned_automation_assets()

        def fake_systemctl_run(command: list[str], **kwargs):
            return unittest.mock.Mock(returncode=0, stdout="Result=success\nUnitFileState=enabled\nSubState=running\nActiveState=active\n", stderr="")

        with patch("mal_updater.cli.subprocess.run", side_effect=fake_systemctl_run):
            exit_code, payload = self._run_health_check()

        self.assertEqual(0, exit_code)
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertNotIn("automation_service_inactive", warning_codes)
        automation = payload["automation"]
        self.assertTrue(automation["runtime_state_available"])
        self.assertEqual([], automation["inactive_services"])
        service_runtime = automation["unit"]["runtime_state"]
        self.assertEqual("active", service_runtime["active_state"])
        self.assertEqual("running", service_runtime["sub_state"])
        self.assertEqual("enabled", service_runtime["unit_file_state"])

    def test_health_check_reports_recent_completed_snapshot_and_counts(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        (crunchyroll_state_root / "sync_boundary.json").write_text("{}\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            conn.execute(
                "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                ("crunchyroll", "series-1", "Example Show", "Example Show Season 1", 1, "{}"),
            )
            conn.execute(
                "INSERT INTO provider_episode_progress(provider, provider_episode_id, provider_series_id, episode_number, episode_title, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                ("crunchyroll", "episode-1", "series-1", 1, "Episode 1", "{}"),
            )
            conn.execute(
                "INSERT INTO provider_watchlist(provider, provider_series_id, raw_json) VALUES (?, ?, ?)",
                ("crunchyroll", "series-1", "{}"),
            )
            conn.execute(
                "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("crunchyroll", "series-1", 1001, 1.0, "user_exact", 1, "exact approval"),
            )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 1, "progress_count": 1, "watchlist_count": 1}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "72")

        self.assertEqual(0, exit_code)
        self.assertTrue(payload["healthy"])
        self.assertEqual([], payload["warnings"])
        self.assertEqual(1, payload["provider_counts"]["series"])
        self.assertEqual(1, payload["provider_counts"]["progress"])
        self.assertEqual(1, payload["provider_counts"]["watchlist"])
        self.assertEqual(1, payload["mappings"]["total"])
        self.assertEqual(1, payload["mappings"]["approved"])
        self.assertEqual(1, payload["mappings"]["by_source"]["user_exact"])
        self.assertEqual(1.0, payload["mappings"]["coverage"]["approved_coverage_ratio"])
        self.assertEqual(0, payload["mappings"]["coverage"]["unmapped_series_count"])
        self.assertEqual([], payload["maintenance"]["recommended_commands"])
        self.assertIsNone(payload["maintenance"]["recommended_command"])
        self.assertIsNone(payload["maintenance"]["recommended_automation_command"])
        self.assertEqual("completed", payload["latest_sync_run"]["status"])
        self.assertEqual("completed", payload["latest_completed_sync_run"]["status"])
        self.assertLess(payload["latest_completed_sync_run_age_seconds"], 300)
        self.assertIsNone(payload["review_queue"]["recommended_next"])
        self.assertEqual([], payload["review_queue"]["recommended_worklist"])
        self.assertIsNone(payload["review_queue"]["recommended_apply_worklist"])

    def test_health_check_flags_failed_latest_run_stale_snapshot_and_open_review_queue(self) -> None:
        with connect(self.config.db_path) as conn:
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, started_at, completed_at, summary_json) VALUES (?, ?, ?, ?, datetime('now', '-10 days'), datetime('now', '-10 days'), ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, started_at, completed_at, summary_json) VALUES (?, ?, ?, ?, datetime('now', '-1 day'), datetime('now', '-1 day'), ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "failed", json.dumps({"error": "watch-history 401"}, sort_keys=True)),
            )
            conn.commit()
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-9",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                }
            ],
        )

        exit_code, payload = self._run_health_check("--stale-hours", "24")

        self.assertEqual(0, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("latest_sync_run_failed", warning_codes)
        self.assertIn("completed_snapshot_stale", warning_codes)
        self.assertIn("open_review_queue", warning_codes)
        self.assertEqual({"mapping_review": 1}, payload["review_queue"]["open"])
        self.assertEqual("failed", payload["latest_sync_run"]["status"])
        self.assertEqual("completed", payload["latest_completed_sync_run"]["status"])
        self.assertEqual([], payload["maintenance"]["recommended_commands"])
        self.assertIsNone(payload["maintenance"]["recommended_command"])
        self.assertIsNone(payload["maintenance"]["recommended_automation_command"])
        self.assertEqual("fix-strategy", payload["review_queue"]["recommended_next"]["bucket_type"])
        self.assertEqual("needs_manual_match | same_franchise_tie", payload["review_queue"]["recommended_next"]["bucket_key"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --fix-strategy \"needs_manual_match | same_franchise_tie\"",
            payload["review_queue"]["recommended_next"]["drilldown_command"],
        )
        self.assertGreaterEqual(len(payload["review_queue"]["recommended_worklist"]), 1)
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli resolve-review-queue --fix-strategy \"needs_manual_match | same_franchise_tie\" --limit 20",
            payload["review_queue"]["recommended_worklist"][0]["resolve_command"],
        )
        self.assertEqual(
            {
                "status_from": "open",
                "status_to": "resolved",
                "bucket_limit": 3,
                "per_bucket_limit": 20,
                "command_args": [
                    "review-queue-apply-worklist",
                    "--limit",
                    "3",
                    "--per-bucket-limit",
                    "20",
                ],
                "command": "PYTHONPATH=src python3 -m mal_updater.cli review-queue-apply-worklist --limit 3 --per-bucket-limit 20",
            },
            payload["review_queue"]["recommended_apply_worklist"],
        )

    def test_health_check_flags_stale_mapping_review_rows_from_older_mapper_revision(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-9",
                    "severity": "warning",
                    "payload": {
                        "title": "Example Show",
                        "decision": "needs_review",
                        "reasons": ["exact_normalized_title"],
                    },
                }
            ],
        )

        exit_code, payload = self._run_health_check("--stale-hours", "24")

        self.assertEqual(0, exit_code)
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("mapping_review_queue_stale_heuristics", warning_codes)
        revision = payload["review_queue"]["mapping_review_revision"]
        self.assertEqual(1, revision["open_count"])
        self.assertEqual(1, revision["stale_open_count"])
        self.assertFalse(revision["all_current"])
        self.assertEqual("series-9", revision["stale_examples"][0]["provider_series_id"])
        self.assertIsNone(revision["stale_examples"][0]["mapper_revision"])

    def test_health_check_recommends_snapshot_refresh_when_auth_exists_but_snapshot_is_stale(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, started_at, completed_at, summary_json) VALUES (?, ?, ?, ?, datetime('now', '-10 days'), datetime('now', '-10 days'), ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "24")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_ingested_snapshot", maintenance_commands[0]["reason_code"])
        self.assertTrue(maintenance_commands[0]["automation_safe"])
        self.assertFalse(maintenance_commands[0]["requires_auth_interaction"])
        self.assertEqual(
            ["crunchyroll-fetch-snapshot", "--out", ".MAL-Updater/cache/live-crunchyroll-snapshot.json", "--ingest"],
            maintenance_commands[0]["command_args"],
        )
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --ingest",
            maintenance_commands[0]["command"],
        )
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])

    def test_health_check_marks_interactive_auth_recommendations_as_not_automation_safe(self) -> None:
        (self.config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")

        exit_code, payload = self._run_health_check("--stale-hours", "72")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("missing_mal_auth_material", maintenance_commands[0]["reason_code"])
        self.assertFalse(maintenance_commands[0]["automation_safe"])
        self.assertTrue(maintenance_commands[0]["requires_auth_interaction"])
        self.assertEqual(["mal-auth-login"], maintenance_commands[0]["command_args"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertIsNone(payload["maintenance"]["recommended_automation_command"])

    def test_health_check_recommends_hidive_snapshot_refresh_when_hidive_is_stale_provider(self) -> None:
        (self.config.secrets_dir / "hidive_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "hidive_password.txt").write_text("super-secret\n", encoding="utf-8")
        hidive_state_root = self.config.state_dir / "hidive" / "default"
        hidive_state_root.mkdir(parents=True, exist_ok=True)
        (hidive_state_root / "authorisation_token.txt").write_text("hidive-token\n", encoding="utf-8")
        (hidive_state_root / "refresh_token.txt").write_text("hidive-refresh\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, started_at, completed_at, summary_json) VALUES (?, ?, ?, ?, datetime('now', '-10 days'), datetime('now', '-10 days'), ?)",
                ("hidive", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "24")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_ingested_snapshot", maintenance_commands[0]["reason_code"])
        self.assertEqual(
            ["provider-fetch-snapshot", "--provider", "hidive", "--out", ".MAL-Updater/cache/live-hidive-snapshot.json", "--ingest"],
            maintenance_commands[0]["command_args"],
        )
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])

    def test_health_check_warns_when_approved_mapping_coverage_is_below_threshold(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "72")

        self.assertEqual(0, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("missing_mal_auth_material", warning_codes)
        self.assertIn("approved_mapping_coverage_below_threshold", warning_codes)
        self.assertEqual(0.6, payload["mappings"]["coverage"]["approved_coverage_ratio"])
        self.assertEqual(2, payload["mappings"]["coverage"]["unmapped_series_count"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_mapping_review_backlog", maintenance_commands[0]["reason_code"])
        self.assertTrue(maintenance_commands[0]["automation_safe"])
        self.assertFalse(maintenance_commands[0]["requires_auth_interaction"])
        self.assertEqual(
            ["review-mappings", "--limit", "25", "--mapping-limit", "5", "--persist-review-queue"],
            maintenance_commands[0]["command_args"],
        )
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])

    def test_health_check_prefers_targeted_mapping_queue_refresh_before_full_backlog_rebuild(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-5",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "reasons": ["exact_normalized_title", "margin=0.019", "top_score=1.000"],
                    },
                }
            ],
        )

        exit_code, payload = self._run_health_check("--stale-hours", "72")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("refresh_mapping_review_queue", maintenance_commands[0]["reason_code"])
        self.assertEqual(
            ["refresh-mapping-review-queue", "--provider-series-id", "series-5"],
            maintenance_commands[0]["command_args"],
        )
        self.assertEqual("refresh_mapping_review_backlog", maintenance_commands[1]["reason_code"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])

    def test_health_check_prefers_mapping_refresh_worklist_when_multiple_open_slices_exist(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 7):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 5):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 6}, sort_keys=True)),
            )
            conn.commit()
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-5",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "title": "Example Show 5",
                        "reasons": ["exact_normalized_title", "margin=0.019", "top_score=1.000"],
                    },
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-6",
                    "severity": "warning",
                    "payload": {
                        "decision": "needs_review",
                        "title": "Different Example 6",
                        "reasons": ["substring_title_match", "margin=0.041", "top_score=0.902"],
                    },
                },
            ],
        )

        exit_code, payload = self._run_health_check("--stale-hours", "72", "--review-worklist-limit", "2")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("refresh_mapping_review_worklist", maintenance_commands[0]["reason_code"])
        self.assertEqual(
            [
                "review-queue-refresh-worklist",
                "--limit",
                "2",
                "--per-bucket-limit",
                "20",
                "--mapping-limit",
                "5",
            ],
            maintenance_commands[0]["command_args"],
        )
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli review-queue-refresh-worklist --limit 2 --per-bucket-limit 20 --mapping-limit 5",
            payload["review_queue"]["recommended_refresh_worklist"]["command"],
        )

    def test_health_check_prioritizes_automation_install_before_mapping_backlog_refresh(self) -> None:
        self._provision_repo_owned_automation_assets()
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "72")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual("install_user_systemd_service", maintenance_commands[0]["reason_code"])
        self.assertEqual("refresh_mapping_review_backlog", maintenance_commands[1]["reason_code"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_command"])
        self.assertEqual(maintenance_commands[0], payload["maintenance"]["recommended_automation_command"])

    def test_health_check_can_override_maintenance_review_limit(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "72", "--maintenance-review-limit", "10")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_mapping_review_backlog", maintenance_commands[0]["reason_code"])
        self.assertEqual(
            ["review-mappings", "--limit", "10", "--mapping-limit", "5", "--persist-review-queue"],
            maintenance_commands[0]["command_args"],
        )

    def test_health_check_uses_full_backlog_rebuild_shape_when_maintenance_review_limit_is_zero(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "72", "--maintenance-review-limit", "0")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_mapping_review_backlog", maintenance_commands[0]["reason_code"])
        self.assertEqual(
            ["review-mappings", "--limit", "0", "--mapping-limit", "5", "--persist-review-queue"],
            maintenance_commands[0]["command_args"],
        )

    def test_health_check_warns_when_latest_sync_only_partially_refreshes_cached_provider_rows(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 5):
                conn.execute(
                    "INSERT INTO provider_episode_progress(provider, provider_episode_id, provider_series_id, episode_number, episode_title, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"episode-{idx}", "series-1", idx, f"Episode {idx}", "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO provider_watchlist(provider, provider_series_id, raw_json) VALUES (?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", "{}"),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                (
                    "crunchyroll",
                    "1.0",
                    "ingest_snapshot",
                    "completed",
                    json.dumps({"series_count": 2, "progress_count": 1, "watchlist_count": 1}, sort_keys=True),
                ),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "72")

        self.assertEqual(0, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("missing_mal_auth_material", warning_codes)
        self.assertIn("latest_sync_run_partial_coverage", warning_codes)
        partial = payload["partial_sync_coverage"]
        self.assertEqual(2, partial["fields"]["series"]["latest_sync_run_count"])
        self.assertEqual(5, partial["fields"]["series"]["provider_total_count"])
        self.assertAlmostEqual(0.4, partial["fields"]["series"]["coverage_ratio"])
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_full_snapshot", maintenance_commands[0]["reason_code"])
        self.assertTrue(maintenance_commands[0]["automation_safe"])
        self.assertFalse(maintenance_commands[0]["requires_auth_interaction"])
        self.assertEqual(
            ["crunchyroll-fetch-snapshot", "--full-refresh", "--out", ".MAL-Updater/cache/live-crunchyroll-snapshot.json", "--ingest"],
            maintenance_commands[0]["command_args"],
        )

    def test_health_check_prefers_full_refresh_over_incremental_refresh_when_partial_coverage_exists(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, started_at, completed_at, summary_json) VALUES (?, ?, ?, ?, datetime('now', '-10 days'), datetime('now', '-10 days'), ?)",
                (
                    "crunchyroll",
                    "1.0",
                    "ingest_snapshot",
                    "completed",
                    json.dumps({"series_count": 2}, sort_keys=True),
                ),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--stale-hours", "24")

        self.assertEqual(0, exit_code)
        maintenance_commands = payload["maintenance"]["recommended_commands"]
        self.assertEqual(1, len(maintenance_commands))
        self.assertEqual("refresh_full_snapshot", maintenance_commands[0]["reason_code"])
        self.assertNotIn("refresh_ingested_snapshot", {command["reason_code"] for command in maintenance_commands})

    def test_health_check_can_focus_recommendations_on_one_issue_type(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-3",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                },
            ],
        )
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="sync_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {"decision": "blocked", "reasons": ["missing_exact_approval"]},
                }
            ],
        )

        exit_code, payload = self._run_health_check("--review-issue-type", "sync_review")

        self.assertEqual(0, exit_code)
        self.assertEqual({"mapping_review": 2, "sync_review": 1}, payload["review_queue"]["open"])
        self.assertEqual("sync_review", payload["review_queue"]["recommendation_issue_type_filter"])
        self.assertEqual("fix-strategy", payload["review_queue"]["recommended_next"]["bucket_type"])
        self.assertEqual("blocked | missing_exact_approval", payload["review_queue"]["recommended_next"]["bucket_key"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --issue-type sync_review --fix-strategy \"blocked | missing_exact_approval\"",
            payload["review_queue"]["recommended_next"]["drilldown_command"],
        )
        self.assertGreaterEqual(len(payload["review_queue"]["recommended_worklist"]), 1)
        for candidate in payload["review_queue"]["recommended_worklist"]:
            self.assertIn("--issue-type sync_review", candidate["drilldown_command"])
            self.assertNotIn("same_franchise_tie", candidate["drilldown_command"])
        self.assertEqual(
            "PYTHONPATH=src python3 -m mal_updater.cli review-queue-apply-worklist --issue-type sync_review --limit 3 --per-bucket-limit 20",
            payload["review_queue"]["recommended_apply_worklist"]["command"],
        )

    def test_health_check_honors_review_worklist_limit(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                },
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-2",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["weak_candidates"]},
                },
            ],
        )

        exit_code, payload = self._run_health_check("--review-worklist-limit", "1")

        self.assertEqual(0, exit_code)
        self.assertEqual(1, payload["review_queue"]["recommendation_worklist_limit"])
        self.assertEqual(1, len(payload["review_queue"]["recommended_worklist"]))

        exit_code_zero, payload_zero = self._run_health_check("--review-worklist-limit", "0")

        self.assertEqual(0, exit_code_zero)
        self.assertEqual([], payload_zero["review_queue"]["recommended_worklist"])

    def test_health_check_summary_format_emits_operator_facing_lines(self) -> None:
        replace_review_queue_entries(
            self.config.db_path,
            issue_type="mapping_review",
            entries=[
                {
                    "provider": "crunchyroll",
                    "provider_series_id": "series-1",
                    "severity": "warning",
                    "payload": {"decision": "needs_manual_match", "reasons": ["same_franchise_tie"]},
                }
            ],
        )

        exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("healthy=False", stdout)
        self.assertIn("warning_count=6", stdout)
        self.assertIn("warnings=missing_crunchyroll_credentials, missing_crunchyroll_state, missing_mal_auth_material, no_completed_ingest_snapshot, mapping_review_queue_stale_heuristics, open_review_queue", stdout)
        self.assertIn("mapping_review_stale_entries=1/1 revision=2026-03-22a", stdout)
        self.assertIn(
            'recommended_next=PYTHONPATH=src python3 -m mal_updater.cli list-review-queue --fix-strategy "needs_manual_match | same_franchise_tie"',
            stdout,
        )
        self.assertIn(
            'recommended_apply_worklist=PYTHONPATH=src python3 -m mal_updater.cli review-queue-apply-worklist --limit 3 --per-bucket-limit 20',
            stdout,
        )
        self.assertIn(
            'recommended_action=PYTHONPATH=src python3 -m mal_updater.cli resolve-review-queue --fix-strategy "needs_manual_match | same_franchise_tie" --limit 20',
            stdout,
        )
        self.assertIn(
            'recommended_resolve=PYTHONPATH=src python3 -m mal_updater.cli resolve-review-queue --fix-strategy "needs_manual_match | same_franchise_tie" --limit 20',
            stdout,
        )

    def test_health_check_summary_format_surfaces_automation_safe_maintenance_command(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, started_at, completed_at, summary_json) VALUES (?, ?, ?, ?, datetime('now', '-10 days'), datetime('now', '-10 days'), ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("maintenance_recommended_command=PYTHONPATH=src python3 -m mal_updater.cli mal-auth-login", stdout)
        self.assertIn(
            "maintenance_recommended_auto_command=PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out .MAL-Updater/cache/live-crunchyroll-snapshot.json --ingest",
            stdout,
        )

    def test_health_check_summary_format_surfaces_automation_drift_hint_when_units_are_outdated(self) -> None:
        target_dir = self._install_repo_owned_automation_assets()
        (target_dir / "mal-updater.service").write_text("[Service]\nExecStart=/tmp/stale\n", encoding="utf-8")

        exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("automation_all_units_installed=True", stdout)
        self.assertIn("automation_all_units_current=False", stdout)
        self.assertIn("automation_outdated_units=mal-updater.service", stdout)
        self.assertIn(
            "automation_install_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )

    def test_health_check_summary_format_surfaces_automation_install_hint_when_units_are_missing(self) -> None:
        self._provision_repo_owned_automation_assets()

        exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("automation_all_units_installed=False", stdout)
        self.assertIn(
            "automation_missing_units=mal-updater.service",
            stdout,
        )
        self.assertIn(
            "automation_install_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )

    def test_health_check_summary_format_surfaces_disabled_timer_hint_when_units_are_not_enabled(self) -> None:
        self._install_repo_owned_automation_assets()

        def fake_systemctl_run(command: list[str], **kwargs):
            return unittest.mock.Mock(returncode=0, stdout="ActiveState=active\nSubState=running\nUnitFileState=disabled\nResult=success\n", stderr="")

        with patch("mal_updater.cli.subprocess.run", side_effect=fake_systemctl_run):
            exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("automation_all_units_installed=True", stdout)
        self.assertIn("automation_all_units_current=True", stdout)
        self.assertIn("automation_service_enabled=False", stdout)
        self.assertIn(
            "automation_disabled_services=mal-updater.service",
            stdout,
        )
        self.assertIn(
            "automation_install_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )

    def test_health_check_summary_format_surfaces_wrong_timer_symlink_as_disabled(self) -> None:
        target_dir = self._install_repo_owned_automation_assets()
        (target_dir / "mal-updater.service").write_text("[Unit]\nDescription=stale\n", encoding="utf-8")

        exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("automation_all_units_installed=True", stdout)
        self.assertIn("automation_all_units_current=False", stdout)
        self.assertIn("automation_service_enabled=True", stdout)
        self.assertIn("automation_outdated_units=mal-updater.service", stdout)
        self.assertIn(
            "automation_install_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )

    def test_health_check_summary_format_surfaces_timer_runtime_when_available(self) -> None:
        self._install_repo_owned_automation_assets()

        def fake_systemctl_run(command: list[str], **kwargs):
            return unittest.mock.Mock(returncode=0, stdout="ActiveState=inactive\nSubState=dead\nUnitFileState=enabled\nResult=success\n", stderr="")

        with patch("mal_updater.cli.subprocess.run", side_effect=fake_systemctl_run):
            exit_code, stdout = self._run_health_check_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("automation_inactive_services=mal-updater.service", stdout)
        self.assertIn("automation_service_runtime=mal-updater.service | active=inactive | sub=dead", stdout)
        self.assertIn(
            "maintenance_recommended_auto_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )

    def test_health_check_summary_prioritizes_automation_install_before_mapping_backlog_refresh(self) -> None:
        self._provision_repo_owned_automation_assets()
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            for idx in range(1, 6):
                conn.execute(
                    "INSERT INTO provider_series(provider, provider_series_id, title, season_title, season_number, raw_json) VALUES (?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", f"Example Show {idx}", f"Example Show {idx}", 1, "{}"),
                )
            for idx in range(1, 4):
                conn.execute(
                    "INSERT INTO mal_series_mapping(provider, provider_series_id, mal_anime_id, confidence, mapping_source, approved_by_user, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("crunchyroll", f"series-{idx}", 1000 + idx, 0.99, "auto_exact", 1, None),
                )
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 5}, sort_keys=True)),
            )
            conn.commit()

        exit_code, stdout = self._run_health_check_raw("--format", "summary", "--stale-hours", "72")

        self.assertEqual(0, exit_code)
        self.assertIn(
            "maintenance_recommended_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )
        self.assertIn(
            "maintenance_recommended_auto_command=" + shlex.quote(str(self.project_root / "scripts" / "install_user_systemd_units.sh")),
            stdout,
        )

    def test_health_check_summary_format_honors_strict_exit_code(self) -> None:
        exit_code, stdout = self._run_health_check_raw("--format", "summary", "--strict")

        self.assertEqual(2, exit_code)
        self.assertIn("healthy=False", stdout)
        self.assertIn("warning_count=4", stdout)

    def test_health_check_strict_returns_non_zero_when_warnings_exist(self) -> None:
        exit_code, payload = self._run_health_check("--strict")

        self.assertEqual(2, exit_code)
        self.assertFalse(payload["healthy"])
        warning_codes = {warning["code"] for warning in payload["warnings"]}
        self.assertIn("missing_crunchyroll_credentials", warning_codes)

    def test_health_check_strict_stays_zero_when_healthy(self) -> None:
        (self.config.secrets_dir / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.config.secrets_dir / "crunchyroll_password.txt").write_text("super-secret\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_access_token.txt").write_text("access-token\n", encoding="utf-8")
        (self.config.secrets_dir / "mal_refresh_token.txt").write_text("refresh-token\n", encoding="utf-8")
        crunchyroll_state_root = self.config.state_dir / "crunchyroll" / "default"
        crunchyroll_state_root.mkdir(parents=True, exist_ok=True)
        (crunchyroll_state_root / "refresh_token.txt").write_text("cr-token\n", encoding="utf-8")
        (crunchyroll_state_root / "device_id.txt").write_text("device-id\n", encoding="utf-8")
        (crunchyroll_state_root / "sync_boundary.json").write_text("{}\n", encoding="utf-8")

        with connect(self.config.db_path) as conn:
            conn.execute(
                "INSERT INTO sync_runs(provider, contract_version, mode, status, completed_at, summary_json) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
                ("crunchyroll", "1.0", "ingest_snapshot", "completed", json.dumps({"series_count": 1}, sort_keys=True)),
            )
            conn.commit()

        exit_code, payload = self._run_health_check("--strict")

        self.assertEqual(0, exit_code)
        self.assertTrue(payload["healthy"])


if __name__ == "__main__":
    unittest.main()
