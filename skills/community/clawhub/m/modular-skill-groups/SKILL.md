---
name: modular-skill-groups
description: Organize, activate, and switch between modular skill groups to keep context windows clean. Use when (1) asked to activate a skill group or switch groups, (2) context window is getting polluted with unused skills, (3) starting a new project phase that needs a different skill focus, (4) listing available skill groups or skills within a group, (5) onboarding a new skill and deciding which group it belongs in. Triggers on: "switch to [group]", "activate skill group", "what skills do I have", "modular skills", "skill groups", "load skills", "context window too big", "too many skills".
---

# Modular Skill Groups

Manage skills as named groups — activate or deactivate entire groups at once to keep context clean.

## Core Files
- `~/.openclaw/active_skill_group` — stores the current active group name
- `SKILL_GROUPS.md` (references/) — full group definitions and skill map

## Quick Commands

```bash
# Switch to a different group
echo "group-name" > ~/.openclaw/active_skill_group

# List all groups and which is active
cat ~/.openclaw/active_skill_group

# Add a skill to a group (append to the group's skill list in references/SKILL_GROUPS.md)
```

## Available Groups

| Group | Use when |
|-------|----------|
| `agent-builder` | M.ai.K.R dev, Stripe, DB, onboarding, agent ops |
| `creative` | Game AI, image/audio generation, multimedia |
| `research` | Deep research, competitive analysis, web intelligence |
| `marketing` | Outreach, email automation, lead generation |
| `minimal` | Tight context — CORE skills only |

## Always-Loaded CORE Skills
These load every session regardless of group: `self-improving`, `proactivity`, `sub-agent-orchestrator`, `research-assistant`, `elite-longterm-memory`, `qdrant-memory`

## Adding a New Skill to a Group

1. Install the skill: `clawhub install <skill-name>`
2. Edit `references/SKILL_GROUPS.md`
3. Add the skill to the appropriate group's skill list

## Creating a New Group

1. Add a new `## GROUP: name` section to `references/SKILL_GROUPS.md`
2. List the skills (or empty for minimal)
3. Activate: `echo "name" > ~/.openclaw/active_skill_group`