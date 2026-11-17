"""Stable command-result helpers shared by every CLI command."""

from __future__ import annotations

import json
from typing import Any


def make_result(
    *,
    status: str,
    code: str,
    message: str,
    artifacts: list[str] | None = None,
    next_actions: list[dict[str, Any]] | None = None,
    needs_user_input: list[dict[str, Any]] | None = None,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the public, JSON-serializable command contract."""

    return {
        "status": status,
        "code": code,
        "message": message,
        "artifacts": artifacts or [],
        "next_actions": next_actions or [],
        "needs_user_input": needs_user_input or [],
        "data": data or {},
    }


def render_result(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)

