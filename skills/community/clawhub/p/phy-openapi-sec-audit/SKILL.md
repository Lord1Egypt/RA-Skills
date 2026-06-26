---
name: OpenAPI Sec Audit
description: OpenAPI/Swagger security auditor. Scans any OpenAPI 3.x or Swagger 2.0 spec (YAML or JSON) for 10 security misconfigurations — missing authentication, plaintext HTTP servers, API keys in query strings, deprecated OAuth flows, sensitive fields in responses, missing input validation, admin endpoints without auth, file upload DoS vectors, wildcard OAuth scopes, and missing 401/403 responses. Zero external dependencies beyond PyYAML. Works on local files, directories, and URLs.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - openapi
  - swagger
  - api
  - rest
  - oauth
  - authentication
  - audit
  - static-analysis
  - zero-deps
---

# phy-openapi-sec-audit — OpenAPI/Swagger Security Auditor

Scans OpenAPI 3.x and Swagger 2.0 specs for **10 security misconfigurations** that API gateways and code review typically miss. Works on local YAML/JSON files, entire directories, or public URLs. Zero external dependencies (only PyYAML for YAML parsing — stdlib JSON always works).

## Quick Start

```bash
# Single spec file
python openapi_sec_audit.py openapi.yaml

# Remote spec (public URL)
python openapi_sec_audit.py https://petstore3.swagger.io/api/v3/openapi.json

# Scan entire API directory
python openapi_sec_audit.py ./api/ --scan-dir

# CI mode — exit 1 on CRITICAL or HIGH findings
python openapi_sec_audit.py openapi.yaml --ci

# Only show HIGH and above
python openapi_sec_audit.py openapi.yaml --only-severity HIGH
```

## The 10 Security Checks

| ID | Severity | Check | CWE |
|----|----------|-------|-----|
| OS001 | HIGH | Missing authentication on endpoint | CWE-306 |
| OS002 | HIGH | Server URL uses plaintext HTTP | CWE-319 |
| OS003 | HIGH | API key passed as query parameter | CWE-598 |
| OS004 | HIGH | Deprecated OAuth2 flow (implicit/password) | CWE-287 |
| OS005 | HIGH | Sensitive field in response schema | CWE-312 |
| OS006 | MEDIUM | Write operation with no request body schema | CWE-20 |
| OS007 | LOW | Authenticated endpoint missing 401/403 response | CWE-284 |
| OS008 | CRITICAL | Admin/internal path with no auth requirement | CWE-285 |
| OS009 | MEDIUM | File upload without maxLength (DoS vector) | CWE-400 |
| OS010 | HIGH | Wildcard OAuth scope violates least privilege | CWE-272 |

### OS001 — Missing Authentication
Checks every operation against global `security:` and operation-level `security:` arrays. Skips `/health`, `/ping`, `/version`, `/status`, `/ready`, `/live` (public endpoints by convention). Flags write operations (POST/PUT/PATCH/DELETE) that explicitly opt out with `security: []`.

### OS002 — Plaintext HTTP Server
Scans `servers[].url` (OpenAPI 3.x) and `schemes:` array (Swagger 2.0). Skips localhost/127.0.0.1 — only flags production URLs.

### OS003 — API Key in Query String
Finds `securitySchemes` with `type: apiKey` and `in: query`. Query parameters appear in server logs, browser history, Referer headers, and CDN access logs — never safe for credentials.

### OS004 — Deprecated OAuth2 Flows
Detects `implicit` and `password` flows (deprecated by RFC 9700 / OAuth 2.1). Implicit flow exposes tokens in URL fragments (no PKCE possible); password flow exposes credentials directly to the client.

### OS005 — Sensitive Fields in Response Schema
Recursively walks all response schemas looking for field names matching: `password`, `passwd`, `secret`, `ssn`, `social_security`, `card_number`, `cvv`, `cvc`, `credit_card`, `private_key`, `api_key`, `access_token`, `refresh_token`, `auth_token`, `bearer`, `jwt`, `session_id`, `pin`, `otp`, `mfa_code`.

