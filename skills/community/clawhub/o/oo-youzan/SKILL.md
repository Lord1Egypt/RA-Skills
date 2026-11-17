---
name: oo-youzan
description: "Youzan (youzan.com). Use this skill for ANY Youzan request — searching and reading data. Whenever a task involves Youzan, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Youzan"
  author: "OOMOL"
  version: "1.0.5"
  services: ["youzan"]
  icon: "https://static.oomol.com/logo/third-party/youzan.png"
---

# Youzan

Operate **Youzan** through your OOMOL-connected account. This skill calls the `youzan` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Youzan. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "youzan" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "youzan" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_item` — Get a Youzan item by its item ID.
- `get_order` — Get a Youzan order by its order ID.
- `get_order_logistics` — Get all express or local-delivery packages and tracking details for a Youzan order.
- `get_refund` — Get a Youzan refund or after-sale record by its refund ID.
- `get_shop` — Get the identity and basic profile of the connected Youzan shop.
- `list_inventory_items` — List shelved or sold-out items from a Youzan store inventory.
- `list_onsale_items` — List items currently visible for sale in a Youzan online or physical store.
- `list_orders` — List Youzan orders using status, time, item, delivery, and text filters.
- `list_refunds` — List Youzan refund and after-sale records using order, status, and time filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Youzan state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Youzan is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/youzan
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Youzan homepage: https://www.youzan.com/
- API documentation: https://doc.youzanyun.com/v2/doc/kdt_id
