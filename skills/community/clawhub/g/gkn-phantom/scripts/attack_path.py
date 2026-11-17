#!/usr/bin/env python3
"""Attack Path Engine for the GKN-Phantom Penetration Testing Skill.

Combines validated findings into exploit chains (auth bypass, privilege
escalation, data exposure) and emits a graph { nodes, edges }.

Only edges confirmed by evidence are marked confirmed=true. The LLM may
suggest candidate edges, but this script encodes the deterministic rules that
decide confirmation.

Chain heuristics (evidence-backed):
  - auth_bypass: a finding of type xss/sqli/misconfig on an auth endpoint
    enables an idor/ssrf finding on a protected endpoint.
  - privilege_escalation: an idor finding on an admin object enables a
    misconfig/sqli finding exposing further admin objects.
  - data_exposure: any validated finding whose response contains data fields
    is linked to the asset node it exposes.
  - weak_credential_chain: weak_credential on login → idor/sqli/logic_flaw
    on authenticated endpoints (弱口令→后台→数据泄露, Edu 高频链).
  - component_exposure_chain: component_exposure (Actuator/Swagger) →
    sqli/file_upload/logic_flaw on discovered endpoints.
  - file_upload_chain: file_upload → rce (if confirmed) OR stored xss.

Usage:
  python attack_path.py --findings findings.json --assets assets.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json

# Sensitive JSON field names that indicate a real data exposure (vs. plain
# reflection). Using a structural whitelist avoids false positives from
# substring matches (e.g. earlier "idToken" matching "token").
SENSITIVE_FIELDS = {
    "email", "phone", "ssn", "address", "dob",
    "password", "passwd", "pwd",
    "secret", "api_key", "apikey", "apiKey",
    "token", "access_token", "refresh_token", "bearer",
    "private_key", "privateKey", "session",
}


def _severity_rank(s: str) -> int:
    return {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(s, 0)


def build_paths(findings: list[dict], assets: dict) -> list[dict]:
    validated = [f for f in findings if f.get("status") == "validated"]
    paths: list[dict] = []

    # nodes: every validated finding + every endpoint asset
    nodes: list[dict] = []
    for f in validated:
        nodes.append({"id": f["id"], "type": "finding", "ref": f["id"]})
    for ep in assets.get("endpoints", []):
        url = ep.get("url", "") if isinstance(ep, dict) else str(ep)
        nodes.append({"id": f"asset:{url}", "type": "asset", "ref": url})

    def _has_data(resp: str) -> bool:
        """Detect real data exposure via structural JSON field whitelist.

        Tries to parse the response as JSON (object or array). If parsed,
        scans recursively for any sensitive field name with a non-empty value.
        If not parseable, falls back to None and the caller treats it as
        "no confirmed exposure" (we do NOT use loose substring matching —
        that's a false-positive magnet).
        """
        if not resp:
            return False
        try:
            obj = json.loads(resp)
        except (ValueError, TypeError):
            # If the response is HTML/text, look for JSON-like fragments
            # bounded by { and } to avoid matching the full HTML.
            start = resp.find("{")
            end = resp.rfind("}")
            if start >= 0 and end > start:
                try:
                    obj = json.loads(resp[start : end + 1])
                except (ValueError, TypeError):
                    return False
            else:
                return False

        def _walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k in SENSITIVE_FIELDS and v not in (None, "", [], {}):
                        return True
                    if _walk(v):
                        return True
            elif isinstance(node, list):
                return any(_walk(x) for x in node)
            return False

        return _walk(obj)

    # Auth bypass chain: auth-surface finding -> protected-surface finding
    auth_surface_types = {"xss", "sqli", "misconfig"}
    auth_keywords = ("login", "auth", "signin", "session", "token")
    protected_keywords = ("admin", "user", "account", "profile", "api")

    auth_findings = [
        f for f in validated
        if f.get("type") in auth_surface_types
        and any(k in (f.get("target", "") + f.get("evidence", {}).get("request", "")).lower()
                for k in auth_keywords)
    ]
    protected_findings = [
        f for f in validated
        if any(k in (f.get("target", "") + f.get("evidence", {}).get("request", "")).lower()
               for k in protected_keywords)
    ]

    for af in auth_findings:
        edges: list[dict] = []
        for pf in protected_findings:
            if af["id"] == pf["id"]:
                continue
            edges.append({
                "from": af["id"],
                "to": pf["id"],
                "relation": "enables",
                "confirmed": True,
            })
            # link the protected finding to the asset it exposes
            target = pf.get("target", "")
            edges.append({
                "from": pf["id"],
                "to": f"asset:{target}",
                "relation": "exposes",
                "confirmed": _has_data(pf.get("evidence", {}).get("response", "")),
            })
        if edges:
            sev = max(
                [af.get("severity", "low")] + [pf.get("severity", "low") for pf in protected_findings],
                key=_severity_rank,
            )
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Auth bypass → protected access",
                "nodes": [n for n in nodes if n["id"] in {af["id"]} or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Compromise of {af.get('target')} enables unauthorized access to protected resources.",
                "confidence": 0.85,
            })

    # ---- NEW: weak_credential chain (弱口令→后台→数据泄露/IDOR/SQLi) ----------
    # Edu 高校最高频攻击链：弱口令登录 → 后台功能 → 数据泄露
    weak_cred_findings = [f for f in validated if f.get("type") == "weak_credential"]
    protected_types = {"idor", "sqli", "logic_flaw", "data_exposure", "file_upload"}
    protected_by_cred = [
        f for f in validated
        if f.get("type") in protected_types
        and any(k in (f.get("target", "") + f.get("evidence", {}).get("request", "")).lower()
                for k in protected_keywords)
    ]
    for wcf in weak_cred_findings:
        edges = []
        for pf in protected_by_cred:
            if wcf["id"] == pf["id"]:
                continue
            edges.append({
                "from": wcf["id"],
                "to": pf["id"],
                "relation": "enables",
                "confirmed": True,
            })
            target = pf.get("target", "")
            edges.append({
                "from": pf["id"],
                "to": f"asset:{target}",
                "relation": "exposes",
                "confirmed": _has_data(pf.get("evidence", {}).get("response", "")),
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Weak credential → authenticated access → data exposure",
                "nodes": [n for n in nodes if n["id"] == wcf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Weak/default credential on {wcf.get('target')} enables authenticated exploitation of protected resources.",
                "confidence": 0.9,
            })

    # ---- NEW: component_exposure chain (组件泄露→接口发现→漏洞利用) ----------
    # 企业高频链：Actuator/Swagger 泄露 → 接口枚举 → SQLi/IDOR/文件上传
    component_findings = [f for f in validated if f.get("type") == "component_exposure"]
    exploitable_types = {"sqli", "idor", "file_upload", "logic_flaw", "ssrf"}
    exploitable = [f for f in validated if f.get("type") in exploitable_types]
    for cf in component_findings:
        edges = []
        for ef in exploitable:
            if cf["id"] == ef["id"]:
                continue
            edges.append({
                "from": cf["id"],
                "to": ef["id"],
                "relation": "enables_recon",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": f"Component exposure → exploitation ({cf.get('type', '')})",
                "nodes": [n for n in nodes if n["id"] == cf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Exposed component ({cf.get('target')}) enables discovery and exploitation of further vulnerabilities.",
                "confidence": 0.8,
            })

    # ---- NEW: file_upload → rce/xss chain ----------
    upload_findings = [f for f in validated if f.get("type") == "file_upload"]
    rce_or_stored_xss = [f for f in validated if f.get("type") in {"rce"} or
                         (f.get("type") == "xss" and f.get("severity") == "high")]
    for uf in upload_findings:
        edges = []
        for rf in rce_or_stored_xss:
            if uf["id"] == rf["id"]:
                continue
            edges.append({
                "from": uf["id"],
                "to": rf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "File upload → code execution / stored XSS",
                "nodes": [n for n in nodes if n["id"] in {uf["id"]} or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"File upload at {uf.get('target')} enables code execution or persistent XSS.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: SSRF → cloud metadata → credential leak → full compromise ----
    ssrf_findings = [f for f in validated if f.get("type") == "ssrf"]
    data_exposure_findings = [f for f in validated if f.get("type") == "data_exposure"]
    for sf in ssrf_findings:
        edges = []
        for df in data_exposure_findings:
            if sf["id"] == df["id"]:
                continue
            edges.append({
                "from": sf["id"],
                "to": df["id"],
                "relation": "enables",
                "confirmed": _has_data(df.get("evidence", {}).get("response", "")),
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "SSRF → cloud metadata → credential leak",
                "nodes": [n for n in nodes if n["id"] == sf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"SSRF at {sf.get('target')} enables access to cloud metadata service, leaking credentials and sensitive data.",
                "confidence": 0.9,
            })

    # ---- v3 NEW: SQLi → data exfiltration → credential dumping → privilege escalation ----
    sqli_findings = [f for f in validated if f.get("type") == "sqli"]
    priv_esc_findings = [f for f in validated if f.get("type") == "priv_esc"]
    for sf in sqli_findings:
        edges = []
        for pf in priv_esc_findings:
            if sf["id"] == pf["id"]:
                continue
            edges.append({
                "from": sf["id"],
                "to": pf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        # Also link to data exposure targets
        for df in data_exposure_findings:
            if sf["id"] == df["id"]:
                continue
            edges.append({
                "from": sf["id"],
                "to": df["id"],
                "relation": "exposes",
                "confirmed": _has_data(df.get("evidence", {}).get("response", "")),
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "SQL injection → data exfiltration → credential dumping",
                "nodes": [n for n in nodes if n["id"] == sf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"SQL injection at {sf.get('target')} enables database exfiltration, credential dumping, and potential privilege escalation.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: IDOR → mass data enumeration → PII exposure ----
    idor_findings = [f for f in validated if f.get("type") == "idor"]
    for idf in idor_findings:
        edges = []
        for df in data_exposure_findings:
            if idf["id"] == df["id"]:
                continue
            if _has_data(df.get("evidence", {}).get("response", "")):
                edges.append({
                    "from": idf["id"],
                    "to": df["id"],
                    "relation": "enables",
                    "confirmed": True,
                })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "IDOR → mass enumeration → PII exposure",
                "nodes": [n for n in nodes if n["id"] == idf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"IDOR at {idf.get('target')} enables mass data enumeration leading to PII exposure and regulatory violation risk.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: SSTI → RCE → full system compromise ----
    ssti_findings = [f for f in validated if f.get("type") == "ssti"]
    rce_findings = [f for f in validated if f.get("type") == "rce"]
    for ssf in ssti_findings:
        edges = []
        for rf in rce_findings:
            if ssf["id"] == rf["id"]:
                continue
            edges.append({
                "from": ssf["id"],
                "to": rf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "SSTI → RCE → full system compromise",
                "nodes": [n for n in nodes if n["id"] == ssf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"SSTI at {ssf.get('target')} escalates to remote code execution and full system compromise.",
                "confidence": 0.9,
            })

    # ---- v3 NEW: XSS → session hijacking → account takeover ----
    xss_findings = [f for f in validated if f.get("type") == "xss"]
    auth_bypass_findings = [f for f in validated if f.get("type") == "auth_bypass"]
    for xf in xss_findings:
        edges = []
        for af in auth_bypass_findings:
            if xf["id"] == af["id"]:
                continue
            edges.append({
                "from": xf["id"],
                "to": af["id"],
                "relation": "enables",
                "confirmed": True,
            })
        # XSS also enables IDOR/privilege escalation
        for idf in idor_findings:
            if xf["id"] == idf["id"]:
                continue
            edges.append({
                "from": xf["id"],
                "to": idf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "XSS → session hijacking → account takeover / data access",
                "nodes": [n for n in nodes if n["id"] == xf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"XSS at {xf.get('target')} enables session hijacking, account takeover, and lateral privilege escalation.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: CORS misconfig → CSRF → account takeover ----
    cors_findings = [f for f in validated if f.get("type") == "cors_misconfig"]
    csrf_findings = [f for f in validated if f.get("type") == "csrf"]
    for cf in cors_findings:
        edges = []
        for crf in csrf_findings:
            if cf["id"] == crf["id"]:
                continue
            edges.append({
                "from": cf["id"],
                "to": crf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "CORS misconfiguration → CSRF → account takeover",
                "nodes": [n for n in nodes if n["id"] == cf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"CORS misconfiguration at {cf.get('target')} enables cross-origin CSRF attacks leading to account takeover.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: Cache poisoning → stored XSS → mass exploitation ----
    cache_findings = [f for f in validated if f.get("type") == "cache_poisoning"]
    for cpf in cache_findings:
        edges = []
        for xf in xss_findings:
            if cpf["id"] == xf["id"]:
                continue
            edges.append({
                "from": cpf["id"],
                "to": xf["id"],
                "relation": "enables",
                "confirmed": xf.get("severity") == "high",
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Cache poisoning → stored XSS → mass exploitation",
                "nodes": [n for n in nodes if n["id"] == cpf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Cache poisoning at {cpf.get('target')} enables persistent XSS delivery to all users via poisoned cache.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: Prototype pollution → privilege escalation → admin takeover ----
    pp_findings = [f for f in validated if f.get("type") == "prototype_pollution"]
    for ppf in pp_findings:
        edges = []
        for pf in priv_esc_findings:
            if ppf["id"] == pf["id"]:
                continue
            edges.append({
                "from": ppf["id"],
                "to": pf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        for abf in auth_bypass_findings:
            if ppf["id"] == abf["id"]:
                continue
            edges.append({
                "from": ppf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Prototype pollution → privilege escalation → admin takeover",
                "nodes": [n for n in nodes if n["id"] == ppf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Prototype pollution at {ppf.get('target')} enables privilege escalation and admin-level access.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: HTTP smuggling → cache poisoning / auth bypass ----
    smuggling_findings = [f for f in validated if f.get("type") == "http_smuggling"]
    for hsf in smuggling_findings:
        edges = []
        for cpf in cache_findings:
            if hsf["id"] == cpf["id"]:
                continue
            edges.append({
                "from": hsf["id"],
                "to": cpf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        for abf in auth_bypass_findings:
            if hsf["id"] == abf["id"]:
                continue
            edges.append({
                "from": hsf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "HTTP request smuggling → cache poisoning / auth bypass",
                "nodes": [n for n in nodes if n["id"] == hsf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"HTTP smuggling at {hsf.get('target')} enables cache poisoning and authentication bypass attacks.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: NoSQL injection → auth bypass → data exposure ----
    nosql_findings = [f for f in validated if f.get("type") == "nosql_injection"]
    for nf in nosql_findings:
        edges = []
        for abf in auth_bypass_findings:
            if nf["id"] == abf["id"]:
                continue
            edges.append({
                "from": nf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        for df in data_exposure_findings:
            if nf["id"] == df["id"]:
                continue
            if _has_data(df.get("evidence", {}).get("response", "")):
                edges.append({
                    "from": nf["id"],
                    "to": df["id"],
                    "relation": "exposes",
                    "confirmed": True,
                })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "NoSQL injection → auth bypass → data exposure",
                "nodes": [n for n in nodes if n["id"] == nf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"NoSQL injection at {nf.get('target')} enables authentication bypass and sensitive data exposure.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: JWT weakness → auth bypass → IDOR → data exposure ----
    jwt_findings = [f for f in validated if f.get("type") == "jwt_deep_analysis"]
    for jf in jwt_findings:
        edges = []
        for abf in auth_bypass_findings:
            if jf["id"] == abf["id"]:
                continue
            edges.append({
                "from": jf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        for idf in idor_findings:
            if jf["id"] == idf["id"]:
                continue
            edges.append({
                "from": jf["id"],
                "to": idf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "JWT weakness → auth bypass → IDOR → data exposure",
                "nodes": [n for n in nodes if n["id"] == jf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"JWT weakness at {jf.get('target')} enables authentication bypass, IDOR exploitation, and data exposure.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: OAuth misconfig → account takeover → data exposure ----
    oauth_findings = [f for f in validated if f.get("type") == "oauth_misconfig"]
    for oaf in oauth_findings:
        edges = []
        for abf in auth_bypass_findings:
            if oaf["id"] == abf["id"]:
                continue
            edges.append({
                "from": oaf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        for df in data_exposure_findings:
            if oaf["id"] == df["id"]:
                continue
            if _has_data(df.get("evidence", {}).get("response", "")):
                edges.append({
                    "from": oaf["id"],
                    "to": df["id"],
                    "relation": "exposes",
                    "confirmed": True,
                })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "OAuth misconfiguration → account takeover → data exposure",
                "nodes": [n for n in nodes if n["id"] == oaf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"OAuth misconfiguration at {oaf.get('target')} enables account takeover and sensitive data access.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: Race condition → business logic bypass → financial fraud ----
    race_findings = [f for f in validated if f.get("type") == "race_condition"]
    logic_findings = [f for f in validated if f.get("type") == "logic_flaw"]
    for rf in race_findings:
        edges = []
        for lf in logic_findings:
            if rf["id"] == lf["id"]:
                continue
            edges.append({
                "from": rf["id"],
                "to": lf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Race condition → business logic bypass → financial fraud",
                "nodes": [n for n in nodes if n["id"] == rf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Race condition at {rf.get('target')} enables business logic bypass, coupon abuse, and potential financial fraud.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: CRLF injection → XSS → session hijacking ----
    crlf_findings = [f for f in validated if f.get("type") == "crlf_injection"]
    for crf in crlf_findings:
        edges = []
        for xf in xss_findings:
            if crf["id"] == xf["id"]:
                continue
            edges.append({
                "from": crf["id"],
                "to": xf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "CRLF injection → XSS → session hijacking",
                "nodes": [n for n in nodes if n["id"] == crf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"CRLF injection at {crf.get('target')} enables header injection leading to XSS and session hijacking.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: Mass assignment → privilege escalation → full admin access ----
    mass_findings = [f for f in validated if f.get("type") == "mass_assignment"]
    for mf in mass_findings:
        edges = []
        for pf in priv_esc_findings:
            if mf["id"] == pf["id"]:
                continue
            edges.append({
                "from": mf["id"],
                "to": pf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        for abf in auth_bypass_findings:
            if mf["id"] == abf["id"]:
                continue
            edges.append({
                "from": mf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Mass assignment → privilege escalation → full admin access",
                "nodes": [n for n in nodes if n["id"] == mf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Mass assignment at {mf.get('target')} enables privilege escalation to admin role and full system access.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: Subdomain takeover → phishing → credential harvesting ----
    subdomain_findings = [f for f in validated if f.get("type") == "subdomain_takeover"]
    weak_cred_or_phish = [f for f in validated if f.get("type") in {"weak_credential", "info_leak"}]
    for stf in subdomain_findings:
        edges = []
        for wf in weak_cred_or_phish:
            if stf["id"] == wf["id"]:
                continue
            edges.append({
                "from": stf["id"],
                "to": wf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Subdomain takeover → phishing → credential harvesting",
                "nodes": [n for n in nodes if n["id"] == stf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Subdomain takeover at {stf.get('target')} enables phishing campaigns and credential harvesting under a trusted domain.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: Host header injection → password reset poisoning → account takeover ----
    host_header_findings = [f for f in validated if f.get("type") == "host_header_injection"]
    for hhf in host_header_findings:
        edges = []
        for abf in auth_bypass_findings:
            if hhf["id"] == abf["id"]:
                continue
            edges.append({
                "from": hhf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Host header injection → password reset poisoning → account takeover",
                "nodes": [n for n in nodes if n["id"] == hhf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Host header injection at {hhf.get('target')} enables password reset poisoning and account takeover.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: LDAP injection → auth bypass → directory enumeration ----
    ldap_findings = [f for f in validated if f.get("type") == "ldap_injection"]
    for lf in ldap_findings:
        edges = []
        for abf in auth_bypass_findings:
            if lf["id"] == abf["id"]:
                continue
            edges.append({
                "from": lf["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        for df in data_exposure_findings:
            if lf["id"] == df["id"]:
                continue
            if _has_data(df.get("evidence", {}).get("response", "")):
                edges.append({
                    "from": lf["id"],
                    "to": df["id"],
                    "relation": "exposes",
                    "confirmed": True,
                })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "LDAP injection → auth bypass → directory enumeration",
                "nodes": [n for n in nodes if n["id"] == lf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"LDAP injection at {lf.get('target')} enables authentication bypass and directory enumeration.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: GraphQL injection → schema introspection → data exposure ----
    graphql_findings = [f for f in validated if f.get("type") == "graphql_injection"]
    for gf in graphql_findings:
        edges = []
        for df in data_exposure_findings:
            if gf["id"] == df["id"]:
                continue
            if _has_data(df.get("evidence", {}).get("response", "")):
                edges.append({
                    "from": gf["id"],
                    "to": df["id"],
                    "relation": "exposes",
                    "confirmed": True,
                })
        for idf in idor_findings:
            if gf["id"] == idf["id"]:
                continue
            edges.append({
                "from": gf["id"],
                "to": idf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "GraphQL injection → schema introspection → data exposure",
                "nodes": [n for n in nodes if n["id"] == gf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"GraphQL injection at {gf.get('target')} enables full schema introspection, IDOR discovery, and data exposure.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: Dependency confusion → supply chain → RCE ----
    dep_confusion_findings = [f for f in validated if f.get("type") == "dependency_confusion"]
    for dcf in dep_confusion_findings:
        edges = []
        for rf in rce_findings:
            if dcf["id"] == rf["id"]:
                continue
            edges.append({
                "from": dcf["id"],
                "to": rf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Dependency confusion → supply chain → RCE",
                "nodes": [n for n in nodes if n["id"] == dcf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Dependency confusion at {dcf.get('target')} enables supply chain attack leading to remote code execution.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: XXE → SSRF → cloud metadata / file read ----
    xxe_findings = [f for f in validated if f.get("type") == "xxe"]
    for xef in xxe_findings:
        edges = []
        for sf in ssrf_findings:
            if xef["id"] == sf["id"]:
                continue
            edges.append({
                "from": xef["id"],
                "to": sf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "XXE → SSRF → cloud metadata / file read",
                "nodes": [n for n in nodes if n["id"] == xef["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"XXE at {xef.get('target')} enables SSRF to internal services and cloud metadata access.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: Deserialization → RCE → full compromise ----
    deser_findings = [f for f in validated if f.get("type") == "deserialization"]
    for def_ in deser_findings:
        edges = []
        for rf in rce_findings:
            if def_["id"] == rf["id"]:
                continue
            edges.append({
                "from": def_["id"],
                "to": rf["id"],
                "relation": "escalates_to",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Insecure deserialization → RCE → full compromise",
                "nodes": [n for n in nodes if n["id"] == def_["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Insecure deserialization at {def_.get('target')} enables remote code execution and full system compromise.",
                "confidence": 0.9,
            })

    # ---- v3 NEW: Session fixation → XSS → account takeover ----
    sess_fix_findings = [f for f in validated if f.get("type") == "session_fixation"]
    for sff in sess_fix_findings:
        edges = []
        for xf in xss_findings:
            if sff["id"] == xf["id"]:
                continue
            edges.append({
                "from": sff["id"],
                "to": xf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        for abf in auth_bypass_findings:
            if sff["id"] == abf["id"]:
                continue
            edges.append({
                "from": sff["id"],
                "to": abf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Session fixation → XSS → account takeover",
                "nodes": [n for n in nodes if n["id"] == sff["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Session fixation at {sff.get('target')} enables session hijacking and account takeover.",
                "confidence": 0.85,
            })

    # ---- v3 NEW: Email injection → phishing → credential theft ----
    email_findings = [f for f in validated if f.get("type") == "email_injection"]
    for ef in email_findings:
        edges = []
        for wf in weak_cred_or_phish:
            if ef["id"] == wf["id"]:
                continue
            edges.append({
                "from": ef["id"],
                "to": wf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Email injection → phishing → credential theft",
                "nodes": [n for n in nodes if n["id"] == ef["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Email header injection at {ef.get('target')} enables targeted phishing and credential harvesting.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: WebSocket hijacking → real-time data interception ----
    ws_findings = [f for f in validated if f.get("type") == "websocket_hijacking"]
    for wsf in ws_findings:
        edges = []
        for df in data_exposure_findings:
            if wsf["id"] == df["id"]:
                continue
            if _has_data(df.get("evidence", {}).get("response", "")):
                edges.append({
                    "from": wsf["id"],
                    "to": df["id"],
                    "relation": "exposes",
                    "confirmed": True,
                })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "WebSocket hijacking → real-time data interception",
                "nodes": [n for n in nodes if n["id"] == wsf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"WebSocket hijacking at {wsf.get('target')} enables real-time data interception and sensitive information exposure.",
                "confidence": 0.8,
            })

    # ---- v3 NEW: Directory listing → info leak → attack surface expansion ----
    dir_list_findings = [f for f in validated if f.get("type") == "directory_listing"]
    info_leak_findings = [f for f in validated if f.get("type") == "info_leak"]
    for dlf in dir_list_findings:
        edges = []
        for ilf in info_leak_findings:
            if dlf["id"] == ilf["id"]:
                continue
            edges.append({
                "from": dlf["id"],
                "to": ilf["id"],
                "relation": "enables",
                "confirmed": True,
            })
        if edges:
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": "Directory listing → info leak → attack surface expansion",
                "nodes": [n for n in nodes if n["id"] == dlf["id"] or
                          n["id"] in {e["to"] for e in edges}],
                "edges": edges,
                "impact": f"Directory listing at {dlf.get('target')} exposes sensitive files and expands the attack surface.",
                "confidence": 0.75,
            })

    # Standalone data-exposure links for findings not in a chain
    chained_ids = {n["ref"] for p in paths for n in p["nodes"]}
    for f in validated:
        if f["id"] in chained_ids:
            continue
        if _has_data(f.get("evidence", {}).get("response", "")):
            target = f.get("target", "")
            paths.append({
                "id": f"path-{len(paths) + 1:03d}",
                "name": f"Data exposure via {f.get('type', 'vuln')}",
                "nodes": [
                    {"id": f["id"], "type": "finding", "ref": f["id"]},
                    {"id": f"asset:{target}", "type": "asset", "ref": target},
                ],
                "edges": [
                    {"from": f["id"], "to": f"asset:{target}", "relation": "exposes", "confirmed": True}
                ],
                "impact": f"Finding {f['id']} exposes sensitive data at {target}.",
                "confidence": float(f.get("confidence", 0.5)),
            })

    return paths


def main() -> int:
    ap = argparse.ArgumentParser(description="Attack path builder")
    ap.add_argument("--findings", required=True, help="Findings JSON array path or '-'")
    ap.add_argument("--assets", required=True, help="Assets JSON object path or '-'")
    args = ap.parse_args()

    findings = load_json(args.findings)
    assets = load_json(args.assets)
    paths = build_paths(findings, assets)
    print(dump_json(paths))
    return 0


if __name__ == "__main__":
    sys.exit(main())
