---
name: oo-raindrop
description: "Raindrop.io (raindrop.io). Use this skill for ANY Raindrop.io request — reading, creating, updating, and deleting data. Whenever a task involves Raindrop.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Raindrop.io"
  author: "OOMOL"
  version: "1.0.4"
  services: ["raindrop"]
  icon: "https://static.oomol.com/logo/third-party/raindrop.svg"
---

# Raindrop.io

Operate **Raindrop.io** through your OOMOL-connected account. This skill calls the `raindrop` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Raindrop.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "raindrop" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "raindrop" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_collection` — Create a Raindrop.io bookmark collection. [write]
- `create_raindrop` — Create a bookmark from a URL in Raindrop.io. [write]
- `delete_collection` — Delete a collection and move its bookmarks to Trash. [destructive]
- `delete_raindrop` — Move a bookmark to Trash, or permanently delete it when already in Trash. [destructive]
- `get_collection` — Get one Raindrop.io collection by ID.
- `get_raindrop` — Get one Raindrop.io bookmark by ID.
- `get_user` — Get the authenticated Raindrop.io user profile.
- `list_collections` — List root collections and optionally include nested child collections.
- `list_raindrops` — List or search bookmarks in a collection or across all collections.
- `list_tags` — List tags across all bookmarks or within one collection.
- `update_collection` — Update an existing Raindrop.io collection. [write]
- `update_raindrop` — Update an existing Raindrop.io bookmark. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Raindrop.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Raindrop.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/raindrop
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Raindrop.io homepage: https://raindrop.io
- API documentation: https://developer.raindrop.io/
