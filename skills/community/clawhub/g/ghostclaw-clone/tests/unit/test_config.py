import os
import json
import pytest
from pathlib import Path
from ghostclaw.core.config import GhostclawConfig

def test_config_load_cli_overrides():
    config = GhostclawConfig.load(".", use_ai=True, ai_provider="openai")
    assert config.use_ai is True
    assert config.ai_provider == "openai"

def test_config_load_env_vars(monkeypatch):
    monkeypatch.setenv("GHOSTCLAW_API_KEY", "test-key")
    monkeypatch.setenv("GHOSTCLAW_USE_AI", "True")

    config = GhostclawConfig.load(".")
    assert config.api_key == "test-key"
    assert config.use_ai is True

def test_config_reject_local_api_key(tmp_path, monkeypatch):
    # Change current working directory to tmp_path for the test
    # since field_validator checks Path(".ghostclaw")
    monkeypatch.chdir(tmp_path)

    # Create local config with api_key
    gc_dir = tmp_path / ".ghostclaw"
    gc_dir.mkdir()
    config_file = gc_dir / "ghostclaw.json"
    with open(config_file, "w") as f:
        json.dump({"api_key": "secret-key"}, f)

    with pytest.raises(ValueError, match="SECURITY RISK: API key found in local project configuration"):
        # The validation is now correctly in the `load` classmethod to check the specific repo path
        GhostclawConfig.load(".")


def test_config_optional_bool_env_vars(monkeypatch, tmp_path):
    """Test that Optional[bool] env vars are correctly converted from strings."""
    # Run in a clean temporary directory to avoid picking up the real .ghostclaw/ghostclaw.json
    monkeypatch.chdir(tmp_path)
    # Also isolate global config by setting HOME to tmp_path
    monkeypatch.setenv("HOME", str(tmp_path))
    # Test use_pyscn (Optional[bool])
    monkeypatch.setenv("GHOSTCLAW_USE_PYSCN", "true")
    config = GhostclawConfig.load(".")
    assert config.use_pyscn is True

    monkeypatch.setenv("GHOSTCLAW_USE_PYSCN", "false")
    config = GhostclawConfig.load(".")
    assert config.use_pyscn is False

    monkeypatch.setenv("GHOSTCLAW_USE_PYSCN", "1")
    config = GhostclawConfig.load(".")
    assert config.use_pyscn is True

    monkeypatch.setenv("GHOSTCLAW_USE_PYSCN", "0")
    config = GhostclawConfig.load(".")
    assert config.use_pyscn is False

    # Test use_ai_codeindex (Optional[bool])
    monkeypatch.setenv("GHOSTCLAW_USE_AI_CODEINDEX", "yes")
    config = GhostclawConfig.load(".")
    assert config.use_ai_codeindex is True

    monkeypatch.setenv("GHOSTCLAW_USE_AI_CODEINDEX", "no")
    config = GhostclawConfig.load(".")
    assert config.use_ai_codeindex is False

    # Test that empty string results in None (optional)
    monkeypatch.delenv("GHOSTCLAW_USE_PYSCN", raising=False)
    monkeypatch.delenv("GHOSTCLAW_USE_AI_CODEINDEX", raising=False)
    config = GhostclawConfig.load(".")
    assert config.use_pyscn is None
    assert config.use_ai_codeindex is None
