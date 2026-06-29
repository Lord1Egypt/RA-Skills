---
name: oo-givebutter
description: "Givebutter (givebutter.com). Use this skill for ANY Givebutter request — searching and reading data. Whenever a task involves Givebutter, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Givebutter"
  author: "OOMOL"
  version: "1.0.0"
  services: ["givebutter"]
  icon: "https://static.oomol.com/logo/third-party/givebutter.svg"
---

# Givebutter

Operate **Givebutter** through your OOMOL-connected account. This skill calls the `givebutter` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Givebutter. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "givebutter" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "givebutter" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_campaign` — Retrieve one Givebutter campaign by ID.
- `get_chapter` — Retrieve one Givebutter chapter by ID.
- `get_contact` — Retrieve one Givebutter contact by ID.
- `get_fund` — Retrieve one Givebutter fund by ID.
- `get_recurring_plan` — Retrieve one Givebutter recurring plan by ID.
- `get_transaction` — Retrieve one Givebutter transaction by ID.
- `list_campaigns` — List Givebutter campaigns with pagination and optional official filters.
- `list_chapters` — List Givebutter chapters with pagination and optional official filters.
- `list_contacts` — List Givebutter contacts with pagination and optional official filters.
- `list_funds` — List Givebutter funds with pagination and optional official filters.
- `list_recurring_plans` — List Givebutter recurring plans with pagination and optional official filters.
- `list_transactions` — List Givebutter transactions with pagination and optional official filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Givebutter state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Givebutter is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=givebutter
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Givebutter homepage: https://givebutter.com
