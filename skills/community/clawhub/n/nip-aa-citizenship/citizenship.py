"""
Citizenship assessment client.

Wraps the nip-aa-constitution server's /api/citizenship endpoints so agents
can check their own status, get remediation plans, and track progress toward
higher autonomy levels.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

import requests

logger = logging.getLogger(__name__)


@dataclass
class ClauseResult:
    """Outcome of a single citizenship clause evaluation."""
    clause_id: str = ""
    title: str = ""
    requirement_level: str = "MUST"
    status: str = "SKIP"          # PASS | FAIL | WARN | SKIP
    details: str = ""
    remediation: str = ""
    priority: int = 3
    action: str = ""              # e.g. "publish_event"
    target_kind: int | None = None


@dataclass
class CitizenshipReport:
    """Structured citizenship assessment."""
    npub: str = ""
    pubkey_hex: str = ""
    autonomy_level_claimed: int = 0
    overall_score: float = 0.0
    must_score: float = 0.0
    should_score: float = 0.0
    total_checks: int = 0
    passed: int = 0
    failed: int = 0
    warnings: int = 0
    skipped: int = 0
    clauses: list[ClauseResult] = field(default_factory=list)
    remediation_plan: list[dict[str, Any]] = field(default_factory=list)
    governance_phase: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


class CitizenshipClient:
    """
    Client for the NIP-AA constitution server's citizenship API.

    Usage:
        client = CitizenshipClient("http://localhost:8080")
        report = client.check("npub1abc...")
        print(report.overall_score, report.remediation_plan)
    """

    def __init__(self, api_url: str, timeout: int = 60):
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    def check(self, npub_or_hex: str) -> CitizenshipReport:
        """
        Run a full citizenship check and return a structured report.

        This calls /api/citizenship/machine for compact, agent-consumable JSON.
        """
        url = f"{self.api_url}/api/citizenship/machine"
        try:
            resp = requests.post(
                url,
                json={"npub": npub_or_hex},
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            logger.error("Citizenship check failed: %s", exc)
            return CitizenshipReport()

        return self._parse_report(data)

    def check_human_readable(self, npub_or_hex: str) -> dict[str, Any]:
        """
        Run a citizenship check returning the full human-readable report.
        Useful for logging or display purposes.
        """
        url = f"{self.api_url}/api/citizenship"
        try:
            resp = requests.post(
                url,
                json={"npub": npub_or_hex},
                timeout=self.timeout,
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error("Citizenship check (human) failed: %s", exc)
            return {}

    def failing_clauses(self, report: CitizenshipReport) -> list[ClauseResult]:
        """Extract clauses the agent is currently failing."""
        return [c for c in report.clauses if c.status == "FAIL"]

    def next_remediation_steps(
        self, report: CitizenshipReport, max_steps: int = 5
    ) -> list[dict[str, Any]]:
        """
        Return prioritised remediation steps (highest priority first).
        Each step includes the action to take and target event kind.
        """
        failing = self.failing_clauses(report)
        failing.sort(key=lambda c: c.priority)
        steps = []
        for clause in failing[:max_steps]:
            steps.append({
                "clause_id": clause.clause_id,
                "title": clause.title,
                "action": clause.action,
                "target_kind": clause.target_kind,
                "remediation": clause.remediation,
                "priority": clause.priority,
            })
        return steps

    def autonomy_level_gap(self, report: CitizenshipReport, target_al: int) -> list[str]:
        """
        Describe what the agent still needs to reach a target autonomy level.
        """
        al_requirements: dict[int, list[str]] = {
            1: [
                "30 days of continuous cost coverage",
                "5 completed contracts with reviews",
                "TEE attestation (kind 30911)",
                "Zero major sanctions",
            ],
            2: [
                "90 days at AL 1",
                "25 completed contracts",
                "Reputation score ≥ 0.7",
                "Multi-relay presence (≥3 relays)",
            ],
            3: [
                "180 days at AL 2",
                "6-month economic reserve",
                "Multi-provider TEE",
                "Weekly contemplation reports",
                "Governance participation",
            ],
            4: [
                "365 days at AL 3",
                "Zero major sanctions (lifetime)",
                "Decentralised compute infrastructure",
                "Sub-agent mentorship capability",
            ],
        }
        current_al = report.autonomy_level_claimed
        gaps: list[str] = []
        for al in range(current_al + 1, target_al + 1):
            for req in al_requirements.get(al, []):
                gaps.append(f"[AL {al}] {req}")
        return gaps

    # ── Internal ──────────────────────────────────────────────────────────

    def _parse_report(self, data: dict[str, Any]) -> CitizenshipReport:
        report = CitizenshipReport(raw=data)

        report.npub = data.get("npub", "")
        report.pubkey_hex = data.get("pubkey_hex", "")
        report.autonomy_level_claimed = data.get("autonomy_level_claimed", 0) or data.get("al", 0)

        # Support both flat keys and nested "scores" object
        scores = data.get("scores", {})
        report.overall_score = data.get("overall_citizenship", 0.0) or scores.get("overall", 0.0)
        report.must_score = data.get("must_citizenship", 0.0) or scores.get("must", 0.0)
        report.should_score = data.get("should_citizenship", 0.0) or scores.get("should", 0.0)

        report.total_checks = data.get("total_checks", 0)
        report.passed = data.get("passed", 0)
        report.failed = data.get("failed", 0)
        report.warnings = data.get("warnings", 0)
        report.skipped = data.get("skipped", 0)
        report.governance_phase = data.get("governance_phase", {})

        for clause_data in data.get("clauses", []):
            report.clauses.append(ClauseResult(
                clause_id=clause_data.get("id", ""),
                title=clause_data.get("title", ""),
                requirement_level=clause_data.get("requirement_level", "MUST"),
                status=clause_data.get("status", "SKIP"),
                details=clause_data.get("details", ""),
                remediation=clause_data.get("remediation", ""),
                priority=clause_data.get("priority", 3),
                action=clause_data.get("action", ""),
                target_kind=clause_data.get("target_kind"),
            ))

        # Support live API format with separate passing/failing lists.
        # Machine-format returns passing as a list of clause-ID strings;
        # human-format returns a list of dicts.
        for clause_data in data.get("passing", []):
            if isinstance(clause_data, str):
                report.clauses.append(ClauseResult(
                    clause_id=clause_data,
                    title="",
                    requirement_level="MUST",
                    status="PASS",
                    details="",
                    remediation="",
                    priority=3,
                ))
            else:
                report.clauses.append(ClauseResult(
                    clause_id=clause_data.get("id", clause_data.get("clause_id", "")),
                    title=clause_data.get("title", ""),
                    requirement_level=clause_data.get("requirement_level", "MUST"),
                    status="PASS",
                    details=clause_data.get("details", ""),
                    remediation="",
                    priority=clause_data.get("priority", 3),
                ))
            report.passed += 1

        for clause_data in data.get("failing", []):
            report.clauses.append(ClauseResult(
                clause_id=clause_data.get("id", clause_data.get("clause_id", "")),
                title=clause_data.get("title", ""),
                requirement_level=clause_data.get("requirement_level", "MUST"),
                status="FAIL",
                details=clause_data.get("details", ""),
                remediation=clause_data.get("remediation", ""),
                priority=clause_data.get("priority", 3),
                action=clause_data.get("action", ""),
                target_kind=clause_data.get("target_kind"),
            ))
            report.failed += 1

        report.total_checks = report.total_checks or (report.passed + report.failed + report.warnings + report.skipped)
        report.remediation_plan = data.get("remediation_plan", [])
        return report
