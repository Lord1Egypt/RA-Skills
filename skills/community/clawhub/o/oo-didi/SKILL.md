---
name: oo-didi
description: "DiDi (mcp.didichuxing.com). Use this skill for ANY DiDi request — reading, creating, updating, and deleting data. Whenever a task involves DiDi, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DiDi"
  author: "OOMOL"
  version: "1.0.1"
  services: ["didi"]
  icon: "https://static.oomol.com/logo/third-party/didi.png"
---

# DiDi

Operate **DiDi** through your OOMOL-connected account. This skill calls the `didi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected DiDi. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "didi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "didi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `maps_direction_bicycling` — Plan a cycling route using coordinates obtained from maps_textsearch.
- `maps_direction_driving` — Plan a driving route using coordinates obtained from maps_textsearch.
- `maps_direction_transit` — Plan a public transit route in the specified city using coordinates obtained from maps_textsearch.
- `maps_direction_walking` — Plan a walking route using coordinates obtained from maps_textsearch.
- `maps_place_around` — Search for nearby places using map-derived coordinates and an optional radius.
- `maps_regeocode` — Convert map-derived coordinates into an address.
- `maps_textsearch` — Search for places by keyword and city. Use returned coordinates for ride estimates and route planning; do not guess coordinates or the user starting location. Ask the user to choose when multiple candidates match.
- `taxi_cancel_order` — Cancel a specified ride order. Trips in progress and completed trips cannot be canceled. [destructive]
- `taxi_create_order` — Create a real ride order using an unexpired taxi_estimate traceId. Show the selected vehicle categories and estimated prices, and obtain explicit user confirmation before calling. On a transport failure, stop and do not automatically retry or switch keys; the booking outcome may be unknown. [write]
- `taxi_estimate` — Estimate available ride categories and prices. Obtain coordinates from maps_textsearch first; ask for the starting location if unknown. Use the exact user-selected category from the returned options; never silently substitute another category. The returned traceId is required for ordering and expires.
- `taxi_generate_ride_app_link` — Generate a deep link for the user to finish ordering in DiDi app version 7.1.2 or later. Obtain coordinates from maps_textsearch; this action does not place an order.
- `taxi_get_driver_location` — Get the driver’s current coordinates for an ongoing ride order.
- `taxi_query_order` — Query ride status, driver details, and progress. Omit order_id to query the current account’s unfinished order. Query once per call; do not interpret unknown status codes as completion.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DiDi state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — DiDi is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/didi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- DiDi homepage: https://mcp.didichuxing.com
- API documentation: https://mcp.didichuxing.com/api
