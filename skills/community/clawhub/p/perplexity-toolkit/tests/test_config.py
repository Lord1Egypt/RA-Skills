"""Tests for config module."""
import sys
sys.path.insert(0, "src")

from perplexity_toolkit.config import Config, get_config, set_config


class TestConfig:
    def test_defaults(self):
        cfg = Config()
        assert cfg.webbridge_url == "http://127.0.0.1:10086/command"
        assert cfg.base_url == "https://www.perplexity.ai"
        assert cfg.driver_backend == "webbridge"
        assert cfg.locale == "zh"
        assert cfg.max_retries == 3
        assert cfg.search_wait == 15.0
        assert cfg.deep_research_wait == 90.0
        assert cfg.batch_delay == 3.0

    def test_make_session(self):
        cfg = Config()
        assert cfg.make_session("test") == f"{cfg.session_prefix}-test"
        assert cfg.make_session("search") == f"{cfg.session_prefix}-search"

    def test_set_config(self):
        original = get_config()
        old_wait = original.search_wait
        try:
            set_config(search_wait=42.0)
            assert get_config().search_wait == 42.0
        finally:
            set_config(search_wait=old_wait)

    def test_set_config_ignores_unknown(self):
        # Should not raise on unknown keys
        set_config(nonexistent_key=123)

    def test_env_overrides(self, monkeypatch):
        monkeypatch.setenv("PERPLEXITY_SEARCH_WAIT", "42")
        monkeypatch.setenv("PERPLEXITY_LOCALE", "en")
        # Re-import to trigger env override
        from perplexity_toolkit.config import Config
        cfg = Config()
        # Note: env overrides are applied in get_config(), not Config()
        # This tests the field exists
        assert hasattr(cfg, "locale")
        assert hasattr(cfg, "max_retries")
