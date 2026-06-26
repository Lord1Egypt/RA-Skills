---
name: oo-gmail
description: "Gmail (workspace.google.com). Use this skill for ANY Gmail request — reading, creating, updating, and deleting data. Whenever a task involves Gmail, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gmail"
  author: "OOMOL"
  version: "1.0.1"
  services: ["gmail"]
  icon: "https://static.oomol.com/logo/third-party/Gmail.svg"
---

# Gmail

Operate **Gmail** through your OOMOL-connected account. This skill calls the `gmail` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gmail. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gmail" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gmail" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_label_to_email` — Add and/or remove labels on a single Gmail message. Provide at least one label mutation and use label IDs from `list_labels`. [write]
- `batch_modify_messages` — Add and/or remove labels on up to 1,000 Gmail messages in one request. Use this for bulk archive, mark-as-read, or custom label workflows. [write]
- `create_draft` — Create a Gmail draft with a simplified input and output shape. This compatibility action returns only the created `draftId`. [write]
- `create_email_draft` — Create a Gmail draft with recipients, subject, body, and optional threading. Use `threadId` to draft a reply in an existing conversation. [write]
- `create_filter` — Create a Gmail filter with matching criteria and resulting actions. Use this to automatically organize incoming mail. [write]
- `create_label` — Create a new Gmail label and return its internal label ID. Use the returned ID in downstream label modification actions. [write]
- `delete_draft` — Permanently delete a Gmail draft by draft ID instead of sending it. [destructive]
- `delete_filter` — Permanently delete a Gmail filter by filter ID. [destructive]
- `delete_label` — Permanently delete a user-created Gmail label from the mailbox. This removes the label definition itself rather than just detaching it from one message. [destructive]
- `fetch_emails` — List Gmail messages with optional query, label, and pagination filters. Use `detail` to choose between identifiers only, lightweight summaries, or full normalized messages.
- `fetch_message_by_message_id` — Fetch a Gmail message by message ID with a controllable response format. Use this when you need the normalized full message payload instead of the simplified `get_message` output.
- `fetch_message_by_thread_id` — Fetch all messages in a Gmail thread. Use this to inspect the full conversation payload for a known `threadId`.
- `get_auto_forwarding` — Get the current Gmail auto-forwarding configuration, including enabled status, forwarding address, and disposition.
- `get_draft` — Get a Gmail draft by draft ID. Use the `format` parameter to control how much message detail is returned.
- `get_filter` — Get a Gmail filter by filter ID so you can inspect its criteria and actions.
- `get_label` — Get details for a Gmail label, including its name, type, visibility settings, counts, and optional color.
- `get_language_settings` — Get the Gmail display language settings for the connected account.
- `get_message` — Get a Gmail message by message ID with a simplified normalized output. Use this when you only need subject, from, to, date, and body.
- `get_profile` — Get the connected Gmail profile, including mailbox totals and the current `historyId`. Use the returned `historyId` as the checkpoint for incremental sync via `list_history`.
- `get_vacation_settings` — Get the Gmail vacation responder settings, including whether auto-replies are enabled and their current content.
- `list_drafts` — List Gmail drafts with pagination, and optionally hydrate each draft into full message details when `verbose` is true.
- `list_filters` — List Gmail filters for the mailbox. Use this to audit existing rules or avoid creating duplicates.
- `list_forwarding_addresses` — List the forwarding addresses that are registered on the Gmail account.
- `list_history` — List Gmail mailbox change history after a known `startHistoryId`. Use this for incremental sync and checkpoint the latest returned `historyId`.
- `list_labels` — List all system and user-created Gmail labels. Use this to discover the internal label IDs required by label mutation actions.
- `list_threads` — List Gmail threads with optional query filtering and pagination. Spam and trash stay excluded unless you explicitly target them in the query.
- `modify_thread_labels` — Add and/or remove labels on every message in a Gmail thread. Use this when the label change should apply to the whole conversation. [write]
- `move_thread_to_trash` — Move an entire Gmail thread to trash, including all messages in that conversation. [destructive]
- `move_to_trash` — Move a Gmail message to trash. The message remains recoverable until it is permanently deleted by Gmail. [destructive]
- `patch_label` — Patch a user-created Gmail label. Use this for partial updates to the label name, visibility settings, or color. [write]
- `reply_email` — Reply to an existing Gmail thread using the original message's reply headers. This compatibility action returns only the new `messageId`. [write]
- `reply_to_thread` — Reply to an existing Gmail thread while preserving Gmail threading. Use this when you want the reply to stay in the same conversation and optionally override recipients. [write]
- `search_threads` — Search Gmail threads by query and return lightweight thread summaries. Spam and trash stay excluded unless you explicitly target them in the query.
- `send_draft` — Send an existing Gmail draft as-is using the recipients already stored in the draft. Sending is immediate and cannot be scheduled by this action. [write]
- `send_email` — Send an email from the connected Gmail account. At least one recipient and one of subject or body are required. [write]
- `settings_get_imap` — Get the Gmail IMAP settings, including whether IMAP is enabled and how expunge or folder size settings are configured.
- `settings_get_pop` — Get the Gmail POP settings, including access window and message disposition.
- `stop_watch` — Stop Gmail push watch notifications for the mailbox. Use this to disable notifications that were previously created via the watch endpoint. [write]
- `untrash_message` — Restore a previously trashed Gmail message back to the mailbox.
- `untrash_thread` — Restore a previously trashed Gmail thread and its messages.
- `update_draft` — Update an existing Gmail draft in place. Omitted fields fall back to the current draft content, so you can replace only the parts you want to change. [write]
- `update_imap_settings` — Update the Gmail IMAP settings, including enablement, auto-expunge behavior, expunge behavior, or max folder size. [write]
- `update_label` — Update an existing Gmail label's properties, including name, visibility settings, or color. [write]
- `update_language_settings` — Update the Gmail display language settings for the connected account. [write]
- `update_pop_settings` — Update the Gmail POP settings, including access window and disposition behavior. [write]
- `update_vacation_settings` — Update the Gmail vacation responder settings. Use this to configure out-of-office auto-replies and their active time window. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gmail state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gmail is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=gmail
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Gmail homepage: https://workspace.google.com/gmail/
