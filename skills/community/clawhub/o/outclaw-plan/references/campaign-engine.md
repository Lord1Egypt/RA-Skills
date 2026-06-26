# Campaign Engine Reference

Full specification for campaign planning, execution, and lifecycle management.

## Campaign Lifecycle

```
PLAN → ACTIVE → { RESPONSE_RECEIVED | FOLLOWUP_SENT | SILENCE }
                       ↓                    ↓              ↓
                 PLAN_REVISION         ACTIVE (next)   ACTIVE (next followup)
                       ↓                    ↓              ↓
                    ACTIVE              COMPLETED      COMPLETED
```

## Campaign Planning

### Step 1 — Prospect Research

**With Leadbay:**
1. Query LeadClaw for company firmographics (size, industry, tech stack, funding, news)
2. Pull contact profile (role, seniority, tenure, public activity)
3. Get ICP match score with dimension breakdown
4. Check existing notes (prior outreach, deal stage, teammate activity)
5. Surface mutual connections from relationship graph
6. Assemble prospect brief

**Without Leadbay (degraded):**
1. Web search for company and contact
2. Warn user about limited data
3. Build prospect brief from public sources only

### Step 2 — Channel Selection

Recommend channels based on:
- Prospect's likely responsiveness per channel
- User's connected channels
- Industry norms

Default ordering: Email → LinkedIn → WhatsApp (if B2B contact has WhatsApp Business)

Present as suggested sequence; user can reorder or remove.

### Step 3 — Message Draft Generation

For each touchpoint, generate draft using the learned style prompt for that channel.

Present as a full plan:

```
OUTREACH PLAN: {Name}, {Title} @ {Company}
═══════════════════════════════════════════════════

Touchpoint 1 — {Channel} ({Type})
  Scheduled: {Date} at {Time}
  ┌──────────────────────────────────────┐
  │ {Message preview}                    │
  └──────────────────────────────────────┘

Touchpoint 2 — {Channel} ({Type})
  Scheduled: {Date} at {Time}
  (only if no reply by then)
  ┌──────────────────────────────────────┐
  │ {Message preview}                    │
  └──────────────────────────────────────┘

... (up to 4-5 touchpoints)

──────────────────────────────────────────
Approve this plan? [Yes / Edit / Cancel]
```

## Execution Engine

### Scheduling
- Each touchpoint registered via `create_scheduled_task` with `fireAt` timestamp
- Managed by `scripts/schedule_manager.py`

### Conditional Gates
Before each touchpoint fires:
1. Check all connected channels for responses from the prospect
2. If response found → skip touchpoint, enter PLAN_REVISION
3. If no response → proceed with send

### Send Confirmation
- Default: ask user approval before each send
- Trust mode: user pre-approves all sends during plan approval (set per campaign)

### Send Execution
Dispatch via appropriate channel MCP tools:
- Email: `gmail.create_draft` + send
- Slack: `slack_send_message`
- WhatsApp: WhatsApp MCP send
- LinkedIn: Browser automation

### Leadbay Activity Logging
After every event, write structured note to lead record via `scripts/leadbay_sync.py`.

## Campaign State Schema

```json
{
  "id": "sarah-chen-acme",
  "prospect": {
    "name": "Sarah Chen",
    "company": "Acme Corp",
    "title": "VP Engineering",
    "channels": {
      "email": "sarah@acme.com",
      "linkedin": "linkedin.com/in/sarachen"
    },
    "leadbay_lead_id": "lb_lead_abc123",
    "leadbay_company_id": "lb_co_xyz789",
    "icp_match_score": 87,
    "leadbay_synced": true
  },
  "status": "active",
  "trust_mode": false,
  "touchpoints": [
    {
      "channel": "email",
      "type": "cold_open",
      "scheduled_at": "2026-04-20T09:15:00-07:00",
      "sent_at": null,
      "message_id": null,
      "thread_id": null,
      "status": "pending",
      "message_draft": "...",
      "condition": null
    }
  ],
  "responses": [],
  "created_at": "2026-04-19T14:30:00-07:00",
  "updated_at": "2026-04-19T14:30:00-07:00"
}
```

## Campaign Dashboard

Format for "show my campaigns":

```
ACTIVE CAMPAIGNS
════════════════════════════════════════════════

1. {Name} — {Title} @ {Company}
   Status:    {status description}
   Next step: {next touchpoint} — {date}
   Channels:  {channel sequence with status icons}
   Progress:  {progress bar} {sent}/{total}

────────────────────────────────────────────────
Summary: {active} active, {replies} reply pending, {completed} completed this week
```

## Anti-Spam Rules

- Max 20 new cold outreaches per day
- Min 3 business days between touchpoints to same prospect
- Immediate opt-out on "stop" / "unsubscribe"
- Sequential-only cross-channel contact
- De-duplicate against existing campaigns and Leadbay notes
