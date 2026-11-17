# Mermail composition tool contract

Read this reference when choosing an external MCP composition operation or constructing its exact arguments. These are Sold API/MCP tools, not the in-app mailbox Assistant's private tool names.

| Intent | Tool | Effect |
| --- | --- | --- |
| Save editable content | `save_draft` | Internal write |
| Regenerate draft with AI | `regenerate_draft` | Internal write and AI usage |
| Send new email | `send_email` | External effect |
| Reply to email | `reply_to_email` | External effect |
| Forward email | `forward_email` | External effect |
| Schedule delivery | `schedule_email_send` | Deferred external effect |

The in-app Assistant uses specialized tools such as `save_draft_reply`, `schedule_send_draft`, and `discard_draft`, and can set `replyAll`. External MCP does not expose those semantics. Do not call or invent those tool names on this surface.

## MCP argument nesting

Always pass Sold API fields under the tool's `body` argument (path params like `mailboxId` stay top-level). Flat Sold fields are also accepted and folded into `body`.

Canonical payload split: send, reply, and forward use `body.html` and/or `body.text` plus required `body.from`; draft and schedule use the string field `body.body`. Prefer these canonical fields even though compatibility aliases are normalized server-side.

`mailboxId` accepts `public_id` (UUID), hosted alias id, or current email — prefer `public_id` from `list_mailboxes`.

## Recipients (`to` / `cc` / `bcc`)

| Surface | Accepted shapes |
| --- | --- |
| `send_email` / `reply_to_email` / `forward_email` | One email string **or** a JSON array of emails |
| `save_draft` / `schedule_email_send` | One email string, comma-separated string, or JSON array |

MCP does **not** expose `replyAll` and does **not** derive Reply / Reply All recipients from thread headers. On replies, pass explicit `to`; pass `cc` and `bcc` only when their intended sets are non-empty. If To is missing on a new compose, ask the user before calling these tools.

For `reply_to_email` and `forward_email`, pass the selected source `emailId` as a top-level path parameter. Threading headers for replies are set server-side, but recipients remain explicit on external MCP.

### Send / reply / forward

Content fields are **`html` and/or `text`** — not `body` or `content`. `from` is required.

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
  "idempotencyKey": "send-2026-07-21-a1",
  "body": {
    "to": "customer@example.com",
    "cc": ["manager@example.com", "ops@example.com"],
    "bcc": ["audit@example.com"],
    "from": "you@mermail.app",
    "subject": "Hello",
    "text": "Plain text body"
  }
}
```

Aliases accepted for send-like tools: `body` or `content` string → `text` (or `html` if the string looks like HTML).

When sending an existing draft, pass `source_draft_id` so it is retired after a successful delivery. Preserve `thread_id`, `in_reply_to`, and `references` when the selected source or draft provides them and the live schema requires them. Attachments use the live send schema and must remain within the user's explicit attachment intent.

### Draft / schedule

Content field is the string **`body`** (HTML or text). Do not use `html`/`text` for drafts.

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
  "body": {
    "to": "customer@example.com",
    "cc": "manager@example.com, ops@example.com",
    "bcc": "audit@example.com",
    "subject": "Hello",
    "body": "<p>Draft HTML</p>"
  }
}
```

Schedule requires at least one To recipient at execution time and `scheduled_send_at` as a future ISO-8601 datetime on `body`. For a scheduled reply, include `in_reply_to` and `thread_id` as available. When replacing an existing regular draft, pass `draft_id`; do not send the reply first.

### Regenerate

`regenerate_draft` uses:

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
  "body": {
    "draftId": "draft-id",
    "prompt": "Make the response warmer and more concise",
    "body": "<p>Current draft body</p>"
  }
}
```

Regeneration changes an unsent draft for review. It does not authorize or perform delivery.

## Idempotency

Pass `idempotencyKey` at the top level when using one. Reuse it only for the identical method, path, query, and body. A replay of most mutations returns a conflict instead of executing twice, so an idempotency key is not permission to loop or to retry an ambiguous external effect with a new key.

## External recipient limits

For Free workspaces, external API/MCP delivery counts every address in To+Cc+Bcc as one recipient unit:

- at most **10 recipients in one request**;
- **10 recipient units/minute**;
- **50 recipient units/hour**;
- **200 recipient units/day**.

These limits apply to `send_email`, `reply_to_email`, `forward_email`, and the actual delivery of `schedule_email_send`. Developer and Enterprise bypass this special external-recipient limiter, but all plans remain subject to workspace RPM, API credits, and ordinary email quota.

Scheduling validates the per-request recipient count when the schedule is created, but rolling recipient quota is consumed only when delivery runs. A scheduled message deferred by the rolling limit remains `scheduled`; it is not sent yet.

| Status/code | Meaning | Required handling |
| --- | --- | --- |
| `400 email_send_recipient_limit_exceeded` | Free request has more than 10 total To+Cc+Bcc recipients | Do not retry or silently alter the approved recipient set; ask for a new exact set. |
| `429 email_send_rate_limit_exceeded` | A rolling recipient window is exhausted | Surface `Retry-After`; do not auto-retry a send-like write. Scheduled delivery may be requeued by Mermail. |
| `503 email_send_rate_limit_unavailable` | The limiter cannot safely verify capacity | Fail closed; do not send through another surface or claim delivery. |

The same stable delivery event is not charged twice by the recipient limiter, but that server-side deduplication is not permission for an agent to replay an uncertain write.

### If you see `Invalid request`

Read `code: "validation_failed"` and the `details` array from the tool result — they name the missing or wrong fields (for example `body: Either 'html' or 'text' must be provided`).
