---
name: planning-with-files
description: "This skill should be used when the user asks to start a complex task, research project, multi-step implementation, or any task expected to require more than 5 tool calls. Triggers: 'plan this', 'start planning', 'help me build', 'research and implement', 'complex task', '/plan'."
metadata: { "openclaw": { "emoji": "📋", "version": "1.0.0", "author": "shannon/openclaw-port" } }
---

# Planning with Files

Manus-style persistent markdown planning. Filesystem = long-term memory. Context window = working RAM.

## Core Principle

```
Context Window = RAM (volatile, limited)
Filesystem     = Disk (persistent, unlimited)
→ Anything important MUST be written to disk.
```

## When to Use

- Multi-step tasks (3+ phases or 5+ tool calls)
- Research + implementation tasks
- Tasks that span multiple sessions
- Any task where goal-drift is a risk

Skip for: single-file edits, quick lookups, simple questions.

## Session Start Protocol

**ALWAYS do this first — no exceptions:**

1. Run the init script to create the three planning files:
   ```
   exec: bash {baseDir}/scripts/init-session.sh "<task description>"
   ```
2. Fill in the `## Goal` section in `task_plan.md` with the full task description.
3. Break the task into 3–7 phases and add them under `## Phases`.
4. Confirm files exist before proceeding.

If exec is not available, create the three files manually using the templates in `{baseDir}/templates/`.

## The Three Files

### task_plan.md — Goal tracker (MOST IMPORTANT)
- Created at session start, never deleted
- Re-read before every major decision
- Update when: phase completes, decision made, error encountered

### findings.md — Knowledge store
- Research results, discoveries, technical decisions
- **2-Action Rule**: after every 2 view/search/fetch operations → update findings.md immediately

### progress.md — Session log
- Actions taken, test results, errors encountered
- Append-only; never rewrite history

## Work Loop

```
BEFORE every major action:
  → Re-read task_plan.md (keeps goal in attention)

EVERY 2 view/search/fetch operations:
  → Save key findings to findings.md NOW

AFTER completing a phase:
  → Update phase status in task_plan.md to "complete"
  → Append phase summary to progress.md

WHEN an error occurs:
  → Log it in task_plan.md under ## Errors table
  → Never repeat the same failing action

BEFORE stopping:
  → Run: exec bash {baseDir}/scripts/check-complete.sh
  → Only stop if all phases show "complete"
```

## File Update Rules

| Trigger | File to update | Section |
|---------|---------------|---------|
| Start task | task_plan.md | Goal + Phases |
| 2nd research op | findings.md | Key Findings |
| Make decision | findings.md | Technical Decisions |
| Phase done | task_plan.md | Phase status → complete |
| Phase done | progress.md | Phase summary |
| Error | task_plan.md | Errors table |
| Test result | progress.md | Test Results |

## Error Recovery Protocol

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully → identify root cause → targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different tool/library/method
  → NEVER repeat the exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions → search for solutions → update plan

AFTER 3 FAILURES:
  → Escalate to user: explain what was tried, share the error, ask for guidance
```

## Completion Verification

Before telling the user the task is done:
1. Run `exec bash {baseDir}/scripts/check-complete.sh`
2. If any phase is NOT "complete" → continue working
3. Only deliver result when all phases are checked off

## Session Recovery

If context was cleared (e.g., `/clear`), resume by:
1. Reading `task_plan.md` to restore goal and phase status
2. Reading `progress.md` to see what was done
3. Reading `findings.md` to restore research context
4. Continuing from the first incomplete phase

## Key Principles

- **Plan is Required**: Never start a complex task without `task_plan.md`
- **Files are Memory**: Context is volatile. Filesystem is permanent. Write important things down.
- **Never Repeat Failures**: Track what was tried. Mutate the approach.
- **Error Recovery = Agentic Behavior**: How you handle failures defines task quality.
- **Re-read Before Deciding**: Attention manipulation — keep the goal visible.
