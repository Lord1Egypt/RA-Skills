---
name: oo-chatwork
description: "Chatwork (go.chatwork.com). Use this skill for ANY Chatwork request — reading, creating, updating, and deleting data. Whenever a task involves Chatwork, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chatwork"
  author: "OOMOL"
  version: "1.0.1"
  services: ["chatwork"]
  icon: "https://static.oomol.com/logo/third-party/Chatwork.svg"
---

# Chatwork

Operate **Chatwork** through your OOMOL-connected account. This skill calls the `chatwork` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chatwork. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chatwork" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chatwork" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_task` — Create a task in a Chatwork room. [write]
- `delete_message` — Delete one message in a Chatwork room. [destructive]
- `get_contacts` — List Chatwork contacts visible to the authenticated account.
- `get_me` — Get the authenticated Chatwork profile.
- `get_message` — Get one message from a Chatwork room.
- `get_room` — Get metadata for one Chatwork room.
- `get_task` — Get one task from a Chatwork room.
- `list_my_tasks` — List Chatwork tasks assigned to the authenticated account.
- `list_room_members` — List all members in one Chatwork room.
- `list_room_messages` — List messages in one Chatwork room.
- `list_room_tasks` — List tasks in one Chatwork room.
- `list_rooms` — List Chatwork rooms visible to the authenticated account.
- `post_message` — Post a message to a Chatwork room. [write]
- `update_message` — Update one message in a Chatwork room. [write]
- `update_task_status` — Update the completion status of one Chatwork task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chatwork state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chatwork is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=chatwork
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Chatwork homepage: https://go.chatwork.com
