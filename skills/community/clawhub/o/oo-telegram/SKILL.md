---
name: oo-telegram
description: "Telegram Bot (core.telegram.org). Use this skill for ANY Telegram Bot request — reading, creating, updating, and deleting data. Whenever a task involves Telegram Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Telegram Bot"
  author: "OOMOL"
  version: "1.0.7"
  services: ["telegram"]
  icon: "https://static.oomol.com/logo/third-party/Telegram.svg"
---

# Telegram Bot

Operate **Telegram Bot** through your OOMOL-connected account. This skill calls the `telegram` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Telegram Bot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "telegram" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "telegram" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `answer_callback_query` — Answer an inline keyboard callback query.
- `approve_chat_join_request` — Approve a user's pending request to join a Telegram chat. [write]
- `ban_chat_member` — Ban a user from a group, supergroup, or channel. [destructive]
- `copy_message` — Copy one message without linking back to the original message. [write]
- `copy_messages` — Copy 1-100 messages without links to the originals while preserving album grouping. [write]
- `create_chat_invite_link` — Create an additional Telegram chat invite link with optional expiry or approval rules. [write]
- `decline_chat_join_request` — Decline a user's pending request to join a Telegram chat. [destructive]
- `delete_business_messages` — Delete one or more messages on behalf of a connected Telegram business account. [destructive]
- `delete_message` — Delete a message from a chat. [destructive]
- `delete_messages` — Delete 1-100 messages from one Telegram chat. [destructive]
- `delete_webhook` — Delete the configured webhook and optionally drop pending updates. [destructive]
- `edit_chat_invite_link` — Edit an additional Telegram chat invite link created by the bot. [write]
- `edit_message_text` — Edit the text of a previously sent message or an inline message. [write]
- `export_chat_invite_link` — Export the primary invite link for a Telegram chat. [write]
- `forward_message` — Forward a message from one chat to another. [write]
- `forward_messages` — Forward 1-100 messages while preserving links and album grouping. [write]
- `get_business_connection` — Return the current state and granted rights of a Telegram business connection.
- `get_chat` — Return metadata for a chat the bot can access.
- `get_chat_administrators` — Return the chat administrators visible to the bot.
- `get_chat_member` — Return information about one chat member.
- `get_chat_members_count` — Return the number of members in a chat.
- `get_me` — Validate the bot token and return the bot profile from Telegram Bot API.
- `get_updates` — Poll pending updates for the bot. Use this only when webhook delivery is disabled or for debugging.
- `get_webhook_info` — Return the webhook status configured for the bot.
- `pin_chat_message` — Pin a message in a Telegram chat. [write]
- `promote_chat_member` — Promote, update, or demote a supergroup or channel administrator. [write]
- `read_business_message` — Mark an incoming message as read on behalf of a connected Telegram business account. [write]
- `restrict_chat_member` — Set temporary or permanent permissions for one supergroup member. [write]
- `revoke_chat_invite_link` — Revoke a Telegram chat invite link created by the bot. [destructive]
- `send_animation` — Send a GIF or silent MPEG-4 animation by URL or Telegram file_id. [write]
- `send_audio` — Send an MP3 or M4A audio track by URL or Telegram file_id. [write]
- `send_chat_action` — Show a temporary typing, upload, recording, or location activity status in a chat. [write]
- `send_contact` — Send a phone contact to a Telegram chat. [write]
- `send_dice` — Send an animated dice, darts, basketball, football, bowling, or slot-machine emoji. [write]
- `send_document` — Send a document by URL or existing Telegram file_id. Multipart uploads are intentionally out of scope for this provider pass. [write]
- `send_location` — Send a map location to a chat. [write]
- `send_media_group` — Send an album containing 2-10 photos, videos, documents, or audio items. [write]
- `send_message` — Send a text message to a chat, group, supergroup, channel, or forum topic. [write]
- `send_photo` — Send a photo by URL or existing Telegram file_id. Multipart uploads are intentionally out of scope for this first pass. [write]
- `send_poll` — Send a native Telegram poll to a chat. [write]
- `send_venue` — Send a venue with coordinates, title, address, and optional place identifiers. [write]
- `send_video` — Send an MPEG-4 video by URL or Telegram file_id. [write]
- `send_voice` — Send a playable voice message by URL or Telegram file_id. [write]
- `set_chat_permissions` — Set default permissions for all members of a group or supergroup. [write]
- `set_message_reaction` — Replace the bot's chosen reaction on a Telegram message. [destructive]
- `set_my_commands` — Set the bot command list exposed in Telegram clients. [write]
- `set_webhook` — Configure a webhook endpoint for update delivery. [write]
- `unban_chat_member` — Unban a user so they can join the chat again. [write]
- `unpin_all_chat_messages` — Remove all pinned messages from a Telegram chat. [destructive]
- `unpin_chat_message` — Unpin one message, or the most recently pinned message, from a Telegram chat. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Telegram Bot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Telegram Bot is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/telegram
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Telegram Bot homepage: https://core.telegram.org/bots
- API documentation: https://core.telegram.org/bots
