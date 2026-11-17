---
name: oo-wp-maps
description: "WP Maps (wpmaps.com). Use this skill for ANY WP Maps request — reading, creating, updating, and deleting data. Whenever a task involves WP Maps, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WP Maps"
  author: "OOMOL"
  version: "1.0.4"
  services: ["wp_maps"]
  icon: "https://static.oomol.com/logo/third-party/wp_maps.svg"
---

# WP Maps

Operate **WP Maps** through your OOMOL-connected account. This skill calls the `wp_maps` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WP Maps. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wp_maps" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wp_maps" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_products` — Create one or more products in WP Maps. [write]
- `create_stores` — Create one or more stores in WP Maps. [write]
- `delete_products` — Delete one or more WP Maps products by ID. [destructive]
- `delete_stores` — Delete one or more WP Maps stores by ID. [destructive]
- `get_product` — Get one WP Maps product by ID.
- `get_store` — Get one WP Maps store by ID.
- `list_products` — List all products in the connected WP Maps account.
- `list_stores` — List all stores in the connected WP Maps account.
- `update_products` — Update one or more existing products in WP Maps. [write]
- `update_stores` — Update one or more existing stores in WP Maps. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WP Maps state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WP Maps is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/wp_maps
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WP Maps homepage: https://wpmaps.com/
- API documentation: https://wpmaps.com/help/wp-maps-api-your-guide-to-integration-and-functionality/
