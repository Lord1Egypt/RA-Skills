---
name: oo-github
description: "GitHub (github.com). Use this skill for ANY GitHub request — reading, creating, updating, and deleting data. Whenever a task involves GitHub, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "GitHub"
  author: "OOMOL"
  version: "1.0.2"
  services: ["github"]
  icon: "https://static.oomol.com/logo/third-party/github.png"
---

# GitHub

Operate **GitHub** through your OOMOL-connected account. This skill calls the `github` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected GitHub. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "github" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "github" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_issue_assignees` — Add assignees to a GitHub issue. [write]
- `add_issue_labels` — Add labels to a GitHub issue. [write]
- `check_pull_request_merged` — Check whether a GitHub pull request has been merged.
- `clear_issue_labels` — Remove all labels from a GitHub issue. [destructive]
- `compare_commits` — Compare two commit references in a GitHub repository.
- `create_commit_status` — Create a commit status for a GitHub commit SHA. [write]
- `create_issue` — Create an issue in a GitHub repository. [write]
- `create_issue_comment` — Create a comment on a GitHub issue. [write]
- `create_label` — Create a label in a GitHub repository. [write]
- `create_or_update_file` — Create or update a repository file through the GitHub contents API. Writing under .github/workflows may require GitHub workflow scope. [write]
- `create_pull_request` — Create a pull request in a GitHub repository. [write]
- `create_pull_request_review` — Create a review for a GitHub pull request, optionally with inline comments. [write]
- `create_pull_request_review_comment` — Create a review comment on a GitHub pull request diff. [write]
- `create_ref` — Create a Git reference in a GitHub repository. [write]
- `create_release` — Create a release in a GitHub repository. [write]
- `create_repository` — Create a repository for the authenticated GitHub user. [write]
- `delete_file` — Delete a repository file through the GitHub contents API. Deleting under .github/workflows may require GitHub workflow scope. [destructive]
- `delete_repository` — Delete a GitHub repository by owner and name. [destructive]
- `get_branch` — Get a GitHub branch by name.
- `get_commit` — Get a commit by SHA in a GitHub repository.
- `get_commit_statuses` — List statuses for a commit reference in reverse chronological order.
- `get_current_user` — Get the current authenticated GitHub user profile.
- `get_file_contents` — Read a repository file and return both base64 and decoded text when available.
- `get_issue` — Get a GitHub issue by number.
- `get_latest_release` — Get the latest published release for a GitHub repository.
- `get_pull_request` — Get a GitHub pull request by number.
- `get_release` — Get a GitHub release by numeric id.
- `get_release_by_tag` — Get a GitHub release by tag name.
- `get_repository` — Get metadata for a GitHub repository by owner and name.
- `get_workflow_run` — Get a GitHub workflow run by id.
- `list_authenticated_user_events` — List activity events for a GitHub user and include private events when the authenticated credential belongs to that user.
- `list_authenticated_user_received_events` — List received activity events for a GitHub user and include private events when the authenticated credential belongs to that user.
- `list_branches` — List branches in a GitHub repository.
- `list_check_runs_for_ref` — List GitHub check runs for a commit SHA, branch, or tag.
- `list_commits` — List commits in a GitHub repository with optional branch, path, author, and date filters.
- `list_directory_contents` — List entries under a repository directory path. Empty path means repository root.
- `list_issue_comments` — List comments under a GitHub issue.
- `list_issue_events` — List events for a GitHub issue.
- `list_issue_labels` — List labels applied to a GitHub issue.
- `list_issue_timeline_events` — List timeline events for a GitHub issue.
- `list_my_repositories` — List repositories visible to the authenticated GitHub user.
- `list_public_events` — List the global public GitHub event feed.
- `list_pull_request_commits` — List commits on a GitHub pull request.
- `list_pull_request_files` — List files changed in a GitHub pull request.
- `list_pull_request_requested_reviewers` — List requested reviewers on a GitHub pull request.
- `list_pull_request_review_comments` — List review comments on a GitHub pull request.
- `list_pull_request_reviews` — List reviews for a GitHub pull request.
- `list_pull_requests` — List pull requests for a GitHub repository.
- `list_pull_requests_associated_with_commit` — List pull requests associated with a commit SHA.
- `list_release_assets` — List assets attached to a GitHub release.
- `list_releases` — List releases for a GitHub repository.
- `list_repository_events` — List recent GitHub events for a repository.
- `list_repository_issue_events` — List issue events across a GitHub repository.
- `list_repository_issues` — List issues for a GitHub repository. Pull requests are filtered out from the response.
- `list_repository_labels` — List labels available in a GitHub repository.
- `list_repository_workflows` — List workflows configured in a GitHub repository.
- `list_user_public_events` — List public GitHub events performed by a user.
- `list_user_received_public_events` — List public GitHub events received by a user.
- `list_workflow_run_jobs` — List jobs for a GitHub workflow run.
- `list_workflow_runs` — List GitHub workflow runs for a repository.
- `lock_issue` — Lock a GitHub issue conversation. [write]
- `merge_branch` — Merge one branch into another in a GitHub repository. [write]
- `merge_pull_request` — Merge a GitHub pull request. [write]
- `remove_issue_assignees` — Remove assignees from a GitHub issue. [destructive]
- `remove_issue_label` — Remove one label from a GitHub issue. [destructive]
- `remove_pull_request_reviewers` — Remove requested reviewers from a GitHub pull request. [destructive]
- `rename_branch` — Rename a branch in a GitHub repository. [write]
- `reply_pull_request_review_comment` — Reply to a top-level GitHub pull request review comment. [write]
- `request_pull_request_reviewers` — Request reviewers on a GitHub pull request. [write]
- `rerequest_check_run` — Re-request a GitHub check run. [write]
- `rerequest_check_suite` — Re-request a GitHub check suite. [write]
- `rerun_workflow` — Re-run a GitHub Actions workflow run. [write]
- `search_code` — Search GitHub code with GitHub search syntax.
- `search_commits` — Search GitHub commits by commit-message text and qualifiers.
- `search_issues_and_pull_requests` — Search GitHub issues and pull requests with raw GitHub search syntax or structured filters close to Composio pull-request search.
- `search_labels` — Search labels within a GitHub repository by repository id and query.
- `search_repositories` — Search GitHub repositories with GitHub search syntax.
- `search_topics` — Search GitHub topics with GitHub search syntax.
- `search_users` — Search GitHub users with GitHub search syntax.
- `set_issue_labels` — Replace all labels on a GitHub issue. [write]
- `submit_pull_request_review` — Submit a pending GitHub pull request review. [write]
- `sync_fork_branch_with_upstream` — Sync a fork branch with its upstream branch. [write]
- `unlock_issue` — Unlock a GitHub issue conversation. [write]
- `update_issue` — Update a GitHub issue by number. [write]
- `update_pull_request` — Update a GitHub pull request title, body, state, base branch, or maintainer-can-modify flag. [write]
- `update_pull_request_branch` — Update a GitHub pull request branch with the latest base branch changes. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change GitHub state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — GitHub is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=github
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- GitHub homepage: https://github.com
