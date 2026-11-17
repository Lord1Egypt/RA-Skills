---
name: oo-luckin-coffee
description: "Luckin Coffee (open.lkcoffee.com). Use this skill for ANY Luckin Coffee request — reading, creating, updating, and deleting data. Whenever a task involves Luckin Coffee, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Luckin Coffee"
  author: "OOMOL"
  version: "1.0.5"
  services: ["luckin_coffee"]
  icon: "https://static.oomol.com/logo/third-party/luckin_coffee.svg"
---

# Luckin Coffee

Operate **Luckin Coffee** through your OOMOL-connected account. This skill calls the `luckin_coffee` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Luckin Coffee. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "luckin_coffee" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "luckin_coffee" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancelOrder` — Cancel a Luckin Coffee order. This changes a real order and may be irreversible; confirm the exact order with the user first. [destructive]
- `createOrder` — Create a real Luckin Coffee order that may require payment. Preview the order first and obtain the user's confirmation before calling this action. [write]
- `previewOrder` — Preview a Luckin Coffee order, including prices and available coupons, without creating it.
- `queryOrderDetailInfo` — Get the current status, pickup details, products, payment, and delivery information for an order.
- `queryProductDetailInfo` — Get the current details, attributes, SKU, and price for one Luckin Coffee product at a store.
- `queryShopList` — Find nearby Luckin Coffee stores using a location and optional store name.
- `searchProductForMcp` — Search and recommend Luckin Coffee products at a specific store from the user's original request.
- `switchProduct` — Change a selectable attribute on a Luckin Coffee product and return the updated SKU and price.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Luckin Coffee state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Luckin Coffee is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/luckin_coffee
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Luckin Coffee homepage: https://open.lkcoffee.com/mcp
- API documentation: https://open.lkcoffee.com/mcp
