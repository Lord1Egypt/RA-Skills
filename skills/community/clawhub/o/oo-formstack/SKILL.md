---
name: oo-formstack
description: "Formstack (formstack.com). Use this skill for ANY Formstack request — reading, creating, updating, and deleting data. Whenever a task involves Formstack, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Formstack"
  author: "OOMOL"
  version: "1.0.5"
  services: ["formstack"]
  icon: "https://static.oomol.com/logo/third-party/formstack.svg"
---

# Formstack

Operate **Formstack** through your OOMOL-connected account. This skill calls the `formstack` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Formstack. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "formstack" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "formstack" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_submission` — Create a submission for a Formstack form using field IDs and typed values. [write]
- `delete_submission` — Permanently delete a Formstack submission and its associated data. [destructive]
- `get_form` — Retrieve one Formstack form, optionally including its fields.
- `get_submission` — Retrieve one Formstack submission and its field data.
- `list_form_fields` — List the fields defined on a Formstack form.
- `list_forms` — List Formstack forms with pagination, name search, sorting, and folder filtering.
- `list_submissions` — List submissions for a Formstack form with pagination, time, keyword, and field-level filters.
- `update_submission` — Replace field values or metadata on an existing Formstack submission. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Formstack state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Formstack is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/formstack
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Formstack homepage: https://www.formstack.com/
- API documentation: https://developers.formstack.com/reference/api-overview
