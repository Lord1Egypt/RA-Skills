#!/usr/bin/env python3
"""JavaScript Static Analyzer — client-side vulnerability mining (v3.0.0).

Analyzes JavaScript source files, source maps, and in-page scripts to discover:
  1. Secrets & API keys leaked in JS bundles
  2. Prototype pollution gadgets (__proto__, constructor.prototype)
  3. DOM clobbering vulnerabilities
  4. postMessage misconfiguration (missing origin check)
  5. Dangerous sinks (eval, innerHTML, document.write, Function constructor)
  6. Debug endpoints & internal URLs
  7. Weak crypto usage (Math.random for tokens, MD5/SHA1 for passwords)
  8. Client-side path traversal / open redirect in JS routing
  9. Hardcoded credentials
  10. Third-party dependency CVE correlation

This module is deterministic and side-effect free: it takes JS source/text
and emits a structured analysis report. The agent is responsible for
fetching JS files via ctx.tools.

Usage (CLI):
  python js_analyzer.py --source app.js --url https://target.test/static/app.js
  python js_analyzer.py --source-list js_files.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json


# ---- Secret patterns (regex) ------------------------------------------------
SECRET_PATTERNS = {
    "aws_access_key": r"AKIA[0-9A-Z]{16}",
    "aws_secret_key": r"(?i)aws[_.-]?secret[_.-]?(?:access[_.-]?)?key\s*[:=]\s*['\"]([^'\"]+)['\"]",
    "github_token": r"gh[pousr]_[a-zA-Z0-9]{36}",
    "google_api_key": r"AIza[0-9A-Za-z\-_]{35}",
    "slack_token": r"xox[baprs]-[0-9A-Za-z\-]+",
    "jwt_token": r"eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}",
    "private_key": r"-----BEGIN (?:RSA|EC|DSA|OPENSSH|PGP) PRIVATE KEY-----",
    "generic_api_key": r"(?i)(?:api[_-]?key|apikey|secret|token|password|passwd)\s*[:=]\s*['\"]([^'\"]{8,})['\"]",
    "connection_string": r"(?:mongodb|mysql|postgres|redis|jdbc)://[^'\"]+",
    "internal_url": r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|172\.16\.\d+\.\d+|192\.168\.\d+\.\d+)[^\s'\"<>]*",
    "stripe_key": r"(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{24,}",
    "firebase_config": r"(?:apiKey|authDomain|projectId|messagingSenderId)\s*:\s*['\"]([^'\"]+)['\"]",
}

# ---- Dangerous sinks (JS API calls that can lead to XSS/DOM-based vulns) ----
DANGEROUS_SINKS = {
    "innerHTML": r"\.innerHTML\s*=",
    "outerHTML": r"\.outerHTML\s*=",
    "document_write": r"document\.write\s*\(",
    "document_writeln": r"document\.writeln\s*\(",
    "eval": r"\beval\s*\(",
    "function_constructor": r"new\s+Function\s*\(",
    "setTimeout_string": r"setTimeout\s*\(\s*['\"]",
    "setInterval_string": r"setInterval\s*\(\s*['\"]",
    "location_href": r"\.location\.href\s*=",
    "location_assign": r"\.location\.assign\s*\(",
    "location_replace": r"\.location\.replace\s*\(",
    "insertAdjacentHTML": r"\.insertAdjacentHTML\s*\(",
    "srcdoc": r"\.srcdoc\s*=",
    "dangerouslySetInnerHTML": r"dangerouslySetInnerHTML",
}

# ---- postMessage patterns ---------------------------------------------------
POSTMESSAGE_PATTERNS = {
    "postMessage_send": r"\.postMessage\s*\(([^)]+)\)",
    "message_listener": r"\.addEventListener\s*\(\s*['\"]message['\"]",
    "origin_check": r"event\.origin\s*[=!]==?\s*['\"]",
}

# ---- Prototype pollution patterns -------------------------------------------
PROTO_POLLUTION_PATTERNS = {
    "proto_access": r"__proto__",
    "constructor_prototype": r"constructor\s*\.\s*prototype",
    "object_assign": r"Object\.assign\s*\(",
    "merge_deep": r"(?:merge|extend|clone|deep)\s*(?:Deep)?\s*\(",
    "spread_operator": r"\.\.\.\w+\s*[,;})]",
    "lodash_merge": r"(?:_\.)?(?:merge|defaultsDeep|mergeWith)\s*\(",
}

# ---- Weak crypto patterns ---------------------------------------------------
WEAK_CRYPTO_PATTERNS = {
    "math_random": r"Math\.random\s*\(\s*\)",
    "md5": r"\b[Mm][Dd]5\b",
    "sha1": r"\b[Ss][Hh][Aa]1\b",
    "des": r"\bDES\b",
    "rc4": r"\bRC4\b",
}

# ---- Debug / internal endpoint patterns -------------------------------------
DEBUG_PATTERNS = {
    "debug_endpoint": r"(?:/debug|/test|/mock|/staging|/internal|/local|/sandbox)",
    "webpack_dev": r"webpack://",
    "source_map": r"//# sourceMappingURL=",
    "console_log": r"console\.(?:log|warn|error)\s*\([^)]*\)",
    "debugger": r"\bdebugger\b",
}

# ---- DOM clobbering patterns ------------------------------------------------
DOM_CLOBBER_PATTERNS = {
    "named_access": r"document\.getElementById|document\.getElementsByName",
    "form_elements": r"\.elements\s*\[",
    "embed_object": r"<(?:embed|object|form)\s",
    "id_attribute": r'\bid\s*=\s*["\']',
}


@dataclass
class JSFinding:
    """A single finding from JS analysis."""
    type: str                # secret_leak | dangerous_sink | proto_pollution |
                             # postmessage_misconfig | weak_crypto | debug_leak |
                             # dom_clobber | hardcoded_cred | internal_url
    severity: str            # low | medium | high | critical
    pattern: str
    match: str
    line: int = 0
    context: str = ""        # surrounding code context
    source_file: str = ""
    source_url: str = ""


@dataclass
class JSAnalysisReport:
    """Full JS analysis report."""
    source_url: str
    source_file: str
    total_lines: int
    findings: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)


def _find_line_number(source: str, match_pos: int) -> int:
    """Calculate the line number of a match position."""
    return source[:match_pos].count("\n") + 1


def _extract_context(source: str, match_start: int, match_end: int, context_lines: int = 2) -> str:
    """Extract surrounding code context around a match."""
    lines = source.split("\n")
    line_num = source[:match_start].count("\n")
    start = max(0, line_num - context_lines)
    end = min(len(lines), line_num + context_lines + 1)
    return "\n".join(lines[start:end])


def _classify_severity(pattern_type: str) -> str:
    """Classify finding severity based on pattern type."""
    critical = {"aws_access_key", "aws_secret_key", "private_key", "connection_string",
                 "github_token", "stripe_key"}
    high = {"google_api_key", "slack_token", "generic_api_key", "jwt_token",
            "dangerouslySetInnerHTML", "eval", "function_constructor"}
    medium = {"internal_url", "innerHTML", "document_write", "insertAdjacentHTML",
              "postmessage_misconfig", "proto_access", "constructor_prototype",
              "firebase_config"}
    low = {"console_log", "debugger", "debug_endpoint", "source_map", "webpack_dev",
           "math_random", "md5", "sha1", "des", "rc4", "form_elements", "named_access"}
    if pattern_type in critical:
        return "critical"
    if pattern_type in high:
        return "high"
    if pattern_type in medium:
        return "medium"
    return "low"


def analyze_secrets(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan JS source for leaked secrets and API keys."""
    findings = []
    for name, pattern in SECRET_PATTERNS.items():
        for m in re.finditer(pattern, source, re.MULTILINE):
            findings.append(JSFinding(
                type="secret_leak",
                severity=_classify_severity(name),
                pattern=name,
                match=m.group(0),
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze_dangerous_sinks(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan for dangerous JS API calls."""
    findings = []
    for name, pattern in DANGEROUS_SINKS.items():
        for m in re.finditer(pattern, source, re.MULTILINE):
            findings.append(JSFinding(
                type="dangerous_sink",
                severity=_classify_severity(name),
                pattern=name,
                match=m.group(0),
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze_postmessage(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan for postMessage misconfiguration."""
    findings = []
    # Check for postMessage listeners
    listeners = list(re.finditer(POSTMESSAGE_PATTERNS["message_listener"], source))
    for lm in listeners:
        # Look for origin check after the listener
        after_listener = source[lm.start():lm.start() + 500]
        has_origin_check = bool(re.search(POSTMESSAGE_PATTERNS["origin_check"], after_listener))
        if not has_origin_check:
            findings.append(JSFinding(
                type="postmessage_misconfig",
                severity="medium",
                pattern="missing_origin_check",
                match="addEventListener('message', ...) without origin check",
                line=_find_line_number(source, lm.start()),
                context=_extract_context(source, lm.start(), lm.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    # Check for postMessage sends
    for m in re.finditer(POSTMESSAGE_PATTERNS["postMessage_send"], source):
        args = m.group(1)
        if "*" in args:
            findings.append(JSFinding(
                type="postmessage_misconfig",
                severity="medium",
                pattern="wildcard_target_origin",
                match=f"postMessage({args})",
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze_prototype_pollution(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan for prototype pollution vectors."""
    findings = []
    for name, pattern in PROTO_POLLUTION_PATTERNS.items():
        for m in re.finditer(pattern, source, re.MULTILINE):
            findings.append(JSFinding(
                type="proto_pollution",
                severity=_classify_severity(name),
                pattern=name,
                match=m.group(0),
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze_weak_crypto(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan for weak cryptographic usage."""
    findings = []
    for name, pattern in WEAK_CRYPTO_PATTERNS.items():
        for m in re.finditer(pattern, source, re.MULTILINE):
            findings.append(JSFinding(
                type="weak_crypto",
                severity=_classify_severity(name),
                pattern=name,
                match=m.group(0),
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze_debug_leaks(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan for debug endpoints, source maps, and dev info leaks."""
    findings = []
    for name, pattern in DEBUG_PATTERNS.items():
        for m in re.finditer(pattern, source, re.MULTILINE):
            findings.append(JSFinding(
                type="debug_leak",
                severity=_classify_severity(name),
                pattern=name,
                match=m.group(0),
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze_dom_clobbering(source: str, source_url: str = "", source_file: str = "") -> list[JSFinding]:
    """Scan for DOM clobbering vulnerabilities."""
    findings = []
    for name, pattern in DOM_CLOBBER_PATTERNS.items():
        for m in re.finditer(pattern, source, re.MULTILINE):
            findings.append(JSFinding(
                type="dom_clobber",
                severity=_classify_severity(name),
                pattern=name,
                match=m.group(0),
                line=_find_line_number(source, m.start()),
                context=_extract_context(source, m.start(), m.end()),
                source_file=source_file,
                source_url=source_url,
            ))
    return findings


def analyze(source: str, source_url: str = "", source_file: str = "") -> JSAnalysisReport:
    """Run all JS analysis modules and return a structured report."""
    report = JSAnalysisReport(
        source_url=source_url,
        source_file=source_file,
        total_lines=source.count("\n") + 1,
    )

    report.findings.extend(analyze_secrets(source, source_url, source_file))
    report.findings.extend(analyze_dangerous_sinks(source, source_url, source_file))
    report.findings.extend(analyze_postmessage(source, source_url, source_file))
    report.findings.extend(analyze_prototype_pollution(source, source_url, source_file))
    report.findings.extend(analyze_weak_crypto(source, source_url, source_file))
    report.findings.extend(analyze_debug_leaks(source, source_url, source_file))
    report.findings.extend(analyze_dom_clobbering(source, source_url, source_file))

    # Summary
    by_type = {}
    by_severity = {}
    for f in report.findings:
        by_type[f.type] = by_type.get(f.type, 0) + 1
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    report.summary = {
        "total_findings": len(report.findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "files_analyzed": 1,
        "total_lines": report.total_lines,
    }
    return report


def analyze_file_list(source_list: list[dict]) -> dict:
    """Analyze multiple JS files from a source list.

    Each item in source_list should have:
      - source (str): JS source code
      - url (str, optional): source URL
      - file (str, optional): source file path
    """
    all_findings = []
    for item in source_list:
        source = item.get("source", "")
        url = item.get("url", "")
        file = item.get("file", "")
        report = analyze(source, url, file)
        all_findings.extend(report.findings)

    by_type = {}
    by_severity = {}
    for f in all_findings:
        by_type[f.type] = by_type.get(f.type, 0) + 1
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    return {
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "files_analyzed": len(source_list),
        "findings": [{
            "type": f.type, "severity": f.severity, "pattern": f.pattern,
            "match": f.match[:200], "line": f.line, "context": f.context[:500],
            "source_file": f.source_file, "source_url": f.source_url,
        } for f in all_findings],
    }


# ---- Hidden endpoint extraction (feeds parameter probing) --------------------

_JS_ENDPOINT_RE = re.compile(
    r"""["'`](/[A-Za-z0-9_\-./%~]*\?[A-Za-z0-9_\-]+=[^"'`\s]+)["'`]"""
)


def extract_endpoint_entries(source: str, base_url: str = "",
                             max_entries: int = 10) -> list[dict]:
    """Extract parameterized endpoints (path?query) hardcoded in JS source.

    JS bundles are the highest-frequency source of hidden API endpoints in
    SRC work. Only relative paths carrying a query string are kept — they
    are resolved against base_url and returned in discover_params-compatible
    shape so the caller can feed them straight into probe_injection:

      [{"url": "https://origin/api/x?id=1", "param": "id", "value": "1"}]
    """
    from urllib.parse import urlsplit, parse_qsl, urljoin

    entries: list[dict] = []
    seen: set[str] = set()
    for m in _JS_ENDPOINT_RE.finditer(source):
        rel = m.group(1)
        if "#" in rel or len(rel) > 512:
            continue
        for name, value in parse_qsl(urlsplit(rel).query, keep_blank_values=True):
            url = urljoin(base_url, rel) if base_url else rel
            key = f"{url}|{name}"
            if key in seen:
                continue
            seen.add(key)
            entries.append({"url": url, "param": name, "value": value})
            if len(entries) >= max_entries:
                return entries
    return entries


def main() -> int:
    ap = argparse.ArgumentParser(description="JS Static Analyzer — client-side vulnerability mining (v3.0)")
    ap.add_argument("--source", help="JS source file path or '-'")
    ap.add_argument("--source-list", help="JSON list of JS files to analyze")
    ap.add_argument("--url", default="", help="Source URL for context")
    args = ap.parse_args()

    if args.source_list:
        source_list = load_json(args.source_list)
        result = analyze_file_list(source_list)
        print(dump_json(result))
    elif args.source:
        source = load_json(args.source) if args.source == "-" else open(args.source, "r", encoding="utf-8", errors="replace").read()
        report = analyze(source, source_url=args.url, source_file=args.source)
        out = {
            "source_url": report.source_url,
            "source_file": report.source_file,
            "total_lines": report.total_lines,
            "summary": report.summary,
            "findings": [{
                "type": f.type, "severity": f.severity, "pattern": f.pattern,
                "match": f.match[:200], "line": f.line, "context": f.context[:500],
            } for f in report.findings],
        }
        print(dump_json(out))
    else:
        print("js_analyzer: --source or --source-list required", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())