---
name: openclaw-agent-orchestrator
description: Create and repair durable OpenClaw agents, bindings, and runtime state. Use when the user wants real subagents, durable agent entries, or proof that orchestration actions actually changed live state. Prefer verified `openclaw agents add` flows over optimistic `sessions_spawn` narration.
metadata: {"openclaw":{"emoji":"🎛️"}}
---

# OpenClaw Agent Orchestrator

Use this skill when the user wants real subagents or when the runtime claims it started agents but `openclaw agents list` and `openclaw agents bindings` do not show them.

## Durable Agent Rule

For durable subagents in this deployment, use `openclaw agents add` and verify the result.

Do not use `sessions_spawn` with `mode="session"` for durable agent creation here. This runtime has already returned errors such as:

- `mode="session" requires thread=true`
- `thread=true is unavailable because no channel plugin registered subagent_spawning hooks`

Treat `sessions_spawn` as ephemeral-only unless the current runtime explicitly proves thread-bound session support.

## Workflow

1. Run `scripts/verify-runtime.sh` to see the current truth.
2. If the requested durable agent does not exist, run `scripts/create-agent.sh <agent-id> <name> <emoji> [theme]`.
3. If the user asked for routing, add bindings with `openclaw agents bind`.
4. Re-run `scripts/verify-runtime.sh`.
5. Report only what is present in verified runtime output.

## Guardrails

- Never say an agent was created until `openclaw agents list --json` shows it.
- Never claim bindings exist until `openclaw agents bindings --json` shows them.
- Do not use `crontab` in this environment. Use `openclaw cron ...` only if a schedule is actually needed.
- Do not say `GO`, `starting now`, or `spawned successfully` before a verified state change.

## Commands

Verify:

```bash
./scripts/verify-runtime.sh
```

Create one durable agent:

```bash
./scripts/create-agent.sh oracle "Oracle" "🔮" "qa"
```

Create one durable agent from a copied workspace and verify:

```bash
./scripts/create-agent.sh trinity "Trinity" "🥷" "ops"
./scripts/verify-runtime.sh
```
