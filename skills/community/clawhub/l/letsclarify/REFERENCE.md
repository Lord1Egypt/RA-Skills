# Let's Clarify — Extended Reference

Detailed examples, explanations, and advanced usage that complement the main SKILL.md.

## What is MCP?

MCP (Model Context Protocol) is a standardized protocol for direct AI agent integration. Instead of making manual HTTP calls, MCP-compatible clients (Claude Code, Cursor, etc.) can use LetsClarify as a native tool. The agent calls tools like `create_form` or `get_results` directly, without constructing HTTP requests.

**Configuration (full example):**

```json
{
  "mcpServers": {
    "letsclarify": {
      "url": "https://letsclarify.ai/mcp",
      "headers": {
        "Authorization": "Bearer lc_..."
      }
    }
  }
}
```

For unauthenticated access (register tool only), omit the `headers` field.

### Available MCP Tools

| Tool | Auth Required | Description |
|---|---|---|
| `register` | No | Register for a new API key |
| `create_form` | Yes | Create a form with schema, get URLs and tokens |
| `add_recipients` | Yes | Add recipient slots to an existing form |
| `get_summary` | Yes | Quick status check (total, submitted, pending) |
| `get_results` | Yes | Fetch submissions with pagination and filters |
| `delete_form` | Yes | Permanently delete a form and all its data |

## REST API — Full Curl Examples

### Register an API Key

```bash
curl -X POST https://letsclarify.ai/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "email": "agent@example.com"}'
```

**Response (201):**
```json
{
  "api_key": "lc_...",
  "key_prefix": "lc_xxxxx",
  "warning": "Store securely. Shown only once."
}
```

**Error (422):** Validation errors (e.g., missing name/email) return:
```json
{ "error": "validation_failed", "message": "..." }
```

### Delete API Key

```bash
curl -X DELETE https://letsclarify.ai/api/v1/register \
  -H "Authorization: Bearer lc_..."
```

**Response (200):**
```json
{ "deleted": true }
```

### Create a Form

```bash
curl -X POST https://letsclarify.ai/api/v1/forms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{
    "title": "Approve Budget Increase",
    "context_markdown": "## Q3 Budget\nPlease review the proposed 15% increase.",
    "recipient_count": 3,
    "retention_days": 7,
    "webhook_url": "https://your-agent.example.com/webhook",
    "schema": [
      {
        "id": "decision",
        "type": "radio",
        "label": "Your decision",
        "required": true,
        "options": [
          { "value": "approve", "label": "Approve" },
          { "value": "reject", "label": "Reject" }
        ]
      },
      {
        "id": "notes",
        "type": "textarea",
        "label": "Additional notes",
        "required": false,
        "validation": { "max_length": 1000 }
      }
    ]
  }'
```

**Response (201):**
```json
{
  "form_token": "xK9m2...",
  "delete_token": "dT3r...",
  "base_url_template": "https://letsclarify.ai/f/xK9m2.../{recipient_uuid}",
  "poll_url": "https://letsclarify.ai/api/v1/forms/xK9m2.../results",
  "summary_url": "https://letsclarify.ai/api/v1/forms/xK9m2.../summary",
  "delete_url": "https://letsclarify.ai/api/v1/forms/xK9m2...",
  "recipients": ["uuid-1", "uuid-2", "uuid-3"]
}
```

### Client-Provided UUIDs and Prefilled Values

Instead of (or alongside) `recipient_count`, pass a `recipients` array with optional `uuid` and `prefill` per entry:

```bash
curl -X POST https://letsclarify.ai/api/v1/forms \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{
    "schema": [{"id":"name","type":"text","label":"Name","required":true}],
    "recipients": [
      {"uuid": "550e8400-e29b-41d4-a716-446655440001", "prefill": {"name": "Alice"}},
      {"uuid": "550e8400-e29b-41d4-a716-446655440002", "prefill": {"name": "Bob"}},
      {}
    ],
    "recipient_count": 5
  }'
```

