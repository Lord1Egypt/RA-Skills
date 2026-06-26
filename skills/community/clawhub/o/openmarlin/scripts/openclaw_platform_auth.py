"""Helpers for storing OpenMarlin platform credentials in OpenClaw auth profiles."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


PLATFORM_AUTH_PROVIDER = "openmarlin-platform"
DEFAULT_PROFILE_ID = f"{PLATFORM_AUTH_PROVIDER}:default"
DEFAULT_AGENT_ID = "main"


def resolve_openclaw_state_dir() -> Path:
    override = os.environ.get("OPENCLAW_STATE_DIR", "").strip()
    if override:
        return Path(override).expanduser()
    return Path.home() / ".openclaw"


def resolve_agent_dir(agent_id: str = DEFAULT_AGENT_ID) -> Path:
    return resolve_openclaw_state_dir() / "agents" / agent_id / "agent"


def resolve_auth_store_path(agent_id: str = DEFAULT_AGENT_ID) -> Path:
    return resolve_agent_dir(agent_id) / "auth-profiles.json"


def ensure_auth_store(agent_id: str = DEFAULT_AGENT_ID) -> tuple[Path, dict[str, Any]]:
    agent_dir = resolve_agent_dir(agent_id)
    agent_dir.mkdir(parents=True, exist_ok=True)
    try:
        agent_dir.chmod(0o700)
    except OSError:
        pass

    auth_path = resolve_auth_store_path(agent_id)
    if not auth_path.exists():
        store: dict[str, Any] = {"version": 1, "profiles": {}}
        save_auth_store(auth_path, store)
        return auth_path, store

    with auth_path.open("r", encoding="utf-8") as handle:
        raw = handle.read().strip()
    if not raw:
        store = {"version": 1, "profiles": {}}
        save_auth_store(auth_path, store)
        return auth_path, store

    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise SystemExit(f"Invalid auth profile store at {auth_path}: expected JSON object.")
    parsed.setdefault("version", 1)
    profiles = parsed.get("profiles")
    if not isinstance(profiles, dict):
        parsed["profiles"] = {}
    return auth_path, parsed


def save_auth_store(path: Path, store: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="auth-profiles-", suffix=".json", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(store, handle, indent=2, sort_keys=True)
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


def upsert_platform_api_key(
    *,
    secret: str,
    profile_id: str = DEFAULT_PROFILE_ID,
    agent_id: str = DEFAULT_AGENT_ID,
    metadata: dict[str, str] | None = None,
) -> dict[str, Any]:
    auth_path, store = ensure_auth_store(agent_id)
    profiles = store.setdefault("profiles", {})
    if not isinstance(profiles, dict):
        raise SystemExit(f"Invalid auth profile store at {auth_path}: profiles must be an object.")

    credential: dict[str, Any] = {
        "type": "api_key",
        "provider": PLATFORM_AUTH_PROVIDER,
        "key": secret,
    }
    if metadata:
        credential["metadata"] = metadata

    profiles[profile_id] = credential
    save_auth_store(auth_path, store)
    return {"auth_store_path": str(auth_path), "profile_id": profile_id, "agent_id": agent_id}


def resolve_platform_api_key(
    *,
    profile_id: str = DEFAULT_PROFILE_ID,
    agent_id: str = DEFAULT_AGENT_ID,
) -> tuple[str | None, dict[str, Any] | None, str]:
    auth_path, store = ensure_auth_store(agent_id)
    profiles = store.get("profiles")
    if not isinstance(profiles, dict):
        return None, None, str(auth_path)

    profile = profiles.get(profile_id)
    if not isinstance(profile, dict):
        return None, None, str(auth_path)
    if profile.get("type") != "api_key":
        return None, profile, str(auth_path)
    key = profile.get("key")
    if not isinstance(key, str) or not key.strip():
        return None, profile, str(auth_path)
    return key.strip(), profile, str(auth_path)
