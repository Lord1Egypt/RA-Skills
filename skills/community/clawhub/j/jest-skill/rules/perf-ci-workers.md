---
title: --runInBand or --maxWorkers for CI
impact: MEDIUM
description: Jest's default worker count can overwhelm CI containers with limited CPUs and memory. Use --runInBand for small suites or --maxWorkers for controlled parallelism.
tags: perf, ci, runInBand, maxWorkers, workers, memory, containers
---

# --runInBand or --maxWorkers for CI

## Problem

By default, Jest spawns one worker per CPU core. In CI environments (Docker containers, GitHub Actions, etc.), the container often reports the host machine's CPU count rather than the allocated cores. A 2-CPU container on a 64-core host spawns 64 workers, causing memory exhaustion, OOM kills, and flaky tests.

## Incorrect

```bash
# BUG: Default workers — CI container with 2 CPUs reports 64 cores from host
npx jest
# Spawns 64 workers → OOM kill → flaky CI
```

```bash
# BUG: --maxWorkers=100% is the default behavior — same problem
npx jest --maxWorkers=100%
```

## Correct

```bash
# Option 1: Run serially — best for small suites (< 100 tests)
npx jest --runInBand

# Option 2: Fixed worker count — predictable resource usage
npx jest --maxWorkers=2

# Option 3: Percentage of available CPUs — scales with container size
npx jest --maxWorkers=50%
```

```javascript
// jest.config.js — set defaults for CI
module.exports = {
  ...(process.env.CI && {
    maxWorkers: process.env.JEST_MAX_WORKERS || 2,
  }),
};
```

## Decision Table

| Suite size | CI resources | Recommendation |
|---|---|---|
| < 100 tests | Any | `--runInBand` (serial — avoids worker overhead) |
| 100–500 tests | 2 CPUs | `--maxWorkers=2` |
| 100–500 tests | 4+ CPUs | `--maxWorkers=50%` |
| 500+ tests | 4+ CPUs | `--maxWorkers=50%` + `--shard` |
| Any | Memory-constrained | `--runInBand` or `--maxWorkers=1` |

## Sharding for Large Suites

```bash
# Split tests across CI jobs (e.g., 4 parallel CI jobs)
# Job 1:
npx jest --shard=1/4
# Job 2:
npx jest --shard=2/4
# Job 3:
npx jest --shard=3/4
# Job 4:
npx jest --shard=4/4
```

## Why

- Each Jest worker is a separate Node.js process (~100–200MB memory).
- Worker spawning has fixed overhead — for small suites, `--runInBand` (single process) is faster than parallelism.
- `--shard` distributes tests across CI jobs at a higher level than `--maxWorkers`, which distributes within a single job.
- `--maxWorkers=50%` is a safe default that leaves CPU headroom for the operating system and other CI processes.
