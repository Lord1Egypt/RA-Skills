import importlib
import os
from pathlib import Path

from governed_agents.contract import TaskContract


class DummyProc:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def _setup_module(monkeypatch, tmp_path):
    db_path = tmp_path / "reputation.db"
    monkeypatch.setenv("GOVERNED_DB_PATH", str(db_path))
    monkeypatch.setenv("OPENCLAW_WORKSPACE", str(tmp_path / "workspace"))
    return importlib.reload(importlib.import_module("governed_agents.openclaw_wrapper"))


def test_codex_subprocess_env_filtered(monkeypatch, tmp_path):
    module = _setup_module(monkeypatch, tmp_path)
    calls = []

    def _mock_run(cmd, **kwargs):
        calls.append(kwargs.get("env", {}))
        if cmd[0] == "git":
            return DummyProc()
        return DummyProc(stdout='```json {"status": "FAILED"} ```')

    monkeypatch.setattr(module.subprocess, "run", _mock_run)
    module.CODEX53_CLI = "codex"

    contract = TaskContract(objective="x", acceptance_criteria=[], required_files=[])
    module.spawn_governed(contract, engine="codex53")

    codex_env = calls[-1]
    for key in codex_env:
        assert key in module._CODEX_ALLOWED_VARS


def test_openclaw_subprocess_env_filtered(monkeypatch, tmp_path):
    module = _setup_module(monkeypatch, tmp_path)
    calls = []

    def _mock_run(cmd, **kwargs):
        calls.append(kwargs.get("env", {}))
        return DummyProc(stdout='```json {"status": "FAILED"} ```')

    monkeypatch.setattr(module.subprocess, "run", _mock_run)

    contract = TaskContract(objective="x", acceptance_criteria=[], required_files=[])
    module.spawn_governed(contract, engine="openclaw")

    openclaw_env = calls[-1]
    for key in openclaw_env:
        assert key in module._OPENCLAW_ALLOWED_VARS


def test_secret_keys_not_in_subprocess_env(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret")
    monkeypatch.setenv("OPENAI_API_KEY", "secret")
    module = _setup_module(monkeypatch, tmp_path)
    calls = []

    def _mock_run(cmd, **kwargs):
        calls.append(kwargs.get("env", {}))
        if cmd[0] == "git":
            return DummyProc()
        return DummyProc(stdout='```json {"status": "FAILED"} ```')

    monkeypatch.setattr(module.subprocess, "run", _mock_run)
    module.CODEX53_CLI = "codex"

    contract = TaskContract(objective="x", acceptance_criteria=[], required_files=[])
    module.spawn_governed(contract, engine="codex53")

    for env in calls:
        assert "ANTHROPIC_API_KEY" not in env
        assert "OPENAI_API_KEY" not in env


def test_pass_env_flag_is_ignored(monkeypatch, tmp_path):
    """GOVERNED_PASS_ENV=1 must NOT bypass the allowlist (escape hatch removed)."""
    monkeypatch.setenv("GOVERNED_PASS_ENV", "1")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret")
    monkeypatch.setenv("OPENAI_API_KEY", "secret")
    module = _setup_module(monkeypatch, tmp_path)
    calls = []

    def _mock_run(cmd, **kwargs):
        calls.append(kwargs.get("env", {}))
        if cmd[0] == "git":
            return DummyProc()
        return DummyProc(stdout='```json {"status": "FAILED"} ```')

    monkeypatch.setattr(module.subprocess, "run", _mock_run)
    module.CODEX53_CLI = "codex"

    contract = TaskContract(objective="x", acceptance_criteria=[], required_files=[])
    module.spawn_governed(contract, engine="codex53")

    # Even with GOVERNED_PASS_ENV=1, secrets must NOT be in subprocess env
    for env in calls:
        assert "ANTHROPIC_API_KEY" not in env
        assert "OPENAI_API_KEY" not in env
        for key in env:
            assert key in module._CODEX_ALLOWED_VARS


def test_git_subprocess_inherits_minimal_env(monkeypatch, tmp_path):
    module = _setup_module(monkeypatch, tmp_path)
    calls = []

    def _mock_run(cmd, **kwargs):
        calls.append((cmd, kwargs.get("env", {})))
        if cmd[0] == "git":
            return DummyProc()
        return DummyProc(stdout='```json {"status": "FAILED"} ```')

    monkeypatch.setattr(module.subprocess, "run", _mock_run)
    module.CODEX53_CLI = "codex"

    contract = TaskContract(objective="x", acceptance_criteria=[], required_files=[])
    module.spawn_governed(contract, engine="codex53")

    git_env = calls[0][1]
    for key in git_env:
        assert key in module._CODEX_ALLOWED_VARS
