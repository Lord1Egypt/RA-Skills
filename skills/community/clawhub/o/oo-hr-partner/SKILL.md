---
name: oo-hr-partner
description: "HR Partner (hrpartner.io). Use this skill for ANY HR Partner request — searching and reading data. Whenever a task involves HR Partner, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "HR Partner"
  author: "OOMOL"
  version: "1.0.4"
  services: ["hr_partner"]
  icon: "https://static.oomol.com/logo/third-party/hr_partner.png"
---

# HR Partner

Operate **HR Partner** through your OOMOL-connected account. This skill calls the `hr_partner` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected HR Partner. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hr_partner" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hr_partner" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_applicant` — Retrieve one HR Partner recruitment applicant by applicant ID or email address, including their job applications when available.
- `get_application` — Retrieve one HR Partner recruitment application by application ID, including applicant, job listing, scorecard, attachment metadata, interviews, and comments when available.
- `get_company` — Retrieve basic HR Partner company information, optionally including custom fields and active modules.
- `get_employee` — Retrieve one HR Partner employee by employee code, including detailed contact, address, tag, and custom field data when available.
- `get_job_listing` — Retrieve one HR Partner recruitment job listing by job ID, including detailed content, custom form, scorecard, and stage data when available.
- `list_applicants` — List HR Partner recruitment applicants, optionally filtered by name or email search text.
- `list_applications` — List HR Partner recruitment applications for one job listing with official filters such as source, stage, submitted date, and read flags.
- `list_employees` — List HR Partner employees with official filters such as search, department, location, status, tags, and employment dates.
- `list_job_listings` — List HR Partner recruitment job listings with official filters such as search, department, publish dates, active state, and response email.
- `list_lookups` — Retrieve one HR Partner read-only lookup file such as departments, locations, positions, tags, stages, or training statuses.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change HR Partner state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — HR Partner is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/hr_partner
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- HR Partner homepage: https://www.hrpartner.io/
- API documentation: https://developer.hrpartner.io/
