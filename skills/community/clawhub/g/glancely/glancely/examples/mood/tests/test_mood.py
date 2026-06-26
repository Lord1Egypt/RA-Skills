"""mood: log -> stats round-trip."""

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


def _run(cmd, env):
    return subprocess.check_output(cmd, env=env, cwd=REPO_ROOT)


def test_log_then_stats():
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GLANCE_HOME": tmp, "PYTHONPATH": str(REPO_ROOT)}
        subprocess.check_call(
            [sys.executable, "-m", "glancely.core.storage.migrations",
             str(COMPONENT_DIR)],
            env=env, cwd=REPO_ROOT,
        )
        out = _run([sys.executable, str(SCRIPTS / "log.py"),
                    "--raw", "feeling fine", "--score", "7", "--label", "calm"], env)
        assert json.loads(out)["ok"] is True

        stats = json.loads(_run([sys.executable, str(SCRIPTS / "stats.py")], env))
        assert stats["status"] == "ok"
        assert stats["summary"]["total"] == 1
        assert stats["summary"]["last_label"] == "calm"


def test_stats_empty():
    with tempfile.TemporaryDirectory() as tmp:
        env = {**os.environ, "GLANCE_HOME": tmp, "PYTHONPATH": str(REPO_ROOT)}
        subprocess.check_call(
            [sys.executable, "-m", "glancely.core.storage.migrations",
             str(COMPONENT_DIR)],
            env=env, cwd=REPO_ROOT,
        )
        stats = json.loads(_run([sys.executable, str(SCRIPTS / "stats.py")], env))
        assert stats["status"] == "empty"


if __name__ == "__main__":
    test_log_then_stats()
    test_stats_empty()
    print("ok")
