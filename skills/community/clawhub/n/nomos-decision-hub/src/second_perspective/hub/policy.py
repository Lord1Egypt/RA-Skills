"""Hub-level policy — configurable guardrails for the IntelligentDecisionHub."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ..models.hub import HubPolicySnapshot


class HubPolicy:
    """Configurable guardrails for the IntelligentDecisionHub orchestrator.

    Controls which optional analyses are run and their budgets.
    """

    def __init__(
        self,
        *,
        policy_id: str | None = None,
        version: str = "0.3.0",
        max_scenarios: int = 10,
        run_causal_reconstruction: bool = True,
        run_cognitive_audit: bool = True,
        build_information_priorities: bool = True,
    ) -> None:
        self.policy_id = policy_id or f"HUB-POL-{uuid4().hex[:8].upper()}"
        self.version = version
        self.max_scenarios = max_scenarios
        self.run_causal_reconstruction = run_causal_reconstruction
        self.run_cognitive_audit = run_cognitive_audit
        self.build_information_priorities = build_information_priorities

    def snapshot(self) -> HubPolicySnapshot:
        """Return an immutable snapshot of the current hub policy."""
        return HubPolicySnapshot(
            policy_id=self.policy_id,
            version=self.version,
            max_scenarios=self.max_scenarios,
            run_causal_reconstruction=self.run_causal_reconstruction,
            run_cognitive_audit=self.run_cognitive_audit,
            build_information_priorities=self.build_information_priorities,
        )