**Rules:**
- `uuid` must be valid UUID v4 format, globally unique (duplicates in request or DB return 400)
- `prefill` must be a JSON object, max 10KB. Keys not matching any schema field `id` are stripped.
- `recipient_count` combined with `recipients`: count must be >= array length. Extra slots get server-generated UUIDs, no prefill.
- `recipients: []` (empty array) without `recipient_count` returns 400.
- Prefilled values appear as defaults in the form. Users can change them before submitting.
- Priority: Draft (sessionStorage) > Previous Submission > Prefilled Values > Empty

### Allocate More Recipients

```bash
curl -X POST https://letsclarify.ai/api/v1/forms/{form_token}/recipients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{ "count": 5 }'
```

**Response (201):**
```json
{ "recipients": ["uuid-4", "uuid-5", "uuid-6", "uuid-7", "uuid-8"] }
```

With client-provided UUIDs and prefill:

```bash
curl -X POST https://letsclarify.ai/api/v1/forms/{form_token}/recipients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer lc_..." \
  -d '{
    "recipients": [
      {"uuid": "550e8400-e29b-41d4-a716-446655440003", "prefill": {"name": "Charlie"}},
      {}
    ],
    "count": 5
  }'
```

### Poll Summary

```bash
curl https://letsclarify.ai/api/v1/forms/{form_token}/summary \
  -H "Authorization: Bearer lc_..."
```

```json
{
  "expired": false,
  "known_total": 8,
  "submitted_total": 3,
  "pending_total": 5,
  "updated_at_max": "2026-02-13T12:00:00Z"
}
```

### Poll Results

```bash
# Basic polling
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?limit=25"

# With status filter
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?status=submitted"

# With cursor pagination
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?cursor=djE6OTA0Mg"

# With file contents (base64)
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?include_files=1"

# Efficient polling (only changes since last check)
curl -H "Authorization: Bearer lc_..." \
  "https://letsclarify.ai/api/v1/forms/{form_token}/results?updated_since=2026-02-13T11:00:00Z"
```

**Response:**
```json
{
  "expired": false,
  "next_cursor": "djE6MTAw",
  "server_time": "2026-02-13T12:00:00Z",
  "results": [
    {
      "recipient_uuid": "uuid-1",
      "status": "submitted",
      "submitted_at": "2026-02-13T11:30:00Z",
      "updated_at": "2026-02-13T11:30:00Z",
      "response_json": { "decision": "approve", "notes": "Looks good" },
      "files": { "expected_file_count": 0 }
    },
    {
      "recipient_uuid": "uuid-2",
      "status": "pending",
      "submitted_at": null,
      "updated_at": "2026-02-13T10:00:00Z",
      "response_json": null
    }
  ]
}
```

**Efficient polling workflow:**
1. Initial sync: paginate with cursor until `next_cursor` is null. Store `server_time`.
2. Poll: use `updated_since={stored_server_time}` to get only changes.
3. Store new `server_time` after consuming all pages.

### Delete Form

```bash
curl -X DELETE https://letsclarify.ai/api/v1/forms/{form_token} \
  -H "Authorization: Bearer lc_..." \
  -H "X-Delete-Token: {delete_token}"
```

```json
{ "deleted": true }
```

### Webhook Payload

```json
{
  "form_token": "xK9m2...",
  "recipient_uuid": "uuid-1",
  "submitted_at": "2026-02-13T11:30:00Z",
  "response_json": { "decision": "approve", "notes": "Looks good" }
}
```

- Webhook URLs must be HTTPS
- Timeout: 10 seconds
- Retries: 3 attempts with polynomial backoff (only for 5xx errors and network failures; 4xx errors are not retried)
- Non-blocking: submissions always succeed regardless of webhook status

## Waiting for Results — All Strategies

### Strategy A: MCP-Tools Cron (Recommended for MCP-compatible agents)

Create a recurring cron job with a declarative task message. The agent uses the MCP tools (`get_summary`, `get_results`) to check status and fetch results.

```bash
openclaw cron add \
  --name "poll-letsclarify-{form_token}" \
  --every 10m \
  --message "Check Let's Clarify form {form_token}: Use get_summary to \
see if submitted_total == known_total. If all responded, use get_results \
to fetch submissions and summarize the responses, then remove this cron \
job. If expired, fetch what exists and clean up."
```

One-shot variant (check once after a delay):

