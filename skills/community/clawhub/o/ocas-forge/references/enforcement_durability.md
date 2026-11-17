# Enforcement Durability

## Problem
Advisory-only enforcement (e.g., writing "use Forge instead of skill_manage" in MEMORY.md) is easily skipped. The agent may read the note but still default to the path of least resistance.

## Solution
**Hard gates must live in the SKILL.md itself** — the artifact that gets loaded and followed. For example:

- Forge's phase 1 existence gate (parent search, standalone test, absorption test) is in the Forge SKILL.md. When the agent loads Forge, those checks are right there in the instructions.
- The naming guard (NEVER create new `ocas-*` skills without explicit user authorization) is in the Forge SKILL.md.

## Why this works
- **Loaded context**: When the agent loads a skill, it follows the instructions in that skill's SKILL.md. If the instructions say "check for parents first," it will.
- **Durability**: Skills in `~/hermes/skills/` persist across updates. MEMORY.md and hermes core do not.
- **Visibility**: The rule is visible at the moment of decision (when the agent is reading the skill's instructions).

## Anti-patterns
- Relying on memory notes as the sole enforcement mechanism.
- Writing rules in hermes core or config files that get wiped on update.
- Creating standalone skills for rules that should be embedded in the relevant class-level skill.

## Example
Instead of:
```markdown
# MEMORY.md
- Always use Forge for skill creation
```

Do:
```markdown
# Forge SKILL.md
## Phase 1: Existence Gate (HARD GATE)
Before creating a new skill, check for parents. If a parent exists, absorb into it.
```