# Personal Plans

Personal planning assistant for OpenClaw. Tracks tasks, to-do lists, deadlines, and daily/weekly plans directly in Telegram.

## What it does

- ✅ Add, complete, and delete tasks
- 📅 Plan by day, week, or month
- ⏰ Track deadlines and reminders
- 🔢 Set task priorities (high/medium/low)
- 📊 Review what's done, pending, or overdue
- 🎯 Break big goals into small steps

## Commands

| Command | Example |
|---------|---------|
| Add task | `нужно позвонить врачу до пятницы` |
| Complete task | `купил продукты — готово` |
| Show tasks | `что у меня на сегодня?` |
| Weekly plan | `план на эту неделю` |
| Show overdue | `что просрочено?` |
| Show instructions | `инструкция` |

## Installation

1. Download ZIP from [ClawhHub](https://clawdhub.com)
2. Extract the skill folder to `/data/.openclaw/workspace/skills/`
3. Restart the container: `docker restart openclaw-ewcl-openclaw-1`

## Data storage

All data is stored locally on your VPS:
`/data/.openclaw/workspace/knowledge/personal/plans.md`
