---
name: oo-autom
description: "Autom (autom.dev). Use this skill for ANY Autom request — searching and reading data. Whenever a task involves Autom, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Autom"
  author: "OOMOL"
  version: "1.0.6"
  services: ["autom"]
  icon: "https://static.oomol.com/logo/third-party/autom.svg"
---

# Autom

Operate **Autom** through your OOMOL-connected account. This skill calls the `autom` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Autom. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "autom" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "autom" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `bing_search` — Search Bing and get organic results with their position, title, link and snippet.
- `brave_search` — Search Brave's web index and get organic results with their position, title, link and snippet.
- `duckduckgo_search` — Search DuckDuckGo and get organic results with their position, title, link and snippet.
- `find_google_countries` — Search supported Google countries in Autom and return matching country codes.
- `find_google_languages` — Search supported Google languages in Autom and return matching language codes.
- `find_google_locations` — Search supported Google locations in Autom and return matching location IDs.
- `get_usage` — Get current Autom credit usage, subscription quota, rate limits, account metadata, and API key metadata.
- `google_autocomplete` — Get the Google Search autocomplete suggestions for a partial query.
- `google_maps` — Search Google Maps and get places with address, website, phone number and coordinates.
- `google_news` — Search Google News and get articles with title, source, date, link and snippet.
- `google_search` — Search Google and get organic results with their position, title, link and snippet, the knowledge graph and the estimated total.
- `google_search_light` — Search Google and get only the organic results, the fastest and cheapest Google search.
- `yahoo_search` — Search Yahoo and get organic results with their position, title, link and snippet.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Autom state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Autom is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/autom
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Autom homepage: https://www.autom.dev
- API documentation: https://docs.autom.dev/usage
