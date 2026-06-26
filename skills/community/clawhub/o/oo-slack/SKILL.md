---
name: oo-slack
description: "Slack (slack.com). Use this skill for ANY Slack request — reading, creating, updating, and deleting data. Whenever a task involves Slack, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Slack"
  author: "OOMOL"
  version: "1.0.3"
  services: ["slack"]
  icon: "https://static.oomol.com/logo/third-party/Slack.svg"
---

# Slack

Operate **Slack** through your OOMOL-connected account. This skill calls the `slack` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Slack. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "slack" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "slack" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_reaction` — Add an emoji reaction to a Slack message. [write]
- `delete_file` — Delete a Slack file. [destructive]
- `delete_message` — Delete a Slack message posted by the bot. [destructive]
- `get_channel_messages` — Get recent messages from a Slack conversation.
- `get_conversation` — Get metadata for a Slack conversation.
- `get_file` — Get metadata for a Slack file.
- `get_message_permalink` — Get a permalink for a Slack message.
- `get_reactions` — Get reactions for a Slack message.
- `get_thread` — Get messages in a Slack thread.
- `get_user` — Get metadata for a Slack user.
- `list_channels` — List Slack public channels visible to the bot.
- `list_conversations` — List Slack conversations visible to the bot.
- `list_files` — List Slack files visible to the bot, optionally filtered by channel or user.
- `list_users` — List Slack users visible to the bot.
- `open_conversation` — Open or resume a direct message with one Slack user. [write]
- `post_ephemeral_message` — Post an ephemeral Slack message visible only to one user in a conversation. [write]
- `post_message` — Post a Slack message. Use text for plain messages, or blocks for rich Block Kit layouts with text as fallback. [write]
- `remove_reaction` — Remove an emoji reaction from a Slack message. [destructive]
- `reply_message` — Reply to a Slack thread. Use text, blocks, or attachments for the reply content. [write]
- `schedule_message` — Schedule a Slack message to be posted later. Use text or blocks for the scheduled content. [write]
- `update_message` — Update a Slack message posted by the bot. Provide text, blocks, or attachments as the new message content. [write]
- `upload_file` — Upload a file to Slack using the current external upload flow. Provide fileUrl; binary content is fetched by the connector runtime. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Slack state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Slack is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=slack
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Slack homepage: https://slack.com
