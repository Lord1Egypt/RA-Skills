"""
JEP Primitive Skills Example: Complex Multi-Agent Workflow
Demonstrates how any complex collaboration decomposes into J/D/T/V atoms.
Run: python complex_workflow.py
"""
import sys
sys.path.insert(0, "..")

from skill.primitives import JudgeSkill, DelegateSkill, TerminateSkill, VerifySkill
from skill.codec import JEPCodec


def run_complex_workflow():
    print("=" * 70)
    print("JEP Primitive Skills: Complex Multi-Agent Workflow")
    print("=" * 70)

    agents = {
        "robot-A": "did:example:robotA",
        "robot-B": "did:example:robotB",
        "human-C": "did:example:humanC",
    }
    target = "warehouse-zone-3"

    # Step 1: Robot A observes door is open (J)
    print("
[Step 1] Robot A observes door is open")
    j1 = JudgeSkill.execute(
        issuer=agents["robot-A"],
        target=target,
        subject="door_01",
        predicate="status",
        value="open",
        confidence=0.95,
    )
    print(f"  J event: nonce={j1.event.nonce}, what={j1.event.what[:30]}...")
    print(f"  Next suggested: {j1.next_suggested_primitive}")

    # Step 2: Robot B verifies the observation (V)
    print("
[Step 2] Robot B confirms Robot A's observation")
    v1 = VerifySkill.execute(
        issuer=agents["robot-B"],
        verify_of=[j1.event.nonce],
        target=target,
        verification_result="confirmed",
        confidence=0.9,
    )
    print(f"  V event: nonce={v1.event.nonce}, ref={v1.event.ref}")

    # Step 3: Human C also verifies (V)
    print("
[Step 3] Human supervisor confirms")
    v2 = VerifySkill.execute(
        issuer=agents["human-C"],
        verify_of=[j1.event.nonce],
        target=target,
        verification_result="confirmed",
        confidence=1.0,
    )
    print(f"  V event: nonce={v2.event.nonce}")

    # Step 4: Robot A delegates continuous monitoring to Robot B (D)
    print("
[Step 4] Robot A delegates continuous observation to Robot B")
    d1 = DelegateSkill.execute(
        issuer=agents["robot-A"],
        delegate_to=agents["robot-B"],
        target=target,
        scope="continuous_observation",
        prev_event_id=j1.event.nonce,
    )
    print(f"  D event: nonce={d1.event.nonce}, assignee in extensions")

    # Step 5: Robot B observes door closed (J, based on prior task)
    print("
[Step 5] Robot B observes door is now closed")
    j2 = JudgeSkill.execute(
        issuer=agents["robot-B"],
        target=target,
        subject="door_01",
        predicate="status",
        value="closed",
        confidence=0.92,
        parent_task_hash=j1.event.nonce,  # JAC-01: this is based on prior task
    )
    print(f"  J event: nonce={j2.event.nonce}, task_based_on={j2.event.task_based_on}")

    # Step 6: Robot A terminates old observation (T)
    print("
[Step 6] Robot A terminates the old 'open' observation")
    t1 = TerminateSkill.execute(
        issuer=agents["robot-A"],
        terminate_of=j1.event.nonce,
        target=target,
        reason="state_changed",
        prev_event_id=j2.event.nonce,
    )
    print(f"  T event: nonce={t1.event.nonce}, terminate_of={t1.event.what[:30]}...")

    # Step 7: Human C verifies the new state (V)
    print("
[Step 7] Human supervisor confirms the closed state")
    v3 = VerifySkill.execute(
        issuer=agents["human-C"],
        verify_of=[j2.event.nonce],
        target=target,
        verification_result="confirmed",
        confidence=1.0,
    )
    print(f"  V event: nonce={v3.event.nonce}")

    # Summary
    print("
" + "=" * 70)
    print("Workflow Summary")
    print("=" * 70)
    events = [j1, v1, v2, d1, j2, t1, v3]
    for i, e in enumerate(events, 1):
        print(f"  {i}. {e.event.verb.value} | {e.event.nonce[:8]}... | {e.event.who[:20]} | {e.message[:50]}")

    print("
All events are strict JEP-04 compliant and can be fed into:")
    print("  - Determinability-Checker (causal sufficiency verification)")
    print("  - COE-Consensus (shared world state formation)")
    print("  - JEP-Guard-Audit (compliance chain generation)")
    print("=" * 70)


if __name__ == "__main__":
    run_complex_workflow()
