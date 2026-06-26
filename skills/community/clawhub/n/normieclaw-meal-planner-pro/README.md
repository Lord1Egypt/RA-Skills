# 🍽️ Meal Planner Pro

**The AI meal planner that learns your family's tastes.**

End the "what's for dinner?" debate forever. Meal Planner Pro is an intelligent AI agent that learns what your household loves (and hates), plans your week, builds organized grocery lists, and gets smarter every time you rate a meal. Free and open-source., no subscriptions, no meal kits — just a really smart kitchen friend.

🛡️ **Codex Security Verified** — Your family's dietary data stays on your infrastructure. No third-party data harvesting, no forced lock-in.

---

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | Complete agent instructions — the brain |
| `SETUP-PROMPT.md` | First-run setup and household interview |
| `README.md` | This file |
| `config/dietary-profiles.md` | Reference: 12+ dietary styles with details |
| `config/cuisine-categories.md` | Reference: cuisine variety and balancing |
| `config/store-sections.md` | Reference: grocery store aisle organization |
| `examples/weekly-plan-example.md` | Sample: full weekly plan conversation |
| `examples/fridge-photo-example.md` | Sample: fridge photo → recipe suggestions |
| `examples/grocery-list-example.md` | Sample: organized grocery list output |
| `dashboard-kit/DASHBOARD-SPEC.md` | Companion dashboard build specification |

## Quick Start

1. **Install** — Copy the `meal-planner-pro/` folder into your OpenClaw skills directory.
2. **Setup** — Run through the interview in `SETUP-PROMPT.md` to build your household profile.
3. **Plan** — Say "plan my week" and let the AI do its thing. Rate meals, and watch it learn.

## What It Does

- **Weekly Meal Plans** — Balanced, personalized plans that respect every family member's allergies, dislikes, and adventurousness level.
- **Smart Grocery Lists** — Aggregated, organized by store aisle, with pantry staple awareness and estimated costs.
- **Fridge Photo Mode** — Snap a pic of what you have → get meal ideas using those ingredients.
- **Learning Engine** — Rate meals ❤️/👍/👎 per person. The agent remembers and adapts.
- **Freezer Tracking** — FIFO inventory so nothing goes to waste.
- **Prep Day Planner** — Timed schedules for Sunday meal prep warriors.
- **Party Mode** — Scale recipes and handle guest allergies for events.
- **Dietary Overrides** — Temporary weekly toggles without changing permanent profiles.
- **Leftover Intelligence** — Tracks yield and suggests lunch reuse.

## Requirements

- **OpenClaw** (any current version)
- **Vision-capable LLM** (for fridge photo mode — e.g., Claude, GPT-4o, Gemini)
- No paid APIs required beyond your existing LLM provider
