"""LLM compliance layer — v0.4 upgrade (G3: LLM adjudication gap).

Problem: earlier implementations let LLM output enter convergence and
scoring decisions, which conflicts with NOMOS's "no subjective /
probabilistic inference" principle.  The problem isn't using LLM — it's
giving LLM adjudicatory power.

This layer defines a three-tier permission model:

  T1  ANNOTATION   — extract existing assumptions / evidence references
  T2  PROPOSAL     — propose possible interaction pairs (strength empty)
  T3  NARRATIVE    — generate natural-language explanation of a verdict
                     that has already been reached

Invariants (L-1 through L-3):
  L-1  No adjudication — LLM output never enters candidate / convergence /
                          scoring / interaction-strength decisions.
  L-2  Strength empty  — LLM-proposed interactions always have None strength;
                          strength must come from explicit human declaration.
  L-3  Provenance      — all LLM output carries model, timestamp, and
                          prompt fingerprint.
"""

from .types import (
    PermissionTier,
    GuardViolationSeverity,
    GuardViolationError,
)
from .provenance import Provenance, make_prompt_fingerprint
from .guard import LLMGate, LLMOutput

__all__ = [
    "PermissionTier",
    "GuardViolationSeverity",
    "GuardViolationError",
    "Provenance",
    "make_prompt_fingerprint",
    "LLMGate",
    "LLMOutput",
]
