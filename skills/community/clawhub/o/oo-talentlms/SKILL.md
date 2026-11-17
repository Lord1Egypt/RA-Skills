---
name: oo-talentlms
description: "TalentLMS (talentlms.com). Use this skill for ANY TalentLMS request — reading, creating, updating, and deleting data. Whenever a task involves TalentLMS, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TalentLMS"
  author: "OOMOL"
  version: "1.0.4"
  services: ["talentlms"]
  icon: "https://static.oomol.com/logo/third-party/talentlms.svg"
---

# TalentLMS

Operate **TalentLMS** through your OOMOL-connected account. This skill calls the `talentlms` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TalentLMS. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "talentlms" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "talentlms" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_user` — Create a TalentLMS user with common user fields and optional raw API fields. [write]
- `delete_user` — Delete a TalentLMS user by ID. [destructive]
- `get_branch` — Get a TalentLMS branch by ID.
- `get_category` — Get a TalentLMS category by ID.
- `get_course` — Get a TalentLMS course by ID.
- `get_group` — Get a TalentLMS group by ID.
- `get_user` — Get a TalentLMS user by ID.
- `health_check` — Check whether the configured TalentLMS API domain and API key can reach API v2.
- `list_branches` — List TalentLMS branches with optional API v2 pagination.
- `list_categories` — List TalentLMS categories with optional API v2 pagination.
- `list_courses` — List TalentLMS courses with optional API v2 pagination.
- `list_groups` — List TalentLMS groups with optional API v2 pagination.
- `list_users` — List TalentLMS users with optional API v2 pagination.
- `update_user` — Update a TalentLMS user with common user fields and optional raw API fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TalentLMS state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TalentLMS is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/talentlms
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TalentLMS homepage: https://www.talentlms.com
- API documentation: https://developers.talentlms.io/intro
