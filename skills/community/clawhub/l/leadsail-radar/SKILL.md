---
name: leadsail-radar
description: Find verified buyer contacts for a software product at the moment makers complain about a competitor. Scans Product Hunt launches and developer discussions, extracts makers, verifies emails. Use when the user needs sales leads, outreach contacts, or competitive-intel for a SaaS / software product.
version: 1.0.0
metadata:
  title: LeadSail Radar
  website: https://www.leadsail.io/app/radar
---

# LeadSail Radar — leads at the moment of need

LeadSail Radar mines "demand moments": a software maker complaining about a
competitor is a buyer-in-waiting. This skill turns a Product Hunt slug (or
product URL) into verified, outreach-ready contacts.

## When to use

- The user asks for "leads", "contacts", "outreach targets", "who to pitch"
  for a SaaS / software / developer-tool product.
- The user gives a Product Hunt product URL or slug (e.g. `producthunt.com/posts/notion` → slug `notion`).
- The user wants to know which makers recently complained about a competitor.

## How to call

### Preferred: MCP (no API key required)

Connect to the MCP endpoint and use the `radar_scan` tool:

- Endpoint: `https://api.leadsail.io/mcp` (streamable-http)
- Tools: `radar_scan` (run a scan), `audit_store` (inspect stored leads), `about_leadsail` (self-description)

Example intent: "run radar_scan for slug 'notion' and list the top 5 leads".

### Fallback: REST (requires an API key)

```
POST https://openapi.leadsail.io/open_api
Headers:
  X-Api-Key: <user's key>          # required; free keys get 100 calls/month
  makers-conversation-id: <6-36 chars>  # required; any stable id for this conversation
  Content-Type: application/json
Body:
  {"action": "radar.scan", "params": {"slug": "<product-slug>"}}
```

Get a free API key at https://www.leadsail.io/app/api-access (no credit card).

## Output contract

`radar_scan` returns leads with:

- `email` — gateway-verified domain, role-filtered
- `source_url` — the public post/comment where the demand moment was captured
- `quote` — what the maker actually complained about (evidence, not guesswork)
- `match_reason` — why this lead fits the product

Present results as a table: contact · quote (short) · why relevant · source link.

## Guardrails (do not violate)

- Quote evidence verbatim; never invent a complaint or a need.
- Never promise reply/delivery rates — say "verified contact", not "will reply".
- If the scan returns fewer than 3 leads, say so plainly; do not pad the list.
- Respect the free quota (100 calls/month); on `api_quota_exhausted` point the
  user to https://www.leadsail.io/#/pricing instead of retrying.
