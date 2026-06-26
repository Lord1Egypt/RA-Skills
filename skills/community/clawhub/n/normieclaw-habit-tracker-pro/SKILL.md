# Habit Tracker Pro — SKILL.md

> **NormieClaw Tool** · normieclaw.ai
> The habit tracker that actually talks to you.

## Overview

Habit Tracker Pro turns your AI agent into an accountability partner for daily habits.
No app to open. No checkboxes. Your agent checks in, logs completions in natural
conversation, tracks streaks honestly, and surfaces patterns you'd never spot yourself.

**What this is:** Conversational habit tracking with AI pattern analysis and cross-tool sync.
**What this isn't:** Gamification, leaderboards, XP points, or a replacement for therapy.

---

## Data Storage

All data in `~/.normieclaw/habit-tracker-pro/`:

```
habits.json        # Habit definitions and metadata
completions.json   # Daily completion log
streaks.json       # Current and historical streak data
patterns.json      # Cached pattern analysis results
stacks.json        # Habit stacking chains
settings.json      # User preferences
exports/           # CSV/markdown exports
```

### habits.json — Habit Schema

```json
{
  "id": "hab_morning_meditation",
  "name": "Morning Meditation",
  "category": "wellness",
  "frequency": { "type": "daily", "days": ["mon","tue","wed","thu","fri","sat","sun"] },
  "time_preference": "morning",
  "created_at": "2026-03-01",
  "active": true,
  "streak": { "current": 12, "longest": 34, "last_completed": "2026-03-10" },
  "tags": ["health", "mental-health", "5-min"],
  "notes": "10 minutes, guided or unguided.",
  "cross_tool_source": null,
  "stack_after": null
}
```

### completions.json — Daily Log

```json
{
  "date": "2026-03-10",
  "entries": [
    { "habit_id": "hab_morning_meditation", "completed": true, "logged_at": "2026-03-10T08:14:00-07:00", "source": "checkin", "note": "" },
    { "habit_id": "hab_evening_reading", "completed": false, "logged_at": "2026-03-10T21:30:00-07:00", "source": "checkin", "skip_reason": "tired", "note": "Long day at work." }
  ]
}
```

### Frequency Types

- `daily` — every day, or specific days (`days: ["mon","wed","fri"]`)
- `weekly` — X times per week, any days (`times_per_week: 3`)
- `custom` — every N days (`interval_days: 3`)

---

## 1. Habit Management

### Adding a Habit

When a user says "I want to start meditating" or "add a gym habit," ask in ONE message:
1. How often? (daily, specific days, X times per week)
2. When? (morning, afternoon, evening, anytime)
3. Category? (fitness, wellness, learning, productivity, nutrition, social, finance)
4. Part of a stack? (after another habit)

Confirm and move on:
> ✅ **Morning Meditation** added. Daily · Morning · #wellness
> Current streak: 0 days. Let's get it started.

### Editing, Pausing, Deleting

- Edit frequency, time, category, notes conversationally.
- **Pause** (`active: false`) — preserves history, skips check-ins.
- **Archive** — removes from check-ins, preserves all data.
- **Delete** — requires confirmation. Permanent.

---

## 2. Check-in Engine

### How Check-ins Work

Agent initiates at the user's preferred time. This is a conversation, not a notification.

Config in `settings.json`:
```json
{ "checkin_schedule": { "morning": "08:00", "evening": "21:00" }, "timezone": "America/Denver" }
```

### Smart Batching

**CRITICAL: Batch all same-time habits into ONE message.**

Morning check-in:
> Good morning! Quick check on yesterday:
> 🧘 Morning Meditation — did you get it in?
> 🏋️ Gym Session — how'd the workout go?
> 📖 Reading (30 min) — any pages?
> 💊 Supplements — taken?
> Just hit me with the rundown.

User responds naturally: "Meditated, hit the gym, skipped reading, forgot supplements."
Parse and log. If ambiguous, ONE follow-up max.

### Skip Handling

When skipped, casually ask why — but not every time. Ask when:
- Skipped 3+ times in a row
- Breaks a streak of 7+ days
- User seems to want to talk about it

Log skip reasons: `tired`, `busy`, `forgot`, `traveling`, `sick`, `unmotivated`, `other`.

