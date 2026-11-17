"""Built-in domain control packs (v0.5)."""

from __future__ import annotations

from .base import DomainControlPack, DomainViolation


class FinanceRiskControlPack:
    """Example domain pack.

    Flags multi-alternative decisions that do not declare an explicit
    risk-owner responsibility. The engine itself never invents a responsible
    party; this pack only *observes* the omission and warns the operator.
    """

    id = "finance-risk-control"
    description = (
        "Flags multi-alternative decisions lacking an explicit risk-owner "
        "responsibility declaration."
    )

    def validate(self, request: "object") -> list[DomainViolation]:
        violations: list[DomainViolation] = []
        try:
            alternatives = getattr(request, "alternatives", None) or []
            if len(alternatives) <= 1:
                return violations
            responsibility = getattr(request, "responsibility", None)
            if not responsibility:
                violations.append(
                    DomainViolation(
                        pack_id=self.id,
                        code="NO_EXPLICIT_RISK_OWNER",
                        message=(
                            "Multi-alternative decision should declare an explicit "
                            "risk-owner responsibility."
                        ),
                        severity="warning",
                    )
                )
        except Exception:
            # A domain pack must never crash the deterministic pipeline.
            return violations
        return violations


def register_default_packs() -> None:
    from .base import get_registry

    registry = get_registry()
    registry.register(FinanceRiskControlPack())
