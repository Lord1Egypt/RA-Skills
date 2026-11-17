#!/usr/bin/env python3
"""API Security Auditor — GraphQL, REST, WebSocket security testing (v3.0.0).

Comprehensive API security auditing beyond basic endpoint discovery:
  1. GraphQL: introspection, query depth analysis, batching attack, field
     suggestion, persisted queries, subscription abuse
  2. REST: API versioning issues, mass assignment detection, method override,
     content-type confusion, excessive data exposure, rate limiting detection
  3. WebSocket: origin validation, authentication bypass, message injection,
     CSWSH (Cross-Site WebSocket Hijacking)
  4. OpenAPI/Swagger: schema analysis, undocumented endpoints, parameter
     tampering based on schema
  5. API key leakage: patterns in API responses, header/cookie analysis

This module is deterministic: it takes API endpoint data and returns
a structured audit plan. The agent executes the plan.

Usage (CLI):
  python api_auditor.py --endpoints endpoints.json --mode graphql
  python api_auditor.py --endpoints endpoints.json --mode rest
  python api_auditor.py --endpoints endpoints.json --mode websocket
  python api_auditor.py --endpoints endpoints.json --mode all
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


# =============================================================================
# GraphQL Audit Payloads
# =============================================================================
GRAPHQL_INTROSPECTION_QUERY = """
query IntrospectionQuery {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      ...FullType
    }
    directives {
      name
      description
      locations
      args {
        ...InputValue
      }
    }
  }
}
fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}
fragment InputValue on __InputValue {
  name
  description
  type { ...TypeRef }
  defaultValue
}
fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
          }
        }
      }
    }
  }
}
"""

GRAPHQL_ATTACK_PAYLOADS = {
    "batching": {
        "description": "Send multiple queries in one request to bypass rate limiting",
        "payload": [
            {"query": "query { __typename }"},
            {"query": "query { __typename }"},
            {"query": "query { __typename }"},
        ],
        "signal": "All 3 queries resolve (rate limit bypassed)",
    },
    "alias_based": {
        "description": "Use aliases to repeat the same query many times",
        "payload": "query { a1:__typename a2:__typename a3:__typename a4:__typename a5:__typename a6:__typename a7:__typename a8:__typename a9:__typename a10:__typename }",
        "signal": "All 10 aliases resolve (alias-based rate limit bypass)",
    },
    "deep_recursion": {
        "description": "Test circular query depth limit",
        "payload": "query { __type(name: \"Query\") { fields { type { fields { type { fields { type { fields { type { fields { name } } } } } } } } } }",
        "signal": "Query accepted (no depth limit) or 400 with depth error",
    },
    "field_suggestion": {
        "description": "Send malformed query to trigger field suggestions",
        "payload": "query { usser { id } }",
        "signal": "Error message suggests correct field name 'user'",
    },
    "field_duplication": {
        "description": "Duplicate the same field to test resource exhaustion",
        "payload": "query { __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename __typename }",
        "signal": "Query accepted with many duplicate fields",
    },
    "directive_overloading": {
        "description": "Test custom directive abuse",
        "payload": "query { __typename @skip(if: false) @include(if: true) @skip(if: false) @include(if: true) }",
        "signal": "Query accepted with many directives",
    },
    "array_based": {
        "description": "Test array-based query injection",
        "payload": "query { user(id: [1, 2, 3, 4, 5]) { id email } }",
        "signal": "Batch user extraction via array argument",
    },
}

GRAPHQL_PROBE_PATHS = [
    "/graphql", "/gql", "/api/graphql", "/v1/graphql", "/v2/graphql",
    "/graphiql", "/playground", "/graphql/console", "/api/graphql/console",
    "/query", "/api/query", "/graphql.php", "/graphql.jsp",
]


# =============================================================================
# REST API Audit Payloads
# =============================================================================
REST_AUDIT_CHECKS = {
    "method_override": {
        "description": "Test HTTP method override (X-HTTP-Method-Override, _method param)",
        "headers": [
            {"X-HTTP-Method-Override": "DELETE"},
            {"X-HTTP-Method": "DELETE"},
            {"X-Method-Override": "DELETE"},
        ],
        "params": [{"_method": "DELETE"}, {"_method": "PUT"}],
        "signal": "Request treated as DELETE/PUT instead of original method",
    },
    "content_type_confusion": {
        "description": "Test content-type switching between JSON/XML/form",
        "payloads": [
            {"content_type": "application/xml", "body": "<root><role>admin</role></root>"},
            {"content_type": "text/xml", "body": "<?xml version=\"1.0\"?><user><role>admin</role></user>"},
            {"content_type": "application/x-www-form-urlencoded", "body": "role=admin&is_admin=true"},
        ],
        "signal": "Same data accepted in different content type",
    },
    "versioning_issues": {
        "description": "Test API versioning for deprecated/unauth endpoints",
        "paths": [],
        "signal": "Deprecated v1 endpoint exposes data without auth",
    },
    "excessive_data_exposure": {
        "description": "Test if API returns more data than needed",
        "checks": [
            "Check if GET /users returns password hashes",
            "Check if GET /profile returns internal IDs/roles",
            "Check if response includes debug info or stack traces",
        ],
        "signal": "Sensitive fields in response (password, token, secret, internal_id)",
    },
    "rate_limiting": {
        "description": "Test API rate limiting",
        "requests": 20,
        "interval_ms": 100,
        "signal": ">50% of requests return 200 (no rate limit applied)",
    },
    "pagination_abuse": {
        "description": "Test pagination for data enumeration",
        "params": [
            {"limit": 999999, "offset": 0},
            {"page": 999999, "size": 999999},
            {"per_page": 999999},
        ],
        "signal": "Large response returned (all data exposed)",
    },
    "filter_injection": {
        "description": "Test filter parameter injection",
        "params": [
            {"filter": '{"$where": "1==1"}'},
            {"filter": '{"$gt": ""}'},
            {"filter": "1=1"},
            {"q": "' OR '1'='1"},
        ],
        "signal": "Filter injection bypasses access control",
    },
    "json_parameter_pollution": {
        "description": "Test JSON parameter pollution (duplicate keys)",
        "payload": '{"user":"attacker","user":"admin"}',
        "signal": "Second key value accepted (parameter pollution)",
    },
}

# =============================================================================
# WebSocket Audit Payloads
# =============================================================================
WEBSOCKET_AUDIT_CHECKS = {
    "origin_spoofing": {
        "description": "Test WebSocket origin validation",
        "origins": ["null", "https://attacker.evil.test", "https://target.test.attacker.evil.test"],
        "signal": "WebSocket handshake accepted with spoofed origin",
    },
    "no_authentication": {
        "description": "Test WebSocket without authentication",
        "signal": "WebSocket connection accepted without auth cookies/tokens",
    },
    "plaintext_ws": {
        "description": "Check if ws:// is used instead of wss://",
        "signal": "WebSocket on plaintext ws:// (not encrypted)",
    },
    "message_injection": {
        "description": "Test WebSocket message injection",
        "payloads": [
            '{"type":"admin","action":"delete"}',
            '{"type":"broadcast","message":"<script>alert(1)</script>"}',
            '{"__proto__":{"isAdmin":true}}',
        ],
        "signal": "Injected message accepted by server",
    },
}

# =============================================================================
# API Key Leakage Patterns
# =============================================================================
API_KEY_PATTERNS = {
    "bearer_token": r"Bearer\s+([a-zA-Z0-9\-_.]+=*)",
    "api_key_header": r"(?i)x-api-key\s*:\s*([^\s]+)",
    "url_embedded_key": r"[?&](?:api_key|apikey|token|access_token|auth)=([^&\s]+)",
    "json_key": r'(?i)"(?:api_?key|apikey|access_?token|auth_?token|secret)"\s*:\s*"([^"]+)"',
}


def build_graphql_audit_plan(endpoints: list[dict]) -> dict:
    """Build GraphQL security audit plan."""
    # Find GraphQL endpoints
    gql_endpoints = []
    for ep in endpoints:
        url = ep.get("url", "")
        if any(path in url.lower() for path in GRAPHQL_PROBE_PATHS):
            gql_endpoints.append(ep)

    if not gql_endpoints:
        # Probe for GraphQL endpoints
        gql_endpoints = [{"url": p, "methods": ["POST"]} for p in GRAPHQL_PROBE_PATHS[:5]]

    tests = []

    # 1. Introspection test
    for ep in gql_endpoints:
        tests.append({
            "test": "introspection",
            "endpoint": ep.get("url", ""),
            "method": "POST",
            "payload": {"query": GRAPHQL_INTROSPECTION_QUERY.strip()},
            "signal": "Full schema returned in response",
            "severity": "low",
        })

    # 2. Attack payloads
    for name, config in GRAPHQL_ATTACK_PAYLOADS.items():
        for ep in gql_endpoints:
            payload = config["payload"]
            if isinstance(payload, list):
                # Batch query
                payload = json.dumps(payload)
            elif isinstance(payload, dict):
                payload = json.dumps(payload)
            tests.append({
                "test": name,
                "endpoint": ep.get("url", ""),
                "method": "POST",
                "payload": payload,
                "signal": config["signal"],
                "severity": "high" if name in ("deep_recursion", "array_based") else "medium",
            })

    return {
        "api_type": "graphql",
        "endpoints_found": len(gql_endpoints),
        "test_count": len(tests),
        "tests": tests,
    }


def build_rest_audit_plan(endpoints: list[dict]) -> dict:
    """Build REST API security audit plan."""
    tests = []
    state_changing = [ep for ep in endpoints if any(m in (ep.get("methods", [])) for m in ["POST", "PUT", "PATCH", "DELETE"])]
    all_eps = endpoints if endpoints else [{"url": "/", "methods": ["GET"]}]

    for ep in state_changing or all_eps:
        url = ep.get("url", "")

        # Method override tests
        if "method_override" in REST_AUDIT_CHECKS:
            for header in REST_AUDIT_CHECKS["method_override"]["headers"]:
                tests.append({
                    "test": "method_override_header",
                    "endpoint": url,
                    "method": "POST",
                    "header": header,
                    "signal": REST_AUDIT_CHECKS["method_override"]["signal"],
                    "severity": "high",
                })

        # Content-Type confusion
        for payload in REST_AUDIT_CHECKS["content_type_confusion"]["payloads"]:
            tests.append({
                "test": "content_type_confusion",
                "endpoint": url,
                "method": "POST",
                "content_type": payload["content_type"],
                "body": payload["body"],
                "signal": REST_AUDIT_CHECKS["content_type_confusion"]["signal"],
                "severity": "medium",
            })

        # Filter injection
        for param in REST_AUDIT_CHECKS["filter_injection"]["params"]:
            tests.append({
                "test": "filter_injection",
                "endpoint": url,
                "method": "GET",
                "params": param,
                "signal": REST_AUDIT_CHECKS["filter_injection"]["signal"],
                "severity": "high",
            })

        # Pagination abuse
        for param in REST_AUDIT_CHECKS["pagination_abuse"]["params"]:
            tests.append({
                "test": "pagination_abuse",
                "endpoint": url,
                "method": "GET",
                "params": param,
                "signal": REST_AUDIT_CHECKS["pagination_abuse"]["signal"],
                "severity": "medium",
            })

    # Rate limiting test
    if all_eps:
        tests.append({
            "test": "rate_limiting",
            "endpoint": all_eps[0].get("url", ""),
            "method": "GET",
            "requests": REST_AUDIT_CHECKS["rate_limiting"]["requests"],
            "interval_ms": REST_AUDIT_CHECKS["rate_limiting"]["interval_ms"],
            "signal": REST_AUDIT_CHECKS["rate_limiting"]["signal"],
            "severity": "medium",
        })

    # JSON parameter pollution
    for ep in state_changing or all_eps[:1]:
        tests.append({
            "test": "json_parameter_pollution",
            "endpoint": ep.get("url", ""),
            "method": "POST",
            "body": REST_AUDIT_CHECKS["json_parameter_pollution"]["payload"],
            "content_type": "application/json",
            "signal": REST_AUDIT_CHECKS["json_parameter_pollution"]["signal"],
            "severity": "high",
        })

    # Excessive data exposure
    for ep in all_eps[:3]:
        tests.append({
            "test": "excessive_data_exposure",
            "endpoint": ep.get("url", ""),
            "method": "GET",
            "signal": REST_AUDIT_CHECKS["excessive_data_exposure"]["signal"],
            "severity": "high",
            "checks": REST_AUDIT_CHECKS["excessive_data_exposure"]["checks"],
        })

    return {
        "api_type": "rest",
        "endpoints_found": len(endpoints),
        "state_changing_endpoints": len(state_changing),
        "test_count": len(tests),
        "tests": tests,
    }


def build_websocket_audit_plan(endpoints: list[dict]) -> dict:
    """Build WebSocket security audit plan."""
    ws_endpoints = [ep for ep in endpoints if "ws://" in ep.get("url", "").lower() or "wss://" in ep.get("url", "").lower()]

    if not ws_endpoints:
        ws_endpoints = [{"url": "ws://target.test/ws"}, {"url": "wss://target.test/ws"}]

    tests = []

    for ep in ws_endpoints:
        url = ep.get("url", "")

        # Origin spoofing
        for origin in WEBSOCKET_AUDIT_CHECKS["origin_spoofing"]["origins"]:
            tests.append({
                "test": "origin_spoofing",
                "endpoint": url,
                "origin": origin,
                "signal": WEBSOCKET_AUDIT_CHECKS["origin_spoofing"]["signal"],
                "severity": "medium",
            })

        # No auth
        tests.append({
            "test": "no_authentication",
            "endpoint": url,
            "signal": WEBSOCKET_AUDIT_CHECKS["no_authentication"]["signal"],
            "severity": "high",
        })

        # Plaintext WS
        if url.startswith("ws://"):
            tests.append({
                "test": "plaintext_ws",
                "endpoint": url,
                "signal": WEBSOCKET_AUDIT_CHECKS["plaintext_ws"]["signal"],
                "severity": "medium",
            })

        # Message injection
        for payload in WEBSOCKET_AUDIT_CHECKS["message_injection"]["payloads"]:
            tests.append({
                "test": "message_injection",
                "endpoint": url,
                "payload": payload,
                "signal": WEBSOCKET_AUDIT_CHECKS["message_injection"]["signal"],
                "severity": "high",
            })

    return {
        "api_type": "websocket",
        "endpoints_found": len(ws_endpoints),
        "test_count": len(tests),
        "tests": tests,
    }


def scan_api_keys(response_body: str) -> list[dict]:
    """Scan response body for leaked API keys and tokens."""
    findings = []
    for name, pattern in API_KEY_PATTERNS.items():
        for m in re.finditer(pattern, response_body):
            findings.append({
                "type": "api_key_leak",
                "pattern": name,
                "match": m.group(0)[:80] + "..." if len(m.group(0)) > 80 else m.group(0),
                "severity": "high",
            })
    return findings


def audit(endpoints: list[dict], mode: str) -> dict:
    """Run API security audit for the given mode.

    Args:
        endpoints: list of endpoint dicts from recon.
        mode: graphql | rest | websocket | all

    Returns:
        Audit plan dict with tests.
    """
    results = {}

    if mode in ("graphql", "all"):
        results["graphql"] = build_graphql_audit_plan(endpoints)

    if mode in ("rest", "all"):
        results["rest"] = build_rest_audit_plan(endpoints)

    if mode in ("websocket", "all"):
        results["websocket"] = build_websocket_audit_plan(endpoints)

    if mode not in ("graphql", "rest", "websocket", "all"):
        return {"error": f"unknown mode: {mode}", "supported": ["graphql", "rest", "websocket", "all"]}

    total_tests = sum(r.get("test_count", 0) for r in results.values())
    results["summary"] = {
        "total_endpoints": len(endpoints),
        "total_tests": total_tests,
        "modes_audited": list(results.keys()),
    }

    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="API Security Auditor (v3.0)")
    ap.add_argument("--endpoints", required=True, help="Endpoints JSON (path or '-')")
    ap.add_argument("--mode", default="all", choices=["graphql", "rest", "websocket", "all"],
                    help="Audit mode")
    ap.add_argument("--scan-keys", help="Response body to scan for API keys")
    args = ap.parse_args()

    if args.scan_keys:
        findings = scan_api_keys(args.scan_keys)
        print(dump_json({"api_key_scan": {"findings": findings, "count": len(findings)}}))
        return 0

    endpoints = load_json(args.endpoints)
    if isinstance(endpoints, dict):
        endpoints = endpoints.get("endpoints", [])
    result = audit(endpoints, args.mode)
    print(dump_json(result))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())