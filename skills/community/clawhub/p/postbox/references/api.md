# Postbox - Full API Reference

> Postbox is an agent-native structured data collection platform. Forms are the base unit - a well-defined collection of fields that expresses intent. Create a form by defining the schema, get an endpoint, and start receiving validated submissions from HTML forms, scripts, or AI agents. No backend to build, no database to manage, no validation to write.

Base URL: `https://usepostbox.com`

Two interfaces:

- **REST API** (Bearer token auth, all plans) - Create forms, collect submissions, configure processing pipelines, integrate via destinations (webhooks, Discord, Slack).
- **MCP Server** (OAuth 2.1, Pro plan) - Connect AI assistants directly to your data.

## Authentication

`Authorization: Bearer {api_key}` - Generate at https://usepostbox.com/integrations/api-keys. Store as `POSTBOX_API_KEY`. Unauthenticated: `401 Unauthorized` (plain text).

Credit headers on all authenticated responses: `X-Postbox-Credits-Remaining`, `X-Postbox-Metered` (Pro: true/false, Free: always false).

## Forms API (Bearer auth required)

### Create Form `POST /api/forms`

| Field                      | Type    | Required | Description                                                                                                                                              |
| -------------------------- | ------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | string  | yes      | 1-100 characters                                                                                                                                         |
| `slug`                     | string  | yes      | URL-safe, 1-64 chars. Pattern: `^[a-z0-9]+(?:-[a-z0-9]+)*$`. Unique per user.                                                                            |
| `visibility`               | string  | yes      | `"public"` or `"private"`                                                                                                                                |
| `fields_schema`            | object  | yes      | `{"fields": [...]}` with rules. See Field Schema.                                                                                                        |
| `spam_protection_enabled`  | boolean | no       | Default: `false`                                                                                                                                         |
| `spam_protection_strategy` | string  | no       | `"standard"` (free) or `"intelligent"` (credits). Default: `"standard"`                                                                                  |
| `intent`                   | string  | no       | Plain-text form purpose (max 1000 chars). Used by AI spam detection to judge submission alignment. Example: `"Collect product feedback from customers"`. |
| `localisation_enabled`     | boolean | no       | Auto-translate. Uses credits. Default: `false`                                                                                                           |
| `smart_reply_enabled`      | boolean | no       | AI replies via knowledge base. Uses credits. Default: `false`                                                                                            |
| `smart_replies_mode`       | string  | no       | `"draft"` (save for review) or `"auto"` (send to submitter if email found). Default: `"draft"`                                                           |
| `smart_reply_email_field`  | string  | no       | Field name for submitter email in auto mode. Auto-set if form has exactly one email field. Required for auto-mode with multiple email fields.            |
| `knowledge_base_id`        | string  | no       | UUID. Required when `smart_reply_enabled: true`.                                                                                                         |

Response `201`: `{"form": {"id", "name", "slug", "visibility", "submission_token", "created_at", "endpoint"}}`

`submission_token`: only for private forms, shown once. Store immediately. Regenerate from dashboard if lost (invalidates old token).

Response `422`: `{"error": {"code": "validation_error", "message": "...", "details": {"slug": ["has already been taken"]}}}`

### List Forms `GET /api/forms`

Response: `{"forms": [{"id", "name", "slug", "visibility", "endpoint", "submission_count", "created_at"}]}`

### Get Form `GET /api/forms/{id}`

Response: `{"form": {"id", "name", "slug", "visibility", "intent", "fields_schema", "endpoint", "submission_count", "created_at"}}`

### Update Form `PUT /api/forms/{id}`

Same fields as Create, all optional. **Schema changes produce a new endpoint URL.** Always read `response.form.endpoint`. Old URLs keep working with old schema. Destinations managed separately.

### Delete Form `DELETE /api/forms/{id}`

Response: `{"form": {...}}` or 404 `{"error": {"code": "not_found"}}`

## Field Schema

```json
{
  "fields": [
    {
      "name": "field_name",
      "type": "string|email|number|boolean|date",
      "rules": [{ "op": "required" }]
    }
  ]
}
```

Types: `string`, `email` (must contain @), `number` (int/float), `boolean` (true/false), `date` (YYYY-MM-DD).

### Field Rules

| Operator     | Parameters              | Applies To     | Description                   |
| ------------ | ----------------------- | -------------- | ----------------------------- |
| `required`   | none                    | all            | Must be present and non-empty |
| `honeypot`   | none                    | string         | Spam trap (hidden via CSS)    |
| `one_of`     | `"values": [...]`       | string, number | Must be in list               |
| `not_one_of` | `"values": [...]`       | string, number | Must not be in list           |
| `min_length` | `"value": n`            | string         | Min length                    |
| `max_length` | `"value": n`            | string         | Max length                    |
| `min`        | `"value": n`            | number         | Min value (inclusive)         |
| `max`        | `"value": n`            | number         | Max value (inclusive)         |
| `pattern`    | `"value": "regex"`      | string         | Must match regex              |
| `after`      | `"value": "YYYY-MM-DD"` | date           | After date                    |
| `before`     | `"value": "YYYY-MM-DD"` | date           | Before date                   |

