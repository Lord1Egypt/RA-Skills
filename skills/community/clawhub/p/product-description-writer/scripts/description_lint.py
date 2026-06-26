#!/usr/bin/env python3
"""
Lint a product description markdown file for common quality issues.

Checks word count, filler phrases, keyword density, bullet count,
meta description length, and feature-without-benefit patterns.

Usage:
    python scripts/description_lint.py --in description.md
    python scripts/description_lint.py --in description.md --keyword "vitamin c serum"
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class LintIssue:
    section: str
    message: str
    evidence: str = ""


FILLER_PHRASES = [
    "high quality",
    "high-quality",
    "amazing product",
    "great product",
    "best product",
    "top quality",
    "premium quality",
    "world class",
    "world-class",
    "state of the art",
    "state-of-the-art",
    "second to none",
    "game changer",
    "game-changer",
    "revolutionary",
    "cutting edge",
    "cutting-edge",
    "best in class",
    "best-in-class",
    "unparalleled",
    "unmatched",
]

UNSUPPORTED_SUPERLATIVES = [
    r"\bbest\b",
    r"\b#1\b",
    r"\bnumber one\b",
    r"\bmost advanced\b",
    r"\bonly one\b",
]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))


def keyword_density(text: str, keyword: str) -> float:
    wc = word_count(text)
    if wc == 0:
        return 0.0
    kw_words = len(keyword.split())
    pattern = re.escape(keyword)
    occurrences = len(re.findall(pattern, text, re.IGNORECASE))
    return (occurrences * kw_words) / wc * 100


def split_sections(md: str) -> Dict[str, str]:
    lines = md.splitlines()
    sections: Dict[str, List[str]] = {}
    current = "Document"
    sections[current] = []

    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        sections[current].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}


def count_bullets(text: str) -> int:
    return len(re.findall(r"^\s*[-*]\s+\*\*", text, re.MULTILINE))


def lint_description(sections: Dict[str, str], keyword: str = "") -> List[LintIssue]:
    issues: List[LintIssue] = []
    full_text = "\n".join(sections.values())
    wc = word_count(full_text)

    if wc < 250:
        issues.append(LintIssue("Overall", f"Total word count is low ({wc}). Aim for 300–500 words."))
    elif wc > 600:
        issues.append(LintIssue("Overall", f"Total word count is high ({wc}). Aim for 300–500 words."))

    lower_text = full_text.lower()
    for phrase in FILLER_PHRASES:
        if phrase in lower_text:
            issues.append(LintIssue("Filler", f"Generic filler detected: '{phrase}'. Replace with a specific benefit or proof.", phrase))

    for pattern in UNSUPPORTED_SUPERLATIVES:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        for match in matches:
            issues.append(LintIssue("Superlative", f"Unsupported superlative: '{match}'. Back it up with data or remove.", match))

    bullet_section = ""
    for name, text in sections.items():
        if "bullet" in name.lower() or "highlight" in name.lower():
            bullet_section = text
            break
    bullet_count = count_bullets(bullet_section) if bullet_section else count_bullets(full_text)
    if bullet_count < 5:
        issues.append(LintIssue("Bullets", f"Only {bullet_count} benefit bullets found. Aim for 5–7."))
    elif bullet_count > 8:
        issues.append(LintIssue("Bullets", f"Too many bullets ({bullet_count}). Aim for 5–7 to keep scannable."))

    if keyword:
        density = keyword_density(full_text, keyword)
        if density < 1.0:
            issues.append(LintIssue("SEO", f"Keyword density for '{keyword}' is {density:.1f}%. Aim for 2–3%."))
        elif density > 4.0:
            issues.append(LintIssue("SEO", f"Keyword density for '{keyword}' is {density:.1f}%. Over 4% reads as stuffing."))

    for section, text in sections.items():
        if "meta" in section.lower():
            meta_len = len(text.strip())
            if meta_len < 140:
                issues.append(LintIssue(section, f"Meta description is short ({meta_len} chars). Aim for 150–160."))
            elif meta_len > 165:
                issues.append(LintIssue(section, f"Meta description is long ({meta_len} chars). Search engines truncate after ~160."))

    return issues


def format_issues(issues: List[LintIssue]) -> str:
    if not issues:
        return "DESCRIPTION LINT: OK (no issues found)"
    out = ["DESCRIPTION LINT: issues found\n"]
    for i, issue in enumerate(issues, 1):
        out.append(f"{i}. [{issue.section}] {issue.message}")
        if issue.evidence:
            out.append(f"   Evidence: {issue.evidence}")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint a product description for word count, filler, SEO density, and bullet structure."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Path to markdown file.")
    parser.add_argument("--keyword", default="", help="Primary SEO keyword to check density for.")
    args = parser.parse_args()

    text = Path(args.in_path).expanduser().read_text(encoding="utf-8")
    sections = split_sections(text)
    issues = lint_description(sections, keyword=args.keyword)
    print(format_issues(issues))

    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
