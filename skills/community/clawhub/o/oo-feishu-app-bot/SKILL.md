---
name: oo-feishu-app-bot
description: "Feishu App Bot (open.feishu.cn). Use this skill for ANY Feishu App Bot request — reading, creating, updating, and deleting data. Whenever a task involves Feishu App Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Feishu App Bot"
  author: "OOMOL"
  version: "1.0.1"
  services: ["feishu_app_bot"]
  icon: "https://static.oomol.com/logo/third-party/feishu_custom_bot.svg"
---

# Feishu App Bot

Operate **Feishu App Bot** through your OOMOL-connected account. This skill calls the `feishu_app_bot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Feishu App Bot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "feishu_app_bot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "feishu_app_bot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_message_reaction` — Add one emoji reaction to a Feishu/Lark message. [write]
- `download_file` — Download one Feishu/Lark file by file key and upload it to transit storage.
- `download_image` — Download one Feishu/Lark image by image key and upload it to transit storage.
- `edit_message` — Edit a Feishu/Lark text or post message sent by the app bot. [write]
- `get_chat` — Fetch one Feishu/Lark chat by `chat_id`.
- `get_message` — Fetch one Feishu/Lark message by `message_id`.
- `list_chat_members` — List visible members in one Feishu/Lark chat.
- `list_chats` — List chats that the Feishu/Lark app bot currently belongs to.
- `list_message_reactions` — List emoji reactions on one Feishu/Lark message.
- `list_messages` — List Feishu/Lark history messages from a chat or thread.
- `list_pins` — List pin records in one Feishu/Lark chat and time window.
- `pin_message` — Pin one Feishu/Lark message inside its chat.
- `recall_message` — Recall one Feishu/Lark message that the app bot sent.
- `remove_message_reaction` — Remove one Feishu/Lark message reaction by `reaction_id`. [destructive]
- `remove_pin` — Remove the pin state from one Feishu/Lark message. [destructive]
- `reply_message` — Reply to an existing Feishu/Lark message as the app bot. [write]
- `search_chats` — Search chats visible to the Feishu/Lark app bot by keyword.
- `send_message` — Send a Feishu/Lark app bot message to a user or chat. [write]
- `upload_file` — Upload one public file URL to Feishu/Lark and return the file key for message sending. [write]
- `upload_image` — Upload one public image URL to Feishu/Lark and return the image key for message sending. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Feishu App Bot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Feishu App Bot is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=feishu_app_bot
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Feishu App Bot homepage: https://open.feishu.cn
