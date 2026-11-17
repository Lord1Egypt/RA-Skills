# Data Schemas — GKN-Phantom Penetration Testing Skill

Authoritative JSON schemas for all inputs and outputs. The agent MUST conform
to these schemas. All examples are illustrative; field names and types are
normative.

## AgentContext

The runtime context handed to `execute(ctx)`. Provided by the OpenClaw agent.

```json
{
  "scope": {
    "domains": ["example.test", "*.staging.example.test"],
    "ip_ranges": ["10.0.0.0/24", "192.168.50.0/24"],
    "allowed_paths": ["/api", "/"],
    "blocked_paths": ["/admin/delete"]
  },
  "targets": [
    "https://staging.example.test",
    "https://api.staging.example.test"
  ],
  "credentials": {
    "type": "cookie",
    "value": "session=...",
    "verify_url": "https://api.staging.example.test/me"
  },
  "config": {
    "rate_limit_rps": 3,
    "safe_mode": true,
    "require_human_approval": true,
    "environment": "staging"
  },
  "tools": {
    "runShell": "<function>",
    "httpRequest": "<function>",
    "browser": "<function>",
    "logger": "<function>"
  },
  "state": {
    "current": "INIT",
    "history": [],
    "session_ref": null
  },
  "memory": {
    "prior_findings": [],
    "asset_cache": {}
  }
}
```

## InputSchema (execute input validation)

```json
{
  "type": "object",
  "required": ["scope", "targets", "config", "tools"],
  "properties": {
    "scope": {
      "type": "object",
      "required": ["domains", "ip_ranges"],
      "properties": {
        "domains": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
        "ip_ranges": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
        "allowed_paths": { "type": "array", "items": { "type": "string" } },
        "blocked_paths": { "type": "array", "items": { "type": "string" } }
      }
    },
    "targets": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "credentials": { "type": "object" },
    "config": {
      "type": "object",
      "properties": {
        "rate_limit_rps": { "type": "integer", "minimum": 1, "default": 3 },
        "safe_mode": { "type": "boolean", "default": true },
        "require_human_approval": { "type": "boolean", "default": true },
        "environment": { "type": "string", "enum": ["staging", "dev", "internal", "lab"] }
      }
    },
    "tools": { "type": "object" },
    "state": { "type": "object" },
    "memory": { "type": "object" }
  }
}
```

## OutputSchema (SkillResult payload)

```json
{
  "type": "object",
  "required": ["summary", "risk_score", "assets", "findings", "attack_paths", "recommendations", "execution_log"],
  "properties": {
    "summary": { "type": "string" },
    "risk_score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "assets": { "type": "object" },
    "findings": { "type": "array", "items": { "$ref": "#/definitions/Finding" } },
    "attack_paths": { "type": "array", "items": { "$ref": "#/definitions/AttackPath" } },
    "recommendations": { "type": "array", "items": { "type": "string" } },
    "execution_log": { "type": "array", "items": { "type": "object" } }
  }
}
```

## Finding (standard)

A Finding is the atomic unit of a vulnerability detection result. Every field
below is normative. The `confidence_breakdown` sub-object is populated by
`scripts/confidence_scoring.py` (see §Confidence Scoring).

