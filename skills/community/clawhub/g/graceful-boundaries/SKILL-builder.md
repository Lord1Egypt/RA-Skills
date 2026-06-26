---
name: graceful-boundaries-builder
description: >
  Implement the Graceful Boundaries specification in a codebase that
  serves HTTP endpoints. Use this skill when building a new API, adding
  error handling to existing endpoints, implementing rate limiting,
  creating middleware for request validation, or generating 4xx/5xx
  response handlers. Also trigger when the user says "add graceful
  boundaries", "make this API agent-friendly", "add structured error
  responses", "implement limit discovery", or "add rate limit headers".
  Distinct from the graceful-boundaries-audit skill, which assesses
  existing live services via HTTP -- this skill modifies source code
  in the current project.
metadata:
  skill_bundle: graceful-boundaries-builder
  file_role: skill
  version: 1
  version_date: 2026-04-08
  author: PAICE.work PBC (paice.work)
  source: https://gracefulboundaries.dev
---

# Graceful Boundaries Builder

## What This Skill Does

Implements the Graceful Boundaries specification in the current
project's source code. Adds structured error responses, a limits
discovery endpoint, constructive guidance fields, and proactive
rate limit headers — progressively, one conformance level at a time.

The output is working code integrated into the project's existing
framework and patterns.

## When To Use This Skill

- Building a new API or HTTP server from scratch
- Adding error handling or rate limiting to existing endpoints
- User asks to make their API agent-friendly
- User asks to add structured error responses
- User asks to implement Graceful Boundaries at any level
- Creating middleware that returns 4xx or 5xx responses
- Refactoring error handling to be more informative

## When NOT To Use This Skill

- Assessing a live URL's conformance (use the audit skill instead)
- Working on a project with no HTTP endpoints
- The project already fully implements Graceful Boundaries

## Implementation Process

Follow these steps in order. Each level builds on the previous one.
Stop at whatever level is appropriate for the project.

### Step 1: Assess the Project

Before writing code, understand what exists:

1. Identify the framework (Express, Fastify, Next.js, Hono, raw Node,
   edge runtime, etc.)
2. Find existing error handling patterns — how does the project
   currently return errors? Is there a shared error handler or
   middleware?
3. Find existing rate limiting — is there rate limit middleware
   already in place? What library?
4. Check for an existing `/api/limits` or error response format

Adapt all code to match the project's existing patterns, conventions,
and framework. Do not introduce new dependencies.

### Step 2: Determine Target Level

Use this decision tree:

- **No API or agentic surface?** → Declare N/A (takes 5 minutes)
- **API with error responses?** → Level 1 (structured refusal)
- **API that agents will call?** → Level 2 (add discovery)
- **Can offer alternatives when refusing?** → Level 3 (constructive guidance)
- **High-traffic API?** → Level 4 (proactive headers)

Most projects should start at Level 1 and add Level 2. Levels 3 and 4
are for services with meaningful traffic from autonomous callers.

### Step 3: Implement Level 1 — Structured Refusal

Create a shared refusal helper that enforces the required fields.
Every non-success response MUST include `error`, `detail`, and `why`.
Every 429 MUST also include `limit` and `retryAfterSeconds`.

