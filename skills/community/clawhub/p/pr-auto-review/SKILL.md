---
name: pr-auto-review
description: |
  Automated PR review pipeline: code review + service health check + Discord notification.
  Trigger when a new PR is submitted or when running post-merge validation.
  Handles: PR diff analysis, CI/CD status check, secret scanning, service health probes,
  and posting structured results to a Discord channel via webhook.
  Use phrases: "review this PR", "run PR checks", "auto-review", "PR pipeline",
  "check PR and notify Discord", "post-merge health check".
---

# PR Auto-Review

Automated pipeline that runs when a new PR is submitted:

1. **Code Review** — fetch PR diff, check CI/CD status, scan for secrets, list changed files
2. **Health Check** — verify service availability (uses healthcheck skill if present, falls back to curl probes)
3. **Discord Notification** — post structured results to a team channel

## Quick Start

```bash
# Review a GitHub PR and notify Discord
bash scripts/pr-auto-review.sh \
  --pr-url https://github.com/org/repo/pull/123 \
  --discord-webhook https://discord.com/api/webhooks/.../...

# Review a branch diff
bash scripts/pr-auto-review.sh \
  --branch feature/new-api \
  --discord-webhook https://discord.com/api/webhooks/.../...

# Review last commit, skip health check
bash scripts/pr-auto-review.sh --skip-healthcheck

# Save report to file
bash scripts/pr-auto-review.sh --pr-url ... --report ./review-report.md
```

## Options

| Flag | Description |
|------|-------------|
| `--pr-url <url>` | GitHub PR URL (extracts PR number automatically) |
| `--branch <name>` | Branch to diff against main/master |
| `--discord-webhook <url>` | Discord webhook URL for notification |
| `--skip-healthcheck` | Skip service health probes |
| `--report <path>` | Save markdown report to file |

## Pipeline Steps

### 1. Code Review

- Fetches PR diff via `gh` CLI
- Reports PR title, author, changed files
- Checks CI/CD status (`gh pr checks`)
- Scans diff for potential hardcoded secrets (password, token, api_key patterns)

### 2. Service Health Check

- If the `healthcheck` skill is installed, runs `healthcheck.sh --json`
- Otherwise, probes common local services via curl (nginx, api, ollama)
- Reports status per service: ✅ OK / 🟡 Degraded / 🔴 Down

### 3. Discord Notification

- Posts the report summary to the configured webhook
- Content truncated to 2000 chars (Discord limit)
- For richer embeds, see [references/discord-formats.md](references/discord-formats.md)

## Dependencies

- `gh` CLI (authenticated) — for PR data
- `git` — for branch diffs
- `curl` — for health probes and Discord webhook
- `jq` — for JSON payload construction

## Integration with Cron

Set up automatic PR review on a schedule:

```bash
# Example: check open PRs every 30 minutes
openclaw cron add --name "pr-review-poll" --every 30m \
  --message "Run pr-auto-review on any new open PRs and notify Discord"
```

## Integration with GitHub Webhooks

For real-time triggering, configure a GitHub webhook to call an endpoint that invokes this skill. The pipeline script accepts `--pr-url` to target the specific PR.

## Output

The script outputs a markdown report to stdout and optionally saves it to a file. The report includes:

- PR metadata (title, author, files)
- CI/CD status summary
- Security scan results
- Service health status
- Actionable summary
