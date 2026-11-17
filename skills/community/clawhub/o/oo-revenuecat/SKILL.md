---
name: oo-revenuecat
description: "RevenueCat (revenuecat.com). Use this skill for ANY RevenueCat request — searching and reading data. Whenever a task involves RevenueCat, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "RevenueCat"
  author: "OOMOL"
  version: "1.0.4"
  services: ["revenuecat"]
  icon: "https://static.oomol.com/logo/third-party/revenuecat.svg"
---

# RevenueCat

Operate **RevenueCat** through your OOMOL-connected account. This skill calls the `revenuecat` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected RevenueCat. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "revenuecat" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "revenuecat" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_customer` — Retrieve a RevenueCat customer and optionally expand the customer's attributes.
- `get_overview_metrics` — Retrieve overview metrics for a RevenueCat project.
- `get_revenue_metric` — Retrieve total RevenueCat project revenue for an inclusive date range.
- `get_subscription` — Retrieve a RevenueCat subscription by its subscription ID.
- `list_customer_active_entitlements` — List the entitlements currently active for a RevenueCat customer.
- `list_customer_subscriptions` — List subscriptions belonging to a RevenueCat customer.
- `list_customers` — List customers in a RevenueCat project, optionally searching by email or customer identifier.
- `list_entitlements` — List entitlement definitions configured in a RevenueCat project.
- `list_offerings` — List offerings configured in a RevenueCat project, optionally expanding packages and products.
- `list_products` — List products configured in a RevenueCat project.
- `list_projects` — List RevenueCat projects accessible to the configured secret API key.
- `search_subscriptions` — Find subscriptions by a store subscription identifier such as an Apple transaction ID or Google order ID.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change RevenueCat state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — RevenueCat is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/revenuecat
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- RevenueCat homepage: https://www.revenuecat.com
- API documentation: https://www.revenuecat.com/docs/api-v2
