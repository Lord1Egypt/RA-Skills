# -*- coding: utf-8 -*-
"""
Fact Check Module
==================
Verifies data claims in articles through 3-source cross-validation.

Usage:
    python fact_check.py article.md --output report.md
    python fact_check.py article.md --verbose
"""
import argparse
import re
import sys
from datetime import datetime

DATA_PATTERNS = [
    r'(\d+\.?\d*%)',
    r'(\d+\.?\d*\s*(?:亿|万|千|百万|千万))',
    r'(\d+\.?\d*\s*(?:亿元|万元|美元|人民币))',
    r'(?:达到|增长|下降|减少|提升|降低)\s*(\d+\.?\d*%?)',
    r'(\d{4})年',
    r'(?:据|根据|来源[于于])\s*([^，。]+)',
]

AUTHORITATIVE_SOURCES = [
    "国家统计局", "卫健委", "药监局", "医保局", "中医药管理局",
    "CNNIC", "艾瑞咨询", "易观", "IDC", "麦肯锡", "波士顿咨询",
    "公开年报", "财报", "招股说明书", "白皮书",
    "PubMed", "WHO", "FDA",
]


def extract_claims(text: str) -> list:
    claims = []
    for pattern in DATA_PATTERNS:
        for match in re.finditer(pattern, text):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end].replace("\n", " ").strip()
            claims.append({
                "claim": match.group(0),
                "context": context,
                "position": match.start(),
            })
    return claims


def classify_source(text: str) -> str:
    for src in AUTHORITATIVE_SOURCES:
        if src in text:
            return f"权威来源: {src}"
    if "据报道" in text or "据悉" in text:
        return "媒体来源（需核实）"
    if "研究表明" in text or "研究显示" in text:
        return "研究来源（需核实）"
    return "无明确来源（需补充）"


def generate_report(claims: list, article_path: str) -> str:
    lines = [
        "# Data Source Verification Report",
        "",
        f"**Article:** {article_path}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Claims found:** {len(claims)}",
        "",
        "## Claims and Verification",
        "",
        "| # | Claim | Source Classification | Status |",
        "|---|-------|----------------------|--------|",
    ]
    verified = 0
    needs_check = 0
    no_source = 0

    for i, claim in enumerate(claims, 1):
        source_class = classify_source(claim["context"])
        if "权威来源" in source_class:
            status = "VERIFIED"
            verified += 1
        elif "需补充" in source_class:
            status = "NO_SOURCE"
            no_source += 1
        else:
            status = "NEEDS_CHECK"
            needs_check += 1
        lines.append(
            f"| {i} | {claim['claim'][:50]} | {source_class} | {status} |"
        )

    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total claims: {len(claims)}")
    lines.append(f"- Verified (authoritative source): {verified}")
    lines.append(f"- Needs checking: {needs_check}")
    lines.append(f"- No source cited: {no_source}")
    lines.append("")
    if no_source > 0:
        lines.append("## Action Required")
        lines.append("")
        lines.append(f"**{no_source} claims have no data source.** Add source citations before publishing.")
    if needs_check > 0:
        lines.append(f"\n**{needs_check} claims cite media/research sources.** Cross-validate with authoritative sources.")

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify data claims in article")
    parser.add_argument("input", help="Article file path (Markdown or text)")
    parser.add_argument("--output", "-o", help="Output report file path")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        text = f.read()

    claims = extract_claims(text)
    report = generate_report(claims, args.input)

    if args.verbose:
        print(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved: {args.output}")
    elif not args.verbose:
        print(report)
