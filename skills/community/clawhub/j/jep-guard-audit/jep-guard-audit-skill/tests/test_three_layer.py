"""
Three-Layer Architecture Unit Tests
Tests JEPCodec (strict), JEPAdapter (mapping), and AuditEngine (business logic).
Run: pytest tests/test_three_layer.py
"""
import sys
sys.path.insert(0, "..")

from skill.codec import JEPCodec
from skill.adapter import JEPAdapter
from skill.core import AuditEngine
from skill.types import FriendlyEvent, Verb, ComplianceStandard


def test_jep_codec_canonicalization():
    """JEPCodec.encode must produce deterministic canonical JSON."""
    from skill.types import JEP04Event
    evt = JEP04Event(
        jep="1", verb=Verb.JUDGE, who="did:example:a", when=1000,
        what="sha256:abc", nonce="uuid-1", aud="platform", ref=None, sig="sig"
    )
    c1 = JEPCodec.encode(evt)
    c2 = JEPCodec.encode(evt)
    assert c1 == c2, "Canonicalization must be deterministic"
    assert '"jep":"1"' in c1
    assert '"verb":"J"' in c1


def test_jep_codec_what_computation():
    """JEPCodec.compute_what must produce sha256: prefix multihash."""
    payload = {"subject": "x", "predicate": "y", "value": 1}
    what = JEPCodec.compute_what(payload)
    assert what.startswith("sha256:")
    assert len(what) == 64 + 7  # prefix + 64 hex chars


def test_jep_adapter_roundtrip():
    """JEPAdapter.to_jep04 must map all friendly fields correctly."""
    fe = FriendlyEvent(
        event_id="evt-1", primitive="J", issuer="agent-a",
        timestamp="2026-04-26T10:00:00Z", target="t1",
        assertion={"s": "x", "p": "y", "v": 1},
        confidence=0.9, prev_event_id=None, parent_task_hash="parent-1",
        signature="sig-1"
    )
    jep = JEPAdapter.to_jep04(fe)
    assert jep.jep == "1"
    assert jep.verb == Verb.JUDGE
    assert jep.who == "agent-a"
    assert jep.when == 1745661600  # Unix seconds for 2026-04-26T10:00:00Z
    assert jep.aud == "t1"
    assert jep.task_based_on == "parent-1"
    assert jep.sig == "sig-1"
    assert jep.nonce != ""  # Auto-generated UUIDv4
    assert jep.what is not None  # Computed from assertion


def test_audit_engine_valid_chain():
    """Two events with correct ref -> valid chain."""
    engine = AuditEngine()
    session = "test-1"
    engine.ingest(session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x", "p": "y", "v": 1}, signature="sig-a"
    ))
    engine.ingest(session, FriendlyEvent(
        event_id="b", primitive="V", issuer="auditor", timestamp="2026-04-26T10:00:05Z",
        target="t", verify_of=["a"], verification_result="confirmed", signature="sig-b"
    ))
    chain = engine.build_chain(session)
    assert chain.chain_valid is True
    assert chain.violation_count == 0


def test_audit_engine_missing_verification():
    """Judge without Verify -> R001 WARNING."""
    engine = AuditEngine()
    session = "test-2"
    engine.ingest(session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x", "p": "y", "v": 1}, signature="sig"
    ))
    chain = engine.build_chain(session)
    assert chain.warning_count >= 1
    assert any("R001" in v for v in chain.links[0].violations)


def test_audit_engine_orphan_termination():
    """Terminate referencing non-existent -> R003 VIOLATION."""
    engine = AuditEngine()
    session = "test-3"
    engine.ingest(session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x", "p": "y", "v": 1}, signature="sig"
    ))
    engine.ingest(session, FriendlyEvent(
        event_id="b", primitive="T", issuer="agent", timestamp="2026-04-26T10:00:05Z",
        target="t", terminate_of="nonexistent", prev_event_id="a", signature="sig"
    ))
    chain = engine.build_chain(session)
    assert chain.violation_count >= 1
    assert any("R003" in v for v in chain.links[1].violations)


def test_compliance_export_generic():
    """Generic export must contain JEP-04 fields."""
    engine = AuditEngine()
    session = "test-4"
    engine.ingest(session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x"}, signature="sig"
    ))
    report = engine.export_compliance(session, ComplianceStandard.GENERIC)
    assert report.standard == ComplianceStandard.GENERIC
    assert "JEP-04" in report.raw_data
    assert "JAC-01" in report.raw_data


if __name__ == "__main__":
    test_jep_codec_canonicalization()
    test_jep_codec_what_computation()
    test_jep_adapter_roundtrip()
    test_audit_engine_valid_chain()
    test_audit_engine_missing_verification()
    test_audit_engine_orphan_termination()
    test_compliance_export_generic()
    print("All 7 tests passed.")
