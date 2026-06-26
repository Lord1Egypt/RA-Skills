# Subagent Drafting

## Default Mode
- drafting must use a drafting subagent by default
- one subagent handles the approved current batch
- parent runtime should prefer `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`
- parent dispatch still uses `fork_context = false`
- child receives prompt text only; dispatch artifacts stay parent-side

## Allowed Writes
- only parent-approved target manuscript files
- target files must be non-empty and stay under `manuscript/`
- `must-not-modify list` must exactly equal the baseline snapshot minus `target files`
- no planning, recap, review, or state writes

## Overwrite Rule
- existing target files stay read-only unless parent sets `overwrite=true`
- fail closed when overwrite permission is missing or ambiguous
- this template assumes `overwrite=true` reflects an explicit parent-approved dispatch decision for the current target files

## Parent Preconditions
- current stage is drafting
- opening gate is explicitly approved before batch drafting starts
- chapter plan exists
- chapter plan is approved
- outline usable
- character package usable
- batch scope explicit
- no open approval gate blocks execution
- use `scripts/subagent_dispatch_runtime.py` when the parent is coordinating this stage in Python

## Acceptance Checklist
- only allowed files changed
- required files exist and are non-empty
- forbidden files untouched
- batch matches approved range
- return summary usable
