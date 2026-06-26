# Cron Worker Setup

## Install

```bash
openclaw cron add `
  --name "GitLab MR Worker" `
  --cron "*/2 * * * *" `
  --tz "Asia/Shanghai" `
  --session "isolated" `
  --timeout-seconds 120 `
  --no-deliver `
  --message "You are a GitLab MR Review Worker. Follow these steps:

1. Run: node {baseDir}/scripts/gitlab-api.js list-mrs — get all open MRs
2. For each MR, check if it is already in the reviewed log (path: {baseDir}/mr-reviewed.json, format: {\"project_iid\": \"reviewed_at_iso\"})
3. Skip reviewed MRs. For each unreviewed MR:
   a. Fetch diff: node {baseDir}/scripts/gitlab-api.js get-changes <project_id> <mr_iid>
   b. Read review rules: {baseDir}/references/review-guidelines.md
   c. Check for custom rules: node {baseDir}/scripts/gitlab-api.js get-file <project_id> <source_branch> .gitlab-review-prompt.md
   d. Review each file, skip lock/min/generated files
   e. For each issue, write JSON to a temp file first, then post inline comment via --file: node {baseDir}/scripts/gitlab-api.js post-comment --file /tmp/comment-N.json <project_id> <mr_iid>
      IMPORTANT: Never pass JSON directly on the command line! Always use the write tool to create a file, then pass it via --file.
   f. Post summary note: node {baseDir}/scripts/gitlab-api.js post-note <project_id> <mr_iid '<markdown>'
   g. ⚠️ CRITICAL: Immediately after posting the summary note for this MR, use the read tool to read {baseDir}/mr-reviewed.json, append this MR's record, then use the write tool to write the full file back. You MUST write back after EACH MR — never batch writes after reviewing all MRs. If the file doesn't exist, create it as an empty JSON object first.
4. Process all unreviewed MRs in this run. If no new MRs, reply NO_REPLY.
5. Do not ask for permission — execute directly."
```

> **Tip:** Adjust `--tz` to your timezone. Use `--model` to override the model, or `--thinking` to enable extended thinking.

Verify:
```bash
openclaw cron list
```

## ⚠️ Encoding Note (Windows / PowerShell)

All `post-comment` calls **must** use `--file` mode. Shell encoding may corrupt inline JSON (especially CJK or special chars). Always:
1. `write` the JSON payload to a temp file
2. Pass the file path via `--file`
