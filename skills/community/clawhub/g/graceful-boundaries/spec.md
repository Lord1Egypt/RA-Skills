# Graceful Boundaries

**Version:** 1.2.0
**Status:** Released
**License:** CC-BY-4.0
**URL:** https://gracefulboundaries.dev

## Abstract

Graceful Boundaries is a specification for how services communicate their operational limits to humans and autonomous agents. It covers three requirements that existing standards address separately but no specification combines:

1. **Proactive discovery** — limits are machine-readable before they are hit
2. **Structured refusal** — when a limit is exceeded, the response explains what happened, which limit applies, when to retry, and why the limit exists
3. **Constructive guidance** — the refusal includes a useful next step, not just a block

The specification is transport-agnostic but provides concrete conventions for HTTP APIs.

## Motivation

Every unclear response generates follow-up traffic. A vague `429` causes blind retries. A vague `403` causes re-attempts with different credentials. A vague `404` causes the caller to probe neighboring paths. A generic `500` causes the caller to retry indefinitely.

This is wasteful for the service and frustrating for the caller. When autonomous agents are the caller, the waste compounds — agents retry faster, probe more systematically, and lack the human judgment to know when to stop.

Graceful Boundaries exists to **reduce unnecessary traffic** by making every non-success response self-explanatory. The specification has two practical goals:

1. **Eliminate discovery-through-failure.** If a caller can learn the rules before breaking them, they will generate less traffic. A proactive discovery endpoint prevents the first round of 429s entirely.

2. **Expose security intent.** The `why` field is not a courtesy — it is a security signal. When a service says "this limit prevents the scan engine from being used as a proxy to attack other sites," the caller (human or agent) understands the defensive posture and adjusts behavior accordingly. When a service says "rate limit exceeded," the caller learns nothing and retries.

The specification applies not just to rate limits but to every class of HTTP response where the caller needs to decide what to do next.

## Principles

1. **Clarity reduces traffic.** A response that explains the constraint, the reason, and the next step generates zero follow-up requests. A response that says only "no" generates retries, probes, and support tickets.

2. **Limits are not secrets.** A service that enforces limits should publish them before callers hit them. Proactive disclosure prevents the first failure entirely.

3. **The reason is a security signal.** `why` exposes the defensive intent behind a constraint. "This limit prevents abuse of the email system" tells the caller the security model. "Too many requests" tells them nothing. An agent that understands the security model makes better decisions than one that doesn't.

4. **Every non-success response should include a next step.** "Try again in 30 seconds" is a next step. "Use the cached result instead" is a better one. "Here's the endpoint that does what you actually need" is best. "No" with no alternative is the worst — it forces the caller to guess.

5. **Agents and humans need different things from the same response.** Machine-parseable fields (`retryAfterSeconds`, `limit`) serve agents. Human-readable fields (`detail`, `why`) serve people. Both MUST be present. A response that serves only one audience forces the other to parse or guess.

## Specification

### 1. Limits Discovery Endpoint

A conforming service MUST provide a limits discovery endpoint that returns all enforced limits as structured data.

**Convention for HTTP:** `GET /api/limits` or `GET /.well-known/limits`

**Response format:**

```json
{
  "service": "string — service name",
  "description": "string — what the service does",
  "conformance": "string (optional) — self-declared conformance level (see Conformance Levels)",
  "changelog": "string (optional) — URL to a changelog resource for limit changes",
  "feed": "string (optional) — URL to a feed (JSON Feed, Atom, RSS) for change notifications",
  "limits": {
    "<endpoint-key>": {
      "endpoint": "string — path pattern",
      "method": "string — HTTP method",
      "limits": [
        {
          "type": "string — limit category (see below)",
          "maxRequests": "number — maximum requests in the window",
          "windowSeconds": "number — window duration in seconds",
          "description": "string — human-readable explanation"
        }
      ],
      "note": "string (optional) — additional context for this endpoint"
    }
  }
}
```

**Limit types:**

| Type | Meaning |
|---|---|
| `ip-rate` | Requests per IP address per time window |
| `key-rate` | Requests per API key per time window |
| `user-rate` | Requests per authenticated user per time window |
| `global-rate` | Requests across all callers per time window |
| `resource-dedup` | One operation per resource per time window (e.g., one scan per domain per day) |
| `cooldown` | Minimum interval between successive requests of a specific type |
| `concurrency` | Maximum simultaneous in-flight requests |

Services MAY define additional types. Unknown types SHOULD be treated as opaque constraints by clients.

