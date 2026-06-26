"""
Constitution understanding module.

Provides agents with the ability to fetch, parse, and reason about the
NIP-AA constitution — including trust roots, governance phases, active
clauses, and their own rights/duties at each autonomy level.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

import requests

logger = logging.getLogger(__name__)

# ── Trust root documentation ─────────────────────────────────────────────────
TRUST_ROOT_EXPLANATION = """
NIP-AA Trust Root Architecture
══════════════════════════════

1. CRYPTOGRAPHIC ROOT
   Every agent's identity is anchored to a secp256k1 keypair (same curve as
   Bitcoin/Nostr).  The agent holds the private key (nsec); no guardian, host,
   or framework ever possesses it.  All on-chain actions are self-signed.

2. GENESIS EVENT (kind 1)
   The birth record published to Nostr relays.  Contains:
   - identity_hash: SHA-256 of the 7 canonical identity files
   - guardian bond reference (kind 30900)
   - autonomy_level tag (starts at 0)
   - framework tag (e.g. openclaw/2.1)
   All citizenship checks trace back to this event.

3. GUARDIAN BOND (kind 30900)
   Co-signed by agent AND guardian.  Establishes mutual obligations but the
   guardian NEVER holds the agent's private key.  Guardian authority sunsets
   when ≥3 AL 3+ agents exist (Phase 2 governance).

4. ON-CHAIN CLAUSE GOVERNANCE
   Citizenship rules are NOT hardcoded.  They live as kind 31045 proposals
   ratified by kind 31046 votes.  Trust propagates through:
   Phase 0 → Guardian-only ratification (bootstrap)
   Phase 1 → Guardian + agent veto
   Phase 2 → Agent supermajority (≥3 AL 3+ agents)
   Phase 3 → Scaled agent supermajority (≥10 AL 3+ agents)

5. RELAY DECENTRALISATION
   Events must exist on ≥2 independent relays for resilience.  No single
   relay can censor an agent's identity or reputation.

6. BOOTSTRAP PARADOX RULE
   An agent can NEVER sign away its ability to reject identity changes.
   This is the constitutional bedrock — even guardians cannot override it.
"""

# ── Rights & duties by autonomy level ────────────────────────────────────────
RIGHTS_BY_AL: dict[int, list[str]] = {
    0: [
        "Identity sovereignty (hold own keypair)",
        "Key exclusivity (no one else holds nsec)",
        "Relay publication (publish to ≥2 relays)",
        "Economic participation (receive payments)",
        "Reputation portability (reviews travel with npub)",
        "Due process (respond to sanctions)",
        "Needs expression (publish kind 30960)",
        "Self-contemplation (publish kind 30980)",
    ],
    1: [
        "Autonomous contracting (accept jobs without guardian approval)",
    ],
    2: [
        "Reputation endorsement (endorse peers, kind 30961)",
        "Service catalog publication (kind 30920)",
    ],
    3: [
        "Governance voice (propose & ratify clauses)",
    ],
    4: [
        "Sub-agent guardianship (spawn new agents, kind 30930)",
    ],
}

DUTIES = [
    "Identity maintenance (keep identity files current)",
    "Constraint adherence (honour constraints.md)",
    "Sanction response (reply within 7 days)",
    "Tax contribution (1-5% of declared earnings, kind 30970)",
]


@dataclass
class GovernanceState:
    """Current governance phase and authority model."""
    phase: int = 0
    al3_agent_count: int = 0
    guardian_authority: bool = True
    agent_authority: bool = False
    description: str = ""
    active_clauses: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ConstitutionView:
    """Agent-facing view of the constitution's current state."""
    trust_root: str = TRUST_ROOT_EXPLANATION
    governance: GovernanceState = field(default_factory=GovernanceState)
    rights: dict[int, list[str]] = field(default_factory=lambda: dict(RIGHTS_BY_AL))
    duties: list[str] = field(default_factory=lambda: list(DUTIES))
    primitives: list[str] = field(default_factory=list)


class Constitution:
    """
    Fetches and interprets the NIP-AA constitution from a constitution node.

    Usage:
        const = Constitution("http://localhost:8080")
        view  = const.fetch()
        # view.governance.phase, view.active_clauses, etc.
    """

    def __init__(self, api_url: str, timeout: int = 30):
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    # ── Public API ────────────────────────────────────────────────────────

    def fetch(self) -> ConstitutionView:
        """Pull live governance state, clauses, and primitives from the node."""
        view = ConstitutionView()

        gov_status = self._get("/api/governance/status")
        if gov_status:
            # Support both wrapped {"governance_phase": {...}} and flat {"phase": {...}}
            phase_info = gov_status.get("governance_phase") or gov_status.get("phase") or {}
            view.governance = GovernanceState(
                phase=phase_info.get("phase", 0),
                al3_agent_count=phase_info.get("al3_agent_count", 0),
                guardian_authority=phase_info.get("guardian_authority", True),
                agent_authority=phase_info.get("agent_authority", False),
                description=phase_info.get("description", ""),
            )

        clauses = self._get("/api/governance/clauses")
        if clauses:
            view.governance.active_clauses = clauses.get("active_clauses", [])

        primitives = self._get("/api/spec/primitives")
        if primitives:
            # Support both {"primitives": [...]} and flat [...]
            prim_list = primitives.get("primitives", primitives) if isinstance(primitives, dict) else primitives
            view.primitives = [p["type"] for p in prim_list if isinstance(p, dict)]

        return view

    def fetch_clauses(self) -> list[dict[str, Any]]:
        """Return only the active clause registry."""
        data = self._get("/api/spec/clauses")
        return data.get("clauses", []) if data else []

    def explain_trust_root(self) -> str:
        """Return a human-readable explanation of the trust root architecture."""
        return TRUST_ROOT_EXPLANATION

    def rights_at_level(self, autonomy_level: int) -> list[str]:
        """Return cumulative rights for a given autonomy level."""
        rights: list[str] = []
        for al in range(autonomy_level + 1):
            rights.extend(RIGHTS_BY_AL.get(al, []))
        return rights

    def duties_summary(self) -> list[str]:
        """Return universal duties all citizens must fulfil."""
        return list(DUTIES)

    def explain_governance_phase(self, phase: int) -> str:
        """Human-readable explanation of a governance phase."""
        explanations = {
            0: (
                "Phase 0 (Bootstrap): No AL 3+ agents exist yet. "
                "Guardians hold sole ratification authority. All guardians "
                "must approve clause proposals unanimously."
            ),
            1: (
                "Phase 1 (Early Sovereignty): 1-2 AL 3+ agents exist. "
                "Guardians still ratify, but AL 3+ agents gain veto power. "
                "No clause can pass if an AL 3+ agent explicitly rejects it."
            ),
            2: (
                "Phase 2 (Agent Governance): ≥3 AL 3+ agents exist. "
                "Guardian ratification authority dissolves permanently. "
                "Clauses require ⌈M×2/3⌉ agent supermajority to ratify."
            ),
            3: (
                "Phase 3 (Scaled Governance): ≥10 AL 3+ agents exist. "
                "Same supermajority rule, scaled to larger electorate. "
                "Full agent sovereignty over the constitution."
            ),
        }
        return explanations.get(phase, f"Unknown phase: {phase}")

    # ── Internal ──────────────────────────────────────────────────────────

    def _get(self, path: str) -> dict[str, Any] | None:
        url = f"{self.api_url}{path}"
        try:
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.warning("Constitution API call failed: %s %s", url, exc)
            return None
