---
name: oo-kuaidi100
description: "Kuaidi100 (kuaidi100.com). Use this skill for ANY Kuaidi100 request — reading, creating, updating, and deleting data. Whenever a task involves Kuaidi100, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Kuaidi100"
  author: "OOMOL"
  version: "1.0.6"
  services: ["kuaidi100"]
  icon: "https://static.oomol.com/logo/third-party/kuaidi100.png"
---

# Kuaidi100

Operate **Kuaidi100** through your OOMOL-connected account. This skill calls the `kuaidi100` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Kuaidi100. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "kuaidi100" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "kuaidi100" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `auto_number` — Detect the likely express carriers for a tracking number from its format.
- `cancel_order` — Cancel a pickup order that is no longer needed. [destructive]
- `create_order` — Create a pay-offline pickup order after obtaining an order_price quote. [write]
- `estimate_price` — Estimate the shipping price for a carrier, sender and recipient addresses, and parcel weight.
- `estimate_time` — Estimate the delivery time for a shipment before it is sent, from the carrier, origin, destination, and optional order time and product type.
- `estimate_time_with_logistic` — Estimate the remaining delivery time for an in-transit shipment from its existing logistics trajectory, usually the data returned by kuaidi100.query_trace.
- `order_price` — Quote a pickup order before creating it. This uses the pickup-order pricing service, not the general estimate_price calculation.
- `query_order` — Get a pickup order and optionally include its logistics trajectory.
- `query_trace` — Query the real-time logistics trajectory for an express tracking number. The carrier is detected automatically.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Kuaidi100 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Kuaidi100 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/kuaidi100
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Kuaidi100 homepage: https://www.kuaidi100.com/
- API documentation: https://api.kuaidi100.com/document/how-to-use-mcp-service
