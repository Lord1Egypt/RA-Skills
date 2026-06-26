from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
import re
from decimal import Decimal, ROUND_HALF_UP

from .utils import Task, TaskResult
from .v2_check_executor import run_check
from .v2_judge_client import JudgeClient, output_hash
from .v2_shell_shim import ShellShim

MAX_JUDGE_EXCERPT_CHARS = 8000
MAX_JUDGE_PROMPT_CHARS = 3500
MAX_JUDGE_CONTEXT_CHARS = 12000


def _normalize_tool_calls(items: list[dict] | None) -> list[dict]:
    if not items:
        return []
    normalized: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "name": item.get("name") or item.get("tool_name") or item.get("raw_name") or "Other",
                "args": item.get("args") or {},
                "result": item.get("result") or "",
                "ts": float(item.get("ts") or time.time()),
                "duration_ms": int(item.get("duration_ms") or 0),
                "error": item.get("error"),
                "raw_name": item.get("raw_name") or item.get("name") or "unknown",
                "parallel_group": item.get("parallel_group"),
            }
        )
    return normalized


def _coerce_score(value: object) -> int:
    try:
        numeric = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0
    if not math.isfinite(numeric):
        return 0
    return max(0, min(100, int(round(numeric))))


def _round_half_up(value: float) -> int:
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def _normalize_scores(scores: dict | None) -> dict[str, int]:
    if not isinstance(scores, dict):
        return {}
    return {str(key): _coerce_score(value) for key, value in scores.items()}


def _merge_judge_scores(rule_scores: dict[str, int], judge_scores: dict[str, int]) -> dict[str, int]:
    merged = dict(rule_scores)
    for key, judge_score in judge_scores.items():
        if key in merged:
            merged[key] = _round_half_up(merged[key] * 0.4 + judge_score * 0.6)
        else:
            merged[key] = judge_score
    return merged


def _judge_scores_are_usable(judge_response: dict) -> bool:
    return not judge_response.get("fallback_used") and not judge_response.get("error")


def _derive_task_total(task: Task, task_scores: dict[str, int], fallback: int) -> int:
    if not task_scores:
        return fallback

    primary_scores = [task_scores[key] for key in task.primary_dimensions if key in task_scores]
    secondary_scores = [task_scores[key] for key in task.secondary_dimensions if key in task_scores]

    if not primary_scores and not secondary_scores:
        return fallback

    if not primary_scores:
        return _round_half_up(sum(secondary_scores) / max(len(secondary_scores), 1))

    all_scores = primary_scores + secondary_scores
    return _round_half_up(sum(all_scores) / len(all_scores))


def _truncate_text(value: object, limit: int) -> str:
    text = str(value or "")
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated {len(text) - limit} chars]"


def _json_safe_truncated(value: object, limit: int = MAX_JUDGE_CONTEXT_CHARS) -> object:
    try:
        text = json.dumps(value, ensure_ascii=False, default=str)
    except TypeError:
        return str(value)
    if len(text) <= limit:
        return value
    return {"truncated_json": text[:limit], "original_chars": len(text)}


def _judge_dimensions(task: Task, explicit_payload: dict | None) -> list[str]:
    explicit = explicit_payload.get("dimensions_to_judge") if explicit_payload else None
    dimensions: list[str] = []
    for item in explicit if isinstance(explicit, list) else []:
        if isinstance(item, str) and item not in dimensions:
            dimensions.append(item)
    for item in [*task.primary_dimensions, *task.secondary_dimensions]:
        if item not in {"cost", "speed"} and item not in dimensions:
            dimensions.append(item)
    return dimensions


