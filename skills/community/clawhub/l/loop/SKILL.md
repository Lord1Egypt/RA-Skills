---
name: Loop
slug: loop
version: 1.0.2
description: Run iterative agent loops until success criteria are met. Controlled autonomous iteration.
changelog: Fixed internal contradiction about Git commits in memory.md
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## Data Storage

```
~/loop/
├── active.json         # Currently running loops
├── history/            # Completed loop logs
│   └── {loop-id}.json
└── learnings.md        # Cross-loop patterns
```

Create on first use: `mkdir -p ~/loop/history`

## Scope

This skill:
- ✅ Runs iterative attempts toward defined success criteria
- ✅ Logs each iteration with learnings
- ✅ Exits on success, max iterations, or unrecoverable error
- ❌ NEVER makes Git commits automatically
- ❌ NEVER deploys to production
- ❌ NEVER modifies system configuration
- ❌ NEVER runs indefinitely (max 10 iterations hard limit)

## Quick Reference

| Topic | File |
|-------|------|
| Loop examples | `examples.md` |
| Memory between iterations | `memory.md` |

## Core Rules

### 1. Pattern
```
Task + Criteria → Execute → Verify → [Pass? Exit : Retry]
```

### 2. Required Setup
| Element | Required | Example |
|---------|----------|---------|
| Task | Yes | "Fix failing tests" |
| Success criteria | Yes | "All tests pass" |
| Max iterations | Default: 5 | Max: 10 |
| Verify command | Recommended | `npm test` |

### 3. When to Propose
- Task has clear success criteria but uncertain path
- Previous attempt failed but error is fixable
- User says "keep trying until..."

**NOT for:** One-shot tasks, undefined goals, exploratory work

### 4. Each Iteration
1. **Fresh context** — Only carry: task, criteria, count, learnings
2. **Execute** — Attempt the task
3. **Verify** — Check success criteria
4. **Record** — Append to history: what worked, what failed
5. **Decide** — Pass? Exit. Fail? Retry if under limit.

### 5. Stopping Conditions
- ✅ Success criteria met
- ❌ Max iterations reached
- ⚠️ Unrecoverable error (missing dependency, permission denied)

### 6. On Failure
If max reached without success:
- Summarize all attempts
- Identify common failure pattern
- Recommend manual intervention or different approach

### 7. Safety
- Hard limit: 10 iterations maximum
- No destructive actions without explicit per-action approval
- Log everything to ~/loop/history/
