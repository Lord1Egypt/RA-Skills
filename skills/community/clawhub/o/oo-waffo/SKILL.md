---
name: oo-waffo
description: "Waffo Pancake (waffo.ai). Use this skill for ANY Waffo Pancake request — reading, creating, updating, and deleting data. Whenever a task involves Waffo Pancake, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Waffo Pancake"
  author: "OOMOL"
  version: "1.0.5"
  services: ["waffo"]
  icon: "https://static.oomol.com/logo/third-party/waffo.svg"
---

# Waffo Pancake

Operate **Waffo Pancake** through your OOMOL-connected account. This skill calls the `waffo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Waffo Pancake. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "waffo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "waffo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_subscription` — Cancel a pending Waffo subscription immediately or schedule an active subscription to end after its current period. [destructive]
- `create_checkout_session` — Create a Waffo hosted checkout session for a one-time or subscription product. [write]
- `create_one_time_product` — Create a one-time purchase product with multi-currency pricing in Waffo. [write]
- `create_refund_ticket` — Request a full or partial Waffo refund for a succeeded payment. [destructive]
- `create_store` — Create a Waffo store for the connected merchant account. [write]
- `create_subscription_product` — Create a recurring subscription product with multi-currency pricing in Waffo. [write]
- `list_products` — List one-time or subscription products in the connected Waffo API key environment.
- `list_stores` — List stores available to the connected Waffo merchant account.
- `publish_product` — Publish the active test version of a one-time or subscription product to production for the first time. [write]
- `resubmit_refund_ticket` — Revise and resubmit a rejected or failed Waffo refund ticket. [destructive]
- `run_query` — Run a read-only query against the Waffo GraphQL API for stores, products, orders, payments, refunds, customers, or analytics.
- `search_orders` — Search one-time or subscription orders by store, status, merchant reference, or creation time.
- `search_payments` — Find a Waffo payment by ID or search payments by status, merchant order reference, or creation time.
- `search_refund_tickets` — Search Waffo refund tickets by status, payment, merchant reference, or creation time.
- `set_product_status` — Activate or deactivate a one-time or subscription product in the connected Waffo API key environment. [destructive]
- `update_product` — Update a one-time or subscription product in the connected Waffo API key environment, creating an immutable version when content changes. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Waffo Pancake state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Waffo Pancake is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/waffo
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Waffo Pancake homepage: https://www.waffo.ai
- API documentation: https://docs.waffo.ai/api-reference/authentication
