from __future__ import annotations

import unittest

from intelligence_desk_brief.config import AppConfig, ConfigurationError


class ConfigTests(unittest.TestCase):
    def test_live_provider_mode_requires_apify_token(self) -> None:
        with self.assertRaises(ConfigurationError):
            AppConfig.from_env({"ENABLE_LIVE_PROVIDERS": "true"})

    def test_live_provider_mode_allows_bootstrap_without_task_ids(self) -> None:
        config = AppConfig.from_env(
            {
                "ENABLE_LIVE_PROVIDERS": "true",
                "APIFY_API_TOKEN": "token",
            }
        )
        self.assertTrue(config.enable_live_providers)
        self.assertIsNone(config.apify_task_id)

    def test_fixture_mode_runs_without_provider_tokens(self) -> None:
        config = AppConfig.from_env({})
        self.assertFalse(config.enable_live_providers)
        self.assertIsNone(config.apify_api_token)

    def test_local_state_dir_can_be_configured(self) -> None:
        config = AppConfig.from_env({"LOCAL_STATE_DIR": "/tmp/prdesk-state"})
        self.assertEqual(config.local_state_dir, "/tmp/prdesk-state")

    def test_retry_attempts_and_log_level_can_be_configured(self) -> None:
        config = AppConfig.from_env({"APIFY_RETRY_ATTEMPTS": "3", "LOG_LEVEL": "DEBUG"})
        self.assertEqual(config.apify_retry_attempts, 3)
        self.assertEqual(config.log_level, "DEBUG")


if __name__ == "__main__":
    unittest.main()
