# Capability map

This document summarizes what the v2 scaffold can currently do.

## Task control plane

- create task records
- track lifecycle state
- record transition history
- store artifacts and worker metadata

## Decision layer

- evaluate done policies
- generate retry briefs
- resolve role-based pipeline presets
- classify environment failures
- recommend next orchestration action

## Execution layer

- generate worker briefs
- support a dedicated probe-mode brief for repo/runtime feasibility checks
- support a dedicated review-mode brief for next-step classification
- route prompts via `TaskFile`
- launch workers in sync or background mode
- reconcile background worker runs
- backfill some objective checks from worker summaries

## Current boundaries

- no fully reliable background session abstraction yet
- no robust PR/test/build parser yet
- environment capability varies with local CLI setup
- supervisor is semi-automatic rather than fully autonomous

## Practical interpretation

The skill is suitable for:
- local orchestration experiments
- supervisor-driven coding workflows
- structured implementation/review loops
- iterative hardening toward a fuller runtime

The skill is not yet ideal for:
- unattended production deployment
- deterministic CI-grade orchestration
- high-confidence automatic merge pipelines
