---
name: oo-google-search-console
description: "Google Search Console (search.google.com). Use this skill for ANY Google Search Console request — reading, creating, updating, and deleting data. Whenever a task involves Google Search Console, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Google Search Console"
  author: "OOMOL"
  version: "1.0.1"
  services: ["google_search_console"]
  icon: "https://static.oomol.com/logo/third-party/google_search_console.svg"
---

# Google Search Console

Operate **Google Search Console** through your OOMOL-connected account. This skill calls the `google_search_console` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Google Search Console. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "google_search_console" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "google_search_console" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_site` — Add a property to the connected account's Search Console site set. [write]
- `delete_site` — Remove a property from the connected account's Search Console site set. [destructive]
- `delete_sitemap` — Delete a sitemap from a Search Console property. [destructive]
- `get_site` — Fetch one Search Console property and the current account permission level.
- `get_sitemap` — Fetch one Search Console sitemap by property URL and sitemap URL.
- `inspect_url` — Inspect the indexed status of a URL under a Search Console property using Google's URL Inspection API.
- `list_sitemaps` — List sitemaps submitted for a Search Console property.
- `list_sites` — List Search Console properties visible to the connected Google account.
- `query_search_analytics` — Query Search Console performance data for a property across dates, dimensions, filters, and search types.
- `submit_sitemap` — Submit a sitemap URL for a Search Console property. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Google Search Console state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Google Search Console is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=google_search_console
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Google Search Console homepage: https://search.google.com/search-console
