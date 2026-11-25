---
name: oo-baobiao
description: "Baobiao (woyaobid.com). Use this skill for ANY Baobiao request — searching and reading data. Whenever a task involves Baobiao, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Baobiao"
  author: "OOMOL"
  version: "1.0.0"
  services: ["baobiao"]
  icon: "https://static.oomol.com/logo/third-party/baobiao.png"
---

# Baobiao

Operate **Baobiao** through your OOMOL-connected account. This skill calls the `baobiao` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Baobiao. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "baobiao" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "baobiao" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `build_search_query` — Turn a plain-language request, such as 湖北近30天物业服务中标结果，金额500万以上, into search_projects filters with keywords, dates, notice class, procurement type, amount range, and region and industry codes. Waits up to about 25 seconds; if status is not completed, call again with the same userQuery to keep polling. A failed rewrite is returned as an error.
- `get_account_resources` — Read the Baobiao account's cash balance, coupon balance, and package call quota. The account must have this endpoint enabled by Baobiao sales; a failure does not mean the balance is zero.
- `get_company_business_info` — Read a company's key business information from a third-party registry: type, industry, region, capital, headcount, status, credit code, scope, and its tender and award counts.
- `get_company_registration` — Read a company's full business registration record: codes, legal representative, capital, status, operating period, scope, address, tax details, industry chain, headcount, listing status, contacts, and tags.
- `get_company_statistics` — Read a company's bid and award statistics by industry and its contact, customer, and supplier relationship counts, without registration details.
- `get_company_summary` — Read a company profile summary: registration, capital, operation and contact details, bid and award statistics by industry, relationship counts, and which datasets have data.
- `get_planned_project` — Read the full details of a planned or under-construction project.
- `get_project_content` — Read the full HTML body of a tender or award notice with its parties, amount, classification, and attachment names. Use get_project_text when plain text is enough.
- `get_project_requirements` — Read the second-stage extraction of a notice: funding sources, subject matter, qualification requirements, evaluation methods, and per-bidder quotes and scores. Only notices published on or after 2026-09-18 may have this data.
- `get_project_source_url` — Get the original web page a tender or award notice was collected from.
- `get_project_structure` — Read fields Baobiao extracted from a notice: project name and numbers, lots, budget and award amounts in yuan, registration deadline, bid opening time and place, buyer, supplier, and agency contacts, bidders, and the source URL.
- `get_project_text` — Read a tender or award notice as plain text without HTML, with region names, amount, category, and buyer, supplier, and agency name lists. Best for summarizing a notice.
- `infer_industry_codes` — Infer national economic industry classification codes (GB/T 4754) for an industry phrase, for use in industryCode filters.
- `list_company_contacts` — List contact people and phone numbers that appeared in a company's tender and award notices. The result contains personal data; use it only for lawful business contact.
- `list_company_customers` — List the buyers a company has supplied, one record per related project.
- `list_company_suppliers` — List the suppliers a company has bought from, one record per related project.
- `list_planned_project_files` — List a planned project's attachments with download links.
- `list_project_files` — List a tender or award notice's attachments with public download links and download state.
- `search_companies` — Search Chinese companies by name, former name, legal representative, unified social credit code, or registration number, and return brief business-registration profiles.
- `search_company_projects` — List the tender and award notices a company took part in as buyer, supplier, or agency.
- `search_contracts` — Search published procurement contracts by keyword, region and industry codes, parties, amount range, and contract period.
- `search_planned_projects` — Search planned and under-construction projects, such as investment filings and approvals, before they go to tender.
- `search_projects` — Search Chinese tender and award notices with code-based filters: notice class, procurement type, region and industry codes, amount range, party names, subject matter, contract end date, and attachments. Use build_search_query to turn a plain-language request into these filters.
- `search_projects_by_number` — Find tender and award notices by their official project or tender number.
- `search_projects_by_source_url` — Search tender and award notices collected from specific publishing websites, such as a provincial government procurement portal.
- `search_projects_simple` — Search Chinese tender, award, contract, procurement-intention, and auction notices with plain-language filters such as a region name, category name, and company name. Prefer this over search_projects unless you need code-based filters. Results include parties, contacts, deadlines, and source links.
- `search_purchasing_units` — Find buyers (tendering organizations) whose name contains the given text, with their historical tender count, total tender amount, and contact and supplier counts.
- `search_winning_suppliers` — Find suppliers (winning bidders) whose name contains the given text, with their historical award count, total award amount, and contact and customer counts.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Baobiao state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Baobiao is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/baobiao
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Baobiao homepage: https://www.woyaobid.com/
- API documentation: https://console.woyaobid.com/gateway-admin/share/api-doc
