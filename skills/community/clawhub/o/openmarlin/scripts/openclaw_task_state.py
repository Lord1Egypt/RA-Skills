"""Helpers for storing recent OpenMarlin task submissions in OpenClaw agent data."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from openclaw_platform_auth import DEFAULT_AGENT_ID, resolve_agent_dir


DEFAULT_TASK_STATE_VERSION = 1


def format_iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def fingerprint_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()


def resolve_task_state_path(agent_id: str = DEFAULT_AGENT_ID) -> Path:
    return resolve_agent_dir(agent_id) / "task-state.json"


def _save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="task-state-", suffix=".json", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        try:
            tmp_path.chmod(0o600)
        except OSError:
            pass
        os.replace(tmp_path, path)
        try:
            path.chmod(0o600)
        except OSError:
            pass
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def ensure_task_state(agent_id: str = DEFAULT_AGENT_ID) -> tuple[Path, dict[str, Any]]:
    agent_dir = resolve_agent_dir(agent_id)
    agent_dir.mkdir(parents=True, exist_ok=True)
    try:
        agent_dir.chmod(0o700)
    except OSError:
        pass

    state_path = resolve_task_state_path(agent_id)
    if not state_path.exists():
        state = {"version": DEFAULT_TASK_STATE_VERSION, "submissions": {}}
        _save_json(state_path, state)
        return state_path, state

    with state_path.open("r", encoding="utf-8") as handle:
        raw = handle.read().strip()

    if not raw:
        state = {"version": DEFAULT_TASK_STATE_VERSION, "submissions": {}}
        _save_json(state_path, state)
        return state_path, state

    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise SystemExit(f"Invalid task state store at {state_path}: expected JSON object.")
    parsed.setdefault("version", DEFAULT_TASK_STATE_VERSION)
    submissions = parsed.get("submissions")
    if not isinstance(submissions, dict):
        parsed["submissions"] = {}
    return state_path, parsed


def save_task_state(path: Path, state: dict[str, Any]) -> None:
    _save_json(path, state)


def _submissions_bucket(state: dict[str, Any]) -> dict[str, Any]:
    bucket = state.setdefault("submissions", {})
    if not isinstance(bucket, dict):
        state["submissions"] = {}
        bucket = state["submissions"]
    return bucket


def _submission_key(*, server_url: str, api_key_fingerprint: str, request_fingerprint: str) -> str:
    return f"{server_url.rstrip('/')}|{api_key_fingerprint}|{request_fingerprint}"


def _parse_iso(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _is_recent(value: Any, *, now: datetime, window_seconds: float) -> bool:
    observed_at = _parse_iso(value)
    if observed_at is None:
        return False
    return observed_at >= now - timedelta(seconds=max(0.0, window_seconds))


def find_recent_matching_submission(
    *,
    server_url: str,
    api_key_fingerprint: str,
    request_fingerprint: str,
    dedupe_window_seconds: float,
    reusable_statuses: set[str] | None,
    agent_id: str = DEFAULT_AGENT_ID,
) -> tuple[dict[str, Any] | None, str]:
    state_path, state = ensure_task_state(agent_id)
    submissions = _submissions_bucket(state)
    entry = submissions.get(
        _submission_key(
            server_url=server_url,
            api_key_fingerprint=api_key_fingerprint,
            request_fingerprint=request_fingerprint,
        )
    )
    if not isinstance(entry, dict):
        return None, str(state_path)

    status = entry.get("status")
    if not isinstance(status, str):
        return None, str(state_path)
    if reusable_statuses is not None and status not in reusable_statuses:
        return None, str(state_path)

    if not _is_recent(entry.get("last_seen_at"), now=datetime.now(timezone.utc), window_seconds=dedupe_window_seconds):
        return None, str(state_path)

    return dict(entry), str(state_path)


def record_task_submission(
    *,
    server_url: str,
    api_key_fingerprint: str,
    request_fingerprint: str,
    idempotency_key: str,
    task_id: str | None,
    kind: str,
    status: str,
    prompt: str,
    agent_id: str = DEFAULT_AGENT_ID,
) -> dict[str, Any]:
    state_path, state = ensure_task_state(agent_id)
    submissions = _submissions_bucket(state)
    now = format_iso_now()
    entry = {
        "server_url": server_url.rstrip("/"),
        "api_key_fingerprint": api_key_fingerprint,
        "request_fingerprint": request_fingerprint,
        "idempotency_key": idempotency_key,
        "kind": kind,
        "status": status,
        "prompt": prompt,
        "recorded_at": now,
        "last_seen_at": now,
    }
    if task_id:
        entry["task_id"] = task_id
    submissions[_submission_key(server_url=server_url, api_key_fingerprint=api_key_fingerprint, request_fingerprint=request_fingerprint)] = entry
    save_task_state(state_path, state)
    return {"task_state_path": str(state_path), "submission": entry}


def record_task_observation(
    *,
    server_url: str,
    api_key_fingerprint: str,
    task: dict[str, Any],
    agent_id: str = DEFAULT_AGENT_ID,
) -> dict[str, Any] | None:
    task_id = task.get("task_id")
    status = task.get("status")
    if not isinstance(task_id, str) or not task_id.strip() or not isinstance(status, str) or not status.strip():
        return None

    state_path, state = ensure_task_state(agent_id)
    submissions = _submissions_bucket(state)
    updated_entry: dict[str, Any] | None = None
    for key, value in submissions.items():
        if not isinstance(value, dict):
            continue
        if value.get("server_url") != server_url.rstrip("/"):
            continue
        if value.get("api_key_fingerprint") != api_key_fingerprint:
            continue
        if value.get("task_id") != task_id:
            continue
        value["status"] = status.strip()
        value["last_seen_at"] = format_iso_now()
        updated_entry = dict(value)
        submissions[key] = value
    if updated_entry is None:
        return None
    save_task_state(state_path, state)
    return {"task_state_path": str(state_path), "submission": updated_entry}
