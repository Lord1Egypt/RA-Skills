"""mit: upsert -> today_brief -> stats round-trip."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from datetime import date
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


def test_upsert_today_brief_stats():
    with tempfile.TemporaryDirectory() as tmp:
        env = _setup(tmp)
        today = date.today().isoformat()
        subprocess.check_call(
            [sys.executable, str(SCRIPTS / "log.py"), "--upsert",
             "--date", today, "--task", "ship v0.1", "--completed", "false"],
            env=env, cwd=REPO_ROOT,
        )
        brief = json.loads(subprocess.check_output(
            [sys.executable, str(SCRIPTS / "today_brief.py")], env=env, cwd=REPO_ROOT))
        assert brief["task"] == "ship v0.1"
        assert brief["completed"] is False

        # Updating same date overwrites
        subprocess.check_call(
            [sys.executable, str(SCRIPTS / "log.py"), "--upsert",
             "--date", today, "--task", "ship v0.1", "--completed", "true"],
            env=env, cwd=REPO_ROOT,
        )
        stats = json.loads(subprocess.check_output(
            [sys.executable, str(SCRIPTS / "stats.py")], env=env, cwd=REPO_ROOT))
        assert stats["status"] == "ok"
        assert stats["summary"]["today_completed"] is True
        assert stats["summary"]["completed_last_7d"] == 1


if __name__ == "__main__":
    test_upsert_today_brief_stats()
    print("ok")
