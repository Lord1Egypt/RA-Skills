---
**⚠️ Important: Not Medical Advice**
This skill is for medication reminder and tracking purposes only. It does not provide medical guidance, diagnoses, or treatment recommendations. Always consult a healthcare professional regarding any medication decisions.
---

# Pill Reminder — OpenClaw Skill

**Never miss a dose. Track it. Print it for your doctor.**

---

## ⚠️ Disclaimer

**This skill does not provide medical advice.**

The reminder warnings and adherence tracking are for informational purposes only. They are not a substitute for professional medical guidance. Always consult your doctor or pharmacist regarding any medication-related decisions.

---

## What It Does

Pill Reminder sends scheduled medication alerts to your preferred chat channel, logs whether you took each dose, and reminds you when it's time to refill. Everything is stored locally — no cloud, no accounts to create.

**Features:**
- ✅ Daily reminders at times you choose
- ✅ Works with GroupMe, Discord, Telegram, and more
- ✅ Tracks `took` vs `didn't take` with a printable adherence log
- ✅ Refill alerts when pill counts run low
- ✅ Supports multiple people (you, a child, a parent — anyone)
- ✅ One-time setup, simple text commands to manage

---

## Who It's For

Anyone who takes daily medication or supplements and wants a simple, low-friction way to stay on track — and have a clean log ready for their next doctor visit.

---

## Setup

**Step 1: Install**

This skill is available on ClawHub. Install via the OpenClaw CLI:

```
clawhub install pill-reminder
```

Or ask your OpenClaw assistant: `install pill reminder from clawhub`

**Step 2: Initialize**

Say to your assistant:
```
setup pill reminder
```

You'll answer a few questions:
1. **Which channel?** (GroupMe, Discord, Telegram, etc.) — pick where you want reminders to land
2. **Your name** — used for your profile
3. **Your first pill** — name, how many pills are in the bottle, when to take it

That's it. The skill creates your config file and schedules the cron jobs automatically.

**Step 3: Add family members**

```
add family [name]
```

Then add pills for them the same way you added yours.

---

## Commands

| Say this | What happens |
|----------|--------------|
| `add pill [name] [count] at [time]` | Add a pill. Include current pill count so refill alerts work. Times can be comma-separated for multiple doses daily. |
| `add pill [name] [count] at [time] refill [N]` | Same, but set a custom refill threshold (alerts when pill count hits N). |
| `remove pill [name]` | Remove a pill from your profile. |
| `add family [name]` | Add a new person to your account. |
| `list pills` | See all your pills, times, and current counts. |
| `list family` | See everyone in your account. |
| `print log [name]` | Generate a clean, printable report for a doctor visit. |
| `set channel [channel]` | Change where reminders are sent (e.g., `set channel discord`). |
| `show config` | Display your current pills.md file. |
| `help pill-reminder` | Show this command list. |

---

## How Reminders Work

When it's time to take a pill, you'll get a message like this:

```
💊 Pill Reminder — Brian
Vitamin D (42 left)
Reply: `took` or `didn't take`
```

**If you reply `took`:**
It's logged. Pill count decrements. If you've hit the refill threshold, you'll get a refill alert.

**If you reply `didn't take`:**
You'll see a gentle reminder about the importance of consistency, followed by:
> *This is not medical advice.*

Then it's logged as missed.

---

## Refill Alerts

When your pill count drops to the threshold you set (default: 7), you'll receive:

```
🔔 Refill Reminder: Vitamin D is running low (7 left)
```

Set a custom threshold when adding a pill:
```
add pill Vitamin D 60 at 8am refill 10
```

---

## Printable Adherence Log

Need to show your doctor how you've been doing? Say:

```
print log Brian
```

You'll get a clean report:

```
PILL REMINDER — ADHERENCE REPORT
Generated: 2026-04-18
Person: Brian

====================================
PILL: Vitamin D
------------------------------------
TAKEN: Mar 1, 3, 5, 8, 10, 12, 15, 17
MISSED: Mar 2, 7

Adherence Rate: 80%
Refills Remaining (est): 6
====================================
```

Print it, email it, show it at your appointment.

---

## Data & Privacy

All data lives in your OpenClaw workspace. Your medication list and adherence history never leave your machine unless you choose to send them via a chat channel. No external servers, no cloud sync of medical data.

---

## Requirements

- OpenClaw installed and running
- A messaging channel configured (GroupMe, Discord, Telegram, etc.)
- Cron enabled (standard on all OpenClaw installs)

---

## Troubleshooting

**Reminders aren't firing?**
Check that your channel is configured correctly. Say `show config` to see what's set.

**Wrong time?**
Times are in 12-hour format (e.g., `8am`, `12:30 PM`). Make sure your OpenClaw timezone is set correctly.

**Need to change a pill time?**
Remove the pill and re-add it with the correct time:
```
remove pill Vitamin D
add pill Vitamin D 60 at 9am
```

---

*Built on OpenClaw. Install from ClawHub.*

---
**Author:** Brian Goodwin