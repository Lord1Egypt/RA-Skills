from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from mal_updater.cli import main as cli_main
from mal_updater.config import ensure_directories, load_config
from mal_updater.service_manager import doctor_service


class ServiceStatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True)
        self.config = load_config(self.project_root)
        ensure_directories(self.config)

    def _run_service_status_raw(self, *args: str) -> tuple[int, str]:
        argv = [
            "mal-updater",
            "--project-root",
            str(self.project_root),
            "service-status",
            *args,
        ]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=io.StringIO) as stdout,
            patch.dict("os.environ", {"HOME": str(self.project_root / "fake-home")}, clear=False),
        ):
            exit_code = cli_main()
        return exit_code, stdout.getvalue()

    def test_doctor_service_includes_recent_task_state_and_log_tail(self) -> None:
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "last_loop_at": "2026-03-20T21:55:00Z",
                    "api_usage": {
                        "mal": {"request_count": 4},
                        "crunchyroll": {"request_count": 2},
                    },
                    "tasks": {
                        "sync": {
                            "last_run_epoch": 123.0,
                            "last_run_at": "2026-03-20T21:54:00Z",
                            "last_status": "ok",
                            "every_seconds": 21600,
                            "budget_provider": "mal",
                            "budget_scope": "task",
                            "projected_request_source": "configured",
                            "projected_request_count": 4,
                            "projected_request_total": 8,
                            "projected_ratio": 0.2,
                            "last_request_delta": 3,
                            "next_due_at": "2026-03-21T03:54:00Z",
                            "last_result": {
                                "label": "sync",
                                "returncode": 0,
                                "stdout": "sync completed\nwith useful detail",
                                "stderr": "",
                            },
                        },
                        "health": {
                            "last_skipped_at": "2026-03-20T21:53:00Z",
                            "last_skip_reason": "crunchyroll_budget_critical ratio=1.000 cooldown=1800s",
                            "budget_backoff_level": "critical",
                            "budget_backoff_until": "2026-03-20T22:23:00Z",
                            "budget_backoff_remaining_seconds": 1800,
                            "budget_backoff_floor_seconds": 1800,
                            "budget_backoff_cooldown_source": "provider_floor",
                            "every_seconds": 43200,
                            "next_due_at": "2026-03-21T09:53:00Z",
                        },
                        "sync_fetch_crunchyroll": {
                            "last_run_at": "2026-03-20T21:52:00Z",
                            "last_status": "error",
                            "last_error": "HTTP 401 from Crunchyroll",
                            "failure_backoff_until": "2026-03-20T22:02:00Z",
                            "failure_backoff_remaining_seconds": 600,
                            "failure_backoff_reason": "HTTP 401 from Crunchyroll",
                            "failure_backoff_class": "auth",
                            "failure_backoff_floor_seconds": 7200,
                            "failure_backoff_consecutive_failures": 2,
                            "every_seconds": 21600,
                            "budget_provider": "crunchyroll",
                            "budget_scope": "provider",
                            "next_due_at": "2026-03-21T03:52:00Z"
                        },
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        self.config.service_log_path.write_text(
            "\n".join(["line-1", "line-2", "line-3"]),
            encoding="utf-8",
        )
        self.config.health_latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.health_latest_json_path.write_text(
            json.dumps({"healthy": True, "warning_count": 0}),
            encoding="utf-8",
        )

        def fake_run(command: list[str], check: bool = True):
            if command[-2:] == ["is-enabled", "mal-updater.service"]:
                return Mock(returncode=0, stdout="enabled\n", stderr="")
            if command[-2:] == ["is-active", "mal-updater.service"]:
                return Mock(returncode=0, stdout="active\n", stderr="")
            raise AssertionError(f"unexpected command: {command}")

        fake_home = self.project_root / "fake-home"
        with (
            patch("mal_updater.service_manager._run", side_effect=fake_run),
            patch.dict("os.environ", {"HOME": str(fake_home)}, clear=False),
        ):
            payload = doctor_service(self.config)

        self.assertTrue(payload["enabled"])
        self.assertTrue(payload["active"])
        self.assertEqual("2026-03-20T21:55:00Z", payload["last_loop_at"])
        self.assertEqual({"request_count": 4}, payload["api_usage"]["mal"])
        self.assertEqual(["line-1", "line-2", "line-3"], payload["service_log_tail"])
        self.assertEqual({"healthy": True, "warning_count": 0}, payload["health_latest_summary"])
        self.assertIsNone(payload["service_state_parse_error"])
        self.assertIsNone(payload["health_latest_parse_error"])
        sync_summary = payload["task_state"]["sync"]
        self.assertEqual(123.0, sync_summary["last_run_epoch"])
        self.assertEqual("2026-03-20T21:54:00Z", sync_summary["last_run_at"])
        self.assertEqual("ok", sync_summary["last_status"])
        self.assertEqual(21600, sync_summary["every_seconds"])
        self.assertEqual("mal", sync_summary["budget_provider"])
        self.assertEqual("task", sync_summary["budget_scope"])
        self.assertEqual("configured", sync_summary["projected_request_source"])
        self.assertEqual(4, sync_summary["projected_request_count"])
        self.assertEqual(8, sync_summary["projected_request_total"])
        self.assertEqual(0.2, sync_summary["projected_ratio"])
        self.assertEqual(3, sync_summary["last_request_delta"])
        self.assertEqual("2026-03-21T03:54:00Z", sync_summary["next_due_at"])
        self.assertIn("next_due_in_seconds", sync_summary)
        self.assertEqual(
            {
                "label": "sync",
                "returncode": 0,
                "stdout_snippet": "sync completed\nwith useful detail",
            },
            sync_summary["last_result"],
        )
        health_summary = payload["task_state"]["health"]
        self.assertEqual("2026-03-20T21:53:00Z", health_summary["last_skipped_at"])
        self.assertEqual("crunchyroll_budget_critical ratio=1.000 cooldown=1800s", health_summary["last_skip_reason"])
        self.assertEqual("critical", health_summary["budget_backoff_level"])
        self.assertEqual("2026-03-20T22:23:00Z", health_summary["budget_backoff_until"])
        self.assertEqual(1800, health_summary["budget_backoff_floor_seconds"])
        self.assertEqual("provider_floor", health_summary["budget_backoff_cooldown_source"])
        self.assertEqual(43200, health_summary["every_seconds"])
        self.assertEqual("2026-03-21T09:53:00Z", health_summary["next_due_at"])
        self.assertIn("next_due_in_seconds", health_summary)
        self.assertIn("budget_backoff_remaining_seconds", health_summary)
        fetch_summary = payload["task_state"]["sync_fetch_crunchyroll"]
        self.assertEqual("error", fetch_summary["last_status"])
        self.assertEqual("HTTP 401 from Crunchyroll", fetch_summary["last_error"])
        self.assertEqual("2026-03-20T22:02:00Z", fetch_summary["failure_backoff_until"])
        self.assertEqual("HTTP 401 from Crunchyroll", fetch_summary["failure_backoff_reason"])
        self.assertEqual("auth", fetch_summary["failure_backoff_class"])
        self.assertEqual(7200, fetch_summary["failure_backoff_floor_seconds"])
        self.assertEqual(2, fetch_summary["failure_backoff_consecutive_failures"])
        self.assertIn("failure_backoff_remaining_seconds", fetch_summary)

    def test_doctor_service_reports_state_parse_errors_without_crashing(self) -> None:
        self.config.service_state_path.write_text("{not-json", encoding="utf-8")
        self.config.health_latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.health_latest_json_path.write_text("[]", encoding="utf-8")

        def fake_run(command: list[str], check: bool = True):
            return Mock(returncode=1, stdout="", stderr="not-found\n")

        fake_home = self.project_root / "fake-home"
        with (
            patch("mal_updater.service_manager._run", side_effect=fake_run),
            patch.dict("os.environ", {"HOME": str(fake_home)}, clear=False),
        ):
            payload = doctor_service(self.config)

        self.assertFalse(payload["enabled"])
        self.assertFalse(payload["active"])
        self.assertIn("JSONDecodeError", payload["service_state_parse_error"])
        self.assertEqual(f"Expected top-level object in {self.config.health_latest_json_path.name}", payload["health_latest_parse_error"])
        self.assertEqual({}, payload["task_state"])
        self.assertIsNone(payload["last_loop_at"])
        self.assertNotIn("api_usage", payload)

    def test_service_status_summary_format_emits_operator_lines(self) -> None:
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "last_loop_at": "2026-03-20T21:55:00Z",
                    "api_usage": {
                        "mal": {
                            "request_count": 4,
                            "success_count": 3,
                            "error_count": 1,
                            "last_event_at": "2026-03-20T21:54:30Z",
                        },
                        "crunchyroll": {
                            "request_count": 2,
                            "success_count": 2,
                            "error_count": 0,
                        },
                    },
                    "tasks": {
                        "sync": {
                            "last_run_at": "2026-03-20T21:54:00Z",
                            "last_status": "ok",
                            "last_decision_at": "2026-03-20T21:54:02Z",
                            "last_started_at": "2026-03-20T21:54:00Z",
                            "last_finished_at": "2026-03-20T21:54:02Z",
                            "last_duration_seconds": 2.0,
                            "every_seconds": 21600,
                            "budget_provider": "mal",
                            "budget_scope": "task",
                            "projected_request_source": "configured",
                            "projected_request_count": 4,
                            "projected_request_total": 8,
                            "projected_ratio": 0.2,
                            "last_request_delta": 3,
                            "next_due_at": "2026-03-21T03:54:00Z",
                        },
                        "health": {
                            "last_skipped_at": "2026-03-20T21:53:00Z",
                            "last_skip_reason": "budget_guard",
                            "last_decision_at": "2026-03-20T21:53:00Z",
                            "budget_backoff_level": "warn",
                            "budget_backoff_until": "2026-03-20T22:13:00Z",
                            "budget_backoff_remaining_seconds": 1200,
                            "budget_backoff_floor_seconds": 900,
                            "budget_backoff_cooldown_source": "provider_floor",
                            "every_seconds": 43200,
                            "next_due_at": "2026-03-21T09:53:00Z",
                        },
                        "sync_fetch_crunchyroll": {
                            "last_run_at": "2026-03-20T21:52:00Z",
                            "last_status": "error",
                            "last_error": "HTTP 401 from Crunchyroll",
                            "failure_backoff_until": "2026-03-20T22:02:00Z",
                            "failure_backoff_remaining_seconds": 600,
                            "failure_backoff_reason": "HTTP 401 from Crunchyroll",
                            "failure_backoff_class": "auth",
                            "failure_backoff_floor_seconds": 7200,
                            "failure_backoff_consecutive_failures": 2,
                            "every_seconds": 21600,
                            "budget_provider": "crunchyroll",
                            "budget_scope": "provider",
                            "next_due_at": "2026-03-21T03:52:00Z"
                        },
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        self.config.service_log_path.write_text("line-1\nline-2", encoding="utf-8")
        self.config.health_latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.health_latest_json_path.write_text(
            json.dumps(
                {
                    "healthy": False,
                    "warnings": [{"code": "open_review_queue"}],
                    "maintenance": {
                        "recommended_command": {"command": "PYTHONPATH=src python3 -m mal_updater.cli review-queue-next"},
                        "recommended_automation_command": {"command": "PYTHONPATH=src python3 -m mal_updater.cli review-queue-apply-worklist --limit 1"},
                    },
                }
            ),
            encoding="utf-8",
        )

        def fake_run(command: list[str], check: bool = True):
            if command[-2:] == ["is-enabled", "mal-updater.service"]:
                return Mock(returncode=0, stdout="enabled\n", stderr="")
            if command[-2:] == ["is-active", "mal-updater.service"]:
                return Mock(returncode=0, stdout="active\n", stderr="")
            raise AssertionError(f"unexpected command: {command}")

        with patch("mal_updater.service_manager._run", side_effect=fake_run):
            exit_code, stdout = self._run_service_status_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("unit_exists=False", stdout)
        self.assertIn("enabled=True", stdout)
        self.assertIn("active=True", stdout)
        self.assertIn("last_loop_at=2026-03-20T21:55:00Z", stdout)
        self.assertIn("health_healthy=False", stdout)
        self.assertIn("health_warning_count=1", stdout)
        self.assertIn("health_warnings=open_review_queue", stdout)
        self.assertIn("maintenance_recommended_command=PYTHONPATH=src python3 -m mal_updater.cli review-queue-next", stdout)
        self.assertIn("maintenance_recommended_auto_command=PYTHONPATH=src python3 -m mal_updater.cli review-queue-apply-worklist --limit 1", stdout)
        self.assertIn("api_mal_request_count=4", stdout)
        self.assertIn("api_crunchyroll_success_count=2", stdout)
        self.assertIn("task_sync_last_status=ok", stdout)
        self.assertIn("task_sync_every_seconds=21600", stdout)
        self.assertIn("task_sync_budget_provider=mal", stdout)
        self.assertIn("task_sync_budget_scope=task", stdout)
        self.assertIn("task_sync_projected_request_source=configured", stdout)
        self.assertIn("task_sync_projected_request_count=4", stdout)
        self.assertIn("task_sync_projected_request_total=8", stdout)
        self.assertIn("task_sync_projected_ratio=0.2", stdout)
        self.assertIn("task_sync_last_request_delta=3", stdout)
        self.assertIn("task_sync_last_decision_at=2026-03-20T21:54:02Z", stdout)
        self.assertIn("task_sync_last_started_at=2026-03-20T21:54:00Z", stdout)
        self.assertIn("task_sync_last_finished_at=2026-03-20T21:54:02Z", stdout)
        self.assertIn("task_sync_last_duration_seconds=2.0", stdout)
        self.assertIn("task_sync_next_due_at=2026-03-21T03:54:00Z", stdout)
        self.assertIn("task_health_last_skip_reason=budget_guard", stdout)
        self.assertIn("task_health_last_decision_at=2026-03-20T21:53:00Z", stdout)
        self.assertIn("task_health_budget_backoff_level=warn", stdout)
        self.assertIn("task_health_budget_backoff_until=2026-03-20T22:13:00Z", stdout)
        self.assertIn("task_health_budget_backoff_remaining_seconds=", stdout)
        self.assertIn("task_health_budget_backoff_floor_seconds=900", stdout)
        self.assertIn("task_health_budget_backoff_cooldown_source=provider_floor", stdout)
        self.assertIn("task_health_next_due_at=2026-03-21T09:53:00Z", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_last_status=error", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_last_error=HTTP 401 from Crunchyroll", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_failure_backoff_until=2026-03-20T22:02:00Z", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_failure_backoff_remaining_seconds=", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_failure_backoff_reason=HTTP 401 from Crunchyroll", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_failure_backoff_class=auth", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_failure_backoff_floor_seconds=7200", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_failure_backoff_consecutive_failures=2", stdout)
        self.assertIn("task_sync_fetch_crunchyroll_budget_scope=provider", stdout)
        self.assertIn("service_log_last_line=line-2", stdout)

    def test_service_status_summary_surfaces_parse_errors(self) -> None:
        self.config.service_state_path.write_text("{not-json", encoding="utf-8")
        self.config.health_latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.health_latest_json_path.write_text("[]", encoding="utf-8")

        def fake_run(command: list[str], check: bool = True):
            return Mock(returncode=1, stdout="", stderr="not-found\n")

        with patch("mal_updater.service_manager._run", side_effect=fake_run):
            exit_code, stdout = self._run_service_status_raw("--format", "summary")

        self.assertEqual(0, exit_code)
        self.assertIn("enabled=False", stdout)
        self.assertIn("active=False", stdout)
        self.assertIn("service_state_parse_error=JSONDecodeError", stdout)
        self.assertIn(f"health_latest_parse_error=Expected top-level object in {self.config.health_latest_json_path.name}", stdout)
