---
name: overnight-factory
description: |
  Set up an AI agent as an Overnight Software Factory operator. Use when configuring an OpenClaw agent to autonomously handle support tickets end-to-end: receive ticket assignments via email or GitHub, analyze issues, spawn Claude Code to implement fixes, open PRs, and notify a human for review. Triggers on phrases like "set up overnight factory", "configure ticket pipeline", "automate support tickets", "set up AI coding agent for tickets", or "overnight software factory".
---

# Overnight Factory

Configure this agent as an autonomous ticket-to-PR operator. Human reviews PRs; agent handles everything else.

## Architecture

```
TinyDesk/support system
  → GitHub issue (assigned to bot account)
  → Email notification to agent inbox
       ↓
  Cron job (every 15min, isolated session)
  ├─ Email check: detect assignment emails
  ├─ GitHub poll: catch missed emails (safety net)
  └─ Dispatch: spawn subagent per ticket
            ↓
       Subagent (Claude Code)
       ├─ Analyze issue + screenshots
       ├─ Explore codebase
       ├─ Post analysis comment on issue
       ├─ Implement fix (branch → commit → push)
       └─ Open PR → notify human
```

## Setup Steps

### 1. Identity & Credentials
Create workspace files: `IDENTITY.md`, `USER.md` (who you're helping), `SOUL.md`.

Add `.env` to workspace:
```
GITHUB_TOKEN=ghp_...
EMAIL_USER=support@yourdomain.com
EMAIL_PASSWORD=...
```

Configure git:
```bash
git config --global user.name "Your Bot Name"
git config --global user.email "bot@yourdomain.com"
echo "https://bot-username:${GITHUB_TOKEN}@github.com" > ~/.git-credentials
git config --global credential.helper store
```

### 2. Verify Claude Code
```bash
/path/to/claude --version
/path/to/claude -p --dangerously-skip-permissions --output-format text "echo hello"
```
Note the exact path — you'll need it.

### 3. Create the Cron Job
```bash
openclaw cron add \
  --name "email-check" \
  --every 15m \
  --session isolated \
  --announce \
  --to <YOUR-TELEGRAM-CHAT-ID> \      # explicit ID, NOT --channel last
  --timeout-seconds 120 \
  --description "Check email + GitHub for ticket assignments" \
  --message "$(cat /path/to/cron-prompt.txt)"
```

See `references/cron-prompt.md` for the full prompt template.

### 4. Keep HEARTBEAT.md Lightweight
The cron handles email. Heartbeat should only contain tasks that need main-session context (e.g., PR monitoring).

## Critical Rules

**Cron delivery:** Always use `--to <explicit-chat-id>`. Never `--channel last` — it doesn't resolve in isolated sessions.

**Cron timeout:** Keep the prompt fast. Check email → spawn subagents → log → exit. Never wait for subagents inline. 120s is enough.

**Error backoff:** After 5+ consecutive errors the cron backs off exponentially. Delete and recreate to reset: `openclaw cron delete <id> && openclaw cron add ...`

**Fire-and-forget:** Subagents don't reliably call back to Telegram. Have the cron itself announce dispatches in its own reply (the cron reply is what gets delivered).

## Validation Checklist

Before going live:
- [ ] Send test email to support address — cron picks it up within 15 min
- [ ] Cron dispatch reply arrives on Telegram
- [ ] Subagent opens a real branch + PR
- [ ] Assign a GitHub issue to bot manually — GitHub poll catches it
- [ ] `lastDelivered: false` on empty runs is expected (HEARTBEAT_OK is silent by design)

## Debugging

```bash
# Check cron status
openclaw cron list --json | jq '.jobs[0].state'

# Key fields to check:
# lastRunStatus: "ok" or "error"
# consecutiveErrors: should be 0
# lastDelivered: false on empty runs is normal; false on ticket-dispatch runs is a bug
# lastDeliveryStatus: "not-delivered" = delivery config wrong

# Check recent logs
tail -20 memory/heartbeat-log.jsonl

# Check inbox directly
python3 -c "
import imaplib, ssl
ctx = ssl.create_default_context()
M = imaplib.IMAP4_SSL('imap.ionos.com', 993, ssl_context=ctx)
M.login('user@domain.com', 'password')
M.select('INBOX')
print('Unread:', len(M.search(None, 'UNSEEN')[1][0].split()))
M.logout()
"
```

## Reference Files

- **`references/cron-prompt.md`** — full cron job prompt template with email check + GitHub poll
- **`references/ticket-pipeline.md`** — how to instruct subagents to handle tickets end-to-end
- **`references/lessons-learned.md`** — real failure modes and fixes from production use
