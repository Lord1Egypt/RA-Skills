---
name: oo-zixflow
description: "Zixflow (zixflow.com). Use this skill for ANY Zixflow request — reading, creating, updating, and deleting data. Whenever a task involves Zixflow, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zixflow"
  author: "OOMOL"
  version: "1.0.4"
  services: ["zixflow"]
  icon: "https://static.oomol.com/logo/third-party/zixflow.svg"
---

# Zixflow

Operate **Zixflow** through your OOMOL-connected account. This skill calls the `zixflow` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zixflow. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zixflow" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zixflow" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_collection_record` — Create a dynamic record in a Zixflow collection. [write]
- `create_list_entry` — Create a dynamic entry in a Zixflow list. [write]
- `delete_collection_record` — Delete a dynamic record from a Zixflow collection. [destructive]
- `delete_list_entry` — Delete a dynamic entry from a Zixflow list. [destructive]
- `get_collection` — Get one Zixflow collection by ID.
- `get_collection_record` — Get one dynamic record from a Zixflow collection.
- `get_list` — Get one Zixflow list by ID.
- `get_list_entry` — Get one dynamic entry from a Zixflow list.
- `get_workspace_member` — Get one Zixflow workspace member by ID.
- `list_collections` — List system and custom collections in the Zixflow workspace.
- `list_lists` — List Zixflow lists in the workspace.
- `list_workspace_members` — List members in the Zixflow workspace.
- `query_collection_records` — Query records from a Zixflow collection using the official filter and paging body.
- `query_list_entries` — Query entries from a Zixflow list using the official filter and paging body.
- `update_collection_record` — Update a dynamic record in a Zixflow collection. [write]
- `update_list_entry` — Update a dynamic entry in a Zixflow list. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zixflow state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zixflow is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zixflow
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zixflow homepage: https://zixflow.com
- API documentation: https://docs.zixflow.com/api-reference/introduction
