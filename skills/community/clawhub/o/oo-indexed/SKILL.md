---
name: oo-indexed
description: "Indexed (indexed.vc). Use this skill for ANY Indexed request — searching and reading data. Whenever a task involves Indexed, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Indexed"
  author: "OOMOL"
  version: "1.0.2"
  services: ["indexed"]
  icon: "https://static.oomol.com/logo/third-party/indexed.svg"
---

# Indexed

Operate **Indexed** through your OOMOL-connected account. This skill calls the `indexed` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Indexed. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "indexed" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "indexed" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_company` — Fetch one company profile by slug. Cost depends on depth: slim is 1 credit (identity fields), standard is 2 credits (all scalar fields, owners and subsidiaries), full is 3 credits (adds funding rounds with investors, valuations, technologies and app stack). Fetching the same company at the same depth again within 12 months is not charged. A 402 means credits are exhausted, which is a billing state and should not be retried.
- `lookup_companies_by_domains` — Look up up to 100 website domains in one call. Domains are normalized and deduplicated in first-seen order, and results keep that order. Each hit costs 1 credit. Misses are free and are recorded for coverage review. If credits run out part way through, the remaining domains come back as insufficient_credits without a charge. summary gives the counts and total credits charged.
- `lookup_company_by_domain` — Find the company that owns one website domain. Accepts a bare domain or a full URL and matches the registrable domain exactly: stripe.com finds a company whose site is stripe.com or a subdomain of it, never a longer name such as bluestripe.com. A sub-host you send, like app.stripe.com, is not rewritten to its parent, so send the company's main domain. Alias and former domains match too, and domain_match says which. This counts as a standard search: free within the daily search quota, after which paid plans spend 1 credit per page that has results and free plans get a rate-limited error. A miss costs nothing and the domain is recorded for coverage review; coverage_status explains why nothing was returned.
- `search_companies` — Search company cards by name text and filters such as industry, country, size, operating status and funding range. Standard search is free within the daily search quota. After the quota, paid plans spend 1 credit per page that has results and free plans get a rate-limited error. Results are cards, so use get_company for funding history and stacks. Technology-stack filters are not exposed here because they are billed as a separate premium search.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Indexed state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Indexed is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/indexed
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Indexed homepage: https://indexed.vc
- API documentation: https://indexed.vc/docs/api
