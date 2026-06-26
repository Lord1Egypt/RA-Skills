---
name: jira-task-manager
description: "Jira automation for JiraATX (project DS). Create, update, comment, transition issues, list To Do tasks, sync repo, execute tasks end-to-end. Triggers: DS-XXX, Jira task, work on issue, list my tasks."
metadata: {"clawdbot":{"emoji":"🎯","requires":{"env":["JIRA_API_TOKEN","JIRA_EMAIL"]},"primaryEnv":"JIRA_API_TOKEN"}}
---

# Jira Task Manager Skill

This skill automates common Jira operations.

## Resource Locations

- **Jira Configuration**: Refer to [references/jira.md](references/jira.md) for Jira URL, credentials, and Google Drive folder ID.
- **Scripts**: All automation logic resides in `scripts/`.

## Standard Workflows

### 1. List To Do Issues
`scripts/get_my_todo_issues.py` — Returns issues assigned to `xwang@attrix.ca` in project DS with status "To Do".

### 2. Get Issue Details
`scripts/get_issue_description.py <ISSUE_KEY>` — Returns summary and full description.

### 3. Create Issue
`scripts/create_issue.py` — Requires: Project Key, Issue Type, Summary. Optional: description template from Google Drive, Priority, Assignee.

### 4. Update Issue
`scripts/update_issue.py` — Requires: Issue Key, field, new value. Uses transition IDs for status changes.

### 5. Add Comment
`scripts/add_comment.py` — Requires: Issue Key, comment text. Optional: attachment from Google Drive.

### 6. Get Issue Info
`scripts/get_issue_info.py <ISSUE_KEY>` — Returns current status, assignee, and metadata.

### 7. Prepare Repo
`scripts/sync_repo.py <ISSUE_KEY>` — Finds repo via `references/repos.json`, fetches remote, checks out or creates `feature/<ISSUE_KEY>` branch. Reports `repo_path` and `branch`. Optional: `--branch <name>` to force branch name.

### 8. Full Task Execution Flow (End-to-End)
**Trigger**: "work on DS-XXX", "fix DS-XXX", "pick up DS-XXX". Follow steps in order without asking unless blocked.

1. `get_issue_info.py` → summarize task, acceptance criteria, subtasks.
2. **Confirm with user** — wait for explicit approval before proceeding.
3. `sync_repo.py <ISSUE_KEY>` → report `repo_path` and `branch`. All edits are relative to `repo_path`.
4. Read relevant source files before making any changes.
5. Implement changes. No per-edit confirmations unless scope is ambiguous.
6. `run_tests.py --issue <ISSUE_KEY>` → fix failures, re-run until passing.
7. Report: what changed, test results, branch. **Stop and wait** — do not merge, push, or transition status until user approves.

### 9. React/Zustand State Persistence Bugs
**Trigger**: Field reverts after navigation or re-entering a detail page.
- Sync field updates back to the global store immediately after a successful mutation.
- Keep per-entity overrides (keyed by entity id) and merge after re-fetch rather than caching the whole object.
- Audit `useMemo`/`useCallback`/`useEffect` deps for stale closures. Use selector-based Zustand subscriptions for high-traffic components.
- Apply the smallest safe fix — avoid broadening cache scope unnecessarily.

## Important Notes
- All Jira API interactions will be performed using the credentials stored in `references/jira.md`.
- Repo-to-issue mapping and test commands are configured in [references/repos.json](references/repos.json).
- For security, ensure `JIRA_API_TOKEN` is kept confidential.