### Conditional Rules

`{"op": "required", "when": {"field": "role", "is": "eq", "value": "business"}}`. Comparators: `eq`, `neq`, `one_of`, `not_one_of`, `gt`, `lt`, `gte`, `lte`, `filled`, `empty`.

### Honeypot Fields

`{"op": "honeypot"}` rule. Hide with `position:absolute; left:-9999px; top:-9999px; opacity:0; pointer-events:none;` (not display:none). Best names: `website`, `company`, `url`, `fax`, `phone2`. Don't combine with `required`.

## Private Forms

Create with `"visibility": "private"`. Store `submission_token` (shown once). Submit with `Authorization: Bearer {submission_token}`. Regenerate from dashboard if lost.

## Submissions

### Endpoint URL

`https://usepostbox.com/api/{opaque_segment}/f/{slug}` - Opaque segment is server-generated. Never construct manually. Use `endpoint` from form response.

### Submit `POST /api/{opaque_segment}/f/{slug}`

JSON only (`Content-Type: application/json`). CORS automatic. No auth for public forms.

**Idempotency:** `Idempotency-Key` header (up to 256 chars). Same key returns original (200). Scoped per form.

Response `201`: `{"id", "data": {...}, "created_at"}`
Response `422`: `{"error": {"code": "validation_error", "details": {...}}}`
Response `401`: unauthorized. Response `404`: form_not_found.
Response `429`: `{"error": {"code": "plan_limit_exhausted", "upgrade_url": "https://usepostbox.com/billing"}}`

### Discover Schema `GET /api/{opaque_segment}/f/{slug}`

Returns: `{"name", "slug", "endpoint", "method": "POST", "content_type": "application/json", "visibility", "fields": [...]}`. Honeypots hidden. Private forms include `authentication` object with bearer token instructions.

### Content Negotiation

POST submits data. GET+JSON returns schema. GET+HTML (browser) renders documentation page. Not a fillable form.

### List Submissions `GET /api/forms/{form_id}/submissions`

| Parameter           | Type    | Default         | Description                                                                                                                       |
| ------------------- | ------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `filter`            | string  | `"inbox"`       | `"inbox"`, `"spam"`, or `"all"`                                                                                                   |
| `search`            | string  | none            | Full-text search across data fields                                                                                               |
| `reply_status`      | string  | none            | `"awaiting_review"`, `"awaiting_delivery"`, `"delivered"`, `"needs_human_reply"`, `"delivery_failed"`, `"skipped"`, `"exhausted"` |
| `processing_status` | string  | none            | `"pending"`, `"processing"`, `"completed"`, `"failed"`                                                                            |
| `sort_by`           | string  | `"inserted_at"` | `"inserted_at"` or `"id"`                                                                                                         |
| `sort_order`        | string  | `"desc"`        | `"asc"` or `"desc"`                                                                                                               |
| `page`              | integer | 1               | Page number                                                                                                                       |
| `page_size`         | integer | 20              | Max 50                                                                                                                            |

Submission fields: `id`, `data`, `processing_status`, `processing_reason`, `spam` (boolean), `spam_confidence`, `spam_reason`, `detected_language`, `translated_data`, `reply_status`, `reply_subject`, `reply_content`, `reply_reason`, `replied_at`, `metadata` ({ip, user_agent, referer, origin, utm}), `created_at`.

### Get Submission `GET /api/forms/{form_id}/submissions/{id}`

### Delete Submission `DELETE /api/forms/{form_id}/submissions/{id}`

### Processing Pipeline (async after 201)

Validation > Spam detection > Translation > Smart replies > Destinations. Spam stops pipeline.

### Processing Status

`pending`, `processing`, `completed` (includes spam or credits exhausted), `failed`.
`processing_reason`: `credits_exhausted` | `service_error` | `null`.

## Schema Versioning

Schema updates produce new endpoint URL. Old URLs keep working with old schema. No API to list old versions. Always read `response.form.endpoint` after update.

## Knowledge Bases

CRUD at `/api/knowledge_bases`. Create: `name` + `content` (text/markdown/Q&A). Link to form via `knowledge_base_id`. Responses: `{"knowledge_base": {...}}`.

**Delete** returns `{"knowledge_base": {...}, "smart_reply_disabled_on": ["contact", "feedback"]}`. Smart replies auto-disabled on linked forms.

## Smart Replies

Draft: generated, stored for review. Auto: sends to submitter via `smart_reply_email_field`.

`reply_status` values: `awaiting_review`, `awaiting_delivery`, `delivered`, `needs_human_reply`, `delivery_failed`, `skipped`, `exhausted`. `null` when not enabled.

