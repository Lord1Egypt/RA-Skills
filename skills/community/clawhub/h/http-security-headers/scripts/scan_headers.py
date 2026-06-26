#!/usr/bin/env python3
"""HTTP Security Headers Analyzer — scan URLs for security header best practices.

Grade websites A-F based on 15 security header checks with OWASP-aligned recommendations.
Pure Python stdlib — no external dependencies.

Usage:
    python3 scan_headers.py <url> [<url2> ...]
    python3 scan_headers.py <url> --format json|markdown|text
    python3 scan_headers.py <url> --min-grade B
"""

import sys
import json
import argparse
import ssl
import re
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime, timezone

# ── Header definitions ──────────────────────────────────────────────────────

SECURITY_HEADERS = {
    "strict-transport-security": {
        "name": "Strict-Transport-Security",
        "impact": "critical",
        "weight": 15,
        "description": "Enforces HTTPS connections",
        "recommendation": "Add header: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload",
        "fixes": {
            "nginx": 'add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;',
            "apache": 'Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"',
            "cloudflare": "Enable HSTS in SSL/TLS > Edge Certificates > HTTP Strict Transport Security",
        },
    },
    "content-security-policy": {
        "name": "Content-Security-Policy",
        "impact": "critical",
        "weight": 15,
        "description": "Prevents XSS, clickjacking, and code injection",
        "recommendation": "Add a Content-Security-Policy header. Start with: default-src 'self'; script-src 'self'",
        "fixes": {
            "nginx": "add_header Content-Security-Policy \"default-src 'self'; script-src 'self'\" always;",
            "apache": "Header always set Content-Security-Policy \"default-src 'self'; script-src 'self'\"",
            "cloudflare": "Use Transform Rules > Response Header Modification to add CSP",
        },
    },
    "x-frame-options": {
        "name": "X-Frame-Options",
        "impact": "high",
        "weight": 10,
        "description": "Prevents clickjacking by controlling iframe embedding",
        "recommendation": "Add header: X-Frame-Options: DENY (or SAMEORIGIN if iframes needed)",
        "fixes": {
            "nginx": "add_header X-Frame-Options DENY always;",
            "apache": "Header always set X-Frame-Options DENY",
            "cloudflare": "Use Transform Rules to add X-Frame-Options: DENY",
        },
    },
    "x-content-type-options": {
        "name": "X-Content-Type-Options",
        "impact": "high",
        "weight": 10,
        "description": "Prevents MIME type sniffing attacks",
        "recommendation": "Add header: X-Content-Type-Options: nosniff",
        "fixes": {
            "nginx": "add_header X-Content-Type-Options nosniff always;",
            "apache": "Header always set X-Content-Type-Options nosniff",
            "cloudflare": "Automatically added by Cloudflare",
        },
    },
    "referrer-policy": {
        "name": "Referrer-Policy",
        "impact": "medium",
        "weight": 7,
        "description": "Controls referrer information sent with requests",
        "recommendation": "Add header: Referrer-Policy: strict-origin-when-cross-origin",
        "fixes": {
            "nginx": "add_header Referrer-Policy strict-origin-when-cross-origin always;",
            "apache": "Header always set Referrer-Policy strict-origin-when-cross-origin",
            "cloudflare": "Use Transform Rules to add Referrer-Policy",
        },
    },
    "permissions-policy": {
        "name": "Permissions-Policy",
        "impact": "medium",
        "weight": 7,
        "description": "Controls browser feature access (camera, mic, geolocation)",
        "recommendation": "Add header: Permissions-Policy: camera=(), microphone=(), geolocation=()",
        "fixes": {
            "nginx": 'add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;',
            "apache": 'Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"',
            "cloudflare": "Use Transform Rules to add Permissions-Policy",
        },
    },
    "x-xss-protection": {
        "name": "X-XSS-Protection",
        "impact": "low",
        "weight": 3,
        "description": "Legacy XSS filter (deprecated but still checked by some scanners)",
        "recommendation": "Add header: X-XSS-Protection: 0 (disable; rely on CSP instead)",
        "fixes": {
            "nginx": "add_header X-XSS-Protection 0 always;",
            "apache": "Header always set X-XSS-Protection 0",
            "cloudflare": "Use Transform Rules to add X-XSS-Protection: 0",
        },
    },
    "cross-origin-opener-policy": {
        "name": "Cross-Origin-Opener-Policy",
        "impact": "medium",
        "weight": 5,
        "description": "Isolates browsing context from cross-origin documents",
        "recommendation": "Add header: Cross-Origin-Opener-Policy: same-origin",
        "fixes": {
            "nginx": "add_header Cross-Origin-Opener-Policy same-origin always;",
            "apache": "Header always set Cross-Origin-Opener-Policy same-origin",
            "cloudflare": "Use Transform Rules to add COOP header",
        },
    },
    "cross-origin-resource-policy": {
        "name": "Cross-Origin-Resource-Policy",
        "impact": "medium",
        "weight": 5,
        "description": "Controls cross-origin resource sharing",
        "recommendation": "Add header: Cross-Origin-Resource-Policy: same-origin",
        "fixes": {
            "nginx": "add_header Cross-Origin-Resource-Policy same-origin always;",
            "apache": "Header always set Cross-Origin-Resource-Policy same-origin",
            "cloudflare": "Use Transform Rules to add CORP header",
        },
    },
    "cross-origin-embedder-policy": {
        "name": "Cross-Origin-Embedder-Policy",
        "impact": "medium",
        "weight": 5,
        "description": "Controls embedding of cross-origin resources",
        "recommendation": "Add header: Cross-Origin-Embedder-Policy: require-corp",
        "fixes": {
            "nginx": "add_header Cross-Origin-Embedder-Policy require-corp always;",
            "apache": "Header always set Cross-Origin-Embedder-Policy require-corp",
            "cloudflare": "Use Transform Rules to add COEP header",
        },
    },
    "cache-control": {
        "name": "Cache-Control",
        "impact": "medium",
        "weight": 5,
        "description": "Controls caching of sensitive data",
        "recommendation": "For sensitive pages: Cache-Control: no-store, no-cache, must-revalidate",
        "fixes": {
            "nginx": "add_header Cache-Control 'no-store, no-cache, must-revalidate' always;",
            "apache": 'Header always set Cache-Control "no-store, no-cache, must-revalidate"',
            "cloudflare": "Configure Cache Rules in Cloudflare dashboard",
        },
    },
    "x-permitted-cross-domain-policies": {
        "name": "X-Permitted-Cross-Domain-Policies",
        "impact": "low",
        "weight": 3,
        "description": "Controls Flash/PDF cross-domain access",
        "recommendation": "Add header: X-Permitted-Cross-Domain-Policies: none",
        "fixes": {
            "nginx": "add_header X-Permitted-Cross-Domain-Policies none always;",
            "apache": "Header always set X-Permitted-Cross-Domain-Policies none",
            "cloudflare": "Use Transform Rules to add this header",
        },
    },
    "x-dns-prefetch-control": {
        "name": "X-DNS-Prefetch-Control",
        "impact": "low",
        "weight": 2,
        "description": "Controls DNS prefetching behavior",
        "recommendation": "Add header: X-DNS-Prefetch-Control: off (for privacy-sensitive sites)",
        "fixes": {
            "nginx": "add_header X-DNS-Prefetch-Control off always;",
            "apache": "Header always set X-DNS-Prefetch-Control off",
            "cloudflare": "Use Transform Rules to add this header",
        },
    },
}

