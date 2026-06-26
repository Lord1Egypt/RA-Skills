"""Contract-level constants shared by docs-facing tools."""

from .capabilities import CAPABILITY_FAMILIES
from .diagnosis_registry import DIAGNOSIS_REGISTRY, DIAGNOSIS_TYPES, SEVERITY_ERROR, SEVERITY_WARN
from .reconciliation_policy import CLAIM_SOURCE, HOST_SOURCE, OBSERVED_SOURCE, SOURCE_PRECEDENCE

__all__ = [
    "CAPABILITY_FAMILIES",
    "CLAIM_SOURCE",
    "DIAGNOSIS_REGISTRY",
    "DIAGNOSIS_TYPES",
    "HOST_SOURCE",
    "OBSERVED_SOURCE",
    "SEVERITY_ERROR",
    "SEVERITY_WARN",
    "SOURCE_PRECEDENCE",
]