```json
{
  "id": "finding-001",
  "type": "xss | sqli | ssrf | idor | misconfig | info_leak | open_redirect | path_traversal | csrf | xxe | ssti | deserialization | command_injection | rce | auth_bypass | priv_esc | data_exposure | weak_credential | component_exposure | captcha_bypass | file_upload | logic_flaw | nosql_injection | ldap_injection | crlf_injection | graphql_injection | graphql_introspection | cors_misconfig | prototype_pollution | cache_poisoning | race_condition | http_smuggling | subdomain_takeover | host_header_injection | jwt_deep_analysis | oauth_misconfig | mass_assignment | dependency_confusion | session_fixation | email_injection | websocket_hijacking | directory_listing",
  "severity": "low | medium | high | critical",
  "tier": "low | medium | high | critical",
  "target": "https://staging.example.test/search?q=test",
  "status": "detected | validated | false_positive",
  "confidence": 0.85,
  "confidence_breakdown": {
    "evidence_strength": 0.9,
    "reproducibility_score": 0.8,
    "signal_clarity": 0.85,
    "corroboration": 0.7,
    "method": "weighted_v2"
  },
  "evidence": {
    "request": "GET /search?q=<script>alert(1)</script> HTTP/1.1\r\nHost: ...",
    "response": "HTTP/1.1 200 OK\r\n...\r\n<p>results for <script>alert(1)</script></p>",
    "timestamp": "2026-06-20T14:03:22Z",
    "tool": "httpRequest",
    "status_code": 200,
    "response_time_ms": 142,
    "headers": { "Content-Type": "text/html" }
  },
  "reproducible": true,
  "reproducibility_score": 0.8,
  "replay_count": 2,
  "replay_results": [
    { "attempt": 1, "signal_matched": true, "delta_ms": 12 },
    { "attempt": 2, "signal_matched": true, "delta_ms": 8 }
  ],
  "safe_poc": true,
  "risk_level": "L2",
  "requires_human_approval": false,
  "blocked_in_safe_mode": false,
  "detection_signal": "Marker reflected unescaped in response body",
  "remediation": "Output-encode user input in HTML context; use a context-aware encoding library.",
  "reproduction_steps": [
    "Send GET /search?q=<script>alert(1)</script> with no authentication.",
    "Observe the payload reflected unescaped in the response body."
  ],
  "adaptive_metadata": {
    "waf_detected": false,
    "waf_type": null,
    "mutations_tried": 0,
    "fallback_strategy": null,
    "retry_count": 0
  },
  "fingerprint": "a1b2c3d4e5f67890"
}
```

Field rules:

- `id` — stable, unique within a run; format `finding-NNN`.
- `type` — one of the enum values (see type→severity baseline below).
- `severity` — follows CVSS-like qualitative bands.
- `tier` — the detection tier that produced this finding (low/medium/high/critical).
- `target` — the exact URL/endpoint where the finding was observed.
- `status` — `detected` (candidate), `validated` (TP, reproducible),
  `false_positive` (FP).
- `confidence` — 0.0–1.0; ≥0.8 required to promote `detected` → `validated`.
  Computed by `confidence_scoring.py` (see §Confidence Scoring below).
- `confidence_breakdown` — sub-scores that aggregate into `confidence`.
  Populated by `scripts/confidence_scoring.py`.
- `evidence` — all core sub-fields required (see safety_policy.md §5).
  Extended fields (`status_code`, `response_time_ms`, `headers`) are optional
  but recommended for confidence scoring.
- `reproducible` — must be re-confirmed by `finding_validator.py`.
- `reproducibility_score` — 0.0–1.0; fraction of replays that matched the
  signal. Populated by `finding_validator.py` + `confidence_scoring.py`.
- `replay_count` — number of times the PoC was replayed for validation.
- `replay_results` — per-attempt signal match + timing delta.
- `safe_poc` — must be true to appear in the final `findings` array.
- `risk_level` — L1–L4 (see safety_policy.md §3).
- `requires_human_approval` — true for L4 and sensitive L3 probes.
- `blocked_in_safe_mode` — true if this probe is blocked when safe_mode is on.
- `detection_signal` — human-readable description of what the detector looked for.
- `adaptive_metadata` — populated by `scripts/adaptive_engine.py` when WAF
  detection, payload mutation, or fallback strategies are engaged.
- `fingerprint` — stable 16-char hash for dedup (see `utils.finding_fingerprint`).

### Type → default severity baseline (overridable by evidence)

| Severity | Default types                                                    | Rationale                                       |
| --------- | --------------------------------------------------------------- | ----------------------------------------------- |
| low       | `info_leak`, `open_redirect`, `csrf` (weak), `misconfig` (header), `graphql_introspection`, `directory_listing` | Limited direct impact, defense-in-depth gaps    |
| medium    | `xss` (reflected), `path_traversal` (read-only), `xxe` (no OOB), `ssti` (reflection-only), `csrf` (state-changing), `weak_credential` (弱口令), `component_exposure` (Actuator/Druid/Swagger), `captcha_bypass` (验证码绕过), `crlf_injection`, `cors_misconfig`, `subdomain_takeover`, `host_header_injection`, `websocket_hijacking`, `session_fixation`, `email_injection`, `deserialization` | User-session scope, requires interaction        |
| high      | `xss` (stored), `sqli`, `ssrf`, `idor`, `command_injection`, `file_upload` (文件上传), `logic_flaw` (逻辑缺陷), `nosql_injection`, `ldap_injection`, `graphql_injection`, `cache_poisoning`, `race_condition`, `prototype_pollution`, `jwt_deep_analysis`, `oauth_misconfig`, `mass_assignment`, `dependency_confusion` | Server-side or cross-user impact                |
| critical  | `rce`, `auth_bypass`, `priv_esc`, `data_exposure` (bulk/PII), `http_smuggling` | Full compromise / mass data exposure            |

