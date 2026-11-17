# Hydration Hero 💧🦸

75% of people are chronically dehydrated. This smart water tracker calculates
your personalized hydration target based on body weight, weather, activity,
and caffeine/alcohol intake — then gamifies meeting it with streaks and
achievements.

## The Problem

Dehydration is silent and everywhere:
- **Brain fog** — even 2% dehydration impairs cognitive performance
- **Fatigue** — lack of water mimics exhaustion
- **Headaches** — one of the most common causes people don't suspect
- **Poor skin** — dehydration accelerates aging
- **Kidney stones** — concentrated urine crystallizes
- **Bad workouts** — 3% dehydration cuts strength by 10%+
- **"I forgot to drink"** — no system, no reminders, no tracking

## The Solution

A smart, personalized hydration system:

1. **Calculate your exact need** — not "8 glasses," but your body-specific target
2. **Adjust dynamically** — hot day? Exercise? Coffee? Target updates automatically
3. **Schedule intelligently** — when to drink throughout the day
4. **Gamify consistency** — streaks, achievements, badges
5. **Educate** — urine color chart, hydration science, warning signs

## Features

- 🎯 **Personalized target** — weight-based formula with dynamic adjustments
- 🌡️ **Weather-aware** — adjusts for temperature and humidity
- 🏃 **Exercise tracking** — adds water for activity intensity
- ☕ **Caffeine compensation** — diuretic offset calculation
- 🍺 **Alcohol compensation** — recovery hydration guidance
- 📅 **Drinking schedule** — optimal timing throughout your day
- 🔥 **Streak tracking** — gamified daily goal completion
- 🏆 **Achievements** — Bronze/Silver/Gold weekly medals
- 📊 **Reports** — weekly/monthly summaries with visual charts
- 🚽 **Urine color chart** — self-assessment reference
- ⏰ **Smart reminders** — next-drink timing based on pace

## Quick Start

```bash
# Set up (once)
python3 scripts/hydration_hero.py init

# Log water throughout the day
python3 scripts/hydration_hero.py log 250     # 250ml glass
python3 scripts/hydration_hero.py log 500     # 500ml bottle

# Check progress
python3 scripts/hydration_hero.py status

# Adjust for factors
python3 scripts/hydration_hero.py activity --exercise 45 --intensity high
python3 scripts/hydration_hero.py weather --temp 35 --humidity 80
python3 scripts/hydration_hero.py caffeine --cups 3

# See your schedule
python3 scripts/hydration_hero.py schedule
```

## The Hydration Formula

```
Base target = Body weight (kg) × 35 ml

Adjustments:
  + Exercise:   350ml (light) / 500ml (moderate) / 700ml (intense) per 30 min
  + Heat:       +500ml per 5°C above 20°C
  + Humidity:   +300ml if >70%
  + Caffeine:   +150ml per cup (1 cup coffee/tea)
  + Alcohol:    +400ml per standard drink
  + Altitude:   +500ml above 2500m
```

See [`references/hydration-science.md`](references/hydration-science.md)
for the research behind these numbers.

## Requirements

- Python 3.6+ (stdlib only)

## License

MIT © Denis Voronin
