---
name: oo-hrmos-kintai
description: "HRMOS Kintai (ieyasu.co). Use this skill for ANY HRMOS Kintai request — reading, creating, updating, and deleting data. Whenever a task involves HRMOS Kintai, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HRMOS Kintai"
  author: "OOMOL"
  version: "1.0.2"
  services: ["hrmos_kintai"]
  icon: "https://static.oomol.com/logo/third-party/hrmos_kintai.svg"
---

# HRMOS Kintai

Operate **HRMOS Kintai** through your OOMOL-connected account. This skill calls the `hrmos_kintai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HRMOS Kintai. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hrmos_kintai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hrmos_kintai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_business_partner` — Create business partner. [write]
- `create_contract` — Create contract. [write]
- `create_partner_contact` — Create business partner approval contacts. [write]
- `create_stamp` — Record a clock-in, clock-out or break punch, with optional location and night-shift information. [write]
- `delete_business_partner` — Delete business partner. [destructive]
- `delete_contract` — Delete contract. [destructive]
- `delete_partner_contact` — Delete business partner approval contacts. [destructive]
- `export_dependent_declaration` — Export dependent declaration as a downloadable CSV file for the specified year.
- `export_housing_loan_declaration` — Export housing loan declaration as a downloadable CSV file for the specified year.
- `export_income_deduction_declaration` — Export income deduction declaration as a downloadable CSV file for the specified year.
- `export_insurance_deduction_declaration` — Export insurance deduction declaration as a downloadable CSV file for the specified year.
- `export_next_year_dependent_declaration` — Export next year dependent declaration as a downloadable CSV file for the specified year.
- `export_previous_employment_withholding` — Export previous employment withholding as a downloadable CSV file for the specified year.
- `get_monthly_report_definitions` — Get field definitions for monthly report.
- `get_time_band_report_definitions` — Get field definitions for time band report.
- `list_business_partners` — List business partners.
- `list_contracts` — List contracts.
- `list_daily_attendance` — List attendance records for all employees on a specified day.
- `list_daily_attendance_differences` — List daily attendance time differences.
- `list_daily_stamp_logs` — List clock-in, clock-out and break punch history for a specified day.
- `list_daily_time_band_totals` — List daily working-time totals for custom time bands within the requested month.
- `list_departments` — List departments in the connected company.
- `list_employee_leave_history` — List an employee's leave grants, usage, adjustments and remaining balances for a leave setting and year.
- `list_employee_stamp_logs` — List an employee's punch history, optionally filtered by punch type and update time.
- `list_employees` — List employees in the connected HRMOS Kintai company.
- `list_employment_types` — List employment types in the connected company.
- `list_leave_types` — List leave settings used to query employee leave balances and history.
- `list_monthly_attendance` — List daily attendance records for a month, respecting each employee's cutoff date. Optionally filter by employee ID.
- `list_monthly_attendance_differences` — List monthly attendance time differences.
- `list_monthly_report_values` — List monthly report values including company-defined fields.
- `list_monthly_reports` — List monthly attendance summaries, optionally filtered by employee numbers and month-closing statuses.
- `list_monthly_time_band_totals` — List monthly working-time totals for custom time bands within the requested month.
- `list_partner_contacts` — List business partner approval contacts.
- `list_prefectures` — List Japanese prefectures for workplace and partner address selection.
- `list_time_band_report_values` — List time band report values including company-defined fields.
- `list_work_segments` — List work classifications and their configured working hours.
- `list_workplaces` — List workplaces, optionally filtered by prefecture.
- `update_attendance` — Update clock-in, clock-out and break times on an existing daily attendance record. [write]
- `update_business_partner` — Update business partner. May end the trading relationship when close_out is 1. [destructive]
- `update_contract` — Update contract. [write]
- `update_partner_contact` — Update business partner approval contacts. [write]
- `upsert_employee` — Register or update an employee matched by login ID, including calendars and approval groups. Login ID, password and cutoff day cannot be changed after registration. [write]
- `upsert_external_attendance` — Register or update external attendance times on an existing daily attendance record. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HRMOS Kintai state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HRMOS Kintai is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/hrmos_kintai
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- HRMOS Kintai homepage: https://www.ieyasu.co/
- API documentation: https://ieyasu.co/docs/api.html
