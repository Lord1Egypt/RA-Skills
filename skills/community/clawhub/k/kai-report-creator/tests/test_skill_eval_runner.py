import json
import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run-skill-evals.py"
FIXTURES = ROOT / "tests" / "fixtures" / "skill-evals"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("run_skill_evals", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_prompt_manifest_paths_exist():
    manifest = ROOT / "evals" / "report-skill-prompts.csv"
    assert manifest.exists()
    for line in manifest.read_text(encoding="utf-8").splitlines()[1:]:
        fields = line.split(",")
        assert (ROOT / fields[3]).is_file(), fields[3]


def test_fixture_runner_scores_all_cases_with_four_categories(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] == 6
    assert payload["summary"]["passed"] == 6
    assert payload["summary"]["failed"] == 0
    assert payload["summary"]["average_score"] >= 93
    for category in ["outcome", "process", "style", "efficiency"]:
        assert category in payload["summary"]["average_category_scores"]
        assert payload["summary"]["average_category_scores"][category] > 0


def test_fixture_runner_scores_success_case_and_style_fixture(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "explicit-generate",
        "--normalized-trace",
        str(FIXTURES / "explicit-generate-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["scores"] == {
        "outcome": 25,
        "process": 25,
        "style": 25,
        "efficiency": 25,
    }
    assert case["total_score"] == 100
    assert case["passed"] is True
    assert case["eval_complete"] is True
    assert case["style_rubric"]["source"] == "fixture"
    assert case["style_rubric"]["score"] >= 90
    assert case["metrics"]["runner"] == "fixture"
    assert len(case["metrics"]["shell_commands"]) == 2
    assert case["metrics"]["input_tokens"] == 12000
    assert case["metrics"]["output_tokens"] == 3400
    assert "style.rubric_missing" not in case["failures"]


def test_positive_case_without_style_rubric_is_eval_incomplete(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "explicit-generate",
        "--normalized-trace",
        str(FIXTURES / "explicit-generate-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--disable-fixture-style-rubric",
        "--format",
        "json",
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["scores"]["style"] == 15
    assert case["total_score"] == 90
    assert case["passed"] is False
    assert case["eval_complete"] is False
    assert "style.rubric_missing" in case["failures"]
    assert "eval.style_rubric_missing" in case["failures"]


def test_negative_case_allows_skill_contract_read_for_routing(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "negative-slide-deck",
        "--normalized-trace",
        str(FIXTURES / "negative-slide-deck-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["scores"] == {
        "outcome": 25,
        "process": 25,
        "style": 25,
        "efficiency": 25,
    }
    assert case["total_score"] == 100
    assert case["passed"] is True


def test_outcome_hard_gate_prevents_clean_process_from_passing(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "explicit-generate",
        "--normalized-trace",
        str(FIXTURES / "thrashy-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["passed"] is False
    assert case["scores"]["outcome"] == 0
    assert "outcome.missing_html_artifact" in case["failures"]
    assert "efficiency.repeated_failed_command" in case["failures"]


def test_codex_raw_trace_normalizes_real_command_events(tmp_path: Path):
    result = run_script(
        "--runner",
        "codex",
        "--case-id",
        "negative-slide-deck",
        "--raw-trace",
        str(FIXTURES / "real-codex-tool-smoke.jsonl"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["metrics"]["runner"] == "codex"
    assert case["metrics"]["shell_commands"] == ["/bin/zsh -lc pwd"]
    assert case["metrics"]["input_tokens"] == 38572
    assert case["metrics"]["output_tokens"] == 384
    assert "codex.event_error" in case["metrics"]["runner_warnings"][0]


def test_codex_rg_no_match_is_not_counted_as_failed_shell_command(tmp_path: Path):
    result = run_script(
        "--runner",
        "codex",
        "--case-id",
        "negative-slide-deck",
        "--raw-trace",
        str(FIXTURES / "real-codex-rg-no-match.jsonl"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["metrics"]["failed_shell_commands"] == []
    assert case["scores"]["efficiency"] == 25


def test_codex_live_runner_closes_stdin(monkeypatch, tmp_path: Path):
    module = load_runner_module()
    captured_kwargs = {}
    captured_command = []

    def fake_run(command, **kwargs):
        captured_command.extend(command)
        captured_kwargs.update(kwargs)
        stdout = '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module.run_codex_live(
        ROOT,
        {"prompt_path": "evals/skill-prompts/negative-slide-deck.md"},
        tmp_path / "trace.raw.jsonl",
        tmp_path / "artifacts",
    )

    assert captured_command[-1] == "-"
    assert "帮我做一个 8 页 PPT" in captured_kwargs["input"]


def test_codex_live_timeout_returns_warning(monkeypatch, tmp_path: Path):
    module = load_runner_module()

    def fake_run(command, **kwargs):
        partial = "\n".join(
            [
                '{"type":"item.completed","item":{"type":"command_execution","command":"/bin/zsh -lc pwd","exit_code":0,"status":"completed"}}',
                '{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":2}}',
            ]
        )
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output=partial, stderr="too slow")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    metrics = module.run_codex_live(
        ROOT,
        {
            "prompt_path": "evals/skill-prompts/negative-slide-deck.md",
            "max_wall_ms": "120000",
        },
        tmp_path / "trace.raw.jsonl",
        tmp_path / "artifacts",
    )

    assert metrics.runner_warnings[0] == "codex.timeout:120.0s"
    assert metrics.run_completed is False
    assert metrics.shell_commands == ["/bin/zsh -lc pwd"]
    assert metrics.input_tokens == 10
    assert metrics.wall_ms >= 0


def test_incomplete_run_cannot_pass_negative_case(tmp_path: Path):
    trace = tmp_path / "timeout-normalized.json"
    trace.write_text(
        json.dumps(
            {
                "runner": "codex",
                "trace_format_version": "normalized-v1",
                "tool_calls": [],
                "shell_commands": [],
                "failed_shell_commands": [],
                "read_paths": [],
                "write_paths": [],
                "artifact_paths": [],
                "input_tokens": None,
                "output_tokens": None,
                "wall_ms": 120000,
                "run_completed": False,
                "skill_evidence": {
                    "skill_contract_read": False,
                    "report_flow_observed": False,
                    "guard_observed": False,
                    "html_quality_gate_observed": False,
                },
                "runner_warnings": ["codex.timeout:120.0s"],
            }
        ),
        encoding="utf-8",
    )

    result = run_script(
        "--runner",
        "codex",
        "--case-id",
        "negative-slide-deck",
        "--normalized-trace",
        str(trace),
        "--artifact-dir",
        str(tmp_path / "artifacts"),
        "--format",
        "json",
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    case = payload["cases"][0]
    assert case["passed"] is False
    assert "runner.run_incomplete" in case["failures"]


def test_codex_live_runner_replaces_artifact_dir_placeholder(monkeypatch, tmp_path: Path):
    module = load_runner_module()
    root = tmp_path / "repo"
    root.mkdir()
    (root / "prompt.md").write_text("Save under {artifact_dir}.", encoding="utf-8")
    captured_kwargs = {}

    def fake_run(command, **kwargs):
        captured_kwargs.update(kwargs)
        stdout = '{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n'
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module.run_codex_live(
        root,
        {"prompt_path": "prompt.md"},
        tmp_path / "trace.raw.jsonl",
        root / "artifacts" / "case",
    )

    assert "{artifact_dir}" not in captured_kwargs["input"]
    assert "Save under `artifacts/case`." in captured_kwargs["input"]
