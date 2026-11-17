---
name: oo-tianyancha
description: "Tianyancha (tianyancha.com). Use this skill for ANY Tianyancha request — searching and reading data. Whenever a task involves Tianyancha, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tianyancha"
  author: "OOMOL"
  version: "1.0.5"
  services: ["tianyancha"]
  icon: "https://static.oomol.com/logo/third-party/tianyancha.svg"
---

# Tianyancha

Operate **Tianyancha** through your OOMOL-connected account. This skill calls the `tianyancha` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tianyancha. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tianyancha" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tianyancha" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `find_company_relationship_paths` — Find the shortest ownership, employment, legal, business, or historical relationship paths between two companies.
- `get_company_actual_control` — Get a company's suspected actual controllers, ownership ratios, and control paths from Tianyancha.
- `get_company_annual_reports` — Get a company's annual reports, including disclosed financial, shareholder, investment, and social security information.
- `get_company_basic_info` — Get Tianyancha company registration details by company identifier.
- `get_company_contact_info` — Get a company's phone numbers, email addresses, websites, and registered address.
- `get_company_development_info` — Get a company's core team, products, financing history, investment events, competitors, and investment institutions.
- `get_company_intellectual_property` — Get a company's trademarks, patents, software copyrights, works copyrights, and ICP registrations.
- `get_company_judicial_risk` — Get a company's combined legal cases, hearings, court notices, enforcement, dishonesty, filing, and service-announcement data.
- `get_company_risk` — Get a company's Tianyancha risk summary, including own, related, historical, and alert risks.
- `get_company_risk_detail` — Get one page of detailed Tianyancha risk records using a risk ID and type from get_company_risk.
- `list_company_branches` — List a company's branch organizations and their registration details.
- `list_company_changes` — List a company's registration changes, including before and after values.
- `list_company_equity_changes` — List a company's disclosed equity changes, including shareholders before and after each change.
- `list_company_historical_investments` — List companies previously invested in by a company using Tianyancha.
- `list_company_historical_shareholders` — List a company's historical shareholders, ownership ratios, and subscribed capital from Tianyancha.
- `list_company_investments` — List companies directly invested in by a company using Tianyancha.
- `list_company_key_personnel` — List a company's directors, supervisors, and senior managers from Tianyancha.
- `list_company_news` — List Tianyancha news for an exact company, optionally filtered by publication date and tags.
- `list_company_shareholders` — List a company's shareholders and contribution details from Tianyancha.
- `list_company_ultimate_beneficiaries` — List a company's ultimate beneficiaries, ownership percentages, and ownership chains from Tianyancha.
- `search_companies` — Search Tianyancha for companies by keyword and return matching company records.
- `search_companies_advanced` — Search Tianyancha for companies by keyword, industry, and region.
- `search_tenders` — Search Tianyancha tender and bid notices by keyword, participant role, notice type, province, and publication date.
- `verify_company_identity` — Verify that a company name, legal representative, and registration code identify the same company.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tianyancha state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tianyancha is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/tianyancha
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tianyancha homepage: https://www.tianyancha.com/data
