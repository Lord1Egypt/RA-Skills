# Graceful Boundaries

A specification for how services communicate their operational limits to humans and autonomous agents.

**[gracefulboundaries.dev](https://gracefulboundaries.dev)**

[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](CHANGELOG.md)
[![Tests](https://img.shields.io/github/actions/workflow/status/snapsynapse/graceful-boundaries/test.yml?label=tests)](https://github.com/snapsynapse/graceful-boundaries/actions)
[![ClawHub](https://img.shields.io/badge/ClawHub-83%20installs-blue)](https://clawhub.ai/snapsynapse/graceful-boundaries)

## The problem

Every unclear response generates follow-up traffic. A vague `429` causes blind retries. A vague `403` causes re-attempts with different credentials. A generic `500` causes indefinite retries. When autonomous agents are the caller, the waste compounds: agents retry faster, probe more systematically, and lack the human judgment to know when to stop.

Most services enforce rate limits but communicate them poorly. A `429 Too Many Requests` with `Retry-After: 60` tells a retry loop what to do. It doesn't tell an autonomous agent whether to retry, use a cached result, try a different endpoint, or inform the human. It doesn't tell a developer what the limits are before they hit them. It doesn't tell anyone *why* the limit exists.

## What Graceful Boundaries does

The specification addresses three gaps that existing standards cover separately but no specification combines:

1. **Proactive discovery** -- limits are machine-readable before they are hit
2. **Structured refusal** -- every non-success response explains what happened, why, and what to do next
3. **Constructive guidance** -- refusals include a useful next step, not just a block

This applies to **every HTTP error class**, not just rate limits. A `400` explains the validation rule and its security rationale. A `404` tells you whether the resource never existed or expired, and offers a creation path. A `500` names the affected subsystem and suggests a retry window. Every non-success response MUST include `error`, `detail`, and `why`.

**Read the full specification:** **[spec.md](spec.md)**

## See it in action

These examples use [Siteline](https://siteline.to/), a Level 4 conformant reference implementation.

**Discover limits before hitting them:**

```bash
curl -s https://siteline.to/api/limits | jq '{service, limits: .limits.scan}'
```

```json
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
        }
      ]
    }
  }
}
```

**Structured refusal with constructive guidance** (when a rate limit is exceeded):

```json
{
  "error": "rate_limit_exceeded",
  "detail": "You can run up to 10 scans per hour. Try again in 2400 seconds.",
  "limit": "10 scans per IP per hour",
  "retryAfterSeconds": 2400,
  "why": "Siteline is a free service. Rate limits keep it available for everyone and prevent abuse.",
  "alternativeEndpoint": "/api/result?id=example.com"
}
```

The caller knows the limit, when to retry, *why* the limit exists, and where to get the result without waiting.

**Every error class is self-explanatory**, not just 429s:

```json
{
  "error": "invalid_input",
  "detail": "This URL points to a private or reserved address and cannot be scanned.",
  "why": "Siteline blocks private IPs, loopback, and cloud metadata endpoints to prevent server-side request forgery.",
  "field": "url",
  "expected": "A public URL with a resolvable hostname on port 80 or 443."
}
```

An agent reading this `400` understands the SSRF protection policy and can fix the input. Without `why`, it would blindly retry with different URLs.

**Proactive headers on successful responses:**

```bash
curl -s 'https://siteline.to/api/result?id=example.com' \
  -D - -o /dev/null 2>&1 | grep ratelimit
```

```
ratelimit: limit=60, remaining=59, reset=60
ratelimit-policy: 60;w=60
```

A caller seeing `remaining=1` self-throttles before the next request. A caller seeing `remaining=59` knows it has budget.

For more examples, see **[docs/curl-examples.md](docs/curl-examples.md)**.

## Conformance levels

Services self-declare a conformance level. The eval suite validates the claim.

| Level | What it requires |
|---|---|
| **N/A: Not Applicable** | No API endpoints, rate limits, or agentic interaction surface. |
| **Level 0: Non-Conformant** | Limits exist but are not described per this specification. |
| **Level 1: Structured Refusal** | All non-success responses include `error`, `detail`, and `why`. All `429`s add `limit` and `retryAfterSeconds`. |
| **Level 2: Discoverable** | Level 1 + a limits discovery endpoint. |
| **Level 3: Constructive** | Level 2 + refusal responses include constructive guidance when applicable. |
| **Level 4: Proactive** | Level 3 + successful responses include proactive limit headers. |

## Evaluate conformance

Clone the repo and run from the project root:

```bash
git clone https://github.com/snapsynapse/graceful-boundaries.git
cd graceful-boundaries
node evals/check.js https://siteline.to          # Level 4 — proactive headers
node evals/check.js https://google.com           # Level 0 — no conformance
node evals/check.js https://your-service.com --json
```

Run the unit test suite (131 tests, no dependencies):

```bash
npm test
```

## Which level should you target?

- **No API or agentic surface?** Declare `not-applicable` — takes 5 minutes.
- **API with rate limits?** Start at **Level 1** (structured refusals). This is the minimum useful level.
- **Agents call your API?** Target **Level 2** (add discovery) so agents learn the rules before breaking them.
- **Want to reduce 429 traffic?** Target **Level 3** (constructive guidance) — offer cached results and alternatives instead of bare refusals.
- **High-traffic API with agent callers?** Target **Level 4** (proactive headers) — callers self-throttle before hitting limits.

For a step-by-step walkthrough with code samples, see the **[implementation guide](docs/implementation-guide.md)**.

## Adopt the spec

**Start here** -- Every non-success response (`400`, `401`, `403`, `404`, `429`, `500`, `503`) MUST include three core fields: `error` (stable machine-parseable string), `detail` (human-readable explanation), and `why` (the security, policy, or operational reason). This applies to all error classes, not just rate limits.

**Level 1** -- All `429` responses include the three core fields plus `limit` (the exact constraint) and `retryAfterSeconds` (machine-parseable retry time).

**Level 2** -- Add a discovery endpoint at `/api/limits` or `/.well-known/limits` that returns all enforced limits as structured JSON. Agents can plan before they hit anything. Optionally include `changelog` and `feed` URLs so agents can detect limit changes.

**Level 3** -- Add constructive guidance to refusals. When a cached result exists, include `cachedResultUrl`. When a different endpoint can help, include `alternativeEndpoint`. When paid access has higher limits, include `upgradeUrl`. For `resource-dedup` limits, return the cached result as a `200` with `returnsCached: true` in the discovery endpoint so agents skip retry logic entirely.

**Level 4** -- Add `RateLimit` and `RateLimit-Policy` headers to successful responses so callers can self-throttle before hitting limits.

**HTML endpoints** -- HTML pages that return `429` SHOULD include `<meta name="retry-after" content="N">` and/or `<link rel="alternate" type="application/json" href="...">` so agents can discover structured refusals without parsing prose.

See the **[full specification](spec.md)** for field definitions, response classes, and security considerations.

## Relationship to existing standards

| Standard | What it covers | What Graceful Boundaries adds |
|---|---|---|
| `draft-ietf-httpapi-ratelimit-headers` | Proactive headers on success | Discovery endpoint, structured refusal body, `why` field, constructive guidance |
| RFC 6585 (429 status) | The status code itself | Structured body format with required fields |
| RFC 9457 (Problem Details) | Generic error format | Required fields for rate limits (`limit`, `retryAfterSeconds`, `why`) and guidance categories |
| OpenAPI Rate Limit extensions | Docs-time limit specs | Runtime discovery endpoint, runtime refusal format |

Graceful Boundaries is complementary to these standards, not a replacement.

## Reference implementation

[Siteline](https://siteline.to/) is a Level 4 conformant implementation with five API endpoints. Verify it from the project root:

```bash
node evals/check.js https://siteline.to
```

## Security

The specification includes a [threat model and security audit](SECURITY-AUDIT.md) covering rate limit calibration attacks, security posture disclosure, validation oracles, content cloaking via agent-signaling headers, and other considerations (SC-1 through SC-9), all addressed in the spec.

## Sponsor

Graceful Boundaries is free and open. If your team relies on this spec, consider [sponsoring its development](https://github.com/sponsors/snapsynapse) to keep it maintained and evolving. See [SPONSORS.md](SPONSORS.md).

## License

CC-BY-4.0. Use it, adapt it, build on it. Attribution required.

## About

Graceful Boundaries is a [PAICE.work](https://paice.work/) project. PAICE.work PBC is a public benefit corporation dedicated to enabling safer and more effective People+AI collaboration. We believe that clear, honest communication between services and their callers (human or AI agent) is foundational to trustworthy AI infrastructure. This specification is part of that mission.

The patterns in this spec emerged from building [Siteline](https://siteline.to/), an AI agent readiness scanner, where the quality of the refusal matters as much as the enforcement.

The conformance audit skill is available on **[ClawHub](https://clawhub.ai/snapsynapse/graceful-boundaries)**.

See also: **[Skill Provenance](https://github.com/snapsynapse/skill-provenance)** -- version identity that travels with agent skill bundles. Also a PAICE.work project.
