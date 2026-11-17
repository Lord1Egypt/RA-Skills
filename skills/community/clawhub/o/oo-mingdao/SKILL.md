---
name: oo-mingdao
description: "Mingdao (mingdao.com). Use this skill for ANY Mingdao request — reading, creating, updating, and deleting data. Whenever a task involves Mingdao, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mingdao"
  author: "OOMOL"
  version: "1.0.3"
  services: ["mingdao"]
  icon: "https://static.oomol.com/logo/third-party/mingdao.png"
---

# Mingdao

Operate **Mingdao** through your OOMOL-connected account. This skill calls the `mingdao` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mingdao. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mingdao" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mingdao" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_role_members` — Add users, departments, department trees, jobs or organization roles to an application role. [write]
- `batch_create_custom_actions` — Create workflow, record-update or related-record custom action buttons. [write]
- `batch_create_records` — Create multiple Mingdao worksheet records with the batch API's string-encoded field values and URL-based attachments. [write]
- `batch_create_views` — Create table, kanban, gallery, calendar, hierarchy, gantt, resource, detail or map views with their configuration. [write]
- `batch_delete_records` — Delete multiple Mingdao worksheet records, optionally permanently instead of using the recycle bin. [destructive]
- `batch_update_records` — Apply the same field updates to multiple Mingdao worksheet records and report successful and failed record IDs. [destructive]
- `create_app_items` — Create blank worksheet or custom-page application items. [write]
- `create_app_sections` — Create navigation sections in the connected Mingdao application. [write]
- `create_chart` — Create a worksheet chart with dimensions, metrics, date ranges and filters. [write]
- `create_chatbot` — Create a chatbot with a system prompt, welcome message and up to five preset questions. [write]
- `create_optionset` — Create an application option set with ordered values, colors and scores. [write]
- `create_record` — Create a Mingdao worksheet record using field IDs or aliases and URL-based attachment values. [write]
- `create_role` — Create an application role with global or per-worksheet, view, field and page permissions. [write]
- `create_worksheet` — Create a worksheet and its fields, including links to already-created worksheets. [write]
- `delete_record` — Delete a Mingdao worksheet record, optionally permanently instead of using the recycle bin. [destructive]
- `delete_role` — Delete an application role and revoke the access it grants. [destructive]
- `delete_worksheet` — Delete a worksheet from the connected application. [destructive]
- `disable_optionset` — Disable an existing application option set. [destructive]
- `generate_record_share_link` — Generate a record share link with selected visible fields, optional password and expiration. Omitted or zero expiration means the link does not expire. [write]
- `get_app` — Get the connected Mingdao application's identity, metadata and navigation sections.
- `get_approval` — Get the execution details, current steps and available operation metadata for an existing Mingdao record approval.
- `get_record` — Get one Mingdao worksheet record with its dynamic field values and optional system fields.
- `get_related_records` — Page through the records linked by a Mingdao record's relationship field.
- `get_role` — Get a Mingdao application role's global, worksheet, field and custom-page permissions.
- `get_workflow` — Get a Mingdao workflow's input and output parameter definitions before triggering it.
- `get_worksheet` — Get a Mingdao worksheet's fields, views and metadata before querying or writing its records.
- `list_approvals` — List approval executions for a Mingdao record, optionally selecting completed or incomplete executions.
- `list_knowledge` — List Mingdao application knowledge bases, including their configured embedding models.
- `list_optionsets` — List the reusable option sets in the connected Mingdao application.
- `list_record_discussions` — Read a Mingdao record's discussions, including replies, mentions and attachment metadata, with optional search and Markdown output.
- `list_record_logs` — Read a Mingdao record's change logs, optionally filtered by operators, field and date range.
- `list_records` — Search, filter, sort and page through Mingdao worksheet records, with optional field selection and total count.
- `list_regions` — List or search Mingdao geographic regions; omit the region ID to retrieve top-level regions.
- `list_roles` — List the connected Mingdao application's roles and their user, department, job and organization-role memberships.
- `list_workflows` — List the existing webhook and packaged business process workflows available in the connected Mingdao application.
- `list_worksheets` — List worksheets in the connected Mingdao application, optionally restricted to selected worksheet IDs.
- `lookup_departments` — Look up departments in the Mingdao application's organization, optionally matching an exact department name.
- `lookup_users` — Look up users in the Mingdao application's organization, optionally matching an exact user name.
- `pivot_records` — Aggregate Mingdao worksheet records into a pivot table with grouping dimensions, filters, sorting and optional summary totals.
- `remove_role_members` — Remove users, departments, department trees, jobs or organization roles from an application role. [destructive]
- `remove_user_from_all_roles` — Remove a user from every role in the connected application. [destructive]
- `search_knowledge` — Search Mingdao knowledge content using vector, keyword or hybrid retrieval. Knowledge bases with different embedding models must be searched in separate calls.
- `trigger_workflow` — Trigger an existing Mingdao workflow with its defined parameters. Its configured steps may update or delete business data; the returned result does not imply that all downstream work has completed. [destructive]
- `update_custom_page` — Replace the complete custom-page component layout, including inline charts, views, tabs, containers and filter groups. [destructive]
- `update_optionset` — Update an option set's name, keyed options, order, colors and scores. [destructive]
- `update_record` — Update a Mingdao worksheet record, replacing, adding or removing supported field values. [destructive]
- `update_worksheet` — Update worksheet metadata and add, edit or delete fields. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mingdao state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mingdao is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/mingdao
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Mingdao homepage: https://www.mingdao.com/
- API documentation: https://help.mingdao.com/api/introduction/
