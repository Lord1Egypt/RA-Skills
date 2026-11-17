"""Approval logic — human-gate for decision records.

The engine never approves its own decisions.  This module provides the
deterministic mechanics for recording a human approval or rejection.
"""

from __future__ import annotations

from datetime import datetime, timezone

from ..models.enums import DecisionStatus
from ..models.schemas import ApprovalRecord, ApprovalRequest, DecisionRecord


class ApprovalError(ValueError):
    """Raised when an approval operation cannot be applied."""


def apply_approval(
    record: DecisionRecord,
    approval: ApprovalRequest,
) -> DecisionRecord:
    """Apply a human approval decision to a decision record.

    Returns a new DecisionRecord with the approval attached and the status
    updated to APPROVED or REJECTED.
    """
    if record.approval is not None:
        raise ApprovalError("Decision already has an approval record")

    if record.result.status not in (
        DecisionStatus.HUMAN_APPROVAL_REQUIRED,
        DecisionStatus.EVIDENCE_PENDING,
    ):
        raise ApprovalError(
            f"Cannot approve decision in status {record.result.status.value}"
        )

    new_status = DecisionStatus.APPROVED if approval.approved else DecisionStatus.REJECTED

    approval_record = ApprovalRecord(
        approved=approval.approved,
        approver=approval.approver,
        authorization_ref=approval.authorization_ref,
        note=approval.note,
        approved_at=datetime.now(timezone.utc),
    )

    updated_result = record.result.model_copy(update={"status": new_status})
    return record.model_copy(
        update={
            "approval": approval_record,
            "result": updated_result,
        }
    )