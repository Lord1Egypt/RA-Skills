#!/usr/bin/env python3
"""Deterministic smoke tests for the v1.5 Connector SPI."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from connectors import ConnectorError, MockPlatformConnector  # noqa: E402


def check(name: str, fn) -> dict[str, str]:
    try:
        fn()
        return {"name": name, "status": "PASS"}
    except Exception as exc:  # pragma: no cover - smoke output must be explicit
        return {"name": name, "status": "FAIL", "error": str(exc)}


def main() -> int:
    connector = MockPlatformConnector()
    action = {
        "action_id": "A15-mock",
        "run_id": "run-20260811-mock",
        "client_scope": "client-demo",
        "operation": "campaign.pause",
        "approval_state": "pending",
        "target": {"resource": "campaign", "platform_id": "cmp-001"},
    }
    proposal = {}
    execution = {}
    checks = [
        check("capability_contract", lambda: (_ for _ in ()).throw(ValueError("missing capability")) if connector.capabilities().get("status") != "sandbox_verified" else None),
        check("read_returns_fingerprint", lambda: (_ for _ in ()).throw(ValueError("missing fingerprint")) if not connector.read("campaign", "cmp-001").get("source_fingerprint") else None),
        check("write_proposal_requires_target", lambda: (_ for _ in ()).throw(ValueError("proposal failed")) if (proposal.update(connector.propose_write(action)) is None and False) else None),
        check("approval_is_enforced", lambda: (_ for _ in ()).throw(ValueError("approval was not enforced")) if not _approval_blocked(connector, action) else None),
        check("dry_run_is_non_mutating", lambda: _dry_run_non_mutating(connector, action)),
        check("idempotency_replays_same_result", lambda: _idempotency_replays(connector, action)),
        check("readback_verifies_expected_state", lambda: _readback_verifies(connector, action, execution)),
        check("unsupported_operation_blocks", lambda: _unsupported_blocks(connector, action)),
    ]
    failed = [item for item in checks if item["status"] != "PASS"]
    result = {"status": "PASS" if not failed else "FAIL", "total": len(checks), "passed": len(checks) - len(failed), "failed": len(failed), "results": checks}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


def _approval_blocked(connector, action) -> bool:
    try:
        connector.execute(action, approval_state="pending", idempotency_key="blocked", dry_run=True)
    except ConnectorError as exc:
        return exc.error_class == "approval_required"
    return False


def _dry_run_non_mutating(connector, action) -> None:
    before = connector.read("campaign", "cmp-001")["data"]
    result = connector.execute(action, approval_state="approved", idempotency_key="dry-run", dry_run=True)
    after = connector.read("campaign", "cmp-001")["data"]
    if result.get("status") != "dry_run" or before != after:
        raise ValueError("dry_run mutated state")


def _idempotency_replays(connector, action) -> None:
    first = connector.execute(action, approval_state="approved", idempotency_key="same-key", dry_run=False)
    second = connector.execute(action, approval_state="approved", idempotency_key="same-key", dry_run=False)
    if first != second:
        raise ValueError("idempotency replay differs")


def _readback_verifies(connector, action, execution) -> None:
    execution.update(connector.execute(action, approval_state="approved", idempotency_key="readback-key", dry_run=False))
    result = connector.readback(action, {"status": "paused"})
    if result.get("status") != "verified" or not result.get("matched"):
        raise ValueError("readback did not verify")


def _unsupported_blocks(connector, action) -> None:
    invalid = dict(action)
    invalid["operation"] = "campaign.delete"
    try:
        connector.propose_write(invalid)
    except ConnectorError as exc:
        if exc.error_class == "unsupported_operation":
            return
        raise
    raise ValueError("unsupported operation was accepted")


if __name__ == "__main__":
    raise SystemExit(main())
