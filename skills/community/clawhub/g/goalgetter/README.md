# GoalGetter - Task & Goal Tracking for OpenClaw

> Simple, privacy-focused task and goal management for OpenClaw AI assistants. No external dependencies, no API keys, no cloud. Just markdown.

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![Author](https://img.shields.io/badge/author-DevSef-purple)](https://github.com/Steffano198)

**GoalGetter** is an OpenClaw skill that brings task and goal management directly into your AI assistant workflow. All data lives in plain markdown files on your local machine.

![GoalGetter Banner](https://via.placeholder.com/800x200?text=GoalGetter+-+Tasks+%26+Goals+for+OpenClaw)

## Why GoalGetter?

- **100% Local** — Your data never leaves your machine
- **No Dependencies** — Just markdown files, no external APIs
- **Privacy First** — No cloud, no tracking, no accounts
- **OpenClaw Native** — Built specifically for OpenClaw agents
- **Git-Friendly** — All data is plain text, version control your tasks
- **Streak Tracking** — Build habits with automatic streak counting

## Features

### ✅ Task Management
- Create tasks with simple commands
- Mark tasks complete
- View all pending tasks
- Archive completed tasks

### 🎯 Goal Tracking
- Create goals with streak counters
- Track daily completions
- View current streaks
- Automatic streak calculation

### 📊 Simple Commands

| Command | Description |
|---------|-------------|
| "Add task: [text]" | Create a new task |
| "Show my tasks" | List all tasks |
| "Complete task: [text]" | Mark task done |
| "New goal: [name]" | Create a goal |
| "Did [goal]" | Log goal completion |
| "Show goal streaks" | View all streaks |

## Installation

### Option 1: ClawHub (Recommended)
```bash
clawhub install goalgetter
```

### Option 2: Manual Install
```bash
git clone https://github.com/Steffano198/goalgetter.git ~/.openclaw/workspace/skills/goalgetter
```

## Quick Start

1. **Install the skill** using ClawHub or manual install
2. **Restart OpenClaw** to load the new skill
3. **Start using it:**

```
You: Add task: Finish SAAS research
GoalGetter: ✅ Task added: "Finish SAAS research"

You: New goal: Morning meditation
GoalGetter: ✅ Goal created: "Morning meditation" (streak: 0)

You: Did meditation
GoalGetter: 🔥 Streak updated! "Morning meditation" is now at 1 day
```

## Data Storage

All data is stored in: `~/.openclaw/goalgetter/`

```
~/.openclaw/goalgetter/
├── tasks.md       # Your todo list
├── goals.md       # Goal tracking with streaks
└── done/          # Archive of completed tasks
```

### Task Format (tasks.md)
```markdown
# Tasks

- [ ] Buy groceries
- [x] Call dentist
- [ ] Finish SAAS research
```

### Goal Format (goals.md)
```markdown
# Goals

## Meditation
- streak: 5
- created: 2026-01-15
- log:
  - 2026-01-15
  - 2026-01-16
  - 2026-01-17
  - 2026-01-18
  - 2026-01-19
```

## Requirements

- OpenClaw installed
- read, write, exec tools enabled
- No external dependencies

## Use Cases

### Personal Productivity
- Daily task lists
- Goal tracking
- Project management

### Habit Building
- Exercise tracking
- Meditation streaks
- Learning goals
- Reading habits

### Team Workflows
- Sprint tasks
- Code review reminders
- Meeting prep

## Comparison

| Feature | GoalGetter | Habitica | Todoist |
|--------|------------|----------|---------|
| Local Only | ✅ | ❌ | ❌ |
| No API Keys | ✅ | ❌ | ❌ |
| Open Source | ✅ | Partial | ❌ |
| Free Forever | ✅ | Freemium | Freemium |
| Markdown Based | ✅ | ❌ | ❌ |

## Contributing

Contributions are welcome! Please open an issue or PR.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Support

- 📖 [Documentation](README.md)
- 🐛 [Issue Tracker](https://github.com/Steffano198/goalgetter/issues)

## Keywords

openclaw, openclaw-skill, ai-assistant, task-manager, goal-tracker, habit-tracker, productivity, markdown, cli, local-only, privacy, gtd, getting-things-done, automation, agent, ai-agent, clawhub, streaks

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Made with 🦔 by [DevSef](https://github.com/Steffano198)
