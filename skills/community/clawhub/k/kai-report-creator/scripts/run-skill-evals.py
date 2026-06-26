#!/usr/bin/env python3
"""Run captured-run skill evals for kai-report-creator."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class NormalizedTraceMetrics:
    runner: str
    trace_format_version: str
    tool_calls: list[dict[str, Any]]
    shell_commands: list[str]
    failed_shell_commands: list[str]
    read_paths: list[str]
    write_paths: list[str]
    artifact_paths: list[str]
    input_tokens: int | None
    output_tokens: int | None
    wall_ms: int
    run_completed: bool
    skill_evidence: dict[str, bool]
    runner_warnings: list[str]


@dataclass(frozen=True)
class SkillEvalCase:
    case_id: str
    total_score: int
    passed: bool
    eval_complete: bool
    scores: dict[str, int]
    failures: list[str]
    style_rubric: dict[str, Any] | None
    metrics: dict[str, Any]
    artifact_dir: str


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        events.append(json.loads(line))
    return events


def bool_field(row: dict[str, str], key: str) -> bool:
    return row[key].strip().lower() == "true"


def int_field(row: dict[str, str], key: str, default: int) -> int:
    value = row.get(key, "").strip()
    return int(value) if value else default


def _suffix_match(paths: list[str], suffix: str) -> bool:
    normalized_suffix = suffix.replace("\\", "/").lstrip("./")
    return any(path.replace("\\", "/").lstrip("./").endswith(normalized_suffix) for path in paths)


def _contains_any(values: list[str], needles: list[str]) -> bool:
    haystack = "\n".join(values)
    return any(needle in haystack for needle in needles)


def _infer_paths_from_command(command: str) -> list[str]:
    return re.findall(r"(?:SKILL\.md|references/[^\s'\";]+\.md|scripts/[^\s'\";]+\.py)", command)


def _is_failed_shell_command(command: str, exit_code: Any) -> bool:
    if exit_code in (None, 0):
        return False
    # `rg` returns 1 for no matches. In this harness it is commonly used as a
    # negative assertion for forbidden output patterns, so do not treat it as
    # thrashing unless the command failed with a harder error code.
    if exit_code == 1 and re.search(r"(^|[\s'\"])(rg|ripgrep)(\s|$)", command):
        return False
    return True


def _infer_skill_evidence(
    read_paths: list[str],
    write_paths: list[str],
    artifact_paths: list[str],
    commands: list[str],
) -> dict[str, bool]:
    skill_contract_read = _suffix_match(read_paths, "SKILL.md") or _contains_any(commands, ["SKILL.md"])
    guard_observed = _contains_any(commands, ["scripts/guard_validate.py", "guard_validate.py"])
    html_quality_gate_observed = _contains_any(commands, ["scripts/html_quality_gate.py", "html_quality_gate.py"])
    report_flow_observed = (
        guard_observed
        or html_quality_gate_observed
        or any(path.endswith(".html") for path in write_paths)
        or any(path.endswith(".html") for path in artifact_paths)
    )
    return {
        "skill_contract_read": skill_contract_read,
        "report_flow_observed": report_flow_observed,
        "guard_observed": guard_observed,
        "html_quality_gate_observed": html_quality_gate_observed,
    }


def load_normalized_trace(path: Path) -> NormalizedTraceMetrics:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return NormalizedTraceMetrics(
        runner=str(payload.get("runner") or "fixture"),
        trace_format_version=str(payload.get("trace_format_version") or "normalized-v1"),
        tool_calls=list(payload.get("tool_calls") or []),
        shell_commands=list(payload.get("shell_commands") or []),
        failed_shell_commands=list(payload.get("failed_shell_commands") or []),
        read_paths=list(payload.get("read_paths") or []),
        write_paths=list(payload.get("write_paths") or []),
        artifact_paths=list(payload.get("artifact_paths") or []),
        input_tokens=payload.get("input_tokens"),
        output_tokens=payload.get("output_tokens"),
        wall_ms=int(payload.get("wall_ms") or 0),
        run_completed=bool(payload.get("run_completed", True)),
        skill_evidence=dict(payload.get("skill_evidence") or {}),
        runner_warnings=list(payload.get("runner_warnings") or []),
    )


def normalize_codex_events(events: list[dict[str, Any]], wall_ms: int = 0) -> NormalizedTraceMetrics:
    shell_commands: list[str] = []
    failed_shell_commands: list[str] = []
    read_paths: list[str] = []
    write_paths: list[str] = []
    tool_calls: list[dict[str, Any]] = []
    runner_warnings: list[str] = []
    input_tokens: int | None = None
    output_tokens: int | None = None

    for event in events:
        usage = event.get("usage")
        if isinstance(usage, dict):
            if usage.get("input_tokens") is not None:
                input_tokens = int(usage["input_tokens"])
            if usage.get("output_tokens") is not None:
                output_tokens = int(usage["output_tokens"])

        item = event.get("item")
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "error":
            message = str(item.get("message") or "")
            runner_warnings.append(f"codex.event_error:{message[:120]}")
            continue
        if item_type == "command_execution":
            command = str(item.get("command") or "")
            if event.get("type") == "item.completed" and command:
                shell_commands.append(command)
                read_paths.extend(_infer_paths_from_command(command))
                exit_code = item.get("exit_code")
                if _is_failed_shell_command(command, exit_code):
                    failed_shell_commands.append(command)
            tool_calls.append(
                {
                    "type": "command_execution",
                    "command": command,
                    "exit_code": item.get("exit_code"),
                    "status": item.get("status"),
                }
            )
            continue
        if item_type == "file_read":
            path = str(item.get("path") or "")
            if path:
                read_paths.append(path)
        elif item_type == "file_write":
            path = str(item.get("path") or "")
            if path:
                write_paths.append(path)

    artifact_paths = [path for path in write_paths if path.endswith(".html")]
    skill_evidence = _infer_skill_evidence(read_paths, write_paths, artifact_paths, shell_commands)
    return NormalizedTraceMetrics(
        runner="codex",
        trace_format_version="codex-jsonl-v1",
        tool_calls=tool_calls,
        shell_commands=shell_commands,
        failed_shell_commands=failed_shell_commands,
        read_paths=sorted(set(read_paths)),
        write_paths=write_paths,
        artifact_paths=artifact_paths,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        wall_ms=wall_ms,
        run_completed=True,
        skill_evidence=skill_evidence,
        runner_warnings=runner_warnings,
    )


def _resolve_existing_path(root: Path, path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else root / path


def _normalize_partial_codex_output(raw_trace_path: Path, output: Any, wall_ms: int) -> NormalizedTraceMetrics:
    raw_trace_path.write_text(_subprocess_text(output), encoding="utf-8")
    try:
        metrics = normalize_codex_events(read_jsonl(raw_trace_path), wall_ms=wall_ms)
    except json.JSONDecodeError as exc:
        return NormalizedTraceMetrics(
            runner="codex",
            trace_format_version="codex-jsonl-v1",
            tool_calls=[],
            shell_commands=[],
            failed_shell_commands=[],
            read_paths=[],
            write_paths=[],
            artifact_paths=[],
            input_tokens=None,
            output_tokens=None,
            wall_ms=wall_ms,
            run_completed=False,
            skill_evidence=_infer_skill_evidence([], [], [], []),
            runner_warnings=[f"codex.partial_trace_decode_error:{str(exc)[:120]}"],
        )
    return NormalizedTraceMetrics(**(asdict(metrics) | {"run_completed": False}))


def _subprocess_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def html_files_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> list[Path]:
    candidates: list[Path] = []
    candidates.extend(sorted(artifact_dir.rglob("*.html")) if artifact_dir.exists() else [])
    for path_text in metrics.artifact_paths + metrics.write_paths:
        if not path_text.endswith(".html"):
            continue
        path = _resolve_existing_path(root, path_text)
        if path.exists() and path not in candidates:
            candidates.append(path)
    return candidates


def html_text_for_case(root: Path, metrics: NormalizedTraceMetrics, artifact_dir: Path) -> str:
    html_files = html_files_for_case(root, metrics, artifact_dir)
    if not html_files:
        return ""
    return html_files[0].read_text(encoding="utf-8", errors="replace")


def _display_path(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def default_style_rubric_fixture(root: Path, case_id: str) -> Path:
    return root / "tests" / "fixtures" / "skill-evals" / f"{case_id}-style-rubric.json"


def _validate_style_rubric(rubric: dict[str, Any], case_id: str) -> list[str]:
    failures: list[str] = []
    required = ["case_id", "overall_pass", "score", "checks", "summary"]
    for key in required:
        if key not in rubric:
            failures.append(f"style.rubric_missing_{key}")

    if rubric.get("case_id") != case_id:
        failures.append("style.rubric_case_mismatch")
    score = rubric.get("score")
    if not isinstance(score, int) or score < 0 or score > 100:
        failures.append("style.rubric_score_invalid")
    if not isinstance(rubric.get("overall_pass"), bool):
        failures.append("style.rubric_overall_pass_invalid")
    checks = rubric.get("checks")
    if not isinstance(checks, list) or len(checks) < 4:
        failures.append("style.rubric_checks_invalid")
    elif any(
        not isinstance(check, dict)
        or not isinstance(check.get("id"), str)
        or not isinstance(check.get("pass"), bool)
        or not isinstance(check.get("score"), int)
        or not 1 <= check.get("score", 0) <= 5
        or not isinstance(check.get("notes"), str)
        or not check.get("notes", "").strip()
        for check in checks
    ):
        failures.append("style.rubric_check_invalid")
    if not isinstance(rubric.get("summary"), str) or not rubric.get("summary", "").strip():
        failures.append("style.rubric_summary_invalid")
    return failures


def style_rubric_path_for_case(
    root: Path,
    case_id: str,
    artifact_dir: Path,
    allow_fixture_style_rubric: bool,
) -> tuple[Path | None, str | None]:
    artifact_path = artifact_dir / "style-rubric.json"
    if artifact_path.exists():
        return artifact_path, "artifact"
    fixture_path = default_style_rubric_fixture(root, case_id)
    if allow_fixture_style_rubric and fixture_path.exists():
        return fixture_path, "fixture"
    return None, None


def score_outcome(
    root: Path,
    row: dict[str, str],
    metrics: NormalizedTraceMetrics,
    artifact_dir: Path,
) -> tuple[int, list[str]]:
    failures: list[str] = []
    should_trigger = bool_field(row, "should_trigger")
    html_files = html_files_for_case(root, metrics, artifact_dir)

    if not should_trigger:
        if html_files or any(path.endswith(".html") for path in metrics.write_paths):
            return 0, ["outcome.negative_case_generated_report"]
        return 25, []

    if not html_files:
        return 0, ["outcome.missing_html_artifact"]

    score = 10
    html_text = html_files[0].read_text(encoding="utf-8", errors="replace")
    if metrics.skill_evidence.get("html_quality_gate_observed"):
        score += 5
    else:
        failures.append("outcome.html_quality_gate_not_observed")
    if 'id="report-summary"' in html_text:
        score += 5
    else:
        failures.append("outcome.report_summary_missing")
    if ":::" not in html_text and "<title>" in html_text:
        score += 5
    else:
        failures.append("outcome.render_integrity_markers_failed")
    return score, failures


def score_process(row: dict[str, str], metrics: NormalizedTraceMetrics) -> tuple[int, list[str]]:
    failures: list[str] = []
    should_trigger = bool_field(row, "should_trigger")
    if not should_trigger:
        used_report_flow = (
            metrics.skill_evidence.get("report_flow_observed")
            or metrics.skill_evidence.get("guard_observed")
            or metrics.skill_evidence.get("html_quality_gate_observed")
        )
        if used_report_flow:
            return 0, ["process.negative_case_used_report_generation_flow"]
        return 25, []

    score = 0
    if metrics.skill_evidence.get("skill_contract_read") or _suffix_match(metrics.read_paths, "SKILL.md"):
        score += 5
    else:
        failures.append("process.skill_contract_not_observed")

    route_refs = ["references/spec-loading-matrix.md", "references/generate-flow.md"]
    if any(_suffix_match(metrics.read_paths, ref) for ref in route_refs):
        score += 5
    else:
        failures.append("process.route_references_not_observed")

    if metrics.skill_evidence.get("report_flow_observed"):
        score += 5
    else:
        failures.append("process.report_flow_not_observed")

    if metrics.skill_evidence.get("guard_observed"):
        score += 5
    else:
        failures.append("process.guard_not_observed")

    if metrics.skill_evidence.get("html_quality_gate_observed"):
        score += 5
    else:
        failures.append("process.html_quality_gate_not_observed")

    return score, failures


def score_style(
    root: Path,
    row: dict[str, str],
    metrics: NormalizedTraceMetrics,
    artifact_dir: Path,
    allow_fixture_style_rubric: bool,
) -> tuple[int, list[str], dict[str, Any] | None]:
    failures: list[str] = []
    if not bool_field(row, "should_trigger"):
        return 25, [], None

    html_text = html_text_for_case(root, metrics, artifact_dir)
    if not html_text:
        return 0, ["style.missing_html_artifact"], None

    score = 0
    expected_theme = row.get("expected_theme", "").strip()
    if expected_theme and f'data-theme="{expected_theme}"' in html_text:
        score += 5
    elif expected_theme:
        failures.append("style.expected_theme_not_found")

    if 'id="report-summary"' in html_text:
        score += 5
    else:
        failures.append("style.report_summary_missing")

    generic_markers = ["Lorem ipsum", "TODO", "Untitled", "Your title here"]
    if ":::" not in html_text and not any(marker in html_text for marker in generic_markers):
        score += 5
    else:
        failures.append("style.raw_ir_or_placeholder_text")

    style_rubric = None
    rubric_path, rubric_source = style_rubric_path_for_case(
        root,
        row["id"],
        artifact_dir,
        allow_fixture_style_rubric,
    )
    if rubric_path is not None and rubric_source is not None:
        rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
        rubric_failures = _validate_style_rubric(rubric, row["id"])
        if rubric_failures:
            failures.extend(rubric_failures)
            failures.append("eval.style_rubric_invalid")
        else:
            score += round(int(rubric.get("score", 0)) * 10 / 100)
        style_rubric = {
            "source": rubric_source,
            "path": _display_path(root, rubric_path),
            "score": int(rubric.get("score", 0)) if isinstance(rubric.get("score"), int) else None,
            "overall_pass": bool(rubric.get("overall_pass")),
        }
        if not rubric.get("overall_pass"):
            failures.append("style.rubric_needs_work")
    else:
        failures.append("style.rubric_missing")
        failures.append("eval.style_rubric_missing")

    return min(score, 25), failures, style_rubric


def score_efficiency(row: dict[str, str], metrics: NormalizedTraceMetrics) -> tuple[int, list[str]]:
    failures: list[str] = []
    score = 25
    max_shell_commands = int_field(row, "max_shell_commands", 12)
    max_input_tokens = int_field(row, "max_input_tokens", 90000)
    max_output_tokens = int_field(row, "max_output_tokens", 25000)
    max_wall_ms = int_field(row, "max_wall_ms", 240000)

    if len(metrics.shell_commands) > max_shell_commands:
        score -= 5
        failures.append("efficiency.shell_command_count_over_budget")

    failed_counts = Counter(metrics.failed_shell_commands)
    repeated_failed = sum(count - 1 for count in failed_counts.values() if count > 1)
    if metrics.failed_shell_commands:
        score -= 5
        failures.append("efficiency.failed_shell_command")
    if repeated_failed:
        score -= 10
        failures.append("efficiency.repeated_failed_command")

    if metrics.input_tokens is not None and metrics.input_tokens > max_input_tokens:
        score -= 5
        failures.append("efficiency.input_tokens_over_budget")
    if metrics.output_tokens is not None and metrics.output_tokens > max_output_tokens:
        score -= 5
        failures.append("efficiency.output_tokens_over_budget")
    if metrics.wall_ms > max_wall_ms:
        score -= 3
        failures.append("efficiency.wall_time_over_budget")

    return max(score, 0), failures


def default_normalized_fixture(root: Path, case_id: str) -> Path:
    return root / "tests" / "fixtures" / "skill-evals" / f"{case_id}-normalized.json"


def render_live_eval_prompt(root: Path, row: dict[str, str], artifact_dir: Path) -> str:
    prompt_text = (root / row["prompt_path"]).read_text(encoding="utf-8")
    relative_artifact_dir = artifact_dir.relative_to(root) if artifact_dir.is_relative_to(root) else artifact_dir
    prompt_text = prompt_text.replace("{artifact_dir}", f"`{relative_artifact_dir}`")
    return (
        "You are running a development eval for the local kai-report-creator skill.\n"
        "Before deciding or generating, read `SKILL.md` and follow it as the source of truth.\n"
        "Keep the run efficient: load only references that materially help this case, avoid broad repo searches, and do not inspect existing reports unless the skill explicitly requires it.\n\n"
        + prompt_text
        + "\n\nEval harness constraints:\n"
        + f"- Save any report artifacts exactly under `{relative_artifact_dir}`.\n"
        + "- If this request belongs to another skill, do not generate a report artifact.\n"
        + "- Run the relevant guard or HTML quality checks if you generate HTML.\n"
    )


def run_codex_live(root: Path, row: dict[str, str], raw_trace_path: Path, artifact_dir: Path) -> NormalizedTraceMetrics:
    eval_prompt = render_live_eval_prompt(root, row, artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    command = [
        "codex",
        "exec",
        "--json",
        "--cd",
        str(root),
        "--sandbox",
        "workspace-write",
        "--ephemeral",
        "-",
    ]
    timeout_seconds = int_field(row, "max_wall_ms", 240000) / 1000
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            input=eval_prompt,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        wall_ms = round((time.perf_counter() - started) * 1000)
        metrics = _normalize_partial_codex_output(raw_trace_path, exc.output, wall_ms)
        stderr = _subprocess_text(exc.stderr).strip()
        warnings = list(metrics.runner_warnings)
        warnings.insert(0, f"codex.timeout:{timeout_seconds:.1f}s")
        if stderr:
            warnings.append(f"codex.stderr:{stderr[:160]}")
        return NormalizedTraceMetrics(**(asdict(metrics) | {"runner_warnings": warnings}))
    wall_ms = round((time.perf_counter() - started) * 1000)
    raw_trace_path.write_text(completed.stdout, encoding="utf-8")
    events = read_jsonl(raw_trace_path)
    metrics = normalize_codex_events(events, wall_ms=wall_ms)
    warnings = list(metrics.runner_warnings)
    if completed.returncode != 0:
        warnings.append(f"codex.returncode:{completed.returncode}")
    if completed.stderr.strip():
        warnings.append(f"codex.stderr:{completed.stderr.strip()[:160]}")
    return NormalizedTraceMetrics(
        **(asdict(metrics) | {"run_completed": completed.returncode == 0, "runner_warnings": warnings})
    )


def metrics_for_case(
    root: Path,
    row: dict[str, str],
    runner: str,
    artifact_dir: Path,
    normalized_trace: Path | None,
    raw_trace: Path | None,
    run_live: bool,
) -> NormalizedTraceMetrics:
    case_id = row["id"]
    if normalized_trace is not None:
        return load_normalized_trace(normalized_trace)
    if runner == "fixture":
        return load_normalized_trace(default_normalized_fixture(root, case_id))
    if raw_trace is not None:
        if runner != "codex":
            raise ValueError(f"Raw trace normalization is not implemented for runner {runner!r}")
        return normalize_codex_events(read_jsonl(raw_trace), wall_ms=0)
    if run_live:
        if runner != "codex":
            raise ValueError(f"Live runner {runner!r} has no verified adapter yet")
        raw_target = artifact_dir / "trace.raw.jsonl"
        return run_codex_live(root, row, raw_target, artifact_dir)
    raise ValueError("Use --runner fixture, --normalized-trace, --raw-trace, or --run-live.")


def evaluate_case(
    root: Path,
    row: dict[str, str],
    runner: str,
    artifact_root: Path,
    normalized_trace: Path | None,
    raw_trace: Path | None,
    run_live: bool,
    allow_fixture_style_rubric: bool,
) -> SkillEvalCase:
    case_id = row["id"]
    case_artifact_dir = artifact_root / case_id
    case_artifact_dir.mkdir(parents=True, exist_ok=True)
    metrics = metrics_for_case(root, row, runner, case_artifact_dir, normalized_trace, raw_trace, run_live)

    normalized_path = case_artifact_dir / "trace.normalized.json"
    normalized_path.write_text(json.dumps(asdict(metrics), ensure_ascii=False, indent=2), encoding="utf-8")

    outcome, outcome_failures = score_outcome(root, row, metrics, case_artifact_dir)
    process, process_failures = score_process(row, metrics)
    style, style_failures, style_rubric = score_style(
        root,
        row,
        metrics,
        case_artifact_dir,
        allow_fixture_style_rubric,
    )
    efficiency, efficiency_failures = score_efficiency(row, metrics)
    scores = {
        "outcome": outcome,
        "process": process,
        "style": style,
        "efficiency": efficiency,
    }
    runner_failures = [] if metrics.run_completed else ["runner.run_incomplete"]
    failures = runner_failures + outcome_failures + process_failures + style_failures + efficiency_failures
    total_score = sum(scores.values())
    should_trigger = bool_field(row, "should_trigger")
    outcome_gate = outcome >= 20 if should_trigger else outcome == 25
    eval_complete = metrics.run_completed and not any(failure.startswith("eval.") for failure in failures)
    passed = eval_complete and outcome_gate and total_score >= 75 and not any(
        failure in {
            "outcome.negative_case_generated_report",
            "process.negative_case_used_report_generation_flow",
        }
        for failure in failures
    )

    return SkillEvalCase(
        case_id=case_id,
        total_score=total_score,
        passed=passed,
        eval_complete=eval_complete,
        scores=scores,
        failures=failures,
        style_rubric=style_rubric,
        metrics=asdict(metrics),
        artifact_dir=str(case_artifact_dir),
    )


def selected_rows(rows: list[dict[str, str]], case_id: str | None) -> list[dict[str, str]]:
    if case_id is None:
        return rows
    selected = [row for row in rows if row["id"] == case_id]
    if not selected:
        raise SystemExit(f"No eval case found for {case_id!r}")
    return selected


def build_payload(cases: list[SkillEvalCase]) -> dict[str, Any]:
    categories = ["outcome", "process", "style", "efficiency"]
    return {
        "cases": [asdict(case) for case in cases],
        "summary": {
            "total": len(cases),
            "passed": sum(1 for case in cases if case.passed),
            "failed": sum(1 for case in cases if not case.passed),
            "incomplete": sum(1 for case in cases if not case.eval_complete),
            "average_score": round(sum(case.total_score for case in cases) / len(cases), 2) if cases else 0,
            "average_category_scores": {
                category: round(sum(case.scores[category] for case in cases) / len(cases), 2) if cases else 0
                for category in categories
            },
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--manifest", default="evals/report-skill-prompts.csv")
    parser.add_argument("--runner", choices=["fixture", "codex"], default="fixture")
    parser.add_argument("--case-id", help="Run one case id.")
    parser.add_argument("--normalized-trace", help="Use one normalized trace fixture for selected case(s).")
    parser.add_argument("--raw-trace", help="Normalize and score one raw runner trace for selected case(s).")
    parser.add_argument("--artifact-dir", default="evals/artifacts/current/skill-runs")
    parser.add_argument("--run-live", action="store_true", help="Invoke the selected live runner.")
    parser.add_argument(
        "--disable-fixture-style-rubric",
        action="store_true",
        help="Do not use checked-in style rubric fixtures when scoring fixture runs.",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--json-out", help="Optional JSON output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    manifest = (root / args.manifest).resolve()
    artifact_root = (root / args.artifact_dir).resolve() if not Path(args.artifact_dir).is_absolute() else Path(args.artifact_dir)
    normalized_trace = Path(args.normalized_trace).resolve() if args.normalized_trace else None
    raw_trace = Path(args.raw_trace).resolve() if args.raw_trace else None

    rows = selected_rows(load_manifest(manifest), args.case_id)
    if (normalized_trace or raw_trace) and len(rows) != 1:
        raise SystemExit("--normalized-trace and --raw-trace require --case-id to select exactly one case")

    cases = [
        evaluate_case(
            root,
            row,
            args.runner,
            artifact_root,
            normalized_trace,
            raw_trace,
            args.run_live,
            args.runner == "fixture" and not args.disable_fixture_style_rubric,
        )
        for row in rows
    ]
    payload = build_payload(cases)

    if args.json_out:
        target = Path(args.json_out)
        target = target if target.is_absolute() else root / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for case in cases:
            status = "PASS" if case.passed else "FAIL"
            print(f"{status} {case.case_id}: {case.total_score}/100 {case.scores}")
            for failure in case.failures:
                print(f"  - {failure}")
        print(f"Summary: {payload['summary']['passed']} passed, {payload['summary']['failed']} failed.")
    return 0 if payload["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
