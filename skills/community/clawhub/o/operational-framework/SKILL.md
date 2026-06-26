---
name: Operational Framework
slug: operational-framework
version: 1.0.0
description: "A disciplined, reproducible workflow for AI agents to log decisions, create rollback snapshots, and generate briefings for any change or feature implementation."
changelog: "Initial polished release – generic, community‑ready"
metadata: {"requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/.openclaw/workspace/"]}
---

# Operational Framework

A disciplined approach to implementing changes with full traceability.

## When to Use

- Implementing improvements or new features
- Making configuration changes
- Any work that needs rollback capability
- Generating case study briefings

## Architecture (generic)

```
<workspace>/
├── decisions/          # Decision logs (JSON per day)
│   └── <date>.json    # Example: 2026‑05‑08.json
├── rollbacks/         # Snapshot directories
│   └── <timestamp>/   # Example: 2026‑05‑08_2005/
├── briefings/         # Case‑study markdown files
│   └── <date>.md      # Example: 2026‑05‑08.md
└── TODO.md            # Persistent task list
```

Replace `<workspace>` with the root of your OpenClaw workspace (usually `~/.openclaw/workspace`).

## Decision Logging (generic)

Log each major decision *before* you start changing anything. Use a simple JSON schema:

```json
{
  "id": "dec_<date>_<seq>",
  "timestamp": "<ISO‑8601>",
  "title": "<short description>",
  "context": "<why this decision matters>",
  "options_considered": ["<opt1>", "<opt2>", "<opt3>"],
  "chosen": "<selected option>",
  "reasoning": "<rationale>",
  "expected_outcome": "<what success looks like>",
  "risk_mitigation": "<how to handle failure>",
  "status": "pending|implemented|reverted"
}
```

**How to log:**
- Manually edit a file in `decisions/` (e.g., `2026-05-08.json`).
- Or, if you have a CLI wrapper, run:
```
/decide "<title>" --context "<ctx>" --options "opt1|opt2|opt3" --chosen "opt2" --reasoning "<reason>"
```

Replace placeholders with your actual values.


## Rollback System (generic)

Take a lightweight snapshot *before* you modify anything. The snapshot can be a simple copy of files or a git commit.

**Typical workflow:**
1. Choose a name (e.g., `2026-05-08_2005`).
2. Copy the relevant files or the whole workspace into `rollbacks/<name>/`.
3. Verify the copy.
4. If needed, restore by copying back.

Example (shell‑style, adapt to your environment):
```bash
# Create snapshot directory
mkdir -p rollbacks/2026-05-08_2005
# Copy files you care about (or the whole workspace)
cp -r decisions rollbacks/2026-05-08_2005/
cp -r briefings rollbacks/2026-05-08_2005/
# ... add other paths as needed
```

**Listing snapshots:**
```bash
ls -1 rollbacks/
```

**Restoring:**
```bash
cp -r rollbacks/2026-05-08_2005/* <workspace>/
```

The exact commands can be wrapped in a script for convenience.

## Implementation Workflow

### 1. Decision Phase
- Log the decision with full context
- Define success criteria
- Identify rollback strategy

### 2. Snapshot Phase
- Capture current state
- Verify snapshot integrity

### 3. Implementation Phase
- Execute change
- Document as you go
- Test incrementally

### 4. Verification Phase
- Does it meet success criteria?
- Any unexpected side effects?

### 5. Briefing Phase
- Generate case study
- Note what worked/didn't
- Update TODO if follow-ups needed

## Briefing Format

```markdown
# Implementation Briefing: [Title]
**Date:** YYYY-MM-DD
**Decision ID:** dec_YYYY-MM-DD_XXX

## Context
[What triggered this]

## Decision
[What was decided and why]

## Implementation
[How it was implemented]

## Outcome
[Success/failure with evidence]

## Lessons Learned
- What worked well
- What would do differently
- Patterns to propagate

## Rollback Point
[Reference to snapshot if needed]
```

## Quick Commands (examples)

Below are *illustrative* commands you can bind to your own CLI or script. They are not built‑in OpenClaw commands, but they show the typical flow.

| Action | Example Shell / Pseudo‑Command |
|--------|---------------------------------|
| Log decision | `echo '{...}' >> decisions/$(date +%F).json` |
| Create snapshot | `./snapshot.sh <name>` (your wrapper script) |
| List snapshots | `ls -1 rollbacks/` |
| Restore snapshot | `./restore.sh <name>` |
| Generate briefing | `./brief.sh <decision‑id>` |
| Open TODO | `vim TODO.md` |

Feel free to adapt these to your preferred tooling (bash, Python, etc.).

## TODO Integration

Maintain `TODO.md` in workspace root:

```markdown
## 2026-05-08 Implementation Session

### Active
- [ ] Decision: Implement X
- [ ] Snapshot: AGENTS.md

### Completed
- [x] Decision: Add memory recall
- [x] Implemented: 2026-05-08
- [x] Briefing: briefings/2026-05-08.md
```

## Key Principles

1. **Log before acting** - Decisions documented before implementation
2. **Snapshot before change** - Always have a rollback path
3. **Brief after completion** - Document for future reference
4. **Never lose context** - Everything survives session restarts

## Integration

This framework integrates with:
- **Self-Improving skill** - Lessons feed into corrections.md
- **HEARTBEAT.md** - Periodic decision review
- **AGENTS.md** - Framework reference in operational procedures

## Requirements

- No credentials required
- No extra binaries required
- Works with existing workspace structure