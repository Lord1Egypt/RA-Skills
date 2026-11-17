---
name: oo-apple-maps
description: "Apple Maps (developer.apple.com). Use this skill for ANY Apple Maps request — searching and reading data. Whenever a task involves Apple Maps, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Apple Maps"
  author: "OOMOL"
  version: "1.0.2"
  services: ["apple_maps"]
  icon: "https://static.oomol.com/logo/third-party/apple_maps.png"
---

# Apple Maps

Operate **Apple Maps** through your OOMOL-connected account. This skill calls the `apple_maps` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Apple Maps. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "apple_maps" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "apple_maps" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `autocomplete_search` — Get autocomplete suggestions for partial search text, such as a place name or address a user is still typing, with the same category, country, result type and location filters as search_places. Each suggestion carries display lines and, when available, a coordinate and structured address. Its completionUrl is a relative /v1/search URL that can be requested through the generic proxy to fetch the full place details.
- `geocode_address` — Convert an address into coordinates with Apple Maps. Returns the places Apple matched to the address with their coordinate, map region and structured address. Pass limitToCountries, searchLocation, searchRegion or userLocation to steer an ambiguous address toward the right area.
- `get_alternate_place_ids` — Get the alternate Place IDs of one or more Apple Maps Place IDs. IDs Apple cannot resolve are listed in errors instead of failing the whole call.
- `get_directions` — Get driving, walking or cycling directions between two places with Apple Maps. Returns the routes with their distance, duration and toll information, and the steps they reference by index. Step paths, the polyline of every step, can be large, so they are only returned when includeStepPaths is true.
- `get_etas` — Estimate the travel time and distance from one origin to up to 10 destinations with Apple Maps, by car, public transit, on foot or by bicycle.
- `get_place` — Get one place by its Apple Maps Place ID.
- `get_places` — Get several places at once by their Apple Maps Place IDs. IDs Apple cannot resolve are listed in errors instead of failing the whole call.
- `reverse_geocode` — Convert a latitude and longitude into the addresses at that point with Apple Maps.
- `search_places` — Search Apple Maps for places and points of interest by name, address or category. Filter by point of interest category, address category, result type and country, bias the search with a location or region, and page through large result sets with enablePagination and pageToken.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Apple Maps state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Apple Maps is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/apple_maps
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Apple Maps homepage: https://developer.apple.com/maps/
- API documentation: https://developer.apple.com/documentation/applemapsserverapi
