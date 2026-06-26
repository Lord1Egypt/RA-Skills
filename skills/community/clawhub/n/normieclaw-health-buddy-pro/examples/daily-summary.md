# Example: Daily Nutrition Summary

This example shows what happens when a user asks "how am I doing today?"

---

## The Conversation

**User:** How am I doing today?

**Health Buddy Pro:**
> 📊 **Today's Snapshot** (March 8)
>
> **Calories:** 1,580 / 2,200 (620 remaining)
> ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░ 72%
>
> **Macros:**
> - Protein: 118g / 150g (32g to go — you're on track! 💪)
> - Carbs: 165g / 220g
> - Fat: 52g / 73g
>
> **Meals logged:**
> - ☀️ Breakfast: Overnight oats w/ banana — 380 cal
> - 🌤️ Lunch: Chipotle burrito bowl — 780 cal
> - 🍎 Snack: Apple + peanut butter — 420 cal
>
> **Water:** 💧 ████████░░ 48/64 oz (75%)
> Maybe grab another glass before dinner? 😊
>
> **Supplements:** ✅ All taken
>
> You've got ~620 cal left — perfect for a solid dinner. Want me to suggest something high-protein to close out the day?

**User:** Yeah, what should I have for dinner?

**Health Buddy Pro:**
> With 620 cal and 32g protein to hit, here are some ideas:
>
> 🥩 **Grilled salmon + roasted veggies** — ~520 cal, 40g protein
> 🍗 **Chicken stir-fry with broccoli** — ~480 cal, 38g protein
> 🥚 **Veggie omelette with side salad** — ~450 cal, 30g protein
>
> Any of those sound good? Or snap a photo of what you end up making!

---

## What's Happening Behind the Scenes

1. Agent reads today's entries from `data/nutrition-log.json`
2. Calculates running totals against targets in `config/health-config.json`
3. Reads `data/hydration-log.json` for water progress
4. Reads `data/supplement-log.json` for supplement status
5. Presents everything in a clean, motivating format
6. Proactively suggests dinner options to help hit remaining targets
