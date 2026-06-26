---
name: github-issue-reply-assistant
description: Free basic version that drafts a structured GitHub issue response and triage checklist. Reserves premium upgrade hooks for multilingual replies and fix-draft generation.
---

# GitHub Issue Smart Reply Assistant

## Value

- Free tier: one high-quality reply draft + triage checklist.
- Premium tier (reserved): multilingual reply, fix-draft, similar-issue clustering.

## Input

- `user_id`
- `repo` (`owner/repo`)
- `issue_title`
- `issue_body`
- optional `tier` (`free`/`premium`)

## Run

```bash
python3 scripts/github_issue_reply_assistant.py \
  --user-id user_003 \
  --repo openclaw/openclaw \
  --issue-title "Bug: login flow crashes" \
  --issue-body "When I click login, app crashes on callback page"
```

## Tests

```bash
python3 -m unittest scripts/test_github_issue_reply_assistant.py -v
```
