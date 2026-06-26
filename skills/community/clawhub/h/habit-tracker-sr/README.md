# HabitTracker — Conversational Habit Tracking

Track habits by talking to your agent. No app switching, no manual logging.

## How It Works

```
Agent: "Morning check-in: Exercise? Water? Reading?"
You: "Ran 3 miles, drank 64oz, no reading"
Agent: "Logged. Exercise: 🔥 12-day streak! Reading: streak broken at 5."
```

## Setup

```yaml
habits:
  - name: exercise
    frequency: daily
    prompt: "Did you exercise today?"
    streak_emoji: "🔥"
  - name: water
    frequency: daily
    unit: oz
    target: 64
  - name: reading
    frequency: daily
    target: 30  # minutes

check_in_time: "08:00"
evening_review: "21:00"
```

## Features

- **Conversational logging** — no forms, just chat
- **Streak tracking** — current and longest streaks
- **Smart reminders** — evening ping for missed habits
- **Weekly report** — completion rates, trends
- **Flexible frequency** — daily, weekdays, 3x/week, custom
- **Trend analysis** — "Your exercise consistency dropped this week"

## Weekly Report

```
📊 Weekly Habits — Feb 22-28

Exercise:  ██████░ 6/7 (86%) 🔥 18-day streak
Water:     ███████ 7/7 (100%) 🔥 31-day streak
Reading:   ████░░░ 4/7 (57%) streak: 2 days

Overall: 68% (up from 61% last week)
```
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
