---
name: graceful-boundaries-audit
description: >
  Assess any API or website's Graceful Boundaries conformance level and
  provide concrete guidance for reaching the next level. Use this skill
  when the user asks to check a URL's rate limit communication, evaluate
  API conformance to Graceful Boundaries, assess how a service handles
  429s, or improve how an API communicates its limits to agents. Also
  trigger when the user says "check this API's boundaries", "what level
  is this service", "assess graceful boundaries compliance", "how does
  this API handle rate limits", or provides a URL and asks about rate
  limit quality, conformance, or structured refusal. Distinct from the
  agent-readiness-audit skill, which assesses overall AI discoverability
  -- this skill specifically evaluates rate limit communication quality
  per the Graceful Boundaries specification.
metadata:
  skill_bundle: graceful-boundaries-audit
  file_role: skill
  version: 3
  version_date: 2026-03-26
  previous_version: 2
  change_summary: >
    Updated for spec v1.1.0. Gap analysis now checks why on all response
    classes (not just 429s), changelog/feed discovery fields, returnsCached
    flag on resource-dedup entries, and HTML 429 machine-accessibility.
    Discovery skeleton includes changelog and feed fields.
  author: PAICE.work PBC (paice.work)
  source: https://gracefulboundaries.dev
---

# Graceful Boundaries Conformance Audit

## What This Skill Does

Assesses a URL's Graceful Boundaries conformance level through direct
HTTP inspection, then provides a concrete implementation plan for
reaching the next level. The output is an actionable document with
code examples the user can implement immediately. No special tooling
or dependencies required — the skill works with any HTTP client.

## When To Use This Skill

- User provides a URL and asks about its rate limit communication
- User asks to check Graceful Boundaries conformance for a service
- User wants to know what level an API is at
- User asks how to improve their API's 429 responses
- User wants to elevate from one conformance level to the next
- User says "audit this API" in the context of rate limits or boundaries

## Assessment Process

Follow these phases in order. Each phase builds on the previous one.

### Phase 1: Discovery Fetch

Fetch the limits discovery endpoint directly. Try both standard paths:

```
GET <url>/api/limits
GET <url>/.well-known/limits
```

Use curl, fetch, or any HTTP client available in the current environment.
No special tooling is required.

If either path returns a JSON response, record:
- Whether the response contains a `service` field
- Whether the response contains a `limits` object
- Whether limit entries are well-formed (each has `type`, `maxRequests`,
  `windowSeconds`, `description`)
- Whether a `conformance` field is present (self-declared level)
- Whether the response includes a `Cache-Control` header with `s-maxage`
- Whether `changelog` or `feed` URLs are present (v1.1 change discovery)
- Whether `resource-dedup` entries include `returnsCached: true` (v1.1)

If neither path returns a valid response, the service has no discovery
endpoint and cannot be Level 2 or above.

**Optional accelerator:** If the graceful-boundaries repo is cloned
locally, the automated checker provides a structured report:

```bash
node evals/check.js <url> --json
```

This is a convenience, not a requirement. The skill works entirely
through direct HTTP inspection.

### Phase 2: Proactive Header Check

If the limits endpoint documents specific API endpoints, fetch one of
them and check for proactive headers on the success response:
- `RateLimit: limit=N, remaining=N, reset=N`
- `RateLimit-Policy: N;w=N`

These headers indicate Level 4 conformance.

**Do NOT attempt to trigger 429s.** That would require hammering the
service and is not appropriate for an audit. Level 1 and Level 3
conformance cannot be verified without observing an actual refusal
response — note these as unverifiable and explain why.

### Phase 3: Level Assessment

Map findings to the conformance levels defined in spec.md:

| Level | How to verify |
|---|---|
| N/A | Site has no API or agentic surface |
| 0 | Service exists but no limits endpoint, no structured responses |
| 1 | Cannot verify without a 429 response (note as unverifiable) |
| 2 | Limits endpoint exists and is well-formed |
| 3 | Cannot verify without a 429 response (note as unverifiable) |
| 4 | Level 2 confirmed + proactive headers present on success responses |

If the service self-declares a conformance level via the `conformance`
field, compare declared vs. validated. Flag any discrepancy.

Report the assessment as:
- **Confirmed level**: what the evidence supports
- **Declared level**: what the service claims (if any)
- **Likely level**: best estimate including unverifiable aspects

### Phase 4: Gap Analysis

For each level above the current confirmed level, list exactly what is
missing. Reference specific sections of spec.md:

**To reach Level 1** (spec sections 2 and 6):
- Do ALL non-success responses (400, 401, 403, 404, 429, 500, 503) include
  `error`, `detail`, and `why`? (v1.1: `why` is MUST for all error classes)
