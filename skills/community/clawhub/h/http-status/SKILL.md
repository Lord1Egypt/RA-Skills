---
name: http-status
description: HTTP status code reference — instant lookup of any status code with meaning, common causes, and fix suggestions. Use when the user asks about an HTTP status code, gets an error response from an API, or needs to understand what a 4xx/5xx means. Covers all RFC-standard codes plus WebDAV, Nginx, Cloudflare, and common unofficial codes. No API key, no network — fully offline lookup table.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🔢"
---

# HTTP Status Code Reference

Instant lookup for any HTTP status code — meaning, common causes, and how to fix it.
Full data table in `references/codes.md`. Zero dependencies, fully offline.

## When to use

- "What does 429 mean?"
- "I'm getting a 502 from my API, what's wrong?"
- "What's the difference between 401 and 403?"
- "Which 5xx errors are retryable?"
- "What does Cloudflare 524 mean?"

---

## Code ranges (quick orientation)

```
1xx  Informational  — request received, continue processing
2xx  Success        — request was received, understood, accepted
3xx  Redirection    — further action needed to complete the request
4xx  Client Error   — request contains bad syntax or cannot be fulfilled
5xx  Server Error   — server failed to fulfil an apparently valid request
```

---

## Lookup procedure

1. Check `references/codes.md` for the exact code
2. If not found, infer from the range (4xx = client error, 5xx = server error)
3. Note the source category: RFC standard / WebDAV / Nginx / Cloudflare / unofficial
4. Return: meaning + common causes + recommended action

---

## Output format

### Single code lookup

```
🔢 HTTP 429 — Too Many Requests
━━━━━━━━━━━━━━━━━━━━
Category:   4xx Client Error
Standard:   RFC 6585
Meaning:    The user has sent too many requests in a given time (rate limiting).

Common causes:
  • API rate limit exceeded
  • Burst traffic hitting a throttling policy
  • Forgot to handle Retry-After header

What to do:
  • Check the Retry-After response header for wait time
  • Implement exponential backoff in your client
  • Review your request frequency and add throttling logic
  • Consider caching responses to reduce request volume

Related codes:  503 (server overloaded)
```

### Comparison query

```
🔢 401 vs 403
━━━━━━━━━━━━━━━━━━━━
401 Unauthorized
  → Authentication is required and has failed or not been provided
  → "You need to log in first"
  → Fix: provide valid credentials / token

403 Forbidden
  → Server understood the request but refuses to authorize it
  → "You're logged in but don't have permission"
  → Fix: check user roles/permissions, contact admin

Key difference:
  401 = identity unknown (not authenticated)
  403 = identity known but access denied (not authorized)
```

### Retryable codes

```
✅ Generally safe to retry (with backoff):
  408  Request Timeout
  429  Too Many Requests       ← respect Retry-After header
  500  Internal Server Error   ← transient server issues
  502  Bad Gateway             ← upstream temporarily unavailable
  503  Service Unavailable     ← server overloaded/maintenance
  504  Gateway Timeout         ← upstream timeout

❌ Do NOT retry blindly:
  400  Bad Request             ← fix your request first
  401  Unauthorized            ← re-authenticate first
  403  Forbidden               ← retrying won't help
  404  Not Found               ← resource doesn't exist
  422  Unprocessable Entity    ← fix validation errors first
```

---

## Notes

- For Nginx-specific codes (444, 494-499) and Cloudflare codes (520-530), see `references/codes.md`
- 418 "I'm a teapot" is a real RFC 2324 status — implemented as an Easter egg in some servers
- Some codes (e.g. 103, 425, 451) are newer and may not be supported by all clients/proxies