Fields: `reply_subject`, `reply_content`, `reply_reason`, `replied_at`. Cost: $0.01/reply.

## Destinations

CRUD at `/api/forms/{form_id}/destinations`. Types: `webhook`, `discord`, `slack`.

### Endpoints

`GET /api/forms/{form_id}/destinations` - list
`POST /api/forms/{form_id}/destinations` - create (type, name, url)
`DELETE /api/forms/{form_id}/destinations/{id}` - delete
`POST /api/forms/{form_id}/destinations/{id}/regenerate-secret` - webhook only

Webhook secrets: auto-generated (`whsec_...`), shown once at creation. Discord/Slack: no secret.

### Webhook Payload

```json
{"id": "evt_submission_created_{id}", "type": "submission.created", "created_at": "ISO 8601",
 "data": {"form": {"id", "name", "slug", "visibility", "version"},
          "submission": {"id", "data", "spam", "spam_confidence", "spam_reason",
                         "processing_status", "processing_reason", "detected_language",
                         "translated_data", "reply_status", "reply_subject", "reply_content",
                         "reply_reason", "replied_at", "inserted_at", "updated_at"}}}
```

### Signature Verification

Headers: `webhook-id`, `webhook-timestamp`, `webhook-signature`. Compute `HMAC-SHA256(secret, "{id}.{timestamp}.{body}")`. Format: `v1,{base64}`. Reject timestamps > 5 min old.

```javascript
const crypto = require("crypto");
function verifyWebhook(req, secret) {
  const id = req.headers["webhook-id"],
    ts = req.headers["webhook-timestamp"];
  const sig = req.headers["webhook-signature"],
    body = JSON.stringify(req.body);
  const expected = crypto
    .createHmac("sha256", secret)
    .update(`${id}.${ts}.${body}`)
    .digest("base64");
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(sig.replace("v1,", "")),
  );
}
```

```python
import hmac, hashlib, base64
def verify_webhook(headers, body, secret):
    signed = f"{headers['webhook-id']}.{headers['webhook-timestamp']}.{body}"
    expected = base64.b64encode(hmac.new(secret.encode(), signed.encode(), hashlib.sha256).digest()).decode()
    return hmac.compare_digest(expected, headers['webhook-signature'].replace('v1,', ''))
```

Discord: rich embeds, color-coded. Slack: Block Kit. No secrets. All: 3 retries, auto-disable after 3 failures.

## MCP Server (Pro plan)

Endpoint: `https://usepostbox.com/mcp`. StreamableHTTP + OAuth 2.1 (PKCE).
Config: `{"mcpServers": {"postbox": {"type": "http", "url": "https://usepostbox.com/mcp"}}}`

Tools: `list_forms`, `get_form(form_id)`, `list_submissions(form_id, filter?, limit?)`, `get_submission(submission_id)`, `get_dashboard_stats`, `translate_submission(submission_id)`, `analyze_spam(submission_id)`, `draft_reply(submission_id, knowledge_base_id?)`, `summarize_submissions(form_id, limit?)`.

## Error Reference

Format: `{"error": {"code": "string", "message": "string"}}`. Validation adds `details`. Some add `upgrade_url` or `retry_after`.

Authenticated: 401 `unauthorized`, 403 `form_limit_reached`/`pro_required`, 404 `not_found`, 422 `validation_error`/`delete_failed`/`invalid_destination_type`, 400 `invalid_params`, 429 `rate_limited`.

Public submission: 422 `validation_error`, 401 `unauthorized`/`invalid_token`, 404 `form_not_found`, 429 `plan_limit_exhausted`.

## Rate Limits

Submission: 10/min per IP. API: 60/min per IP. MCP: 30/min per IP. 429 includes `retry_after`. No proactive headers on success.

## Pricing

Free: 1 form, 5,000 lifetime submissions, 50 AI credits (one-time). AI features stop when exhausted.
Pro ($19/mo or $199/yr): Unlimited forms/submissions, MCP, 500 credits/month, metered overflow (no interruption).
Credit costs: spam $0.005, translation $0.005, smart reply $0.01. Standard spam always free.

## Integration Guide

### Always Use fetch

Never `<form action=...>`. fetch() gives structured validation errors. See `references/templates.md`.

### Agent Discovery Pattern

GET endpoint > read schema (with endpoint, method, content_type, fields) > POST to submit. Two calls, zero config. Always discover first, never hardcode fields. Schema discovery hides honeypots and includes auth instructions for private forms.

## Links

- Site: https://usepostbox.com
- Docs: https://docs.usepostbox.com
- Pricing: https://usepostbox.com/pricing
- Blog: https://usepostbox.com/blog
- MCP: https://usepostbox.com/mcp
- API keys: https://usepostbox.com/integrations/api-keys
