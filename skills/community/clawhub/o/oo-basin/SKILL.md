---
name: oo-basin
description: "Basin (usebasin.com). Use this skill for ANY Basin request — reading, creating, updating, and deleting data. Whenever a task involves Basin, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Basin"
  author: "OOMOL"
  version: "1.0.1"
  services: ["basin"]
  icon: "https://static.oomol.com/logo/third-party/Basin.svg"
---

# Basin

Operate **Basin** through your OOMOL-connected account. This skill calls the `basin` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Basin. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "basin" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "basin" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_form` — Create a new Basin form. [write]
- `create_form_webhook` — Create a new Basin form webhook. [write]
- `create_project` — Create a new Basin project. [write]
- `delete_form` — Delete a Basin form by ID. [destructive]
- `delete_form_webhook` — Delete a Basin form webhook by ID. [destructive]
- `delete_project` — Delete a Basin project by ID. [destructive]
- `delete_submission` — Delete a Basin submission by ID. [destructive]
- `get_form` — Fetch a single Basin form by ID.
- `get_form_webhook` — Fetch a single Basin form webhook by ID.
- `get_project` — Fetch a single Basin project by ID.
- `get_submission` — Fetch a single Basin submission by ID.
- `list_form_webhooks` — List Basin form webhooks with optional filters.
- `list_forms` — List forms available to the current Basin API key.
- `list_projects` — List projects available to the current Basin API key.
- `list_submissions` — List Basin form submissions with optional filters.
- `update_form` — Update an existing Basin form by ID. [write]
- `update_form_webhook` — Update an existing Basin form webhook by ID. [write]
- `update_project` — Update an existing Basin project by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Basin state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Basin is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=basin
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Basin homepage: https://usebasin.com
