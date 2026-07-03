---
name: oo-customerio
description: "Customer.io (customer.io). Use this skill for ANY Customer.io request — reading, creating, updating, and deleting data. Whenever a task involves Customer.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Customer.io"
  author: "OOMOL"
  version: "1.0.0"
  services: ["customerio"]
  icon: "https://static.oomol.com/logo/third-party/customerio.svg"
---

# Customer.io

Operate **Customer.io** through your OOMOL-connected account. This skill calls the `customerio` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Customer.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "customerio" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "customerio" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_customer` — Delete a Customer.io person and their information through the Track API. [destructive]
- `identify_customer` — Add or update a Customer.io person through the Track API.
- `merge_customers` — Merge two Customer.io people, keeping the primary profile and deleting the secondary profile. [write]
- `suppress_customer` — Delete and suppress a Customer.io person identifier so it cannot be re-added until unsuppressed.
- `track_anonymous_event` — Track an event for an anonymous person in Customer.io.
- `track_customer_event` — Track an event associated with an identified Customer.io person.
- `unsuppress_customer` — Unsuppress a Customer.io person identifier so a new profile can be created later.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Customer.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Customer.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=customerio
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Customer.io homepage: https://customer.io/
