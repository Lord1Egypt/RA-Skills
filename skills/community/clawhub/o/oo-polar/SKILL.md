---
name: oo-polar
description: "Polar (polar.sh). Use this skill for ANY Polar request — searching and reading data. Whenever a task involves Polar, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Polar"
  author: "OOMOL"
  version: "1.0.5"
  services: ["polar"]
  icon: "https://static.oomol.com/logo/third-party/polar.svg"
---

# Polar

Operate **Polar** through your OOMOL-connected account. This skill calls the `polar` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Polar. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "polar" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "polar" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_customer` — Get a Polar customer by ID.
- `get_customer_by_external_id` — Get a Polar customer by external ID.
- `get_customer_state` — Get a Polar customer state by customer ID, including subscriptions and benefits.
- `get_customer_state_by_external_id` — Get a Polar customer state by external customer ID, including subscriptions and benefits.
- `get_order` — Get a Polar order by ID.
- `get_organization` — Get a Polar organization by ID.
- `get_product` — Get a Polar product by ID.
- `get_subscription` — Get a Polar subscription by ID.
- `list_customers` — List Polar customers with optional organization, email, search, activity, and metadata filters.
- `list_orders` — List Polar orders with optional organization, product, customer, checkout, subscription, and metadata filters.
- `list_organizations` — List Polar organizations accessible to the Organization Access Token.
- `list_products` — List Polar products with optional organization, name, visibility, and metadata filters.
- `list_subscriptions` — List Polar subscriptions with optional organization, product, customer, status, cancellation, and metadata filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Polar state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Polar is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/polar
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Polar homepage: https://polar.sh
- API documentation: https://polar.sh/docs/api-reference/introduction
