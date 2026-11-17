---
name: oo-fundable
description: "Fundable (tryfundable.ai). Use this skill for ANY Fundable request — reading, creating, and updating data. Whenever a task involves Fundable, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Fundable"
  author: "OOMOL"
  version: "1.0.2"
  services: ["fundable"]
  icon: "https://static.oomol.com/logo/third-party/fundable.svg"
---

# Fundable

Operate **Fundable** through your OOMOL-connected account. This skill calls the `fundable` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Fundable. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fundable" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fundable" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_alert_configurations` — Retrieve all alert configurations for the authenticated user (identified by API key). Returns configuration metadata including filters, frequency, and descriptions. Requires Pro+ or Enterprise; consumes no credits.
- `get_alerts` — Retrieve saved alert data including all deals that matched the alert criteria within the specified date range. Results include a flattened array of deals sorted by date (newest first) with duplicates removed. Requires Pro+ or Enterprise; consumes no credits.
- `get_company` — Use this endpoint when one company is already identified and its full profile and latest funding round are required. Prefer a domain or LinkedIn URL when available; they can be passed directly here without calling `/company/search` first.
- `get_company_deals` — Use this endpoint when a company is already identified and its complete funding history is required. Prefer a domain or LinkedIn URL when available; it can be passed directly without first calling `/company/search`.
- `get_deal_by_id` — Use this endpoint when a deal UUID is already known and full details for that one funding round are required. The response identifies related entities by ID rather than embedding their full profiles. Use `GET /company?id=...` for company metadata and `GET /deals/{id}/investors` for the complete investor lineup.
- `get_deal_investors` — Use this endpoint after identifying a deal when investor IDs in the deal record need to be resolved into the complete investor lineup. It returns firm investors, associated people, angel investors, lead status, and profile links for one deal.
- `get_investor_by_identifier` — Use this endpoint when one investor firm is already identified and its full profile, statistics, and portfolio summary are required. Prefer a domain or LinkedIn URL when available; it can be passed directly without calling `/investor/search` first.
- `get_investor_deals` — Use this endpoint when an investor firm is already identified and its complete deal history is required. Prefer a domain or LinkedIn URL when available; it can be passed directly without calling `/investor/search` first.
- `get_person` — Use this endpoint when one person is already identified and their full profile is required. Prefer a LinkedIn URL when available; it can be passed directly without calling `/person/search` first.
- `get_person_deals` — Use this endpoint when a person is already identified and their investment history is required. It returns deals the person joined as an angel plus lead or firm deals. Prefer a LinkedIn URL when available; it can be passed directly without first calling `/person/search`.
- `get_person_email` — Use this endpoint only when a verified email is explicitly required for an identified person. Return a verified email for a person identified by UUID, LinkedIn, Crunchbase, or Twitter/X. Provide one identifier. If multiple identifiers are supplied, the endpoint uses the first non-empty value in this order: `id`, `linkedin`, `crunchbase`, `twitter`. Unlocks contact information for the account; new unlocks cost 5 credits and repeats cost 0. Requires non-trial Pro+, Enterprise, or API plan. [write]
- `get_person_phone` — Use this endpoint only when a verified phone number is explicitly required for an identified person. Return a verified phone number for a person identified by UUID, LinkedIn, Crunchbase, or Twitter/X. Provide one identifier. If multiple identifiers are supplied, the endpoint uses the first non-empty value in this order: `id`, `linkedin`, `crunchbase`, `twitter`. Unlocks contact information for the account; new unlocks cost 5 credits and repeats cost 0. Requires non-trial Pro+, Enterprise, or API plan. [write]
- `list_investors` — Use this endpoint when the requested result is a list of investor firms. Filters under `company_investments` identify qualifying portfolio companies and deals, then return the firms that participated in those deals. For example, use this route to find San Francisco-based investors that participated in a Seed round during the last year.
- `search_companies` — Use this endpoint by default for company sourcing and discovery. It returns company metadata such as name and domain together with the full details of each company's latest funding round.
- `search_company` — Use this endpoint primarily to resolve a fuzzy company name or an uncertain identifier into matching company records. If a reliable domain or LinkedIn URL is already available, skip this search and pass it directly to `GET /company` for one full profile or to `POST /companies` for a batch lookup.
- `search_deals` — Use this endpoint when the requested result is a set of funding rounds, or when deal criteria must match any historical round rather than only each company's latest round. It supports round-level analysis across the full deal history.
- `search_industries` — Use this endpoint before semantic search to resolve a human-readable category into an exact `INDUSTRY` or `SUPER_CATEGORY` permalink. Agents should not guess permalinks. If the taxonomy has an appropriate result, use its permalink in the structured industry filter. Use `search_query` only when the requested niche is not represented by the taxonomy.
- `search_investors` — Use this endpoint primarily to resolve a fuzzy investor-firm name or an uncertain identifier. If a reliable domain or LinkedIn URL is already available, skip this search and pass it directly to `GET /investor` for one full profile or to `POST /investors` for a batch lookup.
- `search_locations` — Use this endpoint to resolve a human-readable city, state, country, or region into the exact permalink required by location filters on discovery endpoints. Agents should not guess permalinks. Select the result that matches the user's intended geography, then pass its permalink to the relevant filter.
- `search_people` — Use this endpoint when the requested result is a list of people.
- `search_person` — Use this endpoint primarily to resolve a fuzzy person name or uncertain identifier. If a reliable LinkedIn URL is already available, skip this search and pass it directly to `GET /person` for one full profile or to `POST /people` for a batch lookup.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Fundable state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Fundable is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/fundable
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Fundable homepage: https://www.tryfundable.ai
- API documentation: https://docs.tryfundable.ai/