The detector assigns the baseline; the validator may raise or lower severity based on confirmed exploitability and data sensitivity.
- `status` — `detected` (candidate), `validated` (TP, reproducible),
  `false_positive` (FP).
- `confidence` — 0.0–1.0; ≥0.8 required to promote `detected` → `validated`.
- `evidence` — all four sub-fields required (see safety_policy.md §5).
- `reproducible` — must be re-confirmed by `finding_validator.py`.
- `safe_poc` — must be true to appear in the final `findings` array.

## AttackPath (graph structure)

```json
{
  "id": "path-001",
  "name": "Auth bypass → IDOR → data exposure",
  "nodes": [
    { "id": "f-001", "type": "finding", "ref": "finding-001" },
    { "id": "f-003", "type": "finding", "ref": "finding-003" },
    { "id": "asset-2", "type": "asset", "ref": "/api/users/{id}" }
  ],
  "edges": [
    { "from": "f-001", "to": "f-003", "relation": "enables", "confirmed": true },
    { "from": "f-003", "to": "asset-2", "relation": "exposes", "confirmed": true }
  ],
  "impact": "Unauthenticated attacker can read arbitrary user records.",
  "confidence": 0.9
}
```

## FinalOutput

```json
{
  "summary": "string",
  "risk_score": 0,
  "assets": {
    "domains": [],
    "ips": [],
    "endpoints": []
  },
  "findings": [],
  "attack_paths": [],
  "recommendations": [],
  "execution_log": []
}
```

## SARIF-like CI output (inside execution_log or as a sibling artifact)

```json
{
  "version": "2.1.0",
  "runs": [
    {
      "tool": { "driver": { "name": "gkn-phantom", "version": "1.0.0" } },
      "results": [
        {
          "ruleId": "xss-reflected",
          "level": "error",
          "message": { "text": "Reflected XSS at /search" },
          "locations": [
            { "physicalLocation": { "artifactLocation": { "uri": "https://staging.example.test/search" } } }
          ]
        }
      ]
    }
  ]
}
```

## ReconOutput

```json
{
  "assets": {
    "domains": ["staging.example.test", "api.staging.example.test"],
    "ips": ["10.0.0.12"],
    "endpoints": [
      { "url": "https://staging.example.test/search", "methods": ["GET"] },
      { "url": "https://api.staging.example.test/users", "methods": ["GET", "POST"] }
    ]
  }
}
```

## AuthOutput

```json
{
  "authenticated": true,
  "session_ref": "sess-abc123",
  "method": "cookie",
  "verified_at": "2026-06-20T14:02:00Z"
}
```

## Asset (full schema)

An Asset is any discovered target surface. Assets are produced by
RECONNAISSANCE and consumed by ACTIVE_TESTING.

```json
{
  "domains": [
    {
      "domain": "staging.example.test",
      "source": "certificate_transparency",
      "first_seen": "2026-06-20T14:00:05Z",
      "resolved_ips": ["10.0.0.12"],
      "in_scope": true
    }
  ],
  "ips": [
    {
      "ip": "10.0.0.12",
      "hostname": "staging.example.test",
      "in_scope": true,
      "reverse_dns": "staging.example.test"
    }
  ],
  "endpoints": [
    {
      "url": "https://staging.example.test/search",
      "methods": ["GET"],
      "params": [
        { "name": "q", "type": "query", "reflected": true, "sample_value": "test" }
      ],
      "auth_required": false,
      "technologies": ["nginx/1.25", "Express"],
      "status_code": 200,
      "response_time_ms": 45,
      "discovered_via": "wordlist"
    }
  ],
  "technologies": [
    { "name": "nginx", "version": "1.25", "source": "Server header", "cpe": "cpe:/a:nginx:nginx:1.25" }
  ],
  "ports": [
    { "ip": "10.0.0.12", "port": 443, "protocol": "tcp", "service": "https", "state": "open" }
  ]
}
```

Field rules:
- `domains[].in_scope` — must be true for all domains used in probing.
- `endpoints[].params[].reflected` — true if the param value appears in the
  response (candidate for XSS/SSTI injection).
- `endpoints[].auth_required` — true if endpoint returned 401/403 without
  credentials.
- `technologies[].cpe` — CPE identifier for CVE correlation.

## AttackPath (full schema — extended)