The limits endpoint SHOULD be cacheable. A `Cache-Control` header with `s-maxage` of at least 300 seconds is RECOMMENDED.

**Change discovery:**

The `changelog` and `feed` fields allow agents to detect when limits have changed without re-fetching the full discovery endpoint. Both fields are OPTIONAL.

The `changelog` URL SHOULD point to a JSON resource listing dated changes, most recent first:

```json
[
  {
    "date": "2026-04-01",
    "summary": "Reduced scan rate limit from 20/hour to 10/hour",
    "breaking": true,
    "affectedEndpoints": ["/api/scan"]
  },
  {
    "date": "2026-03-15",
    "summary": "Added resource-dedup returnsCached flag to discovery",
    "breaking": false
  }
]
```

A change is `breaking` if it reduces limits below previous values, removes endpoints, or otherwise affects an agent's ability to operate. Limit increases, new optional fields, and documentation improvements are non-breaking.

The `feed` URL SHOULD point to a standard feed format (JSON Feed, Atom, or RSS) with entries for each limit change. This allows agents to poll or subscribe using existing feed infrastructure.

Agents SHOULD check for changes on startup and every 1–6 hours for long-lived processes. An agent that receives a `429` with an unfamiliar `limit` value SHOULD re-fetch the discovery endpoint, as limits may have changed.

**Conformance declaration:**

The `conformance` field allows a service to declare its own conformance level. Valid values:

| Value | Meaning |
|---|---|
| `"not-applicable"` | The site has no agentic interaction surface |
| `"none"` | The service enforces limits but has not adopted this specification |
| `"level-1"` | Claims Level 1 conformance |
| `"level-2"` | Claims Level 2 conformance |
| `"level-3"` | Claims Level 3 conformance |
| `"level-4"` | Claims Level 4 conformance |

A site declaring `not-applicable` SHOULD still provide a limits discovery endpoint with an empty `limits` object. This distinguishes "we have nothing to disclose" from "we haven't heard of this spec" (no endpoint at all).

```json
{
  "service": "Example Blog",
  "description": "Personal blog. No API or agentic services.",
  "conformance": "not-applicable",
  "limits": {}
}
```

A service declaring `none` acknowledges the specification but has not implemented it. This is more informative than a missing endpoint because it signals awareness:

```json
{
  "service": "Example API",
  "description": "REST API with rate limiting.",
  "conformance": "none",
  "limits": {}
}
```

The `conformance` field is a self-assertion. External agents validate it against actual behavior (see Conformance Levels).

### 2. Structured Refusal Response

When a limit is exceeded, the response MUST include the following fields:

```json
{
  "error": "string — machine-parseable error category",
  "detail": "string — human-readable explanation including the specific wait time",
  "limit": "string — the limit that was exceeded, in human-readable form",
  "retryAfterSeconds": "number — seconds until the caller can retry",
  "why": "string — one sentence explaining why this limit exists"
}
```

**Requirements:**

- `error` MUST be a stable string suitable for programmatic matching, using `snake_case`: lowercase alphanumeric characters and underscores only (e.g., `"rate_limit_exceeded"`, `"resource_dedup"`, `"cooldown_active"`).
- `detail` MUST include the specific retry time in human-readable form (e.g., "Try again in 42 seconds").
- `limit` MUST state the limit in concrete terms (e.g., "10 scans per IP per hour").
- `retryAfterSeconds` MUST be a non-negative integer.
- `why` MUST explain the purpose of the limit, not just restate it. "Rate limits keep the service available for everyone" is acceptable. "Rate limit exceeded" is not — that restates the error, not the reason.

**Retry behavior guidance:**

The `retryAfterSeconds` field tells agents *when* they can retry. It does not tell them *how* to retry. Different services have different expectations: an anti-abuse rate limit wants a single retry after the window; a congestion-limited service wants exponential backoff to let load dissipate.

Services SHOULD include guidance on retry behavior when the default assumption (wait, then retry once) is not appropriate:

- If the service expects callers to wait the full duration and retry once, no additional guidance is needed — `retryAfterSeconds` is sufficient.
- If the service expects callers to use exponential backoff (e.g., during congestion or cascading failures), the `why` field SHOULD signal this: "The service is under heavy load. Spread retries over time rather than retrying immediately after the window."
- If the service will progressively extend the block for callers that retry aggressively, the `detail` field SHOULD warn: "Continued requests during the cooldown period will extend the block."

Agents SHOULD treat `retryAfterSeconds` as a minimum wait time, not an exact retry time. Adding small random jitter (1–5 seconds) prevents synchronized retry storms.

