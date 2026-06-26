"""Resolve {{INTERPOLATE_py:path}} (alias `{{@py:path}}`) placeholders; emit `MATCH` markers for round-trip.

Marker forms:
  - `# MATCH:py:path` — what `resolve()` writes; canonical and only writeable form for
    Python (no `#` alias because `# #:py:path` is unreadable).
  - `# DEHYDRATE:py:path` — legacy form, accepted on read so existing deployed
    workflows roll forward to the new placeholder syntax on next dehydrate.
"""
import json
import re
from pathlib import Path

PATTERN = re.compile(r"\{\{(?:INTERPOLATE_|@)py:([^}]+)\}\}")
MATCH_OPEN = "# MATCH:py:{path}"
MATCH_CLOSE = "# /MATCH:py:{path}"

_MARKER_PATTERN = re.compile(
    r"# (MATCH|DEHYDRATE):py:([^\n]+)\n(.+?)\n# /\1:py:\2",
    re.DOTALL,
)

# Source-file collision guards. A user's *.py source must contain none of these substrings.
_FORBIDDEN_MARKER_SUBSTRINGS = (
    "# MATCH:py:",
    "# /MATCH:py:",
    "# DEHYDRATE:py:",
    "# /DEHYDRATE:py:",
)


def resolve(text: str, workspace: Path) -> str:
    """Replace {{INTERPOLATE_py:path}} / {{@py:path}} with JSON-escaped Python content wrapped in `MATCH` markers."""

    def _replace(match: re.Match) -> str:
        rel_path = match.group(1).strip()
        if rel_path.startswith("/"):
            raise ValueError(
                f"Absolute paths in placeholders are forbidden: {{{{@py:{rel_path}}}}}"
            )
        full = workspace / rel_path
        if not full.exists():
            raise FileNotFoundError(f"Python file not found: {full}")
        content = full.read_text(encoding="utf-8")
        for forbidden in _FORBIDDEN_MARKER_SUBSTRINGS:
            if forbidden in content:
                raise ValueError(
                    f"Python file {rel_path} contains a MATCH/DEHYDRATE marker substring; "
                    "this would corrupt round-trip dehydration. Remove the marker from the source."
                )
        block = (
            MATCH_OPEN.format(path=rel_path) + "\n"
            + content.rstrip("\n") + "\n"
            + MATCH_CLOSE.format(path=rel_path)
        )
        return json.dumps(block)[1:-1]

    return PATTERN.sub(_replace, text)


def _walk_strings(obj, fn):
    if isinstance(obj, dict):
        return {k: _walk_strings(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_walk_strings(v, fn) for v in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj


def dehydrate(text: str) -> str:
    """Collapse `MATCH`/`DEHYDRATE`-wrapped Python blocks back to `{{@py:...}}` placeholders. JSON-aware."""
    data = json.loads(text)
    data = _walk_strings(
        data,
        lambda s: _MARKER_PATTERN.sub(
            lambda m: "{{@py:" + m.group(2).strip() + "}}", s
        ),
    )
    return json.dumps(data, indent=2)
