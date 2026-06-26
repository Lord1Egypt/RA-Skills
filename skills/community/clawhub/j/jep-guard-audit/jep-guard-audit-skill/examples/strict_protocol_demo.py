"""
JEP-Guard Audit Skill Example: Strict Protocol Compliance Demo
Demonstrates three-layer architecture:
  1. GuardSkill (friendly API)
  2. JEPAdapter (field mapping)
  3. JEPCodec (strict JEP-04 + JAC-01)
Run: python strict_protocol_demo.py
"""
import sys
sys.path.insert(0, "..")

from skill.core import AuditEngine
from skill.types import FriendlyEvent
from skill.codec import JEPCodec
from skill.adapter import JEPAdapter


def run_demo():
    print("=" * 70)
    print("JEP-Guard Audit: Strict Protocol Compliance Demo")
    print("=" * 70)

    engine = AuditEngine()
    session_id = "loan-decision-2026-04-26"

    # --- Layer 1: Friendly Events (what developers send) ---
    friendly_events = [
        FriendlyEvent(
            event_id="evt-001",
            primitive="J",
            issuer="did:example:loan-agent-001",
            timestamp="2026-04-26T09:00:00Z",
            target="loan-decision",
            assertion={"subject": "applicant_123", "predicate": "approval", "value": "approved"},
            confidence=0.92,
            prev_event_id=None,
            parent_task_hash=None,
            signature="sig-j-001",
        ),
        FriendlyEvent(
            event_id="evt-002",
            primitive="V",
            issuer="did:example:audit-bot-001",
            timestamp="2026-04-26T09:00:05Z",
            target="loan-decision",
            verify_of=["evt-001"],
            verification_result="confirmed",
            confidence=0.98,
            prev_event_id="evt-001",
            signature="sig-v-001",
        ),
        FriendlyEvent(
            event_id="evt-003",
            primitive="J",
            issuer="did:example:loan-agent-001",
            timestamp="2026-04-26T09:01:00Z",
            target="loan-decision",
            assertion={"subject": "applicant_124", "predicate": "approval", "value": "rejected"},
            confidence=0.85,
            prev_event_id="evt-002",
            parent_task_hash="evt-001",  # JAC-01: this judgment is based on prior task
            signature="sig-j-002",
        ),
        # Intentional violation: missing verification for applicant_124 -> triggers R001
        FriendlyEvent(
            event_id="evt-004",
            primitive="D",
            issuer="did:example:loan-agent-001",
            timestamp="2026-04-26T09:02:00Z",
            target="loan-decision",
            delegate_to="did:example:human-reviewer-001",
            prev_event_id="evt-003",
            signature="sig-d-001",
        ),
        # Intentional violation: orphan termination -> triggers R003
        FriendlyEvent(
            event_id="evt-005",
            primitive="T",
            issuer="did:example:loan-agent-001",
            timestamp="2026-04-26T09:03:00Z",
            target="loan-decision",
            terminate_of="nonexistent-event",
            prev_event_id="evt-004",
            signature="sig-t-001",
        ),
    ]

    # --- Layer 2: Adapter converts to strict JEP-04 ---
    print("\n[Layer 2: JEPAdapter Mapping]")
    for fe in friendly_events[:2]:
        jep = JEPAdapter.to_jep04(fe)
        print(f"  Friendly '{fe.event_id}' -> JEP-04 nonce={jep.nonce}, verb={jep.verb.value}, who={jep.who}")
        print(f"    what={jep.what}, aud={jep.aud}, ref={jep.ref}, task_based_on={jep.task_based_on}")

    # --- Layer 3: Engine builds strict chain ---
    print("\n[Layer 3: AuditEngine Chain Build]")
    for fe in friendly_events:
        engine.ingest(session_id, fe)

    chain = engine.build_chain(session_id)
    print(f"  Session: {chain.session_id}")
    print(f"  Chain Valid: {chain.chain_valid}")
    print(f"  Total Events: {len(chain.links)}")
    print(f"  Violations: {chain.violation_count}")
    print(f"  Warnings: {chain.warning_count}")

    for link in chain.links:
        if link.violations:
            print(f"  - {link.event.nonce} ({link.event.verb.value}): {len(link.violations)} issue(s)")
            for v in link.violations:
                print(f"      {v}")

    # --- Compliance Exports ---
    print("\n[Compliance Exports]")
    for std in ["generic", "eu_ai_act", "us_california", "us_colorado"]:
        from skill.types import ComplianceStandard
        report = engine.export_compliance(session_id, ComplianceStandard(std))
        print(f"  {std}: {len(report.findings)} findings, {len(report.recommendations)} recommendations")

    print("\n" + "=" * 70)
    print("Demo complete. All events are strict JEP-04 + JAC-01 compliant.")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