# Headers that indicate information disclosure (negative scoring)
DISCLOSURE_HEADERS = {
    "server": {"name": "Server", "penalty": 3, "description": "Reveals web server software/version"},
    "x-powered-by": {"name": "X-Powered-By", "penalty": 5, "description": "Reveals backend technology"},
    "x-aspnet-version": {"name": "X-AspNet-Version", "penalty": 5, "description": "Reveals ASP.NET version"},
    "x-aspnetmvc-version": {"name": "X-AspNetMvc-Version", "penalty": 5, "description": "Reveals ASP.NET MVC version"},
    "x-generator": {"name": "X-Generator", "penalty": 3, "description": "Reveals CMS/generator"},
}

GRADE_THRESHOLDS = [
    (100, "A+"), (90, "A"), (75, "B"), (60, "C"), (40, "D"), (0, "F"),
]

GRADE_EXIT_CODES = {"A+": 0, "A": 0, "B": 1, "C": 1, "D": 2, "F": 2}


# ── Scanning ────────────────────────────────────────────────────────────────

def fetch_headers(url, timeout=10):
    """Fetch HTTP response headers from a URL."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    ctx = ssl.create_default_context()
    req = Request(url, method="HEAD")
    req.add_header("User-Agent", "SecurityHeadersScanner/1.0")

    try:
        resp = urlopen(req, timeout=timeout, context=ctx)
        headers = {k.lower(): v for k, v in resp.getheaders()}
        return {
            "url": url,
            "status_code": resp.status,
            "headers": headers,
            "error": None,
        }
    except HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()}
        return {
            "url": url,
            "status_code": e.code,
            "headers": headers,
            "error": None,
        }
    except URLError as e:
        return {"url": url, "status_code": None, "headers": {}, "error": str(e.reason)}
    except Exception as e:
        return {"url": url, "status_code": None, "headers": {}, "error": str(e)}


def analyze_hsts(value):
    """Analyze HSTS header quality."""
    issues = []
    if not value:
        return 0, ["Missing"]

    parts = [p.strip().lower() for p in value.split(";")]
    max_age = None
    for p in parts:
        if p.startswith("max-age="):
            try:
                max_age = int(p.split("=")[1])
            except ValueError:
                issues.append("Invalid max-age value")

    if max_age is None:
        issues.append("Missing max-age directive")
        return 0.3, issues
    if max_age < 2592000:  # 30 days
        issues.append(f"max-age too short ({max_age}s, recommend >= 31536000)")
        score = 0.5
    elif max_age < 31536000:  # 1 year
        issues.append(f"max-age could be longer ({max_age}s, ideal: 31536000)")
        score = 0.8
    else:
        score = 1.0

    has_subdomains = any("includesubdomains" in p for p in parts)
    has_preload = any("preload" in p for p in parts)

    if not has_subdomains:
        issues.append("Missing includeSubDomains")
        score *= 0.9
    if not has_preload:
        issues.append("Missing preload directive")
        score *= 0.95

    return score, issues


def analyze_csp(value):
    """Analyze CSP header quality."""
    if not value:
        return 0, ["Missing"]

    issues = []
    score = 1.0

    directives = {}
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        tokens = part.split()
        if tokens:
            directives[tokens[0].lower()] = tokens[1:] if len(tokens) > 1 else []

    # Check for unsafe directives
    for directive, values in directives.items():
        for v in values:
            if v == "'unsafe-inline'" and directive in ("script-src", "style-src", "default-src"):
                issues.append(f"'unsafe-inline' in {directive} weakens XSS protection")
                score *= 0.7
            if v == "'unsafe-eval'" and directive in ("script-src", "default-src"):
                issues.append(f"'unsafe-eval' in {directive} allows eval()")
                score *= 0.7
            if v == "*":
                issues.append(f"Wildcard '*' in {directive} is too permissive")
                score *= 0.5

    if "default-src" not in directives:
        issues.append("Missing default-src fallback directive")
        score *= 0.8

    if "script-src" not in directives and "default-src" not in directives:
        issues.append("No script-src or default-src — scripts unrestricted")
        score *= 0.6

    if "object-src" not in directives:
        issues.append("Missing object-src (should be 'none' to prevent plugin abuse)")
        score *= 0.9

    if "base-uri" not in directives:
        issues.append("Missing base-uri (should be 'self' or 'none')")
        score *= 0.95

    if not issues:
        issues.append("Well configured")

    return max(score, 0.1), issues


def analyze_header(header_key, value):
    """Analyze a specific header's value quality. Returns (quality_score 0-1, issues)."""
    if header_key == "strict-transport-security":
        return analyze_hsts(value)
    if header_key == "content-security-policy":
        return analyze_csp(value)

    # For most headers, presence = good
    if value:
        # Check known-good values
        if header_key == "x-frame-options":
            v = value.upper()
            if v in ("DENY", "SAMEORIGIN"):
                return 1.0, ["Properly configured"]
            return 0.5, [f"Unusual value: {value}"]

        if header_key == "x-content-type-options":
            if value.lower() == "nosniff":
                return 1.0, ["Properly configured"]
            return 0.5, [f"Expected 'nosniff', got: {value}"]

        if header_key == "referrer-policy":
            good_values = {
                "no-referrer", "strict-origin", "strict-origin-when-cross-origin",
                "same-origin", "no-referrer-when-downgrade", "origin",
                "origin-when-cross-origin",
            }
            # Referrer-Policy can be comma-separated (fallback chain)
            policies = [v.strip().lower() for v in value.split(",")]
            if all(p in good_values for p in policies):
                return 1.0, ["Properly configured"]
            if "unsafe-url" in policies:
                return 0.3, ["'unsafe-url' sends full URL — privacy risk"]
            return 0.7, [f"Non-standard value: {value}"]

        if header_key == "x-xss-protection":
            if value.strip() == "0":
                return 1.0, ["Correctly disabled (rely on CSP)"]
            if "1" in value and "mode=block" in value:
                return 0.8, ["Legacy mode — consider setting to 0 with CSP"]
            return 0.6, [f"Unusual value: {value}"]

        return 1.0, ["Present"]

    return 0, ["Missing"]


