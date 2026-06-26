---
name: oo-tomtom
description: "TomTom (developer.tomtom.com). Use this skill for ANY TomTom request — searching and reading data. Whenever a task involves TomTom, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TomTom"
  author: "OOMOL"
  version: "1.0.1"
  services: ["tomtom"]
  icon: "https://static.oomol.com/logo/third-party/Tomtom.svg"
---

# TomTom

Operate **TomTom** through your OOMOL-connected account. This skill calls the `tomtom` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TomTom. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tomtom" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tomtom" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `autocomplete` — Return autocomplete suggestions from the TomTom Search API.
- `fuzzy_search` — Search addresses or places with the TomTom Search API fuzzy search endpoint.
- `geocode` — Convert an address into geographic search results with the TomTom Geocoding API.
- `nearby_search` — Search for nearby places of interest around a coordinate with TomTom.
- `reverse_geocode` — Convert a coordinate into human-readable address candidates with the TomTom Reverse Geocoding API.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TomTom state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TomTom is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=tomtom
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- TomTom homepage: https://developer.tomtom.com
