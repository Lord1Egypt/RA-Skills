from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


SKILL_DIR = Path(__file__).resolve().parents[1]
SNAPSHOT = SKILL_DIR / "scripts" / "audit_snapshot.py"
PACKET = SKILL_DIR / "scripts" / "build_audit_packet.py"
DETECT = SKILL_DIR / "scripts" / "detect_review_models.py"
RUN_EVALS = SKILL_DIR / "scripts" / "run_evals.py"


def run_script(
    script: Path,
    *args: str,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
):
    merged_env = os.environ.copy()
    merged_env["PYTHONDONTWRITEBYTECODE"] = "1"
    if env:
        merged_env.update(env)
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        cwd=cwd,
        env=merged_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )


def git_available() -> bool:
    return shutil.which("git") is not None


def test_snapshot_prunes_skipped_directories(tmp_path: Path) -> None:
    (tmp_path / "node_modules" / "pkg").mkdir(parents=True)
    (tmp_path / "node_modules" / "pkg" / "server.js").write_text("ignored", encoding="utf-8")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "server.py").write_text("print('ok')", encoding="utf-8")

    result = run_script(SNAPSHOT, "--root", str(tmp_path), "--json")
    payload = json.loads(result.stdout)

    assert payload["file_count_seen"] == 1
    assert payload["high_risk_paths_sample"] == ["src/server.py"]


def test_snapshot_auditignore_patterns(tmp_path: Path) -> None:
    (tmp_path / ".auditignore").write_text("ignored/\n*.secret\n", encoding="utf-8")
    (tmp_path / "ignored").mkdir()
    (tmp_path / "ignored" / "auth.py").write_text("ignored", encoding="utf-8")
    (tmp_path / "visible.secret").write_text("ignored", encoding="utf-8")
    (tmp_path / "api.py").write_text("visible", encoding="utf-8")

    result = run_script(SNAPSHOT, "--root", str(tmp_path), "--json")
    payload = json.loads(result.stdout)

    assert payload["file_count_seen"] == 2  # .auditignore plus api.py
    assert "api.py" in payload["high_risk_paths_sample"]
    assert "ignored/auth.py" not in payload["high_risk_paths_sample"]
    assert "visible.secret" not in payload["high_risk_paths_sample"]


def test_build_packet_absolute_path_no_git_repo(tmp_path: Path) -> None:
    result = run_script(
        PACKET,
        "--root",
        str(tmp_path),
        "--mode",
        "standard",
        "--scope",
        "repo",
        env={"GIT_CEILING_DIRECTORIES": str(tmp_path.parent)},
    )

    assert "# Code Audit Packet" in result.stdout
    assert "Branch: `unknown`" in result.stdout
    assert "Diff Body" in result.stdout


def test_build_packet_default_does_not_emit_secret_from_diff(tmp_path: Path) -> None:
    if not git_available():
        return
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    secret_file = tmp_path / "secret.txt"
    secret_file.write_text("token=SECRET_VALUE\n", encoding="utf-8")
    subprocess.run(["git", "add", "secret.txt"], cwd=tmp_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(
        ["git", "-c", "user.email=test@example.com", "-c", "user.name=Test", "commit", "-m", "init"],
        cwd=tmp_path,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    secret_file.write_text("token=SECRET_VALUE_CHANGED\n", encoding="utf-8")

    result = run_script(PACKET, "--root", str(tmp_path), "--mode", "security", "--scope", "diff")

    assert "SECRET_VALUE_CHANGED" not in result.stdout
    assert "Not included. Re-run with `--include-diff`" in result.stdout


def test_detect_review_models_custom_config(tmp_path: Path) -> None:
    config = tmp_path / "routes.json"
    config.write_text(
        json.dumps(
            {
                "routes": [
                    {
                        "name": "deepseek-v4-pro",
                        "kind": "api",
                        "env": ["DEEPSEEK_TEST_KEY"],
                        "model": "deepseek-v4-pro",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = run_script(DETECT, "--config", str(config), env={"DEEPSEEK_TEST_KEY": "present"})
    payload = json.loads(result.stdout)

    assert "deepseek-v4-pro" in payload["available_review_routes"]


def test_run_evals_schema() -> None:
    result = run_script(RUN_EVALS)
    payload = json.loads(result.stdout)

    assert payload["passed"] is True
    assert payload["eval_count"] >= 4
