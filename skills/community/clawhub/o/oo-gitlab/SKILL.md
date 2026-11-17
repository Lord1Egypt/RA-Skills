---
name: oo-gitlab
description: "GitLab (gitlab.com). Use this skill for ANY GitLab request — reading, creating, updating, and deleting data. Whenever a task involves GitLab, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "GitLab"
  author: "OOMOL"
  version: "1.0.8"
  services: ["gitlab"]
  icon: "https://static.oomol.com/logo/third-party/gitlab.svg"
---

# GitLab

Operate **GitLab** through your OOMOL-connected account. This skill calls the `gitlab` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected GitLab. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gitlab" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gitlab" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_issue_note` — Post a comment on a GitLab issue. [write]
- `create_merge_request` — Create a GitLab merge request. [write]
- `create_merge_request_note` — Post a comment on a GitLab merge request. The comment is not attached to a line of the diff. [write]
- `create_project` — Create a new GitLab project owned by the authenticated user. [write]
- `create_project_issue` — Create a new issue in a GitLab project. [write]
- `delete_project` — Mark a GitLab project for deletion. [destructive]
- `delete_project_issue` — Delete a GitLab project issue. [destructive]
- `get_current_user` — Get the current authenticated GitLab user profile.
- `get_merge_request` — Get a single merge request from a GitLab project by its internal merge request ID.
- `get_project` — Get a GitLab project by numeric ID or URL-encoded path with namespace.
- `get_project_issue` — Get a single issue from a GitLab project by its internal issue ID.
- `list_issue_notes` — List the notes (comments and system activity) on a GitLab issue, to read a thread before answering it.
- `list_merge_request_notes` — List the notes (comments and system activity) on a GitLab merge request, to read a thread before answering it.
- `list_project_issues` — List issues for a GitLab project with common state, label, assignee, and search filters.
- `list_project_merge_requests` — List merge requests for a GitLab project with state, branch, search, and pagination filters.
- `list_projects` — List GitLab projects visible to the authenticated personal access token, with optional search and membership filters.
- `merge_merge_request` — Accept and merge a GitLab merge request. [write]
- `update_merge_request` — Update a GitLab merge request. [write]
- `update_project` — Update basic settings for an existing GitLab project. [write]
- `update_project_issue` — Update a GitLab project issue, including its title, labels, assignees, or state. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change GitLab state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — GitLab is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gitlab
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- GitLab homepage: https://gitlab.com
- API documentation: https://docs.gitlab.com/api/rest/authentication/
