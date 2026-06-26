---
name: oo-firecrawl
description: "Firecrawl (firecrawl.dev). Use this skill for ANY Firecrawl request — reading, creating, updating, and deleting data. Whenever a task involves Firecrawl, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Firecrawl"
  author: "OOMOL"
  version: "1.0.1"
  services: ["firecrawl"]
  icon: "https://static.oomol.com/logo/third-party/Firecrawl.svg"
---

# Firecrawl

Operate **Firecrawl** through your OOMOL-connected account. This skill calls the `firecrawl` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Firecrawl. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "firecrawl" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "firecrawl" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `agent_cancel` — Cancel a running Firecrawl agent job by job ID. [write]
- `batch_scrape` — Start a Firecrawl batch scrape job for multiple URLs and return the async job ID.
- `batch_scrape_cancel` — Cancel a running Firecrawl batch scrape job by job ID. [write]
- `batch_scrape_get` — Get the current status and paged results of a Firecrawl batch scrape job by job ID.
- `batch_scrape_get_errors` — Get the failed URLs and robots.txt blocks from a Firecrawl batch scrape job.
- `crawl` — Start a Firecrawl crawl job with compatibility fields accepted from the Composio crawl action.
- `crawl_cancel` — Cancel a running Firecrawl crawl job by job ID. [write]
- `crawl_delete` — Compatibility alias of crawl_cancel for the Composio FIRECRAWL_CRAWL_DELETE action. [destructive]
- `crawl_get` — Get the current status and paged results of a Firecrawl crawl job by job ID.
- `crawl_get_errors` — Get the failed URLs and robots.txt blocks from a Firecrawl crawl job.
- `crawl_list_active` — List the currently active Firecrawl crawl jobs for the authenticated team.
- `crawl_params_preview` — Preview the crawl parameters that Firecrawl would infer from a URL and prompt before starting the crawl.
- `crawl_v2` — Start a Firecrawl crawl job with the official v2 crawl fields, including prompt-driven options generation.
- `credit_usage_get` — Get the authenticated Firecrawl team's current credit usage summary.
- `credit_usage_get_historical` — Get the authenticated Firecrawl team's historical credit usage summary.
- `deep_research` — Start a Firecrawl deep research job. This endpoint remains alpha and Firecrawl currently documents it outside the main v2 endpoint set.
- `extract` — Start a Firecrawl extract job that returns structured data for one or more URLs.
- `extract_get` — Get the current status and output of a Firecrawl extract job by job ID.
- `get_agent_status` — Get the current status and output of a Firecrawl agent job by job ID.
- `get_deep_research_status` — Get the current status and output of a Firecrawl deep research job by job ID.
- `get_the_status_of_a_crawl_job` — Compatibility alias of crawl_get for the Composio FIRECRAWL_GET_THE_STATUS_OF_A_CRAWL_JOB action.
- `llms_txt_generate` — Start an LLMs.txt generation job for a website. This endpoint remains outside the main v2 endpoint set in Firecrawl's docs.
- `llms_txt_get` — Get the current status and generated content of an LLMs.txt job by job ID.
- `map_multiple_urls_based_on_options` — Discover URLs from a website with Firecrawl's map endpoint using the Composio-compatible action name.
- `queue_get` — Get the authenticated Firecrawl team's queue status and concurrency information.
- `scrape` — Scrape a single URL with Firecrawl and return the extracted page content in the requested formats.
- `search` — Search the web with Firecrawl and optionally scrape the top results in the requested formats.
- `start_agent` — Start a Firecrawl agent job for multi-page autonomous browsing and extraction. [write]
- `token_usage_get` — Get the authenticated Firecrawl team's current token usage summary.
- `token_usage_get_historical` — Get the authenticated Firecrawl team's historical token usage summary.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Firecrawl state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Firecrawl is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=firecrawl
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Firecrawl homepage: https://www.firecrawl.dev
