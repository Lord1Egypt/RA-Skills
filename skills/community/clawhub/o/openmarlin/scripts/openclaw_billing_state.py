"""Helpers for storing OpenMarlin billing state in OpenClaw agent data."""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openclaw_platform_auth import DEFAULT_AGENT_ID, resolve_agent_dir


DEFAULT_BILLING_STATE_VERSION = 1


def format_iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def resolve_billing_state_path(agent_id: str = DEFAULT_AGENT_ID) -> Path:
    return resolve_agent_dir(agent_id) / "billing-state.json"


def _save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="billing-state-", suffix=".json", dir=str(path.parent))
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


def ensure_billing_state(agent_id: str = DEFAULT_AGENT_ID) -> tuple[Path, dict[str, Any]]:
    agent_dir = resolve_agent_dir(agent_id)
    agent_dir.mkdir(parents=True, exist_ok=True)
    try:
        agent_dir.chmod(0o700)
    except OSError:
        pass

    state_path = resolve_billing_state_path(agent_id)
    if not state_path.exists():
        state = {"version": DEFAULT_BILLING_STATE_VERSION, "workspaces": {}}
        _save_json(state_path, state)
        return state_path, state

    with state_path.open("r", encoding="utf-8") as handle:
        raw = handle.read().strip()

    if not raw:
        state = {"version": DEFAULT_BILLING_STATE_VERSION, "workspaces": {}}
        _save_json(state_path, state)
        return state_path, state

    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise SystemExit(f"Invalid billing state store at {state_path}: expected JSON object.")
    parsed.setdefault("version", DEFAULT_BILLING_STATE_VERSION)
    workspaces = parsed.get("workspaces")
    if not isinstance(workspaces, dict):
        parsed["workspaces"] = {}
    return state_path, parsed


def save_billing_state(path: Path, state: dict[str, Any]) -> None:
    _save_json(path, state)


def _workspace_bucket(state: dict[str, Any], workspace_id: str) -> dict[str, Any]:
    workspaces = state.setdefault("workspaces", {})
    if not isinstance(workspaces, dict):
        state["workspaces"] = {}
        workspaces = state["workspaces"]
    bucket = workspaces.get(workspace_id)
    if not isinstance(bucket, dict):
        bucket = {}
        workspaces[workspace_id] = bucket
    bucket.setdefault("topup_sessions", {})
    return bucket


def record_balance_snapshot(
    *,
    workspace_id: str,
    amount: float,
    unit: str,
    agent_id: str = DEFAULT_AGENT_ID,
    source: str,
    estimated: bool,
    message: str | None = None,
    required_amount: float | None = None,
    reference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state_path, state = ensure_billing_state(agent_id)
    bucket = _workspace_bucket(state, workspace_id)
    snapshot: dict[str, Any] = {
        "workspace_id": workspace_id,
        "amount": float(amount),
        "unit": unit,
        "observed_at": format_iso_now(),
        "source": source,
        "estimated": estimated,
    }
    if message:
        snapshot["message"] = message
    if required_amount is not None:
        snapshot["required_amount"] = float(required_amount)
    if reference:
        snapshot["reference"] = reference
    bucket["last_balance_snapshot"] = snapshot
    save_billing_state(state_path, state)
    return {"billing_state_path": str(state_path), "snapshot": snapshot}


def get_last_balance_snapshot(*, workspace_id: str, agent_id: str = DEFAULT_AGENT_ID) -> tuple[dict[str, Any] | None, str]:
    state_path, state = ensure_billing_state(agent_id)
    bucket = state.get("workspaces", {}).get(workspace_id)
    if not isinstance(bucket, dict):
        return None, str(state_path)
    snapshot = bucket.get("last_balance_snapshot")
    return snapshot if isinstance(snapshot, dict) else None, str(state_path)


def record_topup_session(
    *,
    session: dict[str, Any],
    agent_id: str = DEFAULT_AGENT_ID,
) -> dict[str, Any]:
    workspace_id = session.get("workspace_id")
    session_id = session.get("topup_session_id")
    if not isinstance(workspace_id, str) or not workspace_id.strip():
        raise SystemExit("Top-up session payload is missing workspace_id.")
    if not isinstance(session_id, str) or not session_id.strip():
        raise SystemExit("Top-up session payload is missing topup_session_id.")

    state_path, state = ensure_billing_state(agent_id)
    bucket = _workspace_bucket(state, workspace_id)
    sessions = bucket.setdefault("topup_sessions", {})
    if not isinstance(sessions, dict):
        sessions = {}
        bucket["topup_sessions"] = sessions

    stored = dict(session)
    stored["last_seen_at"] = format_iso_now()
    sessions[session_id] = stored
    save_billing_state(state_path, state)
    return {"billing_state_path": str(state_path), "session": stored}


def list_topup_sessions(
    *,
    workspace_id: str | None = None,
    agent_id: str = DEFAULT_AGENT_ID,
) -> tuple[list[dict[str, Any]], str]:
    state_path, state = ensure_billing_state(agent_id)
    results: list[dict[str, Any]] = []
    workspaces = state.get("workspaces")
    if not isinstance(workspaces, dict):
        return results, str(state_path)

    workspace_ids = [workspace_id] if workspace_id else list(workspaces.keys())
    for current_workspace_id in workspace_ids:
        bucket = workspaces.get(current_workspace_id)
        if not isinstance(bucket, dict):
            continue
        sessions = bucket.get("topup_sessions")
        if not isinstance(sessions, dict):
            continue
        for session in sessions.values():
            if isinstance(session, dict):
                results.append(session)

    results.sort(key=lambda item: str(item.get("created_at") or item.get("last_seen_at") or ""), reverse=True)
    return results, str(state_path)