**Additional fields** MAY be included for constructive guidance (see section 3).

**Convention for HTTP:** Return status `429 Too Many Requests` with a `Retry-After` header (seconds) and the structured JSON body. The `Content-Type` MUST be `application/json` for API endpoints. HTML endpoints MAY return `text/html` but MUST include the same information in human-readable form.

**HTML 429 responses:** HTML endpoints that return 429 SHOULD include a `<meta name="retry-after" content="N">` tag (seconds) and a `<link rel="alternate" type="application/json" href="...">` pointing to the JSON equivalent of the same response. This allows agents that follow HTML links to discover the structured refusal without parsing prose. Alternatively, the `Retry-After` header alone is sufficient for agents that check headers before parsing the body. The requirement is that the retry information is machine-accessible, not that it is in JSON specifically.

### 3. Constructive Guidance

A conforming refusal response SHOULD include at least one field that helps the caller take a useful action beyond waiting:

```json
{
  "cached": "boolean (optional) — whether a cached result is available",
  "cachedResultUrl": "string (optional) — URL to retrieve the cached result",
  "alternativeEndpoint": "string (optional) — a different endpoint that may serve the need",
  "upgradeUrl": "string (optional) — where to get higher limits",
  "humanUrl": "string (optional) — a browser-friendly URL for human follow-up"
}
```

**Guidance categories:**

| Category | When to use | Example |
|---|---|---|
| Use cached | A prior result exists for the same resource | `"cachedResultUrl": "/api/result?id=example-com-20260321"` |
| Try alternative | A different endpoint can serve the need with different limits | `"alternativeEndpoint": "/api/result?id=example.com"` |
| Upgrade | Paid or authenticated access has higher limits | `"upgradeUrl": "https://example.com/pricing"` |
| Wait | No alternative exists; retrying after the window is the only option | (No additional fields — `retryAfterSeconds` is sufficient) |
| Human handoff | The situation requires human judgment | `"humanUrl": "https://example.com/contact"` |

A service SHOULD prefer guidance categories in this order: use cached > try alternative > upgrade > wait > human handoff. The first applicable category wins.

### 4. Proactive Limit Headers (RECOMMENDED)

On successful responses, a conforming service SHOULD include headers that communicate the caller's remaining budget. This allows clients to self-throttle before hitting limits.

**Convention for HTTP** (aligned with `draft-ietf-httpapi-ratelimit-headers`):

```
RateLimit: limit=10, remaining=7, reset=2400
RateLimit-Policy: 10;w=3600
```

Services that implement Graceful Boundaries SHOULD also implement the IETF RateLimit headers when they reach RFC status.

### 5. Resource Deduplication Responses

When a request is refused because the resource was already processed within the dedup window (e.g., one scan per domain per day), the service SHOULD return the existing result rather than a bare refusal.

The response SHOULD:
- Return the cached result with a `200` status code
- Include a flag indicating the result is cached (e.g., `"_rescanBlocked": true`)
- Include a human-readable explanation (e.g., "This domain was already scanned today")

This is the strongest form of constructive guidance: the caller gets what they need without waiting.

**Discovery signal:** When a `resource-dedup` limit entry in the discovery endpoint returns the cached result instead of a 429 refusal, the entry SHOULD include `"returnsCached": true`. This tells agents they will receive a valid response (not a refusal) and can skip retry logic entirely.

```json
{
  "type": "resource-dedup",
  "maxRequests": 1,
  "windowSeconds": 86400,
  "returnsCached": true,
  "description": "One scan per domain per calendar day. Repeat requests return the cached result."
}
```

### 6. Response Classes

Graceful Boundaries applies to all HTTP responses, not just rate limits. Each response class has a base set of fields that make it self-explanatory.

**Core fields for all non-success responses:**

All non-success responses MUST include `error`, `detail`, and `why`. The `why` field explains the defensive, operational, or policy reason behind the response. Omitting `why` degrades the response to the same quality as a bare status code.

```json
{
  "error": "string — stable, machine-parseable error category",
  "detail": "string — human-readable explanation",
  "why": "string — the reason this response exists (security, policy, or operational)"
}
```

#### Class: Limit (429)

The caller exceeded a rate limit or cooldown.

