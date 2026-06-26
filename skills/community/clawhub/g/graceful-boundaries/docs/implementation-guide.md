# Implementation Guide

A step-by-step guide for adding Graceful Boundaries conformance to an existing HTTP API. Each level builds on the previous one. Start at Level 1 and progress as far as makes sense for your service.

## Before you start

**Prerequisite:** Your service already enforces rate limits or operational constraints. If it doesn't, you may want to declare `not-applicable` (see [Level N/A](#level-na-not-applicable) below).

**Time estimate per level:**

| Level | Effort | What changes |
|---|---|---|
| N/A | 5 minutes | Add one endpoint |
| 1 | 1–2 hours | Modify error response format |
| 2 | 30–60 minutes | Add a discovery endpoint |
| 3 | 30–60 minutes | Add fields to existing refusals |
| 4 | 30–60 minutes | Add headers to success responses |

## Level N/A: Not Applicable

For sites with no API, no rate limits, and no agentic interaction surface (blogs, brochure sites, documentation).

Add a discovery endpoint that signals awareness:

```javascript
// GET /api/limits or GET /.well-known/limits
app.get("/api/limits", (req, res) => {
  res.json({
    service: "My Blog",
    description: "Personal blog. No API or agentic services.",
    conformance: "not-applicable",
    limits: {}
  });
});
```

This distinguishes "we have nothing to disclose" from "we haven't heard of this spec." Agents that discover this endpoint know they can stop probing.

## Level 1: Structured Refusal

**Goal:** Every non-success response includes `error`, `detail`, and `why`. Every `429` adds `limit` and `retryAfterSeconds`.

### Step 1: Create a refusal response helper

```javascript
function refusalResponse(res, status, fields) {
  // Validate required fields
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

### Step 2: Replace bare error responses

**Before (Level 0):**
```javascript
if (rateLimitExceeded) {
  res.status(429).json({ error: "Too many requests" });
}
```

**After (Level 1):**
```javascript
if (rateLimitExceeded) {
  refusalResponse(res, 429, {
    error: "rate_limit_exceeded",
    detail: `You can make ${limit} requests per hour. Try again in ${resetSeconds} seconds.`,
    limit: `${limit} requests per IP per hour`,
    retryAfterSeconds: resetSeconds,
    why: "Rate limits keep the service available for all users and prevent abuse."
  });
}
```

### Step 3: Apply to all error classes

Level 1 isn't just about 429s. Every error response should include `error`, `detail`, and `why`:

```javascript
// 400 — Input validation
refusalResponse(res, 400, {
  error: "invalid_input",
  detail: "The 'email' field must be a valid email address.",
  why: "Email validation prevents malformed data from entering the system.",
  field: "email",
  expected: "A valid email address (e.g., user@example.com)"
});

// 404 — Not found
refusalResponse(res, 404, {
  error: "not_found",
  detail: "No user exists with ID 12345.",
  why: "User records are permanent. If a user was never created, this ID is invalid."
});

