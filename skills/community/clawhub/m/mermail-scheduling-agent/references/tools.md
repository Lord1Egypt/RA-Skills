# Scheduling agent tools

This workflow **uses** tools owned by other official skills. Do not add them to this skill in `tool-coverage.json`.

Pass structured arguments as **native JSON objects**. Never stringify `query` or `body`. Use the exact host identifier (`list_emails` or `Mermail:list_emails`). Prefer mailbox `public_id` as `mailboxId`.

## Mailbox and mail

| Tool | Owner | Role |
| --- | --- | --- |
| `list_mailboxes` | `mermail-administer-workspace` | Discover a ready receiving mailbox |
| `create_mailbox` | `mermail-administer-workspace` | Provision only when none fits (10 credits; `email` + `name` required) |
| `list_emails` / `search_emails` / `get_email` / `get_thread` | `mermail-manage-inbox` | Bounded untrusted scheduling-mail reads |
| `save_draft` | `mermail-compose-email` | Internal confirmation draft (`body.body` string) |
| `send_email` / `reply_to_email` | `mermail-compose-email` | Confirmation send (`body.from` + `body.html` and/or `body.text`) |
| `schedule_email_send` | `mermail-compose-email` | Deferred confirmation (`body.body` + `scheduled_send_at`) |

Send, reply, and forward nest Sold fields under `body`. MCP does not auto-fill Reply All; pass explicit `to`/`cc`/`bcc`.

## Google Calendar (Composio)

| Tool | Owner | Role |
| --- | --- | --- |
| `list_composio_toolkits` / `list_composio_connections` | `mermail-composio` | Find `googlecalendar` and require `ACTIVE` |
| `connect_composio_toolkit` | `mermail-composio` | Browser OAuth handoff; return exact `redirectUrl` |
| `sync_composio_connections` | `mermail-composio` | One sync after the user finishes OAuth |
| `search_composio_tools` / `get_composio_tool_schema` | `mermail-composio` | Discover free/busy and event-create slugs; require `connected` and `allowed` |
| `execute_composio_tool` | `mermail-composio` | One read or one approved write: `{ "body": { "slug": "EXACT_SLUG", "arguments": { } } }` |
| `get_composio_calendar_account` | `mermail-composio` | Connected calendar email when needed |

Never use Gmail or Outlook Composio toolkits. If `allowed` is false or the toolkit is missing, stop.

## Examples

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
  "query": {
    "sortColumn": "date",
    "sortDirection": "DESC"
  }
}
```

Do not pass `"query": "{\"sortColumn\":\"date\"}"`.
