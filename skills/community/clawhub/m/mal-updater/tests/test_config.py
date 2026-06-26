from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from mal_updater.config import load_config, load_mal_secrets


class ConfigLoadingTests(unittest.TestCase):
    def test_defaults_resolve_under_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)

            config = load_config(root)
            secrets = load_mal_secrets(config)

            self.assertEqual(config.settings_path, (root / ".MAL-Updater" / "config" / "settings.toml").resolve())
            self.assertEqual(config.config_dir, (root / ".MAL-Updater" / "config").resolve())
            self.assertEqual(config.secrets_dir, (root / ".MAL-Updater" / "secrets").resolve())
            self.assertEqual(config.data_dir, (root / ".MAL-Updater" / "data").resolve())
            self.assertEqual(config.state_dir, (root / ".MAL-Updater" / "state").resolve())
            self.assertEqual(config.cache_dir, (root / ".MAL-Updater" / "cache").resolve())
            self.assertEqual(config.db_path, (root / ".MAL-Updater" / "data" / "mal_updater.sqlite3").resolve())
            self.assertEqual(config.mal.bind_host, "0.0.0.0")
            self.assertEqual(config.mal.redirect_uri, "http://127.0.0.1:8765/callback")
            self.assertEqual(secrets.client_id_path, (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").resolve())
            self.assertEqual(72, config.service.provider_hourly_limits["hidive"])
            self.assertEqual(48, config.service.task_hourly_limits["sync_apply"])
            self.assertEqual(1, config.service.task_projected_request_counts["mal_refresh"])
            self.assertEqual(8, config.service.task_projected_request_counts["sync_apply"])
            self.assertEqual(4, config.service.task_projected_request_counts_by_mode["sync_fetch_crunchyroll"]["incremental"])
            self.assertEqual(55, config.service.task_projected_request_counts_by_mode["sync_fetch_crunchyroll"]["full_refresh"])
            self.assertEqual(4, config.service.task_projected_request_counts_by_mode["sync_fetch_hidive"]["incremental"])
            self.assertEqual(71, config.service.task_projected_request_counts_by_mode["sync_fetch_hidive"]["full_refresh"])
            self.assertEqual(7, config.service.projected_request_history_window_for("unknown_task", provider="crunchyroll"))
            self.assertEqual(9, config.service.projected_request_history_window_for("unknown_task", provider="hidive"))
            self.assertEqual(3, config.service.projected_request_history_window_for("mal_refresh"))
            self.assertEqual(3, config.service.projected_request_history_window_for("sync_apply"))
            self.assertEqual(0.9, config.service.task_projected_request_percentiles["sync_apply"])
            self.assertEqual(0.9, config.service.projected_request_percentile_for("sync_apply"))
            self.assertEqual(0.9, config.service.projected_request_percentile_for("unknown_task", provider="crunchyroll"))
            self.assertIsNone(config.service.projected_request_percentile_for("unknown_task", provider="hidive"))
            self.assertEqual(900, config.service.backoff_floor_seconds_for("crunchyroll", level="warn"))
            self.assertEqual(900, config.service.backoff_floor_seconds_for("mal", level="warn", task_name="sync_apply"))
            self.assertEqual(1200, config.service.backoff_floor_seconds_for("hidive", level="critical"))
            self.assertEqual(1800, config.service.backoff_floor_seconds_for("mal", level="critical", task_name="sync_apply"))
            self.assertEqual(7200, config.service.auth_failure_backoff_floor_seconds_for("crunchyroll"))
            self.assertEqual(2400, config.service.auth_failure_backoff_floor_seconds_for("mal", task_name="sync_apply"))
            self.assertEqual("task", config.service.budget_scope_for("mal", task_name="sync_apply"))

    def test_settings_file_overrides_paths_and_secret_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    completion_threshold = 0.95
                    contract_version = "2.0"

                    [paths]
                    config_dir = "./"
                    secrets_dir = "../private"
                    data_dir = "../var/data"
                    state_dir = "../var/state"
                    cache_dir = "../var/cache"
                    db_path = "../var/custom.sqlite3"

                    [mal]
                    bind_host = "127.0.0.1"
                    redirect_host = "127.0.0.50"
                    redirect_port = 9999

                    [secret_files]
                    mal_client_id = "ids/client-id.txt"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            config = load_config(root)
            secrets = load_mal_secrets(config)

            self.assertEqual(config.completion_threshold, 0.95)
            self.assertEqual(config.contract_version, "2.0")
            self.assertEqual(config.config_dir, (root / ".MAL-Updater" / "config").resolve())
            self.assertEqual(config.secrets_dir, (root / ".MAL-Updater" / "private").resolve())
            self.assertEqual(config.data_dir, (root / ".MAL-Updater" / "var" / "data").resolve())
            self.assertEqual(config.state_dir, (root / ".MAL-Updater" / "var" / "state").resolve())
            self.assertEqual(config.cache_dir, (root / ".MAL-Updater" / "var" / "cache").resolve())
            self.assertEqual(config.db_path, (root / ".MAL-Updater" / "var" / "custom.sqlite3").resolve())
            self.assertEqual(config.mal.bind_host, "127.0.0.1")
            self.assertEqual(config.mal.redirect_uri, "http://127.0.0.50:9999/callback")
            self.assertEqual(secrets.client_id_path, (root / ".MAL-Updater" / "private" / "ids" / "client-id.txt").resolve())

    def test_settings_file_loads_provider_budget_tables(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [service]
                    source_provider_hourly_limit = 90
                    source_provider_warn_backoff_floor_seconds = 180
                    source_provider_critical_backoff_floor_seconds = 600
                    source_provider_auth_failure_backoff_floor_seconds = 2400

                    [service.provider_hourly_limits]
                    hidive = 72

                    [service.task_hourly_limits]
                    sync_apply = 24

                    [service.task_projected_request_counts]
                    mal_refresh = 2
                    sync_apply = 8
                    sync_fetch_hidive = 14

                    [service.task_projected_request_counts_by_mode.sync_fetch_hidive]
                    full_refresh = 60
                    incremental = 5

                    [service.provider_projected_request_history_windows]
                    crunchyroll = 7
                    hidive = 11

                    [service.task_projected_request_history_windows]
                    mal_refresh = 4
                    sync_apply = 3
                    sync_fetch_hidive = 9

                    [service.provider_projected_request_percentiles]
                    crunchyroll = 0.85
                    hidive = 0.95

                    [service.task_projected_request_percentiles]
                    sync_apply = 0.75
                    sync_fetch_hidive = 0.9

                    [service.provider_warn_backoff_floor_seconds]
                    crunchyroll = 900
                    hidive = 300

                    [service.provider_critical_backoff_floor_seconds]
                    crunchyroll = 1800
                    hidive = 1200

                    [service.task_warn_backoff_floor_seconds]
                    sync_apply = 450

                    [service.task_critical_backoff_floor_seconds]
                    sync_apply = 1500

                    [service.provider_auth_failure_backoff_floor_seconds]
                    hidive = 3600

                    [service.task_auth_failure_backoff_floor_seconds]
                    sync_apply = 2400
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual(90, config.service.source_provider_hourly_limit)
            self.assertEqual(180, config.service.source_provider_warn_backoff_floor_seconds)
            self.assertEqual(600, config.service.source_provider_critical_backoff_floor_seconds)
            self.assertEqual(2400, config.service.source_provider_auth_failure_backoff_floor_seconds)
            self.assertEqual(72, config.service.provider_hourly_limits["hidive"])
            self.assertEqual(24, config.service.task_hourly_limits["sync_apply"])
            self.assertEqual(2, config.service.task_projected_request_counts["mal_refresh"])
            self.assertEqual(8, config.service.task_projected_request_counts["sync_apply"])
            self.assertEqual(14, config.service.task_projected_request_counts["sync_fetch_hidive"])
            self.assertEqual(60, config.service.task_projected_request_counts_by_mode["sync_fetch_hidive"]["full_refresh"])
            self.assertEqual(5, config.service.task_projected_request_counts_by_mode["sync_fetch_hidive"]["incremental"])
            self.assertEqual(7, config.service.provider_projected_request_history_windows["crunchyroll"])
            self.assertEqual(11, config.service.provider_projected_request_history_windows["hidive"])
            self.assertEqual(4, config.service.task_projected_request_history_windows["mal_refresh"])
            self.assertEqual(3, config.service.task_projected_request_history_windows["sync_apply"])
            self.assertEqual(9, config.service.task_projected_request_history_windows["sync_fetch_hidive"])
            self.assertEqual(0.85, config.service.provider_projected_request_percentiles["crunchyroll"])
            self.assertEqual(0.95, config.service.provider_projected_request_percentiles["hidive"])
            self.assertEqual(0.75, config.service.task_projected_request_percentiles["sync_apply"])
            self.assertEqual(0.9, config.service.task_projected_request_percentiles["sync_fetch_hidive"])
            self.assertEqual(900, config.service.provider_warn_backoff_floor_seconds["crunchyroll"])
            self.assertEqual(300, config.service.provider_warn_backoff_floor_seconds["hidive"])
            self.assertEqual(450, config.service.task_warn_backoff_floor_seconds["sync_apply"])
            self.assertEqual(1800, config.service.provider_critical_backoff_floor_seconds["crunchyroll"])
            self.assertEqual(1200, config.service.provider_critical_backoff_floor_seconds["hidive"])
            self.assertEqual(1500, config.service.task_critical_backoff_floor_seconds["sync_apply"])
            self.assertEqual(3600, config.service.provider_auth_failure_backoff_floor_seconds["hidive"])
            self.assertEqual(2400, config.service.task_auth_failure_backoff_floor_seconds["sync_apply"])
            self.assertEqual(90, config.service.hourly_limit_for("new-provider"))
            self.assertEqual(72, config.service.hourly_limit_for("hidive"))
            self.assertEqual(24, config.service.hourly_limit_for("mal", task_name="sync_apply"))
            self.assertEqual(4, config.service.projected_request_history_window_for("mal_refresh"))
            self.assertEqual(3, config.service.projected_request_history_window_for("sync_apply"))
            self.assertEqual(0.75, config.service.projected_request_percentile_for("sync_apply"))
            self.assertEqual(11, config.service.projected_request_history_window_for("unknown_task", provider="hidive"))
            self.assertEqual(0.95, config.service.projected_request_percentile_for("unknown_task", provider="hidive"))
            self.assertEqual(5, config.service.projected_request_history_window_for("unknown_task"))
            self.assertIsNone(config.service.projected_request_percentile_for("unknown_task"))
            self.assertEqual(180, config.service.backoff_floor_seconds_for("new-provider", level="warn"))
            self.assertEqual(600, config.service.backoff_floor_seconds_for("new-provider", level="critical"))
            self.assertEqual(450, config.service.backoff_floor_seconds_for("mal", level="warn", task_name="sync_apply"))
            self.assertEqual(1500, config.service.backoff_floor_seconds_for("mal", level="critical", task_name="sync_apply"))
            self.assertEqual(2400, config.service.auth_failure_backoff_floor_seconds_for("new-provider"))
            self.assertEqual(2400, config.service.auth_failure_backoff_floor_seconds_for("mal", task_name="sync_apply"))
            self.assertEqual("task", config.service.budget_scope_for("mal", task_name="sync_apply"))
            self.assertEqual("provider", config.service.budget_scope_for("hidive", task_name="sync_fetch_hidive"))


if __name__ == "__main__":
    unittest.main()