// 500 — Internal error
refusalResponse(res, 500, {
  error: "internal_error",
  detail: "The database connection pool is exhausted. This is usually transient.",
  why: "The storage backend is under heavy load.",
  retryAfterSeconds: 30
});
```

### Security note

The `why` field describes the **category** of protection, not the **mechanism**:

- Good: "Blocks requests to non-public addresses."
- Bad: "Validates URLs against RFC 1918 ranges and cloud metadata IPs."

See [SC-2 in the security audit](../SECURITY-AUDIT.md) for details.

## Level 2: Discoverable

**Goal:** Add a limits discovery endpoint so agents can learn the rules before breaking them.

### Step 1: Create the discovery endpoint

```javascript
app.get("/api/limits", (req, res) => {
  res.setHeader("Cache-Control", "s-maxage=3600");
  res.json({
    service: "My API",
    description: "What your service does, in one sentence.",
    conformance: "level-2",
    limits: {
      users: {
        endpoint: "/api/users",
        method: "GET",
        limits: [
          {
            type: "ip-rate",
            maxRequests: 100,
            windowSeconds: 3600,
            description: "100 requests per IP per hour."
          }
        ]
      },
      createUser: {
        endpoint: "/api/users",
        method: "POST",
        limits: [
          {
            type: "ip-rate",
            maxRequests: 10,
            windowSeconds: 3600,
            description: "10 account creations per IP per hour."
          },
          {
            type: "cooldown",
            maxRequests: 1,
            windowSeconds: 60,
            description: "One creation request per minute."
          }
        ]
      }
    }
  });
});
```

### Step 2: Keep it accurate

The discovery endpoint is a contract. If your actual limits don't match what the endpoint says, agents will make wrong decisions. Update the endpoint whenever you change limits.

**The published limit is a ceiling, not the exact enforcement threshold.** You MAY enforce stricter internal limits than published (see [SC-1](../SECURITY-AUDIT.md)). But the discovery endpoint MUST NOT overstate limits — an agent that plans around "100 per hour" shouldn't hit a wall at 50.

### Step 3: Only list public endpoints

The discovery endpoint MUST NOT include internal, admin, or debug endpoints. See [SC-4](../SECURITY-AUDIT.md).

## Level 3: Constructive

**Goal:** Refusal responses include a useful next step beyond "wait."

### Step 1: Add guidance fields to 429 responses

```javascript
if (rateLimitExceeded) {
  const guidance = {};

  // Prefer cached result if available
  if (cachedResult) {
    guidance.cachedResultUrl = `/api/result?id=${resourceId}`;
  }

  // Offer alternative endpoint if applicable
  if (alternativeAvailable) {
    guidance.alternativeEndpoint = `/api/lightweight-result?id=${resourceId}`;
  }

  // Always include human fallback
  guidance.humanUrl = "https://example.com/contact";

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

### Step 2: For resource-dedup limits, return the cached result

The strongest form of constructive guidance is returning what the caller needs without making them wait:

```javascript
if (alreadyProcessedToday) {
  // Return the cached result as a 200, not a 429
  res.json({
    ...cachedResult,
    _rescanBlocked: true
  });
}
```

Add `returnsCached: true` to the discovery endpoint so agents know to expect a `200` with data, not a `429`:

```json
{
  "type": "resource-dedup",
  "maxRequests": 1,
  "windowSeconds": 86400,
  "returnsCached": true,
  "description": "One processing per resource per day. Repeat requests return the cached result."
}
```

### Guidance priority

Prefer guidance in this order: use cached > try alternative > upgrade > wait > human handoff. The first applicable category wins.

## Level 4: Proactive

**Goal:** Successful responses include headers that tell callers their remaining budget.

### Step 1: Add RateLimit headers to success responses

```javascript
function addRateLimitHeaders(res, rateCheck) {
  res.setHeader("RateLimit",
    `limit=${rateCheck.limit}, remaining=${rateCheck.remaining}, reset=${rateCheck.reset}`
  );
  res.setHeader("RateLimit-Policy", `${rateCheck.limit};w=${rateCheck.window}`);
}

// In your request handler, after the rate check passes:
addRateLimitHeaders(res, rateCheck);
res.json(result);
```

### Step 2: Edge runtime variant

Edge runtimes (Vercel Edge Functions, Cloudflare Workers, Deno Deploy) use `new Response()` instead of `res.setHeader()`. Create a shared utility:

```javascript
function rateLimitHeaders(rateCheck) {
  return {
    "RateLimit": `limit=${rateCheck.limit}, remaining=${rateCheck.remaining}, reset=${rateCheck.reset}`,
    "RateLimit-Policy": `${rateCheck.limit};w=${rateCheck.window}`,
  };
}

// Edge runtime
return new Response(JSON.stringify(result), {
  headers: {
    ...rateLimitHeaders(rateCheck),
    "Content-Type": "application/json"
  }
});
```

### Step 3: Update your conformance declaration

```json
{
  "conformance": "level-4"
}
```

## Verifying your implementation

Run the conformance checker against your service:

```bash
# Basic check
node evals/check.js https://your-service.com

# Custom limits endpoint path
node evals/check.js https://your-service.com --limits-path /.well-known/limits

# Machine-readable output
node evals/check.js https://your-service.com --json
```

Run the unit tests to validate response format correctness:

```bash
npm test
```

## Using RFC 9457 (Problem Details) as the envelope

The Graceful Boundaries fields work as extension members in a Problem Details response:

```json
{
  "type": "https://example.com/problems/rate-limit",
  "title": "Rate Limit Exceeded",
  "status": 429,
  "detail": "You can make 10 requests per hour. Try again in 42 seconds.",
  "limit": "10 requests per IP per hour",
  "retryAfterSeconds": 42,
  "why": "Rate limits keep the service available for all users.",
  "cachedResultUrl": "/api/result?id=example"
}
```

The `type`, `title`, `status`, and `detail` fields from RFC 9457 map naturally to `error`, `limit`, the HTTP status code, and `detail` respectively.
