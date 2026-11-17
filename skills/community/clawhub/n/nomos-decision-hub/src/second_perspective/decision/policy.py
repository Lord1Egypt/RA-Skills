"""Decision policy — configurable guardrails for the deterministic engine.

The policy is a snapshot of the parameters that control how the engine
evaluates decisions.  It is sealed into the DecisionResult so that
any re-evaluation can be checked against the same policy.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from ..models.schemas import PolicySnapshot


class DecisionPolicy:
    """Configurable guardrails for the deterministic engine.

    Defaults are conservative: every alternative must be complete, critical
    evidence quality is required, and sensitivity delta is 10%.
    """

    def __init__(
        self,
        *,
        policy_id: str | None = None,
        version: str = "0.3.0",
        require_all_alternatives_complete: bool = True,
        require_critical_evidence_quality: bool = True,
        critical_evidence_quality_threshold: Decimal = Decimal("0.7"),
        sensitivity_delta: Decimal = Decimal("0.1"),
    ) -> None:
        self.policy_id = policy_id or f"POL-{uuid4().hex[:8].upper()}"
        self.version = version
        self.require_all_alternatives_complete = require_all_alternatives_complete
        self.require_critical_evidence_quality = require_critical_evidence_quality
        self.critical_evidence_quality_threshold = critical_evidence_quality_threshold
        self.sensitivity_delta = sensitivity_delta

    def snapshot(self) -> PolicySnapshot:
        """Return an immutable snapshot of the current policy."""
        return PolicySnapshot(
            policy_id=self.policy_id,
            version=self.version,
            require_all_alternatives_complete=self.require_all_alternatives_complete,
            require_critical_evidence_quality=self.require_critical_evidence_quality,
            critical_evidence_quality_threshold=self.critical_evidence_quality_threshold,
            sensitivity_delta=self.sensitivity_delta,
        )