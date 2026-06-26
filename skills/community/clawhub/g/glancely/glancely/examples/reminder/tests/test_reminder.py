"""reminder: add -> done -> digest -> stats round-trip."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
COMPONENT_DIR = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def _setup(tmp):
    env = {**os.environ, "GLANCE_HOME": tmp, "PYTHONPATH": str(REPO_ROOT)}
    subprocess.check_call(
        [sys.executable, "-m", "glancely.core.storage.migrations",
         str(COMPONENT_DIR)],
        env=env, cwd=REPO_ROOT,
    )
    return env


def test_add_done_stats():
    with tempfile.TemporaryDirectory() as tmp:
        env = _setup(tmp)
        out = subprocess.check_output(
            [sys.executable, str(SCRIPTS / "log.py"), "--add", "--title", "test reminder", "--due", "2026-12-31"],
            env=env, cwd=REPO_ROOT,
        )
        rid = json.loads(out)["id"]

        stats = json.loads(subprocess.check_output(
            [sys.executable, str(SCRIPTS / "stats.py")], env=env, cwd=REPO_ROOT))
        assert stats["summary"]["active"] == 1
        assert stats["summary"]["overdue"] == 0

        subprocess.check_call(
            [sys.executable, str(SCRIPTS / "log.py"), "--done", "--id", str(rid)],
            env=env, cwd=REPO_ROOT,
        )
        stats = json.loads(subprocess.check_output(
            [sys.executable, str(SCRIPTS / "stats.py")], env=env, cwd=REPO_ROOT))
        assert stats["summary"]["active"] == 0
        assert stats["summary"]["completed_7d"] == 1


def test_digest_empty_and_populated():
    with tempfile.TemporaryDirectory() as tmp:
        env = _setup(tmp)
        empty = subprocess.check_output(
            [sys.executable, str(SCRIPTS / "digest.py")], env=env, cwd=REPO_ROOT,
        ).decode()
        assert "今天没有未完成提醒" in empty

        subprocess.check_call(
            [sys.executable, str(SCRIPTS / "log.py"), "--add", "--title", "ping team"],
            env=env, cwd=REPO_ROOT,
        )
        full = subprocess.check_output(
            [sys.executable, str(SCRIPTS / "digest.py")], env=env, cwd=REPO_ROOT,
        ).decode()
        assert "ping team" in full


if __name__ == "__main__":
    test_add_done_stats()
    test_digest_empty_and_populated()
    print("ok")
