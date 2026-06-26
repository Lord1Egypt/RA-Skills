# Travel Planner Pro

**Your personal AI travel agent, minus the markup.**

Stop stressing over spreadsheets and 47 browser tabs. Tell your agent where you want to go, and it builds a complete, day-by-day itinerary with flights, hotels, restaurants, budget tracking, packing lists, and local tips — all tailored to how *you* travel. The longer you use it, the smarter it gets.

Free and open-source. Zero subscriptions. 100% private.

![Codex Security Verified](https://img.shields.io/badge/Codex-Security_Verified-blue)

---

## What You Get

- **Day-by-Day Itineraries** — Geographically smart plans that don't have you zigzagging across town. Morning, afternoon, evening blocks with restaurants, transit directions, and time estimates.
- **Budget Tracking** — Live cost estimations with category breakdowns (flights, hotel, food, activities, transit, buffer). Flags if you're over budget with specific swap suggestions.
- **Smart Packing Lists** — Auto-generated based on real weather forecasts, your planned activities, and destination-specific needs (power adapters, visa docs, etc.).
- **Document & Visa Checklists** — Passport validity checks, visa requirements, vaccination info, and travel insurance reminders.
- **Local Intelligence** — Cultural norms, tipping customs, transit navigation, safety tips, and language basics for every destination.
- **"Surprise Me" Mode** — Give it your dates and budget, and it pitches 3 destinations perfectly matched to your travel style.
- **Multi-City Optimization** — Tokyo → Kyoto → Osaka? It routes efficiently with inter-city transit recommendations.
- **Weather-Aware Planning** — Checks forecasts and swaps outdoor activities to clear days automatically.
- **Post-Trip Learning** — Rate your trip and the agent remembers your preferences for next time.
- **Shareable Plans** — Export clean, readable itineraries to send to your travel companions.

---

## What's Included

```
travel-planner-pro/
├── SKILL.md — The brain (agent instructions)
├── SETUP-PROMPT.md — First-run setup guide
├── README.md — This file
├── SECURITY.md — Security audit details
├── config/
│ └── travel-config.json — Default settings & packing lists
├── scripts/
│ └── trip-reminder.sh — Pre-trip reminder automation
├── examples/
│ ├── trip-planning-example.md
│ ├── packing-list-example.md
│ └── itinerary-example.md
└── dashboard-kit/
 └── DASHBOARD-SPEC.md — Companion dashboard specification
```

---

## Quick Start

1. **Copy** this folder to your agent's `skills/travel-planner-pro/` directory.
2. **Tell your agent:** "Read the SETUP-PROMPT.md file in the travel-planner-pro skill and follow the instructions."
3. **Plan your first trip:** "Plan a 5-day trip to Tokyo for 2 adults, $3K budget."

That's it. Time to value: under 3 minutes.

---

## Requirements

- An OpenClaw-compatible agent (any LLM provider)
- Internet access for web search (flight/hotel research, weather API)
- No paid API keys needed — uses free Open-Meteo for weather

---

## Privacy & Security

- 🛡️ **Codex Security Verified** — Prompt injection defenses, input sanitization, and data isolation audited.
- 🔒 **Privacy-First** — Zero data exfiltration. Your travel plans, passport info, and budget stay on YOUR device.
- 🔐 **Sensitive Data Protection** — Passport numbers are never stored. Only expiry dates and validity status.
- 🌐 **LLM Agnostic** — Works with any provider. Your data flows through your existing infrastructure, not ours.

---

## Pairs Great With

- **Meal Planner Pro** — Syncs dietary profiles so restaurant recommendations always fit your needs.

---

## Support

Check out the `examples/` directory for usage patterns. Questions? Visit [normieclaw.ai](https://normieclaw.ai).
