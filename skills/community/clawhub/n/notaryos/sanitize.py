# SECURITY MANIFEST:
#   Environment variables accessed: none
#   External endpoints called: none
#   Local files read: none
#   Local files written: none
#   Network calls: none
#   eval/exec usage: none
#   subprocess usage: none
#
# This module is a pure-function payload filter. It takes a dict, removes
# fields matching known sensitive patterns, and returns a new dict. No I/O,
# no network, no side effects.
"""
sanitize.py — Payload sanitization for NotaryOS receipts.

Strips fields matching known sensitive patterns from dicts before they are
sealed and transmitted to the NotaryOS API. Pure function — no network calls,
no file access, no imports beyond typing.

Usage:
    from sanitize import sanitize_payload

    clean = sanitize_payload(raw_payload)
    receipt = notary.seal("action", clean)

BSL-1.1 — https://github.com/hellothere012/notaryos/blob/main/LICENSE
"""

from typing import Any, Dict, Optional, Set

# Field names that are stripped (case-insensitive exact match).
_BLOCKED_FIELDS: Set[str] = {
    "passwd", "bearer", "credentials",
    "private_key", "signing_key",
    "cvv", "cvc", "expiry",
    "account_number", "routing_number",
    "iban", "swift", "bank_account",
    "ssn", "social_security", "national_id",
    "passport_number", "drivers_license",
    "dob", "date_of_birth",
}

# Substrings in field names that indicate sensitivity.
_BLOCKED_SUBSTRINGS = (
    "password", "secret", "token", "credential",
    "api_key", "apikey",
)


def sanitize_payload(
    payload: Dict[str, Any],
    extra_fields: Optional[Set[str]] = None,
    redact: bool = False,
) -> Dict[str, Any]:
    """
    Remove sensitive fields from a payload dict.

    Args:
        payload: Raw dict to sanitize.
        extra_fields: Additional field names to strip.
        redact: If True, replace values with "[REDACTED]" instead of removing.

    Returns:
        New dict with sensitive fields removed. Original is not modified.
    """
    blocked = _BLOCKED_FIELDS | (extra_fields or set())
    result: Dict[str, Any] = {}

    for key, value in payload.items():
        lower = key.lower()

        if lower in blocked or any(p in lower for p in _BLOCKED_SUBSTRINGS):
            if redact:
                result[key] = "[REDACTED]"
            continue

        if isinstance(value, dict):
            result[key] = sanitize_payload(value, extra_fields, redact)
        elif isinstance(value, list):
            result[key] = [
                sanitize_payload(item, extra_fields, redact)
                if isinstance(item, dict) else item
                for item in value
            ]
        else:
            result[key] = value

    return result


def seal_safe(notary, action_type: str, payload: Dict[str, Any], **kwargs):
    """Sanitize then seal in one step."""
    return notary.seal(action_type, sanitize_payload(payload), **kwargs)


# Self-test
if __name__ == "__main__":
    tests_passed = 0

    # 1: Basic removal
    out = sanitize_payload({"user": "alice", "passwd": "x", "action": "login"})
    assert "passwd" not in out and out["user"] == "alice"
    tests_passed += 1

    # 2: Nested
    out = sanitize_payload({"config": {"host": "db", "bearer": "x"}, "name": "svc"})
    assert "bearer" not in out["config"] and out["config"]["host"] == "db"
    tests_passed += 1

    # 3: Substring match
    out = sanitize_payload({"db_secret_key": "x", "display_name": "Alice"})
    assert "db_secret_key" not in out and out["display_name"] == "Alice"
    tests_passed += 1

    # 4: Redact mode
    out = sanitize_payload({"passwd": "x", "user": "a"}, redact=True)
    assert out["passwd"] == "[REDACTED]" and out["user"] == "a"
    tests_passed += 1

    # 5: Extra fields
    out = sanitize_payload({"email": "a@b.com", "name": "A"}, extra_fields={"email"})
    assert "email" not in out and out["name"] == "A"
    tests_passed += 1

    print(f"sanitize.py: {tests_passed}/5 tests passed")
