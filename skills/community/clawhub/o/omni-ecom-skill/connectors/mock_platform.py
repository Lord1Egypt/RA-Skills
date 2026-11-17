#!/usr/bin/env python3
"""In-memory connector for contract, policy and readback tests.

It is intentionally not a real platform adapter. ``dry_run`` is the default;
the optional in-memory mutation only proves the execution/readback contract.
"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock
from typing import Any

from .contract import ConnectorError, canonical_hash, utc_now


class MockPlatformConnector:
    connector_id = "mock-platform"
    platform = "mock"
    connector_version = "1.0.0"

    def __init__(self, initial_state: dict[str, dict[str, Any]] | None = None):
        self._state = deepcopy(initial_state or {"campaign": {"cmp-001": {"status": "paused", "budget": 1000}}})
        self._idempotency: dict[str, dict[str, Any]] = {}
        self._lock = RLock()

    def capabilities(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "connector_id": self.connector_id,
            "platform": self.platform,
            "connector_version": self.connector_version,
            "mode": "mock",
            "status": "sandbox_verified",
            "read_actions": ["campaign.get"],
            "write_actions": ["campaign.pause", "campaign.resume"],
            "conditional_write": True,
            "auth_type": "none",
            "rate_limit": {"requests_per_minute": 60},
            "verified_at": utc_now(),
        }

    def _get(self, resource: str, platform_id: str) -> dict[str, Any]:
        try:
            return self._state[resource][platform_id]
        except KeyError as exc:
            raise ConnectorError("unknown_target", f"mock target not found: {resource}/{platform_id}") from exc

    def read(self, resource: str, platform_id: str) -> dict[str, Any]:
        data = deepcopy(self._get(resource, platform_id))
        return {
            "status": "PASS",
            "connector_id": self.connector_id,
            "platform": self.platform,
            "resource": resource,
            "platform_id": platform_id,
            "data": data,
            "source_fingerprint": canonical_hash({"resource": resource, "platform_id": platform_id, "data": data}),
            "read_at": utc_now(),
        }

    def propose_write(self, action: dict[str, Any]) -> dict[str, Any]:
        operation = str(action.get("operation", ""))
        target = action.get("target") or {}
        if operation not in {"campaign.pause", "campaign.resume"}:
            raise ConnectorError("unsupported_operation", f"mock operation not supported: {operation}")
        if not isinstance(target, dict) or not target.get("resource") or not target.get("platform_id"):
            raise ConnectorError("invalid_target", "target must include resource and platform_id")
        self._get(str(target["resource"]), str(target["platform_id"]))
        return {
            "status": "proposed",
            "action_id": action.get("action_id"),
            "operation": operation,
            "target": {"resource": target["resource"], "platform_id": target["platform_id"]},
            "approval_required": True,
            "approval_state": action.get("approval_state", "pending"),
            "before_snapshot": self.read(str(target["resource"]), str(target["platform_id"])),
            "proposal_hash": canonical_hash(action),
        }

    def execute(self, action: dict[str, Any], *, approval_state: str, idempotency_key: str,
                dry_run: bool = True, expected_data_sha256: str | None = None) -> dict[str, Any]:
        with self._lock:
            return self._execute(action, approval_state=approval_state, idempotency_key=idempotency_key,
                                 dry_run=dry_run, expected_data_sha256=expected_data_sha256)

    def _execute(self, action: dict[str, Any], *, approval_state: str, idempotency_key: str,
                 dry_run: bool, expected_data_sha256: str | None) -> dict[str, Any]:
        if approval_state != "approved":
            raise ConnectorError("approval_required", "connector execution requires approval_state=approved")
        if not idempotency_key:
            raise ConnectorError("idempotency_required", "idempotency_key is required")
        if not isinstance(dry_run, bool):
            raise ConnectorError("invalid_mode", "dry_run must be boolean")
        request_hash = canonical_hash(action)
        if idempotency_key in self._idempotency:
            previous = self._idempotency[idempotency_key]
            if (previous["request_hash"] != request_hash or previous["dry_run"] != dry_run or
                previous['expected_data_sha256'] != expected_data_sha256):
                raise ConnectorError("idempotency_conflict", "key is already bound to another request or execution mode")
            return deepcopy(previous)
        target = action.get("target") or {}
        resource = str(target.get("resource", ""))
        platform_id = str(target.get("platform_id", ""))
        current = self._get(resource, platform_id)
        operation = str(action.get("operation", ""))
        desired = "paused" if operation == "campaign.pause" else "active" if operation == "campaign.resume" else None
        if desired is None:
            raise ConnectorError("unsupported_operation", f"mock operation not supported: {operation}")
        if resource != 'campaign' or ('changes' in action and action['changes'] != {'status': desired}):
            raise ConnectorError('operation_changes_mismatch', 'changes must match the requested operation')
        if expected_data_sha256 is not None and canonical_hash(current) != expected_data_sha256:
            raise ConnectorError('precondition_failed', 'target changed since approved snapshot')
        before = deepcopy(current)
        if not dry_run:
            current["status"] = desired
        after = deepcopy(current)
        result = {
            "status": "dry_run" if dry_run else "executed",
            "simulated": True,
            "dry_run": dry_run,
            "expected_data_sha256": expected_data_sha256,
            "evidence_kind": "synthetic_mock_not_platform_execution",
            "connector_id": self.connector_id,
            "platform": self.platform,
            "operation": operation,
            "target": {"resource": resource, "platform_id": platform_id},
            "before": before,
            "after": after,
            "idempotency_key": idempotency_key,
            "request_hash": request_hash,
            "started_at": utc_now(),
            "finished_at": utc_now(),
        }
        self._idempotency[idempotency_key] = deepcopy(result)
        return result

    def readback(self, action: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(expected, dict) or not expected:
            raise ConnectorError("expected_state_required", "readback requires a nonempty expected state")
        canonical_hash(expected)
        target = action.get("target") or {}
        actual = self.read(str(target.get("resource", "")), str(target.get("platform_id", "")))
        actual_data = actual["data"]
        matched = all(key in actual_data and canonical_hash(actual_data[key]) == canonical_hash(value)
                      for key, value in expected.items())
        return {
            "status": "verified" if matched else "blocked",
            "matched": matched,
            "simulated": True,
            "evidence_kind": "synthetic_mock_not_platform_readback",
            "expected": deepcopy(expected),
            "actual": actual_data,
            "readback_at": utc_now(),
            "source_fingerprint": actual["source_fingerprint"],
        }
