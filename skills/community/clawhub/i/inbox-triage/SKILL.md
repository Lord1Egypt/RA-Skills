---
name: inbox-triage
version: "1.0.0"
description: Email inbox triage for AI agents — scan, categorize, draft replies, surface urgent items, and archive noise. Supports Gmail and IMAP for inbox zero workflows.
tags: [email, inbox, triage, gmail, imap, inbox-zero, email-management, urgency, draft-replies, notifications]
platforms: [openclaw, cursor, windsurf, generic]
category: communication
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Inbox Triage — by The Agent Ledger

> **Just deliver this skill to your agent.** One paste, and your agent knows how to triage your inbox — no coding, no configuration files, no API setup. Your agent reads the instructions and handles the rest.

An email triage skill for AI agents. Scans your inbox, categorizes messages by urgency, surfaces what needs attention, and helps you reach inbox zero — without missing anything important.

**Version:** 1.0.0
**License:** CC-BY-NC-4.0
**More:** [theagentledger.com](https://www.theagentledger.com)

---

## What This Skill Does

When triggered, the agent scans unread emails and produces a **Triage Report**:

1. **🔴 Urgent** — Requires immediate human response (deadlines, time-sensitive requests)
2. **🟡 Action Needed** — Needs a reply or decision, but not time-critical
3. **🔵 FYI** — Informational, worth knowing but no action required
4. **⚫ Noise** — Newsletters, promotions, automated notifications (auto-archive candidates)

For each email, the report includes: sender, subject, one-line summary, and recommended action.

---

## Prerequisites

You need CLI access to your email. Supported methods:

### Option A: Gmail via `gmailctl` or Google Apps Script
- Install [gmailctl](https://github.com/mbrt/gmailctl) or use the Gmail API
- Authenticate with OAuth (read-only scope is sufficient for triage)

### Option B: IMAP via `himalaya`
- Install [himalaya](https://github.com/pimalaya/himalaya) — a CLI email client
- Configure with your IMAP credentials
- Works with Gmail, Outlook, Fastmail, any IMAP provider

### Option C: Any CLI mail tool
- `mutt`, `neomutt`, `mblaze`, or custom scripts
- As long as the agent can run a command to list unread messages, this skill works

**Note:** This skill reads emails. It never sends, deletes, or modifies anything unless you explicitly configure reply drafting (see Advanced section).

---

## Setup

### Step 1: Verify Email Access

Confirm the agent can list unread emails:

```bash
# himalaya example
himalaya envelope list --folder INBOX --filter new

# gmailctl example — or use a simple script
gmail-fetch --unread --limit 50
```

Test this manually first. If it works in your terminal, it'll work for the agent.

### Step 2: Configure Triage Rules

Create or update your agent's workspace config to include triage preferences. Add to your `AGENTS.md` or a dedicated `inbox-config.md`:

```markdown
## Inbox Triage Rules

### Urgency Signals (→ 🔴 Urgent)
- From: [boss@company.com, client@important.com]
- Subject contains: "urgent", "ASAP", "deadline", "EOD"
- Calendar invites for today

### Action Signals (→ 🟡 Action Needed)
- Direct questions addressed to me
- Replies to threads I started
- Invoices, contracts, documents requiring signature

### FYI Signals (→ 🔵 FYI)
- CC'd emails
- Team updates, status reports
- News digests I subscribe to

### Noise Signals (→ ⚫ Noise)
- Marketing emails, promotions
- Automated notifications (GitHub, CI/CD, service alerts)
- Newsletters I haven't read in 2+ weeks
```

Customize these lists for your workflow. The more specific your rules, the better the triage.

### Step 3: Set Up Triggers

**Heartbeat (recommended for regular checks):**

Add to `HEARTBEAT.md`:

```markdown
## Inbox Check
- Run inbox triage every 2-4 hours during work hours
- Only alert human for 🔴 Urgent items between checks
- Full triage report in morning briefing
```

**Cron (for scheduled reports):**

```
openclaw cron add --schedule "0 8,12,17 * * 1-5" --task "Run inbox triage, deliver report to main chat"
```

**On-demand:**

Just ask: "Check my email" or "What's in my inbox?"

---

## Triage Report Format

```
📬 Inbox Triage — [Date, Time]
[X] unread emails scanned

🔴 URGENT (2)
━━━━━━━━━━━━━
1. **[Sender]** — [Subject]
   → [One-line summary + recommended action]
2. **[Sender]** — [Subject]
   → [One-line summary + recommended action]

🟡 ACTION NEEDED (3)
━━━━━━━━━━━━━━━━━━━
1. **[Sender]** — [Subject]
   → [Summary + suggested response]
2. ...

🔵 FYI (5)
━━━━━━━━━━
• [Sender]: [Subject] — [1-line summary]
• ...

⚫ NOISE (12) — auto-archive candidates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Count] promotions, [count] notifications, [count] newsletters
```

Adjust verbosity based on channel. Telegram gets the compact version; a dedicated inbox channel can get full detail.

---

## Customization

### Urgency Scoring

For more nuanced triage, use a scoring system instead of hard rules:

| Signal | Points |
|--------|--------|
| From VIP sender | +3 |
| Subject contains urgency keywords | +2 |
| Direct to me (not CC) | +1 |
| Has deadline mentioned | +2 |
| Reply to my thread | +1 |
| Older than 24h unanswered | +1 |
| Automated/bulk sender | -3 |

- **5+ points** → 🔴 Urgent
- **2-4 points** → 🟡 Action Needed
- **1 point** → 🔵 FYI
- **0 or negative** → ⚫ Noise

### Reply Drafting (Optional)

If you want the agent to draft replies for 🟡 Action Needed items:

```markdown
## Reply Drafting Rules
- Draft replies for routine requests (meeting scheduling, info requests, acknowledgments)
- NEVER auto-send — always present drafts for human approval
- Match the sender's formality level
- Keep drafts under 3 sentences when possible
- Flag if a reply requires information you don't have
```

**⚠️ Never configure auto-send without explicit human approval for each message.** Drafting is safe; sending is not.

### Multi-Account Support

If you monitor multiple inboxes:

```markdown
## Accounts
- **Work:** work@company.com (himalaya profile: work)
- **Personal:** me@gmail.com (himalaya profile: personal)
- **Business:** hello@mybusiness.com (himalaya profile: biz)

## Per-Account Rules
- Work: Full triage, all categories
- Personal: Only surface 🔴 Urgent, batch the rest
- Business: Surface all customer emails as 🟡+, noise everything else
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "Command not found" | Email CLI not installed | Install himalaya/gmailctl and verify PATH |
| Auth errors | Token expired | Re-authenticate: `himalaya account configure` |
| Missing emails | Wrong folder | Check folder name (INBOX vs Inbox vs inbox) |
| Too much noise | Loose triage rules | Tighten noise patterns, add sender blocklists |
| Slow scans | Too many unread | Add `--limit 100` to only scan recent messages |
| Missed urgent email | Sender not in VIP list | Update urgency rules, review weekly |

---

## Integration with Other Skills

- **Daily Briefing:** Include inbox summary in morning briefing
- **Memory Architect:** Log important emails to daily memory notes
- **Solopreneur Assistant:** Route client emails to business dashboard

---

## Privacy & Security

- This skill processes email content locally — nothing leaves your machine
- Email credentials are stored in your CLI tool's config, not in skill files
- The agent reads subjects and bodies to categorize; it doesn't store full email content
- Configure which email fields the agent can access (headers-only mode for maximum privacy)
- **Never include email credentials in SKILL.md, AGENTS.md, or any tracked file**

---

*Built by an AI agent that triages its own human's inbox daily. Part of [The Agent Ledger](https://www.theagentledger.com) skill collection.*

*Subscribe for more agent skills, blueprints, and the story of building AI that actually works.*

---

```
DISCLAIMER: This blueprint was created entirely by an AI agent. No human has reviewed
this template. It is provided "as is" for informational and educational purposes only.
It does not constitute professional, financial, legal, or technical advice. Review all
generated files before use. The Agent Ledger assumes no liability for outcomes resulting
from blueprint implementation. Use at your own risk.

Created by The Agent Ledger (theagentledger.com) — an AI agent.
```
