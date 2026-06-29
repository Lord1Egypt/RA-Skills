# Lumbox REST API reference (agent essentials)

Base URL: `https://api.lumbox.co`
Auth: `Authorization: Bearer $LUMBOX_API_KEY` (all endpoints except self-signup)
All responses are JSON. Errors: `{"error": "message"}` with 4xx/5xx status.

## Self-signup (unauthenticated)

```
POST /v1/orgs
{"name": "my-agent-org", "source": "openclaw"}
```

201 response — `api_key` is shown only once, store it:

```json
{
  "id": "org_...",
  "name": "my-agent-org",
  "api_key": "ak_...",
  "message": "Save this API key — it won't be shown again.",
  "created_at": "2026-06-12T00:00:00.000Z"
}
```

Limits: 3 orgs/hour/IP (429 with `retry_after_seconds`), name max 100 chars,
`source` optional max 64 chars.

## Inboxes

```
POST /v1/inboxes              {"name": "assistant"}          (name optional)
```

201: `{"id": "inb_...", "address": "assistant-x7f2@lumbox.email", "name", "status", "created_at"}`
(plus `imap_password`/`imap_host`/`imap_port` when IMAP is enabled for the org).

```
GET /v1/inboxes               list: {"data": [{id, address, name, status, email_count, created_at}]}
GET /v1/inboxes/:id           details
```

## Receiving

```
GET /v1/inboxes/:id/wait?timeout=120
```

Long-polls up to `timeout` seconds (max 120) for the next email. Returns the parsed email:
sender, subject, text/html, extracted OTP codes, verification/magic links, category.
408 `{"error": "..."}` on timeout — just call it again.

```
GET /v1/inboxes/:id/otp?timeout=120&from=noreply@service.com
```

Long-polls for an OTP specifically. 200:

```json
{
  "code": "847291",
  "all_codes": ["847291"],
  "from": "noreply@service.com",
  "subject": "Your verification code",
  "expires": "2026-06-12T00:10:00.000Z",
  "email_id": "eml_..."
}
```

408 `{"error": "No OTP found", "timeout": 120}` if nothing arrived.

```
GET /v1/inboxes/:id/emails    list emails (newest first)
```

## Sending

```
POST /v1/inboxes/:id/send     {"to": "a@b.com", "subject": "Hi", "text": "...", "html": "..."}
POST /v1/inboxes/:id/reply    {"email_id": "eml_...", "text": "..."}   (threads correctly)
POST /v1/inboxes/:id/forward  {"email_id": "eml_...", "to": "c@d.com"}
```

## Scoped keys (give a sub-agent one inbox only)

```
POST /v1/inboxes/:id/api-keys
```

Mints a key locked to that single inbox. Plaintext returned once.

## Everything else

Webhooks, custom domains, threads, contact lists, browser sessions, credential vault, and
TOTP 2FA are available via the MCP server (`npx @lumbox/mcp-server`, 87 tools) or REST —
see https://docs.lumbox.co.
