---
name: oo-smarthr
description: "SmartHR (smarthr.jp). Use this skill for ANY SmartHR request — reading, creating, updating, and deleting data. Whenever a task involves SmartHR, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SmartHR"
  author: "OOMOL"
  version: "1.0.2"
  services: ["smarthr"]
  icon: "https://static.oomol.com/logo/third-party/smarthr.svg"
---

# SmartHR

Operate **SmartHR** through your OOMOL-connected account. This skill calls the `smarthr` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SmartHR. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "smarthr" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "smarthr" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clear_employee_departments` — Clear all department assignments on a SmartHR employee without deleting the employee or department records. [write]
- `create_department` — Create a SmartHR department. [write]
- `create_employee` — Create a SmartHR employee. No employee fields are mandatory; attachments accept file URLs. [write]
- `create_employment_type` — Create a SmartHR employment type. System preset and scheduled-change restrictions are enforced by SmartHR. [write]
- `create_grade` — Create a SmartHR grade. [write]
- `create_job_category` — Create a SmartHR job category. [write]
- `create_job_title` — Create a SmartHR job title. [write]
- `create_recruitment_type` — Create a SmartHR recruitment type. [write]
- `delete_employee` — Delete a SmartHR employee record. [destructive]
- `delete_employment_type` — Delete a SmartHR employment type. System preset and scheduled-change restrictions are enforced by SmartHR. [destructive]
- `delete_grade` — Delete a SmartHR grade. [destructive]
- `delete_job_category` — Delete a SmartHR job category. [destructive]
- `delete_job_title` — Delete a SmartHR job title. [destructive]
- `delete_recruitment_type` — Delete a SmartHR recruitment type. [destructive]
- `discontinue_department` — Discontinue a SmartHR department on its last active date. The date must be in the past; scheduled employee changes can prevent discontinuation. [destructive]
- `get_department` — Get a SmartHR department by ID.
- `get_employee` — Get a SmartHR employee by ID.
- `get_employee_input_form` — Get a SmartHR employee information collection form by ID.
- `get_employment_type` — Get a SmartHR employment type by ID.
- `get_grade` — Get a SmartHR grade by ID.
- `get_job_category` — Get a SmartHR job category by ID.
- `get_job_title` — Get a SmartHR job title by ID.
- `get_payment_period` — Get a SmartHR payment period by ID.
- `get_recruitment_type` — Get a SmartHR recruitment type by ID.
- `get_user` — Get a SmartHR user by ID.
- `invite_employee` — Send or resend an invitation to the employee email address. The inviter must be an administrator; the invited user receives member permissions. Already accepted invitations cannot be resent. [write]
- `list_bank_account_settings` — List SmartHR bank account setting records with pagination.
- `list_business_establishments` — List SmartHR business establishments with pagination.
- `list_companies` — List SmartHR companies with pagination.
- `list_custom_field_groups` — List SmartHR custom employee field groups with pagination.
- `list_custom_fields` — List SmartHR custom employee fields with pagination.
- `list_departments` — List SmartHR departments with pagination.
- `list_employee_input_forms` — List SmartHR employee information collection form records with pagination.
- `list_employees` — List SmartHR employees with pagination.
- `list_employment_types` — List SmartHR employment types with pagination.
- `list_grades` — List SmartHR grade records with pagination.
- `list_job_categories` — List SmartHR job category records with pagination.
- `list_job_titles` — List SmartHR job title records with pagination.
- `list_payment_periods` — List SmartHR payment period records with pagination.
- `list_recruitment_types` — List SmartHR recruitment type records with pagination.
- `list_users` — List SmartHR user records with pagination.
- `replace_department` — Replace a SmartHR department. Unspecified attributes are cleared by SmartHR. [write]
- `replace_employment_type` — Update a SmartHR employment type using the full-update endpoint; use partial update to preserve unspecified attributes. System preset and scheduled-change restrictions are enforced by SmartHR. [write]
- `replace_grade` — Update a SmartHR grade using the full-update endpoint; use partial update to preserve unspecified attributes. [write]
- `replace_job_category` — Update a SmartHR job category using the full-update endpoint; use partial update to preserve unspecified attributes. [write]
- `replace_job_title` — Update a SmartHR job title using the full-update endpoint; use partial update to preserve unspecified attributes. [write]
- `replace_recruitment_type` — Update a SmartHR recruitment type using the full-update endpoint; use partial update to preserve unspecified attributes. [write]
- `update_department` — Partially update a SmartHR department, preserving unspecified attributes. SmartHR requires name. [write]
- `update_employee` — Update only the supplied SmartHR employee fields. SmartHR prevents clearing populated identity fields; attachments accept file URLs. [write]
- `update_employment_type` — Partially update a SmartHR employment type, preserving unspecified attributes. System preset and scheduled-change restrictions are enforced by SmartHR. [write]
- `update_grade` — Partially update a SmartHR grade, preserving unspecified attributes. [write]
- `update_job_category` — Partially update a SmartHR job category, preserving unspecified attributes. [write]
- `update_job_title` — Partially update a SmartHR job title, preserving unspecified attributes. [write]
- `update_recruitment_type` — Partially update a SmartHR recruitment type, preserving unspecified attributes. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SmartHR state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SmartHR is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/smarthr
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SmartHR homepage: https://smarthr.jp/
- API documentation: https://developer.smarthr.jp/api
