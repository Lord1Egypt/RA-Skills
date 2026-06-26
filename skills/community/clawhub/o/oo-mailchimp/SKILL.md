---
name: oo-mailchimp
description: "Mailchimp (mailchimp.com). Use this skill for ANY Mailchimp request — reading, creating, updating, and deleting data. Whenever a task involves Mailchimp, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mailchimp"
  author: "OOMOL"
  version: "1.0.1"
  services: ["mailchimp"]
  icon: "https://static.oomol.com/logo/third-party/Mailchimp.svg"
---

# Mailchimp

Operate **Mailchimp** through your OOMOL-connected account. This skill calls the `mailchimp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mailchimp. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mailchimp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mailchimp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_member` — Archive a Mailchimp member from the specified audience/list. [write]
- `delete_member_permanently` — Permanently delete a Mailchimp member from the specified audience/list. [destructive]
- `get_list` — Fetch a single Mailchimp audience/list by ID.
- `get_member` — Fetch a single Mailchimp member by subscriber hash or email address.
- `list_lists` — List Mailchimp audiences/lists visible to the current API key.
- `list_member_tags` — List tags currently attached to a Mailchimp member.
- `list_members` — List members in a Mailchimp audience/list.
- `list_merge_fields` — List merge fields defined for a Mailchimp audience/list. [write]
- `update_member` — Patch an existing Mailchimp member by subscriber hash or email address. [write]
- `update_member_tags` — Add or remove Mailchimp member tags using the official tag-update endpoint. [write]
- `upsert_member` — Add or update a Mailchimp member using the official upsert endpoint. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mailchimp state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mailchimp is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=mailchimp
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Mailchimp homepage: https://mailchimp.com