def scan_url(url):
    """Scan a URL and return full analysis."""
    result = fetch_headers(url)

    if result["error"]:
        return {
            "url": result["url"],
            "error": result["error"],
            "grade": "F",
            "score": 0,
            "headers": {},
            "findings": [],
            "disclosure": [],
        }

    headers = result["headers"]
    findings = []
    total_weight = sum(h["weight"] for h in SECURITY_HEADERS.values())
    earned_score = 0

    for key, spec in SECURITY_HEADERS.items():
        value = headers.get(key, "")
        quality, issues = analyze_header(key, value)
        present = bool(value)
        earned = spec["weight"] * quality

        findings.append({
            "header": spec["name"],
            "impact": spec["impact"],
            "present": present,
            "value": value if present else None,
            "quality": round(quality, 2),
            "issues": issues,
            "recommendation": spec["recommendation"] if quality < 1.0 else None,
            "fixes": spec["fixes"] if not present else None,
            "points": round(earned, 1),
            "max_points": spec["weight"],
        })

        earned_score += earned

    # Check disclosure headers (penalties)
    disclosure = []
    penalty = 0
    for key, spec in DISCLOSURE_HEADERS.items():
        value = headers.get(key, "")
        if value:
            disclosure.append({
                "header": spec["name"],
                "value": value,
                "penalty": spec["penalty"],
                "description": spec["description"],
                "recommendation": f"Remove or suppress the {spec['name']} header",
            })
            penalty += spec["penalty"]

    # Calculate final score
    raw_score = (earned_score / total_weight) * 100 if total_weight > 0 else 0
    final_score = max(0, min(100, raw_score - penalty))

    # Determine grade
    grade = "F"
    for threshold, g in GRADE_THRESHOLDS:
        if final_score >= threshold:
            grade = g
            break

    return {
        "url": result["url"],
        "status_code": result["status_code"],
        "error": None,
        "grade": grade,
        "score": round(final_score, 1),
        "raw_score": round(raw_score, 1),
        "penalty": penalty,
        "findings": findings,
        "disclosure": disclosure,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
    }


