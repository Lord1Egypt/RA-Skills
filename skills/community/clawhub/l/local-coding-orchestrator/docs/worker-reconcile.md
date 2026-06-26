# Worker reconcile loop

This document defines the first reconcile step for background worker runs.

## Goal

Take a launched background worker and fold its runtime state back into the task record.

## What reconcile does

- reads the task record
- checks whether the recorded PID is still alive
- updates `lastPolledAt`
- extracts a short log summary
- if the process ended, writes completion metadata
- writes result and summary artifacts when possible

## Important limitation

Reconcile tells you what happened to the worker run and now also writes lightweight classification metadata.
It still does not decide that the task is done.

The supervisor must still decide whether:
- objective checks passed
- review is needed
- retry should be generated
- the task can transition to `completed`

## First heuristic

The initial reconcile step uses a lightweight text heuristic on logs to classify the worker run as `completed` or `failed`.
It also assigns an initial failure kind such as:
- `environment-missing`
- `repo-unavailable`
- `credential-missing`
- `environment-blocked`
- `generic-failure`

That heuristic should be replaced or tightened over time.
