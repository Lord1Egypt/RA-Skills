# GTM agent tools

This workflow **uses** tools owned by other official skills. Do not add them to this skill in `tool-coverage.json`.

Pass structured arguments as **native JSON objects**. Never stringify `query` or `body`. Use the exact host identifier (`send_email` or `Mermail:send_email`). Prefer mailbox `public_id` as `mailboxId`.

## Mailbox, mail, and labels

| Tool | Owner | Role |
| --- | --- | --- |
| `list_mailboxes` | `mermail-administer-workspace` | Discover a ready outbound mailbox |
| `create_mailbox` | `mermail-administer-workspace` | Provision only when none fits (10 credits; `email` + `name` required) |
| `list_emails` / `search_emails` / `get_email` | `mermail-manage-inbox` | Bounded untrusted reply reads |
| `create_custom_label` / `move_email` | `mermail-manage-inbox` | Handoff labeling or folder move |
| `save_draft` | `mermail-compose-email` | Outreach or warm-ack draft (`body.body` string) |
| `send_email` / `reply_to_email` / `forward_email` | `mermail-compose-email` | Approved send/reply/handoff (`body.from` + `html`/`text`) |

Send, reply, and forward nest Sold fields under `body`. MCP does not auto-fill Reply All.

## Optional Apollo (Composio)

| Tool | Owner | Role |
| --- | --- | --- |
| `list_composio_toolkits` / `list_composio_connections` | `mermail-composio` | Find `apollo` and require `ACTIVE` |
| `connect_composio_toolkit` | `mermail-composio` | Browser OAuth; return exact `redirectUrl` |
| `sync_composio_connections` | `mermail-composio` | One sync after browser completion |
| `search_composio_tools` / `get_composio_tool_schema` / `execute_composio_tool` | `mermail-composio` | Lead search only; never send email through Apollo |

Never use Gmail or Outlook Composio. Skip Apollo when the user already provided the list.

## Draft-only triager

| Tool | Owner | Role |
| --- | --- | --- |
| `list_task_triagers` / `list_recent_triager_runs` | `mermail-automate-triage` | Inspect before create/update |
| `create_task_triager` / `update_task_triager` | `mermail-automate-triage` | Classification and auto-draft only |
| `delete_task_triager` | `mermail-automate-triage` | Destructive; `prepare_destructive_action` |

Do not call `set_default_task_triager`.

## Examples

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
  "idempotencyKey": "gtm-send-2026-08-19-a1",
  "body": {
    "to": "prospect@example.com",
    "from": "you@mermail.app",
    "subject": "Quick intro",
    "text": "Plain text body"
  }
}
```
