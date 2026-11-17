from __future__ import annotations

import hashlib
import hmac
import logging
from typing import Any

from ..canonical import canonical_json
from ..models.schemas import AlgorithmAuditEvent

logger = logging.getLogger(__name__)


class AlgorithmAuditLedger:
    """Deterministic, hash-chained execution events without hidden timestamps."""

    def __init__(self, events: list[AlgorithmAuditEvent] | None = None) -> None:
        if events and not verify_algorithm_audit(events):
            raise ValueError("initial algorithm audit events fail integrity verification")
        self._events = [event.model_copy(deep=True) for event in (events or [])]

    @property
    def events(self) -> list[AlgorithmAuditEvent]:
        return [event.model_copy(deep=True) for event in self._events]

    @property
    def root_hash(self) -> str | None:
        return self._events[-1].event_hash if self._events else None

    def append(
        self,
        *,
        stage: str,
        rule_id: str,
        operation: str,
        inputs: dict[str, Any] | None = None,
        output: Any = None,
        references: list[str] | None = None,
    ) -> AlgorithmAuditEvent:
        payload = {
            "sequence": len(self._events) + 1,
            "stage": stage,
            "rule_id": rule_id,
            "operation": operation,
            "inputs": inputs or {},
            "output": output,
            "references": references or [],
            "previous_event_hash": self.root_hash,
        }
        digest = hashlib.sha256(canonical_json(payload)).hexdigest()
        event = AlgorithmAuditEvent(**payload, event_hash=digest)
        self._events.append(event)
        logger.info(
            "audit event appended sequence=%d stage=%s rule_id=%s operation=%s event_hash=%s",
            event.sequence,
            event.stage,
            event.rule_id,
            event.operation,
            event.event_hash,
        )
        return event.model_copy(deep=True)


def verify_algorithm_audit(
    events: list[AlgorithmAuditEvent],
    root_hash: str | None = None,
) -> bool:
    if not events:
        return False
    previous_hash: str | None = None
    for expected_sequence, event in enumerate(events, start=1):
        if event.sequence != expected_sequence:
            return False
        if event.previous_event_hash != previous_hash:
            return False
        payload = event.model_dump(mode="json", exclude={"event_hash"})
        expected_hash = hashlib.sha256(canonical_json(payload)).hexdigest()
        if not hmac.compare_digest(event.event_hash, expected_hash):
            return False
        previous_hash = event.event_hash
    return root_hash is None or hmac.compare_digest(previous_hash or "", root_hash)
