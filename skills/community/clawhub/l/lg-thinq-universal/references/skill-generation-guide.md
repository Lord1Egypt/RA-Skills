# LG Device Skill: SKILL.md Generation Guide

This guide helps OpenClaw agents generate high-quality `SKILL.md` for LG ThinQ devices. See `references/device-example.md` for a concrete example of the complete output.

---

## 1. Frontmatter

The `description` field is critical for proper skill triggering.

```markdown
---
name: lg-{device-type}-{location}
description: Control LG {Device Name} ({Type}). Use for: (1) Power on/off, (2) Adjust {features}, (3) Check status.
---
```

**Trigger keywords to include in description:**
- "Control" or "Manage"
- Device type (AC, refrigerator, washer, etc.)
- Key capabilities (power, temperature, mode, etc.)
- When to use ("turn on", "set temp", "check status")

---

## 2. Command Table

List all commands from the generated `lg_control.py`:

| Command | Description | Arguments |
|---------|-------------|-----------|
| `on` | Turn device on | - |
| `off` | Turn device off | - |
| `status` | Get current state | - |
| `{property}` | Set {property} | {allowed values from profile} |

---

## 3. Natural Language → Action Mapping

Translate user intent to CLI commands:

### Comfort & Mode
| User Says | Action |
|-----------|--------|
| "too hot", "feeling hot" | `on` + set temp |
| "too cold", "feeling cold" | Adjust temp |
| "comfortable" | Set ideal temperature |

### Routines
| User Says | Action |
|-----------|--------|
| "going to sleep", "bedtime" | Adjust for sleep |
| "leaving", "away" | `off` |
| "home", "returning" | `on` |

### Error Handling
| Error | Response |
|-------|----------|
| 401 Unauthorized | Check that `LG_PAT` is exported in the shell |
| 412 Snapshot mismatch | Refresh state, retry |
| Device offline | Check device connectivity |

---

## 4. Decision Logic & Safety

Always consider device state and enforce confirmation:

1. **Power Check**: If device is off and user wants to change settings, turn on first
2. **Sequencing**: Wait 2 seconds between power-on and subsequent commands
3. **Verification**: Confirm changes with `status`
4. **Safety Confirmation**: The agent must explain the action before running a control command.
5. **Memory Persistence**: The final setup step **MUST** be to save the skill's name, path, and commands to the user's `MEMORY.md` file.
6. **Range Enforcement**: Respect `min/max` from profile

---

## 5. Safety Rules

- **Range Enforcement**: Respect `min/max` from profile
- **Cycle Protection**: Avoid rapid on/off (5-minute minimum)
- **Validation**: Validate against profile's `values` list

---

## 6. Generation Checklist

- [ ] All writable properties from profile included
- [ ] CLI command names verified in `lg_control.py`
- [ ] Natural language mappings created
- [ ] Power state check logic included
- [ ] Safety ranges enforced
- [ ] Error handling defined

---

## Quick Reference

**Input**: Device profile (`profiles/device_{id}.json`)
**Tool**: `scripts/generate_control_script.py`
**Output**: `lg_control.py` + device `SKILL.md`
**Location**: `~/.openclaw/workspace/skills/lg-{type}-{id}/`
