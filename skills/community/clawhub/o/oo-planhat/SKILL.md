---
name: oo-planhat
description: "Planhat (planhat.com). Use this skill for ANY Planhat request — reading, creating, and updating data. Whenever a task involves Planhat, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Planhat"
  author: "OOMOL"
  version: "1.0.5"
  services: ["planhat"]
  icon: "https://static.oomol.com/logo/third-party/planhat.svg"
---

# Planhat

Operate **Planhat** through your OOMOL-connected account. This skill calls the `planhat` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Planhat. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "planhat" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "planhat" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_company` — Create a Planhat company. [write]
- `create_enduser` — Create a Planhat end user. [write]
- `get_company` — Get a Planhat company by ID, externalId, or sourceId.
- `get_enduser` — Get a Planhat end user by ID, externalId, or sourceId.
- `list_companies` — List Planhat companies with offset pagination.
- `list_endusers` — List Planhat end users with offset pagination.
- `update_company` — Update a Planhat company by ID, externalId, or sourceId. [write]
- `update_enduser` — Update a Planhat end user by ID, externalId, or sourceId. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Planhat state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Planhat is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/planhat
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Planhat homepage: https://www.planhat.com
- API documentation: https://docs.planhat.com/
