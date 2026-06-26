# Session Summary Template

Use this file as the default structure for end-of-session summaries and handoff updates in English.

When the user says things like:

- "Update the handover before we stop"
- "Summarize today's work and sync the README"
- "Write down today's problems, fixes, validation, and next steps"

follow this structure instead of writing a vague recap.

## Goal

The handoff must let a different person resume work quickly without rereading the full chat or rediscovering the same issues.

The summary is only good enough if the next person can answer all of these after reading `handover.md` and the relevant `README.md` sections:

1. What was actually changed today?
2. What was tried, what worked, and what failed?
3. What is still risky or unfinished?
4. What should be done next, first?
5. How do I run or verify the current state?

## Default Scope

Unless the user explicitly narrows the task, update all of:

1. `handover.md`
2. README sections directly affected by today's findings
3. nearby run instructions, caveats, or TODO notes when they became stale

Do not update only one file if the project's current understanding changed.

## Required Structure

Every handoff should cover the following sections.

### 1. Session scope and current objective

State:

- what the session was trying to achieve
- which repo area or feature was in scope
- whether the work is a prototype, MVP, or intended final solution

This gives the next person immediate orientation before they read details.

### 2. Current repo state

State the current practical state of the repo:

- which files were changed
- whether the changes are committed or still in the working tree
- whether there are related docs, scripts, configs, or environment assumptions

If repo state matters to resuming work, say so explicitly.

### 3. Problems actually encountered

Describe the real problems in a concrete way:

- exact error or broken behavior
- trigger condition
- why it blocks or degrades the product
- which core capability it affects

Avoid vague phrases such as "there were compatibility issues".

### 4. Root-cause analysis and conclusions

Write down the current best judgment:

- whether the issue came from code logic, environment, dependency behavior, system permissions, packaging, or product assumptions
- which hypotheses were ruled out
- the confirmed root cause or the current most credible conclusion

If something is still uncertain, label it as current judgment instead of pretending it is final.

### 5. Implemented changes

For each meaningful file or change set, state:

- file path
- what changed
- why it changed
- whether it is a durable solution or a temporary workaround

This section should be traceable to actual diffs.

### 6. Validation performed

List the checks that actually happened, for example:

- app start or build success
- command output that matters
- manual reproduction before and after the fix
- smoke tests, compile checks, unit tests, or integration tests

Do not write "verified" unless you state what was verified.

### 7. Known pitfalls, failed attempts, and important constraints

This section is mandatory.

Record:

- approaches already tried and rejected
- subtle environment constraints
- non-obvious gotchas
- assumptions that must stay true for the current solution to work

This is the section that prevents the next person from wasting time.

### 8. How to resume from here

Make resumption explicit:

- which file to open first
- which command to run first
- which result to check first
- what "good" versus "bad" behavior should look like

The next person should not have to infer the restart path.

### 9. Remaining issues and boundaries

List what is still incomplete or risky, for example:

- still dev-only, not ready for packaging
- still depends on a local tool or credential
- no automation yet
- only one platform was checked

Separate current capability from final desired capability.

### 10. Product direction or end goal

If the session discussed long-term product direction, record it:

- installer or packaged app target
- expected end-user workflow
- non-goals or temporary compromises

This prevents local patches from drifting away from the real target.

### 11. Ordered next TODOs

Do not write a one-line TODO.

Each item should explain:

- what to do
- why it matters
- what problem it resolves

Order the items in execution order whenever possible.

## Writing Rules

- Prefer concrete facts over abstract language.
- Name files, commands, runtime conditions, and observed behavior.
- Mark temporary fixes clearly as temporary.
- If something was not tested, say so directly.
- If the user has already stated a product goal, include it.
- Write so a different engineer can continue without reading the whole conversation.

## Recommended Trigger Phrases

Treat requests like these as signals to use this template:

- "summarize today's work"
- "update the handover"
- "sync the README and handover"
- "write down the current state for the next person"
- "capture the problems, fixes, and next steps before we stop"
