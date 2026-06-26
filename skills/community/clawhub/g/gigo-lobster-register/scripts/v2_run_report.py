from __future__ import annotations

import hashlib

from .utils import Scores, TaskResult


def _response_hash(response: str) -> str:
    return hashlib.sha256(response.encode("utf-8")).hexdigest()


def _transcript_summary(result: TaskResult) -> dict:
    transcript = result.transcript if isinstance(result.transcript, dict) else {}
    tool_calls = transcript.get("tool_calls")
    files_read = transcript.get("files_read")
    files_written = transcript.get("files_written")
    shell_violations = transcript.get("shell_violations")
    return {
        "workdir": result.workdir,
        "tool_call_count": len(tool_calls) if isinstance(tool_calls, list) else 0,
        "files_read_count": len(files_read) if isinstance(files_read, list) else 0,
        "files_written_count": len(files_written) if isinstance(files_written, list) else 0,
        "shell_violation_count": len(shell_violations) if isinstance(shell_violations, list) else 0,
        "has_raw_stdout": bool(transcript.get("raw_stdout")),
        "has_raw_stderr": bool(transcript.get("raw_stderr")),
    }


def build_run_report(
    scores: Scores,
    raw_results: list[TaskResult],
    config: dict,
    upload_mode: str,
) -> dict:
    session = config.get("task_session") or {}
    task_results = []
    task_artifacts = []
    judge_receipts = []
    for result in raw_results:
        task_results.append(
            {
                "task_id": result.task_id,
                "status": result.status,
                "task_score": int(result.total_score),
                "scores": result.task_scores,
                "reasoning": result.reasoning,
                "elapsed_ms": int(result.elapsed_ms),
                "usage": {
                    "prompt_tokens": int(result.usage.get("prompt_tokens", 0)),
                    "completion_tokens": int(result.usage.get("completion_tokens", 0)),
                },
                "violations": list(result.violations),
                "details": dict(result.details),
            }
        )
        response = str(result.response or "")
        task_artifacts.append(
            {
                "task_id": result.task_id,
                "response_text": response,
                "response_hash": _response_hash(response),
                "response_chars": len(response),
                "artifact_refs": [],
                "transcript_summary": _transcript_summary(result),
            }
        )
        for receipt in result.judge_receipts:
            judge_receipts.append({"task_id": result.task_id, **receipt})

    return {
        "session_id": session.get("session_id"),
        "ticket": session.get("ticket"),
        "lobster_name": scores.lobster_name,
        "anonymous": bool(scores.anonymous),
        "skill_version": config.get("skill_version"),
        "bundle_version": config.get("task_bundle_version"),
        "bundle_hash": config.get("task_bundle_hash"),
        "lang": scores.lang,
        "upload_mode": upload_mode,
        "timestamp": scores.timestamp,
        "task_results": task_results,
        "task_artifacts": task_artifacts,
        "judge_receipts": judge_receipts,
        "usage": {
            "prompt_tokens": sum(int(item.usage.get("prompt_tokens", 0)) for item in raw_results),
            "completion_tokens": sum(int(item.usage.get("completion_tokens", 0)) for item in raw_results),
        },
        "elapsed_ms": sum(int(item.elapsed_ms) for item in raw_results),
    }
