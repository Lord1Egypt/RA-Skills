"""Tests for plugin system robustness (Phase 3)."""

import pytest
import asyncio
from ghostclaw.core.adapters.registry import PluginRegistry
from ghostclaw.core.adapters.base import BaseAdapter, AdapterMetadata


class DummyAdapter(BaseAdapter):
    def __init__(self, name="dummy", issues=None):
        self.name = name
        self.issues = issues or [f"{name} ran"]

    def get_metadata(self):
        return AdapterMetadata(
            name=self.name,
            version="1.0",
            description=f"Dummy plugin {self.name}",
            min_ghostclaw_version="0.1.0",
            max_ghostclaw_version="2.0.0"
        )

    async def ghost_analyze(self, root, files):
        return {"issues": self.issues}

    async def is_available(self) -> bool:
        return True


@pytest.fixture
def fresh_registry():
    reg = PluginRegistry()
    # Do not register internal plugins; only test manual registration
    return reg


def test_check_version_compatible(fresh_registry):
    """Test _check_version_compatible handles constraints correctly."""
    meta = AdapterMetadata(name="test", version="1.0", description="test")
    from ghostclaw.version import __version__ as current_ver
    # No constraints -> always compatible
    assert fresh_registry._check_version_compatible(current_ver, meta) is True

    # min constraint higher than current -> false
    meta.min_ghostclaw_version = "999.0.0"
    assert fresh_registry._check_version_compatible(current_ver, meta) is False

    # max constraint lower than current -> false
    meta.min_ghostclaw_version = None
    meta.max_ghostclaw_version = "0.0.1"
    assert fresh_registry._check_version_compatible(current_ver, meta) is False

    # within range -> true
    meta.min_ghostclaw_version = "0.0.0"
    meta.max_ghostclaw_version = "999.0.0"
    assert fresh_registry._check_version_compatible(current_ver, meta) is True


@pytest.mark.asyncio
async def test_plugin_filtering_by_enabled_plugins(fresh_registry):
    """Test that registry.enabled_plugins correctly filters which adapters run."""
    # Register two dummy adapters with distinct plugin names
    dummy1 = DummyAdapter("dummy1")
    dummy2 = DummyAdapter("dummy2")
    fresh_registry.pm.register(dummy1, name="dummy1")
    fresh_registry.pm.register(dummy2, name="dummy2")

    # 1. enabled_plugins = None -> all run
    fresh_registry.enabled_plugins = None
    results = await fresh_registry.run_analysis("/", [])
    assert len(results) == 2
    all_issues = [i for r in results for i in r.get("issues", [])]
    assert "dummy1 ran" in all_issues
    assert "dummy2 ran" in all_issues

    # 2. enabled_plugins = {"dummy1"} -> only dummy1 runs
    fresh_registry.enabled_plugins = {"dummy1"}
    results = await fresh_registry.run_analysis("/", [])
    assert len(results) == 1
    assert results[0].get("issues") == ["dummy1 ran"]

    # 3. enabled_plugins = {"dummy2"} -> only dummy2 runs
    fresh_registry.enabled_plugins = {"dummy2"}
    results = await fresh_registry.run_analysis("/", [])
    assert len(results) == 1
    assert results[0].get("issues") == ["dummy2 ran"]

    # 4. enabled_plugins = empty set -> none run (empty list of results)
    fresh_registry.enabled_plugins = set()
    results = await fresh_registry.run_analysis("/", [])
    assert len(results) == 0



