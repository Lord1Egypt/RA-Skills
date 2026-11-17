---
name: oo-gift-up
description: "Gift Up (giftup.com). Use this skill for ANY Gift Up request — reading, creating, updating, and deleting data. Whenever a task involves Gift Up, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gift Up"
  author: "OOMOL"
  version: "1.0.6"
  services: ["gift_up"]
  icon: "https://static.oomol.com/logo/third-party/gift_up.png"
---

# Gift Up

Operate **Gift Up** through your OOMOL-connected account. This skill calls the `gift_up` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gift Up. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gift_up" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gift_up" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_company` — Get the Gift Up company associated with the API key.
- `get_gift_card` — Get one Gift Up gift card by code.
- `get_item` — Get one Gift Up item by ID.
- `get_order` — Get one Gift Up order by ID or order number.
- `get_report_transaction` — Get one Gift Up report transaction by ID.
- `list_gift_cards` — List Gift Up gift cards with optional filters.
- `list_items` — List Gift Up items, optionally filtered by item group.
- `list_locations` — List Gift Up account locations.
- `list_orders` — List Gift Up orders with optional filters.
- `list_promotions` — List Gift Up promotions.
- `list_report_transactions` — List Gift Up report transactions with optional filters.
- `reactivate_gift_card` — Reactivate a voided Gift Up gift card. [write]
- `redeem_gift_card` — Redeem a currency amount or units from a Gift Up gift card. [destructive]
- `redeem_gift_card_in_full` — Redeem all remaining balance from a Gift Up gift card. [destructive]
- `top_up_gift_card` — Add currency amount or units to a Gift Up gift card. [write]
- `undo_gift_card_redemption` — Undo a previous Gift Up gift card redemption transaction. [write]
- `void_gift_card` — Void a Gift Up gift card so it can no longer be redeemed. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gift Up state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gift Up is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gift_up
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gift Up homepage: https://www.giftup.com/
- API documentation: https://developer.giftup.com/api#authentication
