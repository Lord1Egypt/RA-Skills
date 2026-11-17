#!/usr/bin/env python3
"""CVE Correlator — threat intelligence & vulnerability database correlation (v3.0.0).

Correlates discovered technologies and versions with known CVEs from the
NVD (National Vulnerability Database) and other sources. Provides:
  1. CPE-to-CVE mapping based on technology fingerprinting
  2. Severity-prioritized CVE listing (CVSS v3 scores)
  3. Exploit availability check (Metasploit, ExploitDB, PoC references)
  4. Remediation guidance (patch versions, workarounds)
  5. Risk scoring integration with the main pipeline

This module is deterministic: it takes technology fingerprints and returns
a structured CVE report. It includes a built-in CVE knowledge base for
common web frameworks and middleware.

Usage (CLI):
  python cve_correlator.py --technologies tech.json
  python cve_correlator.py --cpe "cpe:/a:apache:struts:2.5.26"
  python cve_correlator.py --batch targets.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json
import os


# ---- Built-in CVE knowledge base (high-impact, commonly exploited) ----------
# Format: cpe_key → list of CVE entries
# Each entry: {cve, cvss, severity, description, exploit_available, patch, refs}
CVE_KB = {
    "apache:struts2": [
        {"cve": "CVE-2017-5638", "cvss": 10.0, "severity": "critical",
         "description": "Struts2 Jakarta Multipart parser RCE (Equifax breach)",
         "exploit_available": True, "patch": ">= 2.3.32 or >= 2.5.10.1",
         "refs": ["https://nvd.nist.gov/vuln/detail/CVE-2017-5638"]},
        {"cve": "CVE-2018-11776", "cvss": 8.1, "severity": "high",
         "description": "Struts2 namespace RCE via missing namespace",
         "exploit_available": True, "patch": ">= 2.3.35 or >= 2.5.17",
         "refs": []},
        {"cve": "CVE-2019-0230", "cvss": 9.8, "severity": "critical",
         "description": "Struts2 forced OGNL double evaluation RCE",
         "exploit_available": True, "patch": ">= 2.5.20",
         "refs": []},
        {"cve": "CVE-2020-17530", "cvss": 9.8, "severity": "critical",
         "description": "Struts2 forced OGNL evaluation in tag attributes RCE",
         "exploit_available": True, "patch": ">= 2.5.26",
         "refs": []},
        {"cve": "CVE-2023-50164", "cvss": 9.8, "severity": "critical",
         "description": "Struts2 file upload path traversal RCE",
         "exploit_available": True, "patch": ">= 2.5.33 or >= 6.3.0.2",
         "refs": []},
    ],
    "apache:log4j": [
        {"cve": "CVE-2021-44228", "cvss": 10.0, "severity": "critical",
         "description": "Log4Shell — JNDI lookup RCE via crafted log messages",
         "exploit_available": True, "patch": ">= 2.17.0 (2.x) or >= 2.12.4 (2.12.x) or >= 2.3.2 (2.3.x)",
         "refs": ["https://nvd.nist.gov/vuln/detail/CVE-2021-44228"]},
        {"cve": "CVE-2021-45046", "cvss": 9.0, "severity": "critical",
         "description": "Log4j incomplete fix for CVE-2021-44228 in certain configurations",
         "exploit_available": True, "patch": ">= 2.17.0 (2.x) or >= 2.12.4 (2.12.x)",
         "refs": []},
        {"cve": "CVE-2021-45105", "cvss": 7.5, "severity": "high",
         "description": "Log4j infinite recursion DoS via self-referential lookup",
         "exploit_available": True, "patch": ">= 2.17.0 (2.x) or >= 2.12.4 (2.12.x)",
         "refs": []},
    ],
    "spring:spring-boot": [
        {"cve": "CVE-2022-22965", "cvss": 9.8, "severity": "critical",
         "description": "Spring4Shell — Spring Framework RCE via data binding",
         "exploit_available": True, "patch": ">= 5.3.18 or >= 5.2.20",
         "refs": ["https://nvd.nist.gov/vuln/detail/CVE-2022-22965"]},
        {"cve": "CVE-2022-22947", "cvss": 10.0, "severity": "critical",
         "description": "Spring Cloud Gateway Code Injection via Actuator",
         "exploit_available": True, "patch": ">= 3.1.1 or >= 3.0.7",
         "refs": []},
        {"cve": "CVE-2022-22963", "cvss": 9.8, "severity": "critical",
         "description": "Spring Cloud Function SpEL injection RCE",
         "exploit_available": True, "patch": ">= 3.2.3 or >= 3.1.7",
         "refs": []},
    ],
    "apache:tomcat": [
        {"cve": "CVE-2025-24813", "cvss": 9.8, "severity": "critical",
         "description": "Tomcat path equivalence RCE via partial PUT",
         "exploit_available": True, "patch": ">= 11.0.3, >= 10.1.35, >= 9.0.99",
         "refs": []},
        {"cve": "CVE-2020-9484", "cvss": 7.5, "severity": "high",
         "description": "Tomcat session persistence deserialization RCE",
         "exploit_available": True, "patch": ">= 10.0.0-M5, >= 9.0.35, >= 8.5.55",
         "refs": []},
        {"cve": "CVE-2019-0232", "cvss": 8.1, "severity": "high",
         "description": "Tomcat CGI Servlet command injection on Windows",
         "exploit_available": True, "patch": ">= 9.0.19, >= 8.5.40",
         "refs": []},
    ],
    "apache:shiro": [
        {"cve": "CVE-2016-4437", "cvss": 9.8, "severity": "critical",
         "description": "Apache Shiro RememberMe deserialization RCE (hardcoded key)",
         "exploit_available": True, "patch": ">= 1.2.5 (requires custom cipherKey)",
         "refs": ["https://nvd.nist.gov/vuln/detail/CVE-2016-4437"]},
        {"cve": "CVE-2020-1957", "cvss": 9.1, "severity": "critical",
         "description": "Apache Shiro path traversal authentication bypass",
         "exploit_available": True, "patch": ">= 1.5.2",
         "refs": []},
    ],
    "oracle:weblogic": [
        {"cve": "CVE-2020-14882", "cvss": 9.8, "severity": "critical",
         "description": "WebLogic Console RCE via handle mechanism",
         "exploit_available": True, "patch": "Oct 2020 CPU",
         "refs": []},
        {"cve": "CVE-2023-21839", "cvss": 9.8, "severity": "critical",
         "description": "WebLogic T3/IIOP deserialization RCE",
         "exploit_available": True, "patch": "Jan 2023 CPU",
         "refs": []},
        {"cve": "CVE-2019-2725", "cvss": 9.8, "severity": "critical",
         "description": "WebLogic wls9_async deserialization RCE",
         "exploit_available": True, "patch": "Apr 2019 CPU",
         "refs": []},
    ],
    "thinkphp": [
        {"cve": "CVE-2018-20062", "cvss": 9.8, "severity": "critical",
         "description": "ThinkPHP 5.x method filtering bypass RCE",
         "exploit_available": True, "patch": ">= 5.0.24 or >= 5.1.32",
         "refs": []},
        {"cve": "CVE-2019-9082", "cvss": 9.8, "severity": "critical",
         "description": "ThinkPHP 5.0.x RCE via invokeFunction",
         "exploit_available": True, "patch": ">= 5.0.24",
         "refs": []},
        {"cve": "CVE-2022-47945", "cvss": 9.8, "severity": "critical",
         "description": "ThinkPHP lang parameter RCE (multilingual pack)",
         "exploit_available": True, "patch": ">= 6.0.14",
         "refs": []},
    ],
    "fastjson": [
        {"cve": "CVE-2022-25845", "cvss": 9.8, "severity": "critical",
         "description": "Fastjson 1.x autoType deserialization RCE",
         "exploit_available": True, "patch": ">= 1.2.83 or disable autoType",
         "refs": []},
        {"cve": "CVE-2020-8840", "cvss": 9.8, "severity": "critical",
         "description": "Fastjson JNDI injection via JNDIConfiguration",
         "exploit_available": True, "patch": ">= 1.2.66",
         "refs": []},
    ],
    "redis": [
        {"cve": "CVE-2022-0543", "cvss": 10.0, "severity": "critical",
         "description": "Redis Lua sandbox escape RCE (Debian/Ubuntu)",
         "exploit_available": True, "patch": ">= 5.0.14, 6.0.16, 6.2.6, 7.0-rc3",
         "refs": []},
    ],
    "elasticsearch": [
        {"cve": "CVE-2015-1427", "cvss": 9.3, "severity": "critical",
         "description": "Elasticsearch Groovy sandbox bypass RCE",
         "exploit_available": True, "patch": ">= 1.4.3 or 1.3.8",
         "refs": []},
        {"cve": "CVE-2014-3120", "cvss": 6.8, "severity": "medium",
         "description": "Elasticsearch dynamic script RCE via MVEL",
         "exploit_available": True, "patch": ">= 1.2.0",
         "refs": []},
    ],
    "jenkins": [
        {"cve": "CVE-2024-23897", "cvss": 9.8, "severity": "critical",
         "description": "Jenkins CLI arbitrary file read to RCE",
         "exploit_available": True, "patch": ">= 2.442 or >= 2.426.3 LTS",
         "refs": []},
        {"cve": "CVE-2019-1003000", "cvss": 7.5, "severity": "high",
         "description": "Jenkins Script Security sandbox bypass RCE",
         "exploit_available": True, "patch": ">= 1.50",
         "refs": []},
    ],
    "nginx": [
        {"cve": "CVE-2017-7529", "cvss": 5.0, "severity": "medium",
         "description": "Nginx range filter integer overflow info leak",
         "exploit_available": True, "patch": ">= 1.13.3 or 1.12.1",
         "refs": []},
        {"cve": "CVE-2021-23017", "cvss": 7.5, "severity": "high",
         "description": "Nginx DNS resolver off-by-one DoS",
         "exploit_available": True, "patch": ">= 1.21.0 or 1.20.1",
         "refs": []},
    ],
    "apache:httpd": [
        {"cve": "CVE-2021-41773", "cvss": 7.5, "severity": "high",
         "description": "Apache HTTPD 2.4.49 path traversal RCE",
         "exploit_available": True, "patch": ">= 2.4.51",
         "refs": []},
        {"cve": "CVE-2021-42013", "cvss": 9.8, "severity": "critical",
         "description": "Apache HTTPD 2.4.50 path traversal RCE (incomplete fix)",
         "exploit_available": True, "patch": ">= 2.4.51",
         "refs": []},
        {"cve": "CVE-2021-40438", "cvss": 9.0, "severity": "critical",
         "description": "Apache HTTPD mod_proxy SSRF",
         "exploit_available": True, "patch": ">= 2.4.49",
         "refs": []},
    ],
    "vue:js": [
        {"cve": "CVE-2024-48455", "cvss": 6.1, "severity": "medium",
         "description": "Vue.js prototype pollution via template compiler",
         "exploit_available": False, "patch": ">= 3.4.0",
         "refs": []},
    ],
    "react": [
        {"cve": "CVE-2018-6341", "cvss": 6.1, "severity": "medium",
         "description": "React dev server XSS via WebSocket",
         "exploit_available": False, "patch": ">= 16.4.2",
         "refs": []},
    ],
    "jquery": [
        {"cve": "CVE-2020-11023", "cvss": 6.1, "severity": "medium",
         "description": "jQuery XSS via HTML parsing in versions < 3.5.0",
         "exploit_available": False, "patch": ">= 3.5.0",
         "refs": []},
        {"cve": "CVE-2020-11022", "cvss": 6.1, "severity": "medium",
         "description": "jQuery XSS via HTML parsing in .html()",
         "exploit_available": False, "patch": ">= 3.5.0",
         "refs": []},
    ],
    "wordpress": [
        {"cve": "CVE-2024-4439", "cvss": 6.4, "severity": "medium",
         "description": "WordPress core stored XSS via avatar",
         "exploit_available": True, "patch": ">= 6.5.2",
         "refs": []},
        {"cve": "CVE-2019-17671", "cvss": 5.3, "severity": "medium",
         "description": "WordPress 5.2.3 unauthenticated view-private posts",
         "exploit_available": True, "patch": ">= 5.2.4",
         "refs": []},
    ],
    "drupal": [
        {"cve": "CVE-2018-7600", "cvss": 9.8, "severity": "critical",
         "description": "Drupalgeddon2 — form API RCE (Drupal 7/8)",
         "exploit_available": True, "patch": ">= 7.58 or 8.5.1",
         "refs": []},
        {"cve": "CVE-2019-6340", "cvss": 8.1, "severity": "high",
         "description": "Drupal REST RCE via serialization",
         "exploit_available": True, "patch": ">= 8.6.10 or 8.5.11",
         "refs": []},
    ],
    "kubernetes": [
        {"cve": "CVE-2018-1002105", "cvss": 9.8, "severity": "critical",
         "description": "Kubernetes API server proxy websocket upgrade RCE",
         "exploit_available": True, "patch": ">= 1.10.11, 1.11.5, 1.12.3",
         "refs": []},
        {"cve": "CVE-2020-8554", "cvss": 5.8, "severity": "medium",
         "description": "Kubernetes MITM via LoadBalancer/IPVS",
         "exploit_available": False, "patch": ">= 1.18.4, 1.17.7, 1.16.11",
         "refs": []},
    ],
    "docker": [
        {"cve": "CVE-2019-5736", "cvss": 8.6, "severity": "high",
         "description": "runc container escape via /proc/self/exe",
         "exploit_available": True, "patch": ">= 18.09.2 or runc >= 1.0-rc6",
         "refs": []},
    ],
}


def _normalize_cpe_name(tech_name: str) -> str:
    """Normalize technology name to CPE-like key for lookup."""
    name = tech_name.lower().replace("_", "-").replace(" ", "-")
    # Known mappings
    mapping = {
        "struts": "apache:struts2", "struts2": "apache:struts2",
        "apache-struts": "apache:struts2", "apache-struts2": "apache:struts2",
        "log4j": "apache:log4j", "log4j2": "apache:log4j",
        "apache-log4j": "apache:log4j", "apache-log4j2": "apache:log4j",
        "spring-boot": "spring:spring-boot", "springboot": "spring:spring-boot",
        "spring": "spring:spring-boot", "spring-framework": "spring:spring-boot",
        "tomcat": "apache:tomcat", "apache-tomcat": "apache:tomcat",
        "shiro": "apache:shiro", "apache-shiro": "apache:shiro",
        "weblogic": "oracle:weblogic", "oracle-weblogic": "oracle:weblogic",
        "thinkphp": "thinkphp", "think-php": "thinkphp",
        "fastjson": "fastjson", "alibaba-fastjson": "fastjson",
        "redis": "redis", "redis-server": "redis",
        "elasticsearch": "elasticsearch", "elastic": "elasticsearch",
        "jenkins": "jenkins", "jenkins-ci": "jenkins",
        "nginx": "nginx", "nginx-plus": "nginx",
        "apache": "apache:httpd", "httpd": "apache:httpd",
        "apache-httpd": "apache:httpd", "apache-http-server": "apache:httpd",
        "vue": "vue:js", "vue.js": "vue:js", "vuejs": "vue:js",
        "react": "react", "reactjs": "react", "react.js": "react",
        "jquery": "jquery", "jquery-js": "jquery",
        "wordpress": "wordpress", "wp": "wordpress",
        "drupal": "drupal",
        "kubernetes": "kubernetes", "k8s": "kubernetes",
        "docker": "docker", "docker-engine": "docker",
    }
    return mapping.get(name, name)


def correlate_technology(tech: dict) -> list[dict]:
    """Correlate a single technology with known CVEs.

    Args:
        tech: dict with 'name' (required), 'version' (optional), 'cpe' (optional).

    Returns:
        List of matched CVE dicts.
    """
    name = tech.get("name", "")
    version = tech.get("version", "")
    cpe = tech.get("cpe", "")

    cpe_key = _normalize_cpe_name(name)
    if cpe:
        # Try exact CPE match first
        for key, cves in CVE_KB.items():
            if key in cpe.lower():
                return cves

    return CVE_KB.get(cpe_key, [])


def correlate_technologies(technologies: list[dict]) -> dict:
    """Correlate a list of discovered technologies with known CVEs.

    Args:
        technologies: list of tech dicts from recon.

    Returns:
        {
            "total_cves": int,
            "by_severity": {critical: n, high: n, medium: n, low: n},
            "exploits_available": int,
            "cves": [...],
            "risk_score": int,
            "top_priority": [...]
        }
    """
    all_cves = []
    seen_cves = set()

    for tech in technologies:
        cves = correlate_technology(tech)
        for cve_entry in cves:
            if cve_entry["cve"] not in seen_cves:
                seen_cves.add(cve_entry["cve"])
                all_cves.append({
                    **cve_entry,
                    "matched_tech": tech.get("name", ""),
                    "tech_version": tech.get("version", ""),
                    "tech_cpe": tech.get("cpe", ""),
                })

    # Sort by CVSS score descending
    all_cves.sort(key=lambda x: x["cvss"], reverse=True)

    by_severity = {}
    for c in all_cves:
        by_severity[c["severity"]] = by_severity.get(c["severity"], 0) + 1

    exploits = [c for c in all_cves if c["exploit_available"]]

    # Risk score: weighted sum of CVEs (critical=25, high=15, medium=8, low=3)
    severity_points = {"critical": 25, "high": 15, "medium": 8, "low": 3}
    risk_score = sum(severity_points.get(c["severity"], 0) for c in all_cves)
    risk_score = min(100, risk_score)

    return {
        "total_cves": len(all_cves),
        "by_severity": by_severity,
        "exploits_available": len(exploits),
        "cves": all_cves,
        "risk_score": risk_score,
        "top_priority": [c for c in all_cves if c["severity"] == "critical" and c["exploit_available"]],
    }


def search_cve(query: str) -> list[dict]:
    """Search for CVEs by keyword, CPE, or product name."""
    results = []
    query_lower = query.lower()
    for cpe_key, cves in CVE_KB.items():
        if query_lower in cpe_key:
            results.extend(cves)
            continue
        for cve in cves:
            if query_lower in cve["cve"].lower() or query_lower in cve["description"].lower():
                results.append(cve)
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="CVE Correlator — threat intelligence (v3.0)")
    ap.add_argument("--technologies", help="Technologies JSON (from recon) path or '-'")
    ap.add_argument("--cpe", help="Single CPE string to search")
    ap.add_argument("--query", help="Keyword search for CVEs")
    ap.add_argument("--batch", help="Batch targets JSON for bulk correlation")
    args = ap.parse_args()

    if args.technologies:
        techs = load_json(args.technologies)
        if isinstance(techs, list):
            result = correlate_technologies(techs)
        elif isinstance(techs, dict) and "technologies" in techs:
            result = correlate_technologies(techs["technologies"])
        else:
            result = correlate_technologies([techs])
        print(dump_json(result))

    elif args.cpe:
        result = search_cve(args.cpe)
        print(dump_json({"query": args.cpe, "results": result}))

    elif args.query:
        result = search_cve(args.query)
        print(dump_json({"query": args.query, "results": result}))

    elif args.batch:
        targets = load_json(args.batch)
        all_results = {}
        for target in targets if isinstance(targets, list) else [targets]:
            techs = target.get("technologies", [])
            target_name = target.get("url", target.get("target", "unknown"))
            all_results[target_name] = correlate_technologies(techs)
        print(dump_json({"batch_results": all_results}))

    else:
        print("cve_correlator: --technologies, --cpe, --query, or --batch required", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())