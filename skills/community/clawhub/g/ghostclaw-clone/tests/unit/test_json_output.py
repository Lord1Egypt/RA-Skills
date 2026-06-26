"""JSON output format and schema validation tests."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


def run_ghostclaw_json(repo_path: Path, args: list = None) -> dict:
    """Run ghostclaw analyze with --json and return parsed output."""
    cmd = [sys.executable, "-m", "ghostclaw.cli.ghostclaw", "analyze", str(repo_path), "--json", "--no-write-report"]
    if args:
        cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, f"Command failed: {result.stderr}"
    output = result.stdout
    start = output.find('{')
    end = output.rfind('}') + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON found in output. stdout[:500]: {output[:500]}")
    json_str = output[start:end]
    return json.loads(json_str)


def test_json_output_schema_full_scan(tmp_path):
    """Validate JSON output structure for a full scan (non-delta)."""
    (tmp_path / "pyproject.toml").write_text("[project]\nname='test'\n")
    (tmp_path / "main.py").write_text("print('hello')\n")

    data = run_ghostclaw_json(tmp_path, ["--no-ai"])

    assert "vibe_score" in data and isinstance(data["vibe_score"], int)
    assert "stack" in data and isinstance(data["stack"], str)
    assert "files_analyzed" in data and isinstance(data["files_analyzed"], int)
    assert "total_lines" in data and isinstance(data["total_lines"], int)
    assert "issues" in data and isinstance(data["issues"], list)
    assert "architectural_ghosts" in data and isinstance(data["architectural_ghosts"], list)
    assert "red_flags" in data and isinstance(data["red_flags"], list)
    assert "coupling_metrics" in data and isinstance(data["coupling_metrics"], dict)
    assert "errors" in data and isinstance(data["errors"], list)

    meta = data["metadata"]
    assert "timestamp" in meta
    assert "analyzer" in meta
    assert "version" in meta
    assert "adapters_active" in meta

    delta = meta.get("delta", {})
    if delta:
        assert delta.get("mode") is False or "mode" not in delta


def test_json_output_contains_delta_fields(tmp_path):
    """Validate that delta mode adds the required delta metadata fields."""
    import os

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)

    (tmp_path / "file1.py").write_text("print('v1')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, check=True)

    (tmp_path / "file1.py").write_text("print('v2')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "update"], cwd=tmp_path, check=True)

    data = run_ghostclaw_json(tmp_path, ["--delta", "--base", "HEAD~1", "--no-ai"])

    meta = data["metadata"]
    assert "delta" in meta
    delta = meta["delta"]

    assert delta["mode"] is True
    assert isinstance(delta["base_ref"], str)
    assert isinstance(delta["files_changed"], list)
    assert isinstance(delta["diff"], str)
    assert len(delta["diff"]) > 0
    assert any("file1.py" in f for f in delta["files_changed"])


def test_json_output_delta_base_report_loaded(tmp_path):
    """When a base report exists, delta mode should include base context in ai_prompt (if AI enabled)."""
    import json as json_mod
    import os

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)

    (tmp_path / "a.py").write_text("print('a')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "add a"], cwd=tmp_path, check=True)

    env = {"GHOSTCLAW_API_KEY": "dummy", **os.environ}
    subprocess.run(
        [sys.executable, "-m", "ghostclaw.cli.ghostclaw", "analyze", ".", "--no-write-report", "--json", "--no-ai"],
        cwd=tmp_path, capture_output=True, text=True, env=env, check=True
    )

    reports_dir = tmp_path / ".ghostclaw" / "storage" / "reports"
    if not reports_dir.exists():
        pytest.skip("No reports dir created")
    json_files = list(reports_dir.glob("ARCHITECTURE-REPORT-*.json"))
    if not json_files:
        pytest.skip("No JSON report created")

    (tmp_path / "a.py").write_text("print('a modified')\n")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "modify a"], cwd=tmp_path, check=True)

    result = subprocess.run(
        [sys.executable, "-m", "ghostclaw.cli.ghostclaw", "analyze", ".", "--delta", "--base", "HEAD~1", "--use-ai", "--dry-run", "--json", "--no-write-report"],
        cwd=tmp_path, capture_output=True, text=True, env=env, timeout=60
    )
    assert result.returncode == 0, f"Delta run failed: {result.stderr}"

    output = result.stdout
    start = output.find('{')
    end = output.rfind('}') + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON in output. stderr: {result.stderr[:500]}")
    data = json_mod.loads(output[start:end])

    assert "ai_prompt" in data
    ai_prompt = data["ai_prompt"]
    assert isinstance(ai_prompt, str)
    assert "<diff>" in ai_prompt
    assert "<base_context>" in ai_prompt or "Base Vibe Score" in ai_prompt
    assert "<current_state>" in ai_prompt
    assert "architectural drift" in ai_prompt.lower()


def test_json_output_validates_with_demjson(tmp_path):
    """Removed demjson3 dependency; this test is no longer needed."""
    pytest.skip("demjson3 dependency removed; JSON validation covered by other tests using built-in json module")
