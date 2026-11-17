---
name: oo-firehydrant
description: "FireHydrant (firehydrant.com). Use this skill for ANY FireHydrant request — reading, creating, and updating data. Whenever a task involves FireHydrant, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "FireHydrant"
  author: "OOMOL"
  version: "1.0.4"
  services: ["firehydrant"]
  icon: "https://static.oomol.com/logo/third-party/firehydrant.png"
---

# FireHydrant

Operate **FireHydrant** through your OOMOL-connected account. This skill calls the `firehydrant` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected FireHydrant. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "firehydrant" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "firehydrant" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_incident` — Create a FireHydrant incident using a JSON-friendly request body. [write]
- `get_environment` — Retrieve a single FireHydrant environment by UUID or slug.
- `get_incident` — Retrieve a single FireHydrant incident by ID.
- `get_service` — Retrieve a single FireHydrant service by UUID or slug.
- `list_environments` — List FireHydrant environments with pagination and search filters.
- `list_incidents` — List FireHydrant incidents with stable pagination and common filters.
- `list_services` — List FireHydrant services with pagination and search filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change FireHydrant state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — FireHydrant is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/firehydrant
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- FireHydrant homepage: https://firehydrant.com
- API documentation: https://docs.firehydrant.com/reference/firehydrant-api
