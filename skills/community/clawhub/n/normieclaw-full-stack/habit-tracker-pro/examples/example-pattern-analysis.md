# Example: Pattern Analysis

This shows how Habit Tracker Pro surfaces behavioral patterns after accumulating
enough data (14+ days). The user has been tracking 6 habits for 5 weeks.

---

## Scenario: Agent Surfaces Insights During Check-in

**Agent (morning check-in, Week 5):**

> Morning! Before we do the check-in — I've been looking at your data from the
> last 5 weeks and spotted a few things worth mentioning:
>
> **📊 Pattern spotlight:**
>
> 1. **Friday is your weak day.** Overall completion rate is 74%, but Fridays
>    drop to 38%. You've completed reading only once on a Friday in 5 weeks.
>    Gym is 2 for 5. Fridays just seem to fall apart.
>
> 2. **Meditation predicts everything else.** When you meditate, your other
>    habits complete at 88%. When you skip meditation, the rest drops to 41%.
>    It's your keystone habit.
>
> 3. **You skip gym the day after late check-ins.** When your evening check-in
>    response comes in after 11 PM (happened 8 times), you skip the next
>    morning's gym 75% of the time. Late nights → missed workouts.
>
> Want to dig into any of these, or should we just do today's check-in?

**User:**

> the friday thing is real. and the late night → gym skip is interesting. what would you suggest?

**Agent:**

> For Fridays — your data says it's not laziness, it's a different day. You
> tend to have work dinners or social stuff Thursday nights (I see 3 of your
> "tired" skip reasons are on Fridays after late Thursday responses). Two approaches:
>
> 1. **Make Friday a planned light day.** Keep just supplements and water — the
>    habits that take zero willpower. Drop gym, reading, and meditation from
>    Fridays specifically.
> 2. **Shift Friday habits to different times.** Instead of morning gym on Friday,
>    do an afternoon or evening session.
>
> For the late night → gym pattern — honestly, that might just be your body
> telling you something. If you're up past 11, a 6 AM gym session is going to
> be brutal. Options:
>
> 1. Make next-morning gym optional if your evening check-in comes in after 10:30 PM
> 2. Auto-swap to an evening workout on those days
>
> None of this is permanent. Try something for 2 weeks and we'll see what the
> data says.

**User:**

> let's do the light friday thing. and yeah, make gym optional after late nights

**Agent:**

> Done.
>
> ✅ Fridays updated: only Supplements and Water are scheduled. Meditation,
>    Gym, Reading, and Journaling are now optional on Fridays.
> ✅ Gym auto-adjusts: if your evening check-in is after 10:30 PM, next
>    morning's gym becomes optional (won't count as a miss).
>
> I'll check back in 2 weeks to see if Friday completion improves. Now —
> yesterday's check-in. How'd it go?

---

## Deeper Pattern Analysis (On Request)

**User (later that week):**

> can you give me a full breakdown of my habits? like the detailed version

**Agent:**

> **📊 Full Habit Analysis — 5 Weeks of Data**
>
> **Overall: 68% completion rate (143/210 scheduled)**
>
> **By Habit:**
> 🧘 Meditation — 77% (27/35) · Streak: 6 · Longest: 14
>    → Strong Mon-Thu. Weak Fri-Sun. Your anchor habit.
>
> 🏋️ Gym — 73% (11/15 scheduled MWF) · Streak: 3 · Longest: 8
>    → Solid when you sleep well. Drops after late nights.
>
> 📖 Reading — 60% (21/35) · Streak: 2 · Longest: 11
>    → Evenings only. Competes with screen time. Best on weekdays.
>
> 💊 Supplements — 91% (32/35) · Streak: 18 · Longest: 18 (active!)
>    → Your most consistent habit. Nearly automatic.
>
> 🥤 Water (64oz) — 54% (19/35) · Streak: 1 · Longest: 7
>    → Your weakest habit. No clear day pattern — just inconsistent.
>    Might need a different trigger or tracking method.
>
> 📓 Journaling — 57% (20/35) · Streak: 0 · Longest: 9
>    → Better since moving to evening. Was 40% as a morning habit,
>    now at 67% over the last 2 weeks.
>
> **Skip Reasons (all habits):**
> Tired: 28 times (42%)
> Busy: 19 times (28%)
> Forgot: 11 times (16%)
> Other: 9 times (13%)
>
> **Correlations:**
> Meditation ↔ Journaling: r=0.72 (strong — they rise and fall together)
> Meditation ↔ Gym: r=0.58 (moderate — meditation mornings lead to gym)
> Water ↔ Gym: r=0.45 (weak-moderate — gym days you drink more water)
>
> **Biggest win:** Supplements — 91% with an 18-day active streak.
> **Biggest opportunity:** Water — 54% with no clear pattern. Consider
> stacking it with something consistent (like supplements).

---

## What Makes This Different

Traditional habit apps show you a red/green grid and a streak number.
Habit Tracker Pro tells you:

- **Why** you're missing (day-of-week, time patterns, skip reason analysis)
- **What's connected** (which habits influence each other)
- **What to change** (specific, data-backed adjustment suggestions)
- **Whether changes worked** (2-week check-back on adjustments)

The data exists in every habit app. Nobody else reads it for you.
