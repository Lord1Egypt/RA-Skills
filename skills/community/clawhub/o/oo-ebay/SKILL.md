---
name: oo-ebay
description: "eBay (ebay.com). Use this skill for ANY eBay request — reading, creating, and updating data. Whenever a task involves eBay, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "eBay"
  author: "OOMOL"
  version: "1.0.0"
  services: ["ebay"]
  icon: "https://static.oomol.com/logo/third-party/ebay.svg"
---

# eBay

Operate **eBay** through your OOMOL-connected account. This skill calls the `ebay` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected eBay. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ebay" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ebay" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_shipping_fulfillment` — Record a shipment for an eBay order's line items. Supply the carrier and tracking number together when available. This records fulfillment; it does not purchase a shipping label. [write]
- `get_order` — Get an eBay order's line items, payment details, and shipping instructions.
- `get_shipping_fulfillment` — Get a shipping fulfillment's line items, carrier, and tracking information.
- `get_user` — Get the connected eBay account's public identity and account information.
- `list_orders` — List completed-checkout eBay orders. Without filters, eBay returns orders created in the last 90 days; orders older than two years are unavailable.
- `list_shipping_fulfillments` — List all shipping fulfillments recorded for an eBay order.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change eBay state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — eBay is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/ebay
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- eBay homepage: https://www.ebay.com
- API documentation: https://developer.ebay.com/develop/api/sell/fulfillment_api
