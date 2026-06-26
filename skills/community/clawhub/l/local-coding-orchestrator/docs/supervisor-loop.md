# Supervisor loop

This document describes the first supervisor loop for `local-coding-orchestrator`.

## Goal

Connect task records, done evaluation, and pipeline presets into a single supervisory decision point.

## Current loop

The initial supervisor loop should:
1. load the task record
2. inspect current lifecycle state
3. evaluate objective completion checks
4. resolve the configured pipeline preset
5. recommend the next orchestration action
6. recommend the next lifecycle state

## Important constraint

The initial loop is advisory.
It should recommend actions before it starts mutating task state or launching workers automatically.

This keeps the first version inspectable and safer to debug.

## Example actions

- `queue-task`
- `launch-worker`
- `continue-monitoring`
- `review-for-retry-or-block`
- `generate-retry-brief`
- `prepare-retry`
- `relaunch-worker`
- `transition-to-completed`
- `operator-intervention`
- `decide-requeue-or-cancel`

## Why advisory first

A bad supervisor that auto-mutates state can create confusing failures quickly.
An advisory supervisor gives you a tight feedback loop while preserving human control.

## Current upgrade

The supervisor loop now supports optional controlled actions:
- optionally write state transitions
- optionally trigger retry brief generation
- reconcile background worker state before making the next decision
- auto-recommend review or blocked states when worker outcomes already exist
- optionally auto-launch, auto-probe, and auto-block in safe cases

These actions are opt-in so the default mode stays inspectable.

## Expected next step

After this controlled mode is stable, upgrade it to:
- optionally launch the next worker for the chosen pipeline
- optionally attach worker outputs back into the task record
- optionally enforce queue and scheduler decisions
