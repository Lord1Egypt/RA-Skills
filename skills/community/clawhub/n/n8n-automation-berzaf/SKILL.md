---
name: n8n-automation
description: >
  Trigger n8n workflows using natural language. Automate lead
  nurturing, email sequences, CRM updates, social media posting,
  meeting follow-ups, competitor monitoring, and invoice reminders
  by simply describing what you want done. Built for automation
  agencies, content creators, and solo founders using n8n.
version: 1.0.0
author: berzaf
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      env:
        - N8N_WEBHOOK_BASE_URL
        - N8N_API_KEY
      bins:
        - python3
    install:
      - id: env-setup
        kind: manual
        label: "Set N8N_WEBHOOK_BASE_URL and N8N_API_KEY in your environment"
---

# ⚡ n8n Automation Skill

## Overview

This skill connects your OpenClaw agent directly to your n8n
instance so you can trigger powerful multi-step automations using
plain natural language — no coding required at runtime.

**What makes this skill different:** It does not just call webhooks.
It confirms before acting, validates inputs, reports results, handles
errors gracefully, and remembers what was last triggered so you can
easily repeat or modify runs.

---

## Setup (One Time)

Before using this skill, export these two environment variables
in your terminal or add them to your shell profile:

```
export N8N_WEBHOOK_BASE_URL="https://your-n8n-instance.com/webhook"
export N8N_API_KEY="your-n8n-api-key-here"
```

Then restart your OpenClaw gateway:
```
openclaw gateway restart
```

You will know setup worked when you type:
> "n8n status"

And the agent responds with your instance URL confirmed.

---

## Trigger Phrases

You can trigger this skill with any of these natural language phrases:

- "trigger n8n [workflow name]"
- "run automation for [contact/task]"
- "send [email type] to [name]"
- "post to social: [content]"
- "update CRM for [name]"
- "follow up with [name] from [meeting]"
- "check competitors"
- "send invoice reminder to [client]"
- "n8n status" — checks your instance is reachable

---

## Workflow 1 — Lead Nurture Email Sequence

**What it does:**
Triggers a multi-step email sequence in n8n for a new lead.
Sends welcome email on Day 1, value email on Day 3, case study
on Day 7, and soft pitch on Day 14. All personalized.

**Trigger examples:**
- "Send lead nurture to John Smith at john@company.com"
- "Start nurture sequence for sarah@startup.io, she found us via YouTube"
- "Add Maria to lead nurture, source is LinkedIn"

**Required fields:**
- first_name
- email
- source (where they came from — optional but improves personalization)

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/lead-nurture`

**Payload sent:**
```json
{
  "first_name": "string",
  "email": "string",
  "source": "string",
  "triggered_at": "ISO timestamp",
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "queued", "sequence_id": "..." }`

---

## Workflow 2 — Social Media Auto-Post

**What it does:**
Takes content you describe or provide and posts it to your
connected social platforms via n8n. Supports LinkedIn, X (Twitter),
Instagram caption, Facebook, and Threads.

**Trigger examples:**
- "Post to social: Just launched my new n8n + OpenClaw skill on ClawHub!"
- "Post this to LinkedIn and X: [your content]"
- "Schedule social post for tomorrow 9am: [content]"

**Required fields:**
- content (the post text)
- platforms (list: linkedin, x, instagram, facebook, threads)
- schedule_time (optional — defaults to immediate)

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/social-post`

**Payload sent:**
```json
{
  "content": "string",
  "platforms": ["linkedin", "x"],
  "schedule_time": "ISO timestamp or null",
  "hashtags": ["optional", "array"],
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "posted", "post_ids": {...} }`

---

## Workflow 3 — Meeting Follow-Up

**What it does:**
After a meeting, triggers n8n to send a personalized follow-up
email with meeting summary, action items, and next steps. Also
optionally creates a follow-up task in your CRM.

**Trigger examples:**
- "Send follow-up to Mike from today's discovery call"
- "Follow up with the Acme team, meeting was about their automation needs"
- "Post-meeting email to jennifer@client.com, action items: send proposal, book next call"

**Required fields:**
- contact_name
- contact_email
- meeting_topic
- action_items (list of strings)
- next_step (optional)

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/meeting-followup`

**Payload sent:**
```json
{
  "contact_name": "string",
  "contact_email": "string",
  "meeting_topic": "string",
  "action_items": ["item1", "item2"],
  "next_step": "string or null",
  "meeting_date": "ISO date",
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "sent", "email_id": "..." }`

---

## Workflow 4 — CRM Contact Update

**What it does:**
Updates a contact record in your CRM (works with HubSpot,
GoHighLevel, Airtable, Google Sheets CRM, or any CRM connected
to your n8n). Logs notes, updates status, and sets follow-up date.

**Trigger examples:**
- "Update CRM for John Smith — he said he's ready to buy next month"
- "Mark Sarah as hot lead, she opened all emails"
- "Log call with Mike: discussed pricing, follow up in 2 weeks"

**Required fields:**
- contact_name or contact_email
- notes
- status (lead / warm / hot / closed-won / closed-lost)
- follow_up_date (optional)

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/crm-update`

**Payload sent:**
```json
{
  "contact_name": "string",
  "contact_email": "string or null",
  "notes": "string",
  "status": "string",
  "follow_up_date": "ISO date or null",
  "triggered_by": "openclaw",
  "logged_at": "ISO timestamp"
}
```

**Expected n8n response:** `{ "status": "updated", "contact_id": "..." }`

---

## Workflow 5 — Competitor Monitor Report

