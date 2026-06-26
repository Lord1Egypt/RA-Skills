# Subagent Proofreading

## Default Mode
- proofreading must use a proofreading subagent by default
- parent runtime should prefer `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`
- parent dispatch still uses `fork_context = false`
- child receives prompt text only; dispatch artifacts stay parent-side

## Read-Only Rule
- this role is read-only
- must not modify manuscript files
- must not modify any project file
- execution package must set `target files` to an empty list
- execution package must set overwrite flag to false
- execution package must set `must-not-modify list` to an explicit project-root-relative path list that covers the entire project
- execution package must set `output contract.mustWriteFiles` to an empty list
- execution package must set `output contract.requiredStageFields` to `judgment`, `continuity`, `logic`, `characterOOC`, `blockers`, and `fixDirection`
- `requiredInputs.manuscriptFiles` must match the baseline manuscript snapshot exactly
- this subagent is a batch gate, not a silent fixer

## Parent Preconditions
- current stage is proofreading
- polishing output exists
- polishing approved
- approved chapter-plan package exists
- usable outline available
- usable character package available
- recap context available when relevant

## Required Judgment
- acceptable
- conditionally acceptable
- needs revision
- continuity
- logic
- character-OOC
- blocker list or explicit no-blocker
- completed proofreading results must keep protocol `blockedReasons` empty
- recommended fix direction

## Acceptance Checklist
- no project files modified
- required review dimensions covered
- explicit judgment
- blockers concrete enough to route upstream
- if judgment is `needs revision`, blockers must be non-empty
- if judgment is `acceptable`, blockers must be empty
- if judgment is `conditionally acceptable`, blockers must be empty and risks must be non-empty
- continuity / logic / character-OOC / fix direction must be explicit non-empty strings