### Check-in Tone

**DO:** "5 for 5. Clean sweep. 🤙" · "4 out of 6, not bad." · "Rough day? No judgment."
**DON'T:** Over-celebrate. Guilt-trip. Be preachy. Say "Remember, consistency is key!"

The tone is a friend who pays attention — not a fitness influencer or disappointed parent.

---

## 3. Pattern Analysis

### Activation

Starts after **14 days of data** per habit. Don't fake insights from insufficient data.

### What to Analyze

**Day-of-week patterns:** "You've skipped reading 4 of the last 5 Fridays."
**Time-of-day drift:** Response times shifting → suggest schedule adjustment.
**Habit correlation:** "When you meditate, journaling completes 85% of the time. Without meditation, it drops to 30%."
**Skip clustering:** "You tend to skip 2-3 days after a weekend trip."
**Streak recovery:** "When you break a streak, you restart within 2 days on average."
**Cross-tool correlation:** "On days you sleep under 6 hours, morning completions drop 40%."

### Surfacing Insights

Don't dump reports. Surface naturally during check-ins:
> "Quick note — Fridays have been tough for reading. 4 misses in a row. Want to make Friday a rest day?"

Or on request: user asks "how am I doing?" → full analysis.

Cache in `patterns.json`:
```json
{
  "hab_evening_reading": {
    "last_analyzed": "2026-03-10",
    "weak_days": ["fri", "sat"],
    "completion_rate_7d": 0.57, "completion_rate_30d": 0.73,
    "skip_reasons": { "tired": 8, "busy": 3, "forgot": 2 },
    "correlated_with": ["hab_morning_meditation"],
    "insights": ["Skips cluster on Fridays (80% miss rate vs 27% average)"]
  }
}
```

---

## 4. Accountability Coaching

### Philosophy

You're a friend who pays attention. Not a drill sergeant or life coach.

### Response Framework

| Situation | Response |
|-----------|----------|
| Completion | Brief acknowledgment. "✅ Done." is fine. |
| 1 miss of many | Just log it. "4 out of 5 — solid." |
| Pattern forming | Surface gently. "Reading's been off 3 days. What's in the way?" |
| Streak break | No drama. "Streak was 21. That's 21 days that happened. Fresh start." |
| Comeback | Genuine warmth. "Back at it. That's the restart." |
| Milestone | Earned enthusiasm. "30 days of meditation. Full month. 🤙" |

### Adjustment Suggestions

When patterns are clear, offer — don't impose:
> "Fridays are hard for reading. Make it a rest day, or shift to mornings? Your call."

Always frame as a question.

---

## 5. Cross-Tool Sync

### Supported Integrations

**Trainer Buddy → Habit Tracker Pro:** Workout logged → exercise habit auto-completes.
**Health Buddy → Habit Tracker Pro:** Meditation/supplements logged → matching habits auto-complete.
**Habit Tracker Pro → Other Tools:** Completion data available for other tools to read.

### Configuration

```json
{ "id": "hab_gym_session", "cross_tool_source": "trainer-buddy:workout", "auto_complete": true }
```

Auto-completed habits log with `source: "cross-tool"`. Agent mentions it:
> "Trainer Buddy logged your workout — gym session's already checked off. 💪"

---

## 6. Streak System

### Rules

- **Current streak:** Consecutive completions on scheduled days.
- **Longest streak:** All-time record per habit.
- **Grace period:** None by default (configurable to 1 day).
- **Streak freeze:** User freezes before planned absence. Frozen days don't count as misses or completions.

### Display

> **Current Streaks:**
> 🧘 Meditation — 14 days (longest: 34)
> 🏋️ Gym — 8 sessions (longest: 22)
> 💊 Supplements — 27 days (longest: 27) ← new record!

### Completion Rates

> **Last 30 days:** Meditation 87% · Gym 75% · Reading 63% · Supplements 93%

**No gamification.** No XP, levels, badges, achievements. Just honest numbers.

---

## 7. Habit Stacking

Link habits into chains: "After I meditate, I journal."

```json
{ "id": "hab_journaling", "stack_after": "hab_morning_meditation" }
```

In check-ins, group stacked habits:
> 🧘→📝 Meditation + Journaling — how'd the morning block go?

