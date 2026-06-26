---
name: oo-webscraper-io
description: "WebScraper.io (webscraper.io). Use this skill for ANY WebScraper.io request — reading, creating, updating, and deleting data. Whenever a task involves WebScraper.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WebScraper.io"
  author: "OOMOL"
  version: "1.0.1"
  services: ["webscraper_io"]
  icon: "https://static.oomol.com/logo/third-party/webscraper_io.svg"
---

# WebScraper.io

Operate **WebScraper.io** through your OOMOL-connected account. This skill calls the `webscraper_io` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WebScraper.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "webscraper_io" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "webscraper_io" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_scraping_job` — Create a Web Scraper Cloud scraping job for one sitemap. [write]
- `create_sitemap` — Create a new Web Scraper Cloud sitemap from a sitemap JSON document. [write]
- `delete_scraping_job` — Delete a Web Scraper Cloud scraping job by numeric scraping job ID. [destructive]
- `delete_sitemap` — Delete a Web Scraper Cloud sitemap by numeric sitemap ID. [destructive]
- `download_scraping_job_json` — Download one Web Scraper Cloud scraping job result in JSON Lines format.
- `get_account_info` — Get the current Web Scraper Cloud account profile for the connected API token.
- `get_scraping_job` — Get one Web Scraper Cloud scraping job by numeric scraping job ID.
- `get_sitemap` — Get one Web Scraper Cloud sitemap by numeric sitemap ID.
- `list_scraping_jobs` — List Web Scraper Cloud scraping jobs with optional page, sitemap, and tag filters.
- `list_sitemaps` — List Web Scraper Cloud sitemaps with optional page and tag filters.
- `update_sitemap` — Update an existing Web Scraper Cloud sitemap by numeric sitemap ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WebScraper.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WebScraper.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=webscraper_io
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- WebScraper.io homepage: https://webscraper.io/
