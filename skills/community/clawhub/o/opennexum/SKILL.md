---
name: opennexum
version: 2.1.4
description: Contract-driven multi-agent orchestration with ACP. Contract sync, webhook + dispatch-queue dual dispatch, cross-review, auto-retry, batch progress tracking.
requires:
  node: ">=20"
  tools: [pnpm, openclaw]
---

# OpenNexum

Contract-driven coding agent orchestration via OpenClaw ACP.

## When to use
- Coordinating multiple AI coding agents (Codex + Claude)
- Running generator/evaluator pairs with automatic retry and escalation
- Parallel task execution with independent ACP sessions
- Tracking task progress with OpenClaw notifications

## Architecture

### Dispatch (dual-path)
1. **Webhook (real-time)**: `nexum callback` → POST `/hooks/agent` → orchestrator wakes up immediately
2. **Dispatch Queue (fallback)**: `nexum callback` → writes `nexum/dispatch-queue.jsonl` → heartbeat processes within 10min

### Cross-review
- codex-gen → claude-eval, claude-gen → codex-eval

### Auto-routing
- `generator: auto` in Contract YAML → system selects agent by task type

### Batch progress
- `nexum status` shows current batch progress + overall progress

## Agent Naming: `<model>-<role>-<number>`
- codex-gen-01~03: backend/API code
- claude-gen-01~02: user-facing WebUI/docs
- codex-eval-01 / claude-eval-01: cross-review
- claude-plan-01: architecture (opus)

## Key CLI Commands

```bash
nexum init [--project <dir>] [--yes]
nexum sync [taskId] [--project <dir>]
nexum spawn <taskId> [--project <dir>]
nexum track <taskId> <sessionKey>
nexum callback <taskId> [--role evaluator] [--model gpt-5.4] [--input-tokens N] [--output-tokens N]
nexum eval <taskId>
nexum complete <taskId> <pass|fail|escalated>
nexum status [--project <dir>]
nexum archive [--project <dir>]
nexum health [--project <dir>]
nexum retry <taskId> --force
```

## Contract YAML

```yaml
id: TASK-001
name: "implement feature X"
batch: batch-1
agent:
  generator: codex-gen-01
  evaluator: claude-eval-01
scope:
  files:
    - src/feature.ts
deliverables:
  - path: src/feature.ts
    description: "..."
eval_strategy:
  type: review
  criteria:
    - id: C1
      desc: "..."
      weight: 2
max_iterations: 3
```

## Callback Protocol (injected into AGENTS.md via nexum init)

`nexum init` writes the callback protocol into `AGENTS.md` as the source of truth. If a project only has `CLAUDE.md`, Nexum will seed `AGENTS.md` from it and update `AGENTS.md` going forward.

After completing a task, run:
```bash
nexum callback <taskId> --project <projectDir> \
  --model gpt-5.4 \
  --input-tokens <n> \
  --output-tokens <n>
```

## Git Convention
- Push directly to `main`, revert if needed
- English Conventional Commits: `feat(scope): TASK-ID: description`
