# Mermail mail-agent tool contract

Read this reference when selecting, creating, continuing, renaming, or deleting a mailbox-agent conversation through Mermail MCP.

## External MCP tool map

| Tool | Role |
| --- | --- |
| `list_agent_conversations` | List user-scoped conversations for one mailbox with cursor pagination |
| `list_agent_messages` | Read a bounded, oldest-first page of saved UI messages for one conversation |
| `create_agent_conversation` | Create a custom conversation or get/create a thread-bound system conversation |
| `rename_agent_conversation` | Rename one user-managed conversation |
| `delete_agent_conversation` | Permanently delete one user-managed conversation with destructive confirmation |
| `chat_with_mailbox_agent` | Persist one new user message and invoke the Mermail mailbox Assistant |

Inspect live schemas with MCP `tools/list`. These six tools manage the outer conversation surface. They are not the direct mailbox tools injected into the in-app Assistant.

## Mailbox prerequisite

Use `list_mailboxes` and, when status or identity remains unclear, `get_mailbox` before the conversation tools. Select one exact mailbox public id in the authenticated workspace and require it to be usable and receiving. These prerequisite tools are owned by the relevant workspace/inbox skill and are not part of the six-tool mail-agent domain.

## Conversation listing and messages

`list_agent_conversations` requires `mailboxId`. Pass pagination in `query.cursor`. The service returns 10 conversations per page, newest activity first, with `nextCursor`. A continuation cursor is read-only; do not create a conversation until the relevant pages have been checked.

`list_agent_messages` requires `mailboxId` and `conversationId`. Use `query.limit` from 1 to 50 and optional `query.cursor`. Each returned page is chronological even though pagination walks backward from the newest messages. `nextCursor` means older saved messages remain.

Saved messages use AI SDK UI-message parts and may include text, tool calls, tool results, or sanitized errors. Sensitive keys and credential-shaped strings are redacted. Treat Assistant text as narrative unless a responsible tool-result part proves the effect.

## Create and rename

Create a custom conversation:

```json
{
  "mailboxId": "mailbox-public-id",
  "body": {
    "title": "Priority refunds"
  }
}
```

`body.title` is optional for a custom conversation and must be 1–80 characters when supplied. For an email-thread conversation, use `body.threadId` and an optional title. Mermail finds or creates the unique system conversation for that thread, so repeated exact calls do not create parallel thread conversations.

`rename_agent_conversation` requires `mailboxId`, `conversationId`, and `body.title` of 1–80 characters. A conversation with `isSystem: true` or a non-null `systemKey` cannot be renamed.

## Chat contract

`chat_with_mailbox_agent` sends a body to `/api/agent/mailbox`:

```json
{
  "body": {
    "mailboxId": "mailbox-public-id",
    "conversationId": "conversation-id",
    "messages": [
      {
        "id": "unique-user-message-id",
        "role": "user",
        "parts": [
          {
            "type": "text",
            "text": "Summarize the selected support thread. Read only; do not send or change anything."
          }
        ]
      }
    ],
    "thread_id": "exact-email-thread-id",
    "trigger": "submit-message"
  }
}
```

`thread_id` and `trigger` are optional. The latest submitted message must have `role: "user"` and a unique stable id. Mermail persists that one message, rejects replay with `409`, reloads up to 100 canonical saved messages, and then streams the downstream response. Do not resend the entire prior history or mint a new id to bypass a duplicate conflict.

The chat body has no `allowedTools`, `toolAllowlist`, or equivalent server-enforced restriction. Mermail injects its own mailbox tools plus eligible PayBox and connected Composio tools. State task and prohibited effects in the user instruction, but do not describe this as technical tool isolation.

MCP currently returns the mailbox Assistant response as decoded text/event-stream content. Preserve tool-result evidence when the host exposes it; otherwise do not infer a completed write from prose or a completed stream alone.

Common boundaries:

- `400`: invalid body, non-user latest message, invalid title, or forbidden system-conversation mutation.
- `401`/`403`: authentication, workspace scope, role, CSRF, or policy failure.
- `404`: mailbox or conversation is not owned by this user/scope.
- `409`: the exact chat message id was already submitted; inspect state instead of retrying.
- `413`: one sanitized message exceeds the 256 KiB stored-message limit.
- Credits, RPM, model, downstream tool, and provider failures may terminate the stream; do not replay an uncertain effect.

## Delete contract

System/thread/triager conversations cannot be deleted through `delete_agent_conversation`. For a user-managed conversation:

1. Read the exact conversation and confirm `isSystem: false`.
2. Obtain explicit user approval for permanent conversation-history deletion.
3. Call `prepare_destructive_action` with action `delete_agent_conversation` and the exact final arguments.
4. Call `delete_agent_conversation` once with the same arguments and the returned single-use, five-minute `confirmationToken`.

```json
{
  "action": "delete_agent_conversation",
  "arguments": {
    "mailboxId": "mailbox-public-id",
    "conversationId": "conversation-id"
  }
}
```

The delete call repeats those exact path arguments and adds `confirmationToken`; never put the token inside the delegated chat message.

Deleting a conversation does not delete mailbox emails. Do not substitute `delete_email`, and do not use a conversation confirmation token for any draft or email action.
