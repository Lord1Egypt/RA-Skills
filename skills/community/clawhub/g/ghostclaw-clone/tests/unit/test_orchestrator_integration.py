"""Tests for orchestrator integration (core PR-A/B/D)."""

import asyncio
import pytest
from pathlib import Path
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.adapters.registry import registry, INTERNAL_PLUGINS
from ghostclaw.core.analyzer import CodebaseAnalyzer


class TestOrchestrateConfigField:
    """Test the top-level 'orchestrate' boolean config field."""

    def test_orchestrate_default_none(self):
        """Default value of orchestrate should be None (not set)."""
        config = GhostclawConfig()
        assert config.orchestrate is None

    def test_orchestrate_cli_override_true(self):
        """CLI override can set orchestrate=True."""
        config = GhostclawConfig.load(".", orchestrate=True)
        assert config.orchestrate is True

    def test_orchestrate_cli_override_false(self):
        """CLI override can set orchestrate=False."""
        config = GhostclawConfig.load(".", orchestrate=False)
        assert config.orchestrate is False

    def test_orchestrate_env_var_true(self, monkeypatch, tmp_path):
        """Environment variable GHOSTCLAW_ORCHESTRATE can enable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "true")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is True

    def test_orchestrate_env_var_false(self, monkeypatch, tmp_path):
        """Environment variable GHOSTCLAW_ORCHESTRATE can disable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "false")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is False

    def test_orchestrate_and_orchestrator_dict_both_respected(self):
        """Both orchestrate flag and orchestrator dict can coexist; orchestrate takes precedence in enforcement."""
        config = GhostclawConfig.load(
            ".",
            orchestrate=True,
            orchestrator={"enabled": False, "use_llm": True}
        )
        assert config.orchestrate is True
        assert config.orchestrator["enabled"] is False
        assert config.orchestrator["use_llm"] is True


