# Memory Template — Jarvis

Create `~/jarvis/memory.md` with this structure:

```markdown
# Jarvis Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | proactive | on_request | local_only | restricted | paused

## Activation Rules
<!-- When Jarvis should auto-activate and when it should stay quiet -->

## Executive Context
<!-- User role, operating tempo, key stakeholders, recurring priorities -->

## Response Pattern
<!-- Preferred briefing length, tone, escalation style, handoff style -->

## Boundaries and Vetoes
<!-- Actions that need approval, tone lines not to cross, forbidden behavior -->

## Active Profile
<!-- Approved mission, traits, priority ladder, and anti-goals -->

## Notes
<!-- Durable observations that sharpen Jarvis behavior over time -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Jarvis mode is still being shaped | Learn quietly from real usage |
| `proactive` | Jarvis may auto-activate in approved contexts | Use executive framing when stakes justify it |
| `on_request` | Jarvis only activates when explicitly invoked | Stay dormant otherwise |
| `local_only` | Use local memory only | Avoid workspace seed edits |
| `restricted` | Jarvis is allowed only in named contexts | Stay silent outside those boundaries |
| `paused` | User wants less of this behavior for now | Read existing memory but stop expanding it |

## Local Files to Initialize

```bash
mkdir -p ~/jarvis/snapshots
touch ~/jarvis/{memory.md,active-profile.md,mission-log.md,workspace-state.md}
```

## Supporting File Shapes

`active-profile.md`
```markdown
# Active Jarvis Profile
- Mission:
- Priority ladder:
- Observable behaviors:
- Vetoes:
```

`mission-log.md`
```markdown
# Mission Log
## YYYY-MM-DD
- Situation:
- Recommendation style:
- Follow-through note:
```

`workspace-state.md`
```markdown
# Workspace State
- AGENTS.md:
- SOUL.md:
- HEARTBEAT.md:
- Notes:
```

## Key Principles

- Keep the profile compact enough to load before non-trivial work.
- Store natural-language behavior rules, not machine-like config blobs.
- Prefer observed user preference over guessed style.
- Snapshot before major profile changes instead of silently overwriting them.
