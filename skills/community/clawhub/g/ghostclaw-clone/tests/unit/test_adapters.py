import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock
from ghostclaw.core.adapters.base import MetricAdapter, AdapterMetadata
from ghostclaw.core.adapters.registry import PluginRegistry
from ghostclaw.core.adapters.hooks import hookimpl

class MockMetricAdapter(MetricAdapter):
    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(name="mock_metric", version="0.1.0", description="Mock adapter for tests")
    
    async def is_available(self) -> bool:
        return True

    async def analyze(self, root: str, files: list) -> dict:
        """Requirement for MetricAdapter ABC."""
        return await self.ghost_analyze(root, files)

    @hookimpl
    async def ghost_analyze(self, root: str, files: list) -> dict:
        return {"issues": ["mock issue"], "architectural_ghosts": [], "red_flags": []}

    @hookimpl
    def ghost_get_metadata(self) -> dict:
        meta = self.get_metadata()
        return {"name": meta.name, "version": meta.version, "description": meta.description}

@pytest.fixture
def registry():
    return PluginRegistry()

def test_registry_initialization(registry):
    assert registry.pm is not None
    assert registry.internal_plugins == set()

def test_internal_plugin_registration(registry):
    registry.register_internal_plugins()
    # Check if a few known ones are there
    assert "pyscn" in registry.internal_plugins
    assert "sqlite" in registry.internal_plugins

@pytest.mark.asyncio
async def test_hook_dispatching(registry):
    mock_adapter = MockMetricAdapter()
    registry.pm.register(mock_adapter)
    
    results = await registry.run_analysis("/tmp", [])
    assert len(results) == 1
    assert results[0]["issues"] == ["mock issue"]

def test_metadata_collection(registry):
    mock_adapter = MockMetricAdapter()
    registry.pm.register(mock_adapter)
    
    metadata = registry.get_plugin_metadata()
    assert any(m["name"] == "mock_metric" for m in metadata)

@pytest.mark.asyncio
async def test_dynamic_loading(registry, tmp_path):
    # Create a dummy plugin file
    plugin_dir = tmp_path / "my_plugin"
    plugin_dir.mkdir()
    (plugin_dir / "__init__.py").write_text("""
from ghostclaw.core.adapters.hooks import hookimpl
class MyAdapter:
    @hookimpl
    def ghost_get_metadata(self):
        return {"name": "dynamic_test", "version": "1.0.0"}
""")
    
    registry.load_external_plugins(tmp_path)
    metadata = registry.get_plugin_metadata()
    assert any(m.get("name") == "dynamic_test" for m in metadata)
    # Check if it was tracked as external
    assert any("my_plugin" in name for name in registry.external_plugins)
