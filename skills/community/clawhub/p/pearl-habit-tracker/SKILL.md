---
name: habit-tracker
description: Track habits, log completions, and analyze progress with CLI commands. Use when user wants to build habits, track daily/weekly/monthly routines, log habit completions, view statistics, generate reports, or set up habit reminders. Supports habit creation, logging, statistics analysis, streak tracking, and progress reports.
---

# Habit Tracker

A command-line habit tracking tool for building consistency and monitoring progress.

## Features

- **Habit Definition**: Create habits with custom frequency (daily/weekly/monthly), targets, and reminders
- **Habit Logging**: Log completions manually with optional notes and custom dates
- **Statistics**: View completion rates, streaks, and trends
- **Progress Reports**: Visual progress bars and summary reports
- **Smart Reminders**: Check for due habits based on reminder times

## Installation

The habit tracker is available as a Node.js CLI tool. No dependencies required.

## CLI Commands

### Add a Habit

```bash
node scripts/habit-cli.js add "Exercise" --frequency daily --target 1 --reminder "08:00"
```

Options:
- `--frequency`: daily, weekly, or monthly (default: daily)
- `--target`: completions per period (default: 1)
- `--reminder`: time in HH:MM format
- `--description`: habit description

### List Habits

```bash
node scripts/habit-cli.js list
```

### Log a Completion

```bash
node scripts/habit-cli.js log "Exercise" --count 1 --note "Morning run"
```

Options:
- `--count`: number of completions (default: 1)
- `--date`: YYYY-MM-DD format (default: today)
- `--note`: optional note

### View Logs

```bash
node scripts/habit-cli.js logs "Exercise" --days 7
```

### View Statistics

```bash
node scripts/habit-cli.js stats "Exercise" --days 30
```

Shows:
- Total completions
- Active days
- Completion rate
- Current streak
- Longest streak

### Generate Report

```bash
node scripts/habit-cli.js report --days 7
```

Displays visual progress bars and summary for all habits.

### Edit a Habit

```bash
node scripts/habit-cli.js edit "Exercise" --target 2 --reminder "07:00"
```

### Delete a Habit

```bash
node scripts/habit-cli.js delete "Exercise"
```

### Check Reminders

```bash
node scripts/habit-cli.js reminder
```

## Data Storage

Habits and logs are stored in `~/.config/habit-tracker/`:
- `habits.json`: Habit definitions
- `logs.json`: Completion logs

## Automation

### Cron Job for Reminders

Add to crontab for hourly reminder checks:

```bash
0 * * * * node /path/to/habit-tracker/scripts/habit-cli.js reminder
```

### Daily Report

```bash
0 21 * * * node /path/to/habit-tracker/scripts/habit-cli.js report --days 1
```

## Integration

This skill can be triggered by:
- Direct CLI commands
- Scheduled cron jobs
- Event-based triggers (e.g., after completing a task)

## Examples

**Track a new habit:**
```bash
habit add "Read 30 minutes" --frequency daily --target 1 --reminder "21:00"
habit log "Read 30 minutes" --note "Finished chapter 5"
```

**Weekly habit with multiple targets:**
```bash
habit add "Meditate" --frequency weekly --target 5
habit log "Meditate" --count 1
```

**View progress:**
```bash
habit stats --days 30
habit report --days 7
```
