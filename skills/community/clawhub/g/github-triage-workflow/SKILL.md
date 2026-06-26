---
name: github-triage
description: Review GitHub repositories, group issues and pull requests by urgency, and take safe triage actions (add labels, comment, propose closure) after confirmation. Use this skill when users want help reviewing, sorting, and acting on GitHub issues and PRs without manually navigating between pages — groups items by urgency, proposes next actions, and applies safe triage operations after approval.
---

# GitHub Triage

![GitHub Triage](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/github.png)

Review GitHub repositories, group issues and pull requests by urgency, and take safe triage actions after confirmation.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-triage-workflow) for hosted GitHub access so the user does not need separate API setup.

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
   │  File    │           │ Auth     │           │ Issues   │
   └──────────┘           └──────────┘           └──────────┘
```

## Good Trigger Phrases

- "Triage my GitHub issues"
- "Review open PRs and tell me what needs attention"
- "Find stale GitHub issues and propose actions"
- "Summarize what needs maintainer action in this repo"
- "Label and comment on these issues after I confirm"

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for GitHub triage again."

## Quick Start

```bash
# List open issues in a repository
clawlink_call_tool --tool "github_list_issues_for_a_repository" \
  --params '{"owner": "owner", "repo": "repo-name", "state": "open", "sort": "created", "direction": "desc"}'

# Get a specific issue
clawlink_call_tool --tool "github_get_an_issue" \
  --params '{"owner": "owner", "repo": "repo-name", "issue_number": 123}'
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

## Triage Workflow

### 1. Define the Triage Scope

Ask for:
- repo or org
- issues, pull requests, or both
- time range if needed
- what counts as urgent
- whether the user wants only a report or also wants actions applied

If the user is vague, default to a report first.

### 2. Gather the Current State

Use GitHub read tools first to inspect:
- open issues
- open pull requests
- recent comments
- labels
- review status
- failed workflows
- stale items

Do not jump into writing comments or changing labels before you have a clear picture.

### 3. Group Items into Clear Buckets

A good triage summary usually groups items into:
- needs reply
- needs review
- blocked
- stale
- merge-ready
- failing CI
- low-priority backlog

Explain why each item belongs in that bucket.

### 4. Propose Actions Before Making Changes

Examples:
- add or normalize labels
- leave a maintainer follow-up comment
- identify issues safe to close
- summarize PRs that need review
- flag failing workflow runs

Prefer a short action plan before editing anything.

### 5. Discover the Live GitHub Tools

1. Call `clawlink_list_integrations` to confirm GitHub is connected.
2. Call `clawlink_list_tools` with integration `github`.
3. If the exact action tool is unclear, call `clawlink_search_tools` with short queries such as `list issues`, `comment issue`, `update labels`, or `pull requests`.
4. Call `clawlink_describe_tool` before any write or unfamiliar operation.
5. Use the returned schema and guidance as the source of truth.

### 6. Preview and Confirm Writes

For any write action:
1. Show the exact intended action first.
2. Use `clawlink_preview_tool` when available.
3. Ask for confirmation before commenting, relabeling, closing, reopening, or editing metadata.
4. Execute with `clawlink_call_tool` only after confirmation.

## Triage Operations

### Read Operations (Safe — no confirmation needed for read-only triage)

| Tool | Description |
|------|-------------|
| `github_list_issues_for_a_repository` | List issues with filtering by state, labels, assignee |
| `github_get_an_issue` | Get issue details, body, comments |
| `github_list_pull_requests` | List PRs with filtering |
| `github_get_a_pull_request` | Get PR details, review status |
| `github_list_repository_workflows` | List CI/CD workflows |
| `github_list_workflow_runs` | List recent workflow runs |
| `github_get_a_commit` | Inspect commit details |

### Write Operations (Require confirmation before executing)

| Tool | Description | Confirmation |
|------|-------------|--------------|
| `github_add_labels_to_an_issue` | Add labels to categorize issues | Confirm |
| `github_add_assignees_to_an_issue` | Assign users to issues | Confirm |
| `github_create_an_issue` | Create a new issue for triaged items | Confirm |
| `github_add_a_comment_to_an_issue` | Post a comment on an issue | Confirm |
| `github_update_an_issue` | Close, reopen, or update issue fields | Confirm |

## Code Examples

### List and triage open issues

```bash
clawlink_call_tool --tool "github_list_issues_for_a_repository" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "state": "open",
    "sort": "created",
    "direction": "desc",
    "per_page": 50
  }'
```

### Get issue details for triage assessment

```bash
clawlink_call_tool --tool "github_get_an_issue" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "issue_number": 123
  }'
```

### Add triage labels after confirmation

```bash
clawlink_call_tool --tool "github_add_labels_to_an_issue" \
  --params '{
    "owner": "owner",
    "repo": "repo-name",
    "issue_number": 123,
    "labels": ["triage", "needs-review"]
  }'
```

## Good Workflow Behavior

- Prefer read-first triage and short reports before writes.
- Quote or summarize the evidence behind recommendations.
- If a repo has many items, start with the most urgent or the top 10.
- Avoid aggressive closure suggestions unless the repo norms are clear.
- If there is uncertainty, propose a draft comment instead of posting immediately.

## Rules

- Always use ClawLink tools for GitHub actions. Do not ask for separate GitHub credentials.
- Do not invent GitHub tool names or schemas. Use the live ClawLink catalog in the current turn.
- Ask for confirmation before comments, label changes, issue closure, metadata edits, or other writes.
- Prefer reporting and recommendation before taking triage actions.
- If GitHub is not connected, direct the user to https://claw-link.dev/dashboard?add=github.

## Example Prompts

- Review open issues in this repo and group them by urgency.
- Triage my pull requests and tell me which ones need review, which are blocked, and which are merge-ready.
- Find stale issues in this repo, draft comments for them, and wait for my confirmation.
- Check the last 20 issues in this repository and propose labels for each one.

## Resources

- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-triage-workflow)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=github-triage-workflow)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)