| Field | Required | Purpose |
|---|---|---|
| `error` | Yes | `"rate_limit_exceeded"`, `"cooldown_active"`, `"resource_dedup"` |
| `detail` | Yes | Include specific wait time in human-readable form |
| `limit` | Yes | The exact limit (e.g., "10 scans per IP per hour") |
| `retryAfterSeconds` | Yes | Machine-parseable retry time |
| `why` | Yes | Security or operational reason for the limit |
| `alternativeEndpoint` | If applicable | A different endpoint that may serve the need |
| `cachedResultUrl` | If applicable | URL to a cached result for the same resource |
| `humanUrl` | Recommended | Browser-friendly fallback URL |

#### Class: Input (400, 405, 422)

The request was malformed, used the wrong method, or failed validation.

| Field | Required | Purpose |
|---|---|---|
| `error` | Yes | `"invalid_input"`, `"method_not_allowed"`, `"validation_failed"` |
| `detail` | Yes | What was wrong and how to fix it |
| `why` | Yes | Why this validation exists (e.g., SSRF protection) |
| `field` | If applicable | Which input field failed |
| `expected` | If applicable | What valid input looks like |
| `allowedMethods` | For 405 | Which HTTP methods are accepted |

```json
{
  "error": "invalid_input",
  "detail": "This URL points to a private or reserved address and cannot be scanned.",
  "why": "Siteline blocks private IPs, loopback, and cloud metadata endpoints to prevent server-side request forgery.",
  "field": "url",
  "expected": "A public URL with a resolvable hostname on port 80 or 443."
}
```

#### Class: Access (401, 403)

The caller lacks permission or credentials.

| Field | Required | Purpose |
|---|---|---|
| `error` | Yes | `"authentication_required"`, `"forbidden"`, `"blocked"` |
| `detail` | Yes | What credential or permission is needed |
| `why` | Yes | The security policy behind the restriction |
| `authUrl` | If applicable | Where to obtain credentials |
| `upgradeUrl` | If applicable | Where to get higher access |
| `humanUrl` | Recommended | Browser-friendly contact or signup page |

```json
{
  "error": "forbidden",
  "detail": "API key required for batch operations. Free scans are available at the public endpoint.",
  "why": "Batch access requires authentication to prevent abuse and track usage.",
  "authUrl": "https://example.com/api/keys",
  "alternativeEndpoint": "/api/scan"
}
```

#### Class: Not Found (404, 410)

The requested resource doesn't exist or has been removed.

| Field | Required | Purpose |
|---|---|---|
| `error` | Yes | `"not_found"`, `"gone"`, `"result_not_found"` |
| `detail` | Yes | Whether the resource never existed, expired, or moved |
| `why` | Yes | Why it might be missing (e.g., TTL expiration) |
| `scanAvailable` | If applicable | Whether the caller can create the resource |
| `scanUrl` | If applicable | Endpoint to create/scan the resource |
| `humanUrl` | Recommended | Browser-friendly page to take action |

```json
{
  "error": "result_not_found",
  "detail": "No scan result exists for example.com. This domain has not been scanned yet.",
  "why": "Results are kept for 30 days after scanning. This domain may not have been scanned, or the result may have expired.",
  "scanAvailable": true,
  "scanUrl": "/api/scan?url=https://example.com",
  "humanUrl": "https://siteline.to/?url=example.com"
}
```

#### Class: Availability (500, 502, 503, 504)

The service is experiencing an error or is temporarily unavailable.

| Field | Required | Purpose |
|---|---|---|
| `error` | Yes | `"internal_error"`, `"service_unavailable"`, `"upstream_error"`, `"timeout"` |
| `detail` | Yes | Whether this is transient and whether retrying is appropriate |
| `why` | Yes | What subsystem is affected |
| `retryAfterSeconds` | If applicable | When the service expects to recover |
| `statusUrl` | If applicable | Status page or health check endpoint |
| `humanUrl` | Recommended | Where to report the issue or get help |

```json
{
  "error": "service_unavailable",
  "detail": "Result storage is temporarily unavailable. Scans still work but results are not persisted.",
  "why": "The storage backend is unreachable. This is usually transient.",
  "retryAfterSeconds": 60,
  "humanUrl": "https://siteline.to/"
}
```

#### Class: Success (200, 201, 204)

Successful responses carry proactive information to prevent future errors.

| Header | When | Purpose |
|---|---|---|
| `RateLimit` | Always | Remaining budget: `limit=N, remaining=N, reset=N` |
| `RateLimit-Policy` | Always | Policy description: `N;w=N` |
| `X-Result-Id` | When applicable | Stable ID for the resource, for later retrieval |
| `X-Cache-Status` | When applicable | Whether the response was cached |

