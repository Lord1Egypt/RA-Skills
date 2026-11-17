from __future__ import annotations

import logging

from .decision.engine import IntelligentDecisionEngine
from .decision.integrity import seal_record
from .domain import DomainControlPack, get_registry
from .governance.approval import apply_approval
from .models.schemas import (
    ApprovalRequest,
    DecisionRecord,
    DecisionRequest,
)
from .persistence.event_store import DomainEvent, EventStore, InMemoryEventStore
from .repository import DecisionRepository, InMemoryDecisionRepository
from .tenant import get_tenant

logger = logging.getLogger(__name__)


class DecisionNotFoundError(LookupError):
    pass


class DecisionService:
    def __init__(
        self,
        engine: IntelligentDecisionEngine | None = None,
        repository: DecisionRepository | None = None,
        event_store: EventStore | None = None,
        domain_packs: list[DomainControlPack] | None = None,
        fail_on_domain_violation: bool = False,
    ):
        self.engine = engine or IntelligentDecisionEngine()
        self.repository = repository or InMemoryDecisionRepository()
        self.event_store = event_store or InMemoryEventStore()
        self.domain_packs = domain_packs if domain_packs is not None else list(
            get_registry().all()
        )
        self.fail_on_domain_violation = fail_on_domain_violation

    def evaluate(self, request: DecisionRequest) -> DecisionRecord:
        self._run_domain_packs(request)
        result = self.engine.evaluate(request)
        normalized_request = request.model_copy(
            update={
                "decision_id": result.decision_id,
                "evaluation_as_of": result.evaluation_as_of,
            }
        )
        previous = self.repository.get(result.decision_id)
        record = DecisionRecord(
            request=normalized_request,
            result=result,
            revision=(previous.revision + 1) if previous else 1,
            parent_record_hash=previous.record_hash if previous else None,
        )
        record = seal_record(record)
        self.repository.put(record)
        logger.info(
            "decision sealed decision_id=%s revision=%d record_hash=%s status=%s",
            record.result.decision_id,
            record.revision,
            record.record_hash,
            record.result.status.value,
        )
        self._emit_event(
            "decision.evaluated",
            record.result.decision_id,
            {
                "revision": record.revision,
                "status": record.result.status.value,
                "record_hash": record.record_hash,
            },
        )
        return record

    def _run_domain_packs(self, request: DecisionRequest) -> None:
        violations = []
        for pack in self.domain_packs:
            violations.extend(pack.validate(request))
        if not violations:
            return
        codes = [v.code for v in violations]
        logger.warning("domain control pack violations: %s", codes)
        if self.fail_on_domain_violation and any(
            v.severity == "error" for v in violations
        ):
            blocking = [v.code for v in violations if v.severity == "error"]
            raise ValueError(
                "domain control pack blocked sealing: " + ", ".join(blocking)
            )

    def _emit_event(
        self, event_type: str, aggregate_id: str, payload: dict
    ) -> None:
        tenant = get_tenant()
        prev = self.event_store.last_hash(tenant)
        event = DomainEvent.create(event_type, aggregate_id, payload, prev, tenant)
        self.event_store.append(event)

    def get(self, decision_id: str) -> DecisionRecord:
        record = self.repository.get(decision_id)
        if record is None:
            raise DecisionNotFoundError(decision_id)
        return record

    def approve(self, decision_id: str, approval: ApprovalRequest) -> DecisionRecord:
        record = self.get(decision_id)
        updated = apply_approval(record, approval)
        updated = updated.model_copy(
            update={
                "revision": record.revision + 1,
                "parent_record_hash": record.record_hash,
                "record_hash": "",
            }
        )
        updated = seal_record(updated)
        self.repository.put(updated)
        logger.info(
            "decision approved decision_id=%s revision=%d record_hash=%s approved=%s approver=%s",
            decision_id,
            updated.revision,
            updated.record_hash,
            updated.approval.approved,
            updated.approval.approver,
        )
        self._emit_event(
            "decision.approved",
            decision_id,
            {
                "revision": updated.revision,
                "approved": updated.approval.approved,
                "approver": updated.approval.approver,
                "record_hash": updated.record_hash,
            },
        )
        return updated

    def history(self, decision_id: str) -> list[DecisionRecord]:
        if self.repository.get(decision_id) is None:
            raise DecisionNotFoundError(decision_id)
        return self.repository.history(decision_id)
