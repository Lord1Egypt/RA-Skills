---
name: hermes-skills
description: "Hermes Self-Evolution Skills — Memory management and skill tracking for OpenClaw agents. Use when: (1) tracking memory at regular conversation intervals, (2) compressing context at 50% capacity, (3) saving discovered techniques as skills, (4) implementing programmatic security gates before memory writes. This skill provides 4 memory techniques: Memory Nudge (every 10 exchanges), Memory Flash (at 50% context), Skills Tracker (every 15 calls), Programmatic Gate (security). Works with any agent."
version: "1.0.0"
---

# Hermes Skills — Self-Evolution

> Memory management and skill tracking for OpenClaw agents
> Impersonal — works for any agent

---

## Description

Hermes provides 4 self-evolution techniques for agents:

| Technique | Trigger | Purpose |
|-----------|---------|---------|
| Memory Nudge | Every 10 exchanges | Ask to save important info |
| Memory Flash | At 50% context | Compress + save conversation |
| Skills Tracker | Every 15 tool calls | Save discovered techniques |
| Programmatic Gate | Before memory write | Security scan before write |

---

## Techniques

### 1. Memory Nudge (every 10 exchanges)

```python
# After 10 exchanges, ask:
"Do we need to remember something from this conversation?"
# If yes → save to your memory system
```

### 2. Memory Flash (at 50% context)

```python
# When context hits 50% capacity:
# 1. Compress recent conversation
# 2. Keep first 3 + last 4 messages
# 3. Summary → memory system
```

### 3. Skills Tracker (every 15 calls)

```python
# After 15 tool calls:
"Did we develop a new technique worth saving?"
# If yes → save as skill
```

### 4. Programmatic Gate (security)

```python
# Before any write to memory, verify:
scan_for_prompt_injection(text)        # Check for injection patterns
check_for_invisible_characters(text)   # Check for hidden chars
verify_no_duplicates(text)             # Check for duplicates
# Only write if ALL checks pass
```

---

## Implementation

### Crontab setup

```bash
# Memory Nudge — check every 10 exchanges
# (tracked in session counter)

# Memory Flash — when context high
# (triggered automatically by context monitoring)

# Skills Tracker — every 15 tool calls
# (counter in session)
```

---

## Commands

```bash
# Test all techniques
python3 scripts/hermes_test.py

# Test specific technique
python3 scripts/hermes_test.py --technique memory_nudge
python3 scripts/hermes_test.py --technique memory_flash
python3 scripts/hermes_test.py --technique skills_tracker
python3 scripts/hermes_test.py --technique programmatic_gate
```

---

## Architecture

```
hermes-skills/
├── SKILL.md
├── scripts/
│   ├── hermes_nudge.py    # Memory Nudge
│   ├── hermes_flash.py    # Memory Flash
│   ├── hermes_tracker.py  # Skills Tracker
│   └── hermes_gate.py     # Programmatic Gate
└── references/
    └── hermes-protocol.md
```

---

_In Altum Per Evolution._
Hermes Skills v1.0.0