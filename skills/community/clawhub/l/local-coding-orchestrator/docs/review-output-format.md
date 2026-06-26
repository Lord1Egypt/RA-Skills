# Review output format

This document defines the lightweight structured output expected from review-mode workers.

## Required headings

- `Review Decision:`
- `Risk Level:`
- `Blocker Type:`
- `Recommended Next Step:`
- `Rationale:`

## Allowed values

### Review Decision
- `approved-for-next-step`
- `blocked-by-environment`
- `changes-requested`
- `ready-for-hardening`

### Risk Level
- `low`
- `medium`
- `high`

### Blocker Type
- `none`
- `environment`
- `implementation`
- `mixed`

### Recommended Next Step
- `probe-again`
- `implement`
- `review`
- `harden`
- `operator-intervention`

## Why this exists

The supervisor should not rely only on free-form text when a lightweight structured decision can be requested.
This format is intentionally simple enough for local coding workers to follow without heavy parsing requirements.
