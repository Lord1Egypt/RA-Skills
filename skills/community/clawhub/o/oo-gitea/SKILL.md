---
name: oo-gitea
description: "Gitea (about.gitea.com). Use this skill for ANY Gitea request — reading, creating, updating, and deleting data. Whenever a task involves Gitea, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gitea"
  author: "OOMOL"
  version: "1.0.7"
  services: ["gitea"]
  icon: "https://static.oomol.com/logo/third-party/Gitea.svg"
---

# Gitea

Operate **Gitea** through your OOMOL-connected account. This skill calls the `gitea` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gitea. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gitea" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gitea" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_collaborator` — Add a collaborator to a Gitea repository. [write]
- `add_issue_labels` — Add labels to a Gitea issue. [write]
- `check_pull_request_merged` — Check whether a Gitea pull request has been merged.
- `clear_issue_labels` — Remove all labels from a Gitea issue. [destructive]
- `create_branch` — Create a new branch in a Gitea repository. [write]
- `create_commit_status` — Create a commit status for a commit SHA in a Gitea repository. [write]
- `create_file` — Create a file in a Gitea repository. [write]
- `create_issue` — Create an issue in a Gitea repository. [write]
- `create_issue_comment` — Create a comment on a Gitea issue. [write]
- `create_label` — Create a label in a Gitea repository. [write]
- `create_milestone` — Create a milestone in a Gitea repository. [write]
- `create_pull_request` — Create a pull request in a Gitea repository. [write]
- `create_pull_request_review` — Create a review for a Gitea pull request. [write]
- `create_release` — Create a release in a Gitea repository. [write]
- `create_repository` — Create a repository for the authenticated Gitea user. [write]
- `create_repository_hook` — Create a webhook in a Gitea repository. [write]
- `create_repository_key` — Create a deploy key in a Gitea repository. [write]
- `create_tag` — Create a tag in a Gitea repository. [write]
- `delete_branch` — Delete a branch of a Gitea repository. [destructive]
- `delete_file` — Delete a file from a Gitea repository. [destructive]
- `delete_issue_comment` — Delete a comment from a Gitea issue. [destructive]
- `delete_label` — Delete a label from a Gitea repository. [destructive]
- `delete_milestone` — Delete a milestone from a Gitea repository. [destructive]
- `delete_pull_request_review` — Delete a review from a Gitea pull request. [destructive]
- `delete_release` — Delete a release from a Gitea repository. [destructive]
- `delete_repository` — Delete a Gitea repository permanently. [destructive]
- `delete_repository_hook` — Delete a webhook from a Gitea repository. [destructive]
- `delete_repository_key` — Delete a deploy key from a Gitea repository. [destructive]
- `delete_tag` — Delete a tag from a Gitea repository. [destructive]
- `dismiss_pull_request_review` — Dismiss a review on a Gitea pull request. [destructive]
- `fork_repository` — Fork a Gitea repository to the authenticated user or an organization. [write]
- `get_branch` — Get a branch of a Gitea repository by name.
- `get_collaborator_permission` — Get the permission level of a Gitea repository collaborator.
- `get_commit` — Get a commit of a Gitea repository by SHA.
- `get_current_user` — Get the current authenticated Gitea user profile.
- `get_issue` — Get a Gitea issue by repository and issue number.
- `get_label` — Get a label of a Gitea repository by ID.
- `get_milestone` — Get a milestone of a Gitea repository by ID.
- `get_organization` — Get a Gitea organization by name.
- `get_pull_request` — Get a Gitea pull request by repository and pull request number.
- `get_release` — Get a release of a Gitea repository by ID.
- `get_repository` — Get metadata for a Gitea repository by owner and name.
- `get_repository_contents` — Get the contents or metadata of a file or directory in a Gitea repository.
- `get_repository_hook` — Get a webhook of a Gitea repository by ID.
- `get_repository_key` — Get a deploy key of a Gitea repository by ID.
- `get_tag` — Get a tag of a Gitea repository by name.
- `list_branches` — List branches of a Gitea repository.
- `list_collaborators` — List collaborators of a Gitea repository.
- `list_commit_statuses` — List commit statuses for a commit SHA or ref in a Gitea repository.
- `list_commits` — List commits of a Gitea repository.
- `list_issue_assignees` — List users that can be assigned to issues in a Gitea repository.
- `list_issue_comments` — List comments under a Gitea issue.
- `list_issue_labels` — List labels attached to a Gitea issue.
- `list_milestones` — List milestones of a Gitea repository.
- `list_my_organizations` — List organizations the authenticated Gitea user belongs to.
- `list_my_repositories` — List repositories owned by the authenticated Gitea user.
- `list_organization_members` — List members of a Gitea organization.
- `list_organization_repositories` — List repositories of a Gitea organization.
- `list_pull_request_commits` — List commits of a Gitea pull request.
- `list_pull_request_files` — List files changed by a Gitea pull request.
- `list_pull_request_review_comments` — List review comments of a Gitea pull request review.
- `list_pull_request_reviews` — List reviews for a Gitea pull request.
- `list_pull_requests` — List pull requests in a Gitea repository.
- `list_releases` — List releases of a Gitea repository.
- `list_repository_hooks` — List webhooks of a Gitea repository.
- `list_repository_issues` — List issues in a Gitea repository. Pull requests are filtered out.
- `list_repository_keys` — List deploy keys of a Gitea repository.
- `list_repository_labels` — List labels of a Gitea repository.
- `list_repository_stargazers` — List stargazers of a Gitea repository.
- `list_repository_topics` — List topics of a Gitea repository.
- `list_repository_watchers` — List watchers of a Gitea repository.
- `list_tags` — List tags of a Gitea repository.
- `merge_pull_request` — Merge a Gitea pull request. [destructive]
- `remove_collaborator` — Remove a collaborator from a Gitea repository. [destructive]
- `remove_issue_label` — Remove a label from a Gitea issue. [destructive]
- `remove_pull_request_reviewers` — Remove requested reviewers from a Gitea pull request. [destructive]
- `replace_issue_labels` — Replace all labels of a Gitea issue. [destructive]
- `request_pull_request_reviewers` — Request reviews for a Gitea pull request from users or teams. [write]
- `search_repositories` — Search Gitea repositories by keyword with optional repository filters.
- `star_repository` — Star a Gitea repository for the authenticated user. [write]
- `submit_pull_request_review` — Submit a pending Gitea pull request review. [write]
- `unstar_repository` — Remove a star from a Gitea repository for the authenticated user. [destructive]
- `update_file` — Update or create a file in a Gitea repository. [write]
- `update_issue` — Update an issue in a Gitea repository. [write]
- `update_issue_comment` — Update a comment on a Gitea issue. [write]
- `update_label` — Update a label of a Gitea repository. [write]
- `update_milestone` — Update a milestone of a Gitea repository. [write]
- `update_pull_request` — Update a Gitea pull request title, body, state, base branch, or review assignments. [write]
- `update_pull_request_branch` — Update the head branch of a Gitea pull request to the latest base branch. [write]
- `update_release` — Update a release of a Gitea repository. [write]
- `update_repository` — Update settings of a Gitea repository. [write]
- `update_repository_hook` — Update a webhook of a Gitea repository. [write]
- `update_repository_topics` — Replace all topics of a Gitea repository. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gitea state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gitea is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gitea
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gitea homepage: https://about.gitea.com/products/gitea/
- API documentation: https://docs.gitea.com/development/api-usage
