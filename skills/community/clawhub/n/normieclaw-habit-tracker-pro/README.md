# Habit Tracker Pro

**The habit tracker that actually talks to you.**

A NormieClaw tool package for OpenClaw agents. Turns your AI agent into a
conversational accountability partner for daily habits — with check-ins,
streak tracking, pattern analysis, and cross-tool sync.

## What It Does

- **Conversational check-ins** — Your agent reaches out daily, asks how your
  habits went, and logs responses from natural language. No app to open.
- **Pattern analysis** — After 2+ weeks of data, surfaces insights you'd miss:
  "You skip gym every day after a late night." Correlates habits with each other,
  days of week, skip reasons, and cross-tool data.
- **Honest accountability** — Celebrates wins briefly. Handles misses without
  guilt. Offers adjustment suggestions when patterns emerge. Never preachy.
- **Streak tracking** — Current streaks, longest streaks, completion rates over
  7/30/90 days. No XP, no badges, no gamification. Just honest numbers.
- **Habit stacking** — Link habits into chains. "After I meditate, I journal."
  Agent reminds you about the chain, not individual habits.
- **Cross-tool sync** — Gym habit auto-completes when Trainer Buddy logs a
  workout. Meditation syncs with Health Buddy. No double entry.
- **Dashboard widgets** — Contribution grid, streak board, weekly trends,
  pattern insights, daily summary, category breakdown.

## What It Replaces

| Tool | Cost | What's Missing |
|------|------|---------------|
| Coach.me | $25/week for coaching | Expensive, app is stagnant |
| Habitica | $48/yr premium | Gamification is patronizing for adults |
| Streaks | $5.99 one-time | iOS only, no AI, no accountability |
| Productive | $24/yr | Aggressive upsells, no coaching |

**Habit Tracker Pro: free.** AI coaching for the price of 6 months of a basic habit app.

## Quick Start

1. Copy this tool package to your OpenClaw skills directory.
2. Run `scripts/setup.sh` to initialize data files.
3. Start a conversation with your agent about the habits you want to track.
4. Check-ins begin the next day.

## File Structure

```
habit-tracker-pro/
├── SKILL.md              # Agent behavior and data schemas
├── SETUP-PROMPT.md       # First-run setup flow
├── README.md             # This file
├── SECURITY.md           # Security considerations
├── config/
│   └── settings.json     # Default configuration
├── scripts/
│   ├── setup.sh          # Initialize data directory
│   ├── export-habits.sh  # Export data to CSV/markdown
│   └── weekly-report.sh  # Generate weekly summary
├── examples/
│   ├── example-morning-checkin.md
│   ├── example-pattern-analysis.md
│   └── example-habit-setup.md
└── dashboard-kit/
    ├── manifest.json     # Dashboard widget manifest
    └── DASHBOARD-SPEC.md # Widget specifications
```

## Requirements

- OpenClaw agent with chat channel (Telegram, Discord, etc.)
- `jq` (for scripts — install via `brew install jq` or `apt install jq`)
- Optional: Trainer Buddy, Health Buddy (for cross-tool sync)

## Configuration

See `config/settings.json` for defaults. All settings are adjustable via
conversation with your agent.

## Data Location

All habit data stored in `~/.normieclaw/habit-tracker-pro/`.

## Support

Questions or issues: support@normieclaw.ai

---

*NormieClaw · normieclaw.ai*
*AI agent tools for people who actually want to get things done.*
