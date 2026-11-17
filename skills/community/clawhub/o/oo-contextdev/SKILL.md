---
name: oo-contextdev
description: "Context.dev (context.dev). Use this skill for ANY Context.dev request — reading, creating, updating, and deleting data. Whenever a task involves Context.dev, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Context.dev"
  author: "OOMOL"
  version: "1.0.2"
  services: ["contextdev"]
  icon: "https://static.oomol.com/logo/third-party/contextdev.svg"
---

# Context.dev

Operate **Context.dev** through your OOMOL-connected account. This skill calls the `contextdev` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Context.dev. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "contextdev" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "contextdev" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `answer_research` — Answer a research task.
- `cancel_batch` — Cancel a batch. [destructive]
- `classify_naics` — Classify NAICS codes.
- `classify_sic` — Classify SIC codes.
- `crawl_website` — Crawl a website. [destructive]
- `create_monitor` — Create a monitor. [destructive]
- `delete_batch` — Delete a batch. [destructive]
- `delete_monitor` — Delete a monitor. [destructive]
- `enrich_person` — Enrich a person.
- `extract_data` — Extract structured data. [destructive]
- `extract_fonts` — Extract fonts.
- `extract_styleguide` — Extract a styleguide.
- `get_batch` — Retrieve a batch.
- `get_batch_results` — List batch results.
- `get_change` — Retrieve a monitor change.
- `get_log` — Retrieve a request log.
- `get_monitor` — Retrieve a monitor.
- `get_monitor_limits` — Retrieve monitor limits.
- `get_monitor_run` — Retrieve a monitor run.
- `get_usage` — Retrieve credit usage.
- `get_usage_history` — Retrieve usage history.
- `get_webhook_delivery` — Retrieve a webhook delivery.
- `list_account_runs` — List runs for all monitors.
- `list_batches` — List batches.
- `list_changes` — List changes for all monitors.
- `list_logs` — List request logs.
- `list_monitor_changes` — List monitor changes.
- `list_monitor_credit_usage` — Retrieve monitor credit usage.
- `list_monitor_runs` — List monitor runs.
- `list_monitors` — List monitors.
- `list_profiles` — List browser profiles.
- `list_webhook_deliveries` — List webhook deliveries.
- `list_webhook_delivery_attempts` — List webhook delivery attempts.
- `map_urls` — Map URLs.
- `parse_file` — Parse a file.
- `prefetch_brand` — Prefetch brand data. [write]
- `retrieve_brand` — Retrieve a brand.
- `retry_webhook_delivery` — Retry a webhook delivery. [write]
- `rotate_monitor_webhook_secret` — Rotate a monitor webhook secret. [destructive]
- `run_monitor_now` — Run a monitor now. [destructive]
- `scrape_web` — Scrape Anything. [destructive]
- `search_brands` — Auto-complete Brand.
- `search_companies` — Search companies.
- `search_news` — Search news.
- `search_web` — Search the web.
- `submit_batch` — Submit a batch. [destructive]
- `submit_feedback` — Submit agent feedback. [write]
- `update_monitor` — Update a monitor. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Context.dev state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Context.dev is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/contextdev
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Context.dev homepage: https://context.dev
- API documentation: https://docs.context.dev/quickstart