**Refusal helper (adapt to the project's framework):**

```javascript
function refusalResponse(res, status, fields) {
  const required = ["error", "detail", "why"];
  if (status === 429) required.push("limit", "retryAfterSeconds");
  for (const field of required) {
    if (!fields[field]) throw new Error(`Missing required field: ${field}`);
  }
  if (status === 429) {
    res.setHeader("Retry-After", String(fields.retryAfterSeconds));
  }
  res.status(status).json(fields);
}
```

**Apply to every error response in the project:**

```javascript
// 429 — rate limit exceeded
refusalResponse(res, 429, {
  error: "rate_limit_exceeded",
  detail: `You can make ${limit} requests per hour. Try again in ${resetSeconds} seconds.`,
  limit: `${limit} requests per IP per hour`,
  retryAfterSeconds: resetSeconds,
  why: "Rate limits keep the service available for all users and prevent abuse."
});

// 400 — invalid input
refusalResponse(res, 400, {
  error: "invalid_input",
  detail: "The 'email' field must be a valid email address.",
  why: "Input validation prevents malformed data from entering the system.",
  field: "email",
  expected: "A valid email address (e.g., user@example.com)."
});

// 404 — not found
refusalResponse(res, 404, {
  error: "not_found",
  detail: "No resource exists at this path.",
  why: "This endpoint requires a valid resource identifier."
});

// 500 — server error
refusalResponse(res, 500, {
  error: "internal_error",
  detail: "An unexpected error occurred. Try again shortly.",
  why: "Transient server errors are typically resolved within seconds.",
  retryAfterSeconds: 30
});
```

**Security considerations for Level 1:**
- `error` MUST be a stable snake_case string (e.g., `rate_limit_exceeded`),
  not a human-readable sentence
- `why` MUST describe the category of protection, not the mechanism.
  Good: "Rate limits prevent abuse." Bad: "Our nginx proxy returns 429
  when the token bucket empties." (SC-2)
- `expected` MUST use positive descriptions ("A public URL on port 80
  or 443"), not negative ones that reveal filters ("Not a private IP
  or metadata endpoint") (SC-3)

### Step 4: Implement Level 2 — Discovery Endpoint

Add a `/api/limits` endpoint that describes all enforced limits as
structured JSON. This lets agents learn the rules before breaking them.

```javascript
app.get("/api/limits", (req, res) => {
  res.setHeader("Cache-Control", "public, s-maxage=3600");
  res.json({
    service: "<service name>",
    description: "<what the service does, in one sentence>",
    conformance: "level-2",
    limits: {
      "<endpoint-key>": {
        endpoint: "/api/<path>",
        method: "GET",
        limits: [
          {
            type: "ip-rate",
            maxRequests: 100,
            windowSeconds: 3600,
            description: "100 requests per IP per hour."
          }
        ]
      }
      // Add an entry for every rate-limited endpoint
    }
  });
});
```

**Populate the limits object** by surveying every endpoint in the
project that has rate limiting. Each entry needs:
- `endpoint`: the path
- `method`: HTTP method (GET, POST, etc.)
- `limits`: array of limit objects, each with `type`, `maxRequests`,
  `windowSeconds`, and `description`

**Security considerations for Level 2:**
- Do NOT include internal or admin endpoints in the discovery
  response (SC-4)
- Published limits MAY be higher than actually enforced limits —
  this is fine and even recommended as a security measure (SC-1)
- Add `Cache-Control: public, s-maxage=3600` so agents don't
  re-fetch on every request

### Step 5: Implement Level 3 — Constructive Guidance

When refusing a request, include a useful next step instead of just
blocking. Add these fields to refusal responses where applicable:

```javascript
if (rateLimitExceeded) {
  const guidance = {};

  // If a cached result exists, point to it
  if (cachedResult) {
    guidance.cachedResultUrl = `/api/result?id=${resourceId}`;
  }

  // If a lighter endpoint can help
  if (alternativeAvailable) {
    guidance.alternativeEndpoint = `/api/lightweight?id=${resourceId}`;
  }

  // If paid access has higher limits
  if (hasPaidTier) {
    guidance.upgradeUrl = "/pricing";
  }

  // Always include a human escalation path
  guidance.humanUrl = "/contact";

  refusalResponse(res, 429, {
    error: "rate_limit_exceeded",
    detail: `Try again in ${resetSeconds} seconds.`,
    limit: `${limit} requests per hour`,
    retryAfterSeconds: resetSeconds,
    why: "Rate limits keep the service available for all users.",
    ...guidance
  });
}
```

**For resource deduplication** (same resource requested within a window),
return the cached result as a 200 instead of a 429:

```javascript
if (alreadyProcessedRecently) {
  res.json({
    ...cachedResult,
    _rescanBlocked: true
  });
  return;
}
```

And mark it in the discovery endpoint:

```json
{
  "type": "resource-dedup",
  "maxRequests": 1,
  "windowSeconds": 86400,
  "returnsCached": true,
  "description": "One scan per resource per day. Returns cached result."
}
```

**Security considerations for Level 3:**
- Guidance URLs (`cachedResultUrl`, `alternativeEndpoint`) MUST be
  relative paths or same-origin absolute URLs (SC-6)
- `upgradeUrl` and `humanUrl` MAY be cross-origin

### Step 6: Implement Level 4 — Proactive Headers

Add `RateLimit` and `RateLimit-Policy` headers to every successful
response so callers can self-throttle before hitting limits.

```javascript
function addRateLimitHeaders(res, rateCheck) {
  res.setHeader("RateLimit",
    `limit=${rateCheck.limit}, remaining=${rateCheck.remaining}, reset=${rateCheck.reset}`
  );
  res.setHeader("RateLimit-Policy",
    `${rateCheck.limit};w=${rateCheck.window}`
  );
}

// Add to every success response on rate-limited endpoints
addRateLimitHeaders(res, rateCheck);
res.json(result);
```

**Edge runtime variant:**

```javascript
function rateLimitHeaders(rateCheck) {
  return {
    "RateLimit": `limit=${rateCheck.limit}, remaining=${rateCheck.remaining}, reset=${rateCheck.reset}`,
    "RateLimit-Policy": `${rateCheck.limit};w=${rateCheck.window}`,
  };
}

return new Response(JSON.stringify(result), {
  headers: {
    ...rateLimitHeaders(rateCheck),
    "Content-Type": "application/json"
  }
});
```

Update the discovery endpoint `conformance` field to `"level-4"`.

### Step 7: Verify

After implementation, verify conformance using the checker:

```bash
# Clone the spec repo if not already available
git clone https://github.com/snapsynapse/graceful-boundaries.git
cd graceful-boundaries

# Check the service
node evals/check.js https://localhost:3000
node evals/check.js https://localhost:3000 --json
```

The checker validates:
- Discovery endpoint is well-formed (Level 2)
- Proactive headers are present on success responses (Level 4)
- Level 1 and Level 3 require a 429 response to verify — trigger
  one manually and check the response body

## What This Skill Does NOT Do

- Does not assess live URLs (use the audit skill for that)
- Does not introduce external dependencies
- Does not replace existing error handling that already works — it
  enhances the response format
- Does not implement the actual rate limiting logic — only the
  communication layer around it
