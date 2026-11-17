"""Decision integrity — hash-chain sealing and verification.

Every DecisionRecord is sealed with a `record_hash` that chains it to the
previous revision.  This lets any participant verify that the decision history
has not been tampered with, without trusting the storage layer.
"""

from __future__ import annotations

import hashlib

from ..canonical import canonical_json
from ..models.schemas import DecisionRecord, DecisionRequest


def fingerprint_request(request: DecisionRequest) -> str:
    """Deterministic SHA-256 fingerprint of the decision request.

    Used as the `input_fingerprint` in the DecisionResult to anchor the
    evaluation to a specific input snapshot.
    """
    payload = request.model_dump(mode="json")
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def seal_record(record: DecisionRecord) -> DecisionRecord:
    """Compute and set the `record_hash` on a DecisionRecord.

    The hash covers the full record payload (request, result, approval,
    revision, parent_record_hash) in canonical JSON form.
    """
    payload = record.model_dump(mode="json", exclude={"record_hash"})
    digest = hashlib.sha256(canonical_json(payload)).hexdigest()
    return record.model_copy(update={"record_hash": digest})


def verify_record(record: DecisionRecord) -> bool:
    """Verify that the record_hash matches the record payload."""
    import hmac

    payload = record.model_dump(mode="json", exclude={"record_hash"})
    expected = hashlib.sha256(canonical_json(payload)).hexdigest()
    return hmac.compare_digest(record.record_hash, expected)


def verify_chain(records: list[DecisionRecord]) -> bool:
    """Verify a monotonic hash-chain of decision records.

    Checks:
      1. Revisions are strictly increasing by 1.
      2. Each record's record_hash is self-consistent.
      3. Each record's parent_record_hash matches the previous record's record_hash.
    """
    if not records:
        return True

    for i, record in enumerate(records):
        if not verify_record(record):
            return False

        expected_revision = i + 1
        if record.revision != expected_revision:
            return False

        if i > 0:
            if record.parent_record_hash != records[i - 1].record_hash:
                return False

    return True