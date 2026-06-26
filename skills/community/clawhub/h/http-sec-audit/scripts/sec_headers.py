#!/usr/bin/env python3
"""
sec_headers.py — Audit HTTP security headers for any URL.

Usage:
    python3 sec_headers.py https://example.com
    python3 sec_headers.py https://example.com --json
    python3 sec_headers.py https://example.com https://other.com
"""

import argparse
import json
import sys

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


# Header checks: (header_name, description, severity, recommendation)
SECURITY_HEADERS = [
    {
        "header": "Strict-Transport-Security",
        "alias": "HSTS",
        "severity": "high",
        "desc": "Enforces HTTPS connections, prevents SSL-stripping attacks",
        "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload",
    },
    {
        "header": "Content-Security-Policy",
        "alias": "CSP",
        "severity": "high",
        "desc": "Prevents XSS, clickjacking, and code injection attacks",
        "recommendation": "Add a CSP header. Start with: Content-Security-Policy: default-src 'self'",
    },
    {
        "header": "X-Content-Type-Options",
        "alias": "XCTO",
        "severity": "medium",
        "desc": "Prevents MIME-type sniffing",
        "recommendation": "Add: X-Content-Type-Options: nosniff",
    },
    {
        "header": "X-Frame-Options",
        "alias": "XFO",
        "severity": "medium",
        "desc": "Prevents clickjacking by controlling iframe embedding",
        "recommendation": "Add: X-Frame-Options: DENY (or SAMEORIGIN if iframes needed)",
    },
    {
        "header": "Referrer-Policy",
        "alias": "RP",
        "severity": "medium",
        "desc": "Controls referrer information sent with requests",
        "recommendation": "Add: Referrer-Policy: strict-origin-when-cross-origin",
    },
    {
        "header": "Permissions-Policy",
        "alias": "PP",
        "severity": "medium",
        "desc": "Controls browser features (camera, microphone, geolocation, etc.)",
        "recommendation": "Add: Permissions-Policy: camera=(), microphone=(), geolocation=()",
    },
    {
        "header": "X-XSS-Protection",
        "alias": "XXSS",
        "severity": "low",
        "desc": "Legacy XSS filter (modern browsers use CSP instead)",
        "recommendation": "Add: X-XSS-Protection: 0 (disable legacy filter, rely on CSP)",
    },
    {
        "header": "Cross-Origin-Opener-Policy",
        "alias": "COOP",
        "severity": "low",
        "desc": "Isolates browsing context to prevent cross-origin attacks",
        "recommendation": "Add: Cross-Origin-Opener-Policy: same-origin",
    },
    {
        "header": "Cross-Origin-Resource-Policy",
        "alias": "CORP",
        "severity": "low",
        "desc": "Controls which origins can load the resource",
        "recommendation": "Add: Cross-Origin-Resource-Policy: same-origin",
    },
    {
        "header": "Cross-Origin-Embedder-Policy",
        "alias": "COEP",
        "severity": "low",
        "desc": "Prevents loading cross-origin resources without explicit permission",
        "recommendation": "Add: Cross-Origin-Embedder-Policy: require-corp",
    },
]

DANGEROUS_HEADERS = [
    {
        "header": "Server",
        "desc": "Leaks server software and version information",
        "recommendation": "Remove or obfuscate the Server header",
    },
    {
        "header": "X-Powered-By",
        "desc": "Leaks technology stack information",
        "recommendation": "Remove the X-Powered-By header",
    },
    {
        "header": "X-AspNet-Version",
        "desc": "Leaks ASP.NET version",
        "recommendation": "Remove the X-AspNet-Version header",
    },
]


