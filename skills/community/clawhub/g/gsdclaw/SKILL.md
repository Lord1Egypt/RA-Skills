---
name: gsd-claw
description: >
  Spec-first execution workflow for OpenClaw that turns large, vague, or messy
  project requests into phased, verifiable implementation plans. Helps build,
  rescue, refactor, redesign, organize, and finish apps, features, interfaces,
  and multi-step technical work with scope control, acceptance criteria, and
  incremental verification. Use when: planning a substantial project, scoping a
  feature, rescuing a broken codebase, refactoring an app, improving UI/UX,
  stabilizing a messy implementation, or finishing work that drifted out of
  control.
license: MIT-0
category: productivity
emoji: "🦞"
version: 1.0.0
homepage: https://github.com/gsd-build/get-shit-done
metadata:
  openclaw:
    requires:
      bins: []
      env: []
---

# GSD-Claw

Run medium and large project work without letting scope, structure, or context drift.

## Quick Start

Use this workflow when a request is too large, vague, messy, or failure-prone to execute in one pass.

Default sequence:
1. map current state
2. rewrite request into a build spec
3. define phases
4. set acceptance criteria
5. execute in narrow batches
6. verify after each meaningful step
7. report real status without pretending everything is done

## Security Notes

- This skill is instruction-only.
- It does not require credentials, external APIs, or special binaries.
- It should not claim integrations are real unless they were actually implemented and verified.
- If a project contains secrets, private URLs, or credentials, keep them out of reusable/public skill content.

## Core Workflow

### 1. Map the current state
- Inspect the existing project before proposing major changes.
- Identify stack, entrypoints, broken areas, constraints, and likely risks.
- Prefer short factual notes over speculation.

### 2. Convert the request into an execution spec
- Rewrite the user request into a short internal build spec.
- Separate:
  - objective
  - required outcomes
  - quality bar
  - exclusions / unknowns
  - dependencies / blockers
- If the request is broad, define a practical v1 that still honors the user’s intent.

### 3. Define phases
- Break the work into small phases with visible outputs.
- Each phase must be independently verifiable.
- Prefer this shape when applicable:
  1. stabilize current project
  2. architecture / structure cleanup
  3. UX / UI redesign
  4. core features
  5. integrations / configuration
  6. validation / polish

### 4. Set acceptance criteria before implementation
- Define what “done” means in observable terms.
- Prefer criteria such as:
  - page renders
  - button works
  - form persists
  - config saves
  - layout is responsive
  - build passes
  - no obvious runtime errors

### 5. Execute in narrow batches
- Avoid giant rewrites unless they are clearly safer.
- Prefer a short loop:
  - edit
  - verify
  - continue
- When files are large or write operations are fragile, work in smaller modules and validate after each change.

### 6. Verify aggressively
- After each meaningful step, verify with the strongest available method:
  - file inspection
  - build/run
  - browser/manual rendering check
  - test command
  - diff/output review
- Never assume success from writing alone.

### 7. Report like a builder
- Summarize:
  - what changed
  - what was verified
  - what remains
  - current blockers
- Do not claim completion if major paths are still broken.

## Operating Rules

- Prefer one canonical implementation path. Remove ambiguity before multiplying files.
- Do not leave duplicate competing files unless there is a clear migration reason.
- If the codebase gets fragmented, stop and consolidate before adding more features.
- If the request includes redesign, prioritize information architecture and usability before visual polish.
- If the request includes integrations (APIs, providers, messaging, AI), separate:
  - UI/config capture
  - config persistence
  - connection test
  - real runtime integration
- Clearly distinguish simulated integration from real integration.

## Anti-Context-Drift Rules

- Re-anchor on the user goal before each major phase.
- Prefer short execution plans over long narrative plans.
- Keep a single source of truth for current state.
- If implementation starts drifting, rewrite the project status as:
  - done
  - in progress
  - blocked
  - next
- If a previous attempt produced broken or truncated files, treat that as technical debt and fix it before adding scope.

## Rescue / Salvage Mode

When the existing project is already in a bad state:
1. identify the canonical entrypoint
2. identify duplicated or broken artifacts
3. choose what to keep
4. remove or ignore dead paths
5. restore a minimal working baseline
6. only then continue feature work

Prefer restoring one working path over preserving every partial attempt.

## UI/UX Mode

When improving UI/UX:
- fix structure before styling
- improve hierarchy, spacing, labels, navigation, and flows first
- ensure actions are obvious and feedback is visible
- make primary actions dominant and secondary actions quieter
- ensure empty states, loading states, and error states exist where relevant

## Configuration-Heavy Products

When the app includes provider setup pages, model the feature in this order:
1. provider selector
2. credential fields
3. help/instructions
4. save state
5. connection test
6. runtime usage

Never present a configuration screen as fully functional if it only stores fields locally. Make the distinction explicit in implementation notes and validation.

## Completion Standard

A task is only finished when:
- the main path works end-to-end, or
- the remaining gap is explicitly limited to external dependency/blocker work

If blocked, provide the smallest next unblock step.

## File Reference

Read these when needed:
- `references/execution-template.md` — convert vague requests into a practical build spec
- `references/acceptance-checklist.md` — completion criteria and verification prompts
