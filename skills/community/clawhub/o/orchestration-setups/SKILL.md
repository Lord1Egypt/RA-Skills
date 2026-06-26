---
name: claude-code-control-plane
description: "Hybrid orchestration skill where OpenClaw stays the control plane and ACP Claude Code is the default execution backend for coding work."
metadata: {"openclaw":{"emoji":"🧭"}}
---

# Claude Code Control Plane

Use this when the user wants multi-step coding orchestration without making the main OpenClaw session carry the execution load.

## Core idea

- **OpenClaw main session** = planner, router, state owner, human interface
- **ACP Claude Code sessions** = default builders/reviewers
- **ACP Codex sessions** = optional targeted fixer/batch workers
- **Files** = source of truth for handoffs and state

This skill is for **hybrid orchestration**, not pure OpenClaw swarms.

## When to use

Use this skill when:
- the task is primarily coding or engineering
- the work may span hours
- you may want several workers over time
- the main OpenClaw session should stay stable and lightweight
- session/tool reliability matters more than having every worker inside OpenClaw

Do not use this skill when:
- the task is a quick question
- the task is a tiny one-shot edit
- the work depends mostly on OpenClaw-native tools rather than coding runtime

## Default architecture

### Roles
- **Orchestrator**: OpenClaw main session
- **Builder**: ACP Claude Code session
- **Reviewer**: ACP Claude Code session or ACP Codex session
- **Fixer**: ACP Codex session when patches are narrow and repetitive

### State
Every workstream must have:
1. a task/spec file
2. a shared artifact path
3. a clear handoff packet written before spawn
4. a rolling worker summary file for context rollover

## Launch policy

### Default spawn
For a real coding worker, prefer:
- `sessions_spawn`
- `runtime: "acp"`
- explicit `agentId`
- `thread: true`
- `mode: "session"`

This gives a persistent coding worker instead of a fragile short-lived chat worker.

### Suggested defaults
- **Claude Code builder**: persistent ACP session bound to the thread/workstream
- **Claude Code reviewer**: separate persistent ACP session for clean review context
- **Codex fixer**: one-shot or persistent depending on volume

## Orchestration modes

### 1. Single builder
Use when one worker can do the task.

Pattern:
- OpenClaw defines task
- Claude Code builds
- OpenClaw reviews result and reports

### 2. Builder + reviewer
Use by default for non-trivial code changes.

Pattern:
- Claude Code builder session
- Claude Code or Codex reviewer session
- OpenClaw resolves disagreement and reports back

### 3. Project builder
Use when there is a real repo/worktree with multiple steps.

Pattern:
- planner/spec handoff
- builder session for implementation
- reviewer session for gaps
- fixer loop only on concrete deltas

### 4. Hybrid swarm
Use only when the work is large enough to justify multiple workers.

Pattern:
- Claude Code: architect / planner / nuanced reviewer
- Codex: mechanical builders / fixers
- OpenClaw: state machine + human checkpoints

## Guardrails

1. Do not keep complex run state only in session chat.
2. Do not spawn workers before writing the handoff file.
3. Do not let the orchestrator become the builder.
4. Use worktrees for parallel builders.
5. Prefer fewer persistent workers over many throwaway workers.
6. If OpenClaw runtime looks unhealthy, stop spawning and continue with ACP sessions already alive.
7. Every long-running worker should maintain a rolling summary file covering:
   - what it has done
   - what it is doing now
   - what it learned / what matters next
8. When a worker nears context pressure, compress to file first, then resume or replace the worker from that file instead of letting it drift into a weak soft-stop.

## Recommended file layout

```text
project-specs/
shared-specs/
shared-artifacts/
runs/<run-id>/
worker-state/
```

## Prompt template for ACP workers

```text
## TASK
<exact task>

## EXPECTED OUTPUT
<artifact paths + format>

## MUST DO
- read the listed files first
- write artifacts before claiming completion
- report only the concise delta

## MUST NOT
- do not overwrite unrelated files
- do not self-approve
- do not hide uncertainty

## CONTEXT
- repo/worktree:
- files to read first:
- artifact path:
```

## Recommended starting default

For now, the safest default is:
- OpenClaw main = orchestrator
- Claude Code ACP = primary builder
- Claude Code ACP or Codex ACP = reviewer
- file-native handoffs everywhere

That is the baseline setup this skill assumes.
