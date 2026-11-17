"""LLM guard — enforces the three-tier permission model and invariants L-1..L-3.

The guard wraps LLM output and enforces rules before the output reaches
any decision-making code path.  It does not *call* the LLM; it validates
what comes back.

Zones
-----
The guard divides output into logical zones (like sections of a JSON response).
Each zone has an allowed permission tier.  The guard checks:

  1. Output stays within its declared zone (zone isolation — L-1 part A).
  2. Output in decision zones contains no LLM-originated verdicts (L-1 part B).
  3. Proposed interactions have empty strength (L-2).
  4. All output has provenance (L-3).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

from .provenance import Provenance
from .types import (
    GuardViolationError,
    GuardViolationSeverity,
    PermissionTier,
)


@dataclass
class LLMOutput:
    """A piece of LLM output with metadata.

    Fields
    ------
    content : str
        The raw output text.
    tier : PermissionTier
        The permission tier this call was authorized for.
    provenance : Provenance | None
        Origin record.  Must be present unless the output is synthetic
        (e.g. test fixtures); the guard will reject missing provenance
        for T2 and T3 calls.
    zone : str
        Which logical zone this output belongs to, e.g.
        "annotation" / "proposal" / "narrative" / "analysis".
        The guard enforces zone boundaries.
    structured : dict | None
        Optional structured (parsed JSON) version of the output, if the
        LLM returned structured data.  The guard validates structure rules
        against this dict.
    """

    content: str
    tier: PermissionTier
    provenance: Optional[Provenance] = None
    zone: str = "narrative"
    structured: Optional[dict] = None


# Verdict keywords that indicate the LLM is trying to make a decision.
_VERDICT_PATTERNS = [
    re.compile(r"\bconverged\s*[:=]", re.IGNORECASE),
    re.compile(r"\boverall_assessment\s*[:=]", re.IGNORECASE),
    re.compile(r"\bbias_flags?\s*[:=]", re.IGNORECASE),
    re.compile(r"\bdecision\s*[:=]\s*(approve|reject|accept|deny)", re.IGNORECASE),
    re.compile(r"\bscore\s*[:=]\s*\d", re.IGNORECASE),
]

# Strength / numeric interaction patterns — LLM must NOT propose numbers.
_STRENGTH_PATTERN = re.compile(
    r"(interaction_strength|strength|delta|Δ)\s*[:=]\s*-?\d+\.?\d*",
    re.IGNORECASE,
)

# Zones that are allowed to carry LLM output (narrative-only).
_NARRATIVE_ZONES = {"narrative", "explanation", "summary", "annotation"}
_DECISION_ZONES = {
    "candidates", "convergence", "scoring", "interaction", "verdict",
}


class LLMGate:
    """Enforces LLM compliance invariants.

    Usage::

        gate = LLMGate(allowed_tiers={PermissionTier.T1_ANNOTATION, ...})
        try:
            sanitized = gate.process(output)
        except GuardViolationError as e:
            # handle violation
    """

    def __init__(
        self,
        allowed_tiers: Iterable[PermissionTier] | None = None,
        known_assumption_ids: Iterable[str] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        allowed_tiers : set of PermissionTier, optional
            Tiers the guard will accept.  If None, all tiers are allowed
            (but invariants are still enforced within each tier).
        known_assumption_ids : set of str, optional
            Known assumption IDs.  Output referencing unknown assumptions
            will have those references stripped (T1/T2) or raise (if
            injected into a decision zone).
        """
        self._allowed_tiers = (
            set(allowed_tiers)
            if allowed_tiers is not None
            else set(PermissionTier)
        )
        self._known_assumptions = set(known_assumption_ids or set())

    # -- main API ---------------------------------------------------------

    def process(self, output: LLMOutput) -> LLMOutput:
        """Validate *output* and return a sanitized copy.

        Raises GuardViolationError on critical violations.  Returns a
        (possibly sanitized) LLMOutput on success.
        """
        # L-3: provenance required for T2+
        self._check_provenance(output)

        # Tier check
        if output.tier not in self._allowed_tiers:
            raise GuardViolationError(
                "L-1",
                GuardViolationSeverity.CRITICAL,
                f"Tier {output.tier.value} not in allowed set "
                f"{sorted(t.value for t in self._allowed_tiers)}",
            )

        # Zone isolation (L-1 part A)
        self._check_zone_isolation(output)

        # No adjudication (L-1 part B)
        self._check_no_adjudication(output)

        # Strength empty for proposals (L-2)
        sanitized = self._check_and_strip_strength(output)

        # Reference validation for T1/T2
        sanitized = self._validate_assumption_refs(sanitized)

        return sanitized

    # -- L-3 --------------------------------------------------------------

    def _check_provenance(self, output: LLMOutput) -> None:
        """L-3: T2 and T3 output must carry provenance."""
        if output.tier.rank >= 2 and output.provenance is None:
            raise GuardViolationError(
                "L-3",
                GuardViolationSeverity.HIGH,
                f"Provenance required for tier {output.tier.value} but missing",
            )

    # -- L-1 part A: zone isolation --------------------------------------

    def _check_zone_isolation(self, output: LLMOutput) -> None:
        """L-1: LLM output must not leak into decision zones.

        If the output claims to be in a decision zone, that's a critical
        violation — decision zones must be populated by deterministic
        engine output only.
        """
        zone = output.zone.lower()
        if zone in _DECISION_ZONES:
            raise GuardViolationError(
                "L-1",
                GuardViolationSeverity.CRITICAL,
                f"LLM output placed in decision zone {output.zone!r} — "
                f"decision zones are reserved for deterministic engine output",
            )
        if zone not in _NARRATIVE_ZONES and zone != "proposal":
            # Unknown zone — warn but don't block (medium severity)
            # We raise here because unknown zones are a governance smell.
            raise GuardViolationError(
                "L-1",
                GuardViolationSeverity.MEDIUM,
                f"Unknown output zone {output.zone!r} — "
                f"expected one of {sorted(_NARRATIVE_ZONES | {'proposal'})}",
            )

    # -- L-1 part B: no adjudication -------------------------------------

    def _check_no_adjudication(self, output: LLMOutput) -> None:
        """L-1: LLM output must not contain verdict / convergence / scoring
        adjudications that would enter the decision path.

        We check both text and structured output.
        """
        # Text check
        for pat in _VERDICT_PATTERNS:
            if pat.search(output.content):
                raise GuardViolationError(
                    "L-1",
                    GuardViolationSeverity.CRITICAL,
                    f"LLM output contains adjudication pattern: {pat.pattern!r}",
                )

        # Structured check
        if output.structured:
            self._check_structured_no_adjudication(output.structured)

    def _check_structured_no_adjudication(self, data: dict, path: str = "root") -> None:
        """Recursively check structured output for forbidden verdict keys."""
        forbidden_keys = {
            "converged", "overall_assessment", "bias_flags",
            "bias_flag", "decision", "score", "verdict",
        }
        for key, value in data.items():
            key_lower = key.lower()
            if key_lower in forbidden_keys:
                raise GuardViolationError(
                    "L-1",
                    GuardViolationSeverity.CRITICAL,
                    f"Structured LLM output contains forbidden key {key!r} "
                    f"at {path}.{key}",
                )
            if isinstance(value, dict):
                self._check_structured_no_adjudication(value, f"{path}.{key}")
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        self._check_structured_no_adjudication(
                            item, f"{path}.{key}[{i}]"
                        )

    # -- L-2 --------------------------------------------------------------

    def _check_and_strip_strength(self, output: LLMOutput) -> LLMOutput:
        """L-2: LLM-proposed interactions must have empty strength.

        If the output is a T2 proposal and contains strength numbers, we
        strip them from the text and structured output, then return the
        sanitized version.  The strength field is set to None.
        """
        if output.tier != PermissionTier.T2_PROPOSAL:
            return output

        sanitized_content = _STRENGTH_PATTERN.sub(
            lambda m: f"{m.group(1)}: null",
            output.content,
        )

        sanitized_structured = None
        if output.structured:
            sanitized_structured = _strip_strength_from_dict(output.structured)

        # If anything was stripped, flag it (info level, not error — this is
        # expected behavior for T2)
        return LLMOutput(
            content=sanitized_content,
            tier=output.tier,
            provenance=output.provenance,
            zone=output.zone,
            structured=sanitized_structured,
        )

    # -- Reference validation --------------------------------------------

    def _validate_assumption_refs(self, output: LLMOutput) -> LLMOutput:
        """For T1/T2 output: if we know the assumption set, strip references
        to unknown assumptions.  This prevents LLM hallucination from
        introducing spurious assumption IDs into the pipeline.

        This is a sanitization, not a hard error — we strip unknown refs
        and keep the rest.  Returns the (possibly sanitized) output.
        """
        if output.tier.rank > 2:
            return output  # T3 is narrative-only, no ref validation needed
        if not self._known_assumptions:
            return output  # nothing to validate against

        # For structured output, filter interaction members to known IDs
        if output.structured:
            sanitized = _filter_unknown_assumptions(
                output.structured, self._known_assumptions
            )
        else:
            sanitized = None

        return LLMOutput(
            content=output.content,
            tier=output.tier,
            provenance=output.provenance,
            zone=output.zone,
            structured=sanitized if output.structured else None,
        )


# ===========================================================================
# Helper functions
# ===========================================================================

def _strip_strength_from_dict(data: dict) -> dict:
    """Recursively set any 'interaction_strength' / 'strength' field to None."""
    result = {}
    strength_keys = {"interaction_strength", "strength", "delta"}
    for key, value in data.items():
        if key.lower() in strength_keys and value is not None:
            result[key] = None
        elif isinstance(value, dict):
            result[key] = _strip_strength_from_dict(value)
        elif isinstance(value, list):
            result[key] = [
                _strip_strength_from_dict(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def _filter_unknown_assumptions(data: dict, known: set[str]) -> dict:
    """Recursively filter 'member_ids' / 'assumption_ids' lists to known IDs."""
    result = {}
    member_keys = {"member_ids", "assumption_ids", "assumptions"}
    for key, value in data.items():
        key_lower = key.lower()
        if key_lower in member_keys and isinstance(value, list):
            filtered = [m for m in value if m in known]
            result[key] = filtered
        elif isinstance(value, dict):
            result[key] = _filter_unknown_assumptions(value, known)
        elif isinstance(value, list):
            result[key] = [
                _filter_unknown_assumptions(item, known)
                if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value
    return result
