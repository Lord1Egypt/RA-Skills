---
interval: 1h
timeout: 15m
agent: claude-code
model: opus
name: GitHub Issue Monitor
description: Monitor GitHub issues for new unlabeled issues
---

Check for new GitHub issues on {org}/{repo} using `gh issue list --state open --json number,title,body,labels`.
For any issue with no labels:

- Read the title and body
- Apply one of: `bug`, `feature`, `question`, `security`
- Use `gh issue edit {number} --add-label {label}`

If any issue is labeled `security`, post to Slack:
`curl -X POST -H 'Content-Type: application/json' -d '{"text":"Security issue #{number}: {title}"}' $SLACK_WEBHOOK_URL`

If no unlabeled issues, respond HEARTBEAT_OK.
