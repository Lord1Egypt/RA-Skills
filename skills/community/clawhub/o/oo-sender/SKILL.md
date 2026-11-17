---
name: oo-sender
description: "Sender (sender.net). Use this skill for ANY Sender request — reading, creating, updating, and deleting data. Whenever a task involves Sender, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sender"
  author: "OOMOL"
  version: "1.0.5"
  services: ["sender"]
  icon: "https://static.oomol.com/logo/third-party/sender.svg"
---

# Sender

Operate **Sender** through your OOMOL-connected account. This skill calls the `sender` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sender. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sender" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sender" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_subscribers_to_group` — Add subscribers or a Sender conditions selection to a group. [write]
- `create_field` — Create a Sender custom subscriber field. [write]
- `create_subscriber` — Create a Sender subscriber with optional groups and custom fields. [write]
- `get_campaign` — Get one Sender campaign by ID.
- `get_group` — Get one Sender group by ID.
- `get_subscriber` — Get one Sender subscriber by email address, phone number, or ID.
- `get_workflow` — Get one Sender automation workflow by ID.
- `list_campaigns` — List Sender campaigns with pagination and an optional status filter.
- `list_fields` — List Sender custom subscriber fields with pagination.
- `list_groups` — List Sender groups with pagination.
- `list_subscribers` — List Sender subscribers with pagination.
- `list_workflows` — List Sender automation workflows with pagination and filters.
- `remove_subscribers_from_group` — Remove subscribers or a Sender conditions selection from a group. [destructive]
- `update_subscriber` — Update a Sender subscriber by email address, phone number, or ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sender state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sender is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sender
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sender homepage: https://www.sender.net
- API documentation: https://api.sender.net/
