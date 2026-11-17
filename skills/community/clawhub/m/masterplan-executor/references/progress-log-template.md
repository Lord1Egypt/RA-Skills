# Execution Log Template

Write this to `docs/masterplan/execution-log.md`, create it on first run if it doesn't exist, and update it at the end of every phase (per `references/phase-execution-checklist.md` step 6). This file is the persistent memory of execution across sessions — treat it as load-bearing, not a nice-to-have.

```markdown
# Execution Log — <Project Name>

Masterplan: docs/masterplan/masterplan.md
Last updated: <date>

## Status Overview

| Phase | Status | Completed On |
|---|---|---|
| Phase 1 — <name> | done / in progress / not started | <date or —> |
| Phase 2 — <name> | ... | ... |

## Phase 1 — <name>

### What was built
<Plain description of what actually exists now, specific enough that someone could
verify it against the masterplan's acceptance criteria without reading the code.>

### Research performed
- Question: <what was unclear>
  Source: <what was checked>
  Resolution: <what was decided and why>
(Repeat per research instance this phase. Omit section if none.)

### Deviations from the masterplan
- What the plan said: <...>
  What was actually done: <...>
  Why: <...>
(Omit section if none — deviations should be rare.)

### Self-audit result
- Blocker/Major findings: none, or list each with the fix applied
- Tests run: <what was executed, pass/fail>

### Next concrete step (only if phase is in progress, not done)
<Specific enough to resume without re-deriving state from the code.>

---

## Phase 2 — <name>
...
```

Keep entries factual and specific — this log exists so a gap can be proven absent, the same way the masterplan's own Coverage-style discipline proves nothing was silently dropped during planning. A vague entry ("phase 2 done, works fine") defeats that purpose as surely as not writing one at all.
