---
name: osop-optimize
description: Analyze .osoplog execution history to optimize workflows — finds slow steps and parallelization opportunities
version: 1.2.0
emoji: "\u26A1"
homepage: https://osop.ai
argument-hint: <path-to-osop-file>
metadata:
  openclaw:
    requires:
      bins:
        - bash
      config:
        - ~/.osop/config.yaml
    install: []
    always: false
user-invocable: true
disable-model-invocation: false
---

# OSOP Workflow Optimizer

Improve a workflow based on its execution history.

## Target workflow

$ARGUMENTS

## What to do

1. **Read the .osop file** specified in the argument

2. **Find execution logs** — look for matching `.osoplog.yaml` files in `sessions/` or the same directory

3. **Aggregate stats** from all matching logs:
   - Per-node: average duration, failure rate, timeout rate, common errors
   - Overall: success rate, average total duration, run count

4. **Identify issues**:
   - **Slow steps**: nodes with avg_duration > 5s
   - **Failure hotspots**: nodes with failure_rate > 10%
   - **Bottlenecks**: nodes that are both slow AND unreliable
   - **Missing retries**: external call nodes (api, cli, agent, infra, mcp) without retry_policy
   - **Missing timeouts**: external call nodes without timeout_sec
   - **Parallelization**: sequential chains of 3+ independent nodes
   - **Missing error handling**: high-risk nodes without fallback/error edges

5. **Generate suggestions** and present as a table:
   ```
   | Type | Target Node | Description | Priority |
   |------|-------------|-------------|----------|
   | add_retry | fetch-data | 35% failure rate, add retry with backoff | HIGH |
   | parallelize | scan, test, lint | Independent steps, run in parallel | MEDIUM |
   ```

6. **If user approves**, apply changes to the .osop file

7. **Show diff** of changes before writing

## Self-optimization loop

This skill enables the feedback loop:
```
Execute → Log (.osoplog) → Analyze (this skill) → Improve (.osop) → Re-execute → Better results
```

Each iteration makes the workflow more resilient and efficient.
