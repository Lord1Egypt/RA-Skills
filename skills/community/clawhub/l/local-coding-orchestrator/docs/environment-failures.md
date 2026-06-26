# Environment failure classification

This document defines the first environment-oriented failure classes for `local-coding-orchestrator`.

## Why this exists

A worker can fail even when the task itself was reasonable.
Those cases should not be treated the same as implementation failure.

## Initial classes

- `environment-missing`
  - read-only sandbox
  - non-writable workspace
  - missing local prerequisites

- `repo-unavailable`
  - repository path missing
  - checkout not present
  - expected project directory not found

- `credential-missing`
  - MCP login missing
  - API token missing
  - environment variable for auth missing

- `environment-blocked`
  - the worker explicitly reports blocked prerequisites

## Supervisor behavior

When one of these classes is detected, prefer:
- `nextAction = operator-intervention`
- `recommendedState = blocked`

rather than automatically generating a semantic retry.
