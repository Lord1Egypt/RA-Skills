---
name: oo-bitbucket
description: "Bitbucket (bitbucket.org). Use this skill for ANY Bitbucket request — reading, creating, updating, and deleting data. Whenever a task involves Bitbucket, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bitbucket"
  author: "OOMOL"
  version: "1.0.5"
  services: ["bitbucket"]
  icon: "https://static.oomol.com/logo/third-party/bitbucket.svg"
---

# Bitbucket

Operate **Bitbucket** through your OOMOL-connected account. This skill calls the `bitbucket` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bitbucket. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bitbucket" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bitbucket" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `approve_pull_request` — Approve a Bitbucket pull request. [write]
- `create_branch` — Create a branch from a commit hash or existing revision in a Bitbucket repository. [write]
- `create_issue` — Create an issue in a repository that still supports the deprecated Bitbucket issue tracker. [write]
- `create_issue_comment` — Create an issue comment in a repository that still supports the deprecated Bitbucket issue tracker. [write]
- `create_pipeline_variable` — Create a repository-level Bitbucket Pipelines variable. [write]
- `create_pull_request` — Create a pull request in a Bitbucket repository. [write]
- `create_pull_request_comment` — Create a comment on a Bitbucket pull request. [write]
- `decline_pull_request` — Decline a Bitbucket pull request. [destructive]
- `delete_branch` — Delete a branch from a Bitbucket repository. [destructive]
- `delete_pipeline_variable` — Delete a repository-level Bitbucket Pipelines variable. [destructive]
- `delete_repository` — Permanently delete a Bitbucket repository. [destructive]
- `get_branch` — Get a branch in a Bitbucket repository.
- `get_commit` — Get a commit from a Bitbucket repository.
- `get_current_user` — Get the currently authenticated Bitbucket user.
- `get_issue` — Get an issue from a repository that still supports the deprecated Bitbucket issue tracker.
- `get_pipeline` — Get a Pipelines run from a Bitbucket repository.
- `get_pull_request` — Get a pull request from a Bitbucket repository.
- `get_pull_request_merge_task_status` — Get the status of an asynchronous Bitbucket pull request merge task.
- `get_repository` — Get a Bitbucket repository by workspace and repository slug or UUID.
- `get_snippet` — Get a Bitbucket snippet by workspace and encoded snippet ID.
- `get_workspace` — Get a Bitbucket workspace by slug or UUID.
- `list_branches` — List branches in a Bitbucket repository.
- `list_commits` — List commits in a Bitbucket repository, optionally starting from a revision.
- `list_issue_comments` — List issue comments in a repository that still supports the deprecated Bitbucket issue tracker.
- `list_issues` — List issues in a repository that still supports the deprecated Bitbucket issue tracker.
- `list_pipeline_variables` — List repository-level Bitbucket Pipelines variables.
- `list_pipelines` — List Pipelines runs for a Bitbucket repository.
- `list_pull_request_comments` — List comments on a Bitbucket pull request.
- `list_pull_requests` — List pull requests in a Bitbucket repository.
- `list_repositories` — List repositories in a Bitbucket workspace.
- `list_repository_runners` — List Pipelines runners configured for a Bitbucket repository.
- `list_snippets` — List snippets owned by or visible through a Bitbucket workspace.
- `list_tags` — List tags in a Bitbucket repository.
- `list_workspace_members` — List members of a Bitbucket workspace.
- `list_workspace_projects` — List projects in a Bitbucket workspace.
- `list_workspaces` — List workspaces available to the authenticated Bitbucket user.
- `merge_pull_request` — Merge a Bitbucket pull request. [destructive]
- `run_pipeline` — Trigger a Bitbucket Pipelines run for a branch, tag, or commit. [write]
- `stop_pipeline` — Stop a running Bitbucket pipeline. [destructive]
- `update_issue` — Update an issue in a repository that still supports the deprecated Bitbucket issue tracker. [destructive]
- `update_pipeline_variable` — Replace a repository-level Bitbucket Pipelines variable. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bitbucket state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bitbucket is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/bitbucket
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Bitbucket homepage: https://bitbucket.org
- API documentation: https://developer.atlassian.com/cloud/bitbucket/rest/intro/
