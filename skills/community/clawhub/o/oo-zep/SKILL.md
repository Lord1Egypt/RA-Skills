---
name: oo-zep
description: "Zep (getzep.com). Use this skill for ANY Zep request — reading, creating, updating, and deleting data. Whenever a task involves Zep, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zep"
  author: "OOMOL"
  version: "1.0.4"
  services: ["zep"]
  icon: "https://static.oomol.com/logo/third-party/zep.png"
---

# Zep

Operate **Zep** through your OOMOL-connected account. This skill calls the `zep` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zep. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zep" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zep" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_thread_messages` — Add chat messages to a Zep thread, ingest them into the user's graph, and optionally return current context. [write]
- `create_thread` — Create a conversation thread for an existing Zep user. [write]
- `create_user` — Create a Zep user that can own conversation threads and graph memory. [write]
- `delete_thread` — Delete a Zep conversation thread and its thread-specific memory. [destructive]
- `delete_user` — Delete a Zep user and the threads and graph artifacts associated with that user. [destructive]
- `get_project` — Retrieve the Zep project associated with the connected API key.
- `get_thread_context` — Retrieve the most relevant context from a user's graph for the current Zep thread.
- `get_thread_messages` — Retrieve messages from a Zep thread with cursor or recent-message controls.
- `get_user` — Retrieve one Zep user by its application-defined identifier.
- `list_threads` — List Zep conversation threads with pagination and ordering controls.
- `list_users` — List Zep users with pagination, search, and ordering controls.
- `update_user` — Update the profile, metadata, time zone, or ontology setting of a Zep user. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zep state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zep is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zep
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zep homepage: https://www.getzep.com
- API documentation: https://help.getzep.com/sdk-reference