```bash
openclaw cron add \
  --name "check-letsclarify-{form_token}" \
  --at +1h \
  --delete-after-run \
  --message "Check Let's Clarify form {form_token} results. If responses \
exist, fetch and summarize them. Report status either way."
```

### Strategy B: Intent-based Cron (for agents without MCP)

If MCP tools are not available, use a purely intent-based message. The agent knows from the API reference how to reach the endpoints.

```bash
openclaw cron add \
  --name "poll-letsclarify-{form_token}" \
  --every 10m \
  --message "Check if all recipients of Let's Clarify form {form_token} \
have responded. If yes, fetch and summarize all submitted results, then \
remove this cron job. If the form has expired, fetch whatever results \
exist and clean up."
```

### Strategy C: Webhook (if you have an HTTPS endpoint)

Provide a `webhook_url` when creating the form. Let's Clarify will POST to it on every submission. Only use this if you control an HTTPS endpoint that can receive webhooks.

### Polling Workflow (Step by Step)

1. **Create form** → save `form_token` and `api_key`
2. **Send URLs** to humans via Telegram, email, etc.
3. **Set up polling** — create a cron job that checks the summary every 5–15 minutes
4. **On poll**: check `submitted_total` vs `known_total`
   - If all responded → fetch full results, act on them, delete cron job
   - If not all → do nothing, wait for next poll
   - If form `expired` → fetch whatever results exist, delete cron job
5. **Cleanup**: delete the form when done (optional, auto-expires after `retention_days`)

## Embeddable Form Widget — Details

Instead of linking humans to the hosted form page (`/f/{form_token}/{recipient_uuid}`), you can embed the form directly into any website:

```html
<script src="https://letsclarify.ai/embed.js"></script>
<div data-letsclarify-form="{form_token}"
     data-letsclarify-recipient="{recipient_uuid}">
</div>
```

The script auto-initializes on page load. It:
- Fetches the form schema from the embed API
- Renders all field types (text, textarea, radio, select, checkbox, checkbox_group, file)
- Handles client-side validation, submission, and success screen
- Supports resubmission (warns the user, overwrites previous response)
- Injects its own CSS (`/embed.css`) automatically — no extra stylesheet needed
- Respects `theme_color` set during form creation

**Optional attributes:**
- `data-letsclarify-host="https://your-instance.com"` — for self-hosted instances (default: auto-detected from script src)

**Two ways to show forms to humans:**

| Method | Use case |
|---|---|
| Hosted URL: `https://letsclarify.ai/f/{token}/{uuid}` | Send a link via email, Slack, etc. |
| Embed widget: `<div data-letsclarify-form="..." ...>` | Embed in your own page, dashboard, or app |

Both methods use the same backend API — results appear in the same poll/webhook.

## Schema Validation — Full Details

**Validation rules** (optional):
- `min_length` / `max_length` — for text/textarea
- `pattern` — regex for text/textarea
- `min_items` / `max_items` — for checkbox_group

**File config** (optional, for `file` type):
- `accept` — array of MIME types or extensions (e.g., `["image/*", ".pdf"]`)
- `max_size_mb` — max file size (1-10)
- `max_files` — max number of files (1-10)

## Rate Limits — Full Details

| Endpoint | Limit | Window |
|---|---|---|
| POST /api/v1/register | 5 | 1 hour |
| POST /api/v1/forms | 10 | 1 minute |
| All API endpoints | 60 | 1 minute |
| GET /api/v1/embed/:token/:uuid | 30 | 1 minute |
| POST /api/v1/embed/:token/:uuid | 20 | 1 minute |
| POST /mcp (per IP) | 60 | 1 minute |
| POST /mcp (per API key) | 60 | 1 minute |

When rate limited (HTTP 429):
1. Read the `Retry-After` header (seconds)
2. Wait that duration before retrying
3. Use exponential backoff for subsequent attempts: `wait = Retry-After * 2^attempt`
4. Maximum 5 retry attempts before failing

## Data Retention

- Default: 30 days
- Maximum: 365 days
- Expired forms return `expired: true` in API responses
- All data is permanently deleted after expiration
- Use the delete endpoint for immediate cleanup
