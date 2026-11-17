"""Shared CLI plumbing.

The single entrypoint (`ps.py`) dispatches on `argv[1]` and reads an
optional JSON object from stdin. Results print as one JSON object on
stdout; failures print `{"error": {...}}` and exit non-zero, carrying the
structured error type so a calling agent can branch on `not_supported` vs
`escalation_required` without parsing prose.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from errors import PromoStandardsError


def emit(payload: Any) -> None:
    print(json.dumps(payload, default=str))


def fail(error_type: str, message: str, exit_code: int = 1, **extra: Any) -> None:
    print(json.dumps({"error": {"type": error_type, "message": message,
                                **extra}}))
    sys.exit(exit_code)


def fail_from(exc: PromoStandardsError, exit_code: int = 1) -> None:
    """Emit a structured error straight from the exception."""
    print(json.dumps({"error": exc.as_dict()}, default=str))
    sys.exit(exit_code)


def read_stdin_json() -> dict[str, Any]:
    raw = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("bad_input", f"stdin is not valid JSON: {exc}")
    if not isinstance(payload, dict):
        fail("bad_input", "stdin JSON must be an object")
    return payload


def require(payload: dict, *keys: str) -> tuple:
    missing = [k for k in keys if not payload.get(k)]
    if missing:
        fail("bad_input", f"missing required field(s): {', '.join(missing)}")
    return tuple(payload[k] for k in keys)
