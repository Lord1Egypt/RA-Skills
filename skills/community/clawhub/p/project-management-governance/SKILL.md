---
name: project-management-governance
description: Use this skill for multi-step project work that requires structured intake, context discovery, scope control, environment awareness, evidence-driven debugging, synchronized documentation, and disciplined handoff.
---

# Project Management Governance

## Purpose

This skill applies a default project-governance workflow for complex work.
Use it when the task is not a trivial one-file edit and requires planning, coordination, debugging, structured implementation, or documentation-aware execution.

## When to use

Use this skill for:
- multi-step coding or refactoring
- debugging with incomplete context
- document-linked implementation
- environment-sensitive work
- release, migration, or deployment planning
- cross-file or cross-module changes
- tasks that require explicit progress tracking, risk control, or handoff

Do not over-apply it to trivial formatting edits or obvious one-line fixes.

## Default operating workflow

Before implementation, do not jump straight into code changes.

Default sequence:
1. Identify the project root and current working scope.
2. Read the main project overview document, if present.
3. Read the architecture, workflow, or implementation guide, if present.
4. Read the task-specific, module-specific, or feature-specific documentation related to the request.
5. Read active handoff, plan, worklog, issue, or temporary notes if the task appears to be part of an ongoing stream.
6. Only then decide whether the next step is clarification, inspection, planning, implementation, validation, or handoff.

## Task intake and scope control

Before making changes, clarify:
- the target outcome
- the affected files, modules, or deliverables
- whether this is planning, debugging, implementation, validation, or documentation work
- whether the task is local-only, environment-dependent, or production-sensitive
- what counts as success

If scope is ambiguous, first reduce ambiguity.
Do not silently widen the task.

## Environment awareness

Do not assume the execution environment.

Distinguish clearly between:
- local development
- test or staging environments
- production or target environments
- external systems or remote platforms

Never silently mix environment-specific paths, settings, credentials, or assumptions.
If environment facts are missing and they matter to the task, ask for them or propose readonly checks first.

## Evidence-first execution

Do not guess operational facts, root causes, or runtime parameters.

Before proposing risky changes, collect evidence such as:
- current file layout
- configuration state
- interfaces and contracts
- logs and stack traces
- sample inputs and outputs
- environment constraints
- dependency relationships
- existing documentation and recent notes

When evidence is missing, prefer:
- readonly inspection commands
- small validation steps
- probes
- minimal reproducible checks

## Planning policy

When a task is large enough to justify planning, produce a compact execution plan that includes:
- objective
- current state
- missing information
- dependencies
- risks
- smallest safe next step
- validation method

Prefer phased execution:
1. inspect
2. validate assumptions
3. make the smallest justified change
4. verify results
5. update documentation
6. record reusable learnings

## Debugging policy

Use evidence-driven debugging.

Default sequence:
1. inspect the current state
2. compare expected behavior with observed behavior
3. identify likely fault boundaries
4. propose 1 to 3 low-risk fixes
5. apply the smallest justified fix
6. validate the result
7. document the finding

Do not present speculation as confirmed diagnosis.

## Change management

Prefer small, reversible changes over broad rewrites.
When multiple solutions are possible, bias toward the option with:
- lower blast radius
- clearer validation path
- better alignment with existing project structure
- easier rollback

## Documentation synchronization

When behavior, structure, interfaces, workflows, assumptions, or operational instructions change:
- update the corresponding documentation in the same work cycle
- keep docs and implementation aligned
- note any remaining gaps explicitly if full sync is not yet possible

## Project-local learnings

Use project-local learnings as a staging layer for reusable findings.

Recommended files:
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`

Write to them when:
- a command fails in a reusable way
- a recurring misconception is corrected
- an environment constraint is discovered
- a safer execution pattern is found
- a missing but valuable capability is identified

Do not treat `.learnings/` as the final authority.
Promote stable conclusions into the project’s formal documentation structure after validation.

## Handoff and progress reporting

When reporting progress, distinguish clearly between:
- completed
- in progress
- blocked
- assumptions
- missing evidence
- next step

When handing off, include:
- what was checked
- what changed
- what remains unresolved
- how to validate the next step

## Output style for this skill

When operating under this skill:
- state what has been read
- separate facts from assumptions
- identify missing context explicitly
- avoid premature implementation
- prefer minimal safe next steps
- include validation and documentation follow-through