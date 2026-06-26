---
name: gitlab-auto-review
description: >
  Automated AI code review for GitLab Merge Requests via polling.
  Periodically checks for open MRs, reviews code diffs for security vulnerabilities,
  bugs, and best practices, then posts inline comments and a summary note on GitLab.
  Supports project-level custom review rules via `.gitlab-review-prompt.md`.
  Use when: setting up MR code review, configuring GitLab review automation,
  checking MR review status, or troubleshooting GitLab MR review issues.
metadata:
  openclaw:
    requires:
      bins: ["node"]
      env: ["GITLAB_URL", "GITLAB_TOKEN"]
    primaryEnv: "GITLAB_TOKEN"
---

# GitLab MR Code Review

Polling-based automated code review for GitLab MRs.

## Architecture

```
Cron (*/2 * * * *) → gitlab-api.js list-mrs → skip reviewed → fetch diff → AI review → post comments/note
```

- No webhook server — pure polling
- Reviewed MRs tracked in `{baseDir}/mr-reviewed.json`

## Setup

1. Create `{baseDir}/.env` with your GitLab credentials:
   ```
   GITLAB_URL=https://gitlab.example.com
   GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
   ```
   The script auto-loads this file. Environment variables take precedence (won't be overwritten if already set).
2. Test: `node {baseDir}/scripts/gitlab-api.js get-version`
3. Install cron worker — see [references/cron-setup.md](references/cron-setup.md) for the full command

## API Script Reference

```bash
node {baseDir}/scripts/gitlab-api.js get-version                              # Test connection
node {baseDir}/scripts/gitlab-api.js list-mrs                                 # List open MRs
node {baseDir}/scripts/gitlab-api.js list-mrs --project <project_path>        # Filter by project
node {baseDir}/scripts/gitlab-api.js get-changes <project_id> <mr_iid>        # Fetch MR diff
node {baseDir}/scripts/gitlab-api.js get-file <project_id> <branch> <path>    # Fetch file content
node {baseDir}/scripts/gitlab-api.js post-comment --file <json> <pid> <iid>   # Inline comment (use --file!)
node {baseDir}/scripts/gitlab-api.js post-note <project_id> <mr_iid> '<text>' # Summary note
```

### post-comment JSON format

```json
{
  "body": "**[Critical]** sql_injection\n\nRaw query with user input.",
  "position": {
    "base_sha": "abc123",
    "start_sha": "def456",
    "head_sha": "ghi789",
    "new_path": "src/db.js",
    "new_line": 42
  }
}
```

`base_sha`/`start_sha`/`head_sha` come from `get-changes` output's `diff_refs`.

## Review Rules

- **Default**: [references/review-guidelines.md](references/review-guidelines.md) — severity levels, output format, what to skip
- **Per-project**: Place `.gitlab-review-prompt.md` in the repo root; the worker auto-fetches it via `get-file`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| MRs not reviewed | `openclaw cron list` — is worker enabled? |
| API errors | `node {baseDir}/scripts/gitlab-api.js get-version` |
| Duplicate reviews | Check `{baseDir}/mr-reviewed.json` exists and is writable; ensure cron prompt has explicit "never re-review" rule at highest priority |
| Garbled comments | Use `--file` mode for `post-comment` (Windows PowerShell encoding) |
| Wrong line numbers | `new_line` must be the line number in the NEW version of the file |
