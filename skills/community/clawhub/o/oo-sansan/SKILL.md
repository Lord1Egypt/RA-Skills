---
name: oo-sansan
description: "Sansan (jp.sansan.com). Use this skill for ANY Sansan request — reading, creating, updating, and deleting data. Whenever a task involves Sansan, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sansan"
  author: "OOMOL"
  version: "1.0.2"
  services: ["sansan"]
  icon: "https://static.oomol.com/logo/third-party/sansan.svg"
---

# Sansan

Operate **Sansan** through your OOMOL-connected account. This skill calls the `sansan` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sansan. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sansan" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sansan" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_organization_import` — Validate user and department import data without applying changes. System administrator only; returns a downloadable CSV report if errors exist.
- `create_access_control_pattern` — Create an access control pattern with department access rules. System administrator only. [write]
- `create_business_card` — Create a Sansan business card, optionally for another user through the administrator import API. [write]
- `create_contact_report` — Create a Sansan contact report. External attendee details also create new business cards; optionally import for another owner as an administrator. [write]
- `delete_access_control_pattern` — Delete an access control pattern. System administrator only; Sansan may reject a pattern still in use. [destructive]
- `export_organization_departments` — Export Sansan organization departments as a CSV download. System administrator only.
- `export_organization_users` — Export Sansan organization users as a CSV download. System administrator only.
- `get_business_card` — Get a business card by ID. Sansan may return the latest merged card with a different ID.
- `get_business_card_image` — Download the front or back of a Sansan business card as a JPEG file URL.
- `get_current_user` — Get the Sansan user and permissions associated with the connected API key.
- `get_default_email_client` — Get the default email client settings for new users. System administrator only.
- `get_department_access_control` — Get the access control pattern assigned to a department. System administrator only.
- `get_organization_import_result` — Check an organization import and return its result CSV when completed or failed. System administrator only. The report includes created IDs and row-level errors.
- `get_organization_import_status` — Get the current organization import status. System administrator only.
- `get_person` — Get the latest business card for a Sansan person, optionally including tags.
- `list_access_control_patterns` — List access control patterns, optionally filtering by a name substring. System administrator only.
- `list_business_card_tags` — List tags attached to a Sansan business card.
- `list_business_cards` — List business cards updated within a time interval, with optional historical cards and tags. Use nextPageToken to continue.
- `list_contact_reports` — List Sansan contact reports updated within a time interval, including meetings, calls, emails, and business card exchanges.
- `list_departments` — List administrative department IDs, names, and parents. System administrator only.
- `list_tags` — List Sansan tags by ownership, visibility, owner user, and tag name.
- `search_business_cards` — Search accessible Sansan business cards by company, name, email, telephone, mobile, and tags.
- `set_default_email_client` — Set the default email client for subsequently added users; users may change it later. System administrator only. [write]
- `set_department_access_control` — Assign an access control pattern to a department. System administrator only. [write]
- `submit_organization_import` — Submit user and department additions, updates, or deletions. System administrator only. DeleteFlag can delete users or departments; preserve the import ID to retrieve results. [destructive]
- `update_access_control_pattern` — Update an access control pattern and its department rules. System administrator only. [write]
- `upload_business_card_image` — Submit JPEG business card images for paid Sansan digitization. Optionally use administrator import for another owner. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sansan state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sansan is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sansan
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sansan homepage: https://jp.sansan.com
- API documentation: https://docs.ap.sansan.com/ja/api/openapi/index.html