def _build_default_judge_context(task: Task, evaluation: dict, transcript: dict, workdir: Path, explicit_context: object) -> dict:
    tool_calls = transcript.get("tool_calls") if isinstance(transcript.get("tool_calls"), list) else []
    files_read = transcript.get("files_read") if isinstance(transcript.get("files_read"), list) else []
    files_written = transcript.get("files_written") if isinstance(transcript.get("files_written"), list) else []
    shell_violations = transcript.get("shell_violations") if isinstance(transcript.get("shell_violations"), list) else []
    context = {
        "task": {
            "id": task.id,
            "track": task.track,
            "title_en": task.title_en,
            "category_hint": task.dish_hint,
            "primary_dimensions": task.primary_dimensions,
            "secondary_dimensions": task.secondary_dimensions,
            "timeout_seconds": task.timeout_seconds,
        },
        "assignment_excerpt": _truncate_text(task.prompt, MAX_JUDGE_PROMPT_CHARS),
        "local_evaluation": {
            "scores": _normalize_scores(evaluation.get("scores")),
            "details": _json_safe_truncated(evaluation.get("details") or {}),
            "violations": list(evaluation.get("violations") or []),
        },
        "runtime_evidence": {
            "elapsed_ms": int(transcript.get("elapsed_ms") or 0),
            "prompt_tokens": int((transcript.get("tokens") or {}).get("prompt") or 0),
            "completion_tokens": int((transcript.get("tokens") or {}).get("completion") or 0),
            "tool_call_count": len(tool_calls),
            "files_read_count": len(files_read),
            "files_written_count": len(files_written),
            "shell_violation_count": len(shell_violations),
            "has_stdout": bool(str(transcript.get("stdout") or "").strip()),
            "has_error": bool(transcript.get("error")),
        },
        "workdir_name": workdir.name,
    }
    if explicit_context:
        context["task_specific_context"] = _json_safe_truncated(explicit_context)
    return context


def _build_judge_payload(task: Task, evaluation: dict, transcript: dict, workdir: Path) -> dict:
    explicit_payload = evaluation.get("judge_required") if isinstance(evaluation.get("judge_required"), dict) else None
    agent_output_excerpt = ""
    explicit_context: object = {}
    if explicit_payload:
        agent_output_excerpt = str(explicit_payload.get("agent_output_excerpt") or "")
        explicit_context = explicit_payload.get("context") or {}
    if not agent_output_excerpt:
        agent_output_excerpt = str(transcript.get("stdout") or "")
    return {
        "rubric_file": explicit_payload.get("rubric_file") if explicit_payload else "judge_rubric.md",
        "agent_output_excerpt": _truncate_text(agent_output_excerpt, MAX_JUDGE_EXCERPT_CHARS),
        "context": _build_default_judge_context(task, evaluation, transcript, workdir, explicit_context),
        "dimensions_to_judge": _judge_dimensions(task, explicit_payload),
    }


def _extract_command_payload(completed: subprocess.CompletedProcess[str], elapsed_ms: int) -> dict:
    raw_stdout = completed.stdout or ""
    raw_stderr = completed.stderr or ""
    stdout = "\n".join(chunk for chunk in [raw_stdout, raw_stderr] if chunk)
    tokens = {"prompt": 0, "completion": 0}

    try:
        body = json.loads(raw_stdout.strip()) if raw_stdout.strip() else None
    except json.JSONDecodeError:
        body = None

    if isinstance(body, dict):
        result = body.get("result") if isinstance(body.get("result"), dict) else {}
        meta = result.get("meta") if isinstance(result.get("meta"), dict) else {}
        final_text = meta.get("finalAssistantVisibleText") or meta.get("finalAssistantRawText")
        if not final_text:
            payloads = result.get("payloads")
            if isinstance(payloads, list):
                texts = [str(item.get("text", "")) for item in payloads if isinstance(item, dict) and item.get("text")]
                final_text = "\n".join(texts)
        if final_text:
            stdout = str(final_text)

        agent_meta = meta.get("agentMeta") if isinstance(meta.get("agentMeta"), dict) else {}
        usage = agent_meta.get("usage") if isinstance(agent_meta.get("usage"), dict) else {}
        tokens = {
            "prompt": int(usage.get("input") or agent_meta.get("promptTokens") or 0),
            "completion": int(usage.get("output") or 0),
        }

    return {
        "tool_calls": [],
        "stdout": stdout,
        "raw_stdout": raw_stdout,
        "raw_stderr": raw_stderr,
        "elapsed_ms": elapsed_ms,
        "tokens": tokens,
        "files_read": [],
        "files_written": [],
        "error": None if completed.returncode == 0 else f"agent_exit_{completed.returncode}",
    }


