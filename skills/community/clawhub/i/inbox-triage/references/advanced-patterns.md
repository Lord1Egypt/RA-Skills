# Inbox Triage — Advanced Patterns

## Smart Batching

Instead of checking every hour, batch inbox checks with other periodic tasks:

```markdown
## Heartbeat Batch (every 2-4 hours)
1. Inbox triage (this skill)
2. Calendar check (next 4 hours)
3. Task list review
4. Deliver combined update
```

One API call, three checks. Efficient.

## Thread Tracking

Track ongoing email threads that need follow-up:

```markdown
## Active Threads (in daily memory notes)
- **[Client Name] — Contract Review** | Waiting on their reply since Mon | Follow up Wed if silent
- **[Vendor] — Invoice Dispute** | Sent clarification Tue | Escalate if no response by Fri
```

During each triage, cross-reference active threads. If a tracked thread gets a reply, bump it to 🟡 regardless of other scoring.

## Digest Mode

For high-volume inboxes (50+ emails/day), switch to digest mode:

```
📬 Daily Digest — [Date]

📊 Volume: 47 new emails
🔴 3 urgent (details below)
🟡 8 need action
🔵 15 FYI
⚫ 21 noise (auto-archived)

🔴 URGENT
1. [Detail]
2. [Detail]
3. [Detail]

🟡 TOP 3 ACTION ITEMS
1. [Detail]
2. [Detail]
3. [Detail]

Remaining 5 action items available on request.
```

Only expand categories when asked. Respects attention.

## Auto-Archive Rules

For ⚫ Noise items, optionally configure auto-archiving:

```bash
# himalaya example — move to archive
himalaya envelope move --folder INBOX --target Archive --ids [id1,id2,id3]

# Gmail label approach
gmail-archive --label "Agent-Archived" --ids [id1,id2,id3]
```

**Safeguards:**
- Only archive items scoring ≤ 0 on urgency scale
- Keep an "Agent-Archived" label/folder (never delete)
- Weekly review of archived items to catch false negatives
- First 2 weeks: log what WOULD be archived without acting (dry run)

## Sender Intelligence

Build a sender profile over time:

```json
{
  "sender_profiles": {
    "boss@company.com": {
      "avg_response_expected": "2h",
      "typical_urgency": "high",
      "usual_topics": ["project updates", "meeting requests"],
      "reply_rate": 0.95
    },
    "newsletter@techcrunch.com": {
      "avg_response_expected": null,
      "typical_urgency": "noise",
      "reply_rate": 0.0
    }
  }
}
```

Update profiles weekly. After a month, the agent knows your inbox better than you do.

## Escalation Chains

For time-sensitive inboxes (support, sales):

```markdown
## Escalation Rules
- 🔴 Urgent + no human response in 30 min → send reminder via Telegram
- 🔴 Urgent + no response in 2h → send to backup contact
- 🟡 Action Needed + no response in 24h → bump to next triage with ⚠️
```

## Weekend / Off-Hours Mode

```markdown
## Off-Hours Rules (after 6pm + weekends)
- Only surface 🔴 Urgent items
- Batch everything else for Monday morning briefing
- Exception: emails from [emergency-contacts list]
```

## Metrics & Weekly Review

Track inbox health over time:

```markdown
## Weekly Inbox Report
- Emails received: 234
- Avg daily volume: 33
- Response time (median): 4.2h
- 🔴 Urgent items: 7 (3% of total)
- Auto-archived: 89 (38%)
- Threads closed: 12
- Threads still open: 8
- Top senders: [list of 5]
```

Trends matter more than absolutes. If urgent volume spikes, something changed.

---

*Part of [The Agent Ledger](https://www.theagentledger.com) skill collection.*
