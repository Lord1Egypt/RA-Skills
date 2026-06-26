# Phase model

This document captures the emerging stage-based execution model of `local-coding-orchestrator`.

## Current phases

### 1. Probe
Purpose:
- validate repo access
- inspect minimal structure
- determine runtime feasibility

### 2. Implement
Purpose:
- make code changes
- run implementation-oriented checks when possible

### 3. Review
Purpose:
- inspect probe or implementation outcomes
- classify blockers and next-step risk
- recommend advance, block, or changes requested

### 4. Harden
Purpose:
- perform follow-up fixes, cleanup, or polish before declaring completion

## Why phases matter

Phase-based orchestration avoids asking a single worker to do everything at once.
It lets the supervisor choose lighter or heavier worker modes based on current evidence.