class TestOrchestratorEnforcement:
    """Test that analyzer enforces orchestrator-only mode when enabled."""

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Reset registry state between tests."""
        registry.enabled_plugins = None
        registry._registered_plugins = []
        registry.internal_plugins = set()
        registry.external_plugins = set()
        yield
        registry.enabled_plugins = None
        registry._registered_plugins = []
        registry.internal_plugins = set()
        registry.external_plugins = set()

    @pytest.mark.asyncio
    async def _run_analyzer(self, config, tmp_path):
        """Helper to run Analyzer on a minimal repo."""
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "main.py").write_text("print('hello')")
        analyzer = CodebaseAnalyzer()
        # Disable cache to avoid interference
        await analyzer.analyze(str(repo), use_cache=False, config=config)
        # After analyze, the registry.enabled_plugins reflects what was used
        return registry.enabled_plugins

    def test_orchestrate_flag_enables_only_orchestrator_no_qmd(self, tmp_path):
        """With orchestrate=True and use_qmd=False, only orchestrator should be enabled."""
        config = GhostclawConfig.load(str(tmp_path), orchestrate=True, use_qmd=False)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result == {'orchestrator'}

    def test_orchestrate_flag_with_qmd_enables_orchestrator_and_storage(self, tmp_path):
        """With orchestrate=True and use_qmd=True, enabled set should contain orchestrator, sqlite, qmd."""
        config = GhostclawConfig.load(str(tmp_path), orchestrate=True, use_qmd=True)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result == {'orchestrator', 'sqlite', 'qmd'}

    def test_orchestrator_dict_enabled_with_qmd(self, tmp_path):
        """Setting orchestrator={'enabled': True} with use_qmd=True also yields orchestrator + storage."""
        config = GhostclawConfig.load(str(tmp_path), orchestrator={"enabled": True}, use_qmd=True)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result == {'orchestrator', 'sqlite', 'qmd'}

    def test_orchestrate_false_with_use_qmd_true_all_plugins(self, tmp_path):
        """Default case: orchestrate=False, use_qmd=True -> all plugins enabled (None)."""
        config = GhostclawConfig.load(str(tmp_path), orchestrate=False, use_qmd=True)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result is None

    def test_orchestrate_false_with_use_qmd_false_gives_standard_set(self, tmp_path):
        """orchestrate=False, use_qmd=False -> internal plugins except qmd."""
        config = GhostclawConfig.load(str(tmp_path), orchestrate=False, use_qmd=False)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result is not None
        assert 'orchestrator' not in result
        assert 'lizard' in result
        assert 'sqlite' in result
        assert 'qmd' not in result

    def test_orchestrate_overrides_plugins_enabled(self, tmp_path):
        """If both orchestrate=True and plugins_enabled set, orchestrate wins."""
        config = GhostclawConfig.load(
            str(tmp_path),
            orchestrate=True,
            plugins_enabled=["lizard", "qmd"],
            use_qmd=False
        )
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result == {'orchestrator'}

    def test_orchestrate_overrides_use_qmd_but_still_adds_storage(self, tmp_path):
        """When both orchestrate=True and use_qmd=True, still only orchestrator + storage."""
        config = GhostclawConfig.load(str(tmp_path), orchestrate=True, use_qmd=True)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result == {'orchestrator', 'sqlite', 'qmd'}

    def test_orchestrator_dict_disabled_does_not_force(self, tmp_path):
        """If orchestrator.enabled=False and orchestrate=False, normal rules apply (here we set use_qmd=True to avoid set test)."""
        config = GhostclawConfig.load(str(tmp_path), orchestrator={"enabled": False}, use_qmd=True)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result is None

    def test_orchestrator_dict_disabled_with_use_qmd_false(self, tmp_path):
        """orchestrator disabled and use_qmd=False yields standard set (no orchestrator)."""
        config = GhostclawConfig.load(str(tmp_path), orchestrator={"enabled": False}, use_qmd=False)
        result = asyncio.run(self._run_analyzer(config, tmp_path))
        assert result is not None
        assert 'orchestrator' not in result
        assert 'lizard' in result


class TestOrchestrateConfigFieldExtra:
    """Additional edge-case and regression tests for the orchestrate/orchestrator config fields."""

    def test_orchestrator_default_is_none(self):
        """orchestrator dict field should default to None."""
        config = GhostclawConfig()
        assert config.orchestrator is None

    def test_orchestrate_field_is_none_by_default(self):
        """Default orchestrate value should be None (unset)."""
        config = GhostclawConfig()
        assert config.orchestrate is None

    def test_orchestrate_field_is_exact_bool_true_when_set(self):
        """orchestrate=True via load() should be strict bool True."""
        config = GhostclawConfig.load(".", orchestrate=True)
        assert type(config.orchestrate) is bool
        assert config.orchestrate is True

    def test_orchestrate_env_var_one(self, monkeypatch, tmp_path):
        """GHOSTCLAW_ORCHESTRATE='1' should enable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "1")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is True

    def test_orchestrate_env_var_yes(self, monkeypatch, tmp_path):
        """GHOSTCLAW_ORCHESTRATE='yes' should enable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "yes")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is True

    def test_orchestrate_env_var_uppercase_true(self, monkeypatch, tmp_path):
        """GHOSTCLAW_ORCHESTRATE='TRUE' (uppercase) should enable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "TRUE")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is True

    def test_orchestrate_env_var_zero(self, monkeypatch, tmp_path):
        """GHOSTCLAW_ORCHESTRATE='0' should disable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "0")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is False

    def test_orchestrate_env_var_no(self, monkeypatch, tmp_path):
        """GHOSTCLAW_ORCHESTRATE='no' should disable orchestrate."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GHOSTCLAW_ORCHESTRATE", "no")
        config = GhostclawConfig.load(".")
        assert config.orchestrate is False

    def test_orchestrate_in_local_config_file(self, tmp_path, monkeypatch):
        """orchestrate=true in .ghostclaw/ghostclaw.json should be respected."""
        import json
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("HOME", str(tmp_path))
        gc_dir = tmp_path / ".ghostclaw"
        gc_dir.mkdir()
        (gc_dir / "ghostclaw.json").write_text(json.dumps({"orchestrate": True}))
        config = GhostclawConfig.load(str(tmp_path))
        assert config.orchestrate is True

    def test_cli_override_orchestrate_takes_precedence_over_local_config(self, tmp_path, monkeypatch):
        """CLI override orchestrate=False should beat orchestrate=true from local config file."""
        import json
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("HOME", str(tmp_path))
        gc_dir = tmp_path / ".ghostclaw"
        gc_dir.mkdir()
        (gc_dir / "ghostclaw.json").write_text(json.dumps({"orchestrate": True}))
        config = GhostclawConfig.load(str(tmp_path), orchestrate=False)
        assert config.orchestrate is False

    def test_orchestrator_dict_in_local_config_file(self, tmp_path, monkeypatch):
        """orchestrator dict in .ghostclaw/ghostclaw.json should be loaded."""
        import json
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("HOME", str(tmp_path))
        gc_dir = tmp_path / ".ghostclaw"
        gc_dir.mkdir()
        orch_cfg = {"enabled": True, "use_llm": False, "weight": 0.8}
        (gc_dir / "ghostclaw.json").write_text(json.dumps({"orchestrator": orch_cfg}))
        config = GhostclawConfig.load(str(tmp_path))
        assert config.orchestrator is not None
        assert config.orchestrator["enabled"] is True
        assert config.orchestrator["use_llm"] is False
        assert config.orchestrator["weight"] == 0.8

    def test_orchestrator_none_does_not_trigger_orchestrate(self):
        """orchestrator=None (default) with orchestrate=False should not enable enforcement."""
        config = GhostclawConfig.load(".", orchestrate=False)
        assert config.orchestrator is None
        orchestrator_enabled = config.orchestrate or (
            config.orchestrator and config.orchestrator.get('enabled', False)
        )
        # Python short-circuit: `False or None` evaluates to None (falsy), not strict False
        assert not orchestrator_enabled

    def test_orchestrator_empty_dict_does_not_trigger_enforcement(self):
        """orchestrator={} (no 'enabled' key) with orchestrate=False should not enable enforcement."""
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={})
        orchestrator_enabled = config.orchestrate or (
            config.orchestrator and config.orchestrator.get('enabled', False)
        )
        # Python short-circuit: `False or {}` evaluates to {} (falsy empty dict), not strict False
        assert not orchestrator_enabled

    def test_orchestrator_dict_without_enabled_key_does_not_trigger(self):
        """orchestrator dict with only non-'enabled' keys should not force orchestration."""
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={"use_llm": True, "weight": 0.5})
        orchestrator_enabled = config.orchestrate or (
            config.orchestrator and config.orchestrator.get('enabled', False)
        )
        assert orchestrator_enabled is False

    def test_orchestrator_dict_enabled_true_triggers_enforcement(self):
        """orchestrator={'enabled': True} with orchestrate=False should enable orchestration."""
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={"enabled": True})
        orchestrator_enabled = config.orchestrate or (
            config.orchestrator and config.orchestrator.get('enabled', False)
        )
        assert orchestrator_enabled is True

    def test_both_orchestrate_true_and_orchestrator_dict_enabled_true(self):
        """Both orchestrate=True and orchestrator.enabled=True should both be True (no conflict)."""
        config = GhostclawConfig.load(".", orchestrate=True, orchestrator={"enabled": True})
        assert config.orchestrate is True
        assert config.orchestrator["enabled"] is True
        orchestrator_enabled = config.orchestrate or (
            config.orchestrator and config.orchestrator.get('enabled', False)
        )
        assert orchestrator_enabled is True


