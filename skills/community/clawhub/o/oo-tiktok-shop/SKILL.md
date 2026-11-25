---
name: oo-tiktok-shop
description: "TikTok Shop (shop.tiktok.com). Use this skill for ANY TikTok Shop request — searching and reading data. Whenever a task involves TikTok Shop, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TikTok Shop"
  author: "OOMOL"
  version: "1.0.0"
  services: ["tiktok_shop"]
  icon: "https://static.oomol.com/logo/third-party/tiktok_shop.svg"
---

# TikTok Shop

Operate **TikTok Shop** through your OOMOL-connected account. This skill calls the `tiktok_shop` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TikTok Shop. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tiktok_shop" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tiktok_shop" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_orders` — Get details of up to 50 TikTok Shop orders using API 202507, including payment, items and fulfillment information.
- `get_product` — Get a TikTok Shop product, including SKU inventory, prices and audit details. Select either the draft or under-review version when needed.
- `list_authorized_shops` — List the seller's authorized TikTok Shop stores and their shop ciphers for subsequent product and order calls.
- `search_orders` — Search TikTok Shop orders by creation or update time, status, buyer and warehouse, with cursor pagination.
- `search_products` — Search TikTok Shop products using API 202502, with status, SKU, time, audit and listing filters. Use get_product for complete details.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TikTok Shop state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TikTok Shop is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/tiktok_shop
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TikTok Shop homepage: https://shop.tiktok.com/
- API documentation: https://partner.tiktokshop.com/docv2/
