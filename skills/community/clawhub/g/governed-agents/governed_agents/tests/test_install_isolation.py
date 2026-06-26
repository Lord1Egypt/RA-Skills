import os
import subprocess
from pathlib import Path
import importlib

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
INSTALL = REPO_ROOT / "install.sh"


def _run_install(env: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", str(INSTALL)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=env,
    )


def test_install_rejects_path_traversal(tmp_path):
    env = os.environ.copy()
    env["HOME"] = str(tmp_path / "home")
    env["OPENCLAW_WORKSPACE"] = "/tmp/../../etc"
    result = _run_install(env)
    assert result.returncode != 0


def test_install_rejects_symlink_target(tmp_path):
    home = tmp_path / "home"
    home.mkdir(parents=True, exist_ok=True)
    real_workspace = tmp_path / "real_ws"
    real_workspace.mkdir(parents=True)
    symlink_path = home / f".openclaw_symlink_{os.getpid()}"
    symlink_path.symlink_to(real_workspace)

    env = os.environ.copy()
    env["HOME"] = str(home)
    env["OPENCLAW_WORKSPACE"] = str(symlink_path)
    result = _run_install(env)

    symlink_path.unlink(missing_ok=True)
    assert result.returncode != 0


def test_install_ok_with_valid_path(tmp_path):
    home = tmp_path / "home"
    home.mkdir(parents=True, exist_ok=True)
    workspace = home / f".openclaw_test_{os.getpid()}"
    workspace.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["OPENCLAW_WORKSPACE"] = str(workspace)
    result = _run_install(env)
    assert result.returncode == 0


def test_install_idempotent(tmp_path):
    home = tmp_path / "home"
    home.mkdir(parents=True, exist_ok=True)
    workspace = home / f".openclaw_test_idem_{os.getpid()}"
    workspace.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["OPENCLAW_WORKSPACE"] = str(workspace)
    first = _run_install(env)
    second = _run_install(env)
    assert first.returncode == 0
    assert second.returncode == 0


def test_wrapper_workspace_path_resolved(monkeypatch, tmp_path):
    workspace = Path("/tmp") / f"governed_ws_{os.getpid()}" / ".." / f"governed_ws_{os.getpid()}"
    monkeypatch.setenv("OPENCLAW_WORKSPACE", str(workspace))
    module = importlib.import_module("governed_agents.openclaw_wrapper")
    module = importlib.reload(module)
    assert str(module.WORKSPACE) == str(Path(str(workspace)).resolve())
