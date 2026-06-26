# Habits Tracker

Local Node.js CLI for habit creation, completion logging, streak review, reminders, and weekly progress reports.

## Use Cases

- Build a daily or weekly habit tracking system.
- Log exercise, reading, meditation, writing, study, sleep, or medication routines.
- Review streaks, completion rates, missed days, and trends.
- Recover from broken streaks with smaller targets.

## Quick Start

```bash
node scripts/habit-cli.js add "Read 30 minutes" --frequency daily --target 1 --reminder "21:00"
node scripts/habit-cli.js log "Read 30 minutes" --note "Finished chapter 5"
node scripts/habit-cli.js report --days 7
```

## Local Check

```bash
npm test
```

## Release

Current ClawHub release target: `1.1.0`.
