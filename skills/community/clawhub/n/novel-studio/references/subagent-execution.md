# Subagent Execution

This reference defines the shared parent-orchestrated subagent protocol for `drafting`, `polishing`, and `proofreading`.

The execution package is runtime-only. Canonical workflow state remains file-backed.
Do not persist runtime subagent ids, session ids, raw execution packages, or raw subagent conversation history.
If anything must survive interruption, persist only lightweight execution summaries and lightweight progress events.

## 1. Parent role
- parent agent is the orchestrator
- parent agent validates preconditions
- parent agent assembles curated context
- parent agent dispatches with `fork_context = false`
- parent agent validates results before advancing state

The parent owns stage gating, package construction, dispatch, result validation, and workflow state transitions.

Autopilot does not change this ownership model:
- bounded automation does not turn the parent into the inline drafting / polishing / proofreading executor
- `drafting`, `polishing`, and `proofreading` still belong to their subagents even when autopilot is active
- parent-side automation may only advance safe gates; final review remains manual
- keep surfacing merged chapter progress during automation from file-backed state
- if a child returns `blocked` or `needs_clarification`, stop autopilot with an explicit reason and wait for manual resume

## 2. Execution Package
Every child dispatch must include an inline execution package with these fields:
- task type
- project root
- stage
- batch range
- target files
- overwrite flag
- required inputs
- must-not-modify list
- output contract
- acceptance hints

Execution package shape rules:
- `task type` must be one of `drafting`, `polishing`, or `proofreading`
- `project root` is the absolute root for the active novel project
- `stage` must match the delegated workflow stage for this dispatch
- `batch range` must identify the approved scope for this dispatch
- `target files` must be explicit project-root-relative file paths only
- `target files` must not use globs, directory-only targets, `..`, or ambiguous path expansion
- path lists in the package and result must not contain duplicate entries
- `drafting` target files must be non-empty and stay under `manuscript/`
- `polishing` target files must be non-empty and stay under `manuscript/`
- `proofreading` target files must be an empty list
- `overwrite flag` is a boolean for this dispatch only
- `proofreading` must set `overwrite flag` to `false`
- `required inputs` must be a structured named map, not freeform prose
- `required inputs.batchRange` must match `batch range`
- `required inputs.chapterLabels` must be a non-empty ordered chapter label list for this dispatch
- every stage package must include non-empty `outline`, `batchPlan`, and `characterFiles`
- every stage package must include non-empty `styleBible`, `mainlineSpec`, `platformProfile`, `trackGuide`, and `ledgerSnapshot`
- every stage package should also carry the approved `openingDesign` once the project enters prose drafting
- file-backed `required inputs` content must match the parent snapshot captured in `validationContext.baselineFiles`
- `drafting` and `polishing` `required inputs.chapterLabels` must exactly match `target files` order
- `proofreading` `required inputs.chapterLabels` must cover the full approved batch scope
- `polishing` packages must include non-empty `polishingFocus`
- `polishing` `required inputs.manuscriptFiles` must exactly match `target files`
- `polishing` `target files` must already exist in the baseline snapshot
- `proofreading` packages must include non-empty `required inputs.manuscriptFiles`
- `proofreading` `required inputs.manuscriptFiles` must match the baseline manuscript snapshot
- `must-not-modify list` must be explicit project-root-relative file paths only
- for `drafting` and `polishing`, `must-not-modify list` must exactly equal `baselineFiles - targetFiles`
- `proofreading` `must-not-modify list` must cover the full project snapshot
- `output contract` must state explicit required files and required return fields
- `output contract.requiredReturnFields` must exactly match the shared protocol field list
- `output contract.mustWriteFiles` must exactly match `target files`
- `proofreading` `output contract.requiredStageFields` must exactly list `judgment`, `continuity`, `logic`, `characterOOC`, `blockers`, and `fixDirection`
- `validationContext.executionPackageDigest` must match the canonical digest of `executionPackage`
- `validationContext.baselineFilesDigest` must match the canonical digest of `baselineFiles`
- `validationContext.bundleFingerprint` must match the canonical digest of the validation metadata plus those two digests
- `acceptance hints` must match the canonical stage reminder list for the delegated stage
- `acceptance hints` are optional natural-language reminders and never override output contract or stage rules

Execution packages are runtime-only dispatch payloads. They are not the canonical workflow record.

## 3. Child Return Contract
Every child must return a structured result containing these fields:
- status
- changedFiles
- createdFiles
- blockedReasons
- summary
- notesForNextStage
- risks

