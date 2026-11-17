---
name: oo-zotero
description: "Zotero (zotero.org). Use this skill for ANY Zotero request — reading, creating, updating, and deleting data. Whenever a task involves Zotero, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zotero"
  author: "OOMOL"
  version: "1.0.5"
  services: ["zotero"]
  icon: "https://static.oomol.com/logo/third-party/zotero.png"
---

# Zotero

Operate **Zotero** through your OOMOL-connected account. This skill calls the `zotero` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zotero. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zotero" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zotero" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_collection` — Create one collection in a Zotero user or group library. [write]
- `create_item` — Create one bibliographic item in a Zotero user or group library. [write]
- `delete_collection` — Delete one Zotero collection at a known version. [destructive]
- `delete_item` — Delete one Zotero item at a known version. [destructive]
- `get_collection` — Retrieve one collection from a Zotero user or group library.
- `get_item` — Retrieve one item from a Zotero user or group library.
- `list_collections` — List collections in a Zotero user or group library.
- `list_groups` — List Zotero groups accessible to the user connected by the current API key.
- `list_items` — List or search items in a Zotero user or group library.
- `update_collection` — Replace the editable fields of one Zotero collection at a known version. [destructive]
- `update_item` — Partially update one Zotero item at a known version. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zotero state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zotero is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zotero
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zotero homepage: https://www.zotero.org
- API documentation: https://www.zotero.org/support/dev/web_api/v3/basics