```json
{
  "id": "path-001",
  "name": "Auth bypass → IDOR → data exposure",
  "nodes": [
    { "id": "f-001", "type": "finding", "ref": "finding-001" },
    { "id": "f-003", "type": "finding", "ref": "finding-003" },
    { "id": "asset-2", "type": "asset", "ref": "/api/users/{id}" }
  ],
  "edges": [
    { "from": "f-001", "to": "f-003", "relation": "enables", "confirmed": true, "evidence_ref": "finding-001.evidence" },
    { "from": "f-003", "to": "asset-2", "relation": "exposes", "confirmed": true, "evidence_ref": "finding-003.evidence" }
  ],
  "impact": "Unauthenticated attacker can read arbitrary user records.",
  "confidence": 0.9,
  "chain_type": "auth_bypass | weak_credential_chain | component_exposure_chain | file_upload_chain | data_exposure",
  "estimated_severity": "critical",
  "attack_steps": [
    "Attacker bypasses auth at /login via weak_credential",
    "Attacker enumerates /api/users/{id} via IDOR",
    "Attacker harvests PII from responses"
  ]
}
```

Field rules:
- `edges[].relation` — one of: `enables`, `enables_recon`, `escalates_to`,
  `exposes`, `co_located_weakness`.
- `edges[].confirmed` — true only if backed by evidence; false for LLM-inferred
  candidate edges.
- `chain_type` — categorizes the attack chain for reporting.
- `estimated_severity` — the aggregate severity if the chain is fully exploited.

## Tool I/O Schema

Defines the contract for every tool the agent invokes via `ctx.tools`. Each
tool has a typed input and output. The agent MUST conform to these schemas
when calling tools.

### httpRequest

```json
// INPUT
{
  "method": "GET | POST | PUT | DELETE | HEAD | OPTIONS | PATCH",
  "url": "https://staging.example.test/search?q=test",
  "headers": { "Content-Type": "application/json", "Cookie": "session=..." },
  "body": "{\"q\":\"test\"}",
  "timeout_ms": 10000,
  "follow_redirects": false,
  "verify_tls": true
}
// OUTPUT
{
  "status_code": 200,
  "status_text": "OK",
  "headers": { "Content-Type": "text/html" },
  "body": "<html>...</html>",
  "body_size": 4523,
  "response_time_ms": 142,
  "redirected": false,
  "final_url": "https://staging.example.test/search?q=test",
  "error": null
}
// ERROR STATES
// timeout_ms exceeded → { "error": "timeout", "status_code": null }
// connection refused   → { "error": "connection_refused" }
// TLS failure          → { "error": "tls_error", "detail": "..." }
// out of scope         → { "error": "scope_violation" } (pre-checked by scope_guard)
```

### runShell

```json
// INPUT
{
  "command": "nmap -sT --top-ports 100 10.0.0.12",
  "timeout_ms": 30000,
  "cwd": "/tmp",
  "env": { "PATH": "/usr/bin:/usr/local/bin" }
}
// OUTPUT
{
  "exit_code": 0,
  "stdout": "...",
  "stderr": "...",
  "duration_ms": 12500,
  "error": null
}
// ERROR STATES
// exit_code != 0      → command failed; stderr contains error detail
// timeout_ms exceeded  → { "error": "timeout", "exit_code": null }
// command not found    → { "error": "not_found", "exit_code": 127 }
// scope violation      → { "error": "scope_violation" } (IP not in scope)
```

### browser

```json
// INPUT
{
  "action": "navigate | click | fill | screenshot | evaluate | wait",
  "url": "https://staging.example.test/login",
  "selector": "#username",
  "value": "admin",
  "script": "document.cookie",
  "wait_ms": 3000
}
// OUTPUT
{
  "success": true,
  "result": "...",  // screenshot base64 / element text / script result
  "url": "https://staging.example.test/dashboard",
  "error": null
}
// ERROR STATES
// navigation timeout  → { "error": "navigation_timeout" }
// selector not found   → { "error": "selector_not_found", "selector": "..." }
// script exception     → { "error": "script_error", "detail": "..." }
```

### logger

```json
// INPUT
{
  "level": "debug | info | warn | error | critical",
  "message": "Scope check passed for 2 targets",
  "state": "SCOPE_CHECK",
  "extra": { "targets_checked": 2 }
}
// OUTPUT
{
  "logged": true,
  "entry_id": "log-000123"
}
// ERROR STATES (logger is best-effort; errors are swallowed and logged to stderr)
```
