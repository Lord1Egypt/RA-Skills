---
name: oo-pushbullet
description: "Pushbullet (pushbullet.com). Use this skill for ANY Pushbullet request — reading, creating, updating, and deleting data. Whenever a task involves Pushbullet, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pushbullet"
  author: "OOMOL"
  version: "1.0.1"
  services: ["pushbullet"]
  icon: "https://static.oomol.com/logo/third-party/Pushbullet.svg"
---

# Pushbullet

Operate **Pushbullet** through your OOMOL-connected account. This skill calls the `pushbullet` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pushbullet. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pushbullet" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pushbullet" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_chat` — Create a Pushbullet chat with another user or email address. [write]
- `create_device` — Create a new Pushbullet device for the current user. [write]
- `create_push` — Send a Pushbullet note, link, file, or list push to the current user or a selected target. [write]
- `delete_all_pushes` — Delete all pushes belonging to the current Pushbullet user. [destructive]
- `delete_chat` — Delete one Pushbullet chat by identifier. [destructive]
- `delete_device` — Delete one Pushbullet device by identifier. [destructive]
- `delete_push` — Delete one Pushbullet push by identifier. [destructive]
- `get_current_user` — Get the currently authenticated Pushbullet user profile.
- `list_chats` — List all chats for the current Pushbullet user.
- `list_devices` — List all registered devices for the current Pushbullet user.
- `list_pushes` — List Pushbullet pushes with optional active, modified-after, and cursor filters.
- `update_chat` — Mute or unmute an existing Pushbullet chat. [write]
- `update_device` — Update metadata for an existing Pushbullet device. [write]
- `update_push` — Update a Pushbullet push, typically to dismiss it or update list items. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pushbullet state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pushbullet is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pushbullet
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Pushbullet homepage: https://www.pushbullet.com
