---
name: health-reminder
description: Health reminder assistant - medication reminders, water intake tracking, activity prompts
---

# Health Reminder

Personal health tracking and reminder assistant.

## Features
- Medication reminders
- Water intake tracking
- Activity/movement prompts
- Health habit streaks

## Input
- Medication schedule
- Daily water goal
- Activity intervals

## Output
- Reminder notifications
- Intake tracking
- Completion statistics

## Constraints
- ❌ No medical diagnosis
- ❌ No prescription management
- ❌ No device integration

## Usage
```bash
python3 scripts/health-reminder.py med add "维生素C" "08:00" daily
python3 scripts/health-reminder.py water log 250
python3 scripts/health-reminder.py activity remind
```
