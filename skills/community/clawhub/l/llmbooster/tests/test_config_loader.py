"""Unit tests for ConfigLoader."""

from __future__ import annotations

import json
import os
import sys
import tempfile

import pytest

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config_loader import ConfigLoader
from models import BoosterConfig, ValidationResult


@pytest.fixture
def loader() -> ConfigLoader:
    return ConfigLoader()


# ---------------------------------------------------------------------------
# load() — file not found
# ---------------------------------------------------------------------------

class TestLoadFileNotFound:
    def test_returns_all_defaults(self, loader: ConfigLoader) -> None:
        config = loader.load("/nonexistent/path/config.json")
        assert config.enabled is True
        assert config.thinkingDepth == 4
        assert config.maxRetries == 3

    def test_no_errors_attached(self, loader: ConfigLoader) -> None:
        config = loader.load("/nonexistent/path/config.json")
        assert not hasattr(config, "_errors")


# ---------------------------------------------------------------------------
# load() — JSON parse error
# ---------------------------------------------------------------------------

class TestLoadJsonParseError:
    def test_returns_defaults_on_bad_json(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{not valid json!!}")
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.enabled is True
            assert config.thinkingDepth == 4
            assert config.maxRetries == 3
        finally:
            os.unlink(tmp)

    def test_has_error_message(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("<<<>>>")
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert hasattr(config, "_errors")
            assert len(config._errors) >= 1
            assert "parse" in config._errors[0].lower()
        finally:
            os.unlink(tmp)


# ---------------------------------------------------------------------------
# load() — missing fields use defaults
# ---------------------------------------------------------------------------

class TestLoadMissingFields:
    def test_empty_object_uses_all_defaults(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.enabled is True
            assert config.thinkingDepth == 4
            assert config.maxRetries == 3
        finally:
            os.unlink(tmp)

    def test_partial_config_fills_missing(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"enabled": False}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.enabled is False
            assert config.thinkingDepth == 4
            assert config.maxRetries == 3
        finally:
            os.unlink(tmp)

    def test_only_thinking_depth_present(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"thinkingDepth": 2}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.enabled is True  # default
            assert config.thinkingDepth == 2  # provided
            assert config.maxRetries == 3  # default
        finally:
            os.unlink(tmp)


# ---------------------------------------------------------------------------
# load() — invalid fields fallback to default
# ---------------------------------------------------------------------------

class TestLoadInvalidFields:
    def test_invalid_field_uses_default(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"thinkingDepth": 99, "maxRetries": 5}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.thinkingDepth == 4  # default
            assert config.maxRetries == 5     # valid, kept
        finally:
            os.unlink(tmp)

    def test_error_mentions_field_name(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"maxRetries": "lots"}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert hasattr(config, "_errors")
            assert any("maxRetries" in e for e in config._errors)
        finally:
            os.unlink(tmp)

    def test_multiple_invalid_fields(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"enabled": "yes", "thinkingDepth": -1, "maxRetries": 0}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.enabled is True
            assert config.thinkingDepth == 4
            assert config.maxRetries == 3
            assert hasattr(config, "_errors")
            assert len(config._errors) == 3
        finally:
            os.unlink(tmp)


# ---------------------------------------------------------------------------
# load() — all valid config
# ---------------------------------------------------------------------------

class TestLoadValidConfig:
    def test_all_valid_values_loaded(self, loader: ConfigLoader) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"enabled": False, "thinkingDepth": 2, "maxRetries": 7}, f)
            tmp = f.name
        try:
            config = loader.load(tmp)
            assert config.enabled is False
            assert config.thinkingDepth == 2
            assert config.maxRetries == 7
            assert not hasattr(config, "_errors")
        finally:
            os.unlink(tmp)


# ---------------------------------------------------------------------------
# validate_field() — enabled
# ---------------------------------------------------------------------------

class TestValidateEnabled:
    def test_true_valid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("enabled", True)
        assert r.valid is True

    def test_false_valid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("enabled", False)
        assert r.valid is True

    def test_string_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("enabled", "yes")
        assert r.valid is False
        assert "enabled" in r.error_message

    def test_int_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("enabled", 1)
        assert r.valid is False


# ---------------------------------------------------------------------------
# validate_field() — thinkingDepth
# ---------------------------------------------------------------------------

class TestValidateThinkingDepth:
    @pytest.mark.parametrize("val", [1, 2, 3, 4])
    def test_valid_range(self, loader: ConfigLoader, val: int) -> None:
        r = loader.validate_field("thinkingDepth", val)
        assert r.valid is True

    def test_zero_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("thinkingDepth", 0)
        assert r.valid is False

    def test_five_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("thinkingDepth", 5)
        assert r.valid is False

    def test_bool_rejected(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("thinkingDepth", True)
        assert r.valid is False

    def test_string_rejected(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("thinkingDepth", "high")
        assert r.valid is False


# ---------------------------------------------------------------------------
# validate_field() — maxRetries
# ---------------------------------------------------------------------------

class TestValidateMaxRetries:
    @pytest.mark.parametrize("val", [1, 5, 10])
    def test_valid_range(self, loader: ConfigLoader, val: int) -> None:
        r = loader.validate_field("maxRetries", val)
        assert r.valid is True

    def test_zero_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("maxRetries", 0)
        assert r.valid is False

    def test_eleven_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("maxRetries", 11)
        assert r.valid is False

    def test_error_mentions_range(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("maxRetries", 99)
        assert r.valid is False
        assert "1" in r.error_message and "10" in r.error_message


# ---------------------------------------------------------------------------
# validate_field() — unknown field
# ---------------------------------------------------------------------------

class TestValidateUnknownField:
    def test_unknown_field_invalid(self, loader: ConfigLoader) -> None:
        r = loader.validate_field("unknownField", "whatever")
        assert r.valid is False
        assert "Unknown" in r.error_message or "unknown" in r.error_message