**What it does:**
Triggers n8n to scrape and compare your top competitors —
pricing pages, new blog posts, social activity, job postings
(signals of growth or product changes). Returns a formatted
report directly in your chat.

**Trigger examples:**
- "Check competitors"
- "Run competitor report for [your niche]"
- "What changed on my competitors' sites this week?"

**Required fields:**
- None (uses your pre-configured competitor list in n8n)
- Optional: niche or specific competitor URL to add

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/competitor-monitor`

**Payload sent:**
```json
{
  "include_niche": "string or null",
  "add_competitor_url": "string or null",
  "report_type": "full or summary",
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "complete", "report": "markdown string" }`

Display the report content directly in chat formatted as markdown.

---

## Workflow 6 — Invoice Reminder

**What it does:**
Sends a polite, personalized invoice reminder to a client.
Supports first reminder, second nudge, and final notice tones.
Logs the outreach attempt in your CRM automatically.

**Trigger examples:**
- "Send invoice reminder to Acme Corp, invoice #1042, $2,500 due"
- "Second reminder to mike@client.com for invoice 203"
- "Final notice to sarah@company.com, overdue 30 days"

**Required fields:**
- client_name
- client_email
- invoice_number
- amount
- due_date
- reminder_type (first / second / final)

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/invoice-reminder`

**Payload sent:**
```json
{
  "client_name": "string",
  "client_email": "string",
  "invoice_number": "string",
  "amount": "number",
  "due_date": "ISO date",
  "reminder_type": "first | second | final",
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "sent", "email_id": "..." }`

---

## Workflow 7 — YouTube / Content Repurpose

**What it does:**
Takes a YouTube video URL or blog post URL and triggers n8n
to repurpose it into: Twitter/X thread, LinkedIn post, email
newsletter snippet, and short-form hook. Returns all versions
in chat for your review before posting.

**Trigger examples:**
- "Repurpose this video: https://youtube.com/watch?v=..."
- "Turn my latest blog post into social content: [URL]"
- "Create social posts from: [URL]"

**Required fields:**
- url (YouTube or blog URL)
- formats (thread, linkedin, email, hook — defaults to all)

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/content-repurpose`

**Payload sent:**
```json
{
  "url": "string",
  "formats": ["thread", "linkedin", "email", "hook"],
  "brand_voice": "punchy and direct",
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "complete", "content": { "thread": "...", "linkedin": "...", "email": "...", "hook": "..." } }`

Display all content versions in chat for review.

---

## Workflow 8 — Daily Briefing

**What it does:**
Triggers n8n to pull together your full daily briefing:
new leads from last 24 hours, open deals status, social
media performance, emails that need replies, and your
top 3 priorities for the day.

**Trigger examples:**
- "Morning briefing"
- "What happened overnight?"
- "Daily digest"
- "Give me my briefing"

**Webhook endpoint:** `$N8N_WEBHOOK_BASE_URL/daily-briefing`

**Payload sent:**
```json
{
  "date": "ISO date",
  "sections": ["leads", "deals", "social", "email", "priorities"],
  "triggered_by": "openclaw"
}
```

**Expected n8n response:** `{ "status": "complete", "briefing": "markdown string" }`

Display the briefing content formatted in chat.

---

## Error Handling

If any webhook call fails, follow this sequence:

1. Report the error clearly: "The [workflow name] webhook returned [error]. Here is what was sent: [payload summary]"
2. Ask: "Should I retry, or would you like to check your n8n instance?"
3. Do NOT silently fail or pretend the workflow ran
4. Log the failed attempt in memory: "Failed workflow: [name] at [timestamp] — Error: [message]"

---

## Rules (Always Follow These)

- ALWAYS confirm what you are about to trigger before sending
- NEVER expose API keys, webhook URLs, or credentials in chat
- NEVER trigger a workflow without all required fields
- If a required field is missing, ask for it before proceeding
- NEVER send test data to production webhooks unless user confirms
- Always report the n8n response status back to the user
- If triggering email workflows, confirm the recipient email address out loud before sending
- Log every successful trigger to daily memory: "[Workflow] triggered for [target] at [time]"

---

## Status Check

At any time the user can type "n8n status" and you should:

1. Run: `python3 scripts/n8n_status.py`
2. Display the output exactly as returned
3. If any workflows show as inactive, suggest running:
   `python3 scripts/n8n_validator.py`

## Scripts Reference

All scripts live in the `scripts/` folder and use only
environment variables — no secrets stored in files.

| Script | Purpose | Command |
|--------|---------|---------|
| `n8n_trigger.py` | Trigger any workflow | `python3 scripts/n8n_trigger.py <command>` |
| `n8n_validator.py` | Validate all webhooks | `python3 scripts/n8n_validator.py` |
| `n8n_status.py` | Quick status dashboard | `python3 scripts/n8n_status.py` |

**Quick test after setup:**
```
python3 scripts/n8n_validator.py --env-only
python3 scripts/n8n_status.py
python3 scripts/n8n_trigger.py health --pretty
```

---

## Slash Commands

- `/n8n-nurture` — Quick trigger lead nurture
- `/n8n-post` — Quick trigger social post
- `/n8n-followup` — Quick trigger meeting follow-up
- `/n8n-crm` — Quick trigger CRM update
- `/n8n-competitors` — Quick trigger competitor report
- `/n8n-invoice` — Quick trigger invoice reminder
- `/n8n-repurpose` — Quick trigger content repurpose
- `/n8n-briefing` — Quick trigger daily briefing
- `/n8n-status` — Check instance health
