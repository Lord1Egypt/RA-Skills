---
name: oo-fireflies
description: "Fireflies (fireflies.ai). Use this skill for ANY Fireflies request — reading, creating, updating, and deleting data. Whenever a task involves Fireflies, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Fireflies"
  author: "OOMOL"
  version: "1.0.1"
  services: ["fireflies"]
  icon: "https://static.oomol.com/logo/third-party/Fireflies.svg"
---

# Fireflies

Operate **Fireflies** through your OOMOL-connected account. This skill calls the `fireflies` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Fireflies. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fireflies" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fireflies" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `continue_askfred_thread` — Continue a Fireflies AskFred thread with a follow-up question.
- `create_askfred_thread` — Create a Fireflies AskFred thread from a meeting question. [write]
- `create_bite` — Create a Fireflies bite from a transcript time range. [write]
- `delete_askfred_thread` — Delete a Fireflies AskFred thread by thread ID. [destructive]
- `delete_transcript` — Delete a Fireflies transcript by transcript ID. [destructive]
- `execute_graphql_query` — Execute a raw read-only Fireflies GraphQL query and return the raw response.
- `get_askfred_thread` — Get a Fireflies AskFred thread by thread ID.
- `get_bite` — Get a Fireflies bite by bite ID.
- `get_current_user` — Get the authenticated Fireflies user for the current API key.
- `get_transcript` — Get a Fireflies transcript by transcript ID.
- `get_user` — Get a Fireflies user by user ID.
- `list_ai_app_outputs` — List Fireflies AI app outputs for transcripts or app IDs.
- `list_askfred_threads` — List Fireflies AskFred conversation threads.
- `list_bites` — List Fireflies bites using the available bite filters.
- `list_channels` — List Fireflies channels visible to the current API key.
- `list_transcripts` — List Fireflies transcripts with official filters and include flags.
- `list_user_groups` — List Fireflies user groups visible to the current API key.
- `list_users` — List Fireflies users visible to the current API key.
- `set_user_role` — Set a Fireflies user's role to admin or user. [write]
- `update_meeting_channel` — Update the Fireflies channel assignments for one or more meetings. [write]
- `update_meeting_privacy` — Update the privacy value for a Fireflies meeting. [write]
- `update_meeting_title` — Update the title for a Fireflies meeting. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Fireflies state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Fireflies is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=fireflies
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Fireflies homepage: https://www.fireflies.ai
