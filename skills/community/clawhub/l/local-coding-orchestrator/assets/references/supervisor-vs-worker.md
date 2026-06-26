# Supervisor vs worker responsibilities

This reference clarifies the boundary between orchestration logic and local coding workers.

## Supervisor responsibilities

The supervisor is responsible for:
- accepting or structuring the task
- choosing the pipeline
- choosing worker roles and tools
- creating task records
- managing lifecycle transitions
- evaluating objective completion signals
- deciding whether review is required
- generating retry briefs
- deciding between mechanical retry and semantic retry
- summarizing status to the user
- deciding whether the task is completed, blocked, failed, or needs another pass

## Worker responsibilities

A worker is responsible for:
- reading the current brief
- editing code or producing a review artifact
- running requested local checks when possible
- writing output into the intended directory
- returning raw execution results or files

Workers are not responsible for:
- redefining task scope
- deciding final completion state
- suppressing failed objective checks
- overwriting supervisor decisions

## Boundary rule

Treat workers as specialized executors.
Treat the supervisor as the source of truth for task state.

## Why this matters

Without a clear boundary, orchestration collapses into prompt forwarding.
With a clear boundary, OpenClaw can:
- supervise multiple workers
- retry intelligently
- avoid false completion
- keep a reliable task history
