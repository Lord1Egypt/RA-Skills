---
name: oo-ecologi
description: "Ecologi (ecologi.com). Use this skill for ANY Ecologi request — reading, creating, and updating data. Whenever a task involves Ecologi, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ecologi"
  author: "OOMOL"
  version: "1.0.5"
  services: ["ecologi"]
  icon: "https://static.oomol.com/logo/third-party/ecologi.png"
---

# Ecologi

Operate **Ecologi** through your OOMOL-connected account. This skill calls the `ecologi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ecologi. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ecologi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ecologi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_carbon_offset_totals` — Get the confirmed and pending tonnes of carbon emissions avoided by an Ecologi user.
- `get_carbon_removal_totals` — Get the confirmed and pending tonnes of carbon removed by an Ecologi user.
- `get_habitat_restoration_totals` — Get the confirmed and pending square metres of habitat restored by an Ecologi user.
- `get_total_impact` — Get a combined view of an Ecologi user's confirmed and pending impact totals.
- `get_tree_totals` — Get the confirmed and pending number of trees funded by an Ecologi user.
- `purchase_carbon_avoidance` — Purchase Ecologi carbon avoidance by kilograms or tonnes. [write]
- `purchase_carbon_removal` — Purchase permanent Ecologi carbon removal measured in kilograms. [write]
- `purchase_habitat_restoration` — Purchase Ecologi habitat restoration measured in square metres. [write]
- `purchase_local_trees` — Purchase Ecologi tree planting in the UK, US, Australia, or Brazil. [write]
- `purchase_trees` — Purchase Ecologi tree planting with optional test mode, attribution, notification, and idempotency. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ecologi state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ecologi is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ecologi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Ecologi homepage: https://ecologi.com
- API documentation: https://docs.ecologi.com/
