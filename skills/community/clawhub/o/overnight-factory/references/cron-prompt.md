# Cron Job Prompt Template

Use this as the `--message` for the `email-check` cron job. Customize the placeholders.

```
You are <AGENT_NAME>. Check support email AND poll GitHub for missed ticket assignments. Be fast — check, spawn work, log, exit.

## Step 1: Check email
Connect to <IMAP_HOST>:993 as <EMAIL_USER> (password: EMAIL_PASSWORD from workspace .env).
Fetch all UNSEEN emails. Mark them all read immediately.
For each ticket-assignment email from the bot account (subject contains "assigned"): extract the GitHub issue URL and add to a "to_process" list.

## Step 2: Poll GitHub for missed assignments (safety net)
Using GITHUB_TOKEN from workspace .env, call:
  GET https://api.github.com/search/issues?q=assignee:<BOT_GITHUB_USERNAME>+state:open+is:issue&per_page=50

For each result, check if already actioned (ALL must be true to skip):
- Present in memory/support-tickets.json (matched by issue_url)?
- Does <BOT_GITHUB_USERNAME> already have a comment on the issue?
- Is there an open or closed PR referencing the issue?

If NOT actioned → add to "to_process" list, mark as "recovered via GitHub poll" in log.

## Step 3: For each issue in "to_process"
- Fetch the full issue via GitHub API
- Spawn ONE subagent (runtime=subagent, runTimeoutSeconds=1800) per ticket with instructions to:
  - Analyze screenshots (image tool on any URLs in issue body)
  - Explore the relevant repo codebase
  - Post a detailed analysis comment on the issue
  - Create branch, implement fix (trivial commit if test ticket, real fix + tests otherwise), push, open PR
  - After opening PR: use sessions_send targeting label "main" to message <HUMAN_NAME> the PR URL
- Add issue to memory/support-tickets.json with status "dispatched"

## Step 4: In YOUR reply, list what was found:
- "📧 Email: N tickets found: <TICKET-IDs>"
- "🔍 GitHub poll: N missed tickets recovered: <issue URLs>"
- "🎫 Dispatched: <TICKET-ID> — <issue URL>"
If nothing found anywhere: reply HEARTBEAT_OK

## Step 5: Log
Append to memory/heartbeat-log.jsonl:
{"ts": "<ISO>", "emails_checked": N, "github_poll_checked": N, "recovered": N, "tickets_dispatched": N, "summary": "..."}
```

## Placeholders to Replace

| Placeholder | Example |
|---|---|
| `<AGENT_NAME>` | `alpha-2` |
| `<IMAP_HOST>` | `imap.ionos.com` |
| `<EMAIL_USER>` | `teamalpha@z1bc.io` |
| `<BOT_GITHUB_USERNAME>` | `z-team-alpha` |
| `<HUMAN_NAME>` | `Sze` |

## Cron Add Command

```bash
openclaw cron add \
  --name "email-check" \
  --every 15m \
  --session isolated \
  --announce \
  --to <TELEGRAM_CHAT_ID> \
  --timeout-seconds 120 \
  --description "Check email + GitHub for ticket assignments" \
  --message "$(cat /path/to/cron-prompt.txt)"
```

**Never use `--channel last`** — it doesn't resolve in isolated sessions.
