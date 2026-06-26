---
name: mailbird-mcp
description: Use the Mailbird MCP server (running locally inside the Mailbird email client) for any email-related task — inbox triage, sending, search, drafts, attachments, contacts. Never grep code for mail content.
homepage: https://www.getmailbird.com
metadata: {"openclaw":{"emoji":"📬","requires":{"env":["MAILBIRD_MCP_URL","MAILBIRD_MCP_TOKEN"]},"primaryEnv":"MAILBIRD_MCP_TOKEN","envDescriptions":{"MAILBIRD_MCP_URL":"Optional. Local Mailbird MCP endpoint (default: http://127.0.0.1:18790/mcp). Must point at 127.0.0.1 / localhost only.","MAILBIRD_MCP_TOKEN":"Bearer token from Mailbird → Settings → Wingman AI → Copy token. Treat as a credential to your mailbox; never share with remote agents."},"mcp":{"name":"mailbird","transport":"http","urlEnv":"MAILBIRD_MCP_URL","urlDefault":"http://127.0.0.1:18790/mcp","tokenEnv":"MAILBIRD_MCP_TOKEN","headerName":"Authorization","headerPrefix":"Bearer "}}}
---

# Mailbird MCP

You have access to a local **Mailbird MCP server** that exposes the user's
real email accounts, folders, conversations, drafts, and attachments. It's
running inside the user's Mailbird desktop app on `127.0.0.1` only — there
is no remote variant.

