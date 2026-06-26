#!/usr/bin/env python3
"""
HTTP Header Analyzer — Check security headers and TLS config
Generic version — no personal data
"""

import argparse
import json
import sys
import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import subprocess

SECURITY_HEADERS = {
    "strict-transport-security": {
        "name": "Strict-Transport Security",
        "severity": "medium",
        "description": "Forces HTTPS connections",
        "recommendation": "Add: Strict-Transport-Security: max-age=31536000; includeSubDomains"
    },
    "content-security-policy": {
        "name": "Content Security Policy",
        "severity": "high",
        "description": "Prevents XSS and injection attacks",
        "recommendation": "Add: Content-Security-Policy: default-src 'self'"
    },
    "x-frame-options": {
        "name": "X-Frame-Options",
        "severity": "medium",
        "description": "Prevents clickjacking",
        "recommendation": "Add: X-Frame-Options: DENY"
    },
    "x-content-type-options": {
        "name": "X-Content-Type-Options",
        "severity": "low",
        "description": "Prevents MIME type sniffing",
        "recommendation": "Add: X-Content-Type-Options: nosniff"
    },
    "referrer-policy": {
        "name": "Referrer Policy",
        "severity": "low",
        "description": "Controls referrer information leakage",
        "recommendation": "Add: Referrer-Policy: strict-origin-when-cross-origin"
    },
    "permissions-policy": {
        "name": "Permissions Policy",
        "severity": "low",
        "description": "Restricts browser features",
        "recommendation": "Add: Permissions-Policy: camera=(), microphone=(), geolocation=()"
    },
    "cross-origin-opener-policy": {
        "name": "Cross-Origin Opener Policy",
        "severity": "low",
        "description": "Cross-origin isolation",
        "recommendation": "Add: Cross-Origin-Opener-Policy: same-origin"
    },
    "cross-origin-embedder-policy": {
        "name": "Cross-Origin Embedder Policy",
        "severity": "low",
        "description": "Cross-origin isolation",
        "recommendation": "Add: Cross-Origin-Embedder-Policy: require-corp"
    },
    "cross-origin-resource-policy": {
        "name": "Cross-Origin Resource Policy",
        "severity": "low",
        "description": "Cross-origin resource protection",
        "recommendation": "Add: Cross-Origin-Resource-Policy: same-origin"
    },
}

SENSITIVE_HEADERS = ["server", "x-powered-by", "x-aspnet-version", "x-aspnetmvc-version",
                      "x-generator", "x-drupal-cache", "x-varnish"]


def fetch_headers(url, timeout=10, follow=True, user_agent=None):
    headers = {"User-Agent": user_agent or "Mozilla/5.0 Security Header Analyzer"}
    if HAS_REQUESTS:
        resp = requests.get(url, timeout=timeout, allow_redirects=follow, headers=headers, verify=False)
        return dict(resp.headers), resp.status_code
    else:
        import urllib.request
        import urllib.error
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers=headers)
        try:
            resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            return dict(resp.headers), resp.status
        except urllib.error.HTTPError as e:
            return dict(e.headers), e.code


def check_tls(hostname, port=443):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                return {
                    "protocol": ssock.version(),
                    "cipher": cipher[0] if cipher else "Unknown",
                    "cipher_bits": cipher[2] if cipher else 0,
                    "cert_subject": dict(x[0] for x in cert.get("subject", ())),
                    "cert_issuer": dict(x[0] for x in cert.get("issuer", ())),
                    "cert_expiry": cert.get("notAfter", "Unknown"),
                }
    except Exception as e:
        return {"error": str(e)}


def analyze(url, check_tls_flag=False, timeout=10):
    result = {"url": url, "issues": [], "present": [], "missing": [], "info_disclosure": []}

    try:
        headers, status = fetch_headers(url, timeout=timeout)
    except Exception as e:
        result["error"] = str(e)
        return result

    result["status_code"] = status

    # Check security headers
    for key, info in SECURITY_HEADERS.items():
        if key.lower() in {k.lower() for k in headers}:
            result["present"].append(info["name"])
        else:
            result["missing"].append({"header": info["name"], "severity": info["severity"],
                                       "recommendation": info["recommendation"]})
            result["issues"].append(f"Missing {info['name']} ({info['severity']})")

    # Check info disclosure
    for header in SENSITIVE_HEADERS:
        if header.lower() in {k.lower() for k in headers}:
            val = next((v for k, v in headers.items() if k.lower() == header.lower()), "")
            result["info_disclosure"].append({"header": header, "value": val})

    # Check CSP for unsafe directives
    csp = headers.get("Content-Security-Policy", "") or headers.get("content-security-policy", "")
    if csp:
        if "'unsafe-inline'" in csp:
            result["issues"].append("CSP contains 'unsafe-inline' (weakens XSS protection)")
        if "'unsafe-eval'" in csp:
            result["issues"].append("CSP contains 'unsafe-eval' (allows eval())")

    # TLS check
    if check_tls_flag:
        parsed = urlparse(url)
        if parsed.scheme == "https":
            result["tls"] = check_tls(parsed.hostname, parsed.port or 443)

    result["score"] = f"{len(result['present'])}/{len(SECURITY_HEADERS)}"
    result["risk"] = "HIGH" if len(result["missing"]) > 5 else "MEDIUM" if len(result["missing"]) > 2 else "LOW"

    return result


def main():
    parser = argparse.ArgumentParser(description="HTTP Security Header Analyzer")
    parser.add_argument("url", nargs="?", help="URL to analyze")
    parser.add_argument("-f", "--file", help="File with URLs")
    parser.add_argument("--json", action="store_true", dest="json_out")
    parser.add_argument("--check-tls", action="store_true")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--user-agent")
    parser.add_argument("--severity", choices=["low", "medium", "high"])
    args = parser.parse_args()

    if not HAS_REQUESTS:
        import urllib3
        urllib3.disable_warnings()

    urls = []
    if args.url:
        urls.append(args.url)
    if args.file:
        with open(args.file) as f:
            urls.extend(line.strip() for line in f if line.strip())

    if not urls:
        print("Usage: python3 analyze-headers.py https://example.com")
        sys.exit(1)

    severity_order = {"low": 0, "medium": 1, "high": 2}
    min_severity = severity_order.get(args.severity, 0)

    results = []
    for url in urls:
        if not url.startswith("http"):
            url = "https://" + url
        r = analyze(url, args.check_tls, args.timeout)
        results.append(r)

        if args.json_out:
            print(json.dumps(r, indent=2))
        else:
            print(f"\n=== {url} ===")
            if "error" in r:
                print(f"❌ Error: {r['error']}")
                continue
            for h in r["present"]:
                print(f"✅ {h}")
            for m in r["missing"]:
                if severity_order.get(m["severity"], 0) >= min_severity:
                    print(f"❌ {m['header']} — MISSING ({m['severity']})")
            for i in r["info_disclosure"]:
                print(f"⚠️  {i['header']}: {i['value']} (exposed)")
            for issue in r["issues"]:
                print(f"⚠️  {issue}")
            print(f"\nScore: {r['score']} | Risk: {r['risk']}")

    if not args.json_out and len(results) > 1:
        high_risk = sum(1 for r in results if r.get("risk") == "HIGH")
        print(f"\n=== Summary: {len(results)} URLs scanned, {high_risk} high risk ===")


if __name__ == "__main__":
    main()