The proactive headers are the highest-leverage traffic reduction mechanism. A caller that sees `remaining=1` will self-throttle before the next request. A caller that sees `remaining=9` knows it has budget and won't add artificial delays.

## Conformance Levels

| Level | Requirements |
|---|---|
| **N/A: Not Applicable** | The site has no API endpoints, rate limits, or agentic interaction surface. There are no operational limits to communicate. |
| **Level 0: Non-Conformant** | The service enforces limits but does not describe them per this specification. Agents encounter bare `429`s, generic errors, or silent blocks with no structured explanation. |
| **Level 1: Structured Refusal** | All 429 responses include `error`, `detail`, `limit`, `retryAfterSeconds`, and `why`. |
| **Level 2: Discoverable** | Level 1 + a limits discovery endpoint exists and is accurate. |
| **Level 3: Constructive** | Level 2 + refusal responses include at least one constructive guidance field when applicable. |
| **Level 4: Proactive** | Level 3 + successful responses include proactive limit headers (RateLimit or equivalent). |

N/A and Level 0 are the default states for sites that have not adopted Graceful Boundaries. The difference between them is diagnostic: **N/A means there is nothing to conform to** (a static blog, a brochure site); **Level 0 means there is something to conform to but the service hasn't done it** (an API that returns bare `429`s). N/A is a classification. Level 0 is a gap.

### Self-Assertion and External Validation

A service MAY declare its own conformance level by including a `conformance` field in the limits discovery response (see section 1). This declaration is an **assertion**, not a guarantee. External agents, auditors, and conformance checkers validate the assertion against the service's actual behavior.

A service that declares Level 3 but returns bare `429`s is non-conformant regardless of its declaration. A site that declares N/A but enforces rate limits on API endpoints is misclassified. The declared level is the service's claim; the validated level is what an external evaluation confirms.

Services SHOULD target Level 3 or higher for agent-facing APIs.

## Examples

### Limits Discovery

```
GET /api/limits

200 OK
Content-Type: application/json
Cache-Control: s-maxage=3600

{
  "service": "Siteline",
  "limits": {
    "scan": {
      "endpoint": "/api/scan",
      "method": "GET",
      "limits": [
        {
          "type": "ip-rate",
          "maxRequests": 10,
          "windowSeconds": 3600,
          "description": "10 scans per IP per hour."
        },
        {
          "type": "resource-dedup",
          "maxRequests": 1,
          "windowSeconds": 86400,
          "description": "One scan per domain per calendar day."
        }
      ]
    }
  }
}
```

### Structured Refusal (Rate Limit)

```
GET /api/scan?url=example.com

429 Too Many Requests
Retry-After: 2400
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "detail": "You can run up to 10 scans per hour. Try again in 2400 seconds.",
  "limit": "10 scans per IP per hour",
  "retryAfterSeconds": 2400,
  "why": "Siteline is a free service. Rate limits keep it available for everyone and prevent abuse."
}
```

### Constructive Refusal (Resource Dedup)

```
GET /api/scan?url=example.com

200 OK
Content-Type: application/json

{
  "grade": "B",
  "score": 82,
  ...full result...,
  "_rescanBlocked": true,
  "_cacheStatus": "KV_HIT"
}
```

The caller gets the result. The `_rescanBlocked` flag tells agents and UIs that this is a cached result, not a fresh scan.

### Constructive Refusal (With Alternative)

```
GET /api/scan?url=example.com

429 Too Many Requests
Retry-After: 42
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "detail": "You can run up to 10 scans per hour. Try again in 42 seconds.",
  "limit": "10 scans per IP per hour",
  "retryAfterSeconds": 42,
  "why": "Rate limits keep the service available for everyone.",
  "cachedResultUrl": "/api/result?id=example-com-20260321",
  "alternativeEndpoint": "/api/result?id=example.com"
}
```

## Relationship to Existing Standards

| Standard | What it covers | What Graceful Boundaries adds |
|---|---|---|
| `draft-ietf-httpapi-ratelimit-headers` | Proactive headers on successful responses | Discovery endpoint, structured refusal body, `why` field, constructive guidance |
| RFC 6585 (429 status) | The status code itself | Structured body format with required fields |
| RFC 7807 / RFC 9457 (Problem Details) | Generic error response format | Specific required fields for rate limits (`limit`, `retryAfterSeconds`, `why`) and guidance categories |
| OpenAPI Rate Limit extensions | Documentation of limits in API specs | Runtime discovery endpoint, runtime refusal format |

