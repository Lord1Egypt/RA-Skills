# Detailed Setup Matrix

## A. OpenClaw-only orchestration

### Shape
- main OpenClaw session orchestrates
- OpenClaw subagents do the work

### Strengths
- one tool universe
- one memory/runtime surface
- simple for short and medium tasks

### Weaknesses
- orchestration reliability depends more directly on gateway/session internals
- plugin/runtime hooks on the main session matter more
- not ideal for big coding swarms

### Verdict
Good for light orchestration, not the best default for 10+ heavy coding workers.

---

## B. OpenClaw control plane + ACP Claude Code workers

### Shape
- OpenClaw main = planning, state, checkpoints, reporting
- Claude Code ACP sessions = execution

### Strengths
- strong coding agent with persistent thread/session model
- less pressure on OpenClaw subagent path
- clean separation between control plane and execution plane

### Weaknesses
- requires better handoff discipline
- slightly more operational surface

### Verdict
**Best starting point.**

---

## C. OpenClaw control plane + ACP Codex workers

### Shape
- OpenClaw main = planning/control
- Codex ACP sessions = builders / patchers / testers

### Strengths
- efficient for repetitive code tasks
- good for broad patching and mechanical iteration
- useful as a cheaper parallel execution plane

### Weaknesses
- not my first choice for ambiguous architectural review
- may need stronger reviewer guardrails for subtle product/spec work

### Verdict
Great as a secondary execution engine, or for cost-sensitive parallel fix loops.

---

## D. Hybrid ACP team

### Shape
- OpenClaw main = orchestrator
- Claude Code ACP = architecture / nuanced builder / reviewer
- Codex ACP = fast builder / fixer / batch patcher

### Strengths
- best role specialization
- strongest for medium/large engineering efforts
- lets each runtime do what it is best at

### Weaknesses
- needs disciplined routing and file contracts
- easiest setup to get messy if handoffs are weak

### Verdict
Best long-term target once the simpler Claude Code-first version is working.

---

## E. External-first swarm

### Shape
- OpenClaw becomes almost only a coordinator / observer
- most heavy work happens in ACP/external coding sessions

### Strengths
- isolates heavy execution from OpenClaw runtime quirks
- can scale farther for coding-only swarms

### Weaknesses
- weakest integration with memory, messaging, and internal tools
- requires deliberate synchronization of state back into the shared file/state layer

### Verdict
Useful later, but not the best first refactor.

---

# Recommended target architecture

## Default
- **Control plane**: OpenClaw main
- **Default execution plane**: ACP Claude Code
- **Secondary execution plane**: ACP Codex when useful
- **State plane**: project/task files + `shared/` + `agent/orchestration/runs/`

## Routing rules

### Use OpenClaw-only when
- the task is short
- the task needs many first-class internal tools
- there are <= 2 workers and low code volume

### Use ACP Claude Code when
- the task is a real coding workstream
- the worker needs to stay persistent over time
- the repo context is large
- you want a builder or reviewer with strong coding depth

### Use ACP Codex when
- the task is patch-heavy or repetitive
- the changes are localized and testable
- you want a fast secondary worker for fix loops

### Use Hybrid ACP when
- there are multiple modules
- planning and execution deserve specialization
- you want builder/reviewer separation at runtime level

# Operational guardrails

1. Do not let the OpenClaw main session become a chatty execution worker.
2. Prefer persistent ACP sessions (`thread: true`, `mode: "session"`) for long coding work.
3. Use one worktree per builder stream when parallel edits are real.
4. Always materialize handoffs into files before launching workers.
5. Use OpenClaw for checkpoints and human-facing summaries, not for every edit.