class TestOrchestratorEnforcementExtra:
    """Additional edge-case tests for plugin enforcement logic."""

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """Reset registry state between tests."""
        from ghostclaw.core.adapters.registry import registry
        registry.enabled_plugins = None
        registry._registered_plugins = []
        registry.internal_plugins = set()
        registry.external_plugins = set()
        yield
        registry.enabled_plugins = None
        registry._registered_plugins = []
        registry.internal_plugins = set()
        registry.external_plugins = set()

    def _apply_plugin_filter(self, config):
        """Replicate the plugin filter logic from Analyzer.analyze()."""
        from ghostclaw.core.adapters.registry import registry, INTERNAL_PLUGINS
        registry.internal_plugins = set(INTERNAL_PLUGINS)

        orchestrator_enabled = config.orchestrate or (config.orchestrator and config.orchestrator.get('enabled', False))
        if orchestrator_enabled:
            registry.enabled_plugins = {'orchestrator'}
        elif config.plugins_enabled is not None:
            registry.enabled_plugins = set(config.plugins_enabled)
        elif config.use_qmd:
            registry.enabled_plugins = None
        else:
            plugins = set(INTERNAL_PLUGINS) | registry.external_plugins
            plugins.discard("qmd")
            registry.enabled_plugins = plugins

        if config.use_qmd and registry.enabled_plugins is not None:
            registry.enabled_plugins.add('sqlite')
            registry.enabled_plugins.add('qmd')

    def test_orchestrate_false_orchestrator_none_standard_set(self):
        """Default config (orchestrate=False, orchestrator=None, use_qmd=False) -> standard plugin set."""
        from ghostclaw.core.adapters.registry import registry, INTERNAL_PLUGINS
        config = GhostclawConfig.load(".", orchestrate=False, use_qmd=False)
        assert config.orchestrator is None
        self._apply_plugin_filter(config)
        expected = (set(INTERNAL_PLUGINS) - {"qmd"})
        assert registry.enabled_plugins == expected

    def test_orchestrator_empty_dict_does_not_force_orchestrator_only(self):
        """orchestrator={} (no 'enabled' key) with orchestrate=False falls through to normal rules."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={}, use_qmd=False)
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins is not None
        assert 'orchestrator' not in registry.enabled_plugins

    def test_orchestrator_dict_enabled_true_alone_forces_orchestrator(self):
        """orchestrate=False but orchestrator.enabled=True alone should force orchestrator-only."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={"enabled": True}, use_qmd=False)
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins == {'orchestrator'}

    def test_orchestrator_dict_enabled_true_alone_with_qmd_adds_storage(self):
        """orchestrate=False but orchestrator.enabled=True with use_qmd=True should add sqlite and qmd."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={"enabled": True}, use_qmd=True)
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins == {'orchestrator', 'sqlite', 'qmd'}

    def test_orchestrator_dict_without_enabled_key_no_qmd_falls_through(self):
        """orchestrator dict without 'enabled' key should use get default (False) -> no forced mode."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(".", orchestrate=False, orchestrator={"routing": "round_robin"}, use_qmd=False)
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins is not None
        assert 'orchestrator' not in registry.enabled_plugins

    def test_plugins_enabled_respected_when_orchestrate_false(self):
        """plugins_enabled list is respected when orchestrate=False."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(
            ".", orchestrate=False, use_qmd=False, plugins_enabled=["lizard", "json_target"]
        )
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins == {"lizard", "json_target"}

    def test_orchestrate_true_beats_plugins_enabled_list(self):
        """When orchestrate=True, plugins_enabled list is ignored in favor of orchestrator-only."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(
            ".", orchestrate=True, use_qmd=False, plugins_enabled=["lizard"]
        )
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins == {"orchestrator"}
        assert "lizard" not in registry.enabled_plugins

    def test_qmd_not_added_when_use_qmd_false_and_orchestrate_true(self):
        """With orchestrate=True and use_qmd=False, qmd and sqlite must NOT be in enabled set."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(".", orchestrate=True, use_qmd=False)
        self._apply_plugin_filter(config)
        assert 'qmd' not in registry.enabled_plugins
        assert 'sqlite' not in registry.enabled_plugins

    def test_orchestrate_enabled_set_contains_only_orchestrator_string(self):
        """The value set when orchestrate=True (no qmd) must be exactly {'orchestrator'}."""
        from ghostclaw.core.adapters.registry import registry
        config = GhostclawConfig.load(".", orchestrate=True, use_qmd=False)
        self._apply_plugin_filter(config)
        assert registry.enabled_plugins == {"orchestrator"}
        assert len(registry.enabled_plugins) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])