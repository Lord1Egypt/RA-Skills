"""
Primitive Skills Unit Tests
Run: pytest tests/test_primitives.py
"""
import sys
sys.path.insert(0, "..")

from skill.primitives import JudgeSkill, DelegateSkill, TerminateSkill, VerifySkill
from skill.types import Verb


def test_judge_skill():
    r = JudgeSkill.execute(
        issuer="did:example:a", target="t1", subject="door",
        predicate="status", value="open", confidence=0.95
    )
    assert r.success is True
    assert r.event.verb == Verb.JUDGE
    assert r.event.who == "did:example:a"
    assert r.event.aud == "t1"
    assert r.event.what is not None  # multihash computed
    assert r.event.nonce != ""
    assert r.next_suggested_primitive == "V"


def test_delegate_skill():
    r = DelegateSkill.execute(
        issuer="did:example:a", delegate_to="did:example:b",
        target="t1", scope="continuous_observation"
    )
    assert r.success is True
    assert r.event.verb == Verb.DELEGATE
    assert r.event.who == "did:example:a"
    assert r.next_suggested_primitive == "J"
    # Check JAC assign extension
    assert r.event.extensions is not None
    assert "https://jac.org/assign" in r.event.extensions


def test_terminate_skill():
    r = TerminateSkill.execute(
        issuer="did:example:a", terminate_of="evt-123",
        target="t1", reason="state_changed"
    )
    assert r.success is True
    assert r.event.verb == Verb.TERMINATE
    assert r.event.who == "did:example:a"
    assert r.next_suggested_primitive == "J"
    # Check JAC fault extension
    assert r.event.extensions is not None
    assert "https://jac.org/fault" in r.event.extensions


def test_verify_skill():
    r = VerifySkill.execute(
        issuer="did:example:b", verify_of=["evt-123"],
        target="t1", verification_result="confirmed", confidence=0.9
    )
    assert r.success is True
    assert r.event.verb == Verb.VERIFY
    assert r.event.who == "did:example:b"
    assert r.event.ref == "evt-123"
    assert r.next_suggested_primitive == "V"


def test_judge_with_parent_task():
    r = JudgeSkill.execute(
        issuer="did:example:a", target="t1", subject="door",
        predicate="status", value="closed", parent_task_hash="parent-001"
    )
    assert r.event.task_based_on == "parent-001"


def test_verify_rejected():
    r = VerifySkill.execute(
        issuer="did:example:c", verify_of=["evt-456"],
        target="t1", verification_result="rejected"
    )
    assert r.event.extensions is not None
    jac_result = r.event.extensions.get("https://jac.org/result")
    assert jac_result["verification_result"] == "rejected"


if __name__ == "__main__":
    test_judge_skill()
    test_delegate_skill()
    test_terminate_skill()
    test_verify_skill()
    test_judge_with_parent_task()
    test_verify_rejected()
    print("All 6 tests passed.")
