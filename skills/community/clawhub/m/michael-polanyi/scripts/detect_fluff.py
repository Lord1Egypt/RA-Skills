#!/usr/bin/env python3
"""Detect AI-generic patterns in text output.

Scans a file (or stdin) for phrases and structures that indicate
the response lacks practitioner judgment, per the Michael Polanyi skill.

Usage:
    python scripts/detect_fluff.py <file>
    cat response.txt | python scripts/detect_fluff.py -
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Pattern:
    category: str
    regex: str
    severity: str  # "warning" | "error"


PATTERNS: list[Pattern] = [
    # Empty balance / evasion
    Pattern("empty_balance", r"(?:这取决|取决于|需要综合考|建议根据实际|case by case|it depends)", "warning"),
    Pattern("empty_balance", r"(?:没有标准答案|case[- ]by[- ]case|视情况而定)", "warning"),

    # Abstract principles without grounding
    Pattern("abstract_principle", r"(?:持续优化|不断加强|加强沟通|明确目标|建立机制|提升能力)", "warning"),
    Pattern("abstract_principle", r"(?:continuously optimize|strengthen communication|clarify goals|establish mechanisms)", "warning"),

    # AI connectives (Chinese)
    Pattern("ai_connective", r"(?:总之|综上所述|一方面.*另一方面|值得注意的是|需要注意的是|重要的是|总而言之)", "warning"),

    # AI connectives (English)
    Pattern("ai_connective", r"(?:in conclusion|it's important to note|on the other hand|it is worth noting|more importantly|crucially)", "warning"),

    # Pseudo-depth / mysticism
    Pattern("pseudo_depth", r"(?:只可意会|难以言表|需要慢慢体会|cannot be explained|can only be felt|must be experienced)", "error"),

    # Timid judgment
    Pattern("timid_judgment", r"(?:可能也许|或许大概.*建议|not sure|might want to consider|could potentially)", "warning"),

    # Decorative warmth without substance
    Pattern("decorative_warmth", r"(?:这是一个很好的问题|很好的思考|great question.*worth exploring)", "warning"),

    # Confidence without grounds
    Pattern("unsubstantiated", r"(?:相信你们一定|一定能|I'm confident.*will definitely|rest assured)", "warning"),
]


@dataclass
class Match:
    line_number: int
    category: str
    matched_text: str
    severity: str


def lines_for_scan(source: str, text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()

    if Path(source).name != "examples.md":
        return list(enumerate(lines, start=1))

    selected: list[tuple[int, str]] = []
    in_practitioner_answer = False

    for line_num, line in enumerate(lines, start=1):
        if line.startswith("### Practitioner answer"):
            in_practitioner_answer = True
            continue

        if in_practitioner_answer and line.startswith("### "):
            in_practitioner_answer = False

        if in_practitioner_answer:
            selected.append((line_num, line))

    return selected or list(enumerate(lines, start=1))


def scan(source: str, text: str, patterns: list[Pattern]) -> list[Match]:
    results: list[Match] = []

    compiled = [(p, re.compile(p.regex, re.IGNORECASE)) for p in patterns]

    for line_num, line in lines_for_scan(source, text):
        for pattern, regex in compiled:
            if regex.search(line):
                # Get the matched substring
                m = regex.search(line)
                if m:
                    results.append(Match(
                        line_number=line_num,
                        category=pattern.category,
                        matched_text=m.group(0),
                        severity=pattern.severity,
                    ))

    return results


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        text = sys.stdin.read()
        source = "<stdin>"
    else:
        source = sys.argv[1]
        text = Path(source).read_text(encoding="utf-8")

    matches = scan(source, text, PATTERNS)

    report = {
        "source": source,
        "total_lines": len(text.splitlines()),
        "total_matches": len(matches),
        "errors": sum(1 for m in matches if m.severity == "error"),
        "warnings": sum(1 for m in matches if m.severity == "warning"),
        "matches": [
            {
                "line": m.line_number,
                "category": m.category,
                "text": m.matched_text,
                "severity": m.severity,
            }
            for m in matches
        ],
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))

    # Exit non-zero if errors found
    if report["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
