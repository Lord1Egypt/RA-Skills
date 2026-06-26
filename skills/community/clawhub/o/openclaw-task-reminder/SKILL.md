---
name: openclaw-task-reminder
description: Simple task reminder for OpenClaw agents. Create, list, and manage tasks with priority levels. Use for tracking to-dos and getting reminders for important work. Keep your workspace organized and never miss deadlines.
---

# OpenClaw Task Reminder

Simple task management for your OpenClaw workflow. Track to-dos, set priorities, and stay organized.

## Installation

```bash
npx clawhub@latest install openclaw-task-reminder
```

## Usage

```bash
# Add a new task
node ~/.openclaw/skills/openclaw-task-reminder/task.js add "Your task description"

# List all tasks
node ~/.openclaw/skills/openclaw-task-reminder/task.js list

# Mark task as done
node ~/.openclaw/skills/openclaw-task-reminder/task.js done <task_id>

# Clear completed tasks
node ~/.openclaw/skills/openclaw-task-reminder/task.js clear
```

## Features

- ✅ Add tasks with priorities (high/medium/low)
- ✅ List tasks by priority
- ✅ Mark tasks as done
- ✅ Persistent storage in workspace
- ✅ Simple and fast

## Priority Levels

- 🔴 **High**: Urgent tasks that need immediate attention
- 🟡 **Medium**: Regular tasks to complete today
- 🟢 **Low**: Nice-to-have tasks for later

## Examples

```bash
# Add high priority task
node ~/.openclaw/skills/openclaw-task-reminder/task.js add "Review PR #123" --priority high

# List all tasks
node ~/.openclaw/skills/openclaw-task-reminder/task.js list

# Mark task as done
node ~/.openclaw/skills/openclaw-task-reminder/task.js done 1
```

## Need Help?

If you need help with OpenClaw:
- 📧 **Installation Service**: ¥99-299
- 🔗 **Landing Page**: https://yang1002378395-cmyk.github.io/openclaw-install-service/

## License

MIT