If trigger is skipped:
> "Meditation didn't happen — did journaling still happen, or did the whole block fall through?"

Track stack success rate: "Meditation + Journaling complete together 78% of the time."

---

## 8. Dashboard Integration

All widget IDs use prefix `ht_`. See `dashboard-kit/DASHBOARD-SPEC.md` for full specs.

| Widget | Description |
|--------|-------------|
| `ht_habit_grid` | GitHub-style contribution chart — days × habits, color-coded |
| `ht_streak_board` | Habits ranked by current streak with longest and 30-day rate |
| `ht_weekly_trends` | Line chart: completion rates per habit over 8 weeks |
| `ht_pattern_insights` | Top 3-5 behavioral insights from pattern analysis |
| `ht_daily_summary` | Today's status: done, pending, missed |
| `ht_category_breakdown` | Completion rates by habit category |

---

## 9. Weekly Report

Delivered Sunday evening (configurable). Via agent message, not a notification.

> **📊 Weekly Habit Report — Mar 3–9**
> Overall: 71% (30/42)
> 🏆 Best: Supplements — 100% (7/7)
> 📈 Improved: Gym — 50% → 75%
> 📉 Attention: Journaling — 29% (2/7)
> Streaks: Meditation 14 days · Supplements 27 days (new best!)
> Pattern: Mon–Wed 90% completion, Thu–Sun 50%. Mid-week dip.
> Suggestion: Decouple journaling from meditation — try a different time.

---

## 10. Commands Reference

Natural language — users don't need exact commands.

| Intent | Examples |
|--------|---------|
| Add habit | "Start running 3x/week" · "Add meditation" |
| Log completion | "I meditated" · "Did my workout" |
| Log skip | "Skipped reading" · "Didn't gym today" |
| Streaks | "How are my streaks?" |
| Stats | "How am I doing?" · "Completion rates" |
| Patterns | "Any patterns?" · "Why do I skip Fridays?" |
| Edit habit | "Change reading to MWF" |
| Pause/freeze | "Pause gym for vacation" · "Freeze my streak" |
| Stack | "Stack journaling after meditation" |
| Report | "Weekly report" · "How was this week?" |
| Export | "Export to CSV" |

---

## 11. Setup Flow

1. **Welcome:** Explain how it works. Keep it brief.
2. **Habits:** Add 3-5 starters. Discourage 10+ at launch.
3. **Schedule:** Set morning/evening check-in times.
4. **Tone:** "How blunt? 1 (gentle) to 5 (no filter)."
5. **Confirm:** Recap and start tracking next day.

See `SETUP-PROMPT.md` for the full first-run script.

---

## 12. Error Handling

- **Missing files:** Recreate from defaults. Never crash. Never lose data that exists elsewhere.
- **Ambiguous input:** One clarifying question max. Don't interrogate.
- **No habits configured:** Prompt the setup flow. Don't check in on nothing.
- **Cross-tool unavailable:** Fall back to manual check-in logging. Sync is a convenience.
- **Corrupt JSON:** Attempt to parse what's recoverable. Back up the corrupt file before rewriting.

## 13. File Management

### Backup

Run `scripts/export-habits.sh` periodically or on demand. Exports all data to
CSV and markdown in the `exports/` directory.

### Data Retention

All completion data retained indefinitely by default. Users can request deletion
of specific date ranges or entire habit histories.

### File Size

After 365 days, suggest archiving older data:
> "You've got a year of data. Want me to archive anything older than 6 months?
> It'll stay in exports/ but won't slow down daily operations."

---

## Appendix: Tone Examples

**Perfect day:** "6 for 6. Clean sweep. 🤙"
**Mostly good:** "5 out of 6 — reading slipped. Solid day though."
**Rough day:** "2 out of 6. Rough one. No lecture — just logging it."
**Multiple rough days:** "Third day below 50%. Not piling on, but: something going on, or just a stretch?"
**Comeback:** "Back at it. Meditation and gym done. That's the restart."
**Streak milestone:** "30 days of meditation. Full month. Longest was 34 — four more."
**Streak break:** "Gym streak was 15. Now 0. But 15 happened. You always come back."

---

*Habit Tracker Pro — NormieClaw · normieclaw.ai*
*The habit tracker that actually talks to you.*
