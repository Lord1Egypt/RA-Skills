# Termination Conditions & Escalation Protocol (F47, v1.10.3)

WHY: Vibe-coding / loop-coding agents run until something stops them. Without explicit
termination conditions, they loop forever, burn budget, and produce spaghetti.

---

## Mandatory: TERMINATION CONDITIONS in PROGRESS.md

Before ANY loop-coding task, the agent MUST write to `brain/plans/PROGRESS.md`:

```markdown
## [DATE] [TIME] | Cycle: [NAME]
- Task: [what]
- Attempt: [N]/3
- DONE means: [concrete metrics — e.g. "pytest 14/14 green", "build_skill --check OK"]
- FAILED means: [concrete — e.g. "fuzz < 45/56", "runtime_integration_tester exits 1"]
- Max iterations: 3 (hard limit)
```

After 3 failed attempts → **STOP + ESCALATE** (do not attempt 4th).

---

## Loop Stability Checks (run every 2-3 iterations)

| Pattern | Signal | Action |
|---------|--------|--------|
| Dead retry | Same error 3× | Change approach (not "try harder") |
| Oscillation | Fix A breaks B, fix B breaks A | STOP, ask human for plan |
| Drift | Task lost / context gone | Re-read PROGRESS.md + memory + session_search |
| Amplification | Each change makes it worse | `git revert`, restart from clean |
| Feedback starvation | Tests green, UI broken | Visual/functional check, not just unit |

---

## De-Sloppify (every 2-3 iterations)

- Delete `print()` / `debugPrint` / unused imports
- Delete commented-out code
- Delete unused variables/widgets
- Verify comments not stale

---

## Escalation Template

```
🛑 ESCALATION: [task]
- 3/3 attempts failed
- Last error: [specific]
- Tried: [approach 1, 2, 3]
- Need: [human decision / new approach / scope reduction]
```