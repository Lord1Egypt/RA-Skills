---
name: oo-microsoft-teams
description: "Microsoft Teams (microsoft.com). Use this skill for ANY Microsoft Teams request — reading, creating, and updating data. Whenever a task involves Microsoft Teams, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Microsoft Teams"
  author: "OOMOL"
  version: "1.0.2"
  services: ["microsoft_teams"]
  icon: "https://static.oomol.com/logo/third-party/microsoft_teams.svg"
---

# Microsoft Teams

Operate **Microsoft Teams** through your OOMOL-connected account. This skill calls the `microsoft_teams` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Microsoft Teams. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "microsoft_teams" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "microsoft_teams" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_channel` — Get one channel in a Microsoft team.
- `get_current_user` — Get the profile for the connected Microsoft work or school account.
- `get_team` — Get one Microsoft team by ID.
- `list_channel_messages` — List channel posts with optionally expanded replies, or continue root-message or reply pagination.
- `list_chat_messages` — List messages from an existing one-on-one, group, or meeting chat.
- `list_chats` — List chats that include the connected account.
- `list_joined_teams` — List teams that the connected account has joined.
- `list_team_channels` — List channels visible to the connected account in a team.
- `reply_to_channel_message` — Reply to an existing root message in a Microsoft Teams channel. [write]
- `send_channel_message` — Send a new root message to a Microsoft Teams channel. [write]
- `send_chat_message` — Send a message to an existing one-on-one, group, or meeting chat. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Microsoft Teams state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Microsoft Teams is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/microsoft_teams
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Microsoft Teams homepage: https://www.microsoft.com/microsoft-365/microsoft-teams/group-chat-software
- API documentation: https://learn.microsoft.com/en-us/graph/teams-concept-overview
