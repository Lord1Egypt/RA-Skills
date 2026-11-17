---
name: oo-baidu-maps
description: "Baidu Maps (lbsyun.baidu.com). Use this skill for ANY Baidu Maps request — searching and reading data. Whenever a task involves Baidu Maps, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Baidu Maps"
  author: "OOMOL"
  version: "1.0.4"
  services: ["baidu_maps"]
  icon: "https://static.oomol.com/logo/third-party/baidu_maps.png"
---

# Baidu Maps

Operate **Baidu Maps** through your OOMOL-connected account. This skill calls the `baidu_maps` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Baidu Maps. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "baidu_maps" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "baidu_maps" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `district_search` — Query the Baidu Maps administrative division API (api_region_search).
- `geocode` — Geocode an address with Baidu Maps.
- `get_place_detail` — Look up a Baidu Maps place by its uid.
- `input_tips` — Fetch Baidu Maps input suggestions (keywordsuggestion).
- `ip_locate` — Locate an IP address with Baidu Maps.
- `reverse_geocode` — Reverse geocode coordinates with Baidu Maps.
- `route_bicycling` — Plan a Baidu Maps bicycling route.
- `route_driving` — Plan a Baidu Maps driving route.
- `route_transit` — Plan a Baidu Maps transit route.
- `route_walking` — Plan a Baidu Maps walking route.
- `search_places` — Search Baidu Maps places in a region or city.
- `search_places_around` — Search Baidu Maps places within a radius around a coordinate.
- `search_places_polygon` — Search Baidu Maps places inside a polygon (rectangle).
- `weather` — Fetch weather observations and forecasts for a coordinate.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Baidu Maps state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Baidu Maps is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/baidu_maps
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Baidu Maps homepage: https://lbsyun.baidu.com
- API documentation: https://lbsyun.baidu.com/docs/webapi?title=placev3%2Fguide%2Fwebservice-placeapiV3%2FinterfaceDocumentV2
