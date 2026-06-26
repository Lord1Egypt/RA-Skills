# Graceful Boundaries: curl Examples

All examples use [Siteline](https://siteline.to/), a Level 4 conformant reference implementation. Replace the URLs with your own service to test conformance.

## 1. Discover limits

Fetch all enforced limits before hitting any of them:

```bash
curl -s https://siteline.to/api/limits | jq .
```

Check the standard well-known path:

```bash
curl -s https://your-service.com/.well-known/limits | jq .
```

A conforming discovery response includes `service`, `limits`, and optionally `conformance`, `changelog`, and `feed`:

```json
{
  "service": "Siteline",
  "description": "AI agent readiness scanner for public websites.",
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
          "type": "domain-dedup",
          "maxRequests": 1,
          "windowSeconds": 86400,
          "description": "One scan per domain per calendar day."
        }
      ]
    }
  }
}
```

## 2. Read a structured refusal

When a limit is exceeded, a conforming service returns all five required fields:

```json
{
  "error": "rate_limit_exceeded",
  "detail": "You can run up to 10 scans per hour. Try again in 2400 seconds.",
  "limit": "10 scans per IP per hour",
  "retryAfterSeconds": 2400,
  "why": "Siteline is a free service. Rate limits keep it available for everyone and prevent abuse."
}
```

Key fields:
- `error` -- stable string for programmatic matching (snake_case)
- `detail` -- human-readable with specific wait time
- `limit` -- the exact constraint in concrete terms
- `retryAfterSeconds` -- machine-parseable retry time
- `why` -- explains the *purpose* of the limit, not just restates the error

## 3. Check for constructive guidance

A Level 3 refusal includes fields that help the caller take action beyond waiting:

```json
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

Guidance categories (in recommended priority order):
- `cachedResultUrl` -- a cached result exists for the same resource
- `alternativeEndpoint` -- a different endpoint can serve the need
- `upgradeUrl` -- paid or authenticated access has higher limits
- `humanUrl` -- a browser-friendly URL for human follow-up

## 4. Non-429 response classes

Graceful Boundaries applies to all non-success responses, not just rate limits. Every error MUST include `error`, `detail`, and `why`.

**Input validation (400):**

```json
{
  "error": "invalid_input",
  "detail": "This URL points to a private or reserved address and cannot be scanned.",
  "why": "Siteline blocks private IPs, loopback, and cloud metadata endpoints to prevent server-side request forgery.",
  "field": "url",
  "expected": "A public URL with a resolvable hostname on port 80 or 443."
}
```

**Not Found with creation path (404):**

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

**Service unavailable (503):**

```json
{
  "error": "service_unavailable",
  "detail": "Result storage is temporarily unavailable. Scans still work but results are not persisted.",
  "why": "The storage backend is unreachable. This is usually transient.",
  "retryAfterSeconds": 60
}
```

## 5. HTML 429 machine-accessibility

HTML pages that return 429 should include machine-readable hints so agents don't have to parse prose:

```html
<meta name="retry-after" content="42" />
<link rel="alternate" type="application/json" href="/api/scan?format=json" />
```

The `<meta>` tag provides the retry time. The `<link>` tag points to the JSON-structured refusal. Either alone is sufficient for agent consumption.

## 6. Inspect proactive headers

Check for `RateLimit` headers on a successful response:

```bash
curl -s 'https://siteline.to/api/result?id=example.com' \
  -D - -o /dev/null 2>&1 | grep -i ratelimit
```

```
ratelimit: limit=60, remaining=59, reset=60
ratelimit-policy: 60;w=60
```

The three components of the `RateLimit` header:
- `limit` -- maximum requests in the window
- `remaining` -- requests left before the limit is hit
- `reset` -- seconds until the window resets

## 7. Run the conformance checker

The eval suite includes a live checker that tests a service against all conformance levels:

```bash
# Human-readable output
node evals/check.js https://siteline.to

# Machine-readable JSON
node evals/check.js https://siteline.to --json

# Custom limits endpoint path
node evals/check.js https://your-service.com --limits-path /.well-known/limits
```

## 8. Agent integration pattern

An autonomous agent interacting with a Graceful Boundaries-conformant service should follow this sequence:

**Step 1: Discover limits first.**

```bash
curl -s https://example.com/api/limits
```

Parse the response. Know the rate limits before making any requests. Cache the limits response (respect `Cache-Control`).

**Step 2: Monitor proactive headers.**

On every successful response, read the `RateLimit` header. When `remaining` is low, slow down. When `remaining=0`, stop and wait for `reset` seconds.

**Step 3: Handle refusals constructively.**

When you receive a 429:
1. Read `retryAfterSeconds` -- do not retry before this time.
2. Check for `cachedResultUrl` -- if present, fetch the cached result instead.
3. Check for `alternativeEndpoint` -- if present, try the alternative.
4. Read `why` -- understand the security model. Adjust behavior accordingly.
5. Only if no alternative exists, wait and retry after the specified time.

**Step 4: Never retry blindly.**

A structured refusal tells you everything you need to decide what to do next. If `alternativeEndpoint` gives you what you need, there is no reason to retry the original request at all.
