"""Test that QMDStorageAdapter is filtered by use_qmd config."""
import pytest
from pathlib import Path
from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.adapters.registry import registry, INTERNAL_PLUGINS

@pytest.fixture(autouse=True)
def reset_registry():
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

def _setup_analyzer_plugin_logic(config):
    """Replicate the plugin initialization logic from Analyzer.analyze()."""
    # Register internal plugins
    registry.register_internal_plugins()

    # Apply plugin filter as in analyzer.analyze()
    if config.plugins_enabled is not None:
        registry.enabled_plugins = set(config.plugins_enabled)
    else:
        if config.use_qmd:
            registry.enabled_plugins = None
        else:
            plugins = set(INTERNAL_PLUGINS)
            plugins.discard("qmd")
            plugins.update(registry.external_plugins)
            registry.enabled_plugins = plugins

    # Override: if use_qmd, force-enable sqlite and qmd
    if config.use_qmd and registry.enabled_plugins is not None:
        registry.enabled_plugins.add("sqlite")
        registry.enabled_plugins.add("qmd")

def test_qmd_excluded_when_use_qmd_false(tmp_path):
    """When use_qmd=False, qmd should not be in enabled_plugins by default."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".ghostclaw").mkdir()
    (repo / "main.py").write_text("print('hello')")

    config = GhostclawConfig.load(str(repo), use_qmd=False)

    # Simulate analyzer plugin setup
    _setup_analyzer_plugin_logic(config)

    assert registry.enabled_plugins is not None
    assert "qmd" not in registry.enabled_plugins
    assert "sqlite" in registry.enabled_plugins

def test_qmd_included_when_use_qmd_true(tmp_path):
    """When use_qmd=True, qmd should be enabled (enabled_plugins = None for all)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".ghostclaw").mkdir()
    (repo / "main.py").write_text("print('hello')")

    config = GhostclawConfig.load(str(repo), use_qmd=True)

    _setup_analyzer_plugin_logic(config)

    # With use_qmd=True and no plugins_enabled, all plugins are enabled (None means no filter)
    assert registry.enabled_plugins is None

def test_external_plugins_preserved_when_use_qmd_false(tmp_path):
    """External plugins should remain enabled when use_qmd=False."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".ghostclaw").mkdir()
    (repo / "plugins").mkdir()
    (repo / "main.py").write_text("print('hello')")

    # Simulate an external plugin named 'myplugin'
    # We'll manually add it to registry.external_plugins to simulate loading
    registry.external_plugins.add("myplugin")

    config = GhostclawConfig.load(str(repo), use_qmd=False)

    _setup_analyzer_plugin_logic(config)

    assert registry.enabled_plugins is not None
    assert "qmd" not in registry.enabled_plugins
    assert "myplugin" in registry.enabled_plugins

def test_external_plugins_allowed_when_use_qmd_true(tmp_path):
    """When use_qmd=True, external plugins should also be allowed (enabled_plugins=None)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".ghostclaw").mkdir()
    (repo / "plugins").mkdir()
    (repo / "main.py").write_text("print('hello')")

    registry.external_plugins.add("myplugin")

    config = GhostclawConfig.load(str(repo), use_qmd=True)

    _setup_analyzer_plugin_logic(config)

    # No filter → None
    assert registry.enabled_plugins is None