### OS006 — Missing Request Body Schema
POST/PUT/PATCH operations without a schema on `requestBody.content[*].schema` lose API gateway input validation enforcement. No schema = no automatic type checking, no maxLength enforcement.

### OS007 — Missing 401/403 Responses
Authenticated endpoints that don't define 401 or 403 responses suggest auth may not be enforced. Also prevents SDK generators from handling auth errors correctly.

### OS008 — Admin/Internal Path Without Auth (CRITICAL)
Flags paths matching `/admin`, `/internal`, `/debug`, `/_internal`, `/_debug`, `/management`, `/actuator`, `/metrics`, `/health/detail`, `/swagger-ui`, `/api-docs` that have no security requirement. These are the most exploited endpoints in API breaches.

### OS009 — File Upload Without Size Limit
`multipart/form-data` and `application/octet-stream` endpoints where binary fields lack `maxLength` or `maximum`. An unbound upload endpoint is a trivial denial-of-service vector.

### OS010 — Wildcard OAuth Scope
Detects scopes matching `*`, `admin`, `root`, `superuser`, `all`, `full`, `write:*`, `read:*` in OAuth2 flow definitions. Violates principle of least privilege — a compromised client with `*` scope has full API access.

## Sample Output

```
============================================================
  OpenAPI Security Audit — api/openapi.yaml
  Spec: OpenAPI 3.1.0
============================================================

── CRITICAL (1) ────────────────────────────────────────────
🔴 OS008 [CRITICAL] DELETE /admin/users/{id}
   Admin/internal path '/admin/users/{id}' has no authentication requirement.
   CWE: CWE-285: Improper Authorization
   Fix: Add strict authentication + scope requirement to this endpoint.

── HIGH (3) ────────────────────────────────────────────────
🟠 OS001 [HIGH] GET /invoices
   No security requirement and no global security defined.
   CWE: CWE-306: Missing Authentication for Critical Function
   Fix: Add `security: [{BearerAuth: []}]` to the operation.

🟠 OS003 [HIGH] components/securitySchemes/ApiKeyAuth
   Security scheme 'ApiKeyAuth' passes API key as query parameter.
   CWE: CWE-598: Use of GET Request Method with Sensitive Query Strings
   Fix: Change `in: query` to `in: header`.

🟠 OS005 [HIGH] POST /users → 200 application/json/password
   Response schema contains sensitive field 'password'.
   CWE: CWE-312: Cleartext Storage of Sensitive Information
   Fix: Remove 'password' from response schema or add writeOnly: true.

── MEDIUM (1) ──────────────────────────────────────────────
🟡 OS006 [MEDIUM] POST /documents
   POST endpoint has no requestBody or body parameter defined.
   CWE: CWE-20: Improper Input Validation
   Fix: Add requestBody with schema.

────────────────────────────────────────────────────────────
  Total: 5 findings
  Critical: 1 | High: 3 | Medium: 1 | Low: 0

  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.
```

## CI Integration

```yaml
# GitHub Actions
- name: OpenAPI Security Audit
  run: |
    python openapi_sec_audit.py openapi.yaml --ci
  # Fails the build on CRITICAL or HIGH findings

# GitLab CI
openapi-security:
  script:
    - python openapi_sec_audit.py api/ --scan-dir --ci
  allow_failure: false
```

## Installation

```bash
# Install into current project
cp openapi_sec_audit.py ./scripts/

# Optional: YAML support (JSON specs work without it)
pip install pyyaml

# Alias
alias openapi-sec='python /path/to/openapi_sec_audit.py'
```

## The Script

