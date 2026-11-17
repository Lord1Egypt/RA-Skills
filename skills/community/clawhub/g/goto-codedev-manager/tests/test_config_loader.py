from core.config_loader import ConfigLoader


def test_load_workspace(config_dir):
    loader = ConfigLoader(config_dir=config_dir)
    ws = loader.get_workspace("ws-test")
    assert ws.name == "测试工作区"
    assert ws.stack == "dotnet"
    assert ws.preferred_agent == "codex"
    assert ws.db_context == "AppDbContext"
    assert ws.repo_path == ws.path  # git_repo == path


def test_adapters_and_stacks(config_dir):
    loader = ConfigLoader(config_dir=config_dir)
    assert loader.get_adapter_config("codex")["priority"] == 1
    assert "dotnet" in loader.all_stacks()
    assert loader.get_stack_config("dotnet")["type_map"]["long"] == "bigint"


def test_unknown_workspace_raises(config_dir):
    loader = ConfigLoader(config_dir=config_dir)
    import pytest
    with pytest.raises(KeyError):
        loader.get_workspace("nope")
