# Skill: Morning Brief

**Purpose:** JB's daily wake-up brief. Consolidates everything into one message.

**Trigger:** Daily 7 AM CDT (cron)

**Replaces:** Old "Morning Pulse" + "RCM Pulse Daily"

---

## What It Includes

### 1. Weather (Mission, KS)
- Garmin weather via wttr.in
- Running conditions (temp, humidity, wind, feels-like)

### 2. RCM Pulse (1 insight)
- Top healthcare revenue cycle news
- 1 actionable insight max

### 3. Pittsburgh Sports
- Penguins/Steelers/Pirates scores or next game
- API: BallDontLie for NFL/MLB, web search for NHL

### 4. Fantasy Baseball (season only)
- If MLB season active: brief FA update
- If offseason: skip

---

## Output Format

```
☀️ MORNING BRIEF — March 21, 2026

🏃 RUNNING
High 68° • Low 45° • Wind 12 mph • Run conditions: Good

📰 RCM PULSE
Payer behaviors now #1 risk to revenue (denials up 11.8%). 

🏒 PENGUINS: Next Sat vs WPG 1:00 PM
🏈 STEELERS: Draft Apr 24
⚾ PIRATES: Season starts March 26

📡 Fantasy: Week 1 FA — monitor Cody Ponce, Luke Weaver
```

---

## Cron

```json
{
  "name": "morning-brief",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "America/Chicago" },
  "payload": { "kind": "agentTurn", "message": "Run Morning Brief skill. Get weather, RCM news, Pittsburgh sports, fantasy update. Post to JB." },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce", "channel": "discord" }
}
```

---

## Quality Rules
- Keep under 300 words
- Lead with weather (most actionable)
- Only 1 RCM insight (not 3)
- Sports: lead with what's playing soon
- Skip fantasy if offseason

---

## Files
- `/workspace/skills/morning-brief/SKILL.md` (this)
