# Example: Goal Check-In

This example shows the weekly goal check-in and streak tracking flow.

---

## The Conversation

**User:** How's my week going?

**Health Buddy Pro:**
> 📊 **Week in Review** (Mar 2 – Mar 8)
>
> **Tracking streak:** 🔥 18 days! That's incredible consistency.
>
> **Daily averages:**
> - Calories: 2,080 avg (target: 2,200) — right in the zone ✅
> - Protein: 142g avg (target: 150g) — so close! A scoop of protein powder would close the gap
> - Carbs: 215g avg (target: 220g) ✅
> - Fat: 68g avg (target: 73g) ✅
>
> **Hydration:** Hit your 64oz target 5 out of 7 days 💧
>
> **Best day:** Thursday — nailed every single macro target 🎯
> **Toughest day:** Saturday — 2,650 cal (wing night, no regrets 😄)
>
> **Supplements:** 100% adherence this week! 💊✅
>
> **Weight trend:** 186 lbs → 184.5 lbs (down 1.5 lbs this week)
>
> Overall: You're crushing it. The consistency is what matters and you've got that locked down. Keep it up! 💪

**User:** Nice! I want to bump my protein target to 170g

**Health Buddy Pro:**
> Done! Updated your protein target from 150g → 170g per day.
>
> Quick tip: that's about 20g more protein daily. Easy ways to get there:
> - Add a protein shake post-workout (~25g)
> - Greek yogurt as a snack (~15g)
> - Extra chicken breast at lunch (~25g)
>
> I'll track against the new target starting today. You got this! 💪

---

## What's Happening Behind the Scenes

1. Agent reads the past 7 days from `data/nutrition-log.json` and calculates averages
2. Reads `data/hydration-log.json` for hydration adherence
3. Reads `data/supplement-log.json` for supplement streak
4. Reads `data/custom-metrics.json` for weight entries
5. Compares everything against targets in `config/health-config.json`
6. When user requests a target change, updates `config/health-config.json` and confirms
