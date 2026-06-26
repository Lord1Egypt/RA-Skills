#!/usr/bin/env python3
"""Secure log analyzer for OpenClaw / local services.

Reads only from whitelisted log paths. Sanitizes output to remove
tokens, keys, and passwords. Supports error detection, pattern search,
and summarization. Configurable via config file.

Usage:
    analyzer.py                          # Recent errors summary
    analyzer.py --source openclaw        # OpenClaw logs (journalctl)
    analyzer.py --source rag             # RAG indexing logs
    analyzer.py --source queries         # RAG query logs
    analyzer.py --source gateway         # Gateway logs (journalctl)
    analyzer.py --search "pattern"       # Search across all sources
    analyzer.py --last N                 # Last N lines
    analyzer.py --json                   # JSON output
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/.config/log-analyzer/config.json")

ALLOWED_SOURCES = {
    "openclaw": {"type": "journalctl", "unit": "openclaw-gateway"},
    "gateway": {"type": "journalctl", "unit": "openclaw-gateway"},
    "rag": {"type": "file", "path": os.path.expanduser("~/.local/share/local-rag/index-batch.log")},
    "queries": {"type": "file", "path": os.path.expanduser("~/.local/share/local-rag/queries.log")},
}

DEFAULT_REDACT = [
    (r'(token["\s:=]+)["\']?([a-zA-Z0-9_-]{20,})["\']?', r'\1[REDACTED]'),
    (r'(key["\s:=]+)["\']?([a-zA-Z0-9_-]{20,})["\']?', r'\1[REDACTED]'),
    (r'(?i)(password|passwd|pwd)["\s:=]+["\']?([^\s"\']+)["\']?', r'\1[REDACTED]'),
    (r'(?i)(secret["\s:=]+)["\']?([^\s"\']+)["\']?', r'\1[REDACTED]'),
    (r'(Authorization:\s*Bearer\s+)(\S+)', r'\1[REDACTED]'),
    (r'(age1[a-z0-9]{50,})', r'[KEY-REDACTED]'),
    (r'(sk-[a-zA-Z0-9]{20,})', r'[KEY-REDACTED]'),
    (r'(sm_[a-zA-Z0-9]{20,})', r'[KEY-REDACTED]'),
    (r'\b\d{16,19}\b', r'[CARD-REDACTED]'),
    (r'(?i)(base64[A-Za-z0-9+/=]{40,})', r'[BASE64-REDACTED]'),
]

DEFAULT_ERROR_PATTERNS = [
    r'\bERROR\b', r'\bFATAL\b', r'\bCRITICAL\b', r'\bPANIC\b',
    r'\bOOM\b', r'\bSIGKILL\b', r'\bSIGTERM\b', r'\bkilled\b',
    r'\bFAILED\b', r'\btimeout\b', r'\brefused\b', r'\bdenied\b',
    r'\btraceback\b', r'\bexception\b', r'\bsegfault\b',
]


def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_error_patterns():
    cfg = load_config()
    return cfg.get("error_patterns", DEFAULT_ERROR_PATTERNS)


def get_redact_patterns():
    cfg = load_config()
    return cfg.get("redact_patterns", DEFAULT_REDACT)


def sanitize(line: str) -> str:
    for pattern, replacement in get_redact_patterns():
        line = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
    return line


def read_journalctl(unit: str, lines: int = 100) -> list[str]:
    try:
        result = subprocess.run(
            ["journalctl", "--user", "-u", unit, "-n", str(lines), "--no-pager"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"(journalctl failed: {e})"]


def read_file_log(path: str, lines: int = 100) -> list[str]:
    if not os.path.exists(path):
        return [f"(log file not found: {path})"]
    try:
        with open(path) as f:
            all_lines = f.readlines()
        return [l.rstrip() for l in all_lines[-lines:]]
    except Exception as e:
        return [f"(read failed: {e})"]


def get_logs(source: str, lines: int = 100) -> list[str]:
    if source not in ALLOWED_SOURCES:
        return [f"(unknown source: {source})"]
    cfg = ALLOWED_SOURCES[source]
    if cfg["type"] == "journalctl":
        return read_journalctl(cfg["unit"], lines)
    elif cfg["type"] == "file":
        return read_file_log(cfg["path"], lines)
    return []


def get_all_logs(lines: int = 50) -> dict[str, list[str]]:
    return {source: get_logs(source, lines) for source in ALLOWED_SOURCES}


def find_errors(lines: list[str]) -> list[str]:
    errors = []
    patterns = get_error_patterns()
    for line in lines:
        for pat in patterns:
            if re.search(pat, line, re.IGNORECASE):
                errors.append(sanitize(line))
                break
    return errors


def summarize_errors(all_logs: dict[str, list[str]]) -> list[str]:
    summary = []
    for source, lines in all_logs.items():
        errors = find_errors(lines)
        if errors:
            summary.append(f"📂 {source}: {len(errors)} errors")
            error_types = Counter()
            for e in errors:
                for pat in get_error_patterns():
                    m = re.search(pat, e, re.IGNORECASE)
                    if m:
                        error_types[m.group().upper()] += 1
            for err_type, count in error_types.most_common(5):
                summary.append(f"  - {err_type}: {count}x")
            for e in errors[-3:]:
                summary.append(f"  └ {e[:120]}")
        else:
            summary.append(f"📂 {source}: ✅ no errors")
    return summary


def search_logs(pattern: str, lines: int = 200) -> list[str]:
    results = []
    for source in ALLOWED_SOURCES:
        logs = get_logs(source, lines)
        for line in logs:
            if re.search(pattern, line, re.IGNORECASE):
                results.append(sanitize(f"[{source}] {line}"))
    return results


def main():
    parser = argparse.ArgumentParser(description="Secure log analyzer")
    parser.add_argument("--source", "-s", choices=list(ALLOWED_SOURCES.keys()))
    parser.add_argument("--search", help="Search pattern (regex)")
    parser.add_argument("--last", "-n", type=int, default=100)
    parser.add_argument("--errors", "-e", action="store_true")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.search:
        results = search_logs(args.search, args.last)
        if args.json:
            print(json.dumps({"pattern": args.search, "matches": results}, indent=2))
        else:
            print(f"Search: {args.search} — {len(results)} matches")
            for r in results[:50]:
                print(r)
    elif args.summary or (not args.source and not args.errors):
        all_logs = get_all_logs(args.last)
        if args.json:
            errors = {s: find_errors(l) for s, l in all_logs.items()}
            print(json.dumps(errors, indent=2))
        else:
            for line in summarize_errors(all_logs):
                print(line)
    elif args.source:
        logs = get_logs(args.source, args.last)
        if args.errors:
            logs = find_errors(logs)
        if args.json:
            print(json.dumps({"source": args.source, "lines": [sanitize(l) for l in logs]}, indent=2))
        else:
            for line in logs:
                print(sanitize(line))
    elif args.errors:
        all_logs = get_all_logs(args.last)
        for source, lines in all_logs.items():
            errors = find_errors(lines)
            if errors:
                print(f"\n📂 {source}:")
                for e in errors:
                    print(f"  {e[:150]}")


if __name__ == "__main__":
    main()
