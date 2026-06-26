"""Resolve {{INTERPOLATE_js:path}} (alias `{{@js:path}}`) placeholders; emit `#` markers for round-trip.

Marker forms:
  - `/* #:js:path */` — preferred form, what `resolve()` writes (and what primitives use).
  - `/* MATCH:js:path */` — canonical long form, also accepted on read.
  - `/* DEHYDRATE:js:path */` — legacy form, accepted on read so existing deployed
    workflows roll forward to the new placeholder syntax on next dehydrate.
"""
import json
import re
from pathlib import Path

PATTERN = re.compile(r"\{\{(?:INTERPOLATE_|@)js:([^}]+)\}\}")
MATCH_OPEN = "/* #:js:{path} */"
MATCH_CLOSE = "/* /#:js:{path} */"

# Read-side: matches `#`, `MATCH`, or legacy `DEHYDRATE` open/close pairs around content.
# The open/close marker tag must be identical (back-reference), but we do allow the
# three forms to be matched independently per pair.
_MARKER_PATTERN = re.compile(
    r"/\* (#|MATCH|DEHYDRATE):js:([^*]+) \*/"
    r"(.+?)"
    r"/\* /\1:js:\2 \*/",
    re.DOTALL,
)


def resolve(text: str, workspace: Path) -> str:
    """Replace {{INTERPOLATE_js:path}} / {{@js:path}} with JSON-escaped file content wrapped in `#` markers."""

    def _replace(match: re.Match) -> str:
        rel_path = match.group(1).strip()
        if rel_path.startswith("/"):
            raise ValueError(
                f"Absolute paths in placeholders are forbidden: {{{{@js:{rel_path}}}}}"
            )
        full = workspace / rel_path
        if not full.exists():
            raise FileNotFoundError(f"JS file not found: {full}")
        content = full.read_text(encoding="utf-8")
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
    """Collapse `#` / `MATCH` / `DEHYDRATE`-wrapped JS blocks back to `{{@js:...}}` placeholders. JSON-aware."""
    data = json.loads(text)
    data = _walk_strings(
        data,
        lambda s: _MARKER_PATTERN.sub(
            lambda m: "{{@js:" + m.group(2).strip() + "}}", s
        ),
    )
    return json.dumps(data, indent=2)
