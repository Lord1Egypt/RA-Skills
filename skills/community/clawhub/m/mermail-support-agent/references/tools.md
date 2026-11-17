# Support agent tools

This workflow **uses** tools owned by other official skills. Do not add them to this skill in `tool-coverage.json`.

There are no `respond`, `escalate`, or `close_ticket` tools. Map those intents here.

Pass structured arguments as **native JSON objects**. Never stringify `query` or `body`. Use the exact host identifier (`reply_to_email` or `Mermail:reply_to_email`). Prefer mailbox `public_id` as `mailboxId`.

## Intent map

| Intent | Real operation | Owner |
| --- | --- | --- |
| Read a ticket | `list_emails`, `search_emails`, `get_email`, `get_thread` | `mermail-manage-inbox` |
| Draft a reply | `save_draft` (`body.body` string) | `mermail-compose-email` |
| Respond / send a reply | `reply_to_email` (`body.from` + `html`/`text`, explicit `to`/`cc`/`bcc`) | `mermail-compose-email` |
| Escalate | `forward_email` to the human owner, or `save_draft` addressed to them | `mermail-compose-email` |
| Close / follow up | `create_custom_label` or `move_email` | `mermail-manage-inbox` |
| Delete (rare) | `delete_email` + `prepare_destructive_action` | `mermail-manage-inbox` |

## Mailbox and automation

| Tool | Owner | Role |
| --- | --- | --- |
| `list_mailboxes` | `mermail-administer-workspace` | Discover a ready support mailbox |
| `create_mailbox` | `mermail-administer-workspace` | Provision only when none fits (10 credits; `email` + `name` required) |
| `update_mailbox_settings` | `mermail-administer-workspace` | Admin-only configuration of `agentAutoResponse.mode`; support uses the resulting policy |
| `list_task_triagers` / `list_recent_triager_runs` | `mermail-automate-triage` | Inspect before create/update |
| `create_task_triager` / `update_task_triager` | `mermail-automate-triage` | Classification and auto-draft only |
| `list_agent_conversations` / `chat_with_mailbox_agent` | `mermail-mail-agent` | Only when the user explicitly wants the in-app Assistant |

`draft_for_review` and `automatic_triage` are mailbox response modes, not task triager settings. Do not call `set_default_task_triager`. MCP does not auto-fill Reply All.

## Examples

```json
{
  "mailboxId": "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
  "emailId": "msg_123",
  "body": {
    "to": "customer@example.com",
    "from": "support@mermail.app",
    "text": "Thanks for writing in — here is the next step."
  }
}
```
