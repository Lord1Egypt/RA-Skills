"""Shared redaction helpers for account identifiers in safe diagnostics."""
from __future__ import annotations

import re


_ACCOUNT_LABEL = re.compile(
    r"\b(?:account[ _-]?(?:number|no\.?|id)|acct[ _-]?id|account)"
    r"(?:\s*[:=]\s*|\s+)[^\s&,;]+",
    re.IGNORECASE,
)
_RETAIL_ACCOUNT = re.compile(r"\b(?:DU|U|D|F)\d{4,}\b")


def redact_account_identifiers(message: str) -> str:
    """Remove labelled institutional IDs and standard retail account IDs."""
    redacted = _ACCOUNT_LABEL.sub("account_id=[REDACTED]", message)
    return _RETAIL_ACCOUNT.sub("[REDACTED_ACCOUNT]", redacted)
