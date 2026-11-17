---
name: oo-wecom-bot
description: "WeCom Bot (work.weixin.qq.com). Use this skill for ANY WeCom Bot request — reading, creating, updating, and deleting data. Whenever a task involves WeCom Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WeCom Bot"
  author: "OOMOL"
  version: "1.0.7"
  services: ["wecom_bot"]
  icon: "https://static.oomol.com/logo/third-party/wecom_bot.png"
---

# WeCom Bot

Operate **WeCom Bot** through your OOMOL-connected account. This skill calls the `wecom_bot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WeCom Bot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wecom_bot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wecom_bot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_schedule_attendees` — Add attendees to a WeCom schedule. [write]
- `call_tool` — Call a dynamically discovered WeCom MCP tool that does not have a curated action yet. [destructive]
- `cancel_meeting` — Cancel a scheduled WeCom meeting. [destructive]
- `cancel_schedule` — Cancel a WeCom schedule. [destructive]
- `change_todo_user_status` — Change one follower's status on a WeCom todo. [destructive]
- `check_availability` — Read busy time slots for up to 10 WeCom members.
- `create_doc` — Create an empty WeCom document, online sheet, or smart sheet. [write]
- `create_meeting` — Create a scheduled WeCom meeting. [write]
- `create_schedule` — Create a WeCom schedule with attendees and reminders. [write]
- `create_todo` — Create a WeCom todo with followers, deadline, and reminders. [write]
- `del_schedule_attendees` — Remove attendees from a WeCom schedule. [write]
- `delete_todo` — Delete a WeCom todo. [destructive]
- `download_message_media` — Download WeCom message media and return a Connector transit URL instead of base64 or a server-local path.
- `edit_doc_content` — Replace all content in a WeCom document with Markdown. [write]
- `get_doc_content` — Read complete WeCom document content as Markdown with polling handled internally.
- `get_meeting_info` — Get complete details for a WeCom meeting.
- `get_message` — Read recent messages from one WeCom direct chat or group chat.
- `get_msg_chat_list` — List chats that had messages during a time range.
- `get_schedule_detail` — Get details for up to 50 WeCom schedules.
- `get_schedule_list_by_range` — List WeCom schedule IDs within a time range.
- `get_todo_detail` — Get details for up to 20 WeCom todos.
- `get_todo_list` — List WeCom todos for one follower with optional time and status filters.
- `get_userlist` — List WeCom members visible to the API-mode smart bot.
- `list_tools` — List the current WeCom MCP tools and input schemas available to this bot.
- `list_user_meetings` — List WeCom meetings in a time range.
- `search_todo_userid` — Search WeCom users by name or alias for todo assignment.
- `send_image_message` — Send an image message through the WeCom bot webhook. [write]
- `send_markdown_message` — Send a markdown message through the WeCom bot webhook. [write]
- `send_markdown_v2_message` — Send a markdown_v2 message through the WeCom bot webhook. [write]
- `send_message` — Send a text message to a WeCom direct chat or group chat. [write]
- `send_news_message` — Send a news message through the WeCom bot webhook. [write]
- `send_text_message` — Send a text message through the WeCom bot webhook. [write]
- `set_invite_meeting_members` — Replace the full invitee list for a WeCom meeting. [write]
- `sheet_add_sub` — Add a sub-sheet to a WeCom online sheet. [write]
- `sheet_append_data` — Append one row to the end of a WeCom online sheet. [write]
- `sheet_delete_sub` — Permanently delete a sub-sheet from a WeCom online sheet. [destructive]
- `sheet_get_info` — Get online-sheet metadata and sub-sheet IDs.
- `sheet_update_range_data` — Write cells and formats into a specified online-sheet range. [write]
- `smartpage_create` — Create a WeCom smart page from inline text or Markdown pages. [write]
- `smartpage_export` — Export complete WeCom smart-page content as Markdown with polling handled internally. [write]
- `smartsheet_add_fields` — Add fields to a WeCom smart-sheet sub-sheet. [write]
- `smartsheet_add_records` — Add records to a WeCom smart sheet, uploading `fileUrl` attachments before the write. [write]
- `smartsheet_add_sheet` — Add a sub-sheet to a WeCom smart sheet. [write]
- `smartsheet_delete_fields` — Permanently delete fields from a WeCom smart-sheet sub-sheet. [destructive]
- `smartsheet_delete_records` — Permanently delete records from a WeCom smart-sheet sub-sheet. [destructive]
- `smartsheet_delete_sheet` — Permanently delete a WeCom smart-sheet sub-sheet. [destructive]
- `smartsheet_get_fields` — List fields in a WeCom smart-sheet sub-sheet.
- `smartsheet_get_records` — Read a page of records from a WeCom smart-sheet sub-sheet.
- `smartsheet_get_sheet` — List sub-sheets in a WeCom smart sheet.
- `smartsheet_update_fields` — Rename fields in a WeCom smart-sheet sub-sheet without changing their types. [write]
- `smartsheet_update_records` — Update WeCom smart-sheet records, uploading `fileUrl` attachments before the write. [write]
- `smartsheet_update_sheet` — Rename a WeCom smart-sheet sub-sheet. [write]
- `update_schedule` — Update selected fields on a WeCom schedule. [write]
- `update_todo` — Update a WeCom todo's content, followers, status, deadline, or reminders. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WeCom Bot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WeCom Bot is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, custom credential) at:

  ```text
  https://console.oomol.com/connections/wecom_bot
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WeCom Bot homepage: https://work.weixin.qq.com
- API documentation: https://developer.work.weixin.qq.com/document/path/91770
