---
name: oo-stripe
description: "Stripe (stripe.com). Use this skill for ANY Stripe request — reading, creating, updating, and deleting data. Whenever a task involves Stripe, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Stripe"
  author: "OOMOL"
  version: "1.0.2"
  services: ["stripe"]
  icon: "https://static.oomol.com/logo/third-party/stripe.svg"
---

# Stripe

Operate **Stripe** through your OOMOL-connected account. This skill calls the `stripe` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Stripe. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "stripe" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "stripe" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_customer` — Create a Stripe customer with common profile and metadata fields. [write]
- `create_price` — Create a Stripe one-time or recurring price for an existing or inline product. [write]
- `create_product` — Create a Stripe product with common catalog fields. [write]
- `delete_customer` — Delete a Stripe customer by ID. [destructive]
- `delete_product` — Delete a Stripe product by ID. [destructive]
- `get_customer` — Retrieve a Stripe customer by ID.
- `get_price` — Retrieve a Stripe price by ID.
- `get_product` — Retrieve a Stripe product by ID.
- `identify_account` — Retrieve the Stripe account associated with the current secret API key.
- `list_customers` — List Stripe customers with optional email, created timestamp, and cursor filters.
- `list_prices` — List Stripe prices with optional product, active, type, and cursor filters.
- `list_products` — List Stripe products with optional active and cursor filters.
- `search_customers` — Search Stripe customers with Stripe's search query syntax.
- `search_prices` — Search Stripe prices with Stripe's search query syntax.
- `search_products` — Search Stripe products with Stripe's search query syntax.
- `update_customer` — Update a Stripe customer with common profile and metadata fields. [write]
- `update_price` — Update mutable fields on a Stripe price. [write]
- `update_product` — Update a Stripe product with common catalog fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Stripe state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Stripe is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=stripe
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Stripe homepage: https://stripe.com
