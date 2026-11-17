---
name: oo-parma
description: "Parma (parma.ai). Use this skill for ANY Parma request — reading, creating, updating, and deleting data. Whenever a task involves Parma, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Parma"
  author: "OOMOL"
  version: "1.0.5"
  services: ["parma"]
  icon: "https://static.oomol.com/logo/third-party/parma.png"
---

# Parma

Operate **Parma** through your OOMOL-connected account. This skill calls the `parma` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Parma. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "parma" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "parma" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_relationship_to_group` — Add a Parma relationship to a group. [write]
- `create_note` — Create a note linked to one or more Parma relationships. [write]
- `create_relationship` — Create a person or company relationship in Parma. [write]
- `delete_relationship` — Delete a Parma relationship by ID. [destructive]
- `get_current_user` — Get the current Parma user and workspace account.
- `get_deal` — Get a Parma deal by ID.
- `get_pipeline` — Get a Parma pipeline by ID.
- `get_relationship` — Get a Parma relationship by ID.
- `get_stage` — Get a Parma pipeline stage by ID.
- `get_user` — Get a Parma user by ID.
- `list_deals` — List deals in the connected Parma workspace.
- `list_groups` — List Parma relationship groups, optionally filtered by name.
- `list_notes` — List notes in the connected Parma workspace.
- `list_pipelines` — List pipelines in the connected Parma workspace.
- `list_relationship_groups` — List groups assigned to a Parma relationship.
- `list_relationship_notes` — List notes linked to a Parma relationship.
- `list_relationships` — List and filter relationships in the connected Parma workspace.
- `list_stages` — List pipeline stages in the connected Parma workspace.
- `list_users` — List users in the connected Parma workspace.
- `remove_relationship_from_group` — Remove a Parma relationship from one of its groups. [destructive]
- `update_note` — Update a Parma note by ID. [destructive]
- `update_relationship` — Update a Parma relationship and its custom properties. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Parma state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Parma is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/parma
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Parma homepage: https://parma.ai
- API documentation: https://developers.parma.ai/
