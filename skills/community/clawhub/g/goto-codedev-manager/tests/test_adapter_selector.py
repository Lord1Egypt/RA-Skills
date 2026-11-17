import shutil

from core.adapter_selector import AdapterSelector
from core.config_loader import ConfigLoader


def _selector(config_dir):
    return AdapterSelector(ConfigLoader(config_dir=config_dir))


def test_explicit_agent_wins(config_dir):
    sel = _selector(config_dir)
    ws = ConfigLoader(config_dir=config_dir).get_workspace("ws-test")
    adapter = sel.select(ws, agent="claude_code")
    assert adapter.name == "claude_code"


def test_no_cli_falls_back_to_generic(config_dir, monkeypatch):
    # 所有 CLI 不可用：最终回落到 generic 工作区兜底
    monkeypatch.setattr(shutil, "which", lambda *_a, **_k: None)
    loader = ConfigLoader(config_dir=config_dir)
    sel = AdapterSelector(loader)
    ws = loader.get_workspace("ws-test")
    adapter = sel.select(ws)
    assert adapter.name == "generic"


def test_preferred_cli_available(config_dir, monkeypatch):
    # 只有 codex 可用
    monkeypatch.setattr(shutil, "which", lambda cmd, *a, **k: "/usr/bin/codex" if cmd == "codex" else None)
    loader = ConfigLoader(config_dir=config_dir)
    sel = AdapterSelector(loader)
    ws = loader.get_workspace("ws-test")
    adapter = sel.select(ws)
    assert adapter.name == "codex"


def test_qoer_cli_selected_by_priority(config_dir, monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda cmd, *a, **k: "/usr/bin/qoer" if cmd == "qoer" else None)
    loader = ConfigLoader(config_dir=config_dir)
    sel = AdapterSelector(loader)
    ws = loader.get_workspace("ws-test")
    adapter = sel.select(ws)
    assert adapter.name == "qoer"
    assert adapter.type == "cli"


def test_list_available_sorted_by_priority(config_dir):
    sel = _selector(config_dir)
    listing = sel.list_available()
    priorities = [e["priority"] for e in listing]
    assert priorities == sorted(priorities)
