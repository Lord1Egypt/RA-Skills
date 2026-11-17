---
name: oo-akta
description: "Akta (akta.pro). Use this skill for ANY Akta request — reading, creating, and updating data. Whenever a task involves Akta, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Akta"
  author: "OOMOL"
  version: "1.0.2"
  services: ["akta"]
  icon: "https://static.oomol.com/logo/third-party/akta.png"
---

# Akta

Operate **Akta** through your OOMOL-connected account. This skill calls the `akta` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Akta. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "akta" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "akta" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_company` — Submit a missing company for addition, or return the existing company. Use the returned handle with get_addition_result to wait for completion. [write]
- `build_filters` — Convert a natural language company description into structured list filters.
- `enrich_company` — Enrich a company with any of the 16 data sections; funding and M&A sections require a subscription or Enterprise plan.
- `generate_company_list` — Generate a company list using a natural language query or structured filters, with optional enrichment.
- `get_addition_result` — Wait for company addition using the submission handle; existing companies complete immediately.
- `get_employee_reviews` — Read employee ratings and paginated reviews for a company.
- `get_headcount_trends` — Read company employee counts, growth history and functional breakdowns.
- `get_job_posts` — Read paginated live company job listings.
- `get_product_reviews` — List company products and retrieve reviews for selected product IDs.
- `get_request_status` — Read an asynchronous request by its request ID.
- `get_social_posts` — Read paginated company social posts and engagement data.
- `get_website_traffic` — Read company website engagement, traffic history and acquisition channels.
- `search_companies` — Resolve a company name, website or UUID into matching companies.
- `search_industries` — Resolve an industry topic into ranked taxonomy codes.
- `search_news` — Search company, industry and topic news with entity, date, taxonomy and sentiment filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Akta state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Akta is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/akta
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Akta homepage: https://akta.pro
- API documentation: https://docs.akta.pro/getting-started/overview
