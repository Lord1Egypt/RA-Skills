#!/usr/bin/env python3
"""Small, deterministic Connector SPI used by platform adapters."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Protocol


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_hash(value: Any) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


class ConnectorError(ValueError):
    """A fail-closed connector error with a stable class for audit logs."""

    def __init__(self, error_class: str, message: str):
        super().__init__(message)
        self.error_class = error_class


class ConnectorProtocol(Protocol):
    def capabilities(self) -> dict[str, Any]: ...

    def read(self, resource: str, platform_id: str) -> dict[str, Any]: ...

    def propose_write(self, action: dict[str, Any]) -> dict[str, Any]: ...

    def execute(self, action: dict[str, Any], *, approval_state: str, idempotency_key: str,
                dry_run: bool = True, expected_data_sha256: str | None = None) -> dict[str, Any]: ...

    def readback(self, action: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]: ...
