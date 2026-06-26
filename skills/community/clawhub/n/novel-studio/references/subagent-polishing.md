# Subagent Polishing

## Default Mode
- polishing must use a polishing subagent by default
- parent runtime should prefer `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`
- parent dispatch still uses `fork_context = false`
- child receives prompt text only; dispatch artifacts stay parent-side

## Required Input
- every execution package must include `polishingFocus`
- chapter-plan package for the current batch
- usable outline
- usable character package
- style baseline or tone target
- file-backed inputs must match the parent baseline snapshot exactly

## Allowed Writes
- only parent-approved target manuscript files
- target files must be non-empty and stay under `manuscript/`
- target files must already exist in the baseline snapshot
- `requiredInputs.manuscriptFiles` must exactly match the approved target files
- `must-not-modify list` must exactly equal the baseline snapshot minus `target files`
- must preserve approved plot intent, outline alignment, and role voice
- must not silently change upstream planning assumptions

## Parent Preconditions
- current stage is polishing
- draft output exists
- draft approved
- chapter-plan package exists
- usable outline present
- usable character package present
- target batch complete enough
- focus explicit
- use `scripts/subagent_dispatch_runtime.py` when the parent is coordinating this stage in Python

## Acceptance Checklist
- only allowed manuscript files changed
- planning-character-recap-state untouched
- explicit summary of improvements
- substantive editorial review exists
- explicit optimization suggestions exist
- result still aligns with chapter plan and outline intent
- risks surfaced
