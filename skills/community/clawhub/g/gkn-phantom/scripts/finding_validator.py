#!/usr/bin/env python3
"""Finding Validator for the GKN-Phantom Penetration Testing Skill.

Re-runs a candidate finding's PoC, captures fresh evidence, and classifies it
as validated (TP) or false_positive (FP). Used at the VALIDATION state.

A finding is promoted to `validated` ONLY when:
  - fresh request/response can be reproduced,
  - the detection signal matches the original,
  - reproducible == True,
  - safe_poc == True,
  - confidence >= 0.8.

v5.1 — Automated signal derivation: the validator no longer requires the
caller to pre-judge `signal_matched`. When replay_result omits the field,
the built-in SIGNAL_PATTERNS engine derives it deterministically from the
fresh response body/headers/status code (see match_signal()). An explicit
caller-supplied value is still honored (backward compatible).

This script is intentionally tool-agnostic: it accepts a Finding JSON and a
`replay` callable description, and produces a validated Finding JSON. The
actual HTTP/shell replay is performed by the agent via ctx.tools (or fully
automated by scripts/auto_verifier.py); this script encodes the
deterministic classification logic.

Usage:
  python finding_validator.py --finding finding.json --replay replay.json
  cat finding.json | python finding_validator.py --replay replay.json
  python finding_validator.py --batch findings.json --replays replays.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, utc_now_iso

CONFIDENCE_THRESHOLD = 0.8


def _now_iso() -> str:
    return utc_now_iso()


# =============================================================================
# Signal pattern engine (v5.1 NEW)
# =============================================================================
#
# Deterministic response-body patterns per vulnerability type. These encode
# the "detection_signal" definitions from vuln_detector.py rules into
# machine-checkable regexes so that verification no longer requires a human
# (or the agent) to eyeball the response.

SIGNAL_PATTERNS: dict[str, list[re.Pattern]] = {
    "sqli": [
        re.compile(r"SQL syntax.*?MySQL|Warning.*?\Wmysqli?_", re.I | re.S),
        re.compile(r"MySQLSyntaxErrorException|com\.mysql\.jdbc|MariaDB.*?error", re.I),
        re.compile(r"PostgreSQL.*?ERROR|pg_query\(\).*?failed|Npgsql\.PostgresException", re.I),
        re.compile(r"Microsoft.*?ODBC.*?SQL Server|Unclosed quotation mark|SqlException", re.I),
        re.compile(r"ORA-\d{5}|Oracle.*?Driver|SQL command not properly ended", re.I),
        re.compile(r"SQLite/JDBCDriver|SQLite3?\.query|unrecognized token", re.I),
        re.compile(r"You have an error in your SQL syntax", re.I),
        re.compile(r"syntax error at or near|quoted string not properly terminated", re.I),
    ],
    "path_traversal": [
        re.compile(r"root:x:0:0:"),
        re.compile(r"daemon:x:\d+:\d+:"),
        re.compile(r"\[fonts\]|\[extensions\]", re.I),
        re.compile(r"for 16-bit app support", re.I),
        re.compile(r"; for 16-bit app support", re.I),
    ],
    "info_leak": [
        re.compile(r"\[core\]\s*[\r\n]+\s*repositoryformatversion", re.I),
        re.compile(r"svn:wc:ra_dav:version-url|<svn:", re.I),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"ghp_[A-Za-z0-9]{36}|gho_[A-Za-z0-9]{36}"),
        re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |)PRIVATE KEY-----"),
        re.compile(r"(?i)\b(DB_PASSWORD|APP_KEY|SECRET_KEY|JWT_SECRET|API_KEY)\s*[=:]\s*\S+"),
        re.compile(r"<title>phpinfo\(\)</title>|PHP Version \d\.\d+\.\d+", re.I),
    ],
    "component_exposure": [
        re.compile(r'"activeProfiles"|"propertySources"|"contexts".*?"beans"', re.S),
        re.compile(r'"swagger"\s*:\s*"2\.0"|"openapi"\s*:\s*"3\.', re.I),
        re.compile(r"Druid Stat Index|druid-login|DataSource-|SQL Stat", re.I),
        re.compile(r"Jolokia.*?Agent|jolokia.*?version", re.I),
        re.compile(r"<title>Swagger UI</title>|springfox|knife4j", re.I),
        re.compile(r"UEditor|ueditor\.config", re.I),
    ],
    "directory_listing": [
        re.compile(r"<title>Index of /", re.I),
        re.compile(r">\s*Parent Directory\s*<", re.I),
        re.compile(r"\[To Parent Directory\]", re.I),
    ],
    "graphql_introspection": [
        re.compile(r'"__schema"\s*:', re.I),
        re.compile(r'"queryType"\s*:.*?"types"\s*:\s*\[', re.S),
        re.compile(r"IntrospectionQuery", re.I),
    ],
    "xxe": [
        re.compile(r"SAXParseException|XMLParseException|SimpleXMLElement", re.I),
        re.compile(r"libxml.*?error|XML parser.*?error|DOCTYPE.*?not allowed", re.I),
        re.compile(r"org\.xml\.sax|javax\.xml\.parsers", re.I),
    ],
    "ssti": [
        re.compile(r"jinja2\.|TemplateSyntaxError|UndefinedError", re.I),
        re.compile(r"Twig.*?Error|freemarker\.template|VelocityException", re.I),
    ],
    "deserialization": [
        re.compile(r"InvalidClassException|ObjectInputStream|readObject\(\)", re.I),
        re.compile(r"unserialize\(\)|php unserialize|pickle\.loads|_pickle\.UnpicklingError", re.I),
        re.compile(r"java\.io\.StreamCorruptedException|BinaryReader\.ReadString", re.I),
    ],
    "ldap_injection": [
        re.compile(r"LDAPException|NamingException|javax\.naming", re.I),
        re.compile(r"ldap_bind\(\)|ldap_search\(\)|LDAP error code", re.I),
        re.compile(r"Bad search filter|Invalid DN string", re.I),
    ],
    "nosql_injection": [
        re.compile(r"MongoError|MongoServerError|MongoParseError", re.I),
        re.compile(r"invalid operator|\$where.*?not allowed|unknown operator", re.I),
        re.compile(r"SyntaxError: Unexpected token.*?JSON", re.I),
    ],
    "weak_credential": [
        re.compile(r'"code"\s*:\s*0\s*,\s*"msg"\s*:\s*"(?:success|ok)"', re.I),
        re.compile(r'"success"\s*:\s*true.*?"token"', re.I | re.S),
    ],
    "auth_bypass": [
        re.compile(r'"token"\s*:\s*"[A-Za-z0-9_\-.]{16,}".*?"(?:role|isAdmin)"', re.I | re.S),
    ],
}

# Header-based signal checks: vuln type -> list of (header_name, regex|value_check)
HEADER_SIGNAL_CHECKS: dict[str, list[tuple[str, re.Pattern]]] = {
    "open_redirect": [
        ("Location", re.compile(r"oob\.authorized\.test|PTSKILLTEST|^https?://(?!{host})", re.I)),
    ],
    "crlf_injection": [
        ("Set-Cookie", re.compile(r"PTSKILLTEST=crlf", re.I)),
        ("X-PTSKILLTEST", re.compile(r"injected", re.I)),
    ],
    "cors_misconfig": [
        ("Access-Control-Allow-Origin", re.compile(r"^null$|attacker\.evil\.test|^\*$", re.I)),
    ],
    "host_header_injection": [
        ("Location", re.compile(r"attacker\.evil\.test", re.I)),
    ],
}

# Default markers injected by the detection plan (payload_playbook.md).
DEFAULT_MARKER = "PTSKILLTEST"
SSTI_ARITHMETIC_RESULT = "49"  # {{7*7}}


def _header_lookup(headers: dict | None, name: str) -> str:
    """Case-insensitive header lookup. Returns '' when absent."""
    if not headers:
        return ""
    if isinstance(headers, dict):
        lower = name.lower()
        for k, v in headers.items():
            if str(k).lower() == lower:
                return str(v)
    return ""


def match_signal(
    finding_type: str,
    response_text: str = "",
    headers: dict | None = None,
    status_code: int | None = None,
    marker: str | None = None,
) -> tuple[bool, str]:
    """Deterministically decide whether a fresh response matches the
    detection signal for `finding_type`.

    Returns (matched, reason). `reason` is a short human-readable string
    describing which check fired (or why nothing matched). Used by
    validate() when replay_result does not carry an explicit
    signal_matched flag, and by scripts/auto_verifier.py.
    """
    body = response_text or ""
    marker = marker or DEFAULT_MARKER

    # 1. Type-specific body patterns
    for pattern in SIGNAL_PATTERNS.get(finding_type, []):
        if pattern.search(body):
            return True, f"body pattern matched: {pattern.pattern[:60]}"

    # 2. Header-based signals
    for header_name, pattern in HEADER_SIGNAL_CHECKS.get(finding_type, []):
        value = _header_lookup(headers, header_name)
        if value:
            if header_name == "Location" and finding_type == "open_redirect":
                # Substitute {host} guard: any absolute Location to an
                # external host counts when it carries the marker.
                if marker.lower() in value.lower() or "oob.authorized.test" in value.lower():
                    return True, f"Location header points to authorized sink: {value[:80]}"
            elif pattern.search(value):
                return True, f"header {header_name} matched: {value[:80]}"

    # 3. Marker reflection checks (xss / ssti / host-header / crlf body)
    if finding_type == "xss":
        if marker in body and f"&lt;script&gt;" not in body.lower():
            # Raw marker reflected — check it survived unescaped
            if re.search(re.escape(marker) + r"\s*<", body) or f"<{marker.lower()}" in body.lower() or marker + "<xss>" in body:
                return True, f"marker '{marker}' reflected unescaped"
        escaped_variants = [f"&lt;{marker}", f"&#60;{marker}"]
        if marker in body and not any(e in body for e in escaped_variants):
            return True, f"marker '{marker}' reflected (no escaping detected)"
    elif finding_type == "ssti":
        # Arithmetic evaluation: '49' present while the literal payload is NOT
        if SSTI_ARITHMETIC_RESULT in body and "{{7*7}}" not in body and "${7*7}" not in body:
            return True, "arithmetic result '49' reflected (template evaluated)"
    elif finding_type in ("host_header_injection", "crlf_injection", "open_redirect"):
        if marker in body:
            return True, f"marker '{marker}' reflected in body"
    elif finding_type == "misconfig":
        # misconfig: verbose banner present OR security header absent
        lowered_headers = {str(k).lower() for k in (headers or {})}
        verbose = bool(re.search(r"Server:\s*\S+/\d|X-Powered-By:", body, re.I)) or bool(
            _header_lookup(headers, "X-Powered-By")
        )
        missing = any(
            h not in lowered_headers
            for h in ("strict-transport-security", "content-security-policy", "x-frame-options")
        )
        if verbose or missing:
            return True, "verbose banner present or security header missing"
    elif finding_type == "data_exposure":
        # Local PII threshold check (no network needed) — delegate lazily to
        # vuln_detector.classify_data_exposure to avoid circular import cost
        # at module load.
        try:
            from vuln_detector import classify_data_exposure

            triggered, _score = classify_data_exposure(body)
            if triggered:
                return True, "PII threshold exceeded in response body"
        except ImportError:
            pass

    return False, "no signal matched"


# =============================================================================
# Core validation
# =============================================================================

def validate(finding: dict, replay_result: dict) -> dict:
    """Return a copy of `finding` with updated status/evidence/confidence.

    replay_result shape:
      {
        "request": "...",          # the exact request re-sent
        "response": "...",         # response excerpt captured this run
        "tool": "httpRequest",
        "signal_matched": true,    # OPTIONAL (v5.1): when omitted, derived
                                   # automatically via match_signal()
        "headers": {...},          # OPTIONAL: response headers (dict)
        "status_code": 200,        # OPTIONAL: HTTP status code
        "response_time_ms": 123,   # OPTIONAL: timing evidence
        "marker": "PTSKILLTEST"    # OPTIONAL: custom marker used in probe
      }
    """
    if not isinstance(finding, dict) or not finding.get("type"):
        raise ValueError("finding must be a dict with a 'type' field")
    if not isinstance(replay_result, dict):
        raise ValueError("replay_result must be a dict")

    out = json.loads(json.dumps(finding))  # deep copy
    out.setdefault("evidence", {})

    request = str(replay_result.get("request", "") or "")
    response = str(replay_result.get("response", "") or "")
    tool = replay_result.get("tool", finding.get("evidence", {}).get("tool", ""))
    headers = replay_result.get("headers") or {}
    status_code = replay_result.get("status_code")
    response_time_ms = replay_result.get("response_time_ms")
    marker = replay_result.get("marker")

    # Evidence completeness (safety_policy.md §5)
    evidence_complete = all([request, response, tool])
    if not evidence_complete:
        out["status"] = "false_positive"
        out["confidence"] = 0.0
        out["reproducible"] = False
        out["evidence"]["request"] = request
        out["evidence"]["response"] = response
        out["evidence"]["timestamp"] = _now_iso()
        out["evidence"]["tool"] = tool
        out["validation_note"] = "evidence incomplete; auto-FP"
        return out

    # v5.1: derive signal_matched automatically when the caller did not judge it.
    if "signal_matched" in replay_result:
        signal_matched = bool(replay_result["signal_matched"])
        out["signal_derivation"] = "caller"
    else:
        signal_matched, reason = match_signal(
            out.get("type", ""),
            response_text=response,
            headers=headers,
            status_code=status_code,
            marker=marker,
        )
        out["signal_derivation"] = "auto"
        out["signal_match_reason"] = reason

    # Refresh evidence with the reproducible run
    out["evidence"]["request"] = request
    out["evidence"]["response"] = response
    out["evidence"]["timestamp"] = _now_iso()
    out["evidence"]["tool"] = tool
    if headers:
        out["evidence"]["headers"] = headers
    if status_code is not None:
        out["evidence"]["status_code"] = status_code
    if response_time_ms is not None:
        out["evidence"]["response_time_ms"] = response_time_ms

    reproducible = bool(out.get("reproducible", False)) and signal_matched
    safe_poc = bool(out.get("safe_poc", False))

    if signal_matched:
        # Bump confidence: original + reproduction agree.
        base = float(out.get("confidence", 0.0))
        out["confidence"] = round(min(1.0, max(base, 0.5) + 0.3), 2)
    else:
        out["confidence"] = round(float(out.get("confidence", 0.0)) * 0.3, 2)

    if signal_matched and reproducible and safe_poc and out["confidence"] >= CONFIDENCE_THRESHOLD:
        out["status"] = "validated"
        out["reproducible"] = True
        out["validation_note"] = "reproduced; evidence complete; safe PoC"
    else:
        out["status"] = "false_positive"
        out["reproducible"] = reproducible
        reasons = []
        if not signal_matched:
            reasons.append("signal not matched on replay")
        if not reproducible:
            reasons.append("not reproducible")
        if not safe_poc:
            reasons.append("unsafe PoC")
        if out["confidence"] < CONFIDENCE_THRESHOLD:
            reasons.append(f"confidence {out['confidence']} < {CONFIDENCE_THRESHOLD}")
        out["validation_note"] = "; ".join(reasons) or "unknown"

    return out


def validate_batch(findings: list, replay_results: Any) -> dict:
    """Validate a batch of findings against their replay results.

    replay_results may be:
      - a list aligned 1:1 with `findings`, or
      - a dict keyed by finding id (findings without a matching entry are
        returned with status 'skipped' and reason 'no replay result').

    Returns {"validated": [...], "false_positive": [...], "skipped": [...],
             "summary": {...}}.
    """
    validated: list[dict] = []
    false_positive: list[dict] = []
    skipped: list[dict] = []

    if isinstance(replay_results, dict):
        replay_map: dict[str, dict] = replay_results
        pairs = [(f, replay_map.get(f.get("id", ""))) for f in findings]
    elif isinstance(replay_results, list):
        pairs = list(zip(findings, replay_results))
        if len(findings) > len(replay_results):
            pairs.extend((f, None) for f in findings[len(replay_results):])
    else:
        raise ValueError("replay_results must be a list or a dict keyed by finding id")

    for finding, replay in pairs:
        if not isinstance(finding, dict):
            skipped.append({"finding": finding, "reason": "not a dict"})
            continue
        if not replay:
            entry = json.loads(json.dumps(finding))
            entry["status"] = "skipped"
            entry["validation_note"] = "no replay result provided"
            skipped.append(entry)
            continue
        result = validate(finding, replay)
        if result["status"] == "validated":
            validated.append(result)
        else:
            false_positive.append(result)

    return {
        "validated": validated,
        "false_positive": false_positive,
        "skipped": skipped,
        "summary": {
            "total": len(findings),
            "validated": len(validated),
            "false_positive": len(false_positive),
            "skipped": len(skipped),
        },
    }


def _load(path: str) -> Any:
    return load_json(path)


def main() -> int:
    ap = argparse.ArgumentParser(description="Finding validator (v5.1: auto signal derivation)")
    ap.add_argument("--finding", help="Finding JSON path or '-' (single mode)")
    ap.add_argument("--replay", help="Replay result JSON path or '-' (single mode)")
    ap.add_argument("--batch", help="Findings JSON array path or '-' (batch mode)")
    ap.add_argument("--replays", help="Replay results list/dict path or '-' (batch mode)")
    args = ap.parse_args()

    try:
        if args.batch:
            if not args.replays:
                print("finding_validator: --batch requires --replays", file=sys.stderr)
                return 2
            findings = _load(args.batch)
            replays = _load(args.replays)
            if not isinstance(findings, list):
                print("finding_validator: --batch input must be a JSON array", file=sys.stderr)
                return 2
            result = validate_batch(findings, replays)
            print(dump_json(result))
            return 0 if result["summary"]["validated"] > 0 else 1

        if not args.finding or not args.replay:
            print("finding_validator: provide --finding/--replay or --batch/--replays",
                  file=sys.stderr)
            return 2
        finding = _load(args.finding)
        replay = _load(args.replay)
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"finding_validator: input error: {e}", file=sys.stderr)
        return 2

    try:
        result = validate(finding, replay)
    except ValueError as e:
        print(f"finding_validator: {e}", file=sys.stderr)
        return 2
    print(dump_json(result))
    return 0 if result["status"] == "validated" else 1


if __name__ == "__main__":
    sys.exit(main())
