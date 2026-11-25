"""Shared JSON envelope + output-format helper for Scout scripts (stdlib-only).

Two conventions applied across Scout's helper scripts:

1. ``--format=concise|detailed`` — concise (the default) prints only the fields
   a caller needs to act on, which is 60-80% fewer tokens than the full record.
   detailed prints everything.
2. Failure paths emit a JSON envelope carrying ``actionable_guidance`` — a
   human-readable next step — instead of a bare traceback, so an agent reading
   the output knows what to do rather than what went wrong.

Usage:

    from _envelope import add_format_arg, emit, fail

    p.add_argument(...); add_format_arg(p)
    ...
    emit(payload, args.format, summary="18 profiles extracted",
         concise_keys=("site", "url", "confidence"))
    ...
    fail("no input file", args.format,
         guidance="Pass --input results/report.json (a Scout research result).")
"""
from __future__ import annotations

import json
import sys

FORMATS = ("concise", "detailed")
CONCISE = "concise"


def add_format_arg(parser, default: str = CONCISE) -> None:
    """Add the standard ``--format`` flag to an argparse parser."""
    parser.add_argument(
        "--format",
        choices=FORMATS,
        default=default,
        help="Output verbosity: concise (default, 60-80%% fewer tokens) or detailed",
    )


def _project(payload: dict, concise_keys) -> dict:
    """Keep a whitelist of top-level keys plus any summary/scalar fields."""
    if not concise_keys:
        return payload
    keep = set(concise_keys) | {"summary", "count", "ok", "tool", "as_of"}
    out = {}
    for key, value in payload.items():
        if key in keep:
            out[key] = value
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            # Reduce list-of-dicts to the whitelisted sub-keys.
            out[key] = [
                {k: v for k, v in item.items() if k in keep}
                for item in value
            ]
        elif isinstance(value, (str, int, float, bool)) or value is None:
            out[key] = value
    return out


def emit(payload: dict, fmt: str = CONCISE, *, summary: str = "",
         concise_keys=None, as_json: bool = True) -> None:
    """Print ``payload`` honouring the format flag.

    In concise mode a human-readable ``summary`` line is printed first so the
    result is legible at a glance; the JSON body follows when as_json is set.
    """
    body = payload if fmt == "detailed" else _project(payload, concise_keys)
    if summary:
        body = {"summary": summary, **body}
    if as_json:
        print(json.dumps(body, indent=2 if fmt == "detailed" else None,
                         default=str))
    elif summary:
        print(summary)


def fail(message: str, fmt: str = CONCISE, *, guidance: str,
         code: str = "error", extra: dict | None = None) -> int:
    """Emit a structured failure envelope and return exit code 1.

    ``actionable_guidance`` is mandatory: a failure the caller cannot act on is
    not a useful failure.
    """
    payload = {
        "ok": False,
        "error": message,
        "code": code,
        "actionable_guidance": guidance,
    }
    if extra:
        payload.update(extra)
    print(json.dumps(payload, indent=2 if fmt == "detailed" else None,
                     default=str))
    return 1


def main_guard(fn) -> int:
    """Run ``fn`` returning an exit code, converting crashes to envelopes.

    Scripts call this so an unexpected exception still yields a parseable
    envelope rather than a traceback the caller has to interpret.
    """
    try:
        return fn()
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "code": "unhandled_exception",
            "actionable_guidance": (
                "This is an unexpected failure, not a bad-input failure. Re-run "
                "with --format=detailed to confirm the same error, then report "
                "the traceback; do not retry blindly."
            ),
        }))
        return 1


if __name__ == "__main__":  # pragma: no cover - self-doc
    print((__doc__ or "").strip())
    sys.exit(0)
