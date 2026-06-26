---
name: pitch-follow-up-tracker
description: "Track outreach pitches and draft contextual follow-up emails. Monitors a pitch tracker (Google Sheet or local markdown), checks Gmail for replies, flags stale pitches, and drafts tiered follow-ups (Day 3, Day 7, Day 14) that reference the original pitch content. Use when you need to check on pitch follow-ups, draft follow-up emails, review outreach status, find pitches without replies, or manage an outreach pipeline. Triggers on: 'check follow-ups,' 'who hasn't replied,' 'draft follow-ups,' 'outreach status,' 'pitch tracker,' 'stale pitches,' or any request to manage pitch/outreach follow-up."
---

# Pitch Follow-Up Tracker

Monitor outreach pitches, detect non-replies, and draft contextual, tiered follow-up emails.

## Prerequisites

- **gog CLI** (required) — for Gmail access
  ```bash
  which gog
  ```
- **Google account** configured with gog (`gog gmail --account <email>`)
- **Pitch tracker** — one of:
  - Google Sheet with outreach data
  - Local markdown file with pitch records

## Workflow

### 1. Collect Configuration

Ask the user (or detect from context):

| Parameter | Required | Description |
|-----------|----------|-------------|
| `gmail_account` | yes | Email account to check (e.g., you@company.com) |
| `tracker_type` | yes | "sheet" or "markdown" |
| `tracker_id` | if sheet | Google Sheet ID |
| `tracker_path` | if markdown | Path to local .md file |
| `sender_name` | yes | Name to use in follow-ups |
| `sender_role` | optional | Role/title for email signature context |
| `follow_up_style` | optional | "warm" (default), "direct", or "casual" |

### 2. Load Pitch Data

**From Google Sheet:**
```bash
gog sheets get <SHEET_ID> "<TAB_NAME>!A1:Z500" --json --account <gmail_account>
```

Expected columns (flexible — adapt to whatever columns exist):
- Contact name / email
- Brand / company
- Date sent
- Subject or pitch summary
- Status (if tracked)

**From Markdown file:**
Read the file. Expected format (flexible):
```markdown
## [Brand Name]
- **Contact:** Name <email>
- **Sent:** YYYY-MM-DD
- **Subject:** [pitch subject]
- **Summary:** [what was pitched]
- **Status:** Sent / Replied / Closed
```

Adapt to whatever format the user actually uses. Extract: contact email, brand, date sent, pitch content/subject, current status.

### 3. Verify Reply Status (CRITICAL — Do Not Skip Steps)

Before flagging ANY pitch as "needs follow-up," you MUST complete ALL of these checks. Do not skim. Do not skip. A false positive wastes the user's time and erodes trust.

**Check 1: Search for direct replies**
```bash
gog gmail search "from:<contact_email>" --max 10 --account <gmail_account>
```
Look for any reply from the contact after the pitch send date, even in a different thread.

**Check 2: Search by domain (catches new threads)**
```bash
gog gmail search "from:@<contact_domain>" --max 10 --account <gmail_account>
```
Brands often respond from a different person at the same company. Check for ANY email from that domain since the pitch date.

**Check 3: Search sent folder for user follow-ups**
```bash
gog gmail search "to:<contact_email> OR to:@<contact_domain>" --max 10 --account <gmail_account>
```
Check if the user already sent a response, follow-up, or forwarded the thread.

**Check 4: Search drafts for unsent responses**
```bash
gog gmail search "in:drafts <contact_name> OR <brand_name>" --max 5 --account <gmail_account>
```
A draft response means the user is working on it. Do NOT flag as needing follow-up.

**Check 5: Check if forwarded**
```bash
gog gmail search "subject:Fwd: <original_subject>" --max 5 --account <gmail_account>
```
If the original email was forwarded to a colleague, talent, or team member, it may be in progress.

**Check 6: Read full email threads**
For any matching threads, read the FULL thread content — not just the latest message. Context changes mid-thread.
```bash
gog gmail get <message_id> --account <gmail_account>
```

**Check 7: Check recent memory/context**
If available, check conversation history, daily memory files, or any tracker for recent context about this deal. The user may have mentioned handling it verbally or via another channel (text, WhatsApp, call).

**Classification (only after ALL checks):**
- **Replied** — contact responded (in same or different thread)
- **Already followed up** — user sent a follow-up but no reply yet
- **Draft in progress** — user has an unsent draft
- **Forwarded/delegated** — user forwarded to someone else
- **Needs follow-up** — ALL checks came back empty. No activity since original send.
- **Too fresh** — sent less than 3 days ago

### 4. Calculate Follow-Up Tier

For pitches needing follow-up, determine tier based on days since last outreach:

| Days Since Last Contact | Tier | Tone |
|------------------------|------|------|
| 3-6 days | **Day 3: Gentle Nudge** | Light, brief, bumping to top of inbox |
| 7-13 days | **Day 7: Add Value** | Share something useful — article, idea, new angle |
| 14+ days | **Day 14: Final Check-In** | Direct, low-pressure, leave door open |

If user already sent one follow-up, advance to next tier.

### 5. Draft Follow-Up Emails

Each draft MUST reference the original pitch content. No generic "just checking in" emails.

**Day 3 — Gentle Nudge:**
```
Subject: Re: [Original Subject]

Hi [Name],

Wanted to bump this to the top of your inbox — [one sentence referencing the specific pitch content, e.g., "the proposal for a summer campaign series featuring outdoor content"].

Happy to jump on a quick call or send more details if helpful.

[Sender Name]
```

**Day 7 — Add Value:**
```
Subject: Re: [Original Subject]

Hi [Name],

Following up on my note about [specific pitch reference]. Since I sent that over, [add relevant value: a new idea, a relevant trend, a recent success story, a new content example].

Would love to explore how this could work for [Brand]. Open to a quick chat this week?

[Sender Name]
```

For the "add value" component, search the web for a recent relevant tidbit:
```
web_search "[brand name] [niche] news 2026"
```
Incorporate a genuine, relevant insight — not filler.

**Day 14 — Final Check-In:**
```
Subject: Re: [Original Subject]

Hi [Name],

Circling back one last time on [specific pitch reference]. Totally understand if the timing isn't right — just wanted to make sure this didn't get buried.

If [Brand] is exploring [relevant type of partnership] down the line, I'd love to be on your radar. Always happy to connect.

[Sender Name]
```

Adjust tone based on `follow_up_style`:
- **warm** (default): Friendly, relationship-focused
- **direct**: Shorter, business-focused, clear ask
- **casual**: Conversational, emoji-OK, lighter

### 6. Output Summary

```markdown
# Outreach Follow-Up Report

**Date:** [today]
**Account:** [gmail_account]
**Pitches Reviewed:** [total count]

## ✅ Replies Received ([count])
| Brand | Contact | Replied On | Action Needed |
|-------|---------|------------|---------------|
| [Brand] | [Name] | [date] | [Review reply / Schedule call / Send deck] |

## 🔥 Needs Follow-Up ([count])

### Day 3 — Gentle Nudge
**[Brand Name]** → [Contact Name] <[email]>
- Original pitch: [summary]
- Sent: [date] ([X] days ago)
- Draft:
> [Full draft email]

### Day 7 — Add Value
**[Brand Name]** → [Contact Name] <[email]>
- Original pitch: [summary]
- Sent: [date] ([X] days ago)
- Draft:
> [Full draft email]

### Day 14 — Final Check-In
**[Brand Name]** → [Contact Name] <[email]>
- Original pitch: [summary]
- Sent: [date] ([X] days ago)
- Draft:
> [Full draft email]

## ⏳ Too Fresh to Follow Up ([count])
| Brand | Contact | Sent | Follow-Up Date |
|-------|---------|------|----------------|
| [Brand] | [Name] | [date] | [date when Day 3 hits] |

## 📊 Pipeline Summary
- Total active pitches: [X]
- Awaiting reply: [X]
- Replied: [X]
- Follow-ups needed today: [X]
```

### 7. Create Gmail Drafts (if requested)

If the user approves the follow-up drafts:

```bash
gog gmail draft create --to "<email>" --subject "Re: [subject]" --body "<draft body>" --account <gmail_account>
```

Always ask before creating drafts. Never send emails without explicit approval.

## Error Handling

| Issue | Action |
|-------|--------|
| gog not installed | Stop and instruct: `npm i -g gog` or equivalent |
| Gmail auth expired | Prompt: `gog gmail auth --account <email>` |
| Sheet not accessible | Verify Sheet ID and sharing permissions |
| No pitches found in tracker | Report empty tracker, suggest format |
| Contact email missing | Flag the pitch, skip Gmail check for it |
| Rate limited on Gmail | Space queries with 1-2s delays, process in batches |
| Markdown format unexpected | Adapt parsing to whatever structure exists, ask user if ambiguous |

## Tips

- Run this daily or every 2-3 days for best results
- Keep your pitch tracker updated — the skill is only as good as your data
- Review and personalize drafts before sending — they're starting points, not final copy
- The "add value" follow-up works best when you have genuine news or insights to share