- Are 429 responses JSON with the 5 required fields (`error`, `detail`,
  `limit`, `retryAfterSeconds`, `why`)?
- Does `error` use a stable machine-parseable string (snake_case)?
- Does `detail` include a specific retry time in human-readable form?
- Does `why` explain the purpose, not restate the error?
- Is `retryAfterSeconds` a non-negative integer?
- Does the HTTP response include a `Retry-After` header?
- For HTML 429 pages: is there a `<meta name="retry-after" content="N">`
  tag or a `<link rel="alternate" type="application/json" href="...">`? (v1.1)

**To reach Level 2** (spec section 1):
- Does a limits endpoint exist at `/api/limits` or `/.well-known/limits`?
- Does it return JSON with a `limits` object?
- Are limit entries well-formed (type, maxRequests, windowSeconds, description)?
- Is the endpoint cacheable (Cache-Control header)?
- Does it include `changelog` or `feed` URLs for change discovery? (v1.1, optional but recommended)

**To reach Level 3** (spec sections 3 and 5):
- Do refusal responses include constructive guidance fields?
- Which guidance categories apply? (`cachedResultUrl`, `alternativeEndpoint`,
  `upgradeUrl`, `humanUrl`, `cached`)
- Does the service prefer guidance in the recommended order:
  use cached > try alternative > upgrade > wait > human handoff?
- For `resource-dedup` limits: does the service return cached results as a
  200 instead of a 429? If so, does the discovery endpoint include
  `returnsCached: true` so agents skip retry logic? (v1.1)

**To reach Level 4** (spec section 4):
- Are `RateLimit` headers present on success responses?
- Do they include all three components: `limit`, `remaining`, `reset`?
- Is a `RateLimit-Policy` header present?
- Does the policy format match `N;w=N`?

### Phase 5: Implementation Guidance

Provide concrete, copy-pasteable code for each gap. Use the service's
actual domain and endpoints in examples.

**Limits discovery endpoint skeleton:**
```json
{
  "service": "<service name>",
  "description": "<what the service does>",
  "conformance": "level-2",
  "changelog": "https://<domain>/api/changelog.json",
  "feed": "https://<domain>/feed.json",
  "limits": {
    "<endpoint-key>": {
      "endpoint": "<path>",
      "method": "<HTTP method>",
      "limits": [
        {
          "type": "ip-rate",
          "maxRequests": 100,
          "windowSeconds": 3600,
          "description": "100 requests per IP per hour."
        },
        {
          "type": "resource-dedup",
          "maxRequests": 1,
          "windowSeconds": 86400,
          "returnsCached": true,
          "description": "One operation per resource per day. Repeat requests return the cached result."
        }
      ]
    }
  }
}
```

**Structured refusal body:**
```json
{
  "error": "rate_limit_exceeded",
  "detail": "You have exceeded the limit of 100 requests per hour. Try again in <N> seconds.",
  "limit": "100 requests per IP per hour",
  "retryAfterSeconds": 1234,
  "why": "<one sentence explaining why this limit exists — not just restating the error>"
}
```

**Constructive guidance fields** (add to the refusal body):
```json
{
  "cachedResultUrl": "/api/result?id=<resource>",
  "alternativeEndpoint": "/api/<alternative>",
  "upgradeUrl": "https://<domain>/pricing",
  "humanUrl": "https://<domain>/contact"
}
```

**Proactive headers** (add to success responses):
```
RateLimit: limit=100, remaining=99, reset=3600
RateLimit-Policy: 100;w=3600
```

Reference security considerations where relevant:
- SC-1: Published limits may be higher than enforced limits
- SC-2: `why` must describe the category of protection, not the mechanism
- SC-3: `expected` must use positive descriptions
- SC-6: Guidance URLs must be relative or same-origin

### Phase 6: Generate the Assessment Document

Output a structured markdown document:

```
# Graceful Boundaries Assessment: <domain>

## Summary
- Confirmed level: <N>
- Declared level: <N or "not declared">
- Likely level: <N>

## What was checked
- Limits endpoint: <path> — <found/not found>
- Proactive headers: <present/absent>
- Refusal format: <not verifiable without triggering a 429>

## Gaps to next level
<prioritized list with spec section references>

## Implementation plan
<concrete code examples using the service's actual domain>

## Security notes
<relevant SC-* considerations>
```

## What This Skill Does NOT Do

- Does not implement changes on the target service
- Does not deliberately trigger rate limits or 429 responses
- Does not require access to the service's source code
- Does not assess general API design quality beyond limit communication
- Is distinct from the agent-readiness-audit skill (which assesses
  overall AI discoverability, not rate limit conformance specifically)
