#!/usr/bin/env python3
"""
Landing page HTML auditor for opc-landing-page-manager.

Performs structural quality checks on generated HTML landing pages.
Catches common issues: missing meta tags, leftover placeholders, accessibility
gaps, and compliance requirements.

Usage:
    python3 page_audit.py FILE.html
    python3 page_audit.py FILE.html --json
    python3 page_audit.py FILE.html --compliance
    python3 page_audit.py --dir [pages_dir]

Options:
    FILE.html       Path to HTML file to audit
    --json          Output as JSON instead of human-readable
    --compliance    Also check compliance rules (privacy, terms)
    --dir           Audit all index.html files in a landing-pages directory
    pages_dir       Path to landing-pages directory (default: ./landing-pages)

Exit codes:
    0   All checks pass
    1   One or more checks failed

Dependencies: Python 3.8+ stdlib only
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


def read_html(file_path: Path) -> str:
    """Read an HTML file and return its contents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def check_title_tag(html: str) -> dict:
    """Check that <title> exists and is not empty or a placeholder."""
    match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if not match:
        return {"check": "title_tag", "status": "fail",
                "detail": "No <title> tag found"}
    title = match.group(1).strip()
    if not title:
        return {"check": "title_tag", "status": "fail",
                "detail": "Empty <title> tag"}
    if '{{' in title:
        return {"check": "title_tag", "status": "fail",
                "detail": f"Title contains placeholder: '{title}'"}
    return {"check": "title_tag", "status": "pass",
            "detail": f"Title: '{title}'"}


def check_meta_description(html: str) -> dict:
    """Check that meta description exists with non-empty content."""
    match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html, re.IGNORECASE
    )
    if not match:
        # Try alternate attribute order
        match = re.search(
            r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']',
            html, re.IGNORECASE
        )
    if not match:
        return {"check": "meta_description", "status": "fail",
                "detail": "No <meta name=\"description\"> tag found"}
    content = match.group(1).strip()
    if not content:
        return {"check": "meta_description", "status": "fail",
                "detail": "Empty meta description"}
    if '{{' in content:
        return {"check": "meta_description", "status": "fail",
                "detail": f"Meta description contains placeholder: '{content}'"}
    return {"check": "meta_description", "status": "pass",
            "detail": f"Description: '{content[:80]}...' ({len(content)} chars)"
            if len(content) > 80 else f"Description: '{content}' ({len(content)} chars)"}


def check_og_tags(html: str) -> dict:
    """Check that og:title and og:description are present."""
    og_title = re.search(
        r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']',
        html, re.IGNORECASE
    )
    og_desc = re.search(
        r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']',
        html, re.IGNORECASE
    )
    missing = []
    if not og_title:
        missing.append("og:title")
    elif '{{' in og_title.group(1):
        missing.append("og:title (placeholder)")
    if not og_desc:
        missing.append("og:description")
    elif '{{' in og_desc.group(1):
        missing.append("og:description (placeholder)")

    if missing:
        return {"check": "og_tags", "status": "fail",
                "detail": f"Missing: {', '.join(missing)}"}
    return {"check": "og_tags", "status": "pass",
            "detail": "og:title and og:description present"}


def check_placeholder_tokens(html: str) -> dict:
    """Scan for remaining {{...}} placeholder tokens."""
    # Exclude tokens inside HTML comments
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    tokens = re.findall(r'\{\{[^}]+\}\}', uncommented)
    if tokens:
        unique = sorted(set(tokens))
        return {"check": "placeholder_tokens", "status": "fail",
                "detail": f"Found {len(tokens)} remaining: {', '.join(unique[:10])}"
                + (f" (and {len(unique) - 10} more)" if len(unique) > 10 else "")}
    return {"check": "placeholder_tokens", "status": "pass",
            "detail": "No placeholder tokens remaining"}


def check_img_alt(html: str) -> dict:
    """Check that all <img> tags have non-empty alt attributes."""
    # Exclude commented sections
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    imgs = re.findall(r'<img\s[^>]*?>', uncommented, re.IGNORECASE)
    if not imgs:
        return {"check": "img_alt", "status": "pass",
                "detail": "No <img> tags found"}
    missing = []
    for img in imgs:
        has_alt = re.search(r'\balt=["\']([^"\']*)["\']', img, re.IGNORECASE)
        has_presentation = re.search(r'\brole=["\']presentation["\']', img, re.IGNORECASE)
        if has_presentation:
            continue
        if not has_alt or not has_alt.group(1).strip():
            src_match = re.search(r'\bsrc=["\']([^"\']*)["\']', img, re.IGNORECASE)
            src = src_match.group(1) if src_match else "unknown"
            missing.append(src)
    if missing:
        return {"check": "img_alt", "status": "fail",
                "detail": f"{len(missing)} image(s) missing alt text: {', '.join(missing[:5])}"}
    return {"check": "img_alt", "status": "pass",
            "detail": f"All {len(imgs)} images have alt text"}


