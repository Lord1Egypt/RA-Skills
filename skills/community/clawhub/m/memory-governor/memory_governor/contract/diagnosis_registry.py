"""Named diagnosis types and severity defaults for governance audit output."""

from __future__ import annotations

SEVERITY_ERROR = "ERROR"
SEVERITY_WARN = "WARN"

DIAGNOSIS_REGISTRY = {
    "MissingCapabilityDeclaration": {
        "severity": SEVERITY_WARN,
        "summary": "Skill is missing a machine-readable capability declaration.",
    },
    "InvalidCapabilityDeclaration": {
        "severity": SEVERITY_ERROR,
        "summary": "Capability declaration exists but cannot be parsed or validated.",
    },
    "UnknownCapabilityFamily": {
        "severity": SEVERITY_ERROR,
        "summary": "Capability declaration references a family outside the supported taxonomy.",
    },
    "ConflictingCapabilityDeclaration": {
        "severity": SEVERITY_ERROR,
        "summary": "Capability declarations disagree across sources.",
    },
    "ManifestSkillContractMismatch": {
        "severity": SEVERITY_ERROR,
        "summary": "Host authorization and skill contract disagree on effective capability scope.",
    },
    "CanonicalCompiledBoundaryViolation": {
        "severity": SEVERITY_ERROR,
        "summary": "Compiled view output is being treated as canonical truth.",
    },
    "UnauthorizedPromotionPath": {
        "severity": SEVERITY_ERROR,
        "summary": "A promotion-capable path is active without explicit authorization.",
    },
    "ProvisionalCapabilityDiagnosis": {
        "severity": SEVERITY_WARN,
        "summary": "Observed behavior suggests a provisional capability classification.",
    },
}

DIAGNOSIS_TYPES = tuple(DIAGNOSIS_REGISTRY.keys())
