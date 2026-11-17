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
from skill.security import sign_event,b64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from datetime import datetime,timezone
from uuid import uuid4
keys={i:Ed25519PrivateKey.generate() for i in ['agent','auditor']}
public={i:{'test':b64(k.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw))} for i,k in keys.items()}
ids={i:str(uuid4()) for i in ['a','b']}
def admit(engine,session,event):
    event.event_id=ids[event.event_id]
    event.timestamp=datetime.now(timezone.utc).isoformat()
    if event.verify_of: event.verify_of=[ids.get(i,i) for i in event.verify_of]
    if event.prev_event_id: event.prev_event_id=ids.get(event.prev_event_id,event.prev_event_id)
    event.signature=sign_event(event,{'purpose':'audit','tenant':'local','session':session},keys[event.issuer],'test')
    engine.ingest(session,event)



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
        event_id=str(uuid4()), primitive="J", issuer="agent-a",
        timestamp="2026-04-26T10:00:00Z", target="t1",
        assertion={"s": "x", "p": "y", "v": 1},
        confidence=0.9, prev_event_id=None, parent_task_hash="parent-1",
        signature="sig-1"
    )
    jep = JEPAdapter.to_jep04(fe)
    assert jep.jep == "1"
    assert jep.verb == Verb.JUDGE
    assert jep.who == "agent-a"
    assert jep.when == int(datetime(2026,4,26,10,tzinfo=timezone.utc).timestamp())  # Unix seconds for 2026-04-26T10:00:00Z
    assert jep.aud == "t1"
    assert jep.task_based_on == "parent-1"
    assert jep.sig == "sig-1"
    assert jep.nonce != ""  # Auto-generated UUIDv4
    assert jep.what is not None  # Computed from assertion


def test_audit_engine_valid_chain():
    """Two events with correct ref -> valid chain."""
    engine = AuditEngine(":memory:",public)
    session = "test-1"
    admit(engine,session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x", "p": "y", "v": 1}, signature="sig-a"
    ))
    admit(engine,session, FriendlyEvent(
        event_id="b", primitive="V", issuer="auditor", timestamp="2026-04-26T10:00:05Z",
        target="t", verify_of=["a"], verification_result="confirmed", signature="sig-b"
    ))
    chain = engine.build_chain(session)
    assert chain.chain_valid is True
    assert chain.violation_count == 0


def test_audit_engine_missing_verification():
    """Judge without Verify -> R001 WARNING."""
    engine = AuditEngine(":memory:",public)
    session = "test-2"
    admit(engine,session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x", "p": "y", "v": 1}, signature="sig"
    ))
    chain = engine.build_chain(session)
    assert chain.warning_count >= 1
    assert any("R001" in v for v in chain.links[0].violations)


def test_audit_engine_orphan_termination():
    """Terminate referencing non-existent -> R003 VIOLATION."""
    engine = AuditEngine(":memory:",public)
    session = "test-3"
    admit(engine,session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x", "p": "y", "v": 1}, signature="sig"
    ))
    admit(engine,session, FriendlyEvent(
        event_id="b", primitive="T", issuer="agent", timestamp="2026-04-26T10:00:05Z",
        target="t", terminate_of="nonexistent", prev_event_id="a", signature="sig"
    ))
    chain = engine.build_chain(session)
    assert chain.violation_count >= 1
    assert any("authority" in v for v in chain.links[1].violations)


def test_compliance_export_generic():
    """Generic export must contain JEP-04 fields."""
    engine = AuditEngine(":memory:",public)
    session = "test-4"
    admit(engine,session, FriendlyEvent(
        event_id="a", primitive="J", issuer="agent", timestamp="2026-04-26T10:00:00Z",
        target="t", assertion={"s": "x"}, signature="sig"
    ))
    report = engine.export_compliance(session, ComplianceStandard.GENERIC)
    assert report.standard == ComplianceStandard.GENERIC
    assert "jep-audit-security-v1" in report.raw_data
    assert any("not legal compliance" in r for r in report.recommendations)


if __name__ == "__main__":
    test_jep_codec_canonicalization()
    test_jep_codec_what_computation()
    test_jep_adapter_roundtrip()
    test_audit_engine_valid_chain()
    test_audit_engine_missing_verification()
    test_audit_engine_orphan_termination()
    test_compliance_export_generic()
    print("All 7 tests passed.")
