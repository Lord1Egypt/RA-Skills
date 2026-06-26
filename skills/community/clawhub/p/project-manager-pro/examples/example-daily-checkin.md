# Example: Daily Check-In Conversation

> Agent delivers morning check-in at 8:00 AM on Wednesday, March 11

---

## Morning Check-In

**Agent:**
```
☀️ Morning — Wednesday, March 11

🔴 OVERDUE (1):
  • Submit Q4 expense report (was due Mar 9) · P2 · ~45 min

📋 TODAY (4):
  • Review hot sauce label proof from designer · P1 · ~20 min
  • Call co-packer to confirm March production slot · P1 · ~15 min
  • Write product descriptions for 3 SKUs · P2 · ~60 min
  • Update budget spreadsheet with ingredient costs · P3 · ~30 min

🚫 BLOCKED (1):
  • Order packaging materials — waiting on "Finalize label design" (in-progress)

⚡ QUICK WINS:
  • Reply to vendor email about shipping rates · P4 · ~5 min
  • Renew GoDaddy domain (expires Mar 15) · P3 · ~5 min

What do you want to tackle first?
```

**User:** "Let me knock out those quick wins first, then the label review"

**Agent:**
```
Good call — starting light and building momentum.

🔄 In-progress: Reply to vendor email
🔄 In-progress: Renew GoDaddy domain

I'll have "Review hot sauce label proof" queued up next. Let me know when the quick wins are done.
```

**User:** "Done with both. The domain renewal is actually due the 18th not the 15th, fix that"

**Agent:**
```
✅ Done: Reply to vendor email
✅ Done: Renew GoDaddy domain
📅 Updated due date: Mar 15 → Mar 18

Next up: Review hot sauce label proof · P1 · ~20 min
```

**User:** "Reviewed the label, it needs changes. I sent feedback to the designer. Block the packaging order until the label is finalized."

**Agent:**
```
✅ Done: Review hot sauce label proof
📝 Note added: "Feedback sent to designer, revision needed"
🚫 Confirmed blocked: Order packaging materials — still waiting on label finalization

3 down, 3 to go. The co-packer call is P1 — want to do that next?
```

**User:** "Yeah, calling now"

**Agent:**
```
🔄 In-progress: Call co-packer to confirm March production slot

Let me know how it goes.
```

**User:** "Production confirmed for March 25. They need final labels by March 20."

**Agent:**
```
✅ Done: Call co-packer to confirm March production slot
📝 Note: "Production confirmed Mar 25. Labels due to co-packer by Mar 20."

⚠️ This means "Finalize label design" just became more urgent — 
   the designer revision + your approval + print-ready files all need 
   to happen before Mar 20.

I've escalated "Finalize label design" to P1 and set a hard deadline of Mar 18 
(2-day buffer before the Mar 20 co-packer deadline).

Updated dependency chain:
  🔄 Finalize label design (P1, due Mar 18)
  └── 🚫 Order packaging materials (blocked)
      └── 🔲 Ship materials to co-packer (due Mar 22)
          └── 🔲 Production run (Mar 25)
```

---

## Evening Review

**Agent (7:00 PM):**
```
🌙 Evening Review — Wednesday, March 11

✅ Completed today (5):
  • Reply to vendor email
  • Renew GoDaddy domain
  • Review hot sauce label proof
  • Call co-packer — production confirmed Mar 25
  • Write product descriptions for 3 SKUs

🔄 Carrying over (2):
  • Update budget spreadsheet · P3 · moved to tomorrow
  • Submit Q4 expense report · P2 · overdue day 3

📊 Week progress: 9/16 tasks done (56%)

5 tasks knocked out — solid day. The expense report is stacking up though. 
Want me to bump it to P1 for tomorrow?
```

**User:** "Yeah, make it P1. I'll do it first thing."

**Agent:**
```
✅ Submit Q4 expense report → P1, first on tomorrow's list.

See you in the morning. 🌙
```
