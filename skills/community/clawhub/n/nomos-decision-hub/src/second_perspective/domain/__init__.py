"""Domain control packs (v0.5).

A DomainControlPack encodes domain-specific guardrails (regulatory thresholds,
mandatory disclosures, hard constraints) that sit *outside* the deterministic
engine. Packs never alter the engine's verdict; they surface violations as
warnings and, optionally, block sealing when ``fail_on_violation`` is enabled on
the service. This keeps the engine's "never invent" invariant intact while
allowing operators to attach compliance policy.
"""

from .base import (
    DomainControlPack,
    DomainPackRegistry,
    DomainViolation,
    get_registry,)
from .packs import FinanceRiskControlPack, register_default_packs

__all__ = [
    "DomainControlPack",
    "DomainPackRegistry",
    "DomainViolation",
    "get_registry",
    "FinanceRiskControlPack",
    "register_default_packs",
]
