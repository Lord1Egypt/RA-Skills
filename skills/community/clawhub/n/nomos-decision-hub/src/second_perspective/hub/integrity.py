"""Hub report integrity — hash-chain sealing and verification.

Every HubReport is sealed with a `report_hash` that covers the full report
payload.  This lets any participant verify that the report has not been
tampered with.
"""

from __future__ import annotations

import hashlib
import hmac

from ..canonical import canonical_json
from ..models.hub import HubReport


def seal_hub_report(report: HubReport) -> HubReport:
    """Compute and set the `report_hash` on a HubReport."""
    payload = report.model_dump(mode="json", exclude={"report_hash"})
    digest = hashlib.sha256(canonical_json(payload)).hexdigest()
    return report.model_copy(update={"report_hash": digest})


def verify_hub_report(report: HubReport) -> bool:
    """Verify that the report_hash matches the report payload."""
    if not report.report_hash:
        return False
    payload = report.model_dump(mode="json", exclude={"report_hash"})
    expected = hashlib.sha256(canonical_json(payload)).hexdigest()
    return hmac.compare_digest(report.report_hash, expected)