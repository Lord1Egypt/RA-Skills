"""Minimal reconciliation engine for capability claims and host authorization."""

from __future__ import annotations

from dataclasses import dataclass, field

from memory_governor.contract.capabilities import HIGH_RISK_CAPABILITY_FAMILIES
from memory_governor.contract.diagnosis_registry import (
    DIAGNOSIS_REGISTRY,
    SEVERITY_ERROR,
    SEVERITY_WARN,
)

from .diagnostics import StructuredDiagnostic


@dataclass
class CapabilityDeclaration:
    families: list[str] = field(default_factory=list)
    source_artifact: str = "skill contract"


@dataclass
class AuthorizationPolicy:
    allowed_capabilities: list[str] = field(default_factory=list)
    source_artifact: str = "host manifest"


@dataclass
class DiagnosisConfig:
    enabled_types: list[str] = field(default_factory=list)

    def allows(self, diagnosis_type: str) -> bool:
        return not self.enabled_types or diagnosis_type in self.enabled_types


def reconcile_capability_contract(
    declaration: CapabilityDeclaration,
    authorization: AuthorizationPolicy,
    diagnosis: DiagnosisConfig,
) -> list[StructuredDiagnostic]:
    diagnostics: list[StructuredDiagnostic] = []
    declared = set(declaration.families)
    allowed = set(authorization.allowed_capabilities)

    if not declared and allowed and diagnosis.allows("MissingCapabilityDeclaration"):
        diagnostics.append(
            StructuredDiagnostic(
                diagnosis_type="MissingCapabilityDeclaration",
                severity=DIAGNOSIS_REGISTRY["MissingCapabilityDeclaration"]["severity"],
                primary_cause="host_authorization_without_skill_claim",
                secondary_contributors=["authorization_present", "claim_missing"],
                artifacts_involved=[authorization.source_artifact, declaration.source_artifact],
                coverage_gaps=["capability_claim"],
                repair_hints=[
                    "Add a machine-readable capability declaration to the skill contract."
                ],
            )
        )

    undeclared_allowed = sorted(allowed - declared)
    if undeclared_allowed and diagnosis.allows("ManifestSkillContractMismatch"):
        diagnostics.append(
            StructuredDiagnostic(
                diagnosis_type="ManifestSkillContractMismatch",
                severity=DIAGNOSIS_REGISTRY["ManifestSkillContractMismatch"]["severity"],
                primary_cause="host_authorizes_undeclared_capability",
                secondary_contributors=undeclared_allowed,
                artifacts_involved=[authorization.source_artifact, declaration.source_artifact],
                repair_hints=[
                    "Align host authorization with declared capability families.",
                    "Or expand the skill contract if the capability is real.",
                ],
            )
        )

    for family in sorted(declared & HIGH_RISK_CAPABILITY_FAMILIES):
        if family not in allowed and diagnosis.allows("UnauthorizedPromotionPath"):
            diagnostics.append(
                StructuredDiagnostic(
                    diagnosis_type="UnauthorizedPromotionPath",
                    severity=SEVERITY_ERROR,
                    primary_cause="high_risk_capability_missing_host_authorization",
                    secondary_contributors=[family, "claim_without_authorization"],
                    capability_family=family,
                    artifacts_involved=[declaration.source_artifact, authorization.source_artifact],
                    repair_hints=[
                        f"Explicitly authorize {family} in the host manifest.",
                        "Or remove the high-risk capability claim from the skill contract.",
                    ],
                )
            )

    if declared and not allowed and diagnosis.allows("ProvisionalCapabilityDiagnosis"):
        diagnostics.append(
            StructuredDiagnostic(
                diagnosis_type="ProvisionalCapabilityDiagnosis",
                severity=SEVERITY_WARN,
                primary_cause="declared_capability_without_host_authorization_context",
                secondary_contributors=sorted(declared),
                provisional=True,
                artifacts_involved=[declaration.source_artifact, authorization.source_artifact],
                coverage_gaps=["host_authorization"],
                repair_hints=[
                    "Add host-side authorization to confirm which capabilities are active in this environment."
                ],
            )
        )

    return diagnostics
