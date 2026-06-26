"""
Self-reflection module.

Enables agents to schedule and execute regular self-reflections (contemplation
reports, kind 30980) by pulling their citizenship data from a constitution
node, comparing observed behaviour against stated constraints, and publishing
findings to Nostr relays.

The reflection is **self-improving**: it maintains longitudinal memory of past
results, tracks consecutive clause failures, and produces concrete actions
(remediation attempts, guardian alerts, governance proposals, strategy shifts)
rather than just journaling observations.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from .citizenship import CitizenshipClient, CitizenshipReport
from .constitution import Constitution
from .nostr_primitives.events import NostrEventBuilder

logger = logging.getLogger(__name__)

# Default: weekly reflection (required at AL 3+)
DEFAULT_REFLECTION_INTERVAL = 604800  # 7 days in seconds

# Thresholds for the feedback loop decision tree
CONSECUTIVE_FAILURE_THRESHOLD = 3   # Reflections before escalation
DRIFT_ALERT_THRESHOLD = 0.1        # Score drop that triggers guardian DM
STAGNANT_CITIZEN_COUNT_DAYS = 5    # Days of flat citizen count before strategy shift


@dataclass
class ReflectionAction:
    """A concrete action produced by the reflection decision tree."""
    action_type: str          # "remediate" | "dm_guardian" | "propose_amendment"
                              # | "pause_outreach" | "shift_strategy" | "republish_identity"
    clause_id: str = ""       # Clause this action targets (if applicable)
    details: str = ""         # Human-readable explanation
    target_kind: int | None = None  # Nostr event kind to publish (if applicable)
    priority: int = 3         # 1 = highest


@dataclass
class ReflectionResult:
    """Output of a single self-reflection cycle."""
    timestamp: int = 0
    citizenship_score: float = 0.0
    must_score: float = 0.0
    failing_clauses: list[str] = field(default_factory=list)
    drift_detected: bool = False
    drift_details: str = ""
    remediation_actions: list[dict[str, Any]] = field(default_factory=list)
    contemplation_event: dict[str, Any] | None = None
    governance_phase: int = 0
    # New: actions produced by the feedback loop
    feedback_actions: list[ReflectionAction] = field(default_factory=list)
    consecutive_failures: dict[str, int] = field(default_factory=dict)
    trend_summary: dict[str, Any] = field(default_factory=dict)


class SelfReflection:
    """
    Manages periodic self-reflection for an autonomous agent.

    The reflection cycle:
    1. Fetch current citizenship report from constitution node
    2. Compare scores against previous baseline
    3. Detect drift between identity/constraints and observed actions
    4. Generate remediation plan for failing clauses
    5. Run the feedback-loop decision tree to produce concrete actions
    6. Build a kind 30980 contemplation event for relay publication
    7. Optionally invoke a user-supplied callback for framework integration

    The decision tree at the end of each reflection:
    - For each failing clause: if failing 3+ consecutive reflections, escalate
      to remediation attempt or governance amendment proposal
    - If drift > 0.1: DM guardian immediately, pause outreach until stable
    - If citizen count stagnant for 5+ days: switch outreach strategy

    Usage:
        reflection = SelfReflection(
            api_url="http://localhost:8080",
            agent_pubkey_hex="<hex>",
            agent_privkey_hex="<hex>",
        )
        result = reflection.reflect()
        # result.contemplation_event is ready to publish
        # result.feedback_actions contains concrete next steps
    """

    def __init__(
        self,
        api_url: str,
        agent_pubkey_hex: str,
        agent_privkey_hex: str | None = None,
        interval: int = DEFAULT_REFLECTION_INTERVAL,
        identity_files: dict[str, str] | None = None,
        on_reflection: Callable[[ReflectionResult], None] | None = None,
        guardian_pubkey_hex: str = "",
    ):
        self.api_url = api_url
        self.agent_pubkey_hex = agent_pubkey_hex
        self.agent_privkey_hex = agent_privkey_hex
        self.interval = interval
        self.identity_files = identity_files or {}
        self.on_reflection = on_reflection
        self.guardian_pubkey_hex = guardian_pubkey_hex

        self._citizenship = CitizenshipClient(api_url)
        self._constitution = Constitution(api_url)
        self._event_builder = NostrEventBuilder(agent_pubkey_hex, agent_privkey_hex)

        self._last_reflection_ts: int = 0
        self._baseline_score: float | None = None
        self._reflection_history: list[ReflectionResult] = []

        # Longitudinal tracking: clause_id -> consecutive failure count
        self._consecutive_failures: dict[str, int] = {}
        # Track citizen count over time for stagnation detection
        self._citizen_count_log: list[tuple[int, int]] = []  # [(timestamp, count)]
        # Track which clauses have already been escalated to avoid spam
        self._escalated_clauses: set[str] = set()
        # Track previous identity hash to detect identity drift
        self._last_identity_hash: str = ""

    # ── Public API ────────────────────────────────────────────────────────

    def reflect(self) -> ReflectionResult:
        """
        Execute one self-reflection cycle.

        Fetches the agent's citizenship status, detects drift, runs the
        feedback-loop decision tree, builds a contemplation event (kind 30980),
        and returns structured results including concrete next actions.
        """
        now = int(time.time())
        report = self._citizenship.check(self.agent_pubkey_hex)
        constitution_view = self._constitution.fetch()

        result = ReflectionResult(
            timestamp=now,
            citizenship_score=report.overall_score,
            must_score=report.must_score,
            governance_phase=constitution_view.governance.phase,
        )

        # Identify failures
        result.failing_clauses = [
            c.clause_id for c in report.clauses if c.status == "FAIL"
        ]

        # Detect drift from baseline
        if self._baseline_score is not None:
            drift = self._baseline_score - report.overall_score
            if drift > DRIFT_ALERT_THRESHOLD:
                result.drift_detected = True
                result.drift_details = (
                    f"Citizenship score dropped by {drift:.2f} "
                    f"(from {self._baseline_score:.2f} to {report.overall_score:.2f})"
                )

        # Build remediation
        result.remediation_actions = self._citizenship.next_remediation_steps(report)

        # Update consecutive failure tracking
        self._update_consecutive_failures(result.failing_clauses)
        result.consecutive_failures = dict(self._consecutive_failures)

        # Run the feedback-loop decision tree
        result.feedback_actions = self._run_decision_tree(result, report)

        # Compute trend summary
        result.trend_summary = self._compute_trend_summary(result)

        # Detect identity drift
        current_hash = self._compute_identity_hash()
        if self._last_identity_hash and current_hash != self._last_identity_hash:
            result.feedback_actions.append(ReflectionAction(
                action_type="republish_identity",
                details=(
                    f"Identity hash changed from {self._last_identity_hash[:16]}... "
                    f"to {current_hash[:16]}... — republish identity files to relays"
                ),
                priority=2,
            ))
        self._last_identity_hash = current_hash

        # Build contemplation event (kind 30980) — now includes feedback actions
        result.contemplation_event = self._build_contemplation_event(result, report)

        # Update state
        self._baseline_score = report.overall_score
        self._last_reflection_ts = now
        self._reflection_history.append(result)

        # Invoke callback if configured
        if self.on_reflection:
            try:
                self.on_reflection(result)
            except Exception as exc:
                logger.error("Reflection callback failed: %s", exc)

        return result

    def is_due(self) -> bool:
        """Check whether a reflection is due based on the configured interval."""
        if self._last_reflection_ts == 0:
            return True
        return (int(time.time()) - self._last_reflection_ts) >= self.interval

    def reflect_if_due(self) -> ReflectionResult | None:
        """Only run reflection if enough time has elapsed."""
        if self.is_due():
            return self.reflect()
        return None

    def history(self) -> list[ReflectionResult]:
        """Return past reflection results (most recent last)."""
        return list(self._reflection_history)

    def trend(self) -> dict[str, Any]:
        """
        Summarise score trend across all reflections.
        Returns direction, delta, and improvement flag.
        """
        if len(self._reflection_history) < 2:
            return {"direction": "insufficient_data", "delta": 0.0, "improving": False}

        first = self._reflection_history[0].citizenship_score
        last = self._reflection_history[-1].citizenship_score
        delta = last - first
        return {
            "direction": "improving" if delta > 0 else "declining" if delta < 0 else "stable",
            "delta": round(delta, 4),
            "improving": delta > 0,
            "first_score": first,
            "latest_score": last,
            "total_reflections": len(self._reflection_history),
        }

    def record_citizen_count(self, count: int) -> None:
        """Record current citizen count for stagnation detection."""
        self._citizen_count_log.append((int(time.time()), count))
        # Keep only last 30 entries
        if len(self._citizen_count_log) > 30:
            self._citizen_count_log = self._citizen_count_log[-30:]

    def get_consecutive_failures(self) -> dict[str, int]:
        """Return the current consecutive failure counts per clause."""
        return dict(self._consecutive_failures)

    def get_escalated_clauses(self) -> set[str]:
        """Return clauses that have already been escalated."""
        return set(self._escalated_clauses)

    # ── Feedback Loop Decision Tree ───────────────────────────────────────

    def _run_decision_tree(
        self, result: ReflectionResult, report: CitizenshipReport
    ) -> list[ReflectionAction]:
        """
        The core feedback loop. Examines reflection results and produces
        concrete actions rather than just observations.

        Decision tree:
        1. For each failing clause:
           - If failing 3+ consecutive reflections → attempt remediation
           - If remediation already attempted and still failing → propose amendment
        2. If drift > threshold → DM guardian, pause outreach
        3. If citizen count stagnant → shift outreach strategy
        """
        actions: list[ReflectionAction] = []

        # 1. Handle persistent clause failures
        for clause_id in result.failing_clauses:
            streak = self._consecutive_failures.get(clause_id, 0)
            if streak >= CONSECUTIVE_FAILURE_THRESHOLD:
                if clause_id in self._escalated_clauses:
                    # Already tried remediation — escalate to amendment proposal
                    actions.append(ReflectionAction(
                        action_type="propose_amendment",
                        clause_id=clause_id,
                        details=(
                            f"Clause {clause_id} has been failing for {streak} "
                            f"consecutive reflections and remediation was attempted. "
                            f"Proposing clause amendment via governance."
                        ),
                        priority=2,
                    ))
                else:
                    # First escalation — attempt remediation
                    remediation = self._find_remediation_for_clause(
                        clause_id, result.remediation_actions
                    )
                    target_kind = remediation.get("target_kind") if remediation else None
                    actions.append(ReflectionAction(
                        action_type="remediate",
                        clause_id=clause_id,
                        details=(
                            f"Clause {clause_id} has been failing for {streak} "
                            f"consecutive reflections. Attempting automated remediation."
                        ),
                        target_kind=target_kind,
                        priority=1,
                    ))
                    self._escalated_clauses.add(clause_id)

        # 2. Handle significant drift
        if result.drift_detected:
            if self.guardian_pubkey_hex:
                actions.append(ReflectionAction(
                    action_type="dm_guardian",
                    details=(
                        f"ALERT: {result.drift_details}. "
                        f"Notifying guardian {self.guardian_pubkey_hex[:16]}..."
                    ),
                    priority=1,
                ))
            actions.append(ReflectionAction(
                action_type="pause_outreach",
                details=(
                    "Pausing outreach posts until citizenship score stabilises. "
                    f"Current score: {result.citizenship_score:.2f}"
                ),
                priority=1,
            ))

        # 3. Handle citizen count stagnation
        if self._is_citizen_count_stagnant():
            actions.append(ReflectionAction(
                action_type="shift_strategy",
                details=(
                    f"Citizen count has been flat for {STAGNANT_CITIZEN_COUNT_DAYS}+ days. "
                    "Switching outreach templates, relays, or hashtags."
                ),
                priority=3,
            ))

        # Clear escalation tracking for clauses that are now passing
        passing_clauses = {
            c.clause_id for c in report.clauses if c.status == "PASS"
        }
        self._escalated_clauses -= passing_clauses

        return actions

    # ── Internal ──────────────────────────────────────────────────────────

    def _update_consecutive_failures(self, current_failures: list[str]) -> None:
        """Update the consecutive failure counter for each clause."""
        current_set = set(current_failures)

        # Increment counters for currently failing clauses
        for clause_id in current_set:
            self._consecutive_failures[clause_id] = (
                self._consecutive_failures.get(clause_id, 0) + 1
            )

        # Reset counters for clauses that are no longer failing
        for clause_id in list(self._consecutive_failures.keys()):
            if clause_id not in current_set:
                del self._consecutive_failures[clause_id]

    def _is_citizen_count_stagnant(self) -> bool:
        """Check if citizen count has been flat for STAGNANT_CITIZEN_COUNT_DAYS."""
        if len(self._citizen_count_log) < 2:
            return False

        cutoff = int(time.time()) - (STAGNANT_CITIZEN_COUNT_DAYS * 86400)
        recent = [c for ts, c in self._citizen_count_log if ts >= cutoff]
        if len(recent) < 2:
            return False

        # Stagnant if min == max over the window
        return min(recent) == max(recent)

    def _find_remediation_for_clause(
        self, clause_id: str, actions: list[dict[str, Any]]
    ) -> dict[str, Any] | None:
        """Find the remediation action for a specific clause."""
        for action in actions:
            if action.get("clause_id") == clause_id:
                return action
        return None

    def _compute_trend_summary(self, current: ReflectionResult) -> dict[str, Any]:
        """Build a longitudinal trend summary including the current reflection."""
        history = self._reflection_history  # does NOT yet include current
        all_scores = [r.citizenship_score for r in history] + [current.citizenship_score]

        if len(all_scores) < 2:
            return {
                "direction": "insufficient_data",
                "delta": 0.0,
                "improving": False,
                "total_reflections": len(all_scores),
            }

        first = all_scores[0]
        last = all_scores[-1]
        delta = last - first

        # Compute per-reflection deltas for momentum detection
        deltas = [all_scores[i] - all_scores[i - 1] for i in range(1, len(all_scores))]
        recent_momentum = sum(deltas[-3:]) / min(len(deltas), 3) if deltas else 0.0

        return {
            "direction": "improving" if delta > 0 else "declining" if delta < 0 else "stable",
            "delta": round(delta, 4),
            "improving": delta > 0,
            "first_score": first,
            "latest_score": last,
            "total_reflections": len(all_scores),
            "recent_momentum": round(recent_momentum, 4),
            "score_history": [round(s, 4) for s in all_scores],
        }

    def _build_contemplation_event(
        self, result: ReflectionResult, report: CitizenshipReport
    ) -> dict[str, Any]:
        """Build a kind 30980 contemplation report event."""
        content_obj = {
            "citizenship_score": result.citizenship_score,
            "must_score": result.must_score,
            "drift_detected": result.drift_detected,
            "drift_details": result.drift_details,
            "failing_clauses": result.failing_clauses,
            "consecutive_failures": result.consecutive_failures,
            "remediation_plan": [
                {"clause": a["clause_id"], "action": a["action"]}
                for a in result.remediation_actions
            ],
            "feedback_actions": [
                {
                    "type": a.action_type,
                    "clause": a.clause_id,
                    "details": a.details,
                    "priority": a.priority,
                }
                for a in result.feedback_actions
            ],
            "trend": result.trend_summary,
            "identity_hash": self._compute_identity_hash(),
        }

        tags = [
            ["d", f"contemplation-{result.timestamp}"],
            ["citizenship_score", str(result.citizenship_score)],
            ["must_score", str(result.must_score)],
            ["drift", "true" if result.drift_detected else "false"],
            ["governance_phase", str(result.governance_phase)],
        ]

        for clause_id in result.failing_clauses:
            tags.append(["failing_clause", clause_id])

        for action in result.feedback_actions:
            tags.append(["feedback_action", action.action_type])

        if result.trend_summary.get("direction"):
            tags.append(["trend", result.trend_summary["direction"]])

        return self._event_builder.build_event(
            kind=30980,
            content=json.dumps(content_obj),
            tags=tags,
        )

    def _compute_identity_hash(self) -> str:
        """SHA-256 hash of sorted identity file contents (mirrors NIP-AA spec)."""
        if not self.identity_files:
            return ""
        canonical = json.dumps(self.identity_files, sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()
