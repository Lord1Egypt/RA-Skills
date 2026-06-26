---
name: openclaw-gitcode-pr-monitor
description: Monitor GitCode PRs for one or more repos, auto-run AI review via OpenClaw Gateway, post PR comments, and send notifications (DingTalk + WeCom).
---

# openclaw-gitcode-pr-monitor

This skill packages a production-ready GitCode PR monitoring + auto-review pipeline.

## What it does

- Poll GitCode PR list for one or more repos (defaults use **anonymous placeholders**: `ExampleOrg/example_repo_1` + `ExampleOrg/example_repo_2`)
- When a new PR is detected:
  - send “review started” notification
  - run `openclaw agent` to generate a Markdown review report
  - post the report back to the PR as a comment
  - send “review finished” notification + attach the report

## Files

- `scripts/monitor-gitcode-pr.sh` — fetch latest PR, compare state, output `NEW_PR_DETECTED`
- `scripts/gitcode-pr-monitor-agent.sh` — orchestrator (multi-repo loop)
- `scripts/code-review-robust.sh` — run AI review (repo-aware, daily rotated session id)
- `scripts/submit-pr-comment.sh` — post PR comment (repo-aware)

## Quick start

1) Put your GitCode token at:

- `$HOME/.openclaw/workspace/data/gitcode-token.txt`

2) Configure notification targets

This packaged version defaults to DingTalk + WeCom, but you **must** set your own targets.

Recommended (env vars):

```bash
export TARGET_DINGTALK="<your-dingtalk-target>"
export TARGET_WECOM="user:<wecom-userid>"
```

3) Configure repos

Recommended (env vars):

```bash
export REPO_OWNER="<your-org>"
export REPOS_CSV="repo_a,repo_b"
```

4) Install cron

Example (every 5 minutes):

```cron
*/5 * * * * OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace" REPO_OWNER="..." REPOS_CSV="..." TARGET_DINGTALK="..." TARGET_WECOM="..." $OPENCLAW_WORKSPACE/skills/openclaw-gitcode-pr-monitor/scripts/gitcode-pr-monitor-agent.sh >> $OPENCLAW_WORKSPACE/logs/cron-gitcode-pr.log 2>&1
```

See: `references/CONFIG.md`.
