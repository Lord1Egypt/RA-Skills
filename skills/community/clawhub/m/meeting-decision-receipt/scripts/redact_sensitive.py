#!/usr/bin/env python3
"""Redact common credentials and contact data from text or JSON.

The script never prints detected source values in its report. It can also be
imported by validators and tests through ``redact_text`` and ``redact_value``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable


Replacement = Callable[[re.Match[str]], str]


def _marker(category: str) -> str:
    return f"[REDACTED:{category.upper()}]"


def _assignment_category(label: str) -> str:
    normalized = re.sub(r"[\s_-]+", "", label.lower())
    if normalized in {"password", "passwd", "pwd", "密码", "口令"}:
        return "password"
    if "api" in normalized and "key" in normalized:
        return "api_key"
    if "token" in normalized:
        return "token"
    return "credential"


ASSIGNMENT_RE = re.compile(
    r"(?i)(?P<prefix>\b(?P<label>api[\s_-]?key|access[\s_-]?token|refresh[\s_-]?token|token|password|passwd|pwd|secret|密码|口令)\b"
    r"[\"']?\s*[:=：]\s*[\"']?)(?P<value>[^\s,;，；\"']{4,})(?P<suffix>[\"']?)"
)


PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("token", re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")),
    ("api_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{12,}\b")),
    ("api_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("token", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
    ("email", re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])")),
    ("phone", re.compile(r"(?<!\d)(?:\+?86[\s-]?)?1[3-9]\d{9}(?!\d)")),
]


def redact_text(text: str, custom_terms: list[str] | None = None) -> tuple[str, Counter[str]]:
    """Return redacted text and category counts without retaining raw matches."""

    counts: Counter[str] = Counter()

    def replace_assignment(match: re.Match[str]) -> str:
        category = _assignment_category(match.group("label"))
        counts[category] += 1
        return f"{match.group('prefix')}{_marker(category)}{match.group('suffix')}"

    redacted = ASSIGNMENT_RE.sub(replace_assignment, text)

    for category, pattern in PATTERNS:
        def replacement(match: re.Match[str], current: str = category) -> str:
            counts[current] += 1
            if current == "token" and match.group(0).lower().startswith("bearer "):
                return f"Bearer {_marker(current)}"
            return _marker(current)

        redacted = pattern.sub(replacement, redacted)

    for term in sorted({item for item in (custom_terms or []) if item}, key=len, reverse=True):
        occurrences = redacted.count(term)
        if occurrences:
            redacted = redacted.replace(term, _marker("other"))
            counts["other"] += occurrences

    return redacted, counts


def redact_value(value: Any, custom_terms: list[str] | None = None) -> tuple[Any, Counter[str]]:
    """Recursively redact every string value inside JSON-compatible data."""

    if isinstance(value, str):
        return redact_text(value, custom_terms)
    if isinstance(value, list):
        result: list[Any] = []
        counts: Counter[str] = Counter()
        for item in value:
            redacted, item_counts = redact_value(item, custom_terms)
            result.append(redacted)
            counts.update(item_counts)
        return result, counts
    if isinstance(value, dict):
        result_dict: dict[str, Any] = {}
        counts = Counter()
        for key, item in value.items():
            redacted, item_counts = redact_value(item, custom_terms)
            result_dict[key] = redacted
            counts.update(item_counts)
        return result_dict, counts
    return value, Counter()


def _read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def _write_output(path: str | None, content: str) -> None:
    if path:
        Path(path).write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Redact credentials, phone numbers, and email addresses.")
    parser.add_argument("--input", help="Input file. Reads stdin when omitted.")
    parser.add_argument("--output", help="Output file. Writes stdout when omitted.")
    parser.add_argument("--mode", choices=["auto", "text", "json"], default="auto")
    parser.add_argument("--report", help="Write a count-only JSON report to this path.")
    parser.add_argument("--redact-term", action="append", default=[], help="Also redact this exact project, company, or client term. Repeatable.")
    parser.add_argument("--fail-on-detection", action="store_true", help="Exit 1 when anything was redacted.")
    args = parser.parse_args()

    raw = _read_input(args.input)
    mode = args.mode
    if mode == "auto":
        mode = "json" if args.input and Path(args.input).suffix.lower() == ".json" else "text"

    try:
        if mode == "json":
            data = json.loads(raw)
            redacted, counts = redact_value(data, args.redact_term)
            output = json.dumps(redacted, ensure_ascii=False, indent=2) + "\n"
        else:
            output, counts = redact_text(raw, args.redact_term)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"redaction error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    _write_output(args.output, output)
    report = {
        "redactions": sum(counts.values()),
        "categories": dict(sorted(counts.items())),
        "contains_sensitive_content": bool(counts),
    }
    if args.report:
        Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif args.output:
        print(json.dumps(report, ensure_ascii=False), file=sys.stderr)

    if args.fail_on_detection and counts:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
