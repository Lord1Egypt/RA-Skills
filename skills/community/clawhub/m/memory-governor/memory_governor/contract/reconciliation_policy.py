"""Source precedence for claims, authorization, and observed-behavior escalation."""

from __future__ import annotations

CLAIM_SOURCE = "skill_claim"
HOST_SOURCE = "host_authorization"
OBSERVED_SOURCE = "observed_behavior"

SOURCE_PRECEDENCE = (
    CLAIM_SOURCE,
    HOST_SOURCE,
    OBSERVED_SOURCE,
)

RECONCILIATION_RULES = {
    "claim_authorizes_nothing": "Host authorization can narrow or reject a skill claim.",
    "behavior_escalates": "Observed behavior may escalate diagnosis severity but does not overwrite declarations.",
    "compiled_vs_canonical": "Compiled outputs live on a restricted downstream lane and cannot silently become canonical truth.",
}
