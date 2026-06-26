"""Capability-family contract for memory-adjacent skills."""

from __future__ import annotations

CAPABILITY_FAMILIES = (
    "writer",
    "consumer",
    "compiler",
    "promoter",
)

HIGH_RISK_CAPABILITY_FAMILIES = {
    "promoter",
}


def is_known_capability_family(value: str) -> bool:
    return value in CAPABILITY_FAMILIES
