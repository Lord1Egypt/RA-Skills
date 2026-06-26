---
name: laizy
description: Orchestrate repo-native, supervised software delivery with the Laizy CLI. Use when a user wants to bootstrap or continue a multi-step coding run with explicit planning, replanning, implementation, recovery, verification, and closeout artifacts, especially in repos using Claude Code, Codex, OpenClaw, or similar coding agents.
license: MIT
metadata: {"openclaw":{"emoji":"🪄","homepage":"https://github.com/XiaolongGao521/Laizy","requires":{"bins":["laizy"]},"install":[{"id":"node-github","kind":"node","package":"github:XiaolongGao521/Laizy","bins":["laizy"],"label":"Install Laizy CLI from GitHub (npm)"}]}}
---

# Laizy

Use Laizy as the control plane around existing coding agents, not as a replacement for them.

## Core workflow

1. Create or refresh a **local** milestone plan file for the target repo.
   - Use a local `IMPLEMENTATION_PLAN.md` by convention.
   - Keep it out of git unless the user explicitly wants it committed.
   - If the repo does not have actionable milestones yet, use the planner-needed bootstrap template in `{baseDir}/references/planner-bootstrap.md`.
2. Bootstrap the run once with `laizy start-run`.
3. Use `laizy supervisor-tick` as the source of truth for every later decision.
4. Read the emitted bundle and follow the bounded next action instead of improvising the next step in chat.

## Commands

Bootstrap a run:

```bash
laizy start-run \
  --goal "<user goal>" \
  --plan IMPLEMENTATION_PLAN.md \
  --out state/runs/<run-name>.json
```

Evaluate the next action:

```bash
laizy supervisor-tick \
  --snapshot state/runs/<run-name>.json \
  --out-dir state/runs/<run-name>.supervisor
```

## Decision map

Read `{baseDir}/references/decision-map.md` for the full artifact map. The short version is:

- `plan` / `replan`
  - Read the emitted `planner.request` document.
  - Spawn or steer a planner worker to author/repair the plan.
  - If the run was bootstrapped in `needs-plan` mode, re-run `start-run` after the planner lands the first actionable milestone queue.
- `continue`
  - Read the emitted implementer contract.
  - Execute exactly one bounded milestone.
- `recover`
  - Read the emitted recovery plan.
  - Resume safely without widening scope.
- `verify`
  - Run the emitted verification command.
  - Record the result before marking a milestone complete.
- `closeout`
  - Disable or pause the watchdog.
  - Stop the loop.

## Runtime-profile rules

Use the runtime profile emitted by Laizy when spawning planner, implementer, recovery, or verifier workers.

- Prefer the selected `model`, `thinking`, and `reasoningMode` when the platform allows them.
- If the exact model is rejected by account policy, fall back to an allowed model while preserving the same bounded contract and intended thinking level.
- In shared/group chat surfaces, keep reasoning visibility conservative by default.

## Repo hygiene

Treat generated run artifacts as local state:

- keep `state/runs/` out of git
- keep `state/verification/` out of git
- keep generated `.tgz` files out of git
- keep local maintainer plan files out of git unless the user explicitly wants them committed

## References

- Read `{baseDir}/references/decision-map.md` for emitted artifact names and what to do for each supervisor decision.
- Read `{baseDir}/references/planner-bootstrap.md` when you need a clean planner-needed starting point for a new multi-step run.