# ── Formatters ──────────────────────────────────────────────────────────────

def format_text(results):
    """Format results as colored text."""
    lines = []

    for r in results:
        lines.append(f"\n{'='*60}")
        lines.append(f"  URL: {r['url']}")

        if r["error"]:
            lines.append(f"  ERROR: {r['error']}")
            lines.append(f"{'='*60}")
            continue

        lines.append(f"  Status: {r['status_code']}")
        lines.append(f"  Grade: {r['grade']} ({r['score']}/100)")
        if r["penalty"]:
            lines.append(f"  Penalty: -{r['penalty']} pts (information disclosure)")
        lines.append(f"{'='*60}")

        # Group by impact
        for impact in ["critical", "high", "medium", "low"]:
            impact_findings = [f for f in r["findings"] if f["impact"] == impact]
            if not impact_findings:
                continue

            lines.append(f"\n  [{impact.upper()}]")
            for f in impact_findings:
                status = "PASS" if f["present"] and f["quality"] >= 0.8 else "WARN" if f["present"] else "FAIL"
                icon = {"PASS": "+", "WARN": "~", "FAIL": "-"}[status]
                lines.append(f"  [{icon}] {f['header']} ({f['points']}/{f['max_points']} pts)")

                if f["issues"] and f["issues"] != ["Present"] and f["issues"] != ["Properly configured"]:
                    for issue in f["issues"]:
                        lines.append(f"      ! {issue}")

                if f["recommendation"]:
                    lines.append(f"      > {f['recommendation']}")

        if r["disclosure"]:
            lines.append(f"\n  [DISCLOSURE]")
            for d in r["disclosure"]:
                lines.append(f"  [-] {d['header']}: {d['value']} (-{d['penalty']} pts)")
                lines.append(f"      > {d['recommendation']}")

        # Summary
        present = sum(1 for f in r["findings"] if f["present"])
        total = len(r["findings"])
        critical_missing = [f for f in r["findings"]
                           if f["impact"] == "critical" and not f["present"]]

        lines.append(f"\n  Summary: {present}/{total} headers present")
        if critical_missing:
            names = ", ".join(f["header"] for f in critical_missing)
            lines.append(f"  CRITICAL MISSING: {names}")

    return "\n".join(lines)


