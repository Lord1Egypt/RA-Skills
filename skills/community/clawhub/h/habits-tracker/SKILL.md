---
name: habits-tracker
description: Track habits, routines, streaks, completions, reminders, and weekly progress with a local Node.js CLI. Use when the user wants to build a daily habit system, log habit completions, review consistency, recover from broken streaks, generate reports, or set up cron reminders.
version: v1.0.0
tags: habit-tracking, streak-monitoring, productivity
---

# Habit Tracker

## Usage Scenarios

### Scenario 1: Create and Start Tracking a New Habit
**User input:** "I want to track my daily reading habit — read for 30 minutes every evening"
**Expected output:** The skill provides the exact CLI command (`node scripts/habit-cli.js add "Read 30 minutes" --frequency daily --target 1 --reminder "21:00"`), explains what it records, and suggests a realistic starting target.

### Scenario 2: Review Weekly Progress
**User input:** "How did I do on my habits this week?"
**Expected output:** The skill generates a progress report with visual progress bars, completion rates, current streaks, and a summary of missed days for each tracked habit.

### Scenario 3: Recover from a Broken Streak
**User input:** "I missed three days of exercise this week, what should I do?"
**Expected output:** A recovery plan: log the missed days, temporarily lower the weekly target, and suggests shrinking the habit size rather than adding more reminders if the completion rate is below 50%.
### Scenario 4: 上班族喝水习惯追踪
**User input:** "我经常一忙就忘记喝水，每天喝不到两杯水，想养成多喝水的习惯，怎么做？"
**Expected output:** 设计喝水习惯追踪方案：1）设置每小时闹钟或智能手表提醒；2）使用带刻度的水杯（如500ml瓶装水，目标每天4瓶）；3）在工位显眼位置贴便签提醒；4）使用'小日常'/HabitNow等App做打卡记录。进阶技巧：每次上厕所后回来必喝一口水（形成习惯叠加），用柠檬片/茶包增加喝水乐趣。设定前两周目标：每天1.5L，达标奖励周末一杯奶茶。

## Best Use Cases

- Build a daily or weekly habit tracking system
- Log exercise, reading, meditation, writing, sleep, study, or medication routines
- Review streaks, completion rates, missed days, and consistency trends
- Recover after a broken streak without abandoning the habit
- Generate weekly progress reports for personal review
- Set up local reminders with cron while keeping data on the user's machine

## Quick Start

```bash
node scripts/habit-cli.js add "Read 30 minutes" --frequency daily --target 1 --reminder "21:00"
node scripts/habit-cli.js log "Read 30 minutes" --note "Finished chapter 5"
node scripts/habit-cli.js stats "Read 30 minutes" --days 30
```

When a user asks for habit advice, first decide whether they need:

- a tracking command
- a weekly review
- a streak recovery plan
- a reminder setup
- a habit redesign because the target is too large

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

## Output Guidance

For natural-language requests, return:

1. The exact CLI command to run
2. What the command records or reports
3. One habit-design suggestion if the user's target is vague or too ambitious
4. A privacy note when the habit note may include sensitive health or personal details

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

## Recovery Patterns

- If the user missed one day, recommend logging the miss and resuming today.
- If the user missed several days, lower the target for one week.
- If completion rate is below 50%, suggest shrinking the habit rather than adding more reminders.
- If the user has many habits, recommend tracking the top 3 keystone habits first.