Allowed `status` values are `completed`, `blocked`, or `needs_clarification`.

Return field rules:
- `changedFiles` and `createdFiles` must be explicit project-root-relative path lists
- `blockedReasons` and `risks` must be string lists
- `blockedReasons` and `risks` should be empty lists when not needed
- `blocked` and `needs_clarification` must include non-empty `blockedReasons`
- `completed` must keep `blockedReasons` empty
- `summary` should briefly describe what was completed or why progress stopped
- `notesForNextStage` should be a short string or an empty string
- if `status` is `blocked` or `needs_clarification`, `changedFiles` and `createdFiles` must both be empty
- if `status` is `completed`, every `outputContract.mustWriteFiles` entry must be touched by the current dispatch
- `status` is the protocol execution state. Stage judgments such as `acceptable`, `conditionally acceptable`, and `needs revision` are separate stage-specific outputs.
- `proofreading` completed results must include non-empty `continuity`, `logic`, `characterOOC`, and `fixDirection` strings
- if `proofreading judgment` is `needs revision`, `blockers` must be non-empty
- if `proofreading judgment` is `acceptable`, `blockers` must be empty
- if `proofreading judgment` is `conditionally acceptable`, `blockers` must be empty and `risks` must be non-empty

## 4. Failure Handling
- fail closed
- infrastructure failure: may retry once
- protocol failure: reject result
- content failure: do not advance
- no silent inline fallback

Infrastructure failure means dispatch or transport failed before a valid child result was produced; the parent may automatically retry once. Protocol failure means the child response is missing required fields, violates the contract, writes outside approved boundaries, or otherwise fails validation; the parent must reject the result and stop advancement. Content failure means the child returned a structurally valid result, but the stage output still fails stage-specific quality or completeness requirements; the parent must keep the workflow in the current stage and stop advancement.

## 5. Parent Acceptance Duties
Before advancing canonical file-backed workflow state, the parent must:
- validate the execution package itself before trusting the child result
- confirm the returned `status` is one of `completed / blocked / needs_clarification`
- verify non-completed statuses returned zero file writes
- verify completed results actually touched every required `outputContract.mustWriteFiles` path
- compare the actual filesystem diff against `changedFiles` and `createdFiles` and reject mismatches
- verify `changedFiles` and `createdFiles` stay within the approved target files and overwrite policy
- verify the child respected the must-not-modify list
- verify any stage-specific judgment separately from protocol `status`
- reject incomplete, malformed, or out-of-bounds results
- persist only accepted workflow state updates to file-backed state
- avoid persisting runtime subagent ids
- update file-backed chapter progress from accepted dispatch transitions rather than chat memory

If acceptance fails, the parent must stop, surface the failure clearly, and wait for an explicit next action instead of silently continuing inline.

## 6. Parent Runtime Loop
1. run `scripts/build_stage_execution_package.py`
2. send only `executionPackage` to the child
3. keep `validationContext` parent-side only
4. run `scripts/extract_stage_subagent_result.py` on the child raw response
5. run `scripts/validate_stage_execution_result.py`
6. run `scripts/apply_stage_execution_result.py` only after validation passes

The parent runtime loop is strict:
- keep `taskType`, `stage`, and `validationContext.stage` aligned for the same dispatch
- build the bundle immediately before dispatch
- keep `validationContext.baselineFiles` as a parent-generated snapshot of normalized relative paths mapped to `{ sha256, size }`
- each `baselineFiles` entry must use a 64-character lowercase hex `sha256` and a non-negative integer `size`
- if a sidecar manifest is present, validate it against the bundle file before trusting the bundle contents
- if `manifest.promptFile` and `manifest.promptSha256` are present, validate the prompt file contents before trusting the dispatch artifacts
- do not modify project files after bundle build and before validation finishes
- if parent-side files changed or the session was interrupted, discard the old bundle and rebuild a fresh one
- treat non-JSON child output as protocol failure before validation
- never send `validationContext` to the child
- never apply a child result before validation succeeds
- never persist the raw execution bundle into canonical project state

## 7. Child Prompt Contract
- return one structured result only
- do not echo the full execution package back
- do not claim completion without populated protocol fields
- if the package is insufficient, return `needs_clarification` with zero file writes

When prompting the child:
- restate the stage-specific write boundary
- restate the must-not-modify list
- require the child to return the shared protocol fields exactly once
- require proofreading children to return protocol `status` and separate stage judgment fields
