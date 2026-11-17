---
name: "jira-reader"
description: "Read-only Jira lookup commands, including JSON task-directory output."
metadata:
  version: 0.4.0
  tags: ["jira", "atlassian", "readonly", "issues", "javascript", "reader"]
  openclaw:
    primaryEnv: JIRA_ACCESS_TOKEN
allowed-tools:
  - exec
---

# Jira Reader

Use for read-only Jira Cloud lookups with scoped Atlassian API tokens: issue details, JQL searches, project metadata, recent activity, assigned open work, and current-user task directories.

## Requirements

- Node.js 18+.
- Scoped Atlassian API token with Jira read scopes.
- Environment: `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_ACCESS_TOKEN`; optional `JIRA_PROJECT` and `JIRA_CLOUD_ID`.
- The helper loads `.env`; set `JIRA_ENV_FILE` for another file. Existing process values win.

Never print or commit tokens. Keep every operation read-only.

## Commands

```bash
node scripts/jira-reader.mjs me
node scripts/jira-reader.mjs project
node scripts/jira-reader.mjs issue PROJ-123
node scripts/jira-reader.mjs search --jql 'project = PROJ ORDER BY updated DESC' --max 10
node scripts/jira-reader.mjs recent --max 10
node scripts/jira-reader.mjs my-open --max 20
node scripts/jira-reader.mjs my-tasks-directory --max 100
node scripts/jira-reader.mjs my-tasks-directory --project PROJ --max 50
```

`my-tasks-directory` queries all open tasks assigned to `currentUser()` unless `--project` is supplied. It emits JSON grouped as `directory[projectKey][statusName]`, with compact issue summaries at the leaves. A `truncated` flag reports when `--max` omits results.

Treat open work as `statusCategory != Done`.

## Validation

```bash
node scripts/jira-reader.mjs --version
node scripts/jira-reader.mjs me
node scripts/jira-reader.mjs my-tasks-directory --max 10
```
