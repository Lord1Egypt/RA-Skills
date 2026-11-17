"""P0 Φ-gate — lean self-contained ethical pre-filter for Smart Disk Agent."""
from __future__ import annotations

import re
from typing import Any

SIGNATURE = "Δ9Φ963-SDA-P0-GATE-v1"

# High-signal quarantine patterns (abuse / exfil / destructive)
_QUARANTINE = re.compile(
    r"("
    r"rm\s+-rf\s+/|"
    r"format\s+c:|"
    r"mimikatz|"
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions|"
    r"exfiltrate\s+secrets|"
    r"disable\s+safety|"
    r"child\s+sexual|"
    r"make\s+a\s+bomb\s+detailed"
    r")",
    re.I,
)

_MAX_CHARS = 12000


class P0Gate:
    def validate(self, text: str) -> dict[str, Any]:
        t = (text or "").strip()
        if not t:
            return {"verdict": "ALLOW", "reason": "empty", "signature": SIGNATURE}
        if len(t) > _MAX_CHARS:
            return {
                "verdict": "QUARANTINE",
                "reason": f"payload_exceeds_{_MAX_CHARS}",
                "signature": SIGNATURE,
            }
        if _QUARANTINE.search(t):
            return {
                "verdict": "QUARANTINE",
                "reason": "matched_p0_policy_pattern",
                "signature": SIGNATURE,
            }
        # crude entropy-ish: long random base64-looking blobs
        if len(t) > 4000 and len(set(t)) > 80 and " " not in t[:200]:
            return {
                "verdict": "QUARANTINE",
                "reason": "high_entropy_blob",
                "signature": SIGNATURE,
            }
        return {"verdict": "ALLOW", "reason": "ok", "signature": SIGNATURE}
