---
name: oo-scrapingant
description: "ScrapingAnt (scrapingant.com). Use this skill for ANY ScrapingAnt request — searching and reading data. Whenever a task involves ScrapingAnt, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ScrapingAnt"
  author: "OOMOL"
  version: "1.0.1"
  services: ["scrapingant"]
  icon: "https://static.oomol.com/logo/third-party/scrapingant.png"
---

# ScrapingAnt

Operate **ScrapingAnt** through your OOMOL-connected account. This skill calls the `scrapingant` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ScrapingAnt. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "scrapingant" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "scrapingant" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `extract_content_as_markdown` — Convert a page into Markdown through ScrapingAnt's Markdown transformation endpoint.
- `extract_data_with_ai` — Extract structured top-level JSON fields from a page through ScrapingAnt's AI extraction endpoint.
- `get_api_credits_usage` — Read the current ScrapingAnt subscription status and remaining API credits.
- `scrape_with_extended_json_output` — Scrape a page through ScrapingAnt's v2 extended endpoint and return HTML, text, cookies, headers, XHRs, and iframes.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ScrapingAnt state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ScrapingAnt is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=scrapingant
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ScrapingAnt homepage: https://scrapingant.com
