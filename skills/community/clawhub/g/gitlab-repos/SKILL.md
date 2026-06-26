---
name: gitlab-repos
description: Work with GitLab projects, issues, merge requests, commits, branches, pipelines, and groups via the GitLab API. Use this skill when users want to list projects and groups, inspect issues and MRs, review commits and pipelines, create or update issues after confirmation, or manage project members and CI/CD pipelines in GitLab.
---

# GitLab

![GitLab](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/gitlab.svg)

Access GitLab via the GitLab API with OAuth authentication. Manage projects, issues, merge requests, commits, branches, pipelines, and groups.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=gitlab-repos) for hosted connection flows and credentials so you do not need to configure GitLab API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect GitLab |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect GitLab |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   GitLab API     │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect GitLab    │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ GitLab   │
   │  File    │           │ Auth     │           │ Projects │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for GitLab again."

## Quick Start

```bash
# List projects for the authenticated user
clawlink_call_tool --tool "gitlab_get_projects" --params '{}'

# Get a specific project
clawlink_call_tool --tool "gitlab_get_project" --params '{"id": "owner/repo-name"}'

# List project issues
clawlink_call_tool --tool "gitlab_list_project_issues" --params '{"id": "owner/repo-name", "state": "opened"}'
```

## Authentication

All GitLab tool calls are authenticated automatically by ClawLink using the user's connected GitLab account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every GitLab API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=gitlab and connect GitLab.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `gitlab` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration gitlab
```

**Response:** Returns the live tool catalog for GitLab.

### Reconnect

If GitLab tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=gitlab
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration gitlab`

## Security & Permissions

- Access is scoped to projects and resources accessible to the connected GitLab account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (deleting projects, archiving, removing members) are marked as high-impact and must be confirmed.
- CI/CD pipeline operations affect build and deployment systems — confirm before triggering or canceling.

## Tool Reference

### Projects

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_get_projects` | List all projects accessible to the authenticated user | Read |
| `gitlab_get_project` | Get project details by ID or path | Read |
| `gitlab_create_project` | Create a new project | Write |
| `gitlab_archive_project` | Archive a project (read-only) | Write |
| `gitlab_delete_project` | Delete a project permanently | Write |
| `gitlab_list_project_pipelines` | List CI/CD pipelines for a project | Read |

### Groups

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_get_groups` | List all groups | Read |
| `gitlab_get_group` | Get group details | Read |
| `gitlab_create_group` | Create a new group | Write |
| `gitlab_list_group_members` | List direct members of a group | Read |
| `gitlab_list_all_group_members` | List all members (direct, inherited, invited) | Read |

### Issues

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_list_project_issues` | List issues with filtering (state, labels, assignee) | Read |
| `gitlab_get_project_issue` | Get issue details | Read |
| `gitlab_create_project_issue` | Create a new issue | Write |
| `gitlab_update_project_issue` | Update issue fields (title, description, labels, state) | Write |

### Merge Requests

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_get_project_merge_requests` | List merge requests | Read |
| `gitlab_get_project_merge_request` | Get MR details | Read |
| `gitlab_get_merge_request_notes` | Get comments on an MR | Read |

### Commits & Branches

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_list_repository_commits` | List commits in a repository | Read |
| `gitlab_get_single_commit` | Get commit details | Read |
| `gitlab_get_repository_branches` | List branches | Read |
| `gitlab_create_repository_branch` | Create a new branch | Write |

### Members

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_list_all_project_members` | List all project members | Read |
| `gitlab_import_project_members` | Import members from one project to another | Write |

### User Status

| Tool | Description | Mode |
|------|-------------|------|
| `gitlab_get_user_status` | Get current user's GitLab status | Read |
| `gitlab_set_user_status` | Set current user's status message | Write |

## Code Examples

### List project issues

```bash
clawlink_call_tool --tool "gitlab_list_project_issues" \
  --params '{
    "id": "owner/repo-name",
    "state": "opened",
    "per_page": 20
  }'
```

### Create a new issue

```bash
clawlink_call_tool --tool "gitlab_create_project_issue" \
  --params '{
    "id": "owner/repo-name",
    "title": "Bug: Login fails on mobile",
    "description": "Steps to reproduce: 1. Go to login 2. Enter credentials 3. Error shown",
    "labels": ["bug", "priority::high"]
  }'
```

### Create a new branch

```bash
clawlink_call_tool --tool "gitlab_create_repository_branch" \
  --params '{
    "id": "owner/repo-name",
    "branch": "feature/new-feature",
    "ref": "main"
  }'
```

### List pipeline jobs

```bash
clawlink_call_tool --tool "gitlab_list_pipeline_jobs" \
  --params '{
    "id": "owner/repo-name",
    "pipeline_id": 123
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm GitLab is connected.
2. Call `clawlink_list_tools --integration gitlab` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `gitlab`.
5. If no GitLab tools appear, direct the user to https://claw-link.dev/dashboard?add=gitlab.

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

- GitLab project IDs can be numeric (`12345`) or path-based (`owner/repo-name`).
- GitLab uses scoped labels (`bug`, `priority::high`) rather than simple strings.
- Merge request IIDs are different from issue IIDs — they are numbered separately.
- Pipeline status values: `pending`, `running`, `success`, `failed`, `canceled`, `skipped`.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration gitlab`. |
| Missing connection | GitLab is not connected. Direct the user to https://claw-link.dev/dashboard?add=gitlab. |
| `404 Not Found` | Project, issue, or MR does not exist. Verify the ID or path. |
| `403 Forbidden` | Insufficient permissions for the requested operation. |
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

1. Ensure the integration slug is exactly `gitlab`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [GitLab API Documentation](https://docs.gitlab.com/api/)
- [GitLab REST API](https://docs.gitlab.com/api/rest.html)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=gitlab-repos)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [GitHub Repos](https://clawhub.ai/hith3sh/github-repos) — For GitHub repository management
- [GitHub Triage](https://clawhub.ai/hith3sh/github-triage-workflow) — For GitHub issue triage workflows

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=gitlab-repos)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)