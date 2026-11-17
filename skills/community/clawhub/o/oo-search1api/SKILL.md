---
name: oo-search1api
description: "Search1API (s1.dev). Use this skill for ANY Search1API request — reading, creating, and updating data. Whenever a task involves Search1API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Search1API"
  author: "OOMOL"
  version: "1.0.2"
  services: ["search1api"]
  icon: "https://static.oomol.com/logo/third-party/search1api.svg"
---

# Search1API

Operate **Search1API** through your OOMOL-connected account. This skill calls the `search1api` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Search1API. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "search1api" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "search1api" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ask` — Select search engines and rank relevant sources from a natural-language query. Returns sources, not a generated answer; partial engine failures are preserved.
- `crawl` — Read a public webpage as clean content, with optional fallback retrieval.
- `crawl_batch` — Read multiple public webpages in one batch, preserving individual results and failures.
- `deepcrawl` — Start an asynchronous whole-site crawl. Use get_deepcrawl to wait for the archive download URL. This upstream API is in beta. [write]
- `extract` — Extract structured data from a webpage using a prompt and response schema. This upstream API is in beta.
- `feedback` — Submit product feedback. Do not include credentials, personal data or private content; do not automatically repeat the same report. [write]
- `get_deepcrawl` — Read the state and archive download URL of a deepcrawl task.
- `health` — Check public API health. This does not validate credentials.
- `news` — Search recent news with source, site, language, time, image and full-content options.
- `news_batch` — Run multiple news searches in one batch, preserving each success, failure and credit cost.
- `screenshot` — Capture a public webpage or element as PNG, JPEG or WebP and return a temporary file URL.
- `search` — Search the web with engine, site, language, time, pagination, image and full-content options.
- `search_batch` — Run multiple web searches in one batch, preserving each success, failure and credit cost.
- `sitemap` — Discover page URLs from a site's sitemap or all available links.
- `trending` — Retrieve trending topics from the requested source.
- `usage` — Read the authenticated account's remaining credits without consuming credits.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Search1API state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Search1API is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/connections/search1api
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Search1API homepage: https://s1.dev
- API documentation: https://s1.dev/docs
