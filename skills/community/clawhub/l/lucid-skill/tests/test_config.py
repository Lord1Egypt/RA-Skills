"""Tests for configuration."""

from lucid_skill.config import get_config
from lucid_skill.types import LucidConfig


def test_get_config_returns_lucid_config():
    config = get_config()
    assert isinstance(config, LucidConfig)


def test_default_config_values():
    config = get_config()
    assert config.server.name == "lucid-skill"
    assert config.server.version == "2.0.0"
    assert config.query.max_rows == 1000
    assert config.query.timeout_seconds == 30
    assert config.catalog.auto_profile is True
    assert config.logging.level == "info"
