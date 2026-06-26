# Pill Reminder Skill

**⚠️ Important: Not Medical Advice**
This skill is for medication reminder and tracking purposes only. It does not provide medical guidance, diagnoses, or treatment recommendations. Always consult a healthcare professional regarding any medication decisions.

---

**Skill ID:** `pill-reminder`  
**Version:** 1.0.0  
**Author:** Brian Goodwin

---

## What It Does

Sends daily medication/supplement reminders at user-defined times. Tracks adherence with a printable log for doctor visits. Supports multiple people (user + family members). Includes refill reminders.

**Reminder Flow:**
1. Cron fires → reminder sent to your configured channel
2. You reply `took` or `didn't take`
3. If `took` → logged ✅
4. If `didn't take` → general warning + "Not medical advice" disclaimer → then logged

---

## Setup

Run once to initialize:

```
setup pill reminder
```

This creates `pills.md` in your workspace. You'll answer:
1. **Channel** — GroupMe, Discord, Telegram, etc.
2. **Your name** — for your profile
3. **First pill** — name, pill count, refill threshold, time(s)

---

## Commands

Speak naturally. The skill parses your intent.

| Command | Description |
|---------|-------------|
| `add pill [name] [count] at [time]` | Add a pill. Count = current number in bottle. Times comma-separated for multiple daily doses. Default refill threshold = 7. |
| `add pill [name] [count] at [time] refill [N]` | Same with custom refill alert threshold. |
| `remove pill [name]` | Remove a pill from your profile. |
| `add family [name]` | Add a new person profile (child, spouse, etc.) under your account. |
| `list pills` | Show all pills and schedules for your profile. |
| `list family` | Show all profiles in your household. |
| `print log [name]` | Output a doctor-friendly adherence report for a person. |
| `set channel [channel]` | Change where reminders are sent (groupme, discord, telegram, etc.) |
| `show config` | Display the current pills.md content. |
| `help pill-reminder` | Show this command list. |

---

## "Didn't Take" Warning Language

When user replies `didn't take`, send this before logging:

```
⚠️ Skipping doses can reduce effectiveness. Consistency matters for most medications to work as intended. If missing doses becomes a pattern, consider talking with your doctor or pharmacist.

*This is not medical advice.*
```

---

## Refill Alert Format

When pill count drops to refill threshold:

```
🔔 Refill Reminder: [pill name] is running low ([count] left)
```

Fires automatically when logging a `took` that brings count to or below threshold.

---

## Cron Job Per Pill

Each pill dose gets its own cron job. Format: `X Y * * 1-6` (Mon-Sat at specified hour/min).

When adding a pill with multiple times, create one cron per dose.

---

## Reminder Message Format

```
💊 Pill Reminder — [profile name]
[pill name] ([count] left)
Reply: `took` or `didn't take`
```

---

## Printable Log Format

When `print log [name]` is called, output:

```
PILL REMINDER — ADHERENCE REPORT
Generated: [DATE]
Person: [NAME]

====================================
PILL: [pill name]
------------------------------------
TAKEN:
  - [date]
  - [date]
  - [date]
MISSED:
  - [date]
  - [date]

Adherence Rate: [X]%
Refills Remaining (est): [N]
====================================

Notes: [any logged notes]

---
Prepared for medical review.
```

---

## Data Files

| File | Location | Purpose |
|------|----------|---------|
| Config | `~/.openclaw/workspace/pills.md` | All profiles, pills, schedules, counts |
| Log | `~/.openclaw/workspace/pill-log.md` | Adherence history, dates taken/missed |

---

## Setup Behavior

On first `setup pill reminder`:

1. Ask for channel preference
2. Ask for profile name
3. Offer to add first pill immediately
4. Create `pills.md` with skeleton profile
5. Create cron job(s) for each dose time

On `add family [name]`:

1. Create new profile section in `pills.md`
2. Ask if they want to add pills for this person now

---

## Technical Notes

- Channel must be configured in OpenClaw before use
- "took" / "didn't take" matching is case-insensitive
- Times support 12hr format (8am, 8:00 AM, etc.)
- Reminders fire Mon-Sat by default
- All data stored locally — no cloud, no external API calls except to your messaging channel