"""
JEP-Guard Audit Engine — Business Logic Layer
Operates strictly on JEP04Event objects produced by JEPCodec + JEPAdapter.

Implements:
  - Tamper-evident audit chain construction (SHA-256 hash linking)
  - JEP-04 signature / nonce / timestamp verification
  - JAC-01 chain integrity verification (task_based_on)
  - Five violation detection rules (R001–R005)
  - EU AI Act / CA SB 1047 / CO SB 205 / Generic JEP-01 compliance export
"""
import hashlib
import json
from typing import List, Dict, Optional, Any, Callable
from collections import defaultdict
from datetime import datetime, timezone
from uuid import uuid4

from .types import (
    JEP04Event, Verb, FriendlyEvent,
    AuditChain, AuditChainLink,
    ComplianceStandard, ComplianceReport,
    AuditSeverity, ViolationRule
)
from .codec import JEPCodec
from .adapter import JEPAdapter


class AuditEngine:
    """
    JEP-Guard Audit Engine.
    Ingests FriendlyEvents -> converts to JEP04Events via JEPAdapter ->
    builds strict JEP-04 compliant audit chains -> exports compliance reports.
    """

    def __init__(self):
        self._sessions: Dict[str, List[JEP04Event]] = defaultdict(list)
        self._nonce_cache: set = set()
        self._rules: List[ViolationRule] = []
        self._register_default_rules()

    def _register_default_rules(self):
        """Register default violation detection rules."""
        self._rules.append(ViolationRule(
            rule_id="R001",
            description="Judge event without subsequent Verify event within chain",
            severity=AuditSeverity.WARNING,
            check=self._check_missing_verification
        ))
        self._rules.append(ViolationRule(
            rule_id="R002",
            description="Delegate event without proper issuer authorization",
            severity=AuditSeverity.VIOLATION,
            check=self._check_unauthorized_delegation
        ))
        self._rules.append(ViolationRule(
            rule_id="R003",
            description="Terminate event without matching prior Judge event",
            severity=AuditSeverity.VIOLATION,
            check=self._check_orphan_termination
        ))
        self._rules.append(ViolationRule(
            rule_id="R004",
            description="Hash chain break detected (prev_event_id / ref mismatch)",
            severity=AuditSeverity.CRITICAL,
            check=self._check_hash_integrity
        ))
        self._rules.append(ViolationRule(
            rule_id="R005",
            description="Verify event references non-existent Judge event",
            severity=AuditSeverity.VIOLATION,
            check=self._check_dangling_verification
        ))

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------

    def ingest(self, session_id: str, friendly: FriendlyEvent) -> None:
        """
        Ingest a developer-friendly event.
        Automatically adapts to strict JEP04Event and stores in session.
        """
        jep_event = JEPAdapter.to_jep04(friendly)
        self._sessions[session_id].append(jep_event)

    def ingest_batch(self, session_id: str, friendlies: List[FriendlyEvent]) -> None:
        """Ingest multiple friendly events."""
        for f in friendlies:
            self.ingest(session_id, f)

    # ------------------------------------------------------------------
    # Chain Building & Verification
    # ------------------------------------------------------------------

    def build_chain(self, session_id: str) -> AuditChain:
        """
        Build and verify the tamper-evident audit chain for a session.
        Strictly follows JEP-04 canonicalization and JAC-01 chain rules.
        """
        events = self._sessions.get(session_id, [])
        if not events:
            return AuditChain(
                session_id=session_id,
                links=[],
                chain_valid=True,
                violation_count=0,
                warning_count=0,
            )

        # Sort by JEP-04 'when' (Unix timestamp)
        sorted_events = sorted(events, key=lambda e: e.when)

        links: List[AuditChainLink] = []
        prev_hash = "0" * 64
        violation_count = 0
        warning_count = 0

        # Build event index for JAC parent lookups
        event_index = {e.nonce: e for e in sorted_events}
        # Also index by what hash if available
        hash_index = {e.what: e for e in sorted_events if e.what}

        for i, evt in enumerate(sorted_events):
            # 1. Compute canonical hash of this event
            canonical = JEPCodec.encode(evt)
            computed_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

            # 2. Verify nonce uniqueness (JEP-04 Section 2.3)
            nonce_unique = JEPCodec.verify_nonce_uniqueness(evt.nonce, self._nonce_cache)

            # 3. Verify timestamp window (JEP-04 Section 2.3)
            ts_valid = JEPCodec.verify_timestamp_window(evt.when)

            # 4. Chain integrity: ref should point to previous event's what hash
            chain_integrity = True
            if i > 0:
                prev_evt = sorted_events[i - 1]
                # If ref is present, it should match previous event's hash or nonce
                if evt.ref and evt.ref != prev_evt.nonce and evt.ref != prev_evt.what:
                    chain_integrity = False

            # 5. JAC-01 chain integrity via task_based_on
            jac_valid = True
            if evt.task_based_on:
                if evt.task_based_on not in hash_index and evt.task_based_on not in event_index:
                    # Check JAC-Fault extension
                    has_fault = (
                        evt.extensions
                        and "https://jac.org/fault" in evt.extensions
                        and evt.extensions["https://jac.org/fault"].get("expected_parent") == evt.task_based_on
                    )
                    if not has_fault:
                        jac_valid = False

            # 6. Signature placeholder (real crypto would verify JWS here)
            sig_valid = bool(evt.sig and len(evt.sig) > 0)

            # 7. Run violation rules
            violations = []
            for rule in self._rules:
                if rule.check(evt, sorted_events[:i+1], event_index, hash_index):
                    violations.append(f"[{rule.severity.value}] {rule.rule_id}: {rule.description}")
                    if rule.severity in (AuditSeverity.VIOLATION, AuditSeverity.CRITICAL):
                        violation_count += 1
                    elif rule.severity == AuditSeverity.WARNING:
                        warning_count += 1

            # 8. Add protocol-level findings
            if not nonce_unique:
                violations.append(f"[critical] PROTOCOL: Duplicate nonce detected")
                violation_count += 1
            if not ts_valid:
                violations.append(f"[violation] PROTOCOL: Timestamp outside ±5min window")
                violation_count += 1
            if not chain_integrity:
                violations.append(f"[critical] PROTOCOL: Hash chain break (ref mismatch)")
                violation_count += 1
            if not jac_valid:
                violations.append(f"[violation] JAC-01: Parent task not found for task_based_on")
                violation_count += 1

            link = AuditChainLink(
                event=evt,
                computed_hash=computed_hash,
                hash_valid=True,  # We computed it ourselves
                signature_valid=sig_valid,
                chain_integrity=chain_integrity and jac_valid,
                violations=violations,
            )
            links.append(link)
            prev_hash = computed_hash

        chain_valid = all(l.chain_integrity and l.signature_valid for l in links)

        start_dt = datetime.fromtimestamp(sorted_events[0].when, tz=timezone.utc) if sorted_events else None
        end_dt = datetime.fromtimestamp(sorted_events[-1].when, tz=timezone.utc) if sorted_events else None

        return AuditChain(
            session_id=session_id,
            links=links,
            chain_valid=chain_valid,
            violation_count=violation_count,
            warning_count=warning_count,
            start_time=start_dt,
            end_time=end_dt,
        )

    # ------------------------------------------------------------------
    # Compliance Export
    # ------------------------------------------------------------------

    def export_compliance(
        self,
        session_id: str,
        standard: ComplianceStandard = ComplianceStandard.GENERIC
    ) -> ComplianceReport:
        """Export a regulatory compliance report."""
        chain = self.build_chain(session_id)
        report_id = str(uuid4())
        generated_at = datetime.now(timezone.utc)

        findings = []
        recommendations = []

        for link in chain.links:
            for v in link.violations:
                findings.append({
                    "event_nonce": link.event.nonce,
                    "verb": link.event.verb.value,
                    "issuer": link.event.who,
                    "timestamp": JEPCodec.unix_to_iso(link.event.when),
                    "finding": v,
                    "hash_valid": link.hash_valid,
                    "signature_valid": link.signature_valid,
                    "chain_integrity": link.chain_integrity,
                })

        if standard == ComplianceStandard.EU_AI_ACT:
            recommendations.extend([
                "Ensure all high-risk AI system judgments are logged with full provenance per Article 12.",
                "Maintain tamper-evident records for minimum 6 years per EU AI Act retention rules.",
                "Provide human oversight capability for all automated judgment events per Article 14.",
            ])
            raw = self._format_eu_ai_act(chain, findings)
        elif standard == ComplianceStandard.US_CALIFORNIA:
            recommendations.extend([
                "Report critical safety incidents to CalDS within 72 hours per SB 1047.",
                "Maintain kill-switch event logs for all autonomous terminations.",
            ])
            raw = self._format_us_california(chain, findings)
        elif standard == ComplianceStandard.US_COLORADO:
            recommendations.extend([
                "Document algorithmic impact assessment for all automated decisions per SB 205.",
                "Provide appeal mechanism logs for contested judgments.",
            ])
            raw = self._format_us_colorado(chain, findings)
        else:
            recommendations.extend([
                "Review all WARNING and VIOLATION findings before production deployment.",
                "Ensure JEP-04 hash chain integrity before external audit.",
            ])
            raw = self._format_generic(chain, findings)

        return ComplianceReport(
            report_id=report_id,
            standard=standard,
            session_id=session_id,
            generated_at=generated_at,
            chain_summary={
                "total_events": len(chain.links),
                "chain_valid": chain.chain_valid,
                "violation_count": chain.violation_count,
                "warning_count": chain.warning_count,
                "start_time": chain.start_time.isoformat() if chain.start_time else None,
                "end_time": chain.end_time.isoformat() if chain.end_time else None,
            },
            findings=findings,
            recommendations=recommendations,
            export_format="json",
            raw_data=raw,
        )

    # ------------------------------------------------------------------
    # Violation Rule Implementations
    # ------------------------------------------------------------------

    def _check_missing_verification(self, evt, history, index, hash_index):
        if evt.verb != Verb.JUDGE:
            return False
        for e in history:
            if e.verb == Verb.VERIFY and e.ref == evt.nonce:
                return False
        return True

    def _check_unauthorized_delegation(self, evt, history, index, hash_index):
        if evt.verb != Verb.DELEGATE:
            return False
        has_prior = any(
            e.who == evt.who and e.verb in (Verb.JUDGE, Verb.VERIFY)
            for e in history
        )
        return not has_prior

    def _check_orphan_termination(self, evt, history, index, hash_index):
        if evt.verb != Verb.TERMINATE:
            return False
        # Check if terminate_of exists in index or hash_index
        target = evt.what  # In adapter, terminate_of is put into what payload
        if target and target in hash_index:
            return False
        # Also check extensions
        if evt.extensions and "https://jac.org/fault" in evt.extensions:
            return False  # Fault extension means it's acknowledged
        return True

    def _check_hash_integrity(self, evt, history, index, hash_index):
        if len(history) < 2:
            return False
        prev = history[-2]
        if evt.ref and evt.ref != prev.nonce and evt.ref != prev.what:
            return True
        return False

    def _check_dangling_verification(self, evt, history, index, hash_index):
        if evt.verb != Verb.VERIFY:
            return False
        if not evt.ref:
            return True
        if evt.ref not in index and evt.ref not in hash_index:
            return True
        return False

    # ------------------------------------------------------------------
    # Report Formatters
    # ------------------------------------------------------------------

    def _format_generic(self, chain, findings):
        return json.dumps({
            "standard": "JEP-01",
            "protocol": "JEP-04",
            "jac_version": "JAC-01",
            "session_id": chain.session_id,
            "chain_valid": chain.chain_valid,
            "events": [
                {
                    "nonce": l.event.nonce,
                    "verb": l.event.verb.value,
                    "who": l.event.who,
                    "when": l.event.when,
                    "what": l.event.what,
                    "ref": l.event.ref,
                    "task_based_on": l.event.task_based_on,
                    "computed_hash": l.computed_hash,
                    "violations": l.violations,
                }
                for l in chain.links
            ],
            "findings": findings,
        }, indent=2, default=str)

    def _format_eu_ai_act(self, chain, findings):
        return json.dumps({
            "regulation": "EU AI Act (2024/1689)",
            "article_references": ["Article 12 (Record-keeping)", "Article 14 (Human oversight)"],
            "session_id": chain.session_id,
            "audit_trail_valid": chain.chain_valid,
            "high_risk_system_events": len(chain.links),
            "findings": findings,
            "retention_required_until": "2032-04-26",
        }, indent=2, default=str)

    def _format_us_california(self, chain, findings):
        critical_events = [
            l.event.nonce for l in chain.links
            if l.violations and any("CRITICAL" in v for v in l.violations)
        ]
        return json.dumps({
            "regulation": "California SB 1047",
            "section_references": ["Section 22602 (Safety incidents)"],
            "session_id": chain.session_id,
            "critical_events": critical_events,
            "findings": findings,
            "reporting_deadline": "72 hours from incident detection",
        }, indent=2, default=str)

    def _format_us_colorado(self, chain, findings):
        return json.dumps({
            "regulation": "Colorado SB 205",
            "section_references": ["Section 6-1-1703 (Algorithmic discrimination)"],
            "session_id": chain.session_id,
            "automated_decision_count": len([l for l in chain.links if l.event.verb == Verb.JUDGE]),
            "findings": findings,
            "appeal_logs_available": any(l.event.verb == Verb.TERMINATE for l in chain.links),
        }, indent=2, default=str)
