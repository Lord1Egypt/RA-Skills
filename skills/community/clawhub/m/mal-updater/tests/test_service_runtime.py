from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
import time
from pathlib import Path
from unittest.mock import patch

from mal_updater.config import ensure_directories, load_config
from mal_updater.request_tracking import estimate_budget_recovery_seconds, estimate_budget_recovery_seconds_for_ratio, record_api_request_event
from mal_updater.service_runtime import TaskSpec, _projected_request_count, run_pending_tasks


class ServiceRuntimeFullRefreshCadenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True)
        (self.project_root / ".MAL-Updater" / "secrets").mkdir(parents=True)
        (self.project_root / ".MAL-Updater" / "secrets" / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.project_root / ".MAL-Updater" / "secrets" / "crunchyroll_password.txt").write_text("secret\n", encoding="utf-8")
        self.config = load_config(self.project_root)
        ensure_directories(self.config)
        self.config.service.sync_every_seconds = 0
        self.config.service.health_every_seconds = 3600
        self.config.service.mal_refresh_every_seconds = 3600
        self.config.service.full_refresh_every_seconds = 86400
        now = time.time()
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "started_at": "2026-03-20T20:00:00Z",
                    "tasks": {
                        "mal_refresh": {"last_run_epoch": now, "last_run_at": "2026-03-20T20:00:00Z"},
                        "health": {"last_run_epoch": now, "last_run_at": "2026-03-20T20:00:00Z"},
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def test_run_pending_tasks_seeds_full_refresh_anchor_from_first_incremental_fetch(self) -> None:
        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ) as run_subprocess:
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("incremental", sync_result["fetch_mode"])
        sync_args = run_subprocess.call_args_list[0].args[1]
        self.assertNotIn("--full-refresh", sync_args)

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("incremental", sync_state["last_fetch_mode"])
        self.assertIn("full_refresh_anchor_epoch", sync_state)
        self.assertNotIn("last_successful_full_refresh_epoch", sync_state)

    def test_run_pending_tasks_requests_periodic_provider_full_refresh_when_anchor_is_stale(self) -> None:
        stale_anchor = datetime.now(timezone.utc).timestamp() - 90000
        state = {
            "started_at": "2026-03-20T20:00:00Z",
            "tasks": {
                "mal_refresh": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                "health": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                "sync_fetch_crunchyroll": {
                    "full_refresh_anchor_epoch": stale_anchor,
                    "full_refresh_anchor_at": "2026-03-20T20:00:00Z",
                    "last_run_epoch": 0,
                }
            },
        }
        self.config.service_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ) as run_subprocess:
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("full_refresh", sync_result["fetch_mode"])
        self.assertEqual("periodic_cadence", sync_result["full_refresh_reason"])
        sync_args = run_subprocess.call_args_list[0].args[1]
        self.assertIn("--full-refresh", sync_args)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("full_refresh", sync_state["last_fetch_mode"])
        self.assertEqual("periodic_cadence", sync_state["last_full_refresh_reason"])
        self.assertIn("last_successful_full_refresh_epoch", sync_state)
        self.assertGreater(sync_state["full_refresh_anchor_epoch"], stale_anchor)

    def test_run_pending_tasks_downgrades_budget_blocked_full_refresh_to_incremental_fetch(self) -> None:
        stale_anchor = datetime.now(timezone.utc).timestamp() - 90000
        state = {
            "started_at": "2026-03-20T20:00:00Z",
            "tasks": {
                "mal_refresh": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                "health": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                "sync_fetch_crunchyroll": {
                    "full_refresh_anchor_epoch": stale_anchor,
                    "full_refresh_anchor_at": "2026-03-20T20:00:00Z",
                    "last_run_epoch": 0,
                }
            },
        }
        self.config.service_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        with patch(
            "mal_updater.service_runtime._budget_gate",
            side_effect=[
                (False, "crunchyroll_budget_projected_critical ratio=0.000 projected_ratio=1.000 projected_requests=55 cooldown=1800s", {"provider": "crunchyroll", "projected_request_source": "configured_full_refresh", "projected_request_count": 55}),
                (True, None, {"provider": "crunchyroll", "projected_request_source": "observed_incremental_smoothed", "projected_request_count": 4}),
                (True, None, {"provider": "mal"}),
                (True, None, None),
            ],
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ) as run_subprocess:
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("incremental", sync_result["fetch_mode"])
        self.assertEqual("periodic_cadence", sync_result["deferred_full_refresh_reason"])
        sync_args = run_subprocess.call_args_list[0].args[1]
        self.assertNotIn("--full-refresh", sync_args)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("incremental", sync_state["last_fetch_mode"])
        self.assertEqual(stale_anchor, sync_state["full_refresh_anchor_epoch"])
        self.assertNotIn("last_successful_full_refresh_epoch", sync_state)

    def test_run_pending_tasks_requests_health_recommended_full_refresh(self) -> None:
        self.config.health_latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.health_latest_json_path.write_text(
            json.dumps(
                {
                    "maintenance": {
                        "recommended_commands": [
                            {
                                "reason_code": "refresh_full_snapshot",
                                "command_args": [
                                    "crunchyroll-fetch-snapshot",
                                    "--full-refresh",
                                    "--out",
                                    ".MAL-Updater/cache/live-crunchyroll-snapshot.json",
                                    "--ingest",
                                ],
                            }
                        ]
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ) as run_subprocess:
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("full_refresh", sync_result["fetch_mode"])
        self.assertEqual("health_recommended", sync_result["full_refresh_reason"])
        sync_args = run_subprocess.call_args_list[0].args[1]
        self.assertIn("--full-refresh", sync_args)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("health_recommended", sync_state["last_full_refresh_reason"])

    def test_run_pending_tasks_does_not_repeat_health_recommended_full_refresh_after_newer_success(self) -> None:
        self.config.health_latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.config.health_latest_json_path.write_text(
            json.dumps(
                {
                    "maintenance": {
                        "recommended_commands": [
                            {
                                "reason_code": "refresh_full_snapshot",
                                "command_args": [
                                    "crunchyroll-fetch-snapshot",
                                    "--full-refresh",
                                    "--out",
                                    ".MAL-Updater/cache/live-crunchyroll-snapshot.json",
                                    "--ingest",
                                ],
                            }
                        ]
                    }
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        stale_health_mtime = time.time() - 600
        os.utime(self.config.health_latest_json_path, (stale_health_mtime, stale_health_mtime))
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "started_at": "2026-03-20T20:00:00Z",
                    "tasks": {
                        "mal_refresh": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                        "health": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                        "sync_fetch_crunchyroll": {
                            "last_successful_full_refresh_epoch": time.time(),
                            "full_refresh_anchor_epoch": time.time(),
                            "full_refresh_anchor_at": "2026-03-20T20:00:00Z",
                            "last_run_epoch": 0,
                        },
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ) as run_subprocess:
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("incremental", sync_result["fetch_mode"])
        self.assertNotIn("full_refresh_reason", sync_result)
        sync_args = run_subprocess.call_args_list[0].args[1]
        self.assertNotIn("--full-refresh", sync_args)

    def test_run_pending_tasks_does_not_mark_failed_full_refresh_as_successful(self) -> None:
        stale_anchor = datetime.now(timezone.utc).timestamp() - 90000
        previous_success = stale_anchor - 120
        state = {
            "started_at": "2026-03-20T20:00:00Z",
            "tasks": {
                "mal_refresh": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                "health": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                "sync_fetch_crunchyroll": {
                    "last_fetch_mode": "incremental",
                    "last_fetch_mode_at": "2026-03-20T18:00:00Z",
                    "last_successful_full_refresh_epoch": previous_success,
                    "last_successful_full_refresh_at": "2026-03-20T17:58:00Z",
                    "full_refresh_anchor_epoch": stale_anchor,
                    "full_refresh_anchor_at": "2026-03-20T18:00:00Z",
                    "last_run_epoch": 0,
                },
            },
        }
        self.config.service_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "error", "label": "sync_fetch_crunchyroll", "returncode": 1, "stdout": "", "stderr": "HTTP 401 from Crunchyroll\n"},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ) as run_subprocess:
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("error", sync_result["status"])
        sync_args = run_subprocess.call_args_list[0].args[1]
        self.assertIn("--full-refresh", sync_args)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("incremental", sync_state["last_fetch_mode"])
        self.assertEqual(previous_success, sync_state["last_successful_full_refresh_epoch"])
        self.assertEqual(stale_anchor, sync_state["full_refresh_anchor_epoch"])
        self.assertEqual("auth", sync_state["failure_backoff_class"])


class ServiceRuntimeBudgetBackoffTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.project_root = Path(self.temp_dir.name)
        (self.project_root / ".MAL-Updater" / "config").mkdir(parents=True)
        (self.project_root / ".MAL-Updater" / "secrets").mkdir(parents=True)
        (self.project_root / ".MAL-Updater" / "secrets" / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.project_root / ".MAL-Updater" / "secrets" / "crunchyroll_password.txt").write_text("secret\n", encoding="utf-8")
        self.config = load_config(self.project_root)
        ensure_directories(self.config)

    def _write_request_events(self, provider: str, offsets_seconds: list[int]) -> None:
        now = datetime.now(timezone.utc).replace(microsecond=0)
        events: list[str] = []
        for offset in offsets_seconds:
            at = (now - timedelta(seconds=offset)).isoformat().replace("+00:00", "Z")
            events.append(
                json.dumps(
                    {
                        "at": at,
                        "provider": provider,
                        "operation": "test-op",
                        "url": "https://example.invalid/api",
                        "method": "GET",
                        "outcome": "ok",
                        "status_code": 200,
                        "error": None,
                    },
                    sort_keys=True,
                )
            )
        self.config.api_request_events_path.write_text("\n".join(events) + "\n", encoding="utf-8")

    def test_estimate_budget_recovery_seconds_waits_until_enough_events_age_out(self) -> None:
        self._write_request_events("crunchyroll", [50, 100, 200])
        recovery = estimate_budget_recovery_seconds(provider="crunchyroll", limit=3, critical_ratio=0.95, config=self.config)
        self.assertGreaterEqual(recovery, 3500)
        self.assertLessEqual(recovery, 3555)

    def test_estimate_budget_recovery_seconds_for_warn_ratio(self) -> None:
        self._write_request_events("crunchyroll", [50, 100, 200, 300, 400, 500, 600, 700])
        recovery = estimate_budget_recovery_seconds_for_ratio(provider="crunchyroll", limit=10, target_ratio=0.8, config=self.config)
        self.assertGreaterEqual(recovery, 2850)
        self.assertLessEqual(recovery, 2955)

    def test_run_pending_tasks_records_budget_backoff_and_skips_rechecks_until_expiry(self) -> None:
        self._write_request_events("crunchyroll", [50, 100, 200])
        self.config.service.crunchyroll_hourly_limit = 3

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            return_value={"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("skipped", sync_result["status"])
        self.assertIn("crunchyroll_budget_critical", sync_result["reason"])
        self.assertGreater(sync_result["budget_backoff_remaining_seconds"], 0)

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertIn("budget_backoff_until", sync_state)
        self.assertIn("budget_backoff_until_epoch", sync_state)
        self.assertEqual("skipped", sync_state["last_status"])
        self.assertEqual("crunchyroll", sync_state["budget_provider"])
        self.assertEqual("provider", sync_state["budget_scope"])
        self.assertEqual(self.config.service.sync_every_seconds, sync_state["every_seconds"])
        self.assertIn("next_due_at", sync_state)

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=AssertionError("budget-backed-off sync should not re-run subprocesses"),
        ):
            result_second = run_pending_tasks(self.config)

        sync_result_second = next(item for item in result_second["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("skipped", sync_result_second["status"])
        self.assertIn("budget_backoff_active", sync_result_second["reason"])

        state_second = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state_second = state_second["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("skipped", sync_state_second["last_status"])
        self.assertIn("budget_backoff_active", sync_state_second["last_skip_reason"])
        self.assertGreater(sync_state_second["budget_backoff_remaining_seconds"], 0)

    def test_run_pending_tasks_warn_paces_provider_before_critical_budget(self) -> None:
        self._write_request_events("crunchyroll", [50, 100, 200, 300, 400, 500, 600, 700])
        self.config.service.crunchyroll_hourly_limit = 10
        self.config.service.task_projected_request_counts["sync_fetch_crunchyroll"] = 1

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            return_value={"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("skipped", sync_result["status"])
        self.assertIn("crunchyroll_budget_warn", sync_result["reason"])
        self.assertEqual("warn", sync_result["budget_backoff_level"])
        self.assertGreater(sync_result["budget_backoff_remaining_seconds"], 0)

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("warn", sync_state["budget_backoff_level"])
        self.assertIn("budget_backoff_until", sync_state)
        self.assertIn("next_due_at", sync_state)

    def test_run_pending_tasks_uses_provider_warn_backoff_floor_when_larger_than_recovery(self) -> None:
        self._write_request_events("crunchyroll", [2810, 2820, 2830, 2840, 2850, 2860, 2870, 2880])
        self.config.service.crunchyroll_hourly_limit = 10
        self.config.service.provider_warn_backoff_floor_seconds["crunchyroll"] = 900
        self.config.service.task_projected_request_counts["sync_fetch_crunchyroll"] = 1

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            return_value={"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("skipped", sync_result["status"])
        self.assertEqual("warn", sync_result["budget_backoff_level"])
        self.assertEqual(900, sync_result["budget_backoff_remaining_seconds"])
        self.assertEqual(900, sync_result["budget_backoff_floor_seconds"])
        self.assertEqual("provider_floor", sync_result["budget_backoff_cooldown_source"])
        self.assertIn("cooldown=900s", sync_result["reason"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual(900, sync_state["budget_backoff_floor_seconds"])
        self.assertEqual("provider_floor", sync_state["budget_backoff_cooldown_source"])

    def test_run_pending_tasks_uses_task_specific_budget_limit_and_warn_floor(self) -> None:
        self._write_request_events("mal", [2810, 2820, 2830, 2840])
        self.config.service.mal_hourly_limit = 120
        self.config.service.task_hourly_limits["sync_apply"] = 5
        self.config.service.task_warn_backoff_floor_seconds["sync_apply"] = 900
        self.config.service.task_projected_request_counts.pop("sync_apply", None)

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            result = run_pending_tasks(self.config)

        sync_apply_result = next(item for item in result["results"] if item["task"] == "sync_apply")
        self.assertEqual("skipped", sync_apply_result["status"])
        self.assertEqual("warn", sync_apply_result["budget_backoff_level"])
        self.assertEqual("task", sync_apply_result["budget_scope"])
        self.assertEqual(900, sync_apply_result["budget_backoff_remaining_seconds"])
        self.assertEqual(900, sync_apply_result["budget_backoff_floor_seconds"])
        self.assertEqual("task_floor", sync_apply_result["budget_backoff_cooldown_source"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        apply_state = state["tasks"]["sync_apply"]
        self.assertEqual("mal", apply_state["budget_provider"])
        self.assertEqual("task", apply_state["budget_scope"])
        self.assertEqual(900, apply_state["budget_backoff_floor_seconds"])
        self.assertEqual("task_floor", apply_state["budget_backoff_cooldown_source"])

    def test_run_pending_tasks_projects_warn_budget_from_configured_request_cost(self) -> None:
        self._write_request_events("crunchyroll", [50, 100, 200, 300, 400, 500])
        self.config.service.crunchyroll_hourly_limit = 10
        self.config.service.task_projected_request_counts["sync_fetch_crunchyroll"] = 2

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            return_value={"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("skipped", sync_result["status"])
        self.assertIn("crunchyroll_budget_projected_warn", sync_result["reason"])
        self.assertIn("projected_requests=2", sync_result["reason"])
        self.assertEqual("configured", sync_result["api_usage"]["projected_request_source"])
        self.assertEqual(2, sync_result["api_usage"]["projected_request_count"])
        self.assertEqual(8, sync_result["api_usage"]["projected_request_total"])
        self.assertAlmostEqual(0.8, sync_result["api_usage"]["projected_ratio"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual(2, sync_state["projected_request_count"])
        self.assertEqual(8, sync_state["projected_request_total"])
        self.assertAlmostEqual(0.8, sync_state["projected_ratio"])
        self.assertEqual("configured", sync_state["projected_request_source"])

    def test_run_pending_tasks_prefers_mode_specific_configured_projection_for_full_refresh(self) -> None:
        self._write_request_events("hidive", [50, 100])
        (self.project_root / ".MAL-Updater" / "secrets" / "hidive_username.txt").write_text("user@example.com\n", encoding="utf-8")
        (self.project_root / ".MAL-Updater" / "secrets" / "hidive_password.txt").write_text("secret\n", encoding="utf-8")
        self.config.service.provider_hourly_limits["hidive"] = 72
        self.config.service.task_projected_request_counts["sync_fetch_hidive"] = 14
        self.config.service.task_projected_request_counts_by_mode["sync_fetch_hidive"] = {"full_refresh": 70, "incremental": 5}
        stale_anchor = datetime.now(timezone.utc).timestamp() - 90000
        self.config.service_state_path.write_text(
            json.dumps(
                {
                    "started_at": "2026-03-20T20:00:00Z",
                    "tasks": {
                        "mal_refresh": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                        "health": {"last_run_epoch": time.time(), "last_run_at": "2026-03-20T20:00:00Z"},
                        "sync_fetch_hidive": {
                            "full_refresh_anchor_epoch": stale_anchor,
                            "full_refresh_anchor_at": "2026-03-20T20:00:00Z",
                            "last_run_epoch": 0,
                        },
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        def fake_run_subprocess(config, args, *, label):
            if label == "sync_fetch_hidive":
                for index in range(5):
                    record_api_request_event(
                        "hidive",
                        "sync-fetch",
                        url=f"https://example.invalid/api/{index}",
                        method="GET",
                        outcome="ok",
                        status_code=200,
                        config=config,
                    )
            return {"status": "ok", "label": label, "returncode": 0, "stdout": "", "stderr": ""}

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=fake_run_subprocess,
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_hidive")
        self.assertEqual("ok", sync_result["status"])
        self.assertEqual("incremental", sync_result["fetch_mode"])
        self.assertEqual("periodic_cadence", sync_result["deferred_full_refresh_reason"])
        self.assertEqual(5, sync_result["next_projected_request_count"])
        self.assertEqual("configured_incremental", sync_result["next_projected_request_source"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_hidive"]
        self.assertEqual("incremental", sync_state["last_fetch_mode"])
        self.assertEqual(stale_anchor, sync_state["full_refresh_anchor_epoch"])
        self.assertEqual(5, sync_state["projected_request_count"])
        self.assertEqual("configured_incremental", sync_state["projected_request_source"])


    def test_run_pending_tasks_learns_observed_request_delta_for_future_budgeting(self) -> None:
        self.config.service.sync_every_seconds = 0
        self.config.service.health_every_seconds = 3600
        self.config.service.mal_refresh_every_seconds = 3600
        self.config.service.provider_projected_request_percentiles.pop("crunchyroll", None)

        def fake_run_subprocess(config, args, *, label):
            if label == "sync_fetch_crunchyroll":
                record_api_request_event(
                    "crunchyroll",
                    "sync-fetch",
                    url="https://example.invalid/api/1",
                    method="GET",
                    outcome="ok",
                    status_code=200,
                    config=config,
                )
                record_api_request_event(
                    "crunchyroll",
                    "sync-fetch",
                    url="https://example.invalid/api/2",
                    method="GET",
                    outcome="ok",
                    status_code=200,
                    config=config,
                )
            return {"status": "ok", "label": label, "returncode": 0, "stdout": "", "stderr": ""}

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=fake_run_subprocess,
        ):
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual(2, sync_state["last_request_delta"])
        self.assertEqual({"incremental": 2}, sync_state["last_request_delta_by_mode"])
        self.assertEqual(2, sync_state["projected_request_count"])
        self.assertEqual("observed_incremental_smoothed", sync_state["projected_request_source"])

    def test_run_pending_tasks_smooths_observed_request_delta_history_for_budgeting(self) -> None:
        self.config.service.sync_every_seconds = 0
        self.config.service.health_every_seconds = 3600
        self.config.service.mal_refresh_every_seconds = 3600
        self.config.service.provider_projected_request_percentiles.pop("crunchyroll", None)
        planned_deltas = iter([2, 8, 2])

        def fake_run_subprocess(config, args, *, label):
            if label == "sync_fetch_crunchyroll":
                for index in range(next(planned_deltas)):
                    record_api_request_event(
                        "crunchyroll",
                        "sync-fetch",
                        url=f"https://example.invalid/api/{index}",
                        method="GET",
                        outcome="ok",
                        status_code=200,
                        config=config,
                    )
            return {"status": "ok", "label": label, "returncode": 0, "stdout": "", "stderr": ""}

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=fake_run_subprocess,
        ):
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual([2, 8, 2], sync_state["last_request_delta_history"])
        self.assertEqual({"incremental": [2, 8, 2]}, sync_state["last_request_delta_history_by_mode"])
        self.assertEqual(4, sync_state["projected_request_count"])
        self.assertEqual("observed_incremental_smoothed", sync_state["projected_request_source"])

    def test_run_pending_tasks_uses_task_percentile_projection_and_history_window_for_budgeting(self) -> None:
        self.config.service.sync_every_seconds = 0
        self.config.service.health_every_seconds = 3600
        self.config.service.mal_refresh_every_seconds = 3600
        self.config.service.task_projected_request_history_windows["sync_fetch_crunchyroll"] = 3
        self.config.service.task_projected_request_percentiles["sync_fetch_crunchyroll"] = 0.75
        planned_deltas = iter([2, 8, 2, 20])

        def fake_run_subprocess(config, args, *, label):
            if label == "sync_fetch_crunchyroll":
                for index in range(next(planned_deltas)):
                    record_api_request_event(
                        "crunchyroll",
                        "sync-fetch",
                        url=f"https://example.invalid/api/{index}",
                        method="GET",
                        outcome="ok",
                        status_code=200,
                        config=config,
                    )
            return {"status": "ok", "label": label, "returncode": 0, "stdout": "", "stderr": ""}

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=fake_run_subprocess,
        ):
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual([8, 2, 20], sync_state["last_request_delta_history"])
        self.assertEqual({"incremental": [8, 2, 20]}, sync_state["last_request_delta_history_by_mode"])
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            sync_state,
            fetch_mode="incremental",
        )
        self.assertEqual(20, projected_count)
        self.assertEqual("observed_incremental_p75", projected_source)

    def test_run_pending_tasks_uses_provider_projection_defaults_when_task_override_absent(self) -> None:
        self.config.service.sync_every_seconds = 0
        self.config.service.health_every_seconds = 3600
        self.config.service.mal_refresh_every_seconds = 3600
        self.config.service.provider_projected_request_history_windows["crunchyroll"] = 3
        self.config.service.provider_projected_request_percentiles["crunchyroll"] = 0.75
        planned_deltas = iter([2, 8, 2, 20])

        def fake_run_subprocess(config, args, *, label):
            if label == "sync_fetch_crunchyroll":
                for index in range(next(planned_deltas)):
                    record_api_request_event(
                        "crunchyroll",
                        "sync-fetch",
                        url=f"https://example.invalid/api/{index}",
                        method="GET",
                        outcome="ok",
                        status_code=200,
                        config=config,
                    )
            return {"status": "ok", "label": label, "returncode": 0, "stdout": "", "stderr": ""}

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=fake_run_subprocess,
        ):
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual([8, 2, 20], sync_state["last_request_delta_history"])
        self.assertEqual({"incremental": [8, 2, 20]}, sync_state["last_request_delta_history_by_mode"])

        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            sync_state,
            fetch_mode="incremental",
        )
        self.assertEqual(20, projected_count)
        self.assertEqual("observed_incremental_p75", projected_source)

    def test_projected_request_count_uses_built_in_mal_refresh_default(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("mal_refresh", self.config.service.mal_refresh_every_seconds, budget_provider="mal"),
            {},
        )
        self.assertEqual(1, projected_count)
        self.assertEqual("configured", projected_source)

    def test_projected_request_count_uses_built_in_sync_apply_percentile(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_apply", self.config.service.sync_every_seconds, budget_provider="mal"),
            {"last_request_delta_history": [4, 10, 4]},
        )
        self.assertEqual(10, projected_count)
        self.assertEqual("observed_p90", projected_source)

    def test_projected_request_count_allows_task_percentile_override_for_sync_apply(self) -> None:
        self.config.service.task_projected_request_percentiles["sync_apply"] = 0.75
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_apply", self.config.service.sync_every_seconds, budget_provider="mal"),
            {"last_request_delta_history": [4, 10, 4]},
        )
        self.assertEqual(10, projected_count)
        self.assertEqual("observed_p75", projected_source)

    def test_projected_request_count_uses_built_in_crunchyroll_incremental_default(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            {},
            fetch_mode="incremental",
        )
        self.assertEqual(4, projected_count)
        self.assertEqual("configured_incremental", projected_source)

    def test_projected_request_count_uses_built_in_crunchyroll_full_refresh_default(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            {},
            fetch_mode="full_refresh",
        )
        self.assertEqual(55, projected_count)
        self.assertEqual("configured_full_refresh", projected_source)

    def test_projected_request_count_uses_built_in_hidive_incremental_default(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_hidive", self.config.service.sync_every_seconds, budget_provider="hidive"),
            {},
            fetch_mode="incremental",
        )
        self.assertEqual(4, projected_count)
        self.assertEqual("configured_incremental", projected_source)

    def test_projected_request_count_treats_built_in_mal_refresh_default_as_cold_start_seed(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("mal_refresh", self.config.service.mal_refresh_every_seconds, budget_provider="mal"),
            {"last_request_delta_history": [2, 3, 2]},
        )
        self.assertEqual(3, projected_count)
        self.assertEqual("observed_smoothed", projected_source)

    def test_projected_request_count_treats_built_in_full_refresh_default_as_cold_start_seed(self) -> None:
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            {
                "last_request_delta_history_by_mode": {"full_refresh": [18, 22, 20]},
                "last_request_delta_by_mode": {"full_refresh": 20},
            },
            fetch_mode="full_refresh",
        )
        self.assertEqual(22, projected_count)
        self.assertEqual("observed_full_refresh_p90", projected_source)

    def test_projected_request_count_lets_task_wide_override_beat_built_in_full_refresh_seed(self) -> None:
        self.config.service.task_projected_request_counts["sync_fetch_crunchyroll"] = 12
        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            {},
            fetch_mode="full_refresh",
        )
        self.assertEqual(12, projected_count)
        self.assertEqual("configured", projected_source)

    def test_run_pending_tasks_auto_uses_conservative_percentile_for_bursty_history(self) -> None:
        self.config.service.sync_every_seconds = 0
        self.config.service.health_every_seconds = 3600
        self.config.service.mal_refresh_every_seconds = 3600
        self.config.service.provider_projected_request_percentiles.pop("crunchyroll", None)
        planned_deltas = iter([2, 12, 2, 20])

        def fake_run_subprocess(config, args, *, label):
            if label == "sync_fetch_crunchyroll":
                for index in range(next(planned_deltas)):
                    record_api_request_event(
                        "crunchyroll",
                        "sync-fetch",
                        url=f"https://example.invalid/api/{index}",
                        method="GET",
                        outcome="ok",
                        status_code=200,
                        config=config,
                    )
            return {"status": "ok", "label": label, "returncode": 0, "stdout": "", "stderr": ""}

        with patch("mal_updater.service_runtime._refresh_mal_tokens", return_value={"status": "ok"}), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=fake_run_subprocess,
        ):
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual([2, 12, 2, 20], sync_state["last_request_delta_history"])
        self.assertEqual({"incremental": [2, 12, 2, 20]}, sync_state["last_request_delta_history_by_mode"])
        self.assertEqual(20, sync_state["projected_request_count"])
        self.assertEqual("observed_incremental_auto_p90", sync_state["projected_request_source"])

        projected_count, projected_source = _projected_request_count(
            self.config,
            TaskSpec("sync_fetch_crunchyroll", self.config.service.sync_every_seconds, budget_provider="crunchyroll"),
            sync_state,
            fetch_mode="incremental",
        )
        self.assertEqual(20, projected_count)
        self.assertEqual("observed_incremental_auto_p90", projected_source)

    def test_run_pending_tasks_clears_budget_backoff_after_successful_run(self) -> None:
        state = {
            "started_at": "2026-03-20T20:00:00Z",
            "tasks": {
                "sync_fetch_crunchyroll": {
                    "budget_backoff_level": "warn",
                    "budget_backoff_until_epoch": 1,
                    "budget_backoff_until": "2026-03-20T21:00:00Z",
                }
            },
        }
        self.config.service_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "mal"}), (True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._refresh_mal_tokens",
            return_value={"status": "ok"},
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        self.assertNotIn("budget_backoff_level", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertNotIn("budget_backoff_until", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertNotIn("budget_backoff_until_epoch", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertEqual("ok", saved["tasks"]["sync_fetch_crunchyroll"]["last_status"])
        self.assertIn("next_due_at", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertNotIn("last_skip_reason", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertIn("last_started_at", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertIn("last_finished_at", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertIn("last_decision_at", saved["tasks"]["sync_fetch_crunchyroll"])
        self.assertIn("last_duration_seconds", saved["tasks"]["sync_fetch_crunchyroll"])

    def test_run_pending_tasks_records_failure_backoff_for_provider_errors(self) -> None:
        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "mal"}), (True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._refresh_mal_tokens",
            return_value={"status": "ok"},
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "error", "label": "sync_fetch_crunchyroll", "returncode": 1, "stdout": "", "stderr": "HTTP 401 from Crunchyroll\n"},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("error", sync_result["status"])
        self.assertGreaterEqual(sync_result["failure_backoff_remaining_seconds"], 300)
        self.assertEqual("HTTP 401 from Crunchyroll", sync_result["failure_backoff_reason"])
        self.assertEqual("auth", sync_result["failure_backoff_class"])
        self.assertEqual(7200, sync_result["failure_backoff_floor_seconds"])
        self.assertEqual(1, sync_result["failure_backoff_consecutive_failures"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("error", sync_state["last_status"])
        self.assertEqual("HTTP 401 from Crunchyroll", sync_state["last_error"])
        self.assertEqual("auth", sync_state["failure_backoff_class"])
        self.assertEqual(7200, sync_state["failure_backoff_floor_seconds"])
        self.assertIn("failure_backoff_until", sync_state)
        self.assertIn("failure_backoff_until_epoch", sync_state)
        self.assertGreaterEqual(sync_state["failure_backoff_remaining_seconds"], 300)
        self.assertEqual(1, sync_state["failure_backoff_consecutive_failures"])

    def test_run_pending_tasks_uses_provider_auth_failure_floor_for_auth_style_errors(self) -> None:
        self.config.service.provider_auth_failure_backoff_floor_seconds["crunchyroll"] = 1800

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "mal"}), (True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._refresh_mal_tokens",
            return_value={"status": "ok"},
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "error", "label": "sync_fetch_crunchyroll", "returncode": 1, "stdout": "", "stderr": "login failed for Crunchyroll refresh token\n"},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("auth", sync_result["failure_backoff_class"])
        self.assertEqual(1800, sync_result["failure_backoff_floor_seconds"])
        self.assertEqual(1800, sync_result["failure_backoff_remaining_seconds"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("auth", sync_state["failure_backoff_class"])
        self.assertEqual(1800, sync_state["failure_backoff_floor_seconds"])

    def test_run_pending_tasks_treats_missing_refresh_token_as_auth_style_failure(self) -> None:
        self.config.service.provider_auth_failure_backoff_floor_seconds["crunchyroll"] = 2400

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "mal"}), (True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._refresh_mal_tokens",
            return_value={"status": "ok"},
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "error", "label": "sync_fetch_crunchyroll", "returncode": 1, "stdout": "", "stderr": "Missing Crunchyroll refresh token at /tmp/cr-token\n"},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("auth", sync_result["failure_backoff_class"])
        self.assertEqual(2400, sync_result["failure_backoff_floor_seconds"])
        self.assertEqual("Missing Crunchyroll refresh token at /tmp/cr-token", sync_result["failure_backoff_reason"])

        state = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = state["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("auth", sync_state["failure_backoff_class"])
        self.assertEqual(2400, sync_state["failure_backoff_floor_seconds"])

    def test_run_pending_tasks_skips_provider_retries_while_failure_backoff_is_active(self) -> None:
        state = {
            "started_at": "2026-03-20T20:00:00Z",
            "tasks": {
                "sync_fetch_crunchyroll": {
                    "failure_backoff_until_epoch": datetime.now(timezone.utc).timestamp() + 600,
                    "failure_backoff_until": "2026-03-20T21:10:00Z",
                    "failure_backoff_reason": "HTTP 401 from Crunchyroll",
                    "failure_backoff_class": "auth",
                    "failure_backoff_floor_seconds": 1800,
                    "failure_backoff_consecutive_failures": 2,
                }
            },
        }
        self.config.service_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "mal"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._refresh_mal_tokens",
            return_value={"status": "ok"},
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            result = run_pending_tasks(self.config)

        sync_result = next(item for item in result["results"] if item["task"] == "sync_fetch_crunchyroll")
        self.assertEqual("skipped", sync_result["status"])
        self.assertIn("failure_backoff_active", sync_result["reason"])
        self.assertEqual("HTTP 401 from Crunchyroll", sync_result["failure_backoff_reason"])
        self.assertEqual("auth", sync_result["failure_backoff_class"])
        self.assertEqual(1800, sync_result["failure_backoff_floor_seconds"])
        self.assertEqual(2, sync_result["failure_backoff_consecutive_failures"])

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertEqual("skipped", sync_state["last_status"])
        self.assertIn("failure_backoff_active", sync_state["last_skip_reason"])
        self.assertGreater(sync_state["failure_backoff_remaining_seconds"], 0)

    def test_run_pending_tasks_clears_failure_backoff_after_successful_run(self) -> None:
        state = {
            "started_at": "2026-03-20T20:00:00Z",
            "tasks": {
                "sync_fetch_crunchyroll": {
                    "failure_backoff_until_epoch": 1,
                    "failure_backoff_until": "2026-03-20T21:00:00Z",
                    "failure_backoff_reason": "HTTP 401 from Crunchyroll",
                    "failure_backoff_consecutive_failures": 2,
                }
            },
        }
        self.config.service_state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

        with patch("mal_updater.service_runtime._budget_gate", side_effect=[(True, None, {"provider": "mal"}), (True, None, {"provider": "crunchyroll"}), (True, None, {"provider": "mal"}), (True, None, None)]), patch(
            "mal_updater.service_runtime._refresh_mal_tokens",
            return_value={"status": "ok"},
        ), patch(
            "mal_updater.service_runtime._run_subprocess",
            side_effect=[
                {"status": "ok", "label": "sync_fetch_crunchyroll", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "sync_apply", "returncode": 0, "stdout": "", "stderr": ""},
                {"status": "ok", "label": "health", "returncode": 0, "stdout": "", "stderr": ""},
            ],
        ):
            run_pending_tasks(self.config)

        saved = json.loads(self.config.service_state_path.read_text(encoding="utf-8"))
        sync_state = saved["tasks"]["sync_fetch_crunchyroll"]
        self.assertNotIn("failure_backoff_until", sync_state)
        self.assertNotIn("failure_backoff_until_epoch", sync_state)
        self.assertNotIn("failure_backoff_reason", sync_state)
        self.assertNotIn("failure_backoff_class", sync_state)
        self.assertNotIn("failure_backoff_floor_seconds", sync_state)
        self.assertNotIn("failure_backoff_consecutive_failures", sync_state)
        self.assertEqual("ok", sync_state["last_status"])
