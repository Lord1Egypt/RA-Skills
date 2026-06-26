import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "verify-release.py"


def run_verify_release(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_verify_release_script_exists_and_reports_default_plan():
    assert SCRIPT.exists(), "scripts/verify-release.py should exist"

    result = run_verify_release("--dry-run", "--format", "json")
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    assert [step["name"] for step in payload["steps"]] == [
        "cleanup-generated",
        "pytest",
        "report-evals",
        "late-context-evals",
        "doc-sync",
        "export-smoke",
        "cleanup-generated-final",
    ]
    assert any("scripts/clean-generated.py" in step["command"] for step in payload["steps"])
    assert any("python -m pytest -q" in step["command"] for step in payload["steps"])
    assert any("scripts/run-report-evals.py" in step["command"] for step in payload["steps"])
    assert any("scripts/run-late-context-evals.py" in step["command"] for step in payload["steps"])
    assert any("check-doc-sync.py" in step["command"] for step in payload["steps"])
    assert any("scripts/export-image.py" in step["command"] for step in payload["steps"])
    assert "skill-evals" not in [step["name"] for step in payload["steps"]]


def test_verify_release_respects_skip_flags():
    result = run_verify_release(
        "--dry-run",
        "--format",
        "json",
        "--skip-export-smoke",
        "--skip-doc-sync",
        "--skip-late-context-evals",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    assert [step["name"] for step in payload["steps"]] == [
        "cleanup-generated",
        "pytest",
        "report-evals",
        "cleanup-generated-final",
    ]


def test_verify_release_includes_skill_evals_only_when_requested():
    result = run_verify_release(
        "--dry-run",
        "--format",
        "json",
        "--include-skill-evals",
        "--skill-evals-case-id",
        "explicit-generate",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    steps = [step["name"] for step in payload["steps"]]
    assert "skill-evals" in steps
    skill_step = next(step for step in payload["steps"] if step["name"] == "skill-evals")
    assert "scripts/run-skill-evals.py" in skill_step["command"]
    assert "--runner fixture" in skill_step["command"]
    assert "--run-live" not in skill_step["command"]


def test_verify_release_live_skill_evals_require_explicit_flag():
    result = run_verify_release(
        "--dry-run",
        "--format",
        "json",
        "--include-skill-evals",
        "--skill-evals-runner",
        "codex",
        "--skill-evals-run-live",
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    skill_step = next(step for step in payload["steps"] if step["name"] == "skill-evals")
    assert "--runner codex" in skill_step["command"]
    assert "--run-live" in skill_step["command"]


def test_verify_release_rejects_non_fixture_runner_without_trace_or_live_flag():
    result = run_verify_release(
        "--dry-run",
        "--format",
        "json",
        "--include-skill-evals",
        "--skill-evals-runner",
        "codex",
    )

    assert result.returncode != 0
    assert "requires --skill-evals-raw-trace, --skill-evals-normalized-trace, or --skill-evals-run-live" in result.stderr
