---
name: gusnais-skill
description: Gusnais (Ruby-China/Homeland compatible) API integration with web-parity behavior and permission-consistent UX. Use when users want to connect using only CLIENT_ID and CLIENT_SECRET, auto-complete OAuth/API settings, keep capability differences identical to gusnais.com based on abilities and server authorization, or perform read/write API operations for plugin domains (press, note, jobs, site).
---

# Gusnais Skill

Implement Gusnais API integration that mirrors web behavior and permission boundaries.

## Require only two user inputs
- `CLIENT_ID`
- `CLIENT_SECRET`

Do not ask for base URL, OAuth paths, account IDs, scope defaults, pagination defaults, or serializer mappings unless discovery fails.

## Auto-complete platform config
Use these defaults:
- Site: `https://gusnais.com`
- OAuth Authorize: `/oauth/authorize`
- OAuth Token: `/oauth/token`
- OAuth Revoke: `/oauth/revoke`
- API Base: `/api/v3`

## Auth flow
1. Build authorization URL automatically.
2. Exchange authorization code for `access_token` and `refresh_token`.
3. Validate token with `GET /api/v3/users/me`.
4. Refresh once on 401; if refresh fails, request re-auth.

Prefer Authorization header for requests:
- `Authorization: Bearer <access_token>`

Keep `access_token` query fallback for compatibility with Homeland API behavior.

## Web parity contract
Match gusnais.com UX and permission behavior:

1. **Read abilities first when available**
   - Resource-level actions must follow returned `abilities`.
2. **Dual check**
   - UI check (visible/enabled) using abilities.
   - Execution check with real API call and status code handling.
3. **No privilege escalation**
   - Never assume admin/mod privileges in client logic.
4. **Respect hidden/inaccessible resources**
   - 404/403 semantics should stay consistent with server behavior.

## Capability gating model
For each action produce:
- `visible`: `true|false`
- `enabled`: `true|false`
- `reason`: `ok|no_permission|auth_required|resource_unavailable|validation_error`
- `source`: `abilities|server_status|policy`

## Endpoint behavior alignment
Use endpoint mapping in `references/endpoints.md` and serializer notes for normalized outputs.

Keep defaults aligned with docs:
- offset default: `0`
- limit default: `20`
- limit range on list endpoints: `1..150` (or endpoint-specific documented max)
- topic list default `type=last_actived`

For plugin domain operations (press/note/site/jobs):
- Read plugin web-route parity and API contract in `references/endpoints.md`.
- Read permission nuances in `references/permission-parity.md`.
- Treat 404 on plugin API endpoints as `resource_unavailable` unless deployment has enabled those API routes.

## Topic action safety
For `POST /api/v3/topics/:id/action?type=:type` (`ban|excellent|unexcellent|close|open`):
- Gate by `abilities` if present.
- Enforce final server response.
- Never expose action as enabled when denied.

## Error mapping
Normalize API errors without changing meaning:
- 400 -> `validation_error`
- 401 -> `auth_required` (refresh then retry once)
- 403 -> `no_permission`
- 404 -> `resource_unavailable`
- 500 -> `server_error`

Return original server error text when available.

## Rate limiting / retries
- Respect `Retry-After` on 429.
- Use exponential backoff with jitter for transient 5xx.
- Avoid one-item tight loops for batch writes.

## Read these references before implementation
- `references/endpoints.md`
- `references/permission-parity.md`

## Bootstrap script
Use `scripts/gusnais_bootstrap.py` to initialize runtime config from `CLIENT_ID` and `CLIENT_SECRET`.

Recommended:
- set `TOKEN_STORE_PATH` when exchanging code, so refreshable tokens are persisted to JSON for long-lived automation.

## Plugin API client script
Use `scripts/gusnais_plugin_client.py` for plugin API read/write calls with:
- auto refresh before expiry and on 401;
- one retry after refresh;
- normalized status reason mapping;
- capability hint extraction from `abilities`;
- action-level payload guardrails to avoid avoidable 400/500 (e.g. press create summary fallback).

Current deployment notes (2026-03-19):
- Press API is mounted for read/write (`/api/v3/press/posts*`).
- Note API is mounted for read/write (`/api/v3/note/notes*`).
- Site API is mounted for `sites` CRUD + `site_nodes` list; `undestroy`/site_node writes are not mounted.
- Treat any unmounted plugin API route as `resource_unavailable` and avoid repeated retries.
