---
name: oo-subvisory
description: "Subvisory (subvisory.com). Use this skill for ANY Subvisory request — reading, creating, updating, and deleting data. Whenever a task involves Subvisory, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Subvisory"
  author: "OOMOL"
  version: "1.0.4"
  services: ["subvisory"]
  icon: "https://static.oomol.com/logo/third-party/subvisory.svg"
---

# Subvisory

Operate **Subvisory** through your OOMOL-connected account. This skill calls the `subvisory` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Subvisory. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "subvisory" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "subvisory" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_category` — Create a category in Subvisory. [write]
- `create_payment_method` — Create a payment method in Subvisory. [write]
- `create_subscription` — Create a subscription in Subvisory. [write]
- `delete_category` — Delete a Subvisory category. [destructive]
- `delete_payment_method` — Delete a Subvisory payment method. [destructive]
- `delete_subscription` — Delete a Subvisory subscription. [destructive]
- `get_category` — Retrieve a Subvisory category by ID.
- `get_payment_method` — Retrieve a Subvisory payment method by ID.
- `get_subscription` — Retrieve a Subvisory subscription by ID.
- `list_categories` — List all Subvisory categories.
- `list_payment_methods` — List all Subvisory payment methods.
- `list_subscriptions` — List all subscriptions from Subvisory.
- `update_category` — Update a Subvisory category. [write]
- `update_payment_method` — Update a Subvisory payment method. [write]
- `update_subscription` — Update a Subvisory subscription. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Subvisory state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Subvisory is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/subvisory
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Subvisory homepage: https://www.subvisory.com
- API documentation: https://www.subvisory.com/api/v1/docs
