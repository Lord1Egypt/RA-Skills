---
name: oo-telegram
description: "Telegram Bot (core.telegram.org). Use this skill for ANY Telegram Bot request — reading, creating, updating, and deleting data. Whenever a task involves Telegram Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Telegram Bot"
  author: "OOMOL"
  version: "1.0.1"
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
- `create_chat_invite_link` — Export a new primary invite link for a chat. This maps to Telegram Bot API exportChatInviteLink. [write]
- `delete_message` — Delete a message from a chat. [destructive]
- `delete_webhook` — Delete the configured webhook and optionally drop pending updates. [destructive]
- `edit_message_text` — Edit the text of a previously sent message or an inline message. [write]
- `forward_message` — Forward a message from one chat to another. [write]
- `get_chat` — Return metadata for a chat the bot can access.
- `get_chat_administrators` — Return the chat administrators visible to the bot.
- `get_chat_history` — Get chat history by polling getUpdates, filtering to one chat, and returning message-bearing updates only. This helper requires webhook delivery to be disabled.
- `get_chat_member` — Return information about one chat member.
- `get_chat_members_count` — Return the number of members in a chat.
- `get_me` — Validate the bot token and return the bot profile from Telegram Bot API.
- `get_updates` — Poll pending updates for the bot. Use this only when webhook delivery is disabled or for debugging.
- `get_webhook_info` — Return the webhook status configured for the bot.
- `send_document` — Send a document by URL or existing Telegram file_id. Multipart uploads are intentionally out of scope for this provider pass. [write]
- `send_location` — Send a map location to a chat. [write]
- `send_message` — Send a text message to a chat, group, supergroup, channel, or forum topic. [write]
- `send_photo` — Send a photo by URL or existing Telegram file_id. Multipart uploads are intentionally out of scope for this first pass. [write]
- `send_poll` — Send a native Telegram poll to a chat. [write]
- `set_my_commands` — Set the bot command list exposed in Telegram clients. [write]
- `set_webhook` — Configure a webhook endpoint for update delivery. [write]

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
  https://console.oomol.com/app-connections?provider=telegram
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Telegram Bot homepage: https://core.telegram.org/bots
