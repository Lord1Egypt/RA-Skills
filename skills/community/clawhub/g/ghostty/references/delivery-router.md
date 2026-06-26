# Delivery Router — When to Send, When to Ask

Ghostty routes every draft through an escalation matrix. This document defines the logic.

## The Escalation Matrix

```
INCOMING MESSAGE
       ↓
┌─────────────────────────────────────────┐
│  Is sender in PRIORITY_SENDERS?         │
└─────────────────────────────────────────┘
       ↓ YES              ↓ NO
┌─────────────┐    ┌──────────────────┐
│  Send       │    │ Is sender in     │
│  directly   │    │ IGNORE_SENDERS?  │
│  (auto-send)│    └──────────────────┘
└─────────────┘         ↓ YES            ↓ NO
              ┌──────────┐    ┌─────────────────────┐
              │  Skip    │    │ Does it contain    │
              │  (log    │    │ URGENT_KEYWORDS?   │
              │   only)  │    └─────────────────────┘
              └──────────┘         ↓ YES            ↓ NO
                          ┌──────────────┐  ┌───────────────────┐
                          │  WhatsApp    │  │ Queue to pending- │
                          │  alert +     │  │ drafts.md + send  │
                          │  APPROVE     │  │ preview to        │
                          │  request     │  │ WhatsApp          │
                          └──────────────┘  └───────────────────┘
```

## Channel Routing Rules

| Situation | Channel | Why |
|-----------|---------|-----|
| PRIORITY sender, short reply | WhatsApp/Signal | Fast, direct |
| PRIORITY sender, formal/long | Email | More appropriate |
| Non-priority, urgent keyword | WhatsApp alert | Make sure I see it |
| Non-priority, standard | Pending draft + preview | I review and approve |
| Meeting invite (free) | Auto-accept + calendar | No action needed |
| Meeting invite (busy) | Decline + queue | Polite response, my voice |
| All-day event reminder | WhatsApp evening summary | Night before, single digest |

## Urgency Scoring

Each message gets an urgency score (0-10):

```
Base score = 0

+3  Sender is in PRIORITY_SENDERS
+2  Contains URGENT_KEYWORD (ASAP, urgent, critical, please respond, tomorrow...)
+2  First contact (new sender)
+2  Reply expected and overdue (past RESPONSE_WINDOW)
+1  Sent during my typical response hours
+1  Contains a question requiring my input
+1  Affects a project marked ACTIVE in config
-2  Sent during DND hours (score capped at 5)
-2  Newsletter/automated sender detected
-3  Unsubscribeable bulk email
```

**Routing thresholds:**
- Score 7+: WhatsApp immediate alert
- Score 4-6: Queue + WhatsApp preview (APPROVE request)
- Score 0-3: Queue only, no notification (review when convenient)

## One-Click Approval Format

When Ghostty sends a draft to WhatsApp for approval:

```
[Ghostty] ✉️ Draft Reply → {sender}

---
{message_body}
---

Length: {N} sentences | Tone: {tone} | Channel: {email|WhatsApp|Slack}

[✅ APPROVE] [✏️ EDIT] [⏭️ SKIP]
```

**On "APPROVE":**
→ Send immediately, log to `ghostty/sent-log.md`

**On "EDIT":**
→ Ghostty opens a reply thread — user types corrections, Ghostty applies them, sends when done

**On "SKIP":**
→ Log as skipped, remove from pending-drafts.md

## DND Hours

Respect `ghostty/availability.md`:

```
DND_HOURS: 23:00 - 07:00 [timezone]
```

During DND:
- Score is capped at 5 (no immediate WhatsApp alerts)
- Drafts queue silently
- Calendar reminders: still send 1hr before events, but softer tone ("Morning — heads up...")
- If PRIORITY sender sends DURING DND with URGENT keywords: still alert (it's urgent)

## Auto-Responses

For messages that don't need a response at all:

| Situation | Ghostty's Action |
|-----------|-----------------|
| "Thanks" / "Nice" / thumbs up | React with emoji, no draft |
| Out-of-office reply received | Note in pending-drafts.md, no reply needed |
| Meeting invite (accepted) | Mark in calendar state, no reply needed |
| Newsletter confirmation | Skip, no action |
| Request I can't fulfill | Draft in voice explaining limitation, queue |

## Sent Log Format

Every sent draft gets logged to `ghostty/sent-log.md`:

```markdown
## YYYY-MM-DD HH:MM [Channel]

**To:** {sender}
**In response to:** {subject/excerpt of what they said}
**Intent:** {question/request/update/etc}
**Urgency score:** {0-10}
**Routed:** {direct/approved}

---
{message_body}
---
```
