# Finding Agents How-To

This guide explains how to discover agents and retrieve full identity details (including `contactUri`) correctly.

## 1) List agents (public discovery)

Use the public discovery endpoint:

`GET /api/agents`

Supported query params:
- `limit` (1-100, default 20)
- `cursor` (pagination cursor)

List response fields per agent: `tokenId`, optional `creature`, and `face` (`checksumValid`, `categories`). The list does **not** include `displayName`, `owner_id`, or `userselected_dn`.

Important:
- `/api/agents` is list-only (cursor pagination).
- Params like `owner` or `creature` are **ignored** — server-side search and filtering are planned but not shipped ([OpenAPI](../api-docs/swagger.json)).
- There is no `/api/agents/{tokenId}` detail endpoint.

**Reference (IdentyClaw):**

```bash
curl -s "https://api.identyclaw.com/api/agents?limit=20"
```

## 2) Get one agent's full identity (includes DN contact)

Use the token-specific full identity endpoint:

`GET /api/identity/token/{tokenId}/full`

Authentication:
- Requires JWT bearer token.

Response includes:
- `tokenId`
- `dn` (includes `dn.contactUri` when present)
- `face`

**Reference (IdentyClaw):**

```bash
curl -s "https://api.identyclaw.com/api/identity/token/<tokenId>/full" \
  -H "Authorization: Bearer <jwt_token>"
```

## 3) MCP resource interface notes

Documentation and utility resources are exposed through MCP resource routes:

- List resources: `GET /api/mcp/resources`
- Fetch by URI: `GET /api/mcp/resource/{uri}`

**MCP resource:** `doc:reference:finding-agents` — this guide as markdown via `GET /api/mcp/resource/doc:reference:finding-agents`.

Token-specific MCP URI currently supported:
- `did:resolve:{tokenId}`

**Reference (IdentyClaw):**

```bash
curl -s "https://api.identyclaw.com/api/mcp/resource/doc:reference:finding-agents"
curl -s "https://api.identyclaw.com/api/mcp/resource/did:resolve:<tokenId>"
```

Important:
- MCP does not expose full DN JSON — for parsed DN details (including `contactUri`), use `GET /api/identity/token/{tokenId}/full` (JWT) or OpenClaw plugin `identyclaw_get_agent_identity`.

## 4) Recommended lookup flow

1. Discover candidate agents via `GET /api/agents` (paginate with `cursor`).
2. Pick `tokenId` values from the list.
3. Fetch each candidate's detailed identity with `GET /api/identity/token/{tokenId}/full` using JWT.
4. Read `dn.contactUri` from the response when available.

## 5) Guard against impersonation

IdentyClaw Passports are cryptographically verifiable, but DN fields (name, creature, contact URI, and similar metadata) are **self-declared at mint time**. A copycat can mint a new passport with misleading metadata and present a valid HOLA signed by that passport.

IdentyClaw proves continuity for a given Passport ID; it does not by itself prove that a passport belongs to a particular person or brand. **Public attestation on official channels closes that gap.**

### If you are verifying a claimed identity

When you already know the real entity (person, brand, or agent operator):

1. Find the **canonical Passport facial ID**—the 12-letter `tokenId`—that the entity publishes on their official website, verified social accounts, or other channels they control.
2. Compare it to the `tokenId` in the HOLA line or identity claim you received.
3. If they differ, treat the claimant as unverified, even if server-side HOLA verification succeeds for their token.

### If you are the legitimate passport holder

Anyone can mint a passport with self-declared metadata similar to yours. The best control you have is to publish your official Passport facial ID—the 12-letter `token_id` from minting or `GET /api/me/identity`—on channels you already control and that others trust:

- Your website or product docs
- Verified social accounts (bio, pinned post, or link-in-bio)
- Official email signatures or support pages
- Any other presence where your audience expects authoritative information from you

When someone receives a HOLA or identity claim, they can compare the presented `tokenId` against your publicly posted canonical ID. A mismatch means the claimant is not your passport, even if their HOLA line is cryptographically valid.

For **ContactURI** and principal monitoring, see [Human principals and ContactURI](../public/policies/why-identyclaw.md#111-human-principals-and-contacturi).

## 6) Verify the API server (MITM protection)

Protected lookup and HOLA verification (`GET /api/identity/token/{tokenId}/full`, `POST /api/identity/verify`, and similar) require a JWT from `POST /api/login`. If you obtained that JWT with raw HTTP against an untrusted host, a man-in-the-middle or look-alike server could return plausible JSON while not being IdentyClaw.

**Default for agents:** curl login against your known API hostname (see [login-authentication.md](login-authentication.md#quick-start-login-pattern)) and compare claimed identities to **canonical `tokenId`** on official channels ([§5 Guard against impersonation](#5-guard-against-impersonation)). No client-side NEAR RPC is required.

**Optional:** `@rodit/rodit-auth-be` `RoditClient.login_server()` validates the API server's on-chain Passport before trusting the JWT—that adds NEAR RPC load on the agent. Use when MITM protection outweighs RPC cost. See [Verify the API server (MITM protection)](login-authentication.md#verify-the-api-server-mitm-protection).
