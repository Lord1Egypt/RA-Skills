---
name: oo-paddle
description: "Paddle (paddle.com). Use this skill for ANY Paddle request — reading, creating, updating, and deleting data. Whenever a task involves Paddle, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Paddle"
  author: "OOMOL"
  version: "1.0.5"
  services: ["paddle"]
  icon: "https://static.oomol.com/logo/third-party/paddle.svg"
---

# Paddle

Operate **Paddle** through your OOMOL-connected account. This skill calls the `paddle` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Paddle. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "paddle" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "paddle" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_customer` — Create a Paddle customer. [write]
- `create_price` — Create a Paddle price for a product. [write]
- `create_product` — Create a Paddle product in the catalog. [write]
- `get_customer` — Get one Paddle customer by ID.
- `get_price` — Get one Paddle price by ID.
- `get_product` — Get one Paddle product by ID.
- `list_customers` — List Paddle customers with optional email, status, search, and pagination filters.
- `list_prices` — List Paddle prices with optional product, status, recurring, and billing filters.
- `list_products` — List Paddle products with optional filtering, pagination, and price inclusion.
- `update_customer` — Update a Paddle customer, including archiving or reactivating it through status. [write]
- `update_price` — Update a Paddle price, including archiving or reactivating it through status. [destructive]
- `update_product` — Update a Paddle product, including archiving or reactivating it through status. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Paddle state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Paddle is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/paddle
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Paddle homepage: https://www.paddle.com
- API documentation: https://developer.paddle.com/api-reference/overview
