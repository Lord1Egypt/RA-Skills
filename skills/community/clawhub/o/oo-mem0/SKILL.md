---
name: oo-mem0
description: "Mem0 (mem0.ai). Use this skill for ANY Mem0 request — reading, creating, updating, and deleting data. Whenever a task involves Mem0, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mem0"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mem0"]
  icon: "https://static.oomol.com/logo/third-party/Mem0.svg"
---

# Mem0

Operate **Mem0** through your OOMOL-connected account. This skill calls the `mem0` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mem0. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mem0" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mem0" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_memories` — Add new memories to Mem0 from messages or direct memory text. [write]
- `delete_memory` — Delete a Mem0 memory by memory ID. [destructive]
- `get_event` — Get a single Mem0 event by event ID.
- `get_events` — List Mem0 events for the current API key.
- `get_memories` — List memories from Mem0 with v2 advanced filters.
- `get_memory` — Get a single memory from Mem0 by memory ID.
- `get_memory_history` — Get the change history of a Mem0 memory by memory ID.
- `get_users` — List user entities from Mem0, optionally scoped by org and project.
- `search_memories` — Search memories in Mem0 with semantic query and optional filters.
- `update_memory` — Update text or metadata of a Mem0 memory by memory ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mem0 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mem0 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mem0
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Mem0 homepage: https://mem0.ai