def check_skip_nav(html: str) -> dict:
    """Check for a skip-navigation link."""
    # Look for common skip-nav patterns
    has_skip = re.search(
        r'<a\s[^>]*href=["\']#main["\'][^>]*>',
        html, re.IGNORECASE
    )
    if not has_skip:
        has_skip = re.search(
            r'<a\s[^>]*class=["\'][^"\']*skip[^"\']*["\'][^>]*>',
            html, re.IGNORECASE
        )
    if has_skip:
        return {"check": "skip_nav", "status": "pass",
                "detail": "Skip navigation link found"}
    return {"check": "skip_nav", "status": "fail",
            "detail": "No skip-navigation link found (expected <a href=\"#main\">)"}


def check_anchor_targets(html: str) -> dict:
    """Check that internal anchor links point to existing IDs."""
    # Exclude commented sections
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # Find internal anchor links
    anchors = re.findall(r'href=["\']#([a-zA-Z][a-zA-Z0-9_-]*)["\']', uncommented)
    if not anchors:
        return {"check": "anchor_targets", "status": "pass",
                "detail": "No internal anchor links found"}
    # Find all IDs
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', uncommented))
    missing = [a for a in anchors if a not in ids]
    if missing:
        unique_missing = sorted(set(missing))
        return {"check": "anchor_targets", "status": "fail",
                "detail": f"Broken anchors: {', '.join(unique_missing)}"}
    return {"check": "anchor_targets", "status": "pass",
            "detail": f"All {len(set(anchors))} anchor targets exist"}


def check_primary_cta_count(html: str) -> dict:
    """Count primary CTA elements — warn if more than 3."""
    # Exclude commented sections
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    primary_ctas = re.findall(r'class=["\'][^"\']*\bbtn-primary\b[^"\']*["\']', uncommented)
    count = len(primary_ctas)
    if count > 3:
        return {"check": "primary_cta_count", "status": "warn",
                "detail": f"{count} primary CTAs found (recommended: 3 or fewer)"}
    return {"check": "primary_cta_count", "status": "pass",
            "detail": f"{count} primary CTA(s) found"}


def check_css_tokens(html: str) -> dict:
    """Check that :root CSS custom properties include essential tokens."""
    style_match = re.search(r'<style[^>]*>(.*?)</style>', html, re.DOTALL | re.IGNORECASE)
    if not style_match:
        return {"check": "css_tokens", "status": "fail",
                "detail": "No <style> block found"}
    style = style_match.group(1)
    required = ['--primary', '--accent', '--bg', '--text']
    missing = [t for t in required if t + ':' not in style and t + ' :' not in style]
    if missing:
        return {"check": "css_tokens", "status": "fail",
                "detail": f"Missing CSS tokens: {', '.join(missing)}"}
    return {"check": "css_tokens", "status": "pass",
            "detail": "All required CSS tokens present (--primary, --accent, --bg, --text)"}


def check_section_count(html: str) -> dict:
    """Count <section> elements, warn if too few or too many."""
    # Exclude commented sections
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    sections = re.findall(r'<section\b', uncommented, re.IGNORECASE)
    count = len(sections)
    if count < 3:
        return {"check": "section_count", "status": "warn",
                "detail": f"Only {count} <section> elements (expected 3+)"}
    if count > 15:
        return {"check": "section_count", "status": "warn",
                "detail": f"{count} <section> elements (expected 15 or fewer)"}
    return {"check": "section_count", "status": "pass",
            "detail": f"{count} sections found"}


def check_compliance_privacy(html: str) -> dict:
    """Check if page collects data and has privacy policy link."""
    # Exclude commented sections
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    has_form = bool(re.search(r'<form\b', uncommented, re.IGNORECASE))
    has_email_input = bool(re.search(
        r'<input\s[^>]*type=["\']email["\']', uncommented, re.IGNORECASE
    ))
    if not has_form and not has_email_input:
        return {"check": "compliance_privacy", "status": "pass",
                "detail": "No data collection forms found"}
    # Check for privacy policy link (not commented out)
    has_privacy = bool(re.search(
        r'<a\s[^>]*href=["\'][^"\']*privacy[^"\']*["\']',
        uncommented, re.IGNORECASE
    ))
    if has_privacy:
        return {"check": "compliance_privacy", "status": "pass",
                "detail": "Data collection present, privacy policy link found"}
    return {"check": "compliance_privacy", "status": "fail",
            "detail": "Privacy policy link required (page collects user data via form)"}


