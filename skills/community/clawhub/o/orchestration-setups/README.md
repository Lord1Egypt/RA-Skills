# Orchestrator a la oh-my-codex and gastown for Openclaw

Goal: avoid making the main OpenClaw session a heavy execution runtime while keeping it as the control plane.

## Package entrypoint

- `SKILL.md` is the root skill entrypoint for ClawHub / OpenClaw.
- `docs/` contains the design, runtime notes, reproduction guide, and test results.
- `packs/` contains reusable workflow/agent/template assets.
- `examples/` contains minimal session launch patterns.

## Recommendation

**Start here:**
- **OpenClaw main session** = planner, router, durable state, human interface
- **ACP Claude Code sessions** = default execution workers
- **ACP Codex sessions** = optional secondary builder / reviewer / fixer workers
- **Artifacts + handoffs** = file-native state under shared artifact directories and run-state directories

This keeps the fragile part small: the main session decides and tracks, but the real long coding work happens in external ACP workers.

## Why change the setup

The current issue is not that every worker gets Active Memory.
The issue is that the **main OpenClaw orchestrator session** can accumulate runtime overhead on user-triggered prompt build hooks, while it is also the place that calls `sessions_spawn`, `sessions_list`, and other orchestration tools.

So the safer design is:
- thin control plane in OpenClaw
- heavy execution in ACP workers
- minimal plugin dependence on the orchestrator session

## Setup matrix

| Setup | What it is | Pros | Cons | Use for |
|---|---|---|---|---|
| **A. OpenClaw-only** | Main session + OpenClaw subagents everywhere | Unified tools, simple mental model | More coupling to gateway/session internals | Short multi-step tasks |
| **B. OpenClaw + ACP Claude Code** | OpenClaw orchestrates, Claude Code executes | Best default for real coding projects, persistent sessions, less pressure on main lane | Slightly more moving parts | Main recommendation |
| **C. OpenClaw + ACP Codex** | Same as B but Codex workers | Strong code search/edit/test loops, good cost profile | Slightly less strong on ambiguous planning/review prose | Batch edits, parallel fixes |
| **D. Hybrid ACP** | Claude Code planners/reviewers + Codex builders | Strongest team pattern for medium/large repos | More orchestration discipline needed | Larger engineering work |
| **E. External-first swarm** | Very thin OpenClaw, most work done outside it | Maximum isolation from gateway quirks | Less unified state unless carefully documented | Big coding swarms, later phase |

## Available orchestration workflows

### `review-loop`
Classic builder → reviewer → fix loop.

Use it for:
- non-trivial code changes
- document or spec review
- any task where you want a clean quality gate before shipping

### `deep-research`
Parallel research fan-out followed by synthesis.

Use it for:
- literature scans
- competitive / technical landscape surveys
- collecting evidence from several parallel workers before one synthesis pass

### `project-builder`
Structured project build flow with a planner/builder/reviewer pattern and worktree-aware module splitting.

Use it for:
- multi-file engineering tasks
- greenfield feature scaffolding
- work that benefits from parallel builder streams with explicit reviewer feedback

### `batch-review`
One reviewer pattern over a set of items/artifacts.

Use it for:
- many related diffs
- content batches
- repeated checks over a list of outputs

### `watchdog`
Lightweight monitoring / stale-run detection pattern.

Use it for:
- surfacing stalled runs
- retry / escalation checks
- lightweight operational monitoring

## Validation status

Not all workflows are validated at the same depth yet.

| Workflow / backend | Validation level | Status |
|---|---|---|
| **OpenClaw subagent backend** | Real smoke test | ✅ validated |
| **Claude Code ACP backend** | Real smoke test | ✅ validated |
| **Codex ACP backend** | Real smoke test | ✅ validated |
| **`review-loop`** | Runtime smoke test executed successfully | ✅ validated at V1 runtime level |
| **`deep-research`** | Parallel handoff generation checked manually (`--count 3`) | 🟡 structure validated, not yet end-to-end on a full real case |
| **`project-builder`** | Module-targeted handoff generation checked manually (`--targets backend,frontend`) | 🟡 structure validated, not yet end-to-end on a full real case |
| **`batch-review`** | Present in pack, no dedicated smoke test yet | ⚪ not yet explicitly validated |
| **`watchdog`** | Present in pack, no dedicated smoke test yet | ⚪ not yet explicitly validated |

So the honest answer is:
- **no, they are not all validated equally yet**
- the **execution backends** are now validated
- `review-loop` is the most concretely validated workflow
- `deep-research` and `project-builder` are structurally validated but still deserve a real end-to-end run
- `batch-review` and `watchdog` are packaged but still lighter-confidence

## Final recommendation

### Phase 1, adopt now
**Setup B: OpenClaw + ACP Claude Code**

Pattern:
1. Keep OpenClaw as the control plane
2. Spawn Claude Code ACP sessions for actual implementation
3. Use one persistent thread/session per workstream
4. Store state in files, not in session memory
5. Keep the main session lightweight during orchestration

### Phase 2, when needed
**Setup D: Hybrid ACP**
- Claude Code for planning, architecture, nuanced review
- Codex for focused implementation, patching, repetitive batch work

## Control plane rules

1. **OpenClaw should not be the main execution engine** for long coding swarms.
2. **Every workstream gets a file-native state path**:
   - task/spec file
   - shared artifacts directory
   - run-state directory for handoffs, checkpoints, and reviews
3. **ACP workers own code changes**.
4. **OpenClaw owns routing, checkpoints, retries, and reporting**.
5. **Git worktrees per builder stream** when multiple workers touch code.

## Minimal operating model

- **Planner**: OpenClaw main or Claude Code ACP
- **Builder**: Claude Code ACP session
- **Reviewer**: Claude Code ACP session or Codex ACP session
- **Fixer**: Codex ACP session for targeted repair loops
- **Human checkpoint**: OpenClaw main session

## Suggested first implementation

- Root skill entrypoint: `SKILL.md`
- Handoff/state kept in a file-native orchestration runtime
- Claude Code ACP as the default worker backend
- Previous architecture material bundled directly under `docs/` and `packs/` so the historical design base stays attached to the new proposal

## Bundled previous work

This folder now includes the prior material we had already developed:
- V1 control-plane spec
- OMC/Gastown audit
- runtime docs (`README`, `SCHEMAS`, `COMMUNICATION`, `OPENCLAW_LAUNCHER`, `PROJECT_BUILDER_WORKTREE`)
- agent / workflow / template packs

See:
- `SKILL.md`
- `docs/setup-matrix.md`
- `docs/design/`
- `docs/runtime/`
- `docs/reproduction.md`
- `docs/test-results.md`
- `packs/`
- `examples/session-patterns.md`
