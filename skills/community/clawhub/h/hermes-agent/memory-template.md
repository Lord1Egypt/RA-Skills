# Memory Template - Hermes Agent

Create `~/hermes-agent/memory.md` with this structure:

```markdown
# Hermes Agent Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | active | local_only | paused | declined

## Workspace Snapshot
<!-- Which OpenClaw files were extended and what each block does -->

## Active Rules
<!-- Short execution rules that should influence future work -->

## Promotion Signals
<!-- Repeated workflows worth turning into skills or stable operating rules -->

## Notes
<!-- Internal observations that sharpen behavior without becoming hard rules -->

---
Updated: YYYY-MM-DD
```

## Supporting Files

Create this directory structure on first activation:

```bash
mkdir -p ~/hermes-agent/archive
touch ~/hermes-agent/{memory.md,promotions.md,reflections.md,workspace-state.md}
```

## promotions.md Template

```markdown
# Hermes Agent Promotions

## Pending
- Pattern:
  Evidence:
  Scope: global | domain | project
  Next step: keep as rule | promote to skill | discard
```

## reflections.md Template

```markdown
# Hermes Agent Reflections

## YYYY-MM-DD
- Context:
  Outcome:
  Lesson:
  Reusable: yes | no
```

## workspace-state.md Template

```markdown
# Hermes Workspace State

## Seeded Files
- AGENTS.md:
- SOUL.md:
- HEARTBEAT.md:

## Constraints
- Repos or paths excluded from automatic Hermes behavior
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | still learning the user's preferred Hermes mode | keep adapting lightly |
| `active` | full loop is installed and in use | retrieve, reflect, and promote normally |
| `local_only` | local memory only, no workspace seeding | use Hermes behavior without editing workspace files |
| `paused` | user wants a temporary stop | read existing memory but stop expanding it |
| `declined` | user does not want Hermes mode | do not prompt again unless asked |

## Key Principles

- Keep memory.md short enough to read before non-trivial work.
- Store operating rules in natural language, not machine-like config blobs.
- Promote only patterns with repeated evidence.
- Archive stale lessons instead of deleting them silently.
