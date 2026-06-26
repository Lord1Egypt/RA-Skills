import pytest
from pathlib import Path
from ghostclaw.cli.services import PluginService

def test_plugin_service_list_plugins(mocker):
    service = PluginService()
    mock_registry = mocker.patch("ghostclaw.cli.services.registry")
    mock_registry.get_plugin_metadata.return_value = [{"name": "test-plugin", "version": "1.0"}]

    plugins = service.list_plugins()
    assert len(plugins) == 1
    assert plugins[0]["name"] == "test-plugin"

def test_plugin_service_get_plugin_info(mocker):
    service = PluginService()
    mock_registry = mocker.patch("ghostclaw.cli.services.registry")
    mock_registry.get_plugin_metadata.return_value = [{"name": "test-plugin", "version": "1.0"}]

    info = service.get_plugin_info("test-plugin")
    assert info["version"] == "1.0"

    info_none = service.get_plugin_info("nonexistent")
    assert info_none is None

def test_plugin_service_add_plugin(mocker, tmp_path):
    service = PluginService(workspace_path=str(tmp_path))
    source_file = tmp_path / "myplugin.py"
    source_file.write_text("print('hello')")

    target = service.add_plugin(str(source_file))
    assert target.exists()
    assert target.read_text() == "print('hello')"

def test_plugin_service_remove_plugin(mocker, tmp_path):
    service = PluginService(workspace_path=str(tmp_path))
    target = service.plugins_dir / "myplugin.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("print('hello')")

    mock_registry = mocker.patch("ghostclaw.cli.services.registry")
    mock_registry.internal_plugins = []

    service.remove_plugin("myplugin.py")
    assert not target.exists()

def test_plugin_service_scaffold_plugin(tmp_path):
    service = PluginService(workspace_path=str(tmp_path))
    target = service.scaffold_plugin("new-plugin")
    assert target.exists()
    assert (target / "__init__.py").exists()
