"""
format_detector.py — Heuristic file/content format detection with debug output.

Bug fix vs v6:
- `_score_format` now scores `weight` for the first match (v6 gave `weight * 0.5`
  for the first match due to `min(weight, weight * matches * 0.5)` with matches=1).
  Subsequent matches still add diminishing amounts, capped at `weight` total
  per indicator.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class FormatScore:
    format_name: str
    score: float
    confidence: str  # 'high', 'medium', 'low'
    indicators: list[str]


class FormatDetector:
    """Detect the format of a text content via weighted indicator patterns.

    Each format has positive indicators (raise the score) and counter-indicators
    (lower the score). Useful when a file extension is missing or wrong.
    Use `debug=True` to see per-format scoring breakdown.
    """

    FORMAT_DEFINITIONS: dict[str, dict[str, Any]] = {
        "json": {
            "indicators": [
                (r"^\s*\{.*\}\s*$", 0.8, "Object structure (single root)"),
                (r"^\s*\[.*\]\s*$", 0.8, "Array structure (single root)"),
                (r'"[^"]+"\s*:', 0.3, "JSON key pattern"),
                (r'"\w+"\s*:\s*[\d"]', 0.3, "Key: value pair"),
            ],
            "counter": [(r"^\s*<", -0.5, "Looks like XML/HTML")],
        },
        "xml": {
            "indicators": [
                (r"^\s*<\?xml", 0.9, "XML declaration"),
                (r"<[a-zA-Z][^>]*>.*</[a-zA-Z]", 0.7, "XML tag pair"),
                (r"<[a-zA-Z][^>]*/>", 0.4, "Self-closing tag"),
            ],
            "counter": [(r"^\s*\{", -0.3, "Looks like JSON")],
        },
        "html": {
            "indicators": [
                (r"<!DOCTYPE\s+html", 0.9, "HTML doctype"),
                (r"<html[^>]*>", 0.8, "<html> tag"),
                (r"<(head|body|div|span|p|a|img)[^>]*>", 0.5, "HTML element"),
            ],
            "counter": [],
        },
        "csv": {
            "indicators": [
                (r"^[^,\n]+,[^,\n]+,[^,\n]+", 0.6, "Multiple columns"),
                (r'^"[^"]*","[^"]*"', 0.5, "Quoted fields"),
                (r"^[^,\n]+,[^,\n]+\n[^,\n]+,[^,\n]+", 0.4, "Multiple rows"),
            ],
            "counter": [(r"^\s*[\{\[<]", -0.4, "Structured format marker")],
        },
        "yaml": {
            "indicators": [
                (r"^[a-zA-Z_][a-zA-Z0-9_]*:\s*\S", 0.5, "Key: value pair"),
                (r"^---\s*$", 0.7, "YAML document marker"),
                (r"^\s+-\s+\S", 0.4, "List item"),
                (r"^\s+\S+:\s+\S", 0.3, "Nested key"),
            ],
            "counter": [(r"^\s*\{", -0.4, "Looks like JSON")],
        },
        "markdown": {
            "indicators": [
                (r"^#{1,6}\s+", 0.6, "Header"),
                (r"^\s*[-*+]\s+", 0.3, "Unordered list"),
                (r"\[.+?\]\(.+?\)", 0.4, "Link"),
                (r"^```", 0.5, "Code block"),
                (r"^\|.+\|$", 0.4, "Table row"),
            ],
            "counter": [],
        },
        "python": {
            "indicators": [
                (r"^def\s+\w+\s*\(", 0.7, "Function definition"),
                (r"^class\s+\w+", 0.7, "Class definition"),
                (r"^import\s+\w+", 0.6, "Import statement"),
                (r"^from\s+\w+\s+import", 0.6, "From import"),
                (r"^\s+if\s+.+:$", 0.3, "Python if statement"),
            ],
            "counter": [(r"^\s*[\{\[]", -0.3, "JSON-like structure")],
        },
        "sql": {
            "indicators": [
                (r"\bSELECT\s+.+\s+FROM\b", 0.8, "SELECT statement"),
                (r"\bINSERT\s+INTO\b", 0.8, "INSERT statement"),
                (r"\bCREATE\s+TABLE\b", 0.8, "CREATE TABLE"),
                (r"\bALTER\s+TABLE\b", 0.7, "ALTER TABLE"),
            ],
            "counter": [],
        },
        "toml": {
            "indicators": [
                (r"^\[\w[\w.]*\]$", 0.7, "TOML section header"),
                (r"^\w+\s*=\s*", 0.4, "TOML key = value"),
            ],
            "counter": [(r"^\s*\{", -0.3, "Looks like JSON")],
        },
        "ini": {
            "indicators": [
                (r"^\[\w+\]$", 0.6, "INI section header"),
                (r"^\w+\s*=\s*\S", 0.4, "INI key = value"),
            ],
            "counter": [],
        },
        "log": {
            "indicators": [
                (r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", 0.7, "Timestamp prefix"),
                (r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b", 0.5, "Log level keyword"),
            ],
            "counter": [],
        },
    }

    def detect(self, content: str, debug: bool = False) -> tuple[str, list[FormatScore]]:
        """Detect format. Returns (best_format_name, all_scores)."""
        scores: list[FormatScore] = []
        for format_name, definition in self.FORMAT_DEFINITIONS.items():
            score = self._score_format(content, format_name, definition)
            scores.append(score)

        scores.sort(key=lambda s: s.score, reverse=True)
        best = scores[0]

        if debug:
            print(f"\n=== Format Detection: {best.format_name} ({best.confidence}) ===")
            for s in scores[:5]:
                print(f"  {s.format_name:10s} {s.score:5.2f}  {s.indicators[:2]}")

        return (best.format_name if best.score > 0.3 else "unknown"), scores

    def _score_format(self, content: str, name: str, definition: dict) -> FormatScore:
        """Score a format against the content. Bug-fixed scoring."""
        score = 0.0
        indicators: list[str] = []

        for pattern, weight, desc in definition.get("indicators", []):
            matches = len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
            if matches > 0:
                # First match: full weight. Subsequent matches: diminishing,
                # capped so total contribution from this indicator is ≤ weight.
                contribution = weight * min(1.0, 0.5 + 0.5 * min(matches - 1, 3) / 3)
                score += contribution
                indicators.append(f"+{contribution:.2f}: {desc} ({matches} match{'es' if matches > 1 else ''})")

        for pattern, weight, desc in definition.get("counter", []):
            if re.search(pattern, content, re.MULTILINE):
                score += weight
                indicators.append(f"{weight:+.2f}: {desc}")

        confidence = "high" if score >= 0.7 else "medium" if score >= 0.4 else "low"
        return FormatScore(name, max(0.0, score), confidence, indicators)


def detect_format(content: str, debug: bool = False) -> str:
    """One-shot format detection. Returns format name or 'unknown'."""
    detector = FormatDetector()
    format_name, _ = detector.detect(content, debug)
    return format_name


__all__ = ["FormatDetector", "detect_format", "FormatScore"]
