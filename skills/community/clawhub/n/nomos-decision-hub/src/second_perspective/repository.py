"""In-memory decision repository (development default)."""

from __future__ import annotations

from threading import RLock
from typing import Protocol

from .decision.integrity import verify_chain, verify_record
from .models.schemas import DecisionRecord


class DecisionRepository(Protocol):
    """Protocol for decision-record persistence."""

    def put(self, record: DecisionRecord) -> None: ...

    def get(self, decision_id: str) -> DecisionRecord | None: ...

    def history(self, decision_id: str) -> list[DecisionRecord]: ...


class InMemoryDecisionRepository:
    """Thread-safe in-memory development store for decision records.

    Integrity verification (hash-chain) is enforced on read to catch
    tampering at the storage layer.
    """

    def __init__(self) -> None:
        self._records: dict[str, list[DecisionRecord]] = {}
        self._lock = RLock()

    def put(self, record: DecisionRecord) -> None:
        with self._lock:
            if not verify_record(record):
                raise ValueError("record_hash does not match the decision record payload")
            decision_id = record.result.decision_id
            chain = self._records.setdefault(decision_id, [])
            if chain:
                expected_revision = chain[-1].revision + 1
                if record.revision != expected_revision:
                    raise ValueError(
                        f"revision must be {expected_revision} for {decision_id}; "
                        f"received {record.revision}"
                    )
                if record.parent_record_hash != chain[-1].record_hash:
                    raise ValueError("parent_record_hash does not match latest revision")
            chain.append(record.model_copy(deep=True))

    def get(self, decision_id: str) -> DecisionRecord | None:
        with self._lock:
            chain = self._records.get(decision_id)
            if not chain:
                return None
            if not verify_chain(chain):
                raise ValueError(f"integrity verification failed for {decision_id}")
            return chain[-1].model_copy(deep=True)

    def history(self, decision_id: str) -> list[DecisionRecord]:
        with self._lock:
            chain = self._records.get(decision_id)
            if not chain:
                return []
            if not verify_chain(chain):
                raise ValueError(f"integrity verification failed for {decision_id}")
            return [r.model_copy(deep=True) for r in chain]