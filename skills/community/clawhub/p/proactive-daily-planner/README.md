# 📅 Proactive Daily Planner Skill for OpenClaw

A proactive personal assistant skill that helps you plan your day, track tasks, and stay motivated.

## 🎯 Features

- **Proactive Planning**: Initiates daily planning automatically
- **Time-aware**: Different planning for morning/afternoon/evening
- **Task Management**: Track and prioritize daily tasks
- **Motivation System**: 50+ motivational messages and encouragement
- **Progress Tracking**: Monitors task completion throughout the day
- **Evening Review**: Helps reflect on accomplishments and plan for tomorrow
- **Customizable**: Fully configurable to your preferences

## 🚀 Quick Start

### Installation

```bash
# Clone or copy the skill
cd ~/.openclaw/workspace
cp -r proactive-daily-planner skills/

# Run installer
cd skills/proactive-daily-planner
./scripts/install.sh
```

### Basic Usage

```bash
# Morning planning
node planner.js morning

# Progress check
node planner.js progress

# Evening review
node planner.js evening

# Auto-detect based on time
node planner.js auto

# Get motivation
node planner.js motivate
```

### Installation via OpenClaw

Once published on ClawHub:
```bash
openclaw skill install proactive-daily-planner
```

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "user": {
    "name": "Your Name",
    "timezone": "Your/Timezone",
    "workHours": "9:00-18:00"
  },
  "schedule": {
    "morningCheckin": "8:00",
    "afternoonCheckin": "13:00",
    "eveningReview": "20:00"
  },
  "planning": {
    "categories": ["work", "learning", "fitness", "personal"],
    "maxTasksPerDay": 8
  }
}
```

## 📁 Project Structure

```
proactive-daily-planner/
├── SKILL.md          # Skill documentation
├── planner.js        # Main JavaScript implementation
├── config.json       # User configuration
├── README.md         # This file
├── templates/        # Planning templates
│   ├── morning.md
│   ├── afternoon.md
│   └── evening.md
└── scripts/
    └── install.sh    # Installation script
```

## 🔧 Integration with OpenClaw

### As a Standalone Skill
The skill can run independently using Node.js.

### With OpenClaw Proactive System
Integrate with OpenClaw's proactive assistant by adding to `HEARTBEAT.md`:

```markdown
# HEARTBEAT.md
- Run daily planner: cd ~/.openclaw/workspace/skills/daily-planner && node planner.js auto
```

### Scheduled Execution
Set up cron jobs for automatic planning:

```bash
# Morning planning at 8 AM
0 8 * * * cd ~/.openclaw/workspace/skills/daily-planner && node planner.js morning

# Afternoon check at 1 PM  
0 13 * * * cd ~/.openclaw/workspace/skills/daily-planner && node planner.js progress

# Evening review at 8 PM
0 20 * * * cd ~/.openclaw/workspace/skills/daily-planner && node planner.js evening
```

## 📊 Data Storage

Planning data is stored in OpenClaw's memory system:

- `~/.openclaw/workspace/memory/daily-plan-YYYY-MM-DD.md` - Daily plans
- `~/.openclaw/workspace/memory/task-history.json` - Task completion history
- `~/.openclaw/workspace/memory/progress-stats.json` - Progress statistics

## 🎨 Customization

### Templates
Edit the Markdown templates in `templates/` to match your planning style.

### Motivation Messages
Add your own motivational messages to `config.json`:

```json
"motivation": {
  "messages": [
    "Your custom message here! 💪",
    "Another inspiring message! 🚀"
  ]
}
```

## 🤝 Development

### Prerequisites
- Node.js (for running the skill)
- OpenClaw (for integration)

### Building
The skill is written in vanilla JavaScript with no external dependencies.

### Testing
```bash
# Test all commands
node planner.js morning
node planner.js progress  
node planner.js evening
node planner.js auto
node planner.js help
```

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built for [OpenClaw](https://openclaw.ai) AI Assistant
- Inspired by proactive assistant patterns
- Designed for personal productivity enhancement

## 🚀 Future Enhancements

Planned features:
- Calendar integration
- Email task extraction
- Habit tracking
- Weekly/Monthly reviews
- Team planning features
- Mobile app interface

---

**Happy Planning!** May your days be productive and fulfilling. 📅✨

*Built with ❤️ by Akshay Memane*