```python
#!/usr/bin/env python3
"""
phy-openapi-sec-audit — OpenAPI/Swagger Security Auditor
Scans OpenAPI 3.x (YAML/JSON) and Swagger 2.0 specs for 10 security misconfigurations.
Zero external dependencies beyond PyYAML (stdlib JSON always works).
"""

import sys
import json
import re
import os
from dataclasses import dataclass, field
from typing import Any, Optional
from pathlib import Path


# ─── Data Structures ─────────────────────────────────────────────────────────

@dataclass
class Finding:
    check_id: str
    severity: str        # CRITICAL / HIGH / MEDIUM / LOW
    path: str            # OpenAPI path (e.g. GET /users/{id})
    message: str
    cwe: str = ""
    fix: str = ""

    def __str__(self) -> str:
        icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🔵"}.get(self.severity, "⚪")
        parts = [f"{icon} {self.check_id} [{self.severity}] {self.path}"]
        parts.append(f"   {self.message}")
        if self.cwe:
            parts.append(f"   CWE: {self.cwe}")
        if self.fix:
            parts.append(f"   Fix: {self.fix}")
        return "\n".join(parts)


@dataclass
class AuditResult:
    spec_file: str
    spec_version: str = "unknown"
    findings: list = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "CRITICAL")

    @property
    def high_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "HIGH")

    @property
    def medium_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "MEDIUM")

    @property
    def low_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "LOW")


# ─── Constants ────────────────────────────────────────────────────────────────

SENSITIVE_FIELD_PATTERNS = re.compile(
    r"^(password|passwd|secret|ssn|social.?security|card.?number|cvv|cvc|"
    r"credit.?card|private.?key|api.?key|access.?token|refresh.?token|"
    r"auth.?token|bearer|jwt|session.?id|pin|otp|mfa.?code)$",
    re.IGNORECASE,
)

ADMIN_PATH_PATTERNS = re.compile(
    r"/(admin|internal|debug|_internal|_debug|management|actuator|"
    r"metrics|health/detail|swagger-ui|api-docs)(/|$)",
    re.IGNORECASE,
)

# OAuth2 flows deprecated in RFC 9700 / OAuth 2.1
DEPRECATED_FLOWS = {"implicit", "password"}

HTTP_METHODS = ["get", "post", "put", "patch", "delete", "options", "head", "trace"]

# Public endpoints — skip OS001 auth check
PUBLIC_PATH_RE = re.compile(
    r"/(health|ping|version|status|ready|live|favicon|robots\.txt)$",
    re.IGNORECASE,
)


# ─── YAML/JSON Loading ────────────────────────────────────────────────────────

def load_spec(source: str) -> dict:
    """Load OpenAPI spec from file path or URL."""
    content = ""
    if source.startswith("http://") or source.startswith("https://"):
        try:
            import urllib.request
            with urllib.request.urlopen(source, timeout=10) as r:
                content = r.read().decode()
        except Exception as e:
            sys.exit(f"Cannot fetch spec from URL: {e}")
    else:
        path = Path(source)
        if not path.exists():
            sys.exit(f"Spec file not found: {source}")
        content = path.read_text()

    # Try JSON first, then YAML
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    try:
        import yaml
        return yaml.safe_load(content)
    except ImportError:
        sys.exit(
            "PyYAML required for YAML specs. Install: pip install pyyaml\n"
            "Or convert your spec to JSON first: python -c \"import yaml,json; print(json.dumps(yaml.safe_load(open('spec.yaml').read()), indent=2))\" > spec.json"
        )


# ─── Spec Helpers ────────────────────────────────────────────────────────────

def detect_version(spec: dict) -> str:
    if "openapi" in spec:
        return f"OpenAPI {spec['openapi']}"
    if "swagger" in spec:
        return f"Swagger {spec['swagger']}"
    return "unknown"


def get_operations(spec: dict) -> list:
    """Returns list of (path, method, operation_obj) for all operations."""
    ops = []
    for path, path_item in spec.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue
        for method in HTTP_METHODS:
            op = path_item.get(method)
            if isinstance(op, dict):
                ops.append((path, method.upper(), op))
    return ops


def resolve_ref(spec: dict, ref: str) -> dict:
    """Simple local $ref resolver (handles #/components/schemas/Foo style)."""
    if not ref.startswith("#/"):
        return {}
    parts = ref[2:].split("/")
    node = spec
    for part in parts:
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            return {}
        node = node[part]
    return node if isinstance(node, dict) else {}


def get_global_security(spec: dict) -> list:
    return spec.get("security", [])


def get_security_schemes(spec: dict) -> dict:
    # OpenAPI 3.x
    components = spec.get("components", {})
    if components:
        return components.get("securitySchemes", {})
    # Swagger 2.0
    return spec.get("securityDefinitions", {})


# ─── Security Checks ─────────────────────────────────────────────────────────

def check_os001_missing_security(spec: dict, ops: list) -> list:
    """OS001 — Endpoint missing authentication requirement."""
    findings = []
    global_security = get_global_security(spec)
    schemes = get_security_schemes(spec)

    if not schemes:
        findings.append(Finding(
            check_id="OS001",
            severity="HIGH",
            path="<spec>",
            message="No securitySchemes defined. All endpoints are unauthenticated.",
            cwe="CWE-306: Missing Authentication for Critical Function",
            fix="Add securitySchemes under components/securitySchemes and apply via global security: [] or per-operation security:",
        ))
        return findings

    for path, method, op in ops:
        if PUBLIC_PATH_RE.search(path):
            continue  # Skip public health/ping endpoints

        op_security = op.get("security")
        if op_security is None:
            if not global_security:
                findings.append(Finding(
                    check_id="OS001",
                    severity="HIGH",
                    path=f"{method} {path}",
                    message="No security requirement on this endpoint and no global security defined.",
                    cwe="CWE-306: Missing Authentication for Critical Function",
                    fix="Add `security: [{BearerAuth: []}]` to the operation or define global security.",
                ))
        elif op_security == []:
            # Explicitly opts out of global security
            if method in ("POST", "PUT", "PATCH", "DELETE"):
                findings.append(Finding(
                    check_id="OS001",
                    severity="MEDIUM",
                    path=f"{method} {path}",
                    message="Security explicitly disabled (security: []). Verify this write operation intentionally requires no authentication.",
                    cwe="CWE-306",
                    fix="Add auth requirement or add `x-public: true` extension to document intentional public access.",
                ))
    return findings


def check_os002_http_server(spec: dict) -> list:
    """OS002 — Server URL uses plaintext HTTP (not localhost)."""
    findings = []
    LOCALHOST_RE = re.compile(r"localhost|127\.0\.0\.1|0\.0\.0\.0|::1")

    # OpenAPI 3.x servers array
    for server in spec.get("servers", []):
        url = server.get("url", "")
        if url.startswith("http://") and not LOCALHOST_RE.search(url):
            findings.append(Finding(
                check_id="OS002",
                severity="HIGH",
                path=f"servers[].url = {url}",
                message=f"Production server uses plaintext HTTP: {url}. Credentials and tokens transmitted in clear text.",
                cwe="CWE-319: Cleartext Transmission of Sensitive Information",
                fix="Change server URL to https://.",
            ))

    # Swagger 2.0 schemes + host
    schemes = spec.get("schemes", [])
    host = spec.get("host", "")
    if "http" in schemes and "https" not in schemes and host and not LOCALHOST_RE.search(host):
        findings.append(Finding(
            check_id="OS002",
            severity="HIGH",
            path=f"schemes: {schemes}, host: {host}",
            message="API only allows plaintext HTTP connections.",
            cwe="CWE-319",
            fix="Remove 'http' from schemes array, keep only 'https'.",
        ))
    return findings


def check_os003_apikey_in_query(spec: dict) -> list:
    """OS003 — API key passed as query parameter (appears in logs/history)."""
    findings = []
    schemes = get_security_schemes(spec)
    for name, scheme in schemes.items():
        if not isinstance(scheme, dict):
            continue
        if scheme.get("type") == "apiKey" and scheme.get("in") == "query":
            findings.append(Finding(
                check_id="OS003",
                severity="HIGH",
                path=f"securitySchemes/{name}",
                message=f"Scheme '{name}' passes API key as query parameter. Keys in URLs appear in server logs, browser history, CDN access logs, and HTTP Referer headers.",
                cwe="CWE-598: Use of GET Request Method with Sensitive Query Strings",
                fix="Change `in: query` to `in: header`. Use Authorization: Bearer or X-API-Key header instead.",
            ))
    return findings


def check_os004_deprecated_oauth_flow(spec: dict) -> list:
    """OS004 — OAuth2 implicit or password flow (deprecated, PKCE bypass)."""
    findings = []
    schemes = get_security_schemes(spec)
    for name, scheme in schemes.items():
        if not isinstance(scheme, dict):
            continue
        # OpenAPI 3.x flows object
        for flow_name in DEPRECATED_FLOWS:
            if flow_name in scheme.get("flows", {}):
                findings.append(Finding(
                    check_id="OS004",
                    severity="HIGH",
                    path=f"securitySchemes/{name}/flows/{flow_name}",
                    message=f"OAuth2 '{flow_name}' flow is deprecated (RFC 9700). Implicit exposes tokens in URL fragments; password flow exposes credentials to the client application.",
                    cwe="CWE-287: Improper Authentication",
                    fix="Replace implicit with authorization_code + PKCE. Replace password with device_code or authorization_code flow.",
                ))
        # Swagger 2.0 single flow field
        if scheme.get("type") == "oauth2" and scheme.get("flow") in DEPRECATED_FLOWS:
            findings.append(Finding(
                check_id="OS004",
                severity="HIGH",
                path=f"securityDefinitions/{name}",
                message=f"OAuth2 '{scheme.get('flow')}' flow is deprecated.",
                cwe="CWE-287",
                fix="Migrate to authorization_code flow with PKCE.",
            ))
    return findings


def check_os005_sensitive_fields_in_response(spec: dict, ops: list) -> list:
    """OS005 — Sensitive field names in response schemas."""
    findings = []

    def scan_schema(schema: dict, location: str, depth: int = 0) -> list:
        if depth > 8:  # Prevent infinite recursion on circular refs
            return []
        results = []
        if "$ref" in schema:
            schema = resolve_ref(spec, schema["$ref"])
        props = schema.get("properties", {})
        for field_name, field_schema in props.items():
            if SENSITIVE_FIELD_PATTERNS.match(field_name):
                results.append(Finding(
                    check_id="OS005",
                    severity="HIGH",
                    path=location,
                    message=f"Response schema exposes sensitive field '{field_name}'. Verify this is intentional.",
                    cwe="CWE-312: Cleartext Storage of Sensitive Information",
                    fix=f"Remove '{field_name}' from response schema. If accepted as input only, add `writeOnly: true`. Never return passwords, tokens, or keys in API responses.",
                ))
            # Recurse into nested objects
            if isinstance(field_schema, dict):
                results.extend(scan_schema(field_schema, f"{location}/{field_name}", depth + 1))
        # Array items
        items = schema.get("items", {})
        if isinstance(items, dict):
            results.extend(scan_schema(items, f"{location}[]", depth + 1))
        return results

    seen_refs = set()  # Deduplicate $ref scans
    for path, method, op in ops:
        for status_code, response in op.get("responses", {}).items():
            if not isinstance(response, dict):
                continue
            if "$ref" in response:
                ref_key = response["$ref"]
                if ref_key in seen_refs:
                    continue
                seen_refs.add(ref_key)
                response = resolve_ref(spec, ref_key)
            # OpenAPI 3.x content
            for media_type, media_obj in response.get("content", {}).items():
                if not isinstance(media_obj, dict):
                    continue
                schema = media_obj.get("schema", {})
                if schema:
                    loc = f"{method} {path} → {status_code} {media_type}"
                    findings.extend(scan_schema(schema, loc))
            # Swagger 2.0 schema
            schema = response.get("schema", {})
            if schema:
                findings.extend(scan_schema(schema, f"{method} {path} → {status_code}"))
    return findings


def check_os006_missing_request_body_schema(spec: dict, ops: list) -> list:
    """OS006 — Write operations without request body schema (no input validation)."""
    findings = []
    for path, method, op in ops:
        if method not in ("POST", "PUT", "PATCH"):
            continue
        # OpenAPI 3.x
        request_body = op.get("requestBody")
        if request_body is not None:
            if "$ref" in request_body:
                request_body = resolve_ref(spec, request_body["$ref"])
            content = request_body.get("content", {})
            for media_type, media_obj in content.items():
                if not isinstance(media_obj, dict):
                    continue
                if not media_obj.get("schema"):
                    findings.append(Finding(
                        check_id="OS006",
                        severity="MEDIUM",
                        path=f"{method} {path}",
                        message=f"Request body for '{media_type}' has no schema. API gateways cannot enforce input validation.",
                        cwe="CWE-20: Improper Input Validation",
                        fix="Add a schema with property types, required fields, and maxLength constraints.",
                    ))
        elif method == "POST":
            # Check Swagger 2.0 body parameters
            body_params = [
                p for p in op.get("parameters", [])
                if isinstance(p, dict) and p.get("in") == "body"
            ]
            if not body_params and not op.get("requestBody"):
                findings.append(Finding(
                    check_id="OS006",
                    severity="MEDIUM",
                    path=f"{method} {path}",
                    message="POST endpoint has no requestBody or body parameter. Input is completely unvalidated by the spec.",
                    cwe="CWE-20",
                    fix="Add requestBody with schema (OpenAPI 3.x) or body parameter with schema (Swagger 2.0).",
                ))
    return findings


def check_os007_missing_auth_responses(spec: dict, ops: list) -> list:
    """OS007 — Authenticated endpoints missing 401/403 response definitions."""
    findings = []
    global_security = get_global_security(spec)

    for path, method, op in ops:
        op_security = op.get("security", global_security)
        if not op_security:
            continue  # Public endpoint — skip

        responses = op.get("responses", {})
        has_401 = "401" in responses or 401 in responses
        has_403 = "403" in responses or 403 in responses

        if not has_401 and not has_403:
            findings.append(Finding(
                check_id="OS007",
                severity="LOW",
                path=f"{method} {path}",
                message="Authenticated endpoint defines no 401 or 403 response. Clients cannot distinguish auth failures; SDK generators may not handle auth errors correctly.",
                cwe="CWE-284: Improper Access Control",
                fix="Add `401: {description: Unauthorized}` and `403: {description: Forbidden}` to operation responses.",
            ))
    return findings


def check_os008_admin_path_no_auth(spec: dict, ops: list) -> list:
    """OS008 — Admin/debug/internal paths without authentication (CRITICAL)."""
    findings = []
    global_security = get_global_security(spec)

    for path, method, op in ops:
        if not ADMIN_PATH_PATTERNS.search(path):
            continue
        op_security = op.get("security", global_security)
        if not op_security:
            findings.append(Finding(
                check_id="OS008",
                severity="CRITICAL",
                path=f"{method} {path}",
                message=f"Admin/internal path '{path}' has no authentication. Publicly accessible — highest breach risk.",
                cwe="CWE-285: Improper Authorization",
                fix="Add strict authentication + elevated scope (e.g., scope: admin) to this endpoint. Consider removing it from public-facing specs entirely.",
            ))
    return findings


def check_os009_file_upload_no_size_limit(spec: dict, ops: list) -> list:
    """OS009 — File upload without maxLength constraint (DoS vector)."""
    findings = []
    for path, method, op in ops:
        if method not in ("POST", "PUT", "PATCH"):
            continue
        request_body = op.get("requestBody", {})
        if "$ref" in request_body:
            request_body = resolve_ref(spec, request_body["$ref"])
        content = request_body.get("content", {})
        for media_type, media_obj in content.items():
            if "multipart" not in media_type and "octet-stream" not in media_type:
                continue
            if not isinstance(media_obj, dict):
                continue
            schema = media_obj.get("schema", {})
            if "$ref" in schema:
                schema = resolve_ref(spec, schema["$ref"])
            props = schema.get("properties", {})
            for prop_name, prop_schema in props.items():
                if not isinstance(prop_schema, dict):
                    continue
                is_binary = (
                    prop_schema.get("format") == "binary"
                    or prop_schema.get("type") == "string"
                )
                if is_binary and "maxLength" not in prop_schema and "maximum" not in prop_schema:
                    findings.append(Finding(
                        check_id="OS009",
                        severity="MEDIUM",
                        path=f"{method} {path} → {prop_name}",
                        message=f"File upload field '{prop_name}' has no maxLength. Unbounded uploads enable DoS via large files.",
                        cwe="CWE-400: Uncontrolled Resource Consumption",
                        fix=f"Add `maxLength: 10485760` (10MB) or appropriate limit to the '{prop_name}' schema.",
                    ))
    return findings


def check_os010_wildcard_scope(spec: dict) -> list:
    """OS010 — OAuth2 scopes with wildcard or overly broad permissions."""
    findings = []
    schemes = get_security_schemes(spec)

    WILDCARD_SCOPE_RE = re.compile(
        r"(\*|^admin$|^root$|^superuser$|^all$|^full$|write:\*|read:\*)",
        re.IGNORECASE,
    )

    for name, scheme in schemes.items():
        if not isinstance(scheme, dict):
            continue
        scopes: set = set()
        # OpenAPI 3.x flows
        for flow_obj in scheme.get("flows", {}).values():
            if isinstance(flow_obj, dict):
                scopes.update(flow_obj.get("scopes", {}).keys())
        # Swagger 2.0
        scopes.update(scheme.get("scopes", {}).keys())

        for scope in scopes:
            if WILDCARD_SCOPE_RE.search(scope):
                findings.append(Finding(
                    check_id="OS010",
                    severity="HIGH",
                    path=f"securitySchemes/{name}/scopes/{scope}",
                    message=f"OAuth scope '{scope}' is overly broad. A compromised client with this scope has unrestricted API access.",
                    cwe="CWE-272: Least Privilege Violation",
                    fix="Replace wildcard scopes with specific resource:action scopes (e.g. 'users:read', 'orders:write'). Never grant * or bare admin scope.",
                ))
    return findings


# ─── Main Audit ───────────────────────────────────────────────────────────────

def audit_spec(source: str) -> AuditResult:
    spec = load_spec(source)
    result = AuditResult(spec_file=source, spec_version=detect_version(spec))
    ops = get_operations(spec)

    checks = [
        check_os001_missing_security(spec, ops),
        check_os002_http_server(spec),
        check_os003_apikey_in_query(spec),
        check_os004_deprecated_oauth_flow(spec),
        check_os005_sensitive_fields_in_response(spec, ops),
        check_os006_missing_request_body_schema(spec, ops),
        check_os007_missing_auth_responses(spec, ops),
        check_os008_admin_path_no_auth(spec, ops),
        check_os009_file_upload_no_size_limit(spec, ops),
        check_os010_wildcard_scope(spec),
    ]
    for findings in checks:
        result.findings.extend(findings)
    return result


def format_report(result: AuditResult, ci_mode: bool = False) -> str:
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  OpenAPI Security Audit — {result.spec_file}")
    lines.append(f"  Spec: {result.spec_version}")
    lines.append(f"{'='*60}")

    if not result.findings:
        lines.append("✅ No security issues found.")
        return "\n".join(lines)

    for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
        sev_findings = [f for f in result.findings if f.severity == severity]
        if sev_findings:
            lines.append(f"\n── {severity} ({len(sev_findings)}) {'─'*40}")
            for finding in sev_findings:
                lines.append(str(finding))

    lines.append(f"\n{'─'*60}")
    lines.append(
        f"  Total: {len(result.findings)} findings  |  "
        f"Critical: {result.critical_count}  High: {result.high_count}  "
        f"Medium: {result.medium_count}  Low: {result.low_count}"
    )
    if ci_mode and (result.critical_count > 0 or result.high_count > 0):
        lines.append("\n  ❌ CI GATE FAILED — resolve CRITICAL/HIGH findings before merging.")
    return "\n".join(lines)


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-openapi-sec-audit — OpenAPI/Swagger Security Auditor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python openapi_sec_audit.py openapi.yaml
  python openapi_sec_audit.py https://petstore3.swagger.io/api/v3/openapi.json
  python openapi_sec_audit.py api/ --scan-dir
  python openapi_sec_audit.py openapi.yaml --ci
  python openapi_sec_audit.py openapi.yaml --only-severity HIGH
        """,
    )
    parser.add_argument("spec", help="Path to OpenAPI spec (YAML/JSON), URL, or directory")
    parser.add_argument("--ci", action="store_true", help="Exit 1 on CRITICAL or HIGH findings")
    parser.add_argument("--scan-dir", action="store_true", help="Scan directory for all spec files")
    parser.add_argument(
        "--only-severity",
        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        help="Filter output to this severity and above",
    )
    args = parser.parse_args()

    specs_to_scan = []

    if args.scan_dir:
        spec_dir = Path(args.spec)
        if not spec_dir.is_dir():
            sys.exit(f"Not a directory: {args.spec}")
        for ext in ("*.yaml", "*.yml", "*.json"):
            for f in spec_dir.rglob(ext):
                try:
                    content = f.read_text()
                    if ("openapi" in content or "swagger" in content) and "paths" in content:
                        specs_to_scan.append(str(f))
                except Exception:
                    pass
    else:
        specs_to_scan.append(args.spec)

    if not specs_to_scan:
        print("No OpenAPI spec files found.")
        sys.exit(0)

    exit_code = 0
    sev_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

    for spec_path in specs_to_scan:
        try:
            result = audit_spec(spec_path)
            if args.only_severity:
                cutoff = sev_order.index(args.only_severity)
                result.findings = [
                    f for f in result.findings if sev_order.index(f.severity) <= cutoff
                ]
            print(format_report(result, ci_mode=args.ci))
            if args.ci and (result.critical_count > 0 or result.high_count > 0):
                exit_code = 1
        except Exception as e:
            print(f"Error auditing {spec_path}: {e}", file=sys.stderr)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
```

## False Positive Notes

- **OS001 skips** `/health`, `/ping`, `/version`, `/status`, `/ready`, `/live` — these are intentionally public
- **OS002 skips** localhost/127.0.0.1 — local dev HTTP is fine
- **OS005 deduplicates** shared `$ref` schemas — a reused `UserResponse` schema is only flagged once
- **OS001 flags MEDIUM (not HIGH)** when `security: []` is explicit on a write endpoint — this may be intentional (e.g., a public webhook receiver)

## Related Skills

- **phy-api-version-audit** — checks API versioning health (Sunset headers, version gaps)
- **phy-api-changelog-gen** — diffs two OpenAPI specs and classifies breaking changes
- **phy-cors-audit** — CORS misconfiguration prober (live endpoint + source code)
- **phy-jwt-auth-audit** — audits JWT tokens and auth middleware in source code

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
