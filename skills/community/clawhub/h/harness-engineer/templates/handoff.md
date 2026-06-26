# HANDOFF -- <timestamp>
Reason: context-reset | session-end | sub-agent | compact

## System State
Phase: <current harness phase: research | plan | implement | verify | reflect>
Cycle: NNN
Loop mode: single-pass | maintenance | continuous
Last checkpoint commit: <git SHA or "none">

## Current Task
Task ID: T-NNN
Task description: <one sentence>
Status: <what was completed, what remains>
Next step: <exact next action for resuming agent -- be specific>

## Active Constraints
<list prevention rules from references/constraints.md that apply to current work>

## Plan Reference
Plan: PLAN-NNN.md
Plan approval: <timestamp of human approval or "pending">

## Open Questions / Blockers
<list any unresolved decisions, conflicts, or blockers>
<for each: describe what is needed to resolve>

## Files Modified This Session
<list of file paths only -- no contents>

## Recovery Instructions
1. Read docs/status/PROGRESS.md
2. Read <PLAN-NNN.md>
3. Run: git log --oneline -5 (verify last checkpoint)
4. Read references/constraints.md
5. Read MEMORY.md
6. Resume from "Next step" above
