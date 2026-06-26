"""配置系统测试。"""

import os
import tempfile
from pathlib import Path

import pytest

from src.config import clear_cache, get_setting, load_all_sites, load_settings, load_site_config, load_yaml


@pytest.fixture(autouse=True)
def reset_cache():
    """每个测试前清除缓存。"""
    clear_cache()
    yield
    clear_cache()


class TestLoadYaml:
    def test_load_valid_yaml(self, tmp_path):
        f = tmp_path / "test.yaml"
        f.write_text("key: value\nnested:\n  a: 1")
        result = load_yaml(f)
        assert result == {"key": "value", "nested": {"a": 1}}

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_yaml("/nonexistent/path.yaml")


class TestLoadSettings:
    def test_load_default_settings(self):
        config = load_settings()
        assert "project" in config
        assert config["project"]["name"] == "lobster-crawler-skill"

    def test_env_override_db_path(self, monkeypatch):
        monkeypatch.setenv("DB_PATH", "/tmp/test.db")
        config = load_settings(force_reload=True)
        assert config["database"]["path"] == "/tmp/test.db"


class TestLoadSiteConfig:
    def test_load_webnovel(self):
        config = load_site_config("webnovel")
        assert config["site"]["name"] == "webnovel"

    def test_load_reelshorts(self):
        config = load_site_config("reelshorts")
        assert config["site"]["name"] == "reelshorts"

    def test_site_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_site_config("nonexistent_site")


class TestLoadAllSites:
    def test_loads_all(self):
        sites = load_all_sites()
        assert "webnovel" in sites
        assert "reelshorts" in sites
        assert len(sites) >= 2


class TestGetSetting:
    def test_nested_key(self):
        val = get_setting("database", "engine")
        assert val == "sqlite"

    def test_missing_key(self):
        val = get_setting("nonexistent", "deep", default="fallback")
        assert val == "fallback"
