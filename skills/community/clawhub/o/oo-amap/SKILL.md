---
name: oo-amap
description: "AMap (amap.com). Use this skill for ANY AMap request — searching and reading data. Whenever a task involves AMap, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AMap"
  author: "OOMOL"
  version: "1.0.1"
  services: ["amap"]
  icon: "https://static.oomol.com/logo/third-party/amap.svg"
---

# AMap

Operate **AMap** through your OOMOL-connected account. This skill calls the `amap` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AMap. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "amap" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "amap" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `district_search` — Search administrative districts.
- `geocode` — Convert an address to coordinates.
- `get_place_detail` — Get place details by id.
- `input_tips` — Get input tips by keywords.
- `ip_locate` — Locate by IP address.
- `reverse_geocode` — Convert coordinates to an address.
- `route_bicycling` — Plan a bicycling route.
- `route_driving` — Plan a driving route.
- `route_electrobike` — Plan an electric bike route.
- `route_transit` — Plan a transit route.
- `route_walking` — Plan a walking route.
- `search_places` — Search places by keyword.
- `search_places_around` — Search places around a location.
- `search_places_polygon` — Search places inside a polygon.
- `weather` — Get weather information.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AMap state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AMap is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=amap
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- AMap homepage: https://www.amap.com
