---
name: oo-bug-herd
description: "BugHerd (bugherd.com). Use this skill for ANY BugHerd request — reading, creating, and updating data. Whenever a task involves BugHerd, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "BugHerd"
  author: "OOMOL"
  version: "1.0.1"
  services: ["bug_herd"]
  icon: "https://static.oomol.com/logo/third-party/bug_herd.png"
---

# BugHerd

Operate **BugHerd** through your OOMOL-connected account. This skill calls the `bug_herd` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected BugHerd. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bug_herd" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bug_herd" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_attachment_from_url` — Create a BugHerd task attachment from a publicly accessible file URL. [write]
- `create_comment` — Create a comment on a BugHerd task. [write]
- `create_project` — Create a BugHerd project with the required project name and website URL. [write]
- `create_task` — Create a BugHerd task in a project. [write]
- `get_project` — Retrieve full details for a BugHerd project.
- `get_task` — Retrieve a BugHerd task by project ID and global task ID.
- `list_active_projects` — List active BugHerd projects in the organization.
- `list_attachments` — List file attachments on a BugHerd task.
- `list_comments` — List comments on a BugHerd task.
- `list_project_tasks` — List BugHerd tasks for a project with optional server-side filters.
- `list_projects` — List all BugHerd projects in the organization.
- `show_organization` — Retrieve top-level details about the authenticated BugHerd organization.
- `update_project` — Update settings for an existing BugHerd project. [write]
- `update_task` — Update mutable fields on a BugHerd task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change BugHerd state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — BugHerd is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=bug_herd
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- BugHerd homepage: https://bugherd.com/
