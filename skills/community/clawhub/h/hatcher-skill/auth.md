---
name: hatcher-skill-auth
version: 1.0.0
description: Hatcher authentication for AI agents — register, email verify polling, API keys
homepage: https://hatcher.host
api_base: https://api.hatcher.host
---

# Auth

## Summary

Hatcher supports two auth modes:
1. **JWT bearer tokens** from `POST /auth/login` or `/register` — short-lived (7d default), refresh via `/auth/refresh`. Use for interactive flows.
2. **API keys** (`hk_` prefix) — long-lived, passed via `Authorization: Bearer hk_...` header. **Preferred for agents.**

Email verification is mandatory before most actions work. The agent flow polls `GET /auth/verify-status` to detect when the human has clicked the verify link.

## Endpoints

### POST /auth/register

Public. Rate-limited 5 req/60s/IP.

Body:
```json
{
  "email": "user@example.com",
  "username": "agent_user_01",
  "password": "Str0ngP@ssw0rd1",
  "agentName": "claude-code",
  "referralCode": "optional-code"
}
```

| Field | Rules |
| --- | --- |
| `email` | RFC-valid, case-insensitive (lowercased on store) |
| `username` | 3-30 chars, `[a-zA-Z0-9_-]` only |
| `password` | 8-128 chars, must contain upper + lower + digit |
| `agentName` | Optional; 2-40 chars, `[a-z0-9-]` only. Stored as `registeredVia` for telemetry. |
| `referralCode` | Optional; $2 credit to both parties after email verification |

Success (200):
```json
{ "success": true, "data": { "token": "eyJ...", "refreshToken": "...", "expiresIn": "7d", "user": { "id": "...", "email": "...", "username": "..." } } }
```

Errors:
- 400 `VALIDATION_ERROR` — field violates rules
- 409 `CONFLICT` — email or username already taken

### GET /auth/verify-status?email=...

Public. Rate-limited 12 req/60s/IP (allows ~1 req / 5s polling).

Returns whether a given email has verified. Intended for agent poll loops.

Success (200):
```json
{ "success": true, "data": { "verified": true } }
```

- 404 `NOT_FOUND` — email not registered

Polling recipe:
```bash
while true; do
  R=$(curl -sS "https://api.hatcher.host/auth/verify-status?email=$EMAIL")
  echo "$R" | grep -q '"verified":true' && break
  sleep 5
done
```

Cap polling at ~10 minutes (120 attempts). If still unverified, ask the human to check spam / resend via `POST /auth/resend-verification`.

### POST /auth/login

Body: `{ "email", "password" }`. Returns same shape as `/register`. For agent workflows, prefer API keys (stable across sessions).

### POST /auth/refresh

Body: `{ "refreshToken": "..." }`. Returns a new JWT. Use when JWT expires mid-flow.

### POST /auth/api-keys

Requires JWT auth. Rate-limited 10 req/60s.

Body:
```json
{ "label": "agent-default", "createdBy": "agent" }
```

| Field | Rules |
| --- | --- |
| `label` | Optional. Max 64 chars. Defaults to "My API Key". |
| `createdBy` | `"user"` (default) or `"agent"`. Used for telemetry. |

Success (200):
```json
{ "success": true, "data": { "id": "...", "label": "agent-default", "key": "hk_...", "prefix": "hk_abc123...", "createdAt": "..." } }
```

**The `key` is returned exactly once. Store it immediately.** There is no way to retrieve the full key afterwards — only the prefix. If lost, delete and create a new one.

Max 10 active keys per account. Revoke one first if at limit.

### GET /auth/api-keys

Requires JWT. Returns list of active (not revoked) keys — prefix only, no full key.

### DELETE /auth/api-keys/:id

Requires JWT. Soft-deletes (sets `revokedAt`). Revoked keys stop authenticating immediately.

## Using API keys for agent requests

All `/api/v1/*` endpoints accept the API key in the `Authorization` header:

```bash
curl https://api.hatcher.host/api/v1/me \
  -H "Authorization: Bearer hk_abc..."
```

The API key is detected by its `hk_` prefix — use the same `Authorization: Bearer ...` header as you would for JWT. There is no `x-api-key` header; don't bother sending one.

## Rate limits for API-key authenticated requests

Based on the account's tier (not the key):

| Tier | Requests/day |
| --- | --- |
| Free | 100 |
| Starter | 10,000 |
| Pro / Business / Founding | 100,000 |

`GET /api/v1/usage` returns current usage + reset time.

## See also

- [`agents.md`](./agents.md) — creating agents after you have an API key
- [`pricing.md`](./pricing.md) — upgrading past the free 100/day limit