def audit_url(url: str, timeout: int) -> dict:
    """Audit a single URL and return results."""
    result = {
        "url": url,
        "status": None,
        "present": [],
        "missing": [],
        "warnings": [],
        "info_leak": [],
        "score": 0,
        "grade": "",
        "error": None,
    }

    headers = {"User-Agent": "SecHeadersAudit/1.0 (OpenClaw skill)"}

    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        result["status"] = resp.status_code
    except requests.exceptions.SSLError as e:
        result["error"] = f"SSL error: {e}"
        result["grade"] = "F"
        return result
    except Exception as e:
        result["error"] = f"Request failed: {e}"
        result["grade"] = "F"
        return result

    resp_headers = {k.lower(): v for k, v in resp.headers.items()}

    # Check security headers
    total_weight = 0
    earned_weight = 0
    weight_map = {"high": 3, "medium": 2, "low": 1}

    for check in SECURITY_HEADERS:
        header_lower = check["header"].lower()
        weight = weight_map[check["severity"]]
        total_weight += weight

        if header_lower in resp_headers:
            value = resp_headers[header_lower]
            result["present"].append({
                "header": check["header"],
                "value": value,
                "severity": check["severity"],
            })
            earned_weight += weight

            # Warn about weak values
            if check["header"] == "Strict-Transport-Security":
                if "max-age=0" in value:
                    result["warnings"].append(f"HSTS max-age=0 effectively disables HSTS")
                    earned_weight -= weight
            if check["header"] == "Content-Security-Policy":
                if "unsafe-inline" in value or "unsafe-eval" in value:
                    result["warnings"].append(f"CSP contains unsafe directives: {value[:80]}")
        else:
            result["missing"].append({
                "header": check["header"],
                "severity": check["severity"],
                "desc": check["desc"],
                "recommendation": check["recommendation"],
            })

    # Check for info leaks
    for check in DANGEROUS_HEADERS:
        header_lower = check["header"].lower()
        if header_lower in resp_headers:
            result["info_leak"].append({
                "header": check["header"],
                "value": resp_headers[header_lower],
                "desc": check["desc"],
                "recommendation": check["recommendation"],
            })

    # Calculate score and grade
    score = round((earned_weight / total_weight) * 100) if total_weight > 0 else 0
    # Penalize info leaks slightly
    score = max(0, score - len(result["info_leak"]) * 3)
    result["score"] = score

    if score >= 90:
        result["grade"] = "A"
    elif score >= 75:
        result["grade"] = "B"
    elif score >= 50:
        result["grade"] = "C"
    elif score >= 25:
        result["grade"] = "D"
    else:
        result["grade"] = "F"

    return result


def print_report(result: dict):
    """Print a human-readable report."""
    url = result["url"]
    print(f"\n{'='*60}")
    print(f" HTTP Security Headers Audit")
    print(f" {url}")
    print(f"{'='*60}")

    if result["error"]:
        print(f"\n ERROR: {result['error']}")
        return

    print(f"\n Status: {result['status']}")
    print(f" Score:  {result['score']}/100 (Grade: {result['grade']})")

    if result["present"]:
        print(f"\n PRESENT ({len(result['present'])} headers):")
        for h in result["present"]:
            sev_icon = {"high": "●", "medium": "◐", "low": "○"}[h["severity"]]
            val_preview = h["value"][:60] + ("..." if len(h["value"]) > 60 else "")
            print(f"   {sev_icon} {h['header']}: {val_preview}")

    if result["missing"]:
        print(f"\n MISSING ({len(result['missing'])} headers):")
        for h in result["missing"]:
            sev_icon = {"high": "●", "medium": "◐", "low": "○"}[h["severity"]]
            print(f"   {sev_icon} [{h['severity'].upper()}] {h['header']}")
            print(f"     → {h['desc']}")
            print(f"     Fix: {h['recommendation']}")

    if result["warnings"]:
        print(f"\n WARNINGS:")
        for w in result["warnings"]:
            print(f"   ⚠ {w}")

    if result["info_leak"]:
        print(f"\n INFO LEAKS:")
        for h in result["info_leak"]:
            print(f"   ! {h['header']}: {h['value']}")
            print(f"     → {h['recommendation']}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Audit HTTP security headers for one or more URLs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com https://google.com
  %(prog)s https://example.com --json
  %(prog)s https://example.com --timeout 5
""",
    )
    parser.add_argument("urls", nargs="+", help="One or more URLs to audit")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")

    args = parser.parse_args()

    results = []
    for url in args.urls:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        results.append(audit_url(url, args.timeout))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print_report(r)
        # Summary
        if len(results) > 1:
            print("SUMMARY:")
            for r in results:
                grade = r.get("grade", "?")
                score = r.get("score", 0)
                print(f"  {grade} ({score}/100) — {r['url']}")
            print()


if __name__ == "__main__":
    main()
