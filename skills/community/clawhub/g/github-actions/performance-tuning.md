# Performance Tuning - GitHub Actions

Use this file when workflow minutes, queue time, or feedback speed are the bottleneck.

## First Levers

Start with the highest-yield optimizations:
- cancel superseded runs with `concurrency`
- use native setup-action caches before custom cache paths
- split slow optional work from required status checks
- avoid rebuilding in downstream jobs when artifacts can be reused

## Cache Strategy

Cache only stable, expensive-to-restore inputs.

Good cache candidates:
- package manager caches
- language toolchains
- browser binaries or dependency registries with stable versions

Bad cache candidates:
- generated artifacts that should move through explicit uploads
- mutable deploy state
- directories affected by secrets or timestamps

## Matrix Cost Control

Before adding a matrix, ask:
- does each cell prove a real compatibility promise?
- can the matrix be split into fast required cells and slower optional cells?
- should shards depend on historical test runtime instead of arbitrary counts?

If one cell is enough for pull requests, keep the full matrix for main or nightly runs.

## Path Filters and Workflow Split

Use path filters when repo layout is stable enough to trust them.
In monorepos:
- keep shared dependency or tooling paths in every relevant filter
- avoid overfitting filters so tightly that important validations stop running
- prefer reusable workflows plus small entry workflows per product area

## Runner Decisions

Use GitHub-hosted runners by default.
Switch only when there is a clear reason:
- macOS or Windows requirement
- custom hardware or network reach
- long warm caches that justify self-hosting

Self-hosting is an operations choice, not just a cost choice.

## Queue and Reliability Trade-Offs

The fastest workflow is not always the best workflow.

- shaving one minute is not worth losing reproducibility
- parallelism helps until logs become unreadable and failures hard to isolate
- retries are useful for flaky providers but can hide deterministic bugs if overused

Optimize for fast, trusted feedback instead of raw benchmark speed.
