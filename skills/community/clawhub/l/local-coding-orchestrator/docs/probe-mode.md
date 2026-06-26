# Probe mode

This document defines the lightweight worker probe mode.

## Goal

Separate repo/runtime feasibility checks from full implementation work.

## Why it exists

In constrained environments, a full worker brief may waste time on:
- loading workspace context the worker cannot access
- complex shell probing
- implementation planning before basic repo access is confirmed

## Probe mode rules

A probe worker should:
- verify repo path access
- inspect top-level structure only
- determine whether build/test can proceed
- report blockers clearly

A probe worker should not:
- load orchestrator workspace context files
- treat missing workspace context as a blocker
- start full implementation planning
- rely on complex multi-line shell constructions

## When to use

Use probe mode when:
- validating a new repo target
- testing a constrained environment
- checking whether the local runtime is viable before handing off a bigger task
