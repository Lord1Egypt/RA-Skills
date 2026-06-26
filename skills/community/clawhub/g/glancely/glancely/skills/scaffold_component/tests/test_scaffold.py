"""scaffold_component: end-to-end generation + cleanup."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SCAFFOLD = REPO_ROOT / "glancely" / "skills" / "scaffold_component" / "scripts" / "scaffold.py"


def test_scaffold_generates_and_runs():
    name = "pr_scaffold_test_tmp"
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "components" / name
        env = {**os.environ, "GLANCE_HOME": tmp, "PYTHONPATH": str(REPO_ROOT)}
        try:
            out = subprocess.check_output(
                [
                    sys.executable,
                    str(SCAFFOLD),
                    "--name",
                    name,
                    "--title",
                    "Test",
                    "--field",
                    "count:int",
                    "--field",
                    "note:text",
                ],
                env=env,
                cwd=REPO_ROOT,
            )
            result = json.loads(out)
            assert result["ok"] is True
            assert "001_init.sql" in result["migrations_applied"]
            assert target.is_dir()

            # Generated log.py works
            log_out = subprocess.check_output(
                [
                    sys.executable,
                    str(target / "scripts" / "log.py"),
                    "--count",
                    "3",
                    "--note",
                    "hi",
                ],
                env=env,
                cwd=REPO_ROOT,
            )
            assert json.loads(log_out)["ok"] is True

            # Generated stats.py works
            stats_out = subprocess.check_output(
                [sys.executable, str(target / "scripts" / "stats.py")],
                env=env,
                cwd=REPO_ROOT,
            )
            stats = json.loads(stats_out)
            assert stats["status"] == "ok"
            assert stats["summary"]["total"] == 1
        finally:
            if target.exists():
                shutil.rmtree(target)


if __name__ == "__main__":
    test_scaffold_generates_and_runs()
    print("ok")
