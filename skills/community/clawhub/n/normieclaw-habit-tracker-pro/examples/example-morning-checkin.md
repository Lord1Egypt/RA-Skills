# Example: Morning Check-in Conversation

This is a real example of how Habit Tracker Pro handles a daily morning check-in.
The user has 5 morning habits configured. Check-in is set for 8:00 AM.

---

## The Check-in

**Agent (8:00 AM):**

> Good morning! Quick check on yesterday:
>
> 🧘 Morning Meditation (10 min)
> 🏋️ Gym Session
> 💊 Supplements
> 🥤 64oz Water
> 📓 Morning Pages (journaling)
>
> How'd it go?

**User:**

> meditated, gym was solid, took supplements, definitely didn't drink enough water, and skipped morning pages

**Agent:**

> Got it. Logging:
>
> ✅ Meditation — done
> ✅ Gym — done
> ✅ Supplements — done
> ❌ Water (64oz) — missed
> ❌ Morning Pages — skipped
>
> 3 out of 5. Gym streak is at 9 sessions — nice run going.
>
> Morning Pages has been off 4 of the last 6 days. What's getting in the way?

**User:**

> honestly just running out of time in the morning. by the time I meditate and get ready for the gym there's no time left

**Agent:**

> Makes sense — the morning block is stacked pretty tight. Two options:
>
> 1. Move Morning Pages to evening — decouple it from the morning rush
> 2. Shorten it to 5 minutes instead of a full session — lower the bar so it actually happens
>
> Want to try one of those, or keep it as-is and see if this week goes better?

**User:**

> let's move it to evening

**Agent:**

> ✅ Morning Pages moved to evening check-in. I'll ask about it at 9 PM instead.
> Your morning block is now: Meditation → Gym → Supplements → Water. More breathing room.

---

## What Happened Behind the Scenes

1. Agent parsed natural language response and matched to 5 habits
2. Logged 3 completions and 2 skips in `completions.json`
3. Updated streak data in `streaks.json` (gym streak → 9)
4. Detected pattern: Morning Pages missed 4/6 recent days
5. Offered adjustment (not demanded)
6. Updated habit time_preference from "morning" to "evening" per user choice
