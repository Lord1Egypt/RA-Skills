---
name: oo-getresponse
description: "GetResponse (getresponse.com). Use this skill for ANY GetResponse request — reading, creating, updating, and deleting data. Whenever a task involves GetResponse, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "GetResponse"
  author: "OOMOL"
  version: "1.0.5"
  services: ["getresponse"]
  icon: "https://static.oomol.com/logo/third-party/getresponse.svg"
---

# GetResponse

Operate **GetResponse** through your OOMOL-connected account. This skill calls the `getresponse` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected GetResponse. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "getresponse" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "getresponse" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_campaign` — Create a GetResponse campaign for organizing contacts. [write]
- `create_contact` — Queue a contact for creation in a GetResponse campaign. [write]
- `delete_contact` — Permanently delete a GetResponse contact by ID. [destructive]
- `get_campaign` — Retrieve one GetResponse campaign by ID.
- `get_contact` — Retrieve one GetResponse contact by ID.
- `get_newsletter` — Retrieve one GetResponse newsletter by ID.
- `get_newsletter_statistics` — Retrieve delivery and engagement statistics for one GetResponse newsletter.
- `list_campaigns` — List GetResponse campaigns, which represent contact lists.
- `list_contacts` — List and search GetResponse contacts with page-based pagination.
- `list_custom_fields` — List GetResponse custom fields that can be assigned to contacts.
- `list_newsletters` — List GetResponse newsletters with filters and pagination.
- `list_tags` — List GetResponse tags that can be assigned to contacts.
- `update_campaign` — Update mutable fields on a GetResponse campaign. [write]
- `update_contact` — Update a GetResponse contact, replacing tag and custom-field assignments when supplied. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change GetResponse state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — GetResponse is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/getresponse
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- GetResponse homepage: https://www.getresponse.com
- API documentation: https://apidocs.getresponse.com/v3