def check_compliance_terms(html: str) -> dict:
    """Check if page involves payment and has terms link."""
    # Exclude commented sections
    uncommented = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    purchase_patterns = [
        r'\bbuy\b', r'\bpurchase\b', r'\bsubscribe\b',
        r'\border\s+now\b', r'\bcheckout\b',
        r'\bpayment\b', r'\bpricing\b'
    ]
    has_purchase = any(
        re.search(p, uncommented, re.IGNORECASE) for p in purchase_patterns
    )
    if not has_purchase:
        return {"check": "compliance_terms", "status": "pass",
                "detail": "No purchase/payment CTAs detected"}
    has_terms = bool(re.search(
        r'<a\s[^>]*href=["\'][^"\']*terms[^"\']*["\']',
        uncommented, re.IGNORECASE
    ))
    if has_terms:
        return {"check": "compliance_terms", "status": "pass",
                "detail": "Purchase CTAs present, terms of service link found"}
    return {"check": "compliance_terms", "status": "fail",
            "detail": "Terms of service link required (page involves payment/purchase)"}


def audit_file(file_path: Path, compliance: bool = False) -> dict:
    """Run all checks on an HTML file."""
    html = read_html(file_path)

    checks = [
        check_title_tag(html),
        check_meta_description(html),
        check_og_tags(html),
        check_placeholder_tokens(html),
        check_img_alt(html),
        check_skip_nav(html),
        check_anchor_targets(html),
        check_primary_cta_count(html),
        check_css_tokens(html),
        check_section_count(html),
    ]

    compliance_blockers = []
    if compliance:
        privacy_check = check_compliance_privacy(html)
        terms_check = check_compliance_terms(html)
        checks.append(privacy_check)
        checks.append(terms_check)
        if privacy_check["status"] == "fail":
            compliance_blockers.append(privacy_check["detail"])
        if terms_check["status"] == "fail":
            compliance_blockers.append(terms_check["detail"])

    passed = sum(1 for c in checks if c["status"] == "pass")
    failed = sum(1 for c in checks if c["status"] == "fail")
    warnings = sum(1 for c in checks if c["status"] == "warn")

    # Compute a simple readiness score
    total = len(checks)
    readiness = int((passed / total) * 100) if total > 0 else 0

    result = {
        "file": str(file_path),
        "audited_at": date.today().isoformat(),
        "checks": checks,
        "passed": passed,
        "failed": failed,
        "warnings": warnings,
        "readiness_score": readiness,
    }
    if compliance:
        result["compliance_blockers"] = compliance_blockers

    return result


def format_audit_human(result: dict) -> str:
    """Format audit results for human reading."""
    lines = []
    lines.append(f"AUDIT: {result['file']}")
    lines.append(f"Date: {result['audited_at']}")
    lines.append("")

    status_icons = {"pass": "PASS", "fail": "FAIL", "warn": "WARN"}
    for check in result["checks"]:
        icon = status_icons.get(check["status"], "????")
        lines.append(f"  [{icon}] {check['check']:25s}  {check['detail']}")

    lines.append("")
    lines.append(
        f"Results: {result['passed']} passed, {result['failed']} failed, "
        f"{result['warnings']} warnings"
    )
    lines.append(f"Readiness: {result['readiness_score']}%")

    if result.get("compliance_blockers"):
        lines.append("")
        lines.append("Compliance Blockers:")
        for b in result["compliance_blockers"]:
            lines.append(f"  - {b}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Landing page HTML auditor."
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='HTML file to audit'
    )
    parser.add_argument(
        '--dir',
        nargs='?',
        const='./landing-pages',
        help='Audit all index.html files in a landing-pages directory'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--compliance',
        action='store_true',
        help='Also check compliance rules (privacy, terms)'
    )

    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    results = []

    if args.dir:
        pages_dir = Path(args.dir)
        if not pages_dir.is_dir():
            msg = f"Directory not found: {pages_dir}"
            if args.json:
                print(json.dumps({"error": msg}))
            else:
                print(msg, file=sys.stderr)
            sys.exit(1)

        for html_file in sorted(pages_dir.rglob('index.html')):
            try:
                results.append(audit_file(html_file, args.compliance))
            except Exception as e:
                print(f"Warning: Could not audit {html_file}: {e}",
                      file=sys.stderr)

        if not results:
            if args.json:
                print(json.dumps({"message": "No index.html files found"}))
            else:
                print("No index.html files found in " + str(pages_dir))
            sys.exit(0)

    elif args.file:
        file_path = Path(args.file)
        if not file_path.is_file():
            msg = f"File not found: {file_path}"
            if args.json:
                print(json.dumps({"error": msg}))
            else:
                print(msg, file=sys.stderr)
            sys.exit(1)

        try:
            results.append(audit_file(file_path, args.compliance))
        except Exception as e:
            if args.json:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Output
    if args.json:
        output = results if len(results) > 1 else results[0]
        print(json.dumps(output, indent=2))
    else:
        for i, result in enumerate(results):
            if i > 0:
                print("\n" + "=" * 60 + "\n")
            print(format_audit_human(result))

    # Exit code: 1 if any failures
    has_failures = any(r["failed"] > 0 for r in results)
    sys.exit(1 if has_failures else 0)


if __name__ == '__main__':
    main()
