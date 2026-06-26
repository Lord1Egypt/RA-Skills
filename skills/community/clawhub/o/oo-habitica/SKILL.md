---
name: oo-habitica
description: "Habitica (habitica.com). Use this skill for ANY Habitica request — reading, creating, updating, and deleting data. Whenever a task involves Habitica, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Habitica"
  author: "OOMOL"
  version: "1.0.1"
  services: ["habitica"]
  icon: "https://static.oomol.com/logo/third-party/habitica.png"
---

# Habitica

Operate **Habitica** through your OOMOL-connected account. This skill calls the `habitica` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Habitica. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "habitica" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "habitica" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_tag` — Create one new Habitica tag. [write]
- `create_task` — Create one new personal Habitica task from a single JSON task object. [write]
- `delete_tag` — Delete one Habitica tag by tag ID. [destructive]
- `delete_task` — Delete one Habitica task by task ID or alias. [destructive]
- `get_task` — Get one Habitica task by task ID or alias.
- `get_user_profile` — Get the authenticated Habitica user's profile with optional userFields filtering.
- `list_my_tasks` — List the authenticated Habitica user's tasks with optional type and dueDate filters.
- `list_tags` — List the authenticated Habitica user's tags.
- `score_task` — Score one Habitica task in the up or down direction.
- `update_tag` — Update one Habitica tag by tag ID. [write]
- `update_task` — Update one Habitica task by task ID or alias. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Habitica state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Habitica is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=habitica
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Habitica homepage: https://habitica.com
