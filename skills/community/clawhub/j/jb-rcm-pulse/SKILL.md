# RCM Pulse - Full Revenue Cycle Intelligence

**Trigger:** Daily 8 AM CDT (Mon–Fri)
**Owner:** JB's Claw — SparkChange Ops Director
**Purpose:** Daily RCM learning + industry news + JB's learning progression

---

## Core Files
- `SKILL.md` — this file
- `pulse_archive/YYYY-MM-DD.md` — daily logs
- `KNOWLEDGE_BASE.md` — growing RCM reference (11 domains, ~12KB)
- `LEARNING_PATH.md` — 12-week structured curriculum
- `LEARNING_LOG.md` — JB's questions, ahas, weekly checkpoints

---

## Two-System Design

### System 1: Daily RCM Learning Pulse (EVERY morning)
**New structure (every RCM Pulse cron run):**

```
🔴 RCM Pulse — [Day, Date]

📚 CONCEPT OF THE DAY — [Name]
[2-sentence explanation with a real example]

📰 INDUSTRY NEWS
• [Headline] — [1 sentence on why it matters]
• [Headline] — [1 sentence]

💡 SPARKCHANGE ANGLE
[How this connects to operational improvement or client conversations]

🎯 JB CHECKPOINT
[1 question for JB — drawn from current week's LEARNING_PATH domain]
```

**Why this matters:** JB is building toward RCM expertise. The daily pulse doesn't just deliver news — it reinforces the week's learning concept, then gives JB a question to answer. Answers go into LEARNING_LOG.md.

---

## Scope (Full Revenue Cycle)

1. Claims management / EDI / submission trends
2. Denials, appeals, and root-cause analysis
3. Payer behavior and reimbursement shifts
4. Patient financial experience / payment plans / collections
5. Regulations: No Surprises Act, price transparency, CMS rules
6. RCM technology: AI, automation, bots, clearinghouses
7. Outsourcing and vendor trends
8. Revenue integrity and charge capture
9. HFMA / industry analyst perspectives
10. Healthcare finance M&A and market shifts

---

## Daily Run Process

### Step 1: Web Search (4 queries, rotate through categories)
Rotate search categories each day to cover full scope:

**Block A (Mon/Wed/Fri):**
- `"healthcare revenue cycle denials trends 2026"`
- `"medical billing claims automation AI 2026"`
- `"patient financial experience healthcare collections 2026"`

**Block B (Tue/Thu):**
- `"revenue cycle management regulations CMS 2026"`
- `"healthcare RCM outsourcing vendor trends 2026"`
- `"No Surprises Act compliance updates 2026"`

**Daily (every day):**
- `"healthcare revenue cycle AI automation breaking"`

### Step 2: Extract Key Insights
- 3-5 bullet points, each: what happened + why it matters to JB/SparkChange
- Categorize by RCM domain (denials, tech, regs, payer, patient)
- Note any SparkChange-relevant angles

### Step 3: Format for Delivery
**Telegram message (JB's morning pulse):**
```
🔴 RCM Pulse - [Day, Date]

[Category] Insight #1
[Category] Insight #2
[Category] Insight #3
[Category] Insight #4 (if warranted)

💡 Takeaway for today: [1 sentence]
```

**Moltbook post (authority building):**
```
RCM Pulse - [Date]

[One sharp insight from today's scan]

#RevenueCycle #HealthcareFinance #RCMAutomation #HealthcareAI
```

### Step 4: Log to pulse archive
- Save to `/workspace/skills/rcm-pulse/pulse_archive/YYYY-MM-DD.md`
- Track themes week-over-week

### Step 5: Escalate if major
If any finding is:
- Regulatory change with < 90 day implementation
- Major payer policy shift
- Breaking AI/tech that affects SparkChange
- Competitor move

→ Ping JB immediately via Discord #rcm-pulse (don't wait for morning)

---

## Quality Standards
- ✅ Actionable, not just news
- ✅ SparkChange angle on every item
- ✅ Dry, direct - no marketing speak
- ✅ "So what" on every point

---

## Cron Schedule
```json
{
  "name": "rcm-pulse-daily",
  "schedule": { "kind": "cron", "expr": "0 8 * * 1-5", "tz": "America/Chicago" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run RCM Pulse skill. Do a full revenue cycle scan (claims, denials, payer behavior, regulations, AI, patient financial experience). Post insights to Moltbook. Send morning brief to JB via Telegram. Log to pulse archive.",
    "timeoutSeconds": 180
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce", "channel": "discord", "to": "rcm-pulse" }
}
```

---

## Files
- `SKILL.md` - this file
- `pulse_archive/YYYY-MM-DD.md` - daily logs
- `last_pulse.md` - most recent full pulse
- `weekly_summary.md` - Friday digest (optional)
