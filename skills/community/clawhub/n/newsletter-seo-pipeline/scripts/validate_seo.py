#!/usr/bin/env python3
"""
validate_seo.py — SEO validation for newsletter-seo-pipeline
Checks meta title, meta description, H1 count, keyword presence.

Usage:
    python3 validate_seo.py <article_file> <primary_keyword>

Exit codes:
    0 = all checks passed
    1 = one or more issues found
"""

import sys
import re

def validate(filepath, keyword):
    with open(filepath, 'r') as f:
        content = f.read()

    issues = []
    warnings = []

    # --- Meta title ---
    meta_title_match = re.search(r'(?i)^meta[_\s-]?title:\s*(.+)$', content, re.MULTILINE)
    if meta_title_match:
        title = meta_title_match.group(1).strip().strip('"\'')
        tlen = len(title)
        if tlen < 50:
            warnings.append(f"Meta title short: {tlen} chars (aim 50–60)")
        elif tlen > 60:
            issues.append(f"Meta title too long: {tlen} chars (max 60)")
        kw_lower = keyword.lower()
        if kw_lower not in title.lower():
            issues.append(f"Meta title missing primary keyword: '{keyword}'")
    else:
        issues.append("Meta title not found (expected 'Meta Title: ...' line)")

    # --- Meta description ---
    meta_desc_match = re.search(r'(?i)^meta[_\s-]?description:\s*(.+)$', content, re.MULTILINE)
    if meta_desc_match:
        desc = meta_desc_match.group(1).strip().strip('"\'')
        dlen = len(desc)
        if dlen < 150:
            warnings.append(f"Meta description short: {dlen} chars (aim 150–160)")
        elif dlen > 160:
            issues.append(f"Meta description too long: {dlen} chars (max 160)")
        if keyword.lower() not in desc.lower():
            warnings.append(f"Meta description missing primary keyword: '{keyword}'")
    else:
        issues.append("Meta description not found (expected 'Meta Description: ...' line)")

    # --- H1 count ---
    h1s = re.findall(r'^# .+', content, re.MULTILINE)
    if len(h1s) == 0:
        issues.append("No H1 found (expected exactly 1)")
    elif len(h1s) > 1:
        issues.append(f"Multiple H1s found: {len(h1s)} (expected exactly 1)")

    # --- Keyword in first 100 words ---
    body_start = re.search(r'^# .+', content, re.MULTILINE)
    if body_start:
        body = content[body_start.start():]
        first_100 = ' '.join(body.split()[:100])
        if keyword.lower() not in first_100.lower():
            warnings.append(f"Primary keyword '{keyword}' not in first 100 words")

    # --- H2s present ---
    h2s = re.findall(r'^## .+', content, re.MULTILINE)
    if len(h2s) < 2:
        warnings.append(f"Only {len(h2s)} H2 section(s) found — aim for 3+")

    # --- Output ---
    print("\n=== SEO Validation Report ===")
    if issues:
        print("\n❌ ISSUES (must fix):")
        for i in issues:
            print(f"  • {i}")
    if warnings:
        print("\n⚠️  WARNINGS (should fix):")
        for w in warnings:
            print(f"  • {w}")
    if not issues and not warnings:
        print("\n✅ All SEO checks passed.")
    elif not issues:
        print("\n✅ No blocking issues. Fix warnings before publishing.")

    print()
    return len(issues)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 validate_seo.py <article_file> <primary_keyword>")
        sys.exit(1)
    exit_code = validate(sys.argv[1], ' '.join(sys.argv[2:]))
    sys.exit(exit_code)
