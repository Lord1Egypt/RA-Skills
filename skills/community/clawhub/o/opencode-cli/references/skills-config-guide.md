# Skills Configuration Guide

> OpenCode Skills file locations and format specification

---

## Configuration Locations

Skill files are auto-discovered in these directories:

| Location | Purpose | Priority |
|----------|---------|----------|
| `.agents/skills/<skill>/SKILL.md` | Project-level | High |
| `~/.config/opencode/skills/<skill>/SKILL.md` | Global | Low |

**Priority note:** Project-level skills override same-name global skills.

---

## Skill Format

```markdown
---
name: my-skill
description: Description of what this skill does and when to use it.
---

# Skill Content

Instructions and documentation here...
```

---

## Naming Rules

- Lowercase letters, numbers, single hyphens
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Must match directory name

**Correct examples:**
- `opencode`
- `my-skill`
- `test-helper`

**Wrong examples:**
- `My-Skill` (uppercase)
- `-my-skill` (starts with hyphen)
- `my--skill` (consecutive hyphens)

---

## Directory Structure

```
~/.config/opencode/skills/
├── opencode-cli/
│   ├── SKILL.md
│   └── references/
│       ├── mcp-config-guide.md
│       └── skills-config-guide.md
└── another-skill/
    └── SKILL.md
```

```
<project>/.agents/skills/
├── project-specific-skill/
│   └── SKILL.md
└── another-project-skill/
    └── SKILL.md
```

---

## References

- [AgentSkills Specification](https://agentskills.io/specification)
- [OpenCode Documentation](https://opencode.ai/docs)

---

*Configuration Guide v1.0 - 2026-04-05*