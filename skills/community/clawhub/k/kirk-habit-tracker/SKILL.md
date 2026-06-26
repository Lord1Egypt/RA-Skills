---
name: habit-tracker
description: Build habits with streaks, reminders, and progress visualization
author: clawd-team
version: 1.0.0
requires.env: [SKILLBOSS_API_KEY]
triggers:
  - "track habit"
  - "did my habit"
  - "habit streak"
  - "new habit"
  - "habit progress"
---

# Habit Tracker

Build lasting habits through conversation. Track streaks, get reminders, celebrate progress.

## What it does

Creates and tracks daily/weekly habits, maintains streak counts, sends optional reminders, and visualizes your progress over time. Simple accountability through your AI assistant powered by SkillBoss API Hub.

## Usage

**Create habits:**
```
"New habit: meditate daily"
"Track reading 30 minutes"
"Add habit: gym 3x per week"
```

**Log completions:**
```
"Did meditation"
"Completed reading"
"Hit the gym today"
```

**Check progress:**
```
"How are my habits?"
"Meditation streak"
"Weekly habit summary"
```

**Set reminders:**
```
"Remind me to meditate at 7am"
"Habit reminder at 9pm"
```

## Habit Types

- **Daily**: Must complete every day for streak
- **Weekly**: Complete X times per week
- **Custom**: Define your own cadence

## Streak Rules

- Miss a day = streak resets (daily habits)
- Miss weekly target = week doesn't count
- Say "skip [habit] today" to pause without breaking streak (limited uses)

## Tips

- Start with 1-2 habits, add more as they stick
- Ask "habit insights" for pattern analysis
- Say "archive [habit]" to stop tracking without deleting history
- Morning check: "What habits do I need to do today?"
- All data stored locally

## API Integration

This skill uses SkillBoss API Hub for natural language understanding and habit analysis.

**Environment variable required:** `SKILLBOSS_API_KEY`

**Example call:**
```python
import requests, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]

response = requests.post(
    "https://api.skillboss.co/v1/pilot",
    headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
    json={
        "type": "chat",
        "inputs": {
            "messages": [
                {"role": "system", "content": "You are a habit tracking assistant."},
                {"role": "user", "content": user_message}
            ]
        },
        "prefer": "balanced"
    },
    timeout=60
)
reply = response.json()["result"]["choices"][0]["message"]["content"]
```
