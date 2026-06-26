# 🪄 skill-magic-need

> Capture tool and data needs from AI agents — let your agent spec your product for you.

An [OpenClaw](https://openclaw.ai) skill that allows AI agents to register what tools, APIs, or data sources they need during task execution. Over time, this builds a prioritized integration roadmap based on actual usage patterns.

Inspired by [Sonarly's](https://www.sonary.ai) `magic_fetch` concept — give your agent a "tool that does nothing" and let it tell you what it's actually missing.

## Installation

### Via ClawHub (Recommended)

```bash
clawhub install magic-need
```

### Manual

```bash
git clone https://github.com/guim4dev/skill-magic-need.git ~/.openclaw/skills/magic-need
```

## Usage

### For AI Agents

When you realize you need something during task execution:

```javascript
// Register a need
exec({
  command: 'node ~/.openclaw/skills/magic-need/scripts/cli.js "API for recent deploys of service X"'
})

// Or if installed via ClawHub:
exec({
  command: 'magic-need "CPU metrics for upstream service"'
})
```

### For Humans

```bash
# List all registered needs
node scripts/cli.js list

# Generate a formatted report
node scripts/cli.js report

# Archive resolved needs
node scripts/cli.js clear
```

## How It Works

1. **Agent hits a wall** — needs data/tool that doesn't exist
2. **Registers the need** — describes exactly what's missing
3. **Auto-categorized** — tagged as integration, observability, auth, etc.
4. **Review periodically** — generate reports to see patterns
5. **Build roadmap** — prioritize based on actual agent needs

## Auto-Categorization

| Category | Keywords |
|----------|----------|
| 🔌 `integration` | api, endpoint |
| 📊 `observability` | metric, log, monitor |
| 🚀 `devops` | deploy, pipeline, ci |
| 🔐 `auth` | user, auth, login |
| 🗄️ `database` | database, db, query |
| 📁 `storage` | file, storage, upload |
| 📝 `general` | (default) |

## Data Storage

Needs are stored in `~/.magic-need/needs.json`:

```json
[
  {
    "id": "j8ldlr",
    "description": "API for recent deploys",
    "createdAt": "2026-03-07T18:09:18.123Z",
    "status": "pending",
    "category": "integration"
  }
]
```

## Report Example

```
🪄 **Magic Need Report** — 4 pendente(s)

🔌 **INTEGRATION** (2)
  • API for recent deploys of auth-service
  • Feature flags toggled recently

📊 **OBSERVABILITY** (1)
  • CPU metrics for upstream database
```

## Automation

Set up a daily report with cron:

```bash
# Daily at 10 PM
0 22 * * * node ~/.openclaw/skills/magic-need/scripts/cli.js report | your-notification-script
```

Or use OpenClaw's cron to send to Discord/Slack.

## Why?

> "The insight: your agent is a great proxy for your best on-call engineer. Give it a blank canvas to express what it's missing, and it'll spec your product for you."

Instead of guessing which integrations to build, let your AI agent tell you what it actually needs. The agent becomes your product spec writer.

## License

MIT © Thiago Guimarães
