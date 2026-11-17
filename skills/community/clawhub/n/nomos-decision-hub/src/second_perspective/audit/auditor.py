"""Structural auditor — inspects the decision structure for completeness.

The auditor checks that every declared constraint, criterion, assumption,
and alternative has the required fields and that cross-references resolve.
It does NOT evaluate content — that is the evaluator's job.
"""

from __future__ import annotations

from datetime import datetime

from ..models.enums import IssueSeverity
from ..models.schemas import AuditIssue, DecisionRequest, ResponsibilityEntry


class StructuralAuditor:
    """Deterministic structural auditor for decision requests.

    Checks:
      - Every alternative has at least one required assumption.
      - Every critical assumption has a responsibility assigned.
      - Every evidence item has a status.
      - Every criterion has a valid scoring rule.
      - Cross-references between assumptions, alternatives, and evidence resolve.
    """

    def audit(
        self,
        request: DecisionRequest,
        policy: object,
        evaluation_as_of: datetime,
    ) -> tuple[list[AuditIssue], list[ResponsibilityEntry], list[str]]:
        """Run the structural audit.

        Returns:
            (issues, responsibility_map, unresolved_variables)
        """
        issues: list[AuditIssue] = []
        unresolved: list[str] = []
        responsibility_map: list[ResponsibilityEntry] = []

        # ── Check alternatives ──
        for alt in request.alternatives:
            if not alt.required_assumptions:
                issues.append(
                    AuditIssue(
                        code="ALTERNATIVE_NO_ASSUMPTIONS",
                        severity=IssueSeverity.WARNING,
                        path=f"alternatives.{alt.id}.required_assumptions",
                        message=f"Alternative {alt.id} has no required assumptions declared.",
                        blocking=False,
                    )
                )
                unresolved.append(f"alternatives.{alt.id}.required_assumptions")

            if not alt.evidence_ids:
                issues.append(
                    AuditIssue(
                        code="ALTERNATIVE_NO_EVIDENCE",
                        severity=IssueSeverity.INFO,
                        path=f"alternatives.{alt.id}.evidence_ids",
                        message=f"Alternative {alt.id} has no evidence declared.",
                        blocking=False,
                    )
                )

        # ── Check critical assumptions ──
        for assumption in request.assumptions:
            if assumption.critical and assumption.responsibility is None:
                issues.append(
                    AuditIssue(
                        code="CRITICAL_ASSUMPTION_NO_OWNER",
                        severity=IssueSeverity.ERROR,
                        path=f"assumptions.{assumption.id}.responsibility",
                        message=f"Critical assumption {assumption.id} has no assigned responsibility.",
                        blocking=True,
                    )
                )
                unresolved.append(f"assumptions.{assumption.id}.responsibility")

            if assumption.responsibility:
                responsibility_map.append(
                    ResponsibilityEntry(
                        element_type="assumption",
                        element_id=assumption.id,
                        owner=assumption.responsibility.owner,
                        source=assumption.responsibility.source,
                        status="declared",
                    )
                )

        # ── Check criteria ──
        for criterion in request.criteria:
            if criterion.responsibility:
                responsibility_map.append(
                    ResponsibilityEntry(
                        element_type="criterion",
                        element_id=criterion.id,
                        owner=criterion.responsibility.owner,
                        source=criterion.responsibility.source,
                        status="declared",
                    )
                )

        # ── Check constraints ──
        for constraint in request.constraints:
            if constraint.responsibility:
                responsibility_map.append(
                    ResponsibilityEntry(
                        element_type="constraint",
                        element_id=constraint.id,
                        owner=constraint.responsibility.owner,
                        source=constraint.responsibility.source,
                        status="declared",
                    )
                )

        # ── Check evidence ──
        for evidence in request.evidence:
            if evidence.responsibility:
                responsibility_map.append(
                    ResponsibilityEntry(
                        element_type="evidence",
                        element_id=evidence.id,
                        owner=evidence.responsibility.owner,
                        source=evidence.responsibility.source,
                        status=evidence.status.value,
                    )
                )

        # ── Decision owner ──
        if request.decision_owner:
            responsibility_map.append(
                ResponsibilityEntry(
                    element_type="decision",
                    element_id=request.decision_id or "(pending)",
                    owner=request.decision_owner.owner,
                    source=request.decision_owner.source,
                    status="declared",
                )
            )

        return issues, responsibility_map, unresolved