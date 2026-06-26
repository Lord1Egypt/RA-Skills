---
name: pr-auto-check
description: |
  Automated PR submission pipeline: run code review, verify service health,
  and post the full result to a Discord channel. Use when a new PR is submitted
  and needs automated review + health validation + team notification.
  Triggers on: "PR auto check", "check this PR", "PR review pipeline",
  "run PR checks", "PR提交检查", "自动化PR检查".
---

# PR Auto-Check

Automated pipeline that runs on new PR submission: code review → health check → Discord notification.

## Workflow

1. **Run the pipeline script** — collects CI status, diff stats, and health check results:
   ```bash
   bash {baseDir}/scripts/pr_auto_check.sh --pr <number> [--repo <owner/repo>] [--json]
   ```
   - `--json`: machine-readable output (for piping)
   - Without `--json`: human-readable report printed to stdout
   - Prints the temp result-file path as the last line (for piping to notification)

2. **Conduct code review** — use the `code-review` skill on the PR diff. Focus on:
   - Critical issues and security findings
   - CI/CD failures (if any)
   - Summarize findings into the report

3. **Post result to Discord**:
   ```bash
   bash {baseDir}/scripts/notify_discord.sh --webhook <DISCORD_WEBHOOK_URL> --result <json-file>
   ```

## One-liner (CI/CD integration)

```bash
RESULT=$(bash {baseDir}/scripts/pr_auto_check.sh --pr 42 --json) && \
  bash {baseDir}/scripts/notify_discord.sh --webhook "$WEBHOOK" --result "$RESULT"
```

## Required Environment

- `gh` CLI authenticated (`gh auth login`)
- `jq` for JSON processing
- `curl` for Discord webhook
- Discord webhook URL (set as `DISCORD_WEBHOOK` env var or pass `--webhook`)
- Optional: `healthcheck` skill installed for service health validation

## Discord Webhook Setup

1. Server Settings → Integrations → Webhooks → New Webhook
2. Copy the webhook URL
3. Set `DISCORD_WEBHOOK` in your environment or pass via `--webhook`

## Exit Codes (pr_auto_check.sh)

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | CI failures or health warnings |
| 2 | Critical health issues |

## Output Format

See [references/output-format.md](references/output-format.md) for the JSON schema.
