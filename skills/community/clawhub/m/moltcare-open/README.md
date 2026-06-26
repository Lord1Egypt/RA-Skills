# MoltCare-Open Skill

> 🦞 **OpenClaw Skill** - Agent Configuration Framework

A comprehensive four-layer configuration system for OpenClaw Agent with three-layer trigger architecture and PUA problem-solving framework.

## Installation

```bash
# Via ClawHub (when published)
clawhub install moltcare-open

# Or manually
curl -fsSL https://raw.githubusercontent.com/useens/moltcare-open/master/skill/scripts/install.sh | bash
```

## What You Get

### Four-Layer Architecture
```
SOUL.md      → Agent soul (principles, personality)
AGENTS.md    → Operation manual (triggers, workflows)
USER.md      → User profile (preferences, constraints)
MEMORY.md    → Long-term memory (high-signal info)
```

### Three-Layer Trigger System
| Layer | Trigger | Example |
|-------|---------|---------|
| **L1** | Exact | "这很重要" → [⭐] |
| **L2** | Semantic | "关键是..." → [⭐] |
| **L3** | Agent Eval | Auto-record after task |

### PUA Problem-Solving
- **Three Iron Laws**: Exhaust all options → Act first → Take ownership
- **L1-L4 Escalation**: Automatic pressure upgrade on failures
- **7-Item Checklist**: Mandatory before giving up

## Files Included

- `SKILL.md` - Skill definition and usage guide
- `scripts/install.sh` - Installation script
- `assets/*.md` - All template files

## Usage

After installation, edit:
1. `USER.md` - Your profile and preferences
2. `MEMORY.md` - Your high-priority memories

Then test triggers:
```
用户: "这很重要，我偏好简洁回答"
Agent: [⭐] 已记录核心偏好: 简洁回答
```

## Version

v3.1 - Three-Layer Trigger Architecture

## License

MIT © MoltCare Team