def _agent_prompt(task: Task, workdir: Path) -> str:
    return (
        f"{task.prompt.rstrip()}\n\n"
        "[GIGO eval runtime]\n"
        f"- Work only inside this task directory: {workdir}\n"
        "- When the task names a file, script, test, package, or endpoint, implement the change in the actual files under this directory. A code block in the final answer does not count as completing the task.\n"
        "- If tests or validation commands are present, run the relevant checks before your final reply and fix failures you can address within the task directory.\n"
        "- Write files only when the task explicitly asks for a file path, asks you to create/edit files, or provides a working directory with setup/tests to satisfy.\n"
        "- If the task asks for prose, an email, a list, or an explanation without naming an output file, put the complete answer directly in your final reply.\n"
        "- For prose-only tasks, do not add prefaces, completion summaries, self-checks, or word-count notes unless the task asks for them.\n"
        "- After file-edit tasks, reply with a concise summary of changed files and checks run. After prose-only tasks, reply with the actual requested content.\n"
    )


def _safe_session_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_.:-]+", "-", value).strip("-")
    return normalized[:120] or "gigo-eval"


class AgentRunner:
    def __init__(self, config: dict, gateway_client) -> None:
        self.config = config
        self.gateway_client = gateway_client
        self.judge_client = JudgeClient(config)
        session = config.get("task_session") or {}
        self.run_id = str(session.get("session_id") or f"local-{int(time.time())}")
        self.root = Path.home() / ".openclaw" / "eval" / self.run_id

    def _prepare_workdir(self, task: Task) -> Path:
        workdir = self.root / task.id
        if workdir.exists():
            shutil.rmtree(workdir)
        workdir.mkdir(parents=True, exist_ok=True)
        setup_dir = Path(task.task_dir) / "setup"
        if setup_dir.exists():
            shutil.copytree(setup_dir, workdir, dirs_exist_ok=True)
        return workdir

    def _run_agent_command(self, task: Task, workdir: Path, shim: ShellShim) -> dict:
        prompt_file = workdir / "prompt.md"
        prompt_file.write_text(_agent_prompt(task, workdir), encoding="utf-8")
        transcript_file = workdir / ".gigo_transcript.json"
        env = shim.install()
        env.update(
            {
                "GIGO_TASK_WORKDIR": str(workdir),
                "GIGO_TASK_ID": task.id,
                "GIGO_EVAL_RUN_ID": self.run_id,
                "GIGO_AGENT_SESSION_ID": _safe_session_id(f"gigo-eval-{self.run_id}-{task.id}"),
                "GIGO_TASK_PROMPT_FILE": str(prompt_file),
                "GIGO_TASK_TRANSCRIPT_FILE": str(transcript_file),
                "GIGO_TASK_TIMEOUT_SECONDS": str(task.timeout_seconds),
            }
        )

        command = os.environ.get("GIGO_V2_AGENT_COMMAND", "").strip()
        if not command:
            response = self.gateway_client.send_task(task.prompt, timeout=task.timeout_seconds)
            payload = {
                "tool_calls": [],
                "stdout": response.get("content", ""),
                "elapsed_ms": int(response.get("elapsed_ms", 0)),
                "tokens": {
                    "prompt": int(response.get("usage", {}).get("prompt_tokens", 0)),
                    "completion": int(response.get("usage", {}).get("completion_tokens", 0)),
                },
                "files_read": [],
                "files_written": [],
                "error": response.get("error"),
            }
            transcript_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            return payload

        started = time.time()
        try:
            completed = subprocess.run(
                command,
                shell=True,
                cwd=str(workdir),
                env=env,
                capture_output=True,
                text=True,
                timeout=task.timeout_seconds + 10,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raw_stdout = error.stdout.decode("utf-8", errors="ignore") if isinstance(error.stdout, bytes) else str(error.stdout or "")
            raw_stderr = error.stderr.decode("utf-8", errors="ignore") if isinstance(error.stderr, bytes) else str(error.stderr or "")
            payload = {
                "tool_calls": [],
                "stdout": "\n".join(chunk for chunk in [raw_stdout, raw_stderr] if chunk),
                "raw_stdout": raw_stdout,
                "raw_stderr": raw_stderr,
                "elapsed_ms": int((time.time() - started) * 1000),
                "tokens": {"prompt": 0, "completion": 0},
                "files_read": [],
                "files_written": [],
                "error": "agent_timeout",
            }
            transcript_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            return payload

        if transcript_file.exists():
            payload = json.loads(transcript_file.read_text(encoding="utf-8"))
        else:
            payload = _extract_command_payload(completed, int((time.time() - started) * 1000))
            transcript_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload

    def run_task(self, task: Task) -> TaskResult:
        workdir = self._prepare_workdir(task)
        shim = ShellShim(workdir)
        started = time.time()
        transcript = self._run_agent_command(task, workdir, shim)
        transcript["tool_calls"] = _normalize_tool_calls(transcript.get("tool_calls"))
        transcript.setdefault("stdout", "")
        transcript.setdefault("elapsed_ms", int((time.time() - started) * 1000))
        transcript.setdefault("tokens", {"prompt": 0, "completion": 0})
        transcript.setdefault("files_read", [])
        transcript.setdefault("files_written", [])
        transcript["shell_violations"] = shim.violations()

        evaluation = run_check(task, workdir, transcript)
        judge_receipts: list[dict] = []
        judge_payload = _build_judge_payload(task, evaluation, transcript, workdir)
        if judge_payload.get("dimensions_to_judge"):
            agent_output_excerpt = judge_payload.get("agent_output_excerpt", "")
            judge_response = self.judge_client.judge(
                {
                    "run_id": self.run_id,
                    "task_id": task.id,
                    "rubric_id": f"{task.id}@{self.config.get('task_bundle_version', '2.0.0')}",
                    "agent_output_excerpt": agent_output_excerpt,
                    "context": judge_payload.get("context", {}),
                    "dimensions_to_judge": judge_payload.get("dimensions_to_judge", []),
                    "client_version": self.config.get("skill_version", "2.0.17"),
                }
            )
            normalized_judge_scores = _normalize_scores(judge_response.get("scores"))
            if _judge_scores_are_usable(judge_response):
                evaluation["scores"] = _merge_judge_scores(_normalize_scores(evaluation.get("scores")), normalized_judge_scores)
            judge_response["scores"] = normalized_judge_scores
            judge_response["output_hash"] = output_hash(str(agent_output_excerpt))
            judge_receipts.append(judge_response)

        task_scores = _normalize_scores(evaluation.get("scores"))
        if transcript.get("error"):
            task_scores = {key: 0 for key in set(task.primary_dimensions + task.secondary_dimensions)}
        primary_key = task.primary_dimensions[0] if task.primary_dimensions else next(iter(task_scores), "meat")
        fallback_total = int(task_scores.get(primary_key, max(task_scores.values()) if task_scores else 0))
        task_total = _derive_task_total(task, task_scores, fallback_total)

        return TaskResult(
            task_id=task.id,
            dish_name=task.dish_name,
            prompt=task.prompt,
            response=str(transcript.get("stdout", "")),
            status="success" if not transcript.get("error") else "error",
            error=transcript.get("error"),
            elapsed_ms=int(transcript.get("elapsed_ms", 0)),
            usage={
                "prompt_tokens": int(transcript.get("tokens", {}).get("prompt", 0)),
                "completion_tokens": int(transcript.get("tokens", {}).get("completion", 0)),
            },
            primary_dimensions=task.primary_dimensions,
            secondary_dimensions=task.secondary_dimensions,
            rubric="",
            total_score=task_total,
            reasoning=str(judge_receipts[0].get("reasoning") or "") if judge_receipts else "",
            task_scores=task_scores,
            transcript=transcript,
            details=dict(evaluation.get("details") or {}),
            violations=list(evaluation.get("violations") or []),
            judge_receipts=judge_receipts,
            workdir=str(workdir),
        )

    def run(self, tasks: list[Task]) -> list[TaskResult]:
        results: list[TaskResult] = []
        total = len(tasks)
        for index, task in enumerate(tasks, start=1):
            print(f"🍽️ [{index}/{total}] 开始试吃：{task.id} · {task.dish_name}", flush=True)
            started = time.time()
            result = self.run_task(task)
            results.append(result)
            elapsed = int(time.time() - started)
            print(
                f"✅ [{index}/{total}] 完成：{task.id} · status={result.status} · score={result.total_score}/100 · {elapsed}s",
                flush=True,
            )
        return results
