# Worker launch adapter

This document defines the first worker launch adapter for `local-coding-orchestrator`.

## Goal

Bridge pipeline presets to a concrete worker selection and a concrete worker brief.

## First-stage behavior

The first-stage adapter should:
1. load the task record
2. resolve the configured pipeline preset
3. choose a worker role
4. write a worker brief into `local-orchestrator/prompts/`
5. record the brief path into the task artifacts
6. return the intended launch command preview

## Why preview first

Directly attaching live worker execution is powerful but riskier.
Preview-first lets you verify:
- worker selection
- prompt structure
- role mapping
- artifact wiring

before you start large background runs.

## Current upgrade

The adapter now supports an initial synchronous execution mode and uses file-based prompt handoff.

In execution mode it can:
- call the actual tool wrapper
- pass prompt content by `TaskFile` instead of inline multi-line command arguments
- capture raw output into logs
- write result JSON and summary files
- update `workerRun` metadata in the task record

## Expected next step

After synchronous execution is stable, the adapter can:
- let the supervisor trigger worker launch automatically
- add background execution for long-running tasks
- attach richer parsing/cleaning of worker output
- feed execution results back into objective checks and review routing
