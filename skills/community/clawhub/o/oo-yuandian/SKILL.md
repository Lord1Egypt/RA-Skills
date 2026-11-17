---
name: oo-yuandian
description: "Yuan Dian (open.chineselaw.com). Use this skill for ANY Yuan Dian request — searching and reading data. Whenever a task involves Yuan Dian, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Yuan Dian"
  author: "OOMOL"
  version: "1.0.5"
  services: ["yuandian"]
  icon: "https://static.oomol.com/logo/third-party/yuandian.svg"
---

# Yuan Dian

Operate **Yuan Dian** through your OOMOL-connected account. This skill calls the `yuandian` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Yuan Dian. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "yuandian" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "yuandian" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_legal_hallucinations` — Check legal text for hallucinated or inconsistent statute, clause, and case references using Yuan Dian.
- `get_case_details` — Retrieve Yuan Dian ordinary or authoritative case details by case ID or case number.
- `get_clause_detail` — Retrieve one Yuan Dian statutory clause detail by clause ID or by regulation name and clause number.
- `get_enterprise_aggregation_summary` — Retrieve Yuan Dian enterprise aggregation summary for due-diligence and risk review.
- `get_enterprise_annual_report` — Retrieve one Yuan Dian enterprise annual report by enterprise ID or unified social credit code and year.
- `get_enterprise_base_info` — Retrieve Yuan Dian enterprise base registration, shareholder, member, and branch information.
- `get_enterprise_detail` — Retrieve one Yuan Dian enterprise aggregate detail by enterprise ID or unified social credit code.
- `get_enterprise_litigation_statistics` — Retrieve Yuan Dian enterprise litigation statistics grouped by case, court, year, region, and party dimensions.
- `get_regulation_detail` — Retrieve one Yuan Dian regulation detail by regulation ID or regulation name, optionally at a reference date.
- `list_enterprise_business_records` — List paginated Yuan Dian enterprise changes, investments, guarantees, pledges, or frozen-equity records.
- `list_enterprise_compliance_records` — List paginated Yuan Dian punishment, abnormal-operation, serious-illegal, or tax records for one enterprise.
- `list_enterprise_court_notices` — List paginated Yuan Dian court session notices or court notices for one enterprise.
- `list_enterprise_execution_risks` — List paginated Yuan Dian executed-person or dishonest-execution records for one enterprise.
- `list_enterprise_ip_assets` — List paginated Yuan Dian patents, trademarks, copyrights, software copyrights, or ICP filings for one enterprise.
- `list_enterprise_writs` — List paginated Yuan Dian writ summaries related to one enterprise.
- `search_authoritative_cases` — Search Yuan Dian authoritative, typical, reference, bulletin, and guidance cases by metadata and full-text filters.
- `search_clauses` — Search Yuan Dian statutory clauses by required content keyword plus optional regulation metadata filters.
- `search_enterprise_profiles` — Search Yuan Dian enterprise profile candidates by enterprise name or stock short name.
- `search_enterprises` — Search Yuan Dian enterprises by name and return low-cost enterprise identifier candidates.
- `search_ordinary_cases` — Search Yuan Dian ordinary adjudication cases by case metadata, full text, analysis text, and cited clauses.
- `search_regulations` — Search Yuan Dian regulations by keyword, name, validity, region, effect level, issuing authority, and dates.
- `semantic_search_cases` — Run a natural-language semantic search over Yuan Dian cases with optional case metadata filters.
- `semantic_search_regulations` — Run a natural-language semantic search over Yuan Dian statutory clauses and return matched clauses.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Yuan Dian state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Yuan Dian is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/yuandian
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Yuan Dian homepage: https://open.chineselaw.com
- API documentation: https://open.chineselaw.com/api-square/
