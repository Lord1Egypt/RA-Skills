"""Shared runtime contract for memory-governor tooling."""

from .contract.capabilities import CAPABILITY_FAMILIES
from .contract.diagnosis_registry import DIAGNOSIS_REGISTRY, SEVERITY_ERROR, SEVERITY_WARN

__all__ = [
    "CAPABILITY_FAMILIES",
    "DIAGNOSIS_REGISTRY",
    "SEVERITY_ERROR",
    "SEVERITY_WARN",
]
