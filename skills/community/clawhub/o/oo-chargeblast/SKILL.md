---
name: oo-chargeblast
description: "Chargeblast (chargeblast.com). Use this skill for ANY Chargeblast request — reading, creating, and updating data. Whenever a task involves Chargeblast, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chargeblast"
  author: "OOMOL"
  version: "1.0.5"
  services: ["chargeblast"]
  icon: "https://static.oomol.com/logo/third-party/chargeblast.png"
---

# Chargeblast

Operate **Chargeblast** through your OOMOL-connected account. This skill calls the `chargeblast` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chargeblast. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chargeblast" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chargeblast" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_credit_request` — Create a Chargeblast credit request for a rejected alert. [write]
- `get_alert` — Fetch one Chargeblast alert by identifier.
- `get_order` — Fetch one Chargeblast order by identifier, including receipt and eligibility data.
- `list_alerts` — List Chargeblast alerts with optional alert-network filtering and pagination.
- `list_deflection_logs` — List Chargeblast digital receipt and deflection lookup logs.
- `list_merchants` — List merchants in a Chargeblast account.
- `list_orders` — List Chargeblast order identifiers with pagination.
- `update_alert` — Action one Chargeblast alert with an official reason code and optional expiration-time handling. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chargeblast state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chargeblast is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/chargeblast
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Chargeblast homepage: https://www.chargeblast.com
- API documentation: https://docs.chargeblast.com/
