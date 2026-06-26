# Email Assistant

**5,000 unread emails? Let's fix that.**

Stop drowning in your inbox. Email Assistant isn't just another summarizer — it's a context-aware AI that reads, categorizes, and preps your responses so you only focus on what actually matters.

Free and open-source. Zero subscriptions. 100% private.

## Features

- **Smart Inbox Triage:** Automatically sorts every email into Urgent, Action Needed, FYI, or Archive — so you know exactly where to focus.
- **One-Click Draft Replies:** Get perfectly toned, context-aware draft replies ready for your review. Your agent matches your writing style.
- **VIP Sender System:** Emails from your boss or top clients bypass the queue and get flagged immediately. You set the rules.
- **Draft-Only Mode:** Your agent NEVER sends an email without you. It preps the work — you always pull the trigger. No rogue replies. Ever.
- **Already-Addressed Detection:** Already replied on your phone? Your agent knows. No more stale alerts or double-handling.
- **Proactive Research:** "Want me to pull up the Q3 numbers before you reply to Sarah?" Your agent anticipates what you need.
- **Anti-Phishing Defense:** Suspicious emails get flagged with clear explanations. Typosquat domains, credential requests, urgency scams — caught automatically.
- **Flexible Scheduling:** Get briefed hourly, twice a day, or just once in the morning. Your schedule, your rules.

## Installation

1. Copy the contents of this package to your `skills/email-assistant/` directory.
2. Ask your OpenClaw agent: **"Read the SETUP-PROMPT.md file in the email-assistant skill and follow the instructions."**
3. That's it. Start with "What's in my inbox?"

## Requirements

You need an email access tool configured in your environment. Any of these work:
- **himalaya** (recommended) — lightweight IMAP/SMTP CLI
- **gog** — for Google Workspace / Gmail users
- **mutt/neomutt** — classic IMAP tools
- **MCP email server** — if configured in your agent

The setup process will check for you and guide you if nothing is found.

## Security & Privacy

- **Codex Security Verified** — rigorous prompt injection and anti-phishing defenses included.
- **No data exfiltration** — our code never phones home or sends your data anywhere.
- **Draft-Only guarantee** — the agent cannot send emails. Period. You always approve.
- **Anti-phishing built in** — suspicious emails flagged with clear explanations.
- **Local data** — everything stays in your workspace with locked-down file permissions.

See `SECURITY.md` for the full audit and guarantees.

## What's Inside

```
SKILL.md — Full skill instructions for your agent
SETUP-PROMPT.md — One-time setup (your agent runs this)
README.md — You're reading it
SECURITY.md — Security audit and guarantees
config/
 email-config.json — Default triage rules, VIPs, and schedule
examples/
 inbox-triage-example.md
 draft-reply-example.md
 digest-example.md
scripts/
 email-health-check.sh
dashboard-kit/
 DASHBOARD-SPEC.md — Companion dashboard spec
```
