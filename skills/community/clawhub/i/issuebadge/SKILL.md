---
name: issuebadge
description: Connect an agent to issuebadge.com and exchange data with it. Use when a user wants to issue, verify, revoke or export digital certificates or badges, list their certificate templates, download certificate PDFs, create dynamic QR codes, or wire IssueBadge into another system by API key, OAuth 2.1 or the MCP server.
license: MIT
metadata:
  author: issuebadge
  version: "1.0.1"
  homepage: https://issuebadge.com/h/integration/mcp
---

# Working with IssueBadge

IssueBadge (https://issuebadge.com) issues digital certificates and Open Badges. An organization designs a template once, issues it to a recipient by name and email, and every credential gets a public verification page at `https://app.issuebadge.com/v/{IssueId}` with a QR code. Recipients never need an account.

## 1. Choose how to connect

| Way | When to use it | What the user needs to do |
|---|---|---|
| **MCP server with OAuth 2.1** | ChatGPT, Claude, Cursor, VS Code or any MCP client that can open a browser | Add `https://issuebadge-mcp.issuebadge.workers.dev/mcp` with no header. The client discovers the sign-in itself; the user approves the `read` and `write` scopes once. |
| **MCP server with API key** | MCP clients that cannot open a browser, CI | Same URL with header `Authorization: Bearer <API key>` |
| **REST API with API key** | Your own code, scripts, no-code tools | Create the key at app.issuebadge.com, Developer, API key. Send it as `Authorization: Bearer <key>` on every request to `https://app.issuebadge.com/api/v1/...` |
| **Viktor (viktor.com)** | Viktor workspaces | Integrations, Add Custom, MCP Server, paste the MCP URL and sign in; or Add Custom, API with base URL `https://app.issuebadge.com/api/v1` and a bearer token. See the `issuebadge-viktor` skill. |
| **Agent CLI** | Shell-based agents | `pip install cli-anything-issuebadge`, set `ISSUEBADGE_API_KEY`, run `cli-anything-issuebadge --json <group> <command>` |

OAuth discovery, if you implement a client yourself: an unauthenticated call to the MCP URL returns 401 with a `WWW-Authenticate` header pointing at `/.well-known/oauth-protected-resource`; that names `https://app.issuebadge.com` as the authorization server; read `/.well-known/oauth-authorization-server` there; register with `POST /oauth/register` (dynamic client registration); run the authorization-code flow with PKCE S256; exchange at `/oauth/token`. Access tokens last one year.

Never ask the user to paste an API key into a chat when an OAuth-capable client is available. Never print, log or echo a key or token back to the user.

## 2. Check the connection

- MCP: call `validate_key`. REST: `POST /api/v1/validate-key`. CLI: `server status`.
- If it fails, tell the user to confirm the key or sign in again. Do not retry in a loop.

## 3. Core workflow: issue a credential

1. **List templates.** MCP `get_all_badges`, REST `GET /api/v1/badge/getall`, CLI `badge list`. Each template has an `id` (for example `YJ8VOL29N`) and a `name`.
2. **Pick the template** whose name matches what the user asked for. If several could match, show the names and ask. Never guess a template id.
3. **Confirm the recipient** full name and email before issuing. Issuing sends an email the user cannot recall.
4. **Issue.** MCP `issue_badge`, REST `POST /api/v1/issue/create`, CLI `issue create`. Fields:
   - `badge_id` (required), `name` (required), `email` (recommended; the certificate is emailed when present)
   - `issue_date`, `expire_date` as `YYYY-MM-DD` (optional; the template's expiry rule applies otherwise)
   - `idempotency_key` (strongly recommended): use `<badge_id>-<email>-<YYYY-MM-DD>` or a stable record id. Re-sending the same key returns the existing credential instead of issuing a duplicate.
   - `metadata`: an object of values for the template's custom fields (for example `{"club_name": "...", "score": 95}`). Only fields defined on the template are stored; check `GET /api/v1/badge/{id}` for `custom_fields`.
5. **Return the result.** The response contains `IssueId` and `publicUrl`. Give the user the verification URL; it is public and safe to share.

For many recipients, issue one request per person with a per-person idempotency key. Stop and report on the first error instead of retrying.

## 4. Share data back out of IssueBadge

| Need | How |
|---|---|
| List issued credentials | `GET /api/v1/issue/get` (CLI `issue list`); one record: `GET /api/v1/issue/get/{IssueId}` |
| Audit trail of one credential | `GET /api/v1/issue/{IssueId}/history` |
| Certificate PDF | `POST /api/v1/certificate/generate` with the issue id (PDF bytes); `/certificate/base64` for JSON; batch variants `/certificate/batch/generate` and `/certificate/batch/base64`. CLI `certificate download --out file.pdf` |
| Revoke or reinstate | `POST /api/v1/issue/revoke` with a reason; `PATCH /api/v1/issue/{IssueId}` updates `expire_date`, `memo` or reinstates |
| Verification page for a person | `https://app.issuebadge.com/v/{IssueId}` |
| Push events to another system | Webhooks are configured in the dashboard (Settings, Webhooks) for issued, viewed and revoked events; point them at the receiving system's HTTPS endpoint |
| Dynamic QR codes | `GET/POST /api/v1/qrcode`, `/qrcode/{code}`, `/qrcode/{code}/image`, `/qrcode/{code}/scans`; MCP tools `create_qr_code`, `list_qr_codes`, `get_qr_code`, `update_qr_code`, `get_qr_code_scans`, `delete_qr_code`. Updating the target changes where an already printed code goes. |

Bulk input: the dashboard accepts CSV, TXT, XLS or XLSX with column mapping. From an agent, prefer one `issue/create` call per row with idempotency keys so a rerun is safe.

## 5. Rules

- Confirm template and recipient before the first issue in a conversation. Do not issue to example or placeholder addresses unless the user explicitly asks for a test.
- Do not invent template ids, recipient details or custom field values.
- A failed issue call must not be retried with the same key blindly; report the error, then only issue again once the user confirms nothing was received.
- Issuing needs an active IssueBadge plan; "requires an active plan" is a billing message, not a bug. Point the user to https://issuebadge.com/h/pricing.
- HTTP 401 means the key or token is invalid or revoked. HTTP 422 carries field-level validation errors in `message`; show them verbatim.
- Only `app.issuebadge.com` and the MCP host ever receive credentials.

## 6. Reference

- Setup page for every client: https://issuebadge.com/h/integration/mcp
- API docs: https://issuebadge.com/h/developer
- MCP server source: https://github.com/issuebadge/mcp-server
- Agent CLI source: https://github.com/issuebadge2026/cli-anything-issuebadge
- Laravel notification channel: https://github.com/issuebadge2026/laravel-notification-channel-issuebadge
- Support: https://issuebadge.com/h/contact
