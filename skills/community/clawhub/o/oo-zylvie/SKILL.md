---
name: oo-zylvie
description: "Zylvie (zylvie.com). Use this skill for ANY Zylvie request — reading, creating, updating, and deleting data. Whenever a task involves Zylvie, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Zylvie"
  author: "OOMOL"
  version: "1.0.5"
  services: ["zylvie"]
  icon: "https://static.oomol.com/logo/third-party/zylvie.svg"
---

# Zylvie

Operate **Zylvie** through your OOMOL-connected account. This skill calls the `zylvie` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Zylvie. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zylvie" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zylvie" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_coupon` — Create a coupon in Zylvie. [write]
- `create_product` — Create a product in Zylvie. [write]
- `delete_coupon` — Delete a Zylvie coupon, or archive it when transaction history requires it. [destructive]
- `delete_product` — Delete a Zylvie product, or archive it when transaction history requires it. [destructive]
- `get_current_user` — Get the Zylvie user and brand authenticated by the current API key.
- `list_coupons` — List active or archived coupons for the authenticated Zylvie brand.
- `redeem_license_key` — Mark a Zylvie license key as redeemed. [write]
- `refund_license_key` — Mark a Zylvie license key as refunded. [destructive]
- `update_coupon` — Update selected fields on an existing Zylvie coupon. [write]
- `update_product` — Update selected fields on an existing Zylvie product. [write]
- `verify_license_key` — Verify that a Zylvie license key is valid for a product.
- `verify_subscriptions` — List Zylvie subscriptions associated with a subscriber email address.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Zylvie state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Zylvie is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/zylvie
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Zylvie homepage: https://zylvie.com/
- API documentation: https://developers.zylvie.com/
