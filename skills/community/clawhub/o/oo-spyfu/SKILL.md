---
name: oo-spyfu
description: "SpyFu (spyfu.com). Use this skill for ANY SpyFu request — searching and reading data. Whenever a task involves SpyFu, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SpyFu"
  author: "OOMOL"
  version: "1.0.4"
  services: ["spyfu"]
  icon: "https://static.oomol.com/logo/third-party/spyfu.svg"
---

# SpyFu

Operate **SpyFu** through your OOMOL-connected account. This skill calls the `spyfu` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SpyFu. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "spyfu" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "spyfu" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `find_matching_domains` — Discover domains matching a wildcard pattern and optional traffic, budget, rank, or strength criteria.
- `get_bulk_domain_stats` — Retrieve current or historical SEO and PPC statistics for multiple domains.
- `get_competing_keywords` — Find SEO or PPC keywords shared by selected domains with optional exclusions.
- `get_competitors` — Retrieve a domain's top SEO, PPC, or combined search competitors.
- `get_domain_ad_history` — Retrieve historical advertising copy and keywords for a domain.
- `get_domain_keyword_rankings` — Compare one domain's historical organic rankings across selected keywords.
- `get_domain_ranking_history` — Retrieve historical keyword ranks and aggregate click changes for a domain across a month range.
- `get_keyword_ad_history` — Retrieve historical advertisers and ad copy for a keyword.
- `get_keyword_ad_history_with_stats` — Retrieve keyword ad history enriched with advertiser budgets, coverage, and top-ad statistics.
- `get_keyword_domain_rankings` — Compare one keyword's historical organic rankings across multiple domains.
- `get_keyword_expansions` — Expand a seed keyword into related, question, transactional, co-ranking, or co-advertised terms.
- `get_keyword_information` — Retrieve search, difficulty, click, cost, and intent metrics for exact keywords.
- `get_latest_domain_stats` — Retrieve the latest SEO and PPC statistics for a domain.
- `get_live_seo_stats` — Retrieve live aggregate organic visibility, click, value, and search-volume metrics for a domain or URL.
- `get_monthly_usage` — Retrieve SpyFu API usage and cost totals for one calendar month.
- `get_ppc_keywords` — Retrieve current ads, most successful paid keywords, or newly acquired paid keywords for a domain.
- `get_seo_keywords` — Retrieve SEO keywords for a domain by value, ranking change, click change, or page-one movement.
- `get_serp_analysis` — Analyze the current organic search result landscape for a keyword, including ranks and competing pages.
- `get_top_pages` — Retrieve a domain's highest-traffic or newly successful organic pages and their top keywords.
- `get_usage_breakdown` — Retrieve SpyFu API usage broken down by day or API method for one month.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SpyFu state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SpyFu is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/spyfu
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SpyFu homepage: https://www.spyfu.com/
- API documentation: https://developer.spyfu.com/docs/api-pricing