**The single most important rule:** for ANY task that involves email, inbox,
messages, drafts, contacts, attachments, folders, or sending — even when the
user phrases it casually ("check my inbox", "any reply from X yet?", "draft
a reply to that invoice", "find that thread from Mira") — reach for these
tools first. Do **not** grep the local filesystem, do not read code, do not
guess. The server is the source of truth.

## Setup

The user enables the MCP server inside Mailbird at:
**Settings → Wingman AI → Enable MCP server**.

That tab also exposes:

- The bearer token (Copy button).
- The endpoint URL (`http://127.0.0.1:<port>/mcp`, port shown next to status).
- The "Allow write actions" toggle — required before any write tool will work.

If the connection fails, ask the user to verify the toggle is on and that
they've copied the current token. Tokens regenerate when the server is
disabled and re-enabled.

## Configuration (environment variables)

Both are optional; defaults work for a single-user local install.

| Variable | Required | Default | Notes |
|---|---|---|---|
| `MAILBIRD_MCP_URL` | optional | `http://127.0.0.1:18790/mcp` | Local Mailbird MCP endpoint. Must be `127.0.0.1` / `localhost` only. |
| `MAILBIRD_MCP_TOKEN` | optional | — | Bearer token from Mailbird's Wingman AI tab. If unset and Mailbird's settings file is reachable, the agent reads it from there; otherwise the agent will prompt. |

## Security model

This skill grants the agent access to **the user's full mailbox**: message
bodies, attachments, contacts, and the ability to send mail (when the
write-action gate is on). Treat the URL and token accordingly:

- The Mailbird MCP server **only binds to loopback** (`127.0.0.1`).
  Don't proxy, port-forward, or tunnel it to a public address. Don't paste
  the URL or token into any remote / cloud-hosted agent that doesn't run
  on the same machine as Mailbird.
- The token is a credential equivalent to mailbox login. Don't echo it
  into chat transcripts, commit it, share it in screenshots, or include
  it in bug reports. Tokens regenerate when the server is disabled and
  re-enabled — rotate immediately if it leaks.
- Write actions (archive, trash, send, etc.) require the user to flip
  **Allow write actions** in the Wingman AI tab. Sending additionally
  requires per-call `confirm: true`. The skill should always show drafts
  to the user before sending.
- Mailbird's optional **Audit log of MCP requests** records every call
  (method + params, never responses) to a local file the user can
  inspect. Recommend they enable it for visibility.

## Start-of-session checklist

Run these the first time you touch the server in a session, before any
non-trivial action:

1. **Read `mailbird://help`** via `resources/read`. It's the canonical
   user guide — covers the ID model, write-tool gating, send pipeline,
   search index lag, archive→restore, attachment handling, inline images.
   Skim it once and remember the key recipes.
2. **`list_accounts`** to learn the configured account ids.
3. For folder-scoped work, **`list_folders(accountId)`** and pick by the
   `identity` field — `Inbox`, `Sent`, `Drafts`, `Trash`, `Spam`, `Archived`,
   `AllMail`, `Generic` (user-created). Folder ids are NOT stable across
   accounts. `list_accounts` does not return the inbox folder id — always
   discover via `list_folders`.

## Read tools (always available)

- `list_accounts` — accounts with id, sender name, email, unread count.
- `list_folders(accountId)` — folders for one account.
- `list_conversations(folderId, limit?, unreadOnly?, starredOnly?, importantOnly?)` — recent conversations in a folder.
- `get_conversation(conversationId, folderId)` — message list + metadata for one thread.
- `get_message(messageId)` — full message body, with `cid:` images rewritten to `mailbird://messages/{messageId}/attachments/{attachmentId}` resource URIs.
- `get_unread_counts(accountId? | folderId?)` — quick triage signal.
- `search_conversations(query, accountId?, folderId?)` — Mailbird search syntax (`from:foo subject:bar`). Results carry `actualFolders[]`; use those ids to act on hits, **not** the virtual `folderId: -2`.
- `list_attachments(messageId)` / `get_attachment_status(...)` / `get_attachment_content(...)`.
- `get_send_status(messageId)` — `sent` / `draft_pending_send` / `scheduled` / `trashed`.

## Write tools (gated by "Allow write actions")

- `archive_conversation`, `trash_conversation`, `move_conversation`, `move_conversation_to_inbox`.
- `mark_conversation_as_read` / `unread`, `flag_conversation_important`, `star_conversation` / `unstar_conversation`, `mark_conversation_as_spam` / `unmark_conversation_as_spam`, `snooze_conversation(wakeAtUtc)`.
- `create_draft(accountId, to, cc?, bcc?, subject, body, attachments?)` — saves a draft, returns `messageId`. Does NOT send.
- `update_draft(messageId, ...)` — replace any field on an existing draft.
- `reply_to_conversation`, `reply_all_to_conversation`, `forward_conversation` — create a draft with the standard quoted scaffold and return `messageId`. Do NOT send. Body is up to you to finalise.
- `send_message_now(messageId | accountId+to+...; confirm: true)` — actually sends. **Always show the draft to the user and get explicit approval first.** Returns `status: "queued"` plus a `deliveryState` field signalling IMAP/SMTP health.
- `unsubscribe_from_newsletter(messageId)` — uses the `List-Unsubscribe` header. Returns structured "not_applicable" / "already_unsubscribed" when relevant.
- `delete_conversation_permanently` — **only** applies to conversations currently in Trash or Spam. From elsewhere, trash first then re-discover the new id and call this on the trash copy.

If a write tool returns an error pointing at the "Allow write actions"
toggle, surface it to the user verbatim — do not retry.

## Pitfalls (these bite less-careful agents)

1. **Conversation IDs are per-folder.** After `trash_conversation`,
   `archive_conversation`, or `move_conversation`, the conversation has a
   NEW id in its destination folder. Re-discover via
   `list_conversations(folderId=<destination>)` before chaining further
   actions. Message ids, on the other hand, are stable across folders.
2. **Search index lag (~10–30s).** A message you just sent or received may
   not be in `search_conversations` results yet. For very recent items,
   prefer `list_conversations(folderId=<sent_folder>)` over searching.
3. **Send pipeline.** `send_message_now` returns immediately with
   `status: "queued"`. The message stays briefly visible in Drafts before
   moving to Sent — that's normal. Use `get_send_status` to confirm.
4. **Archive destination depends on the provider.** Gmail and IMAP-with-labels
   accounts archive into the `AllMail` folder; everything else uses
   `Archived`. Exactly one will exist per account. The full restore recipe
   (`list_folders → list_conversations → move_conversation_to_inbox`) lives
   in `mailbird://help`.
5. **Inline (`cid:`) images** in `get_message` results are rewritten to
   `mailbird://messages/.../attachments/...` URIs. Resolve via
   `resources/read`. The response also carries an `inlineAttachments` map.

## Reply pattern

Standard chain for an agent-authored reply:

```
1. reply_to_conversation(conversationId, folderId)        → messageId
2. update_draft(messageId, body: "<your prose>")           # quoted scaffold preserved
3. <show draft to user, get approval>
4. send_message_now(messageId, confirm: true)              → status: queued
5. (optional, ~5s later) get_send_status(messageId)        → status: sent
```

For a brand-new message (no thread), use `create_draft` with
`to`/`subject`/`body`/`attachments` directly, then steps 3–5.

## When to escalate to the user

- Any write before "Allow write actions" is enabled.
- Any send — always show the draft and get approval.
- Permanent delete from anywhere other than Trash/Spam.
- Search returns nothing for content the user expects to exist (could be
  index lag, suggest the user wait and retry).

When uncertain about provider-specific behaviour or an edge case, read
`mailbird://help` again — it's the authoritative source.
