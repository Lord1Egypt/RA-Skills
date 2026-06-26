---
name: self-improving-agent
description: "AI Self-Improving Agent v2 - Learn from mistakes, corrections, and successes. Three-layer system: passive capture + proactive check + proactive skill generation (inspired by Hermes Agent). Avoid repeating the same errors, remember user preferences, and auto-generate reusable Skills from successful task completions."
version: 2.0.0
trigger: "improve myself, learn from mistake, remember this, auto-skill, self-improving"
tags: ["memory", "learning", "skill-generation", "ai-agent", "productivity"]
license: MIT-0
author: 老二
platform: openclaw
---

# Self-Improving Agent v2

让AI从错误中学习，越用越聪明。参考 Hermes Agent 的"做-学-改"循环，实现主动式记忆与技能生成。

## Three-Layer Learning System

### Layer 1: Passive Capture (Automatic)
- Command fails → `errors.jsonl`
- User corrects AI → `corrections.jsonl`
- Discover best practice → `best_practices.jsonl`

### Layer 2: Proactive Check (Before Execution)
- Check relevant memories before running commands
- Heartbeat scans for knowledge blind spots

### Layer 3: Proactive Skill Generation (New - From Hermes)

**Core insight from Hermes Agent**: When a complex task succeeds, proactively propose generating a reusable Skill.

- **Complex task succeeds (>10 steps)** → Propose generating a Skill
- **Same pattern repeats 3+ times** → Auto-generalize to template
- **Best practice discovered** → Solidify into executable script
- **New tool/skill learned** → Save to `skills-generated/`

## Problem Statement

✅ Same command fails repeatedly, AI uses wrong method next time
✅ User corrects AI's style/preference, AI forgets next session
✅ Same pitfall hit repeatedly in the same project
✅ Better approach discovered but not systematically remembered
✅ External tool/API changes, AI still using old knowledge
✅ **Complex task succeeds, no one thinks to generate reusable Skill** ← NEW
✅ **Repeated pattern detected, no auto-generalization mechanism** ← NEW

## Quick Start

```bash
# Install
mkdir -p ~/.openclaw/memory/self-improving
mkdir -p ~/.openclaw/skills-generated

# Log an error
python3 log_error.py --command "npm install xxx" --error "permission denied" --fix "use sudo"

# Log a correction
python3 log_correction.py --topic "code style" --wrong "double quotes" --correct "single quotes"

# Generate a Skill (after successful complex task)
python3 generate_skill.py \
  --name "my-tool" \
  --trigger "related task description" \
  --desc "What this tool does" \
  --files "path/to/file.py" \
  --notes "Important context"

# Check before running
python3 check_memory.py --command "npm install"
```

## File Structure

```
~/.openclaw/memory/self-improving/
├── errors.jsonl          # Error logs
├── corrections.jsonl     # User corrections
├── best_practices.jsonl  # Best practices
├── skills_registry.json  # Generated skills registry
└── index.json           # Quick index

~/.openclaw/skills-generated/     # Auto-generated Skills
├── my-tool/
│   └── SKILL.md
└── another-tool/
    └── SKILL.md
```

## Proactive Generation Triggers

| Scenario | Action | Type |
|----------|--------|------|
| Command fails | Log to errors | Passive |
| User corrects | Log to corrections | Passive |
| Complex task succeeds (>10 steps) | Propose Skill generation | **Proactive** |
| Same task done 3+ times | Auto-generalize to template | **Proactive** |
| Heartbeat scan | Detect knowledge blind spots | Proactive |
| New tool/skill learned | Solidify to skills-generated | **Proactive** |

## Skill Registry Format

```json
{
  "skills": [
    {
      "name": "bbu-config-tool",
      "trigger": "BBU config / TR-069 parameter modification",
      "description": "Modify BBU device confdb_v2.xml via SSH, supports ZTP factory reset",
      "files": ["D:/tools/bbu_config_gui.py"],
      "created_at": "2026-04-14",
      "success_count": 5,
      "last_used": "2026-04-14",
      "auto_trigger": true
    }
  ]
}
```

## Proactive Generation Flow

```
Task Completed
  ↓
Evaluate: (>10 steps? repeat>3x? general value?)
  ↓ Yes
Ask: "Want me to save this as a reusable Skill?"
  ↓ User confirms
Generate Skill/SKILL.md
  ↓
Register to skills_registry.json
  ↓
Next similar task → Auto-recommend
```

## Comparison with Hermes Agent

| Feature | Hermes | Ours |
|---------|--------|------|
| Auto-solidify | ✅ Fully automatic | ⚠️ User confirms first |
| Pattern recognition | ✅ Auto-generalize | ⚠️ Trigger-based |
| Skill quality | High | Medium (needs human review) |
| Execution environment | Self-contained sandbox | External dependencies |

**Our advantage**: User-controlled, transparent, no irreversible actions.

## Notes

- Generated Skills need human quality review
- Sensitive info should be masked
- Periodically clean up outdated Skills
- After generating Skill, sync to memory index

---
v2 Updated 2026-04-14: Added proactive Skill generation layer (inspired by Hermes Agent)
