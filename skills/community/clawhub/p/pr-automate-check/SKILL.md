---
name: pr-automate-check
description: |
  Automated PR submission pipeline: code review, service health validation, and Discord notification.
  Use when a new PR is submitted and needs automated checks before merge. Triggers on
  "PR check", "PR automation", "auto review", "pre-merge check", "PR提交检查", "自动化评审".
---

# PR Automate Check

Automated pipeline that runs on every new PR submission:

1. **Code Review** — diff analysis via `gh pr diff`, CI/CD status check
2. **Health Check** — service health validation (reuses the healthcheck skill)
3. **Discord Notification** — posts structured embed to a team channel

## Quick Start

```bash
# Full pipeline (review + health + Discord)
bash {baseDir}/scripts/pr-check.sh <PR_URL> <DISCORD_WEBHOOK_URL>

# Review + health only (no Discord)
bash {baseDir}/scripts/pr-check.sh <PR_URL>
```

## Workflow

### Step 1: Trigger

When a new PR is submitted, run the script with the PR URL. The PR URL must be a GitHub pull request URL (`https://github.com/owner/repo/pull/123`).

### Step 2: Code Review

The script extracts the PR number, fetches the diff and CI status via `gh`, and writes them to a temp directory. The agent then reads the diff and performs a structured review following the code-review skill's guidelines (quality, security, performance, test coverage).

### Step 3: Health Check

Runs the healthcheck skill (`healthcheck.sh --json`) if installed; otherwise emits a stub. The JSON output includes per-service status and a severity level:

| Severity | Meaning |
|----------|---------|
| 0 | All healthy |
| 1 | Warnings |
| 2 | Critical |

### Step 4: Discord Notification

If a Discord webhook URL is provided, the script posts a color-coded embed:

- 🟢 Green: all services healthy
- 🟡 Yellow: warnings
- 🔴 Red: critical issues

The embed includes the health summary and PR link.

### Step 5: Report

A JSON report is written containing timestamp, PR metadata, and health results. The agent uses this to compose a final summary.

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `PR_URL` | Yes | GitHub PR URL |
| `DISCORD_WEBHOOK` | No | Discord webhook URL for notifications |

## Dependencies

- `gh` (GitHub CLI) — authenticated
- `jq` — JSON processing
- `curl` — Discord webhook
- `python3` — health summary formatting
- healthcheck skill (optional) — for full service checks

## Integration with OpenClaw Cron

To run automatically on PR events, set up a cron job or webhook that calls:

```
bash {baseDir}/scripts/pr-check.sh <PR_URL> <WEBHOOK>
```

Or use the agent directly:

```
Run the PR automate check for <PR_URL> and post results to Discord.
```
