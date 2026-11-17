---
name: hackernews-api
title: Hacker News Public Reads
description: Read-only Hacker News API for AI agents: monitor top, new, best, Ask HN, Show HN, and job stories, search discussions, and fetch public items or users through ReplyNodes. Bearer API key required; no write, login, vote, submit, or private-data capability.
version: 2.0.1
mode: readonly
auth: Authorization: Bearer YOUR_FETCHER_KEY
---

# Hacker News Public Reads

Read-only Hacker News API for AI agents: monitor top, new, best, Ask HN, Show HN, and job stories, search discussions, and fetch public items or users through ReplyNodes. A preconfigured Bearer API key is required; no write, login, vote, submit, or private-data capability exists.

## Access

This provider currently requires a preconfigured `REPLYNODES_API_KEY` sent as an
Authorization Bearer header to `https://api.replynodes.com`. Do not ask the user
to paste a key into chat, and do not implement account signup or key provisioning
inside this skill. If no key is available, stop and report that the provider is
not anonymous/keyless.

Gateway: https://api.replynodes.com

## Authentication

Use one long-lived ReplyNodes fetcher key. Send it on every request as:

```http
Authorization: Bearer YOUR_FETCHER_KEY
```

Store the real key in the agent's secret configuration. Never put it in prompts, source files, logs, URLs, or returned data. The gateway performs shared control-plane scope and entitlement checks.

## Plans and prepaid credits

- Payment mode: `prepaid_credit` only.
- Free: 500 one-time credits.
- Developer: 10,000 credits/month at $19/month.
- Pro: 100,000 credits/month at $99/month.
- Failed or provider-error requests cost zero; monthly credits do not roll over; paid overage requires an explicit cap.


## Read-only operations

Every operation is an HTTP GET and reads public data only:

- `stories_top` — `GET https://api.replynodes.com/v1/hackernews/stories_top`. List top public Hacker News stories This operation costs 2 prepaid credits.
- `stories_new` — `GET https://api.replynodes.com/v1/hackernews/stories_new`. List newest public Hacker News stories This operation costs 2 prepaid credits.
- `stories_best` — `GET https://api.replynodes.com/v1/hackernews/stories_best`. List best public Hacker News stories This operation costs 2 prepaid credits.
- `stories_ask` — `GET https://api.replynodes.com/v1/hackernews/stories_ask`. List public Ask HN stories This operation costs 2 prepaid credits.
- `stories_show` — `GET https://api.replynodes.com/v1/hackernews/stories_show`. List public Show HN stories This operation costs 2 prepaid credits.
- `stories_job` — `GET https://api.replynodes.com/v1/hackernews/stories_job`. List public Hacker News job stories This operation costs 2 prepaid credits.
- `item` — `GET https://api.replynodes.com/v1/hackernews/item/{id}`. Fetch one public Hacker News item This operation costs 2 prepaid credits.
- `user` — `GET https://api.replynodes.com/v1/hackernews/user/{handle}`. Fetch one public Hacker News user This operation costs 2 prepaid credits.
- `search` — `GET https://api.replynodes.com/v1/hackernews/search`. Search public Hacker News discussions This operation costs 2 prepaid credits.

## Request and response behavior

- Use `https://api.replynodes.com` as the gateway origin.
- Encode path parameters and query values; do not put credentials in query strings.
- Preserve the gateway response envelope and request ID when reporting results.
- Treat unavailable upstream data as unavailable; do not fabricate fields or success.
- Do not retry non-idempotent methods: this package has no non-GET methods.

## Example

```bash
curl -sS https://api.replynodes.com/v1/hackernews/capabilities
curl -sS -H "Authorization: Bearer YOUR_FETCHER_KEY" \
  "https://api.replynodes.com/v1/hackernews/stories_top"
```

## Safety boundaries

This skill has no write, publish, account, follow, or credential-management operation. It must not be used to claim private data access, unauthenticated access, guaranteed availability, or unsupported pricing.

## Source and validation

The operation list is generated from `services/hackernews-fetcher/internal/capabilities/capabilities.go`. `manifest.json`, `references/operations.json`, and `CHECKSUMS.sha256` are generated artifacts; change the catalog or source capability contract and regenerate them together.
