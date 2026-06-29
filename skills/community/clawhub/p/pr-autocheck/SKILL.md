---
name: pr-autocheck
description: >-
  Automated post-submit checks for an AI code-review platform. Use when a new pull
  request is submitted (or on demand) to run a code review, validate service
  health, combine both into one report, and sync the result to a team Discord
  channel via webhook. Triggers on requests like "run PR autocheck", "review this
  PR and post to Discord", "automate PR checks", or wiring a CI/post-submit hook.
---

# PR Autocheck

End-to-end pipeline for a newly submitted PR: **code review → service health → Discord sync**.
All steps are deterministic shell + `jq`; no `gh` required (falls back to `git diff`).

## Quick start

Run from inside the target git repository:

```bash
bash scripts/run.sh --base origin/main --head HEAD --repo myrepo --pr 130
```

This prints the combined JSON report, saves a copy to `reports/`, and posts an
embed to Discord when `DISCORD_WEBHOOK_URL` is set.

## Configuration

| Env | Purpose | Default |
|-----|---------|---------|
| `DISCORD_WEBHOOK_URL` | Discord channel webhook for delivery | unset → payload saved to `reports/`, exit 3 |
| `HEALTHCHECK_CMD` | Override health command (must emit JSON) | healthcheck skill `healthcheck.sh --json` |
| `PR_AUTOCHECK_AI` | `1` allow optional AI deepening, `0` skip | `1` |

## Steps & scripts

1. `scripts/review.sh BASE HEAD` — deterministic review of the diff. Flags
   hardcoded secrets, dynamic eval/exec, debug prints, TODO/FIXME, oversized
   diffs. Emits `{status, files_changed, findings[], summary}`.
2. Service health — reuses the `healthcheck` skill (`--json`) when available,
   otherwise reports `unknown` instead of failing the pipeline.
3. `scripts/notify-discord.sh` — builds a color-coded Discord embed from the
   combined report and POSTs it to the webhook. **No webhook = no fake success**:
   it saves the payload and exits `3` so callers can surface "delivery pending".

`scripts/run.sh` orchestrates all three and computes an `overall` severity
(`ok` / `warn` / `critical`).

## Wiring as a post-submit hook

Point your PR event (CI job, GitHub Action, or OpenClaw cron) at:

```bash
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..." \
  bash scripts/run.sh --base "$BASE_SHA" --head "$HEAD_SHA" --repo "$REPO" --pr "$PR_NUMBER"
```

Exit code is `0` (pipeline ran); inspect the JSON `overall` field and the
`discord_exit` line on stderr to gate merges or alert.