def format_json(results):
    """Format results as JSON."""
    return json.dumps(results, indent=2)


def format_markdown(results):
    """Format results as Markdown report."""
    lines = ["# HTTP Security Headers Report", ""]
    lines.append(f"*Scanned: {results[0].get('scanned_at', 'N/A')}*")
    lines.append("")

    for r in results:
        lines.append(f"## {r['url']}")
        lines.append("")

        if r["error"]:
            lines.append(f"**Error:** {r['error']}")
            lines.append("")
            continue

        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Grade | **{r['grade']}** |")
        lines.append(f"| Score | {r['score']}/100 |")
        lines.append(f"| HTTP Status | {r['status_code']} |")
        if r["penalty"]:
            lines.append(f"| Disclosure Penalty | -{r['penalty']} pts |")
        lines.append("")

        lines.append("### Security Headers")
        lines.append("")
        lines.append("| Header | Status | Impact | Score |")
        lines.append("|--------|--------|--------|-------|")

        for f in r["findings"]:
            status = "PASS" if f["present"] and f["quality"] >= 0.8 else "WARN" if f["present"] else "MISSING"
            lines.append(f"| {f['header']} | {status} | {f['impact']} | {f['points']}/{f['max_points']} |")

        lines.append("")

        # Recommendations
        recs = [f for f in r["findings"] if f["recommendation"]]
        if recs:
            lines.append("### Recommendations")
            lines.append("")
            for f in recs:
                lines.append(f"- **{f['header']}**: {f['recommendation']}")
                if f["fixes"]:
                    lines.append(f"  - Nginx: `{f['fixes']['nginx']}`")
                    lines.append(f"  - Apache: `{f['fixes']['apache']}`")
            lines.append("")

        if r["disclosure"]:
            lines.append("### Information Disclosure")
            lines.append("")
            for d in r["disclosure"]:
                lines.append(f"- **{d['header']}**: `{d['value']}` (-{d['penalty']} pts) — {d['recommendation']}")
            lines.append("")

    return "\n".join(lines)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="HTTP Security Headers Analyzer — grade websites A-F on security header configuration"
    )
    parser.add_argument("urls", nargs="+", help="URL(s) to scan")
    parser.add_argument("--format", "-f", choices=["text", "json", "markdown"],
                       default="text", help="Output format (default: text)")
    parser.add_argument("--min-grade", "-g", choices=["A+", "A", "B", "C", "D"],
                       default=None, help="Minimum passing grade for CI (exit 2 if below)")
    parser.add_argument("--timeout", "-t", type=int, default=10,
                       help="Request timeout in seconds (default: 10)")

    args = parser.parse_args()

    results = []
    for url in args.urls:
        results.append(scan_url(url))

    # Output
    formatters = {"text": format_text, "json": format_json, "markdown": format_markdown}
    print(formatters[args.format](results))

    # Exit code
    if args.min_grade:
        grade_order = ["F", "D", "C", "B", "A", "A+"]
        min_idx = grade_order.index(args.min_grade)
        worst_grade = min(results, key=lambda r: grade_order.index(r["grade"]))
        worst_idx = grade_order.index(worst_grade["grade"])
        if worst_idx < min_idx:
            sys.exit(2)
        sys.exit(0)
    else:
        worst = min(results, key=lambda r: r["score"])
        sys.exit(GRADE_EXIT_CODES.get(worst["grade"], 2))


if __name__ == "__main__":
    main()