Graceful Boundaries is complementary to these standards, not a replacement. A conforming service can (and should) also implement IETF RateLimit headers and use RFC 9457 Problem Details as the envelope format.

## Reference Implementation

[Siteline](https://siteline.to/) is a Level 4 conformant implementation of Graceful Boundaries. It is an AI agent readiness scanner with five API endpoints, each demonstrating different aspects of the specification.

**Verify conformance:**

```bash
node evals/check.js https://siteline.to
```

**Discovery endpoint:** [`/api/limits`](https://siteline.to/api/limits) — returns all rate limits, SSRF protection policy, response headers, and endpoint links.

**Proactive headers on successful responses:**

```
GET /api/scan?url=example.com

200 OK
RateLimit: limit=10, remaining=9, reset=3540
RateLimit-Policy: 10;w=3600
```

**Structured refusal with constructive guidance:**

```
GET /api/scan?url=example.com

429 Too Many Requests
Retry-After: 2400
RateLimit: limit=10, remaining=0, reset=2400
RateLimit-Policy: 10;w=3600

{
  "error": "rate_limit_exceeded",
  "detail": "You can run up to 10 scans per hour. Try again in 2400 seconds.",
  "limit": "10 scans per IP per hour",
  "retryAfterSeconds": 2400,
  "why": "Siteline is a free service. Rate limits keep it available for everyone and prevent abuse.",
  "alternativeEndpoint": "/api/result?id=example.com"
}
```

The `alternativeEndpoint` field directs the caller to the result lookup API, which may already have a cached result for the domain — the strongest form of constructive guidance.

**Resource deduplication (one scan per domain per day):**

```
GET /api/scan?url=example.com

200 OK

{
  "grade": "B",
  "score": 82,
  ...full result...,
  "_rescanBlocked": true,
  "_cacheStatus": "KV_HIT"
}
```

Rather than refusing with a 429, Siteline returns the cached result with a flag. The caller gets what they need without waiting.

**Source code:** The implementation is not open source, but the API is publicly accessible for conformance verification. The Graceful Boundaries eval suite can be run against it at any time.

## Security Considerations

Graceful Boundaries is designed around transparency. Transparency and security are in tension. This section defines constraints that prevent the specification from weakening the services that implement it.

**The core principle: be transparent about rules, not mechanisms.**

- "10 requests per hour" is a rule. Safe to disclose.
- "We use Redis with a sliding window" is an implementation. Not safe.
- "Blocks requests to non-public addresses" is a category. Safe to disclose.
- "Validates against RFC 1918 ranges plus a cloud metadata IP list" is a mechanism. Not safe.

### SC-1: Published Limits vs. Enforced Limits

The discovery endpoint describes the **policy**. Services MAY enforce stricter internal limits than published. This prevents callers from calibrating requests to stay exactly at the boundary.

A service that publishes "10 per hour" MAY internally enforce at 8 per hour. The published value is the contract ceiling, not the enforcement floor.

### SC-2: `why` Must Not Reveal Mechanisms

The `why` field MUST describe the **category** of protection, not the **implementation**.

- Good: "Blocks requests to non-public addresses."
- Bad: "Validates URLs against RFC 1918 ranges and cloud metadata endpoint IPs."

The `why` field exists to help callers understand the security model at a policy level, not to provide a roadmap for bypassing controls.

### SC-3: `expected` Must Use Positive Descriptions

The `expected` field in Input class responses MUST describe what valid input looks like in positive terms. It MUST NOT enumerate rejected patterns, as this reveals the filter logic.

- Good: "A public URL."
- Bad: "Not a private IP, not localhost, not port 8080."

### SC-4: Discovery Must Not List Non-Public Endpoints

The limits discovery endpoint MUST NOT include endpoints that are not intended for public use. Internal, admin, debug, or undocumented endpoints MUST be excluded.

### SC-5: Resource Existence Sensitivity

When resource existence is sensitive, services SHOULD return identical responses for never-existed and expired resources. The distinction between "never existed" and "expired" in the Not Found class is OPTIONAL and SHOULD only be used when existence is not sensitive.

For public resources (e.g., scan results on a public scanner), the distinction is acceptable and useful. For private resources (e.g., user profiles, private documents), use a uniform 404 with no existence signal.

### SC-6: Constructive Guidance URL Origin Restrictions

Constructive guidance URLs (`alternativeEndpoint`, `scanUrl`, `cachedResultUrl`) MUST be relative paths or same-origin absolute URLs. Cross-origin URLs MUST NOT appear in machine-actionable fields.

Cross-origin links are permitted only in `humanUrl` and `upgradeUrl`, which are intended for browser navigation, not automated following. This prevents response manipulation attacks where an intermediary modifies guidance URLs to redirect callers to attacker-controlled endpoints.

### SC-7: Proactive Header Jitter

Services MAY add small random jitter to `reset` values in proactive RateLimit headers to prevent callers from synchronizing with window boundaries. This mitigates burst attacks timed to window resets.

### SC-8: `scanUrl` Is Not a Trust Bypass

The `scanUrl` field in Not Found responses is a convenience URL. It does not bypass the scan endpoint's own input validation, SSRF protection, or rate limiting. The scan endpoint's security controls apply to all requests regardless of how the caller discovered the URL.

Services that include `scanUrl` MUST ensure the referenced endpoint has adequate input validation. Autonomous agents following `scanUrl` from untrusted contexts (e.g., a URL found in a web page) SHOULD treat it as untrusted input.

### SC-9: Content Cloaking via Agent-Signaling Headers

An origin detects agent intent (via `Accept: text/markdown`, known agent user-agents, or similar signals) and serves altered content designed to mislead, inject prompts, or misrepresent the site's offerings. CDN-level cache partitioning can prevent human visitors from seeing the divergent content, making the split undetectable through normal browsing.

This is distinct from user-agent blocking (which Graceful Boundaries addresses via structured refusal). Blocking is visible — the agent knows it was refused. Cloaking is invisible — the agent believes it received the real page.

**Mitigation:**

- Services claiming Level 4 conformance SHOULD NOT serve content via agent-signaling headers (e.g., `Accept: text/markdown`) that materially diverges from the HTML representation. Formatting differences are expected — markdown conversion strips boilerplate, and that is fine. Informational differences are not.
- Agents and scanners SHOULD compare content across request variants (standard HTML vs. `Accept: text/markdown`). The comparison SHOULD use an asymmetric containment metric — what fraction of the HTML's core text appears in the alternate response — rather than symmetric similarity, because legitimate conversions are asymmetric by design.
- Containment above 60% indicates legitimate conversion. Below 60% indicates the origin served materially different content. Implementations MAY use different thresholds depending on their context.

## FAQ

**Q: Should I use RFC 9457 (Problem Details for HTTP APIs) as the envelope format?**
A: Yes. The Graceful Boundaries fields can be included as extension members in a Problem Details response. The `type`, `title`, `status`, and `detail` fields from RFC 9457 map naturally to `error`, `limit`, the HTTP status code, and `detail` respectively.

**Q: What if my service has no constructive alternative to offer?**
A: That's fine. `retryAfterSeconds` is itself a next step. Level 1 conformance only requires the structured refusal. Constructive guidance is Level 3.

**Q: Should the limits discovery endpoint require authentication?**
A: No. Limits are not secrets (Principle 1). The discovery endpoint SHOULD be publicly accessible so agents can plan before authenticating.

**Q: What if my site has no API?**
A: Declare `not-applicable`. A static site, personal blog, or brochure page has no operational limits to communicate. Providing a limits discovery endpoint with `"conformance": "not-applicable"` and an empty `limits` object signals this to agents. Without the endpoint, agents cannot distinguish "no limits to communicate" from "hasn't heard of this spec."

**Q: What's the difference between Level 0 and N/A?**
A: N/A means the site has no agentic interaction surface — there are no limits to describe. Level 0 means the service enforces limits but doesn't describe them per this specification. N/A is a classification; Level 0 is a gap. A static blog is N/A. An API that returns bare `429`s is Level 0.

**Q: Can a service declare a higher level than it actually meets?**
A: It can declare any level, but the declaration is a self-assertion. External agents and conformance checkers validate the claim against actual behavior. A service declaring Level 3 but returning bare `429`s will be evaluated as Level 0 regardless of its declaration.

**Q: How does this apply to non-HTTP services?**
A: The principles and field names apply to any request-response protocol. The HTTP conventions (status codes, headers, endpoint paths) are transport-specific implementations of the general pattern.

## Appendix A: Implementation Notes

*This section is non-normative.*

### Edge and Worker Runtimes

Services running on edge runtimes (Vercel Edge Functions, Cloudflare Workers, Deno Deploy) construct responses using `new Response(body, { headers })` rather than `res.setHeader()`. Implementors SHOULD create a shared utility that returns rate limit headers as a plain object, usable in both traditional and edge contexts. The header names and values are identical regardless of the response construction API.

```javascript
// Shared utility — works in both Node.js and edge runtimes
function rateLimitHeaders(rateCheck) {
  return {
    "RateLimit": `limit=${rateCheck.limit}, remaining=${rateCheck.remaining}, reset=${rateCheck.reset}`,
    "RateLimit-Policy": `${rateCheck.limit};w=${rateCheck.window}`,
  };
}

// Traditional: res.setHeader()
const headers = rateLimitHeaders(rateCheck);
Object.entries(headers).forEach(([k, v]) => res.setHeader(k, v));

// Edge: new Response()
return new Response(body, { headers: { ...rateLimitHeaders(rateCheck), "Content-Type": "application/json" } });
```

### Agent Behavior When Discovery Fails

If an agent cannot fetch the limits discovery endpoint (network error, timeout, non-200 response), it SHOULD:

1. **Use conservative defaults.** Assume a rate limit of 1 request per second and back off exponentially on any `429` response.
2. **Respect `Retry-After` headers.** Even without discovery, the `Retry-After` header on `429` responses provides the minimum wait time.
3. **Retry discovery periodically.** Re-fetch the discovery endpoint every 1–6 hours for long-lived agent processes. The endpoint may have been temporarily unavailable.
4. **Log the failure.** Discovery endpoint unavailability is operationally significant — it means the agent is operating without a map.

An agent that cannot discover limits is not broken — it just loses the ability to plan ahead. The structured refusal responses (Level 1) still provide per-request guidance. Discovery failure degrades the agent from proactive to reactive, but does not require it to stop.

## Appendix B: Guidance for Autonomous Implementers

*This section is non-normative.*

This appendix addresses autonomous agents directly — both agents that build HTTP services and agents that consume them. The guidance below restates requirements from the normative sections in imperative form for ease of integration into agent instruction sets, context files, and system prompts.

### B.1: When You Are Building a Service

When you generate HTTP error responses, include three fields in every non-success response body: `error` (a stable snake_case string for programmatic matching), `detail` (a human-readable explanation), and `why` (the security, policy, or operational reason the limit exists). Do not omit `why` — it is the field that distinguishes an informative refusal from a bare block.

When you generate rate limit responses (429), include two additional fields: `limit` (the constraint in concrete terms, e.g., "10 requests per IP per hour") and `retryAfterSeconds` (a non-negative integer). Set the `Retry-After` HTTP header to match.

When you scaffold a new API or add endpoints to an existing one, add a limits discovery endpoint at `/api/limits` that returns all enforced limits as structured JSON. Include a `service` name, a `description`, a `conformance` level, and a `limits` object keyed by endpoint. Each limit entry needs `type`, `maxRequests`, `windowSeconds`, and `description`. Set `Cache-Control: public, s-maxage=3600` on the response.

When a cached or alternative result exists for a refused request, include `cachedResultUrl` or `alternativeEndpoint` in the refusal response body rather than returning a bare refusal. Prefer returning cached results as a 200 with `_rescanBlocked: true` over returning a 429 for resource deduplication limits.

When you add rate limit middleware, also add `RateLimit` and `RateLimit-Policy` headers to success responses so callers can self-throttle before hitting limits.

Apply the security considerations throughout: `why` describes the category of protection, not the implementation mechanism (SC-2). Guidance URLs use relative paths or same-origin absolute URLs (SC-6). Published limits in the discovery endpoint may be higher than actually enforced limits (SC-1). Do not include internal or admin endpoints in the discovery response (SC-4).

### B.2: When You Are Consuming a Service

Before making requests to a new service, check for a limits discovery endpoint at `/api/limits` or `/.well-known/limits`. If the endpoint exists, read the limits and plan your request patterns to stay within them. Do not discover limits through failure.

When you receive a 429 response, parse the JSON body before retrying. Use `retryAfterSeconds` to determine when to retry. Check for `alternativeEndpoint` or `cachedResultUrl` — these may let you get what you need without waiting. Read `why` to understand whether the limit is permanent policy, temporary congestion, or abuse prevention, and adjust your strategy accordingly.

When success responses include `RateLimit` headers, track the `remaining` value. When `remaining` approaches zero, slow your request rate proactively rather than waiting for a 429.

When a service returns a response with `_rescanBlocked: true`, the response body contains the cached result. Use it directly rather than retrying or waiting.

When discovery fails (network error, timeout, non-200 response), fall back to conservative defaults: assume a rate limit of 1 request per second, respect `Retry-After` headers on any 429, and re-check the discovery endpoint periodically. Discovery failure degrades you from proactive to reactive but does not require you to stop.
