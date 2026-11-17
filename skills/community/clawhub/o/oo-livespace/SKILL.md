---
name: oo-livespace
description: "Livespace (livespace.io). Use this skill for ANY Livespace request — reading, creating, updating, and deleting data. Whenever a task involves Livespace, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Livespace"
  author: "OOMOL"
  version: "1.0.4"
  services: ["livespace"]
  icon: "https://static.oomol.com/logo/third-party/livespace.svg"
---

# Livespace

Operate **Livespace** through your OOMOL-connected account. This skill calls the `livespace` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Livespace. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "livespace" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "livespace" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_company` — Create a Livespace company. [write]
- `create_deal` — Create a Livespace deal. [write]
- `create_person` — Create a Livespace person. [write]
- `create_task` — Create a Livespace todo. [write]
- `delete_company` — Delete a Livespace company. [destructive]
- `delete_deal` — Delete a Livespace deal. [destructive]
- `delete_person` — Delete a Livespace person. [destructive]
- `delete_task` — Delete a Livespace todo. [destructive]
- `get_company` — Get a Livespace company by ID.
- `get_current_user` — Get information about the current Livespace API user.
- `get_deal` — Get a Livespace deal by ID.
- `get_person` — Get a Livespace person by ID.
- `get_task` — Get a Livespace todo by ID.
- `get_tasks_for_object` — List Livespace todos assigned to an object.
- `list_companies` — List Livespace companies with simple pagination.
- `list_deals` — List Livespace deals using optional Livespace filters.
- `list_people` — List Livespace people with simple pagination.
- `list_tasks` — List Livespace todos using optional Livespace filters.
- `list_users` — List Livespace users visible to the API credential.
- `search_companies` — Search Livespace companies.
- `search_deals` — Search Livespace deals.
- `search_people` — Search Livespace people.
- `update_company` — Update a Livespace company. [write]
- `update_deal` — Update a Livespace deal. [write]
- `update_person` — Update a Livespace person. [write]
- `update_task` — Update a Livespace todo. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Livespace state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Livespace is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/livespace
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Livespace homepage: https://www.livespace.io/
- API documentation: https://support.livespace.io/en/articles/3572069-api-documentation-and-information
