# Learning Check-in

A daily learning habit tracker skill for CoPaw/OpenClaw agents.

## Features

- **Simple Check-in**: Just tell your agent "I'm done" or "check-in complete"
- **Streak Tracking**: Build your consecutive day streak
- **Customizable**: Edit rules to fit your schedule

## Installation

This skill follows the OpenClaw skill standard installation method.

1. Copy this skill folder to your agent's skill storage directory
2. The skill will automatically initialize its data folder on first use

## Usage

Simply tell your agent:

- **First time:** "I want to use the learning check-in skill"
- **Daily check-in:** "I'm done with my learning" or "check-in complete"
- **Check progress:** "What's my streak?" or "How am I doing?"

## Quick Start

### 1. First Time Setup

Tell your agent: "I want to use the learning check-in skill"

The agent will welcome you and explain the rules, then ask you to start your first check-in.

### 2. Daily Check-in

After completing your daily learning, tell your agent:
- "I'm done with my learning"
- "Check-in complete"
- "I finished studying"

Your agent will record your check-in and show your current streak.

## Data Storage

Your check-in data is stored locally in the skill's data folder:

```
<skill_directory>/data/
├── rule.md           - Your personalized rules
├── records.json      - Check-in history
├── version.txt       - Current skill version
├── cron_status.json  - Reminder configuration status
└── reminder_log.json - Reminder sending log
```

## Customization

Edit the `rule.md` file in the data folder to customize reminder messages or notes.

## Technical Requirements

- Python 3.x
- No external dependencies (standard library only)
- Works on Windows, Linux, and macOS

## Version

Current: **3.1.0**

## GitHub

https://github.com/daizongyu/learning-checkin

## License

MIT