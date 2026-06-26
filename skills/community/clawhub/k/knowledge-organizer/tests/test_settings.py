import os

from scripts import settings


def test_resolve_vault_root_prefers_env_then_config_then_default(monkeypatch):
    monkeypatch.delenv("OPENCLAW_KB_ROOT", raising=False)

    env_root = "~/ocl_env_root"
    config_root = "~/ocl_config_root"

    monkeypatch.setenv("OPENCLAW_KB_ROOT", env_root)
    assert settings.resolve_vault_root(config_root) == os.path.expanduser(env_root)

    monkeypatch.delenv("OPENCLAW_KB_ROOT", raising=False)
    assert settings.resolve_vault_root(config_root) == os.path.expanduser(config_root)

    assert settings.resolve_vault_root(None) == settings.DEFAULT_KB_PATH


def test_resolve_vault_root_can_require_explicit_configuration(monkeypatch):
    monkeypatch.delenv("OPENCLAW_KB_ROOT", raising=False)

    assert settings.resolve_vault_root(None, allow_default=False) is None


def test_resolve_vault_root_expands_tilde(monkeypatch):
    monkeypatch.setenv("OPENCLAW_KB_ROOT", "~/ocl_env_root_expand")
    expanded_env = settings.resolve_vault_root()
    assert expanded_env == os.path.expanduser("~/ocl_env_root_expand")

    monkeypatch.delenv("OPENCLAW_KB_ROOT", raising=False)
    expanded_config = settings.resolve_vault_root("~/ocl_config_root_expand")
    assert expanded_config == os.path.expanduser("~/ocl_config_root_expand")
