---
name: github-repos
description: Work with GitHub repositories, issues, pull requests, commits, branches, releases, and workflows via the GitHub REST and GraphQL APIs. Use this skill when users want to list repositories, inspect issues and PRs, manage branches and commits, create or update issues after confirmation, or trigger and inspect GitHub Actions workflows.
---

# GitHub

![GitHub](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/github.png)

Access GitHub via the GitHub API with OAuth authentication. Manage repositories, issues, pull requests, commits, branches, releases, and workflows.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-repos) for hosted connection flows and credentials so you do not need to configure GitHub API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect GitHub |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect GitHub |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   GitHub API     │
│   (User Chat)   │     │   (OAuth)    │     │   (REST/GraphQL) │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect GitHub    │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ GitHub   │
   │  File    │           │ Auth     │           │ Repos    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for GitHub again."

## Quick Start

```bash
# List repositories for the authenticated user
clawlink_call_tool --tool "github_list_repositories_for_the_authenticated_user" --params '{}'

# Get a specific repository
clawlink_call_tool --tool "github_get_a_repository" --params '{"owner": "owner", "repo": "repo-name"}'

# List issues in a repository
clawlink_call_tool --tool "github_list_issues_for_a_repository" --params '{"owner": "owner", "repo": "repo-name", "state": "open"}'
```

## Authentication

All GitHub tool calls are authenticated automatically by ClawLink using the user's connected GitHub account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every GitHub API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=github and connect GitHub.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `github` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration github
```

**Response:** Returns the live tool catalog for GitHub.

### Reconnect

If GitHub tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=github
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration github`

## Security & Permissions

- Access is scoped to repositories and resources accessible to the connected GitHub account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting issues, closing PRs, removing collaborators) are marked as high-impact and must be confirmed.
- Workflow triggers and deployments affect external systems — always confirm before executing.

## Tool Reference

### Repositories

| Tool | Description | Mode |
|------|-------------|------|
| `github_list_repositories_for_the_authenticated_user` | List all repos for the authenticated user | Read |
| `github_get_a_repository` | Get repository details | Read |
| `github_create_a_repository` | Create a new repository | Write |
| `github_update_a_repository` | Update repository settings | Write |
| `github_delete_a_repository` | Delete a repository | Write |
| `github_list_repository_collaborators` | List repo collaborators | Read |

### Issues

| Tool | Description | Mode |
|------|-------------|------|
| `github_list_issues_for_a_repository` | List issues with filtering | Read |
| `github_get_an_issue` | Get issue details | Read |
| `github_create_an_issue` | Create a new issue | Write |
| `github_update_an_issue` | Update issue fields (labels, assignee, state) | Write |
| `github_add_labels_to_an_issue` | Add labels to an issue | Write |
| `github_add_assignees_to_an_issue` | Add assignees to an issue | Write |

### Pull Requests

| Tool | Description | Mode |
|------|-------------|------|
| `github_list_pull_requests` | List PRs in a repository | Read |
| `github_get_a_pull_request` | Get PR details | Read |
| `github_create_a_pull_request` | Create a new PR | Write |
| `github_update_a_pull_request` | Update PR fields | Write |

### Commits & Branches

| Tool | Description | Mode |
|------|-------------|------|
| `github_list_commits` | List commits in a repository | Read |
| `github_get_a_commit` | Get commit details | Read |
| `github_list_branches` | List branches in a repository | Read |
| `github_create_a_branch` | Create a new branch | Write |

### Workflows

| Tool | Description | Mode |
|------|-------------|------|
| `github_list_repository_workflows` | List workflows in a repo | Read |
| `github_list_workflow_runs` | List workflow runs | Read |
| `github_get_a_workflow_run` | Get workflow run details | Read |
| `github_cancel_workflow_run` | Cancel an in-progress workflow run | Write |

### Releases

| Tool | Description | Mode |
|------|-------------|------|
| `github_list_releases` | List releases in a repository | Read |
| `github_get_a_release` | Get release details | Read |
| `github_create_a_release` | Create a new release | Write |

## Code Examples

### List open issues in a repository

```bash
clawlink_call_tool --tool "github_list_issues_for_a_repository" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "state": "open",
    "sort": "created",
    "direction": "desc"
  }'
```

### Create a new issue

```bash
clawlink_call_tool --tool "github_create_an_issue" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "title": "Bug: Login fails on mobile",
    "body": "Steps to reproduce: 1. Go to login 2. Enter credentials 3. Error shown",
    "labels": ["bug", "high-priority"]
  }'
```

### Add labels to an issue

```bash
clawlink_call_tool --tool "github_add_labels_to_an_issue" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "issue_number": 123,
    "labels": ["needs-review", "bug"]
  }'
```

### Create a pull request

```bash
clawlink_call_tool --tool "github_create_a_pull_request" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "title": "Fix login bug",
    "head": "fix/login-bug",
    "base": "main",
    "body": "Fixes #123 - Login fails on mobile devices"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm GitHub is connected.
2. Call `clawlink_list_tools --integration github` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `github`.
5. If no GitHub tools appear, direct the user to https://claw-link.dev/dashboard?add=github.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List issues → Get issue → Show details            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview issue → User approves     │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- GitHub API rate limits apply. The number of calls depends on the connected account type (free, pro, or enterprise).
- Some tools require specific OAuth scopes. If a tool fails with insufficient scope, verify the connection has the right permissions.
- Repository names must use `owner/repo` format for owner and repo parameters.
- Issues and PRs use different numbering systems within the same repository.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration github`. |
| Missing connection | GitHub is not connected. Direct the user to https://claw-link.dev/dashboard?add=github. |
| `404 Not Found` | Repository, issue, or PR does not exist. Verify owner, repo, and number. |
| `403 Forbidden` | Rate limit exceeded or insufficient permissions. |
| `422 Unprocessable` | Invalid request body or missing required fields. Verify tool schema. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `github`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-repos)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [GitLab Repos](https://clawhub.ai/hith3sh/gitlab-repos) — For GitLab project management
- [GitHub Triage](https://clawhub.ai/hith3sh/github-triage-workflow) — For GitHub issue triage workflows

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-repos)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)