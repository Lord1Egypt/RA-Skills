---
name: oo-attio
description: "Attio (attio.com). Use this skill for ANY Attio request — reading, creating, updating, and deleting data. Whenever a task involves Attio, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Attio"
  author: "OOMOL"
  version: "1.0.7"
  services: ["attio"]
  icon: "https://static.oomol.com/logo/third-party/attio.svg"
---

# Attio

Operate **Attio** through your OOMOL-connected account. This skill calls the `attio` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Attio. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "attio" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "attio" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_comment` — Create a plaintext comment on a record or entry, or reply to a thread. Requires an explicit workspace member author. [write]
- `create_entry` — Create a list entry. [write]
- `create_note` — Create a plaintext or Markdown note on a record. [write]
- `create_record` — Create a record for an Attio object using documented attribute value shapes. [write]
- `create_task` — Create a follow-up task. Defaults to incomplete, without deadline, linked records or assignees. [write]
- `delete_comment` — Delete a comment. [destructive]
- `delete_entry` — Remove a list entry without deleting its parent record. [destructive]
- `delete_note` — Delete a note. [destructive]
- `delete_record` — Delete a single Attio record by object and record ID. [destructive]
- `delete_task` — Delete a task. [destructive]
- `get_comment` — Get a comment.
- `get_entry` — Get a list entry and its attribute values.
- `get_list` — Get a list by ID or slug.
- `get_note` — Get a note.
- `get_object` — Get one Attio object by object ID or API slug.
- `get_record` — Get a single Attio record by object and record ID.
- `get_task` — Get a task.
- `get_thread` — Get a thread and paginate its comments.
- `get_workspace_member` — Get a workspace member.
- `identify` — Identify the current Attio access token, its workspace, and the scopes attached to it.
- `list_attributes` — List attributes on an object, list or activity. Requires the selected target configuration read scope.
- `list_entries` — Query entries in a list with filters, sorting and offset pagination.
- `list_list_views` — List saved views and their filters for an Attio list.
- `list_lists` — List all lists in the workspace.
- `list_notes` — List notes, optionally filtered by parent record.
- `list_object_views` — List saved views and their filters for an Attio object.
- `list_objects` — List all system-defined and user-defined objects in an Attio workspace.
- `list_record_entries` — List the list entries belonging to a record.
- `list_records` — List Attio records for an object with optional filtering, view filtering, sorting, limit, and offset.
- `list_select_options` — List available options for an object, list or activity attribute. Requires the selected target configuration read scope.
- `list_statuses` — List available statuses for an object or list attribute. Requires the selected target configuration read scope.
- `list_tasks` — List tasks filtered by completion, assignee or linked record.
- `list_threads` — List discussion threads, optionally filtered by record or list entry.
- `list_workspace_members` — List workspace members to resolve task assignees and comment authors.
- `search_records` — Search records across selected objects by name, email, domain, phone or social handle.
- `update_entry` — Update list entry values, appending or overwriting multiselect values. [write]
- `update_note` — Update note title or content; content is replaced when supplied. [write]
- `update_record` — Update an Attio record by appending or overwriting multiselect values according to Attio's PATCH and PUT semantics. [write]
- `update_task` — Update task completion, deadline, linked records or assignees. Attio does not support editing task content. [write]
- `upsert_entry` — Create or update a list entry by its parent record; supplied multiselect values overwrite existing values. [write]
- `upsert_record` — Create or update an Attio record for an object using a matching attribute that identifies at most one record. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Attio state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Attio is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/connections/attio
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Attio homepage: https://attio.com
- API documentation: https://docs.attio.com/
