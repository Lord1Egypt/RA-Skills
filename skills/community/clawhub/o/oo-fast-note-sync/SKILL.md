---
name: oo-fast-note-sync
description: "Fast Note Sync (github.com). Use this skill for ANY Fast Note Sync request — reading, creating, updating, and deleting data. Whenever a task involves Fast Note Sync, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Fast Note Sync"
  author: "OOMOL"
  version: "1.0.5"
  services: ["fast_note_sync"]
  icon: "https://static.oomol.com/logo/third-party/fast_note_sync.png"
---

# Fast Note Sync

Operate **Fast Note Sync** through your OOMOL-connected account. This skill calls the `fast_note_sync` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Fast Note Sync. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fast_note_sync" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fast_note_sync" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_attachment` — Permanently delete one FNS attachment by path and path hash. [destructive]
- `delete_note` — Move one FNS note to the recycle bin. [destructive]
- `delete_vault` — Permanently delete an FNS vault and all notes and attachments it contains. [destructive]
- `download_attachment` — Download an FNS attachment into connector file transit and return its transit URL.
- `get_current_user` — Get the user associated with the connected FNS API token.
- `get_note` — Get one FNS note's Markdown content and metadata by path.
- `get_vault` — Get one FNS vault by its numeric id.
- `list_attachments` — List attachment metadata in an FNS vault with search, pagination, and sorting.
- `list_notes` — List note metadata in an FNS vault with pagination and sorting.
- `list_vaults` — List every note vault owned by the authenticated FNS user.
- `search_notes` — Search note paths or note content in an FNS vault.
- `upload_attachment` — Download a public file URL and upload it as an attachment to an FNS vault. [write]
- `upsert_note` — Create an FNS note or replace the content of an existing note at the same path. [destructive]
- `upsert_vault` — Create an FNS vault or update an existing vault when its id is provided. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Fast Note Sync state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Fast Note Sync is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/fast_note_sync
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Fast Note Sync homepage: https://github.com/haierkeys/fast-note-sync-service
- API documentation: https://github.com/haierkeys/fast-note-sync-service/blob/master/docs/REST_API.md
