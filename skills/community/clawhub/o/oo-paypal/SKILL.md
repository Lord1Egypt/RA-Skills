---
name: oo-paypal
description: "PayPal (paypal.com). Use this skill for ANY PayPal request — reading, creating, updating, and deleting data. Whenever a task involves PayPal, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PayPal"
  author: "OOMOL"
  version: "1.0.5"
  services: ["paypal"]
  icon: "https://static.oomol.com/logo/third-party/paypal.svg"
---

# PayPal

Operate **PayPal** through your OOMOL-connected account. This skill calls the `paypal` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PayPal. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "paypal" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "paypal" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_tracking` — Add shipment tracking information to a completed capture in a PayPal order. [write]
- `authorize_order` — Authorize an approved PayPal order so its funds can be captured later. [write]
- `capture_authorization` — Capture all or part of an authorized PayPal payment. [write]
- `capture_order` — Capture payment for an approved PayPal order with CAPTURE intent. [write]
- `create_order` — Create a PayPal order and return the approval links needed to continue checkout. [write]
- `get_authorization` — Retrieve details for a PayPal authorized payment.
- `get_balances` — Retrieve PayPal account balances, including available and withheld amounts by currency.
- `get_capture` — Retrieve details for a captured PayPal payment.
- `get_order` — Retrieve the current details and status of a PayPal order.
- `get_refund` — Retrieve the current details and status of a PayPal refund.
- `list_transactions` — List PayPal account transactions for reconciliation, support, and financial reporting.
- `refund_capture` — Refund all or part of a captured PayPal payment. [destructive]
- `update_tracking` — Update an order shipment tracker, replace its items, notify the payer, or cancel it. [destructive]
- `void_authorization` — Void a PayPal authorization that has not been fully captured. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PayPal state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PayPal is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/paypal
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- PayPal homepage: https://www.paypal.com/
- API documentation: https://developer.paypal.com/docs/api/orders/v2/
