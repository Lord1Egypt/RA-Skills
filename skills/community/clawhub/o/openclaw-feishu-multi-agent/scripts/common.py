#!/usr/bin/env python3
"""Shared helpers for OpenClaw + Feishu multi-agent scripts."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any


PLACEHOLDER_VALUES = {"replace_me", "ou_replace_me", "/path/to/workspace", "/path/to/agentDir"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backup_file(path: Path) -> Path:
    backup_path = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup_path)
    return backup_path


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def is_placeholder(value: Any) -> bool:
    return not value or value in PLACEHOLDER_VALUES


def normalize_roles_path(path: str) -> Path:
    return Path(path).expanduser().resolve()


def load_roles(path: Path) -> tuple[str, list[dict[str, Any]]]:
    data = load_json(path)
    roles = data.get("roles")
    if not isinstance(roles, list) or not roles:
        raise ValueError("roles file must contain a non-empty 'roles' array")
    coordinators = [role for role in roles if role.get("isCoordinator")]
    if len(coordinators) != 1:
        raise ValueError("roles file must contain exactly one coordinator")
    for role in roles:
        for key in ("agentId", "roleName", "accountId", "openId", "responsibility"):
            if not role.get(key):
                raise ValueError(f"role {role!r} is missing required field: {key}")
        trigger_terms = role.get("triggerTerms", [])
        if not isinstance(trigger_terms, list) or not all(isinstance(x, str) and x for x in trigger_terms):
            raise ValueError(f"role {role['agentId']} has invalid triggerTerms")
    return data.get("systemName", "OpenClaw Feishu Multi-Agent"), roles


def find_coordinator(roles: list[dict[str, Any]]) -> dict[str, Any]:
    return next(role for role in roles if role["isCoordinator"])


def role_default_dir(state_dir: Path, role: dict[str, Any]) -> Path:
    return state_dir / "agents" / role["agentId"] / "agent"


def role_workspace(role: dict[str, Any], state_dir: Path) -> Path:
    raw = role.get("workspace")
    if raw and not is_placeholder(raw):
        return Path(raw).expanduser().resolve()
    raw = role.get("agentDir")
    if raw and not is_placeholder(raw):
        return Path(raw).expanduser().resolve()
    return role_default_dir(state_dir, role)


def role_agent_dir(role: dict[str, Any], state_dir: Path) -> Path:
    raw = role.get("agentDir")
    if raw and not is_placeholder(raw):
        return Path(raw).expanduser().resolve()
    return role_default_dir(state_dir, role)


def dotted_get(data: dict[str, Any], path: list[str], default: Any = None) -> Any:
    cur: Any = data
    for part in path:
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur
