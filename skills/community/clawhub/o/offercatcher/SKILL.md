---
name: offercatcher
description: Turn recruiting emails into native Apple Reminders. AI-powered parsing extracts interview/assessment events and syncs to iPhone.
version: 0.1.0
---

# OfferCatcher

## What It Does

Scans your Apple Mail for recruiting emails, extracts important events (interviews, assessments, deadlines) using LLM, and creates native Apple Reminders that sync to your iPhone.

## How To Use

### Trigger Phrases

- "Check my recruiting emails"
- "Any interviews coming up?"
- "Sync interview emails to reminders"
- "Don't let me miss my coding test"

### Workflow

```
1. Scan: --scan-only → returns JSON with raw emails
2. Parse: OpenClaw LLM extracts events from emails
3. Apply: --apply-events → creates Apple Reminders
```

### Step 1: Scan Emails

```bash
python3 scripts/recruiting_sync.py --scan-only
```

Returns raw email data for LLM to parse.

### Step 2: LLM Parses

For each email, extract:
- `company`: Company name
- `event_type`: interview / ai_interview / written_exam / assessment / authorization / deadline
- `timing`: `{"start": "YYYY-MM-DD HH:MM", "end": "..."}` or `{"deadline": "..."}`
- `role`: Job title
- `link`: Event URL

### Step 3: Apply Events

```bash
python3 scripts/recruiting_sync.py --apply-events /tmp/events.json
```

## LLM Parsing Prompt

```
Extract recruiting event information from this email. Return JSON.

Email:
{body}

Extract:
- company: Company name
- event_type: interview / ai_interview / written_exam / assessment / authorization / deadline
- timing: {"start": "YYYY-MM-DD HH:MM", "end": "..."} or {"deadline": "..."}
- role: Job title
- link: Event URL
- notes: Additional info
```

## Output Rules

- Reminder title: Company + Event type (e.g., "Google Interview", "Meta Coding Test")
- Include: Time, role, link in notes
- If no new events: respond `HEARTBEAT_OK`

## Configuration

`~/.openclaw/offercatcher.yaml`:

```yaml
mail_account: "Gmail"    # Apple Mail account name
mailbox: INBOX           # Folder to scan
days: 2                  # Scan last N days
max_results: 60          # Max emails
```

## Supported Languages

The LLM parser works with any language—Chinese, English, Japanese, German, etc. No regex, no language-specific rules.