#!/usr/bin/env python3
"""Orchestrator dispatch for the auto-improvement pipeline.

Coordinates the full PROPOSE → DISCRIMINATE → EVALUATE → EXECUTE → GATE loop
with Ralph Wiggum-style retry: on revert, capture a structured failure trace
and feed it back into the next proposal round.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
REPO_ROOT = _REPO_ROOT

from lib.common import read_json, utc_now_iso, write_json

# ---------------------------------------------------------------------------
# Script paths (relative to repo root)
# ---------------------------------------------------------------------------

GENERATOR_SCRIPT = REPO_ROOT / "skills" / "improvement-generator" / "scripts" / "propose.py"
DISCRIMINATOR_SCRIPT = REPO_ROOT / "skills" / "improvement-discriminator" / "scripts" / "score.py"
EVALUATOR_SCRIPT = REPO_ROOT / "skills" / "improvement-evaluator" / "scripts" / "evaluate.py"
EXECUTOR_SCRIPT = REPO_ROOT / "skills" / "improvement-executor" / "scripts" / "execute.py"
GATE_SCRIPT = REPO_ROOT / "skills" / "improvement-gate" / "scripts" / "gate.py"

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Orchestrate the full auto-improvement pipeline",
    )
    parser.add_argument("--target", required=True, help="Target skill/file path")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Feedback/memory source (repeatable)",
    )
    parser.add_argument("--state-root", required=True, help="State directory root")
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Max retry attempts on revert (default: 3)",
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Run full pipeline without pausing",
    )
    parser.add_argument(
        "--task-suite",
        help="Path to task_suite.yaml for evaluator (enables real LLM evaluation)",
    )
    parser.add_argument(
        "--eval-mock",
        action="store_true",
        help="Run evaluator in mock mode (no claude -p calls)",
    )
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Subprocess helpers
# ---------------------------------------------------------------------------


def _run_script(cmd: list[str], label: str) -> str:
    """Run a subprocess and return its stdout (stripped).

    Raises RuntimeError on non-zero exit.
    """
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    if result.returncode != 0:
        raise RuntimeError(
            f"{label} failed (exit {result.returncode}):\n"
            f"  stdout: {result.stdout.strip()}\n"
            f"  stderr: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def run_script(script: Path, args: list[str], label: str) -> Path:
    """Run a script with args and return the artifact path as a Path.

    Higher-level wrapper around subprocess that:
    - Raises RuntimeError (with stderr) on non-zero exit.
    - Raises RuntimeError when stdout is blank.
    - Returns the last non-blank line of stdout as a resolved Path.
    """
    cmd = [sys.executable, str(script)] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    if result.returncode != 0:
        raise RuntimeError(
            f"{label} failed (exit {result.returncode}):\n"
            f"  stdout: {result.stdout.strip()}\n"
            f"  stderr: {result.stderr.strip()}"
        )
    stdout = result.stdout.strip()
    if not stdout:
        raise RuntimeError(f"{label} produced no output")
    path = Path(stdout)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve()


def run_proposer(
    target: str,
    sources: list[str],
    state_root: str,
    trace: str | None = None,
) -> dict[str, Any]:
    """Call propose.py and return the candidate artifact."""
    cmd = [
        sys.executable,
        str(GENERATOR_SCRIPT),
        "--target",
        str(target),
        "--state-root",
        str(state_root),
    ]
    for s in sources:
        cmd.extend(["--source", str(s)])
    if trace:
        cmd.extend(["--trace", str(trace)])
    artifact_path = _run_script(cmd, "proposer")
    return read_json(Path(artifact_path))


def run_discriminator(
    candidate_artifact_path: str,
    state_root: str,
) -> dict[str, Any]:
    """Call score.py and return the ranking artifact."""
    cmd = [
        sys.executable,
        str(DISCRIMINATOR_SCRIPT),
        "--input",
        str(candidate_artifact_path),
        "--state-root",
        str(state_root),
    ]
    artifact_path = _run_script(cmd, "discriminator")
    return read_json(Path(artifact_path))


def run_executor(
    ranking_artifact_path: str,
    candidate_id: str,
    state_root: str,
) -> dict[str, Any]:
    """Call execute.py and return the execution artifact."""
    cmd = [
        sys.executable,
        str(EXECUTOR_SCRIPT),
        "--input",
        str(ranking_artifact_path),
        "--candidate-id",
        candidate_id,
        "--state-root",
        str(state_root),
    ]
    artifact_path = _run_script(cmd, "executor")
    return read_json(Path(artifact_path))


def run_evaluator(
    ranking_artifact_path: str,
    candidate_id: str,
    state_root: str,
    task_suite: str | None = None,
    eval_threshold: float = 6.0,
    mock: bool = False,
) -> dict[str, Any] | None:
    """Call evaluate.py if a task suite exists for the target skill.

    Returns evaluation artifact dict, or None if skipped (no task suite
    or evaluator script not found).
    """
    if not EVALUATOR_SCRIPT.exists():
        print("  Evaluator: skipped (script not found)")
        return None
    if not task_suite:
        print("  Evaluator: skipped (no --task-suite provided)")
        return None
    cmd = [
        sys.executable,
        str(EVALUATOR_SCRIPT),
        "--input", str(ranking_artifact_path),
        "--candidate-id", candidate_id,
        "--task-suite", str(task_suite),
        "--state-root", str(state_root),
        "--eval-threshold", str(eval_threshold),
    ]
    if mock:
        cmd.append("--mock")
    try:
        artifact_path = _run_script(cmd, "evaluator")
        result = read_json(Path(artifact_path))
        evaluation = result.get("evaluation", {})
        verdict = evaluation.get("verdict", result.get("verdict", "skipped"))
        if verdict == "skipped":
            print("  Evaluator: skipped (no task suite)")
            return None
        print(f"  Evaluator: {verdict} (pass_rate={evaluation.get('execution_pass_rate', 'N/A')})")
        return result
    except RuntimeError as exc:
        print(f"  Evaluator: error ({exc}), continuing without evaluation")
        return None


def run_gate(
    ranking_artifact_path: str,
    execution_artifact_path: str,
    state_root: str,
) -> dict[str, Any]:
    """Call gate.py and return the gate receipt."""
    cmd = [
        sys.executable,
        str(GATE_SCRIPT),
        "--ranking",
        str(ranking_artifact_path),
        "--execution",
        str(execution_artifact_path),
        "--state-root",
        str(state_root),
    ]
    artifact_path = _run_script(cmd, "gate")
    return read_json(Path(artifact_path))


# ---------------------------------------------------------------------------
# Candidate selection
# ---------------------------------------------------------------------------


def find_best_accepted(ranking_artifact: dict[str, Any]) -> dict[str, Any] | None:
    """Return the highest-scored candidate with recommendation=accept_for_execution.

    Candidates in the ranking artifact are already sorted by score (descending),
    so the first match is the best.
    """
    for candidate in ranking_artifact.get("scored_candidates", []):
        if candidate.get("recommendation") == "accept_for_execution":
            return candidate
    return None


# ---------------------------------------------------------------------------
# Failure trace (Ralph Wiggum feedback loop)
# ---------------------------------------------------------------------------


def extract_failure_trace(
    receipt: dict[str, Any],
    execution_artifact: dict[str, Any],
    state_root: str,
) -> str:
    """Extract structured failure trace and write it to a file.

    The returned path can be passed as --trace to the next proposer round,
    enabling the Ralph Wiggum retry pattern: failures feed forward as
    context for the next attempt.
    """
    trace = {
        "type": "failure_trace",
        "candidate_id": receipt.get("candidate_id"),
        "decision": receipt.get("decision"),
        "reason": receipt.get("reason"),
        "execution_status": execution_artifact.get("result", {}).get("status"),
        "diff": execution_artifact.get("result", {}).get("diff", ""),
        "gate_blockers": receipt.get("blockers", []),
        "timestamp": utc_now_iso(),
    }
    run_id = receipt.get("run_id", "unknown")
    trace_dir = Path(state_root) / "traces"
    trace_path = trace_dir / f"trace-{run_id}.json"
    write_json(trace_path, trace)
    return str(trace_path)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


def run_baseline_evaluation(
    target: str,
    task_suite: str,
    state_root: str,
    mock: bool = False,
) -> str | None:
    """Run evaluator in standalone mode on current SKILL.md to get baseline failures.

    Returns path to a feedback source file containing per-task failure details,
    or None if no failures found or evaluator unavailable.
    """
    if not EVALUATOR_SCRIPT.exists():
        return None

    cmd = [
        sys.executable,
        str(EVALUATOR_SCRIPT),
        "--standalone",
        "--task-suite", str(task_suite),
        "--state-root", str(state_root),
        "--skill-path", str(target),
    ]
    if mock:
        cmd.append("--mock")

    try:
        stdout = _run_script(cmd, "baseline-evaluator")
        result = read_json(Path(stdout))
    except RuntimeError as exc:
        print(f"  Baseline evaluation failed ({exc}), continuing without feedback")
        return None

    # Extract failed tasks as feedback for generator
    task_results = result.get("task_results", [])
    failed_tasks = [r for r in task_results if not r.get("passed")]
    if not failed_tasks:
        print(f"  Baseline: all tasks passed, no failures to feed back")
        return None

    pass_rate = result.get("evaluation", {}).get("pass_rate", 0)
    print(f"  Baseline: {len(failed_tasks)} task(s) failed (pass_rate={pass_rate})")

    # Write failure details as a source file for generator
    feedback = {
        "type": "evaluator_baseline_failures",
        "pass_rate": pass_rate,
        "failed_tasks": [],
        "timestamp": utc_now_iso(),
    }
    for t in failed_tasks:
        feedback["failed_tasks"].append({
            "task_id": t.get("task_id"),
            "score": t.get("score", 0),
            "details": t.get("details", ""),
            "error": t.get("error", ""),
        })

    feedback_dir = Path(state_root) / "traces"
    feedback_dir.mkdir(parents=True, exist_ok=True)
    feedback_path = feedback_dir / "baseline-failures.json"
    write_json(feedback_path, feedback)
    return str(feedback_path)


def run_pipeline(
    target: str,
    sources: list[str],
    state_root: str,
    max_retries: int = 3,
    task_suite: str | None = None,
    eval_mock: bool = False,
) -> dict[str, Any]:
    """Run the full PROPOSE → DISCRIMINATE → EVALUATE → EXECUTE → GATE loop.

    Returns a summary dict with the final outcome.
    """
    # Mutable copy so we can append failure traces across retries
    active_sources = list(sources)
    active_trace: str | None = None
    final_decision = "no_candidates"
    final_candidate_id: str | None = None
    final_artifact_path: str | None = None
    attempts_used = 0

    # 0. BASELINE EVALUATION — run evaluator on current SKILL.md first
    #    to discover which tasks fail, then inject as feedback for generator
    if task_suite:
        baseline_feedback = run_baseline_evaluation(
            target, task_suite, state_root, mock=eval_mock,
        )
        if baseline_feedback:
            active_sources.append(baseline_feedback)

    for attempt in range(1, max_retries + 1):
        attempts_used = attempt
        # 1. PROPOSE
        candidate_artifact = run_proposer(target, active_sources, state_root, trace=active_trace)
        candidate_artifact_path = candidate_artifact.get("truth_anchor", "")

        # 2. DISCRIMINATE (score + rank)
        ranking_artifact = run_discriminator(candidate_artifact_path, state_root)
        ranking_artifact_path = ranking_artifact.get("truth_anchor", "")

        # 3. Find best accepted candidate
        best = find_best_accepted(ranking_artifact)
        if not best:
            if attempt >= max_retries:
                final_decision = "no_accepted_candidates"
                print(f"  No accepted candidates after {attempt} attempts")
                break
            # Inject rejection trace for next round
            trace_dir = Path(state_root) / "traces"
            trace_dir.mkdir(parents=True, exist_ok=True)
            rejection_trace = {
                "type": "all_rejected_trace",
                "scored_candidates": [
                    {"id": c.get("id"), "score": c.get("score"), "recommendation": c.get("recommendation")}
                    for c in ranking_artifact.get("scored_candidates", [])
                ],
                "timestamp": utc_now_iso(),
            }
            trace_path = trace_dir / f"rejection-trace-attempt-{attempt}.json"
            write_json(trace_path, rejection_trace)
            active_trace = str(trace_path)
            print(f"  No accepted candidates, retrying ({attempt}/{max_retries})")
            continue

        candidate_id = best["id"]

        # 3.5 EVALUATE (optional — skipped if no --task-suite provided)
        eval_result = run_evaluator(
            ranking_artifact_path,
            candidate_id,
            state_root,
            task_suite=task_suite,
            mock=eval_mock,
        )
        eval_verdict = eval_result.get("evaluation", {}).get("verdict") if eval_result else None
        if eval_verdict == "fail":
            # Evaluation failed — treat as revert and retry
            trace = {
                "type": "evaluation_failure_trace",
                "candidate_id": candidate_id,
                "evaluation_results": eval_result.get("evaluation", {}),
                "timestamp": utc_now_iso(),
            }
            trace_dir = Path(state_root) / "traces"
            trace_dir.mkdir(parents=True, exist_ok=True)
            trace_path = trace_dir / f"eval-trace-{candidate_id}.json"
            write_json(trace_path, trace)
            active_trace = str(trace_path)
            print(f"  Evaluation failed, retrying ({attempt}/{max_retries})")
            continue

        # 4. EXECUTE
        execution_artifact = run_executor(
            ranking_artifact_path,
            candidate_id,
            state_root,
        )
        execution_artifact_path = execution_artifact.get("truth_anchor", "")

        # 5. GATE (verify after execution)
        receipt = run_gate(
            ranking_artifact_path,
            execution_artifact_path,
            state_root,
        )

        # 6. DECIDE
        decision = receipt.get("decision", "reject")
        final_decision = decision
        final_candidate_id = candidate_id
        final_artifact_path = receipt.get("truth_anchor")

        if decision == "keep":
            print(f"  Kept: {candidate_id}")
            break
        elif decision == "revert":
            # Ralph Wiggum: capture trace, inject into next round
            trace_path = extract_failure_trace(
                receipt, execution_artifact, state_root,
            )
            active_trace = trace_path
            print(
                f"  Reverted, retrying ({attempt}/{max_retries})"
            )
            continue
        elif decision == "pending_promote":
            print(f"  Pending human review: {candidate_id}")
            break
        else:  # reject
            print(f"  Rejected: {candidate_id}")
            break

    return {
        "target": target,
        "attempts": attempts_used,
        "max_retries": max_retries,
        "final_decision": final_decision,
        "final_candidate_id": final_candidate_id,
        "final_artifact_path": final_artifact_path,
    }


# ---------------------------------------------------------------------------
# Summary report
# ---------------------------------------------------------------------------


def print_summary(summary: dict[str, Any]) -> None:
    """Print a human-readable pipeline summary."""
    print("\nPipeline Summary:")
    print(f"  Target: {summary['target']}")
    print(f"  Attempts: {summary['attempts']}/{summary['max_retries']}")
    print(f"  Final Decision: {summary['final_decision']}")
    print(f"  Candidate: {summary.get('final_candidate_id', 'N/A')}")
    print(f"  Artifact: {summary.get('final_artifact_path', 'N/A')}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    target = str(Path(args.target).expanduser().resolve())
    state_root = str(Path(args.state_root).expanduser().resolve())
    sources = [str(Path(s).expanduser().resolve()) for s in args.source if s]

    task_suite = str(Path(args.task_suite).expanduser().resolve()) if args.task_suite else None

    try:
        summary = run_pipeline(
            target=target,
            sources=sources,
            state_root=state_root,
            max_retries=args.max_retries,
            task_suite=task_suite,
            eval_mock=args.eval_mock,
        )
    except RuntimeError as exc:
        print(f"Pipeline error: {exc}", file=sys.stderr)
        return 1

    print_summary(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
