"""
log_analyzer.py — Parse and summarize log files.

Supports two log formats out of the box:
- Python logging: `2026-01-15 10:30:45,123 - logger_name - LEVEL - message`
- JSON-lines: `{"level": "ERROR", "message": "...", "timestamp": "..."}`

For custom formats, subclass LogAnalyzer and override `_parse()`.
"""
from __future__ import annotations

import glob
import json
import re
from collections import Counter
from typing import Any


class LogAnalyzer:
    """Analyze log files for level distribution, error patterns, and timing."""

    # Order matters: first match wins. Standard Python logging format is
    # very common, so it goes first.
    PATTERNS: dict[str, str] = {
        "python": r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?)\s+-?\s*([\w.]+)\s+-\s+(\w+)\s+-\s+(.+)",
        "standard": r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.+)",
        "syslog": r"(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+(\w+):\s+(.+)",
    }

    ERROR_LEVELS = {"ERROR", "CRITICAL", "FATAL", "SEVERE"}

    def __init__(self):
        self.entries: list[dict] = []
        self._unparsed: list[str] = []

    def load(self, path: str) -> int:
        """Load log entries from a file or glob pattern. Returns count."""
        for filepath in sorted(glob.glob(path)):
            with open(filepath, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    line = line.rstrip()
                    if not line:
                        continue
                    entry = self._parse(line)
                    if entry:
                        self.entries.append(entry)
                    else:
                        self._unparsed.append(line)
        return len(self.entries)

    def _parse(self, line: str) -> dict | None:
        """Parse a single line. Returns None if no pattern matches."""
        # JSON-lines first
        if line.startswith("{"):
            try:
                d = json.loads(line)
                return {
                    "timestamp": d.get("timestamp") or d.get("ts") or d.get("@timestamp"),
                    "logger": d.get("logger") or d.get("name"),
                    "level": (d.get("level") or d.get("severity") or "INFO").upper(),
                    "message": d.get("message") or d.get("msg") or "",
                    "extra": {k: v for k, v in d.items()
                              if k not in {"timestamp", "ts", "@timestamp", "logger", "name",
                                            "level", "severity", "message", "msg"}},
                }
            except json.JSONDecodeError:
                pass

        for pattern_name, pattern in self.PATTERNS.items():
            m = re.match(pattern, line)
            if m:
                if pattern_name == "python":
                    return {"timestamp": m.group(1), "logger": m.group(2),
                            "level": m.group(3).upper(), "message": m.group(4)}
                elif pattern_name == "standard":
                    return {"timestamp": m.group(1), "logger": None,
                            "level": m.group(2).upper(), "message": m.group(3)}
                elif pattern_name == "syslog":
                    return {"timestamp": m.group(1), "logger": m.group(2),
                            "level": m.group(3).upper(), "message": m.group(4)}

        # Last resort: look for a level keyword anywhere
        level_match = re.search(r"\b(DEBUG|INFO|WARNING|WARN|ERROR|CRITICAL|FATAL)\b", line)
        if level_match:
            return {"timestamp": None, "logger": None,
                    "level": level_match.group(1).upper(), "message": line}

        return None

    def get_errors(self) -> list[dict]:
        """Return only entries with error-or-worse level."""
        return [e for e in self.entries if e["level"] in self.ERROR_LEVELS]

    def get_by_level(self, level: str) -> list[dict]:
        """Filter entries by level (case-insensitive)."""
        level = level.upper()
        return [e for e in self.entries if e["level"] == level]

    def error_patterns(self, top_n: int = 10) -> list[tuple[str, int]]:
        """Find the most common error messages (with numbers stripped)."""
        errors = self.get_errors()
        # Normalize messages by replacing numbers with # for grouping
        normalized = [re.sub(r"\d+", "#", e["message"]) for e in errors]
        return Counter(normalized).most_common(top_n)

    def time_window(self, start: str | None = None, end: str | None = None) -> list[dict]:
        """Filter entries to a time window. Strings are compared lexically
        (works for ISO 8601 timestamps)."""
        result = []
        for e in self.entries:
            ts = e.get("timestamp")
            if not ts:
                continue
            if start and ts < start:
                continue
            if end and ts > end:
                continue
            result.append(e)
        return result

    def summarize(self) -> dict[str, Any]:
        """Return a summary dict: total, by_level, errors, top patterns."""
        return {
            "total": len(self.entries),
            "unparsed": len(self._unparsed),
            "by_level": dict(Counter(e["level"] for e in self.entries)),
            "errors": len(self.get_errors()),
            "top_error_patterns": self.error_patterns(5),
            "time_range": self._time_range(),
        }

    def _time_range(self) -> dict | None:
        timestamps = [e["timestamp"] for e in self.entries if e.get("timestamp")]
        if not timestamps:
            return None
        return {"start": min(timestamps), "end": max(timestamps)}


def analyze_logs(path: str) -> dict[str, Any]:
    """One-shot: load and summarize logs at `path` (file or glob)."""
    analyzer = LogAnalyzer()
    analyzer.load(path)
    return analyzer.summarize()


__all__ = ["LogAnalyzer", "analyze_logs"]
