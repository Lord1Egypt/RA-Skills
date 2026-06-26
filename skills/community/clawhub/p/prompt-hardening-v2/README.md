# prompt-hardening

Systematic methods for hardening LLM agent prompts to reliably follow instructions.

## Quick Start

```bash
# Audit an existing prompt
~/.openclaw/skills/prompt-hardening/scripts/audit.sh ~/path/to/SOUL.md

# Apply hardening (read SKILL.md for the 16 patterns)
cat ~/.openclaw/skills/prompt-hardening/SKILL.md
```

## When to Use

- Agent repeatedly violates rules
- Deploying new agent system prompt
- Agent creatively bypasses tool constraints
- Long conversation behavior drift

## Structure

- `SKILL.md` — 16 hardening patterns with examples and checklist
- `scripts/audit.sh` — Quick 16-point audit of any prompt file
- `references/sources.md` — Research sources and empirical data
