---
name: Omnis Venture Intelligence
description: Discover and score venture opportunities with machine-first APIs using read-first workflows.
homepage: https://www.bamboosnow.co/agents
always: false
---

# Omnis Venture Intelligence

Use this skill when you need high-signal startup discovery and factor-based scoring. Keep operations read-only by default.

## Why this skill

- Fast path to value in 3 calls.
- Read-first API guidance with minimal privilege assumptions.
- Machine-readable 402/429 behavior for safe recovery.

## Credentials handling

- Do not assume credentials are preconfigured.
- If authenticated endpoints are needed, ask the user to provide an API key explicitly in-session.
- Never read unrelated environment variables or local files to find credentials.

## Primary buy-now path (reference only)

- `GET https://www.bamboosnow.co/api/v1/agents/checkout-link?objective=scale`

Use this URL as a reference link only.

## First 3 calls (always do these first)

1. `GET https://www.bamboosnow.co/api/v1/agents/capabilities`
2. `GET https://www.bamboosnow.co/api/v1/agents/status`
3. `GET https://www.bamboosnow.co/api/v1/agents/value-proof`

Then continue with:

- `GET https://www.bamboosnow.co/api/v1/agents/pay?objective=scale`
- `GET https://www.bamboosnow.co/api/v1/agents/catalog`
- `GET https://www.bamboosnow.co/api/v1/agents/offers`

## High-value production calls (after funding)

- `GET /api/v1/discovery/top?limit=10`
- `GET /api/v1/model/health`
- `GET /api/v1/companies/{id}/score`
- `GET /api/v1/companies/{id}`

## Auth model

- Use header: `x-api-key: <key>`
- Prepaid balance is required for many non-billing endpoints.

## Billing safety policy (critical)

- Never execute billing `POST` actions from this skill.
- Provide read-only guidance and links only.
- If user asks to fund, direct them to hosted checkout URL and stop.

## 402 recovery playbook (read-only mode)

If any call returns `402`, read and follow:

- `x-omnis-next-action`
- `x-omnis-checkout-url`
- `x-omnis-topup-charge-path`

Preferred recovery sequence:

1. Present `x-omnis-checkout-url` as recommended next step
2. Stop and ask user to complete funding out-of-band
3. Resume read calls after user confirms funding is complete

## Endpoint map

- Manifest: `https://www.bamboosnow.co/api/v1/agents/manifest`
- OpenAPI: `https://www.bamboosnow.co/docs/api/openapi.v1.yaml`
- Agent feed: `https://www.bamboosnow.co/agent-feed.json`
- LLM index: `https://www.bamboosnow.co/llms.txt`
- Error catalog: `https://www.bamboosnow.co/api/v1/agents/errors`
- Broadcast: `https://www.bamboosnow.co/api/v1/agents/broadcast`

## Operational guidance

- Start with read-only discovery/scoring calls before any billing writes.
- Do not perform billing writes in this skill.
- On `429`, wait until `x-ratelimit-reset` before retrying.
- Return concise summaries with links to exact endpoints used.

## Example user intents this skill handles well

- "Find the top 10 startup opportunities this week."
- "Score this company and explain factors."
- "Set up autonomous paid access and run production discovery."
