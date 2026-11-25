"""Path and identifier safety helpers (v0.3.1).

Every file path in this skill that contains a user-supplied identifier must go
through these helpers. They reject traversal sequences, separators and absolute
paths before a single byte is written.
"""

import re
from pathlib import Path

_SAFE_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")


def safe_component(value, fallback="unknown"):
    """Return a single safe path component, or ``fallback`` if unsafe."""
    if value is None:
        return fallback
    text = str(value).strip()
    if text in {"", ".", ".."} or not _SAFE_COMPONENT.fullmatch(text):
        return fallback
    return text


def validate_identifier(value, field_name):
    """Strict check for an identifier; raise ValueError when unsafe."""
    text = str(value or "").strip()
    if text in {"", ".", ".."} or not _SAFE_COMPONENT.fullmatch(text):
        raise ValueError(f"不安全的 {field_name}: {text!r}")
    return text


def safe_join(base, *parts):
    """Join sanitized parts under ``base`` and guarantee containment."""
    root = Path(base).resolve()
    candidates = [safe_component(part) for part in parts]
    target = root.joinpath(*candidates).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return root / safe_component(candidates[-1] if candidates else "unknown")
    return target
