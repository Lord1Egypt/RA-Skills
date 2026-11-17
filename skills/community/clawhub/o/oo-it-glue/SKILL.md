---
name: oo-it-glue
description: "IT Glue (itglue.com). Use this skill for ANY IT Glue request — searching and reading data. Whenever a task involves IT Glue, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "IT Glue"
  author: "OOMOL"
  version: "1.0.5"
  services: ["it_glue"]
  icon: "https://static.oomol.com/logo/third-party/it_glue.svg"
---

# IT Glue

Operate **IT Glue** through your OOMOL-connected account. This skill calls the `it_glue` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected IT Glue. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "it_glue" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "it_glue" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_configuration` — Retrieve one IT Glue configuration by ID, optionally scoped to one organization.
- `get_contact` — Retrieve one IT Glue contact by ID, optionally scoped to one organization.
- `get_organization` — Retrieve one IT Glue organization by ID.
- `get_user` — Retrieve one IT Glue user by ID.
- `list_configurations` — List IT Glue configurations, optionally scoped to one organization, with filters and pagination.
- `list_contacts` — List IT Glue contacts, optionally scoped to one organization, with filters and pagination.
- `list_organizations` — List organizations in an IT Glue account with optional filters and pagination.
- `list_users` — List users in an IT Glue account with optional filters and pagination.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change IT Glue state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — IT Glue is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/it_glue
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- IT Glue homepage: https://www.itglue.com/
- API documentation: https://api.itglue.com/developer/
