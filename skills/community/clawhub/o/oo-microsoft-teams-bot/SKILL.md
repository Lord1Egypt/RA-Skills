---
name: oo-microsoft-teams-bot
description: "Microsoft Teams Bot (learn.microsoft.com). Use this skill for ANY Microsoft Teams Bot request — reading, creating, updating, and deleting data. Whenever a task involves Microsoft Teams Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Microsoft Teams Bot"
  author: "OOMOL"
  version: "1.0.1"
  services: ["microsoft_teams_bot"]
  icon: "https://static.oomol.com/logo/third-party/microsoft_teams_bot.svg"
---

# Microsoft Teams Bot

Operate **Microsoft Teams Bot** through your OOMOL-connected account. This skill calls the `microsoft_teams_bot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Microsoft Teams Bot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "microsoft_teams_bot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "microsoft_teams_bot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_conversation` — Start a proactive one-on-one conversation with a user, or a new thread in a team's general channel, and optionally post a first message. [write]
- `delete_message` — Delete a message the bot previously sent. [destructive]
- `list_conversation_members` — List one page of the members of a Teams conversation.
- `list_team_channels` — List the channels of a team the bot is installed in. The Bot Connector cannot list the teams a bot is in: learn a team's ID from channelData.team.id on its activities, such as the conversationUpdate Teams sends when the bot is added to the team.
- `reply_to_message` — Reply to an existing activity in a Teams conversation, with text, cards such as an Adaptive Card, or both. [write]
- `send_message` — Send a new message from the bot into an existing Teams conversation, with text, cards such as an Adaptive Card, or both. [write]
- `update_message` — Replace a message the bot previously sent. The new text and cards replace the old message entirely, so leaving out attachments removes its cards, for example to swap a card with buttons for one without. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Microsoft Teams Bot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Microsoft Teams Bot is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/microsoft_teams_bot
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Microsoft Teams Bot homepage: https://learn.microsoft.com/en-us/azure/bot-service/
