# OpenClaw Ops Skills Pack

> **Production-Ready Skills for OpenClaw Infrastructure**
> Version: 1.0.0 | Last Updated: 2026-03-10

## Overview

This is a comprehensive skill package designed to transform OpenClaw from a chatbot into reliable infrastructure. Based on 1.4 billion tokens of real-world testing, these skills provide the guardrails, workflows, and best practices needed for autonomous agent operations.

## What This Solves

| Problem | Solution |
|---------|----------|
| Agent loops on same answer 8 times | `execution-discipline.md` |
| Agent edits files it shouldn't touch | `scope-control.md` |
| Agent skips documentation and breaks things | `docs-first.md` |
| Agent stops after one task and waits | `task-autonomy.md` |
| Lost context when sessions compress | `memory-persistence.md` |
| Massive token waste on wrong models | `model-routing.md` |
| Security vulnerabilities | `security-hardening.md` |
| No visibility into overnight work | `progress-logging.md` |

## Quick Start

```bash
# Clone to your OpenClaw workspace
git clone https://github.com/yourusername/openclaw-ops-skills.git ~/.openclaw/workspace/skills/ops-pack

# Or copy individual skills
cp skills/*.md ~/.openclaw/workspace/skills/

# Restart OpenClaw
openclaw restart
```

## Skills Included

### Core Infrastructure Skills

| Skill | Purpose | Priority |
|-------|---------|----------|
| `model-routing.md` | Optimize model selection for cost/quality | ⭐⭐⭐ |
| `execution-discipline.md` | Build → Test → Document → Decide loop | ⭐⭐⭐ |
| `docs-first.md` | Force documentation before code changes | ⭐⭐⭐ |
| `scope-control.md` | Define and respect operational boundaries | ⭐⭐⭐ |
| `task-autonomy.md` | Self-expanding task management | ⭐⭐⭐ |
| `progress-logging.md` | Comprehensive progress tracking | ⭐⭐⭐ |

### Operational Skills

| Skill | Purpose | Priority |
|-------|---------|----------|
| `memory-persistence.md` | Maintain state across sessions | ⭐⭐ |
| `cron-orchestration.md` | Scheduled task management | ⭐⭐ |
| `error-recovery.md` | Graceful failure handling | ⭐⭐ |
| `security-hardening.md` | Security best practices | ⭐⭐⭐ |
| `testing-protocol.md` | Validation requirements | ⭐⭐ |
| `communication.md` | Update standards | ⭐⭐ |

### Advanced Skills

| Skill | Purpose | Priority |
|-------|---------|----------|
| `cost-optimization.md` | Token usage optimization | ⭐⭐ |
| `debugging-methodology.md` | Systematic troubleshooting | ⭐⭐ |
| `integration-guide.md` | Safe third-party connections | ⭐ |

## Recommended Configuration

### Model Routing Setup

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallbacks": [
          "anthropic/claude-opus-4-6",
          "openrouter/moonshotai/kimi-k2.5"
        ]
      }
    }
  }
}
```

### Cron Schedule Template

```bash
# Overnight work cycles
openclaw cron add --name "overnight-2am" --cron "0 2 * * *" --message "Check Todo.md. Pick up incomplete tasks. Log progress."
openclaw cron add --name "overnight-4am" --cron "0 4 * * *" --message "Continue working through Todo.md. Update progress-log."
openclaw cron add --name "overnight-6am" --cron "0 6 * * *" --message "Final check. Summarize all overnight work."
```

### Required Workspace Files

```
~/.openclaw/workspace/
├── USER.md              # Your identity, preferences, context
├── AGENTS.md            # Agent identities and routing
├── SOUL.md              # Decision loops and behavior
├── MEMORY.md            # Long-term facts
├── Todo.md              # Current tasks (self-expanding)
└── progress-log.md      # Execution log
```

## Usage Patterns

### For Development Work

```bash
# Use Claude Code / Codex for development
# Point to clean git repo
# Focus on: writing code, debugging, shipping features
```

### For Operations Work

```bash
# Use OpenClaw for operations
# Focus on: monitoring, scheduling, communication, automation
# These skills apply here
```

## Key Principles

1. **Model Quality ≠ Agent Quality** - Chat ability doesn't equal tool-calling ability
2. **Files Are Memory** - Session compression deletes context; write everything down
3. **Cron Jobs > Long Sessions** - Background work needs scheduled wake-ups
4. **One Integration at a Time** - Each integration is a failure point
5. **Transparency Over Recall** - You must see what your agent "knows"

## Security Considerations

```bash
# Run health checks regularly
openclaw doctor --deep --fix --yes

# Security audit
openclaw security audit --fix

# Full status
openclaw status --all --deep
```

## Model Recommendations (Feb 2026)

| Model | Agent Quality | Tool Calling | Cost | Use Case |
|-------|---------------|--------------|------|----------|
| Sonnet 4.6 | Excellent | Reliable | $3/$15M | Daily operations |
| Opus 4.6 | Excellent | Reliable | $15/$75M | Deep reasoning |
| Kimi K2.5 | Good | Reliable | ~$0.6/$2M | Budget tasks |
| MiniMax M2.5 | Good | Reliable | $0.3/$1.20M | Cheapest option |
| GPT-5.3-Codex | Excellent | Reliable | Pro sub | Code writing |

## Installation Order

1. **Week 1**: Install core skills only
   - `model-routing.md`
   - `execution-discipline.md`
   - `scope-control.md`

2. **Week 2**: Add operational skills
   - `docs-first.md`
   - `task-autonomy.md`
   - `progress-logging.md`

3. **Week 3**: Add advanced skills
   - `memory-persistence.md`
   - `cron-orchestration.md`
   - `error-recovery.md`

## Troubleshooting

### Agent stops after one task
→ Enable `task-autonomy.md`

### Agent makes same mistakes repeatedly
→ Enable `execution-discipline.md` and check `lessons.md`

### Token costs exploding
→ Enable `model-routing.md` and `cost-optimization.md`

### Agent breaks things
→ Enable `docs-first.md` and `scope-control.md`

### No visibility into overnight work
→ Enable `progress-logging.md`

## Author

**Eric Jie** <jxmerich@mail.com>

## Contributing

This is an open-source project. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Add your skill with proper documentation
4. Submit a pull request

## License

MIT License - Free to use, modify, and distribute.

## Credits

Created based on real-world production experience with OpenClaw.
Tested across 1.4+ billion tokens of agent operations.

---

**Remember**: Configuration is the work. You're not using a tool, you're building a system. These skills are your guardrails.
