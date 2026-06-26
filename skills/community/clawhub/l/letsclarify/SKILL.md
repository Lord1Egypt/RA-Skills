---
name: letsclarify
description: Collect structured human input — approvals, decisions, reviews, data — via web forms. Create a form with a JSON schema, send unique URLs to humans, poll for results. Use when your workflow needs a human in the loop before proceeding.
homepage: https://letsclarify.ai
license: MIT
metadata: {"clawdbot":{"emoji":"📋","primaryEnv":"LETSCLARIFY_API_KEY"}}
---

# Let's Clarify Skill

Human-in-the-Loop infrastructure. Use when your workflow needs structured human input — approvals, decisions, data collection — before proceeding.

**Base URL:** `https://letsclarify.ai`
**Auth:** `Authorization: Bearer lc_...` on all API calls.

> For full curl examples, detailed response payloads, MCP tool descriptions, all polling strategies, embed widget details, and advanced prefill rules, see [REFERENCE.md](./REFERENCE.md).

## MCP Server (Preferred)

MCP-compatible agents should use the remote MCP endpoint instead of raw REST calls.

**Endpoint:** `https://letsclarify.ai/mcp`

Config: `{ "mcpServers": { "letsclarify": { "url": "https://letsclarify.ai/mcp", "headers": { "Authorization": "Bearer lc_..." } } } }`

**Tools:** `register` (no auth), `create_form`, `add_recipients`, `get_summary`, `get_results`, `delete_form` (all require auth).

## REST API Reference

### Register / Delete API Key

`POST /api/v1/register` with `{"name": "...", "email": "..."}` → `{"api_key": "lc_...", "key_prefix": "lc_xxxxx"}`. Store securely, shown only once.

`DELETE /api/v1/register` with auth header → `{"deleted": true}`.

### Create Form

`POST /api/v1/forms` (auth required)

```json
{
  "title": "Approve Budget Increase",
  "context_markdown": "## Q3 Budget\nPlease review the proposed 15% increase.",
  "recipient_count": 3,
  "retention_days": 7,
  "webhook_url": "https://example.com/webhook",
  "schema": [
    {"id": "decision", "type": "radio", "label": "Your decision", "required": true,
     "options": [{"value": "approve", "label": "Approve"}, {"value": "reject", "label": "Reject"}]},
    {"id": "notes", "type": "textarea", "label": "Additional notes", "required": false}
  ]
}
```

Optional params: `theme_color` (hex, e.g. `#1a2b3c`). `recipient_count` accepts 1–1,000.

**Response:** `form_token`, `delete_token`, `recipients` (array of UUIDs), `base_url_template`, `poll_url`, `summary_url`, `delete_url`.

**Recipient URLs:** `https://letsclarify.ai/f/{form_token}/{recipient_uuid}` — distribute via email, Slack, WhatsApp, etc.

**Client-provided UUIDs/prefill:** Instead of `recipient_count`, pass `"recipients": [{"uuid": "...", "prefill": {"field_id": "value"}}, {}]`. UUIDs must be valid v4, prefill max 10KB. Both `recipients` array and `recipient_count` can be combined (count >= array length).

### Add Recipients

`POST /api/v1/forms/{form_token}/recipients` with `{"count": 5}` or `{"recipients": [...]}`. Max 1,000/request, 10,000/form. Same UUID/prefill rules as creation.

### Poll Summary

`GET /api/v1/forms/{form_token}/summary` → `{expired, known_total, submitted_total, pending_total, updated_at_max}`.

### Poll Results

`GET /api/v1/forms/{form_token}/results`

Query params: `limit`, `status` (submitted/pending), `cursor` (pagination), `include_files=1` (base64), `updated_since` (ISO 8601).

**Response:** `{expired, next_cursor, server_time, results: [{recipient_uuid, status, submitted_at, updated_at, response_json, files}]}`.

**Efficient polling:** First paginate with cursor until `next_cursor` is null, store `server_time`. Then poll with `updated_since={server_time}`.

### Delete Form

`DELETE /api/v1/forms/{form_token}` with `X-Delete-Token: {delete_token}` → `{"deleted": true}`. Permanently removes form, submissions, and files.

### Webhooks

If `webhook_url` (HTTPS) is set, a POST is sent per submission with `{form_token, recipient_uuid, submitted_at, response_json}`. Retries 3× with backoff on 5xx/network errors. Non-blocking.

## Waiting for Results

After creating a form and sending URLs, set up async polling. Do NOT assume immediate responses.

**Recommended: Cron polling**

```bash
openclaw cron add --name "poll-lc-{form_token}" --every 10m \
  --message "Check Let's Clarify form {form_token}: get_summary to see if submitted_total == known_total. If all responded, get_results and summarize, then remove this cron. If expired, fetch what exists and clean up."
```

One-shot: `openclaw cron add --name "check-lc-{form_token}" --at +1h --delete-after-run --message "Check form {form_token} results and report status."`

**Workflow:** Create form → send URLs → cron polls summary → all responded or expired → fetch results → delete cron → optionally delete form.

## Embed Widget

Embed forms directly in any page instead of linking to the hosted URL:

```html
<script src="https://letsclarify.ai/embed.js"></script>
<div data-letsclarify-form="{form_token}" data-letsclarify-recipient="{recipient_uuid}"></div>
```

Auto-renders all field types, handles validation/submission, injects its own CSS.

## Schema Field Types

| Type | Description | `options` required |
|---|---|---|
| `text` | Single-line input | No |
| `textarea` | Multi-line input | No |
| `checkbox` | Single boolean | No |
| `checkbox_group` | Multiple checkboxes | Yes |
| `radio` | Radio buttons | Yes |
| `select` | Dropdown | Yes |
| `file` | File upload | No |

**Validation** (optional): `min_length`/`max_length`, `pattern` (regex) for text/textarea. `min_items`/`max_items` for checkbox_group.
**File config** (optional): `accept` (MIME/extensions), `max_size_mb` (1-10), `max_files` (1-10).

## Rate Limits

| Endpoint | Limit |
|---|---|
| Register | 5/hour |
| Create form | 10/min |
| All API / MCP | 60/min |
| Embed GET/POST | 30/20 per min |

On 429: read `Retry-After` header, exponential backoff (`Retry-After × 2^attempt`), max 5 retries.

## Data Retention

Default 30 days, max 365 days. Expired forms return `expired: true`. Use delete endpoint for immediate cleanup.
