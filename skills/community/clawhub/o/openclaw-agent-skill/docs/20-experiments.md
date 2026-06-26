# Experiments & Design Docs

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 10

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/plans/pty-process-supervision -->

# PTY and Process Supervision Plan

## 1\. Problem and goal

We need one reliable lifecycle for long-running command execution across:

*   `exec` foreground runs
*   `exec` background runs
*   `process` follow up actions (`poll`, `log`, `send-keys`, `paste`, `submit`, `kill`, `remove`)
*   CLI agent runner subprocesses

The goal is not just to support PTY. The goal is predictable ownership, cancellation, timeout, and cleanup with no unsafe process matching heuristics.

## 2\. Scope and boundaries

*   Keep implementation internal in `src/process/supervisor`.
*   Do not create a new package for this.
*   Keep current behavior compatibility where practical.
*   Do not broaden scope to terminal replay or tmux style session persistence.

## 3\. Implemented in this branch

### Supervisor baseline already present

*   Supervisor module is in place under `src/process/supervisor/*`.
*   Exec runtime and CLI runner are already routed through supervisor spawn and wait.
*   Registry finalization is idempotent.

### This pass completed

1.  Explicit PTY command contract

*   `SpawnInput` is now a discriminated union in `src/process/supervisor/types.ts`.
*   PTY runs require `ptyCommand` instead of reusing generic `argv`.
*   Supervisor no longer rebuilds PTY command strings from argv joins in `src/process/supervisor/supervisor.ts`.
*   Exec runtime now passes `ptyCommand` directly in `src/agents/bash-tools.exec-runtime.ts`.

2.  Process layer type decoupling

*   Supervisor types no longer import `SessionStdin` from agents.
*   Process local stdin contract lives in `src/process/supervisor/types.ts` (`ManagedRunStdin`).
*   Adapters now depend only on process level types:
    *   `src/process/supervisor/adapters/child.ts`
    *   `src/process/supervisor/adapters/pty.ts`

3.  Process tool lifecycle ownership improvement

*   `src/agents/bash-tools.process.ts` now requests cancellation through supervisor first.
*   `process kill/remove` now use process-tree fallback termination when supervisor lookup misses.
*   `remove` keeps deterministic remove behavior by dropping running session entries immediately after termination is requested.

4.  Single source watchdog defaults

*   Added shared defaults in `src/agents/cli-watchdog-defaults.ts`.
*   `src/agents/cli-backends.ts` consumes the shared defaults.
*   `src/agents/cli-runner/reliability.ts` consumes the same shared defaults.

5.  Dead helper cleanup

*   Removed unused `killSession` helper path from `src/agents/bash-tools.shared.ts`.

6.  Direct supervisor path tests added

*   Added `src/agents/bash-tools.process.supervisor.test.ts` to cover kill and remove routing through supervisor cancellation.

7.  Reliability gap fixes completed

*   `src/agents/bash-tools.process.ts` now falls back to real OS-level process termination when supervisor lookup misses.
*   `src/process/supervisor/adapters/child.ts` now uses process-tree termination semantics for default cancel/timeout kill paths.
*   Added shared process-tree utility in `src/process/kill-tree.ts`.

8.  PTY contract edge-case coverage added

*   Added `src/process/supervisor/supervisor.pty-command.test.ts` for verbatim PTY command forwarding and empty-command rejection.
*   Added `src/process/supervisor/adapters/child.test.ts` for process-tree kill behavior in child adapter cancellation.

## 4\. Remaining gaps and decisions

### Reliability status

The two required reliability gaps for this pass are now closed:

*   `process kill/remove` now has a real OS termination fallback when supervisor lookup misses.
*   child cancel/timeout now uses process-tree kill semantics for default kill path.
*   Regression tests were added for both behaviors.

### Durability and startup reconciliation

Restart behavior is now explicitly defined as in-memory lifecycle only.

*   `reconcileOrphans()` remains a no-op in `src/process/supervisor/supervisor.ts` by design.
*   Active runs are not recovered after process restart.
*   This boundary is intentional for this implementation pass to avoid partial persistence risks.

### Maintainability follow-ups

1.  `runExecProcess` in `src/agents/bash-tools.exec-runtime.ts` still handles multiple responsibilities and can be split into focused helpers in a follow-up.

## 5\. Implementation plan

The implementation pass for required reliability and contract items is complete. Completed:

*   `process kill/remove` fallback real termination
*   process-tree cancellation for child adapter default kill path
*   regression tests for fallback kill and child adapter kill path
*   PTY command edge-case tests under explicit `ptyCommand`
*   explicit in-memory restart boundary with `reconcileOrphans()` no-op by design

Optional follow-up:

*   split `runExecProcess` into focused helpers with no behavior drift

## 6\. File map

### Process supervisor

*   `src/process/supervisor/types.ts` updated with discriminated spawn input and process local stdin contract.
*   `src/process/supervisor/supervisor.ts` updated to use explicit `ptyCommand`.
*   `src/process/supervisor/adapters/child.ts` and `src/process/supervisor/adapters/pty.ts` decoupled from agent types.
*   `src/process/supervisor/registry.ts` idempotent finalize unchanged and retained.

### Exec and process integration

*   `src/agents/bash-tools.exec-runtime.ts` updated to pass PTY command explicitly and keep fallback path.
*   `src/agents/bash-tools.process.ts` updated to cancel via supervisor with real process-tree fallback termination.
*   `src/agents/bash-tools.shared.ts` removed direct kill helper path.

### CLI reliability

*   `src/agents/cli-watchdog-defaults.ts` added as shared baseline.
*   `src/agents/cli-backends.ts` and `src/agents/cli-runner/reliability.ts` now consume same defaults.

## 7\. Validation run in this pass

Unit tests:

*   `pnpm vitest src/process/supervisor/registry.test.ts`
*   `pnpm vitest src/process/supervisor/supervisor.test.ts`
*   `pnpm vitest src/process/supervisor/supervisor.pty-command.test.ts`
*   `pnpm vitest src/process/supervisor/adapters/child.test.ts`
*   `pnpm vitest src/agents/cli-backends.test.ts`
*   `pnpm vitest src/agents/bash-tools.exec.pty-cleanup.test.ts`
*   `pnpm vitest src/agents/bash-tools.process.poll-timeout.test.ts`
*   `pnpm vitest src/agents/bash-tools.process.supervisor.test.ts`
*   `pnpm vitest src/process/exec.test.ts`

E2E targets:

*   `pnpm vitest src/agents/cli-runner.test.ts`
*   `pnpm vitest run src/agents/bash-tools.exec.pty-fallback.test.ts src/agents/bash-tools.exec.background-abort.test.ts src/agents/bash-tools.process.send-keys.test.ts`

Typecheck note:

*   Use `pnpm build` (and `pnpm check` for full lint/docs gate) in this repo. Older notes that mention `pnpm tsgo` are obsolete.

## 8\. Operational guarantees preserved

*   Exec env hardening behavior is unchanged.
*   Approval and allowlist flow is unchanged.
*   Output sanitization and output caps are unchanged.
*   PTY adapter still guarantees wait settlement on forced kill and listener disposal.

## 9\. Definition of done

1.  Supervisor is lifecycle owner for managed runs.
2.  PTY spawn uses explicit command contract with no argv reconstruction.
3.  Process layer has no type dependency on agent layer for supervisor stdin contracts.
4.  Watchdog defaults are single source.
5.  Targeted unit and e2e tests remain green.
6.  Restart durability boundary is explicitly documented or fully implemented.

## 10\. Summary

The branch now has a coherent and safer supervision shape:

*   explicit PTY contract
*   cleaner process layering
*   supervisor driven cancellation path for process operations
*   real fallback termination when supervisor lookup misses
*   process-tree cancellation for child-run default kill paths
*   unified watchdog defaults
*   explicit in-memory restart boundary (no orphan reconciliation across restart in this pass)

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/proposals/model-config -->

# Model Config Exploration - OpenClaw

This document captures **ideas** for future model configuration. It is not a shipping spec. For current behavior, see:

*   [Models](https://docs.openclaw.ai/concepts/models)
*   [Model failover](https://docs.openclaw.ai/concepts/model-failover)
*   [OAuth + profiles](https://docs.openclaw.ai/concepts/oauth)

## Motivation

Operators want:

*   Multiple auth profiles per provider (personal vs work).
*   Simple `/model` selection with predictable fallbacks.
*   Clear separation between text models and image-capable models.

## Possible direction (high level)

*   Keep model selection simple: `provider/model` with optional aliases.
*   Let providers have multiple auth profiles, with an explicit order.
*   Use a global fallback list so all sessions fail over consistently.
*   Only override image routing when explicitly configured.

## Open questions

*   Should profile rotation be per-provider or per-model?
*   How should the UI surface profile selection for a session?
*   What is the safest migration path from legacy config keys?

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/research/memory -->

# Workspace Memory Research - OpenClaw

## Workspace Memory v2 (offline): research notes

Target: Clawd-style workspace (`agents.defaults.workspace`, default `~/.openclaw/workspace`) where “memory” is stored as one Markdown file per day (`memory/YYYY-MM-DD.md`) plus a small set of stable files (e.g. `memory.md`, `SOUL.md`). This doc proposes an **offline-first** memory architecture that keeps Markdown as the canonical, reviewable source of truth, but adds **structured recall** (search, entity summaries, confidence updates) via a derived index.

## Why change?

The current setup (one file per day) is excellent for:

*   “append-only” journaling
*   human editing
*   git-backed durability + auditability
*   low-friction capture (“just write it down”)

It’s weak for:

*   high-recall retrieval (“what did we decide about X?”, “last time we tried Y?”)
*   entity-centric answers (“tell me about Alice / The Castle / warelay”) without rereading many files
*   opinion/preference stability (and evidence when it changes)
*   time constraints (“what was true during Nov 2025?”) and conflict resolution

## Design goals

*   **Offline**: works without network; can run on laptop/Castle; no cloud dependency.
*   **Explainable**: retrieved items should be attributable (file + location) and separable from inference.
*   **Low ceremony**: daily logging stays Markdown, no heavy schema work.
*   **Incremental**: v1 is useful with FTS only; semantic/vector and graphs are optional upgrades.
*   **Agent-friendly**: makes “recall within token budgets” easy (return small bundles of facts).

## North star model (Hindsight × Letta)

Two pieces to blend:

1.  **Letta/MemGPT-style control loop**

*   keep a small “core” always in context (persona + key user facts)
*   everything else is out-of-context and retrieved via tools
*   memory writes are explicit tool calls (append/replace/insert), persisted, then re-injected next turn

2.  **Hindsight-style memory substrate**

*   separate what’s observed vs what’s believed vs what’s summarized
*   support retain/recall/reflect
*   confidence-bearing opinions that can evolve with evidence
*   entity-aware retrieval + temporal queries (even without full knowledge graphs)

## Proposed architecture (Markdown source-of-truth + derived index)

### Canonical store (git-friendly)

Keep `~/.openclaw/workspace` as canonical human-readable memory. Suggested workspace layout:

```
~/.openclaw/workspace/
  memory.md                    # small: durable facts + preferences (core-ish)
  memory/
    YYYY-MM-DD.md              # daily log (append; narrative)
  bank/                        # “typed” memory pages (stable, reviewable)
    world.md                   # objective facts about the world
    experience.md              # what the agent did (first-person)
    opinions.md                # subjective prefs/judgments + confidence + evidence pointers
    entities/
      Peter.md
      The-Castle.md
      warelay.md
      ...
```

Notes:

*   **Daily log stays daily log**. No need to turn it into JSON.
*   The `bank/` files are **curated**, produced by reflection jobs, and can still be edited by hand.
*   `memory.md` remains “small + core-ish”: the things you want Clawd to see every session.

### Derived store (machine recall)

Add a derived index under the workspace (not necessarily git tracked):

```
~/.openclaw/workspace/.memory/index.sqlite
```

Back it with:

*   SQLite schema for facts + entity links + opinion metadata
*   SQLite **FTS5** for lexical recall (fast, tiny, offline)
*   optional embeddings table for semantic recall (still offline)

The index is always **rebuildable from Markdown**.

## Retain / Recall / Reflect (operational loop)

### Retain: normalize daily logs into “facts”

Hindsight’s key insight that matters here: store **narrative, self-contained facts**, not tiny snippets. Practical rule for `memory/YYYY-MM-DD.md`:

*   at end of day (or during), add a `## Retain` section with 2–5 bullets that are:
    *   narrative (cross-turn context preserved)
    *   self-contained (standalone makes sense later)
    *   tagged with type + entity mentions

Example:

```
## Retain
- W @Peter: Currently in Marrakech (Nov 27–Dec 1, 2025) for Andy’s birthday.
- B @warelay: I fixed the Baileys WS crash by wrapping connection.update handlers in try/catch (see memory/2025-11-27.md).
- O(c=0.95) @Peter: Prefers concise replies (&lt;1500 chars) on WhatsApp; long content goes into files.
```

Minimal parsing:

*   Type prefix: `W` (world), `B` (experience/biographical), `O` (opinion), `S` (observation/summary; usually generated)
*   Entities: `@Peter`, `@warelay`, etc (slugs map to `bank/entities/*.md`)
*   Opinion confidence: `O(c=0.0..1.0)` optional

If you don’t want authors to think about it: the reflect job can infer these bullets from the rest of the log, but having an explicit `## Retain` section is the easiest “quality lever”.

### Recall: queries over the derived index

Recall should support:

*   **lexical**: “find exact terms / names / commands” (FTS5)
*   **entity**: “tell me about X” (entity pages + entity-linked facts)
*   **temporal**: “what happened around Nov 27” / “since last week”
*   **opinion**: “what does Peter prefer?” (with confidence + evidence)

Return format should be agent-friendly and cite sources:

*   `kind` (`world|experience|opinion|observation`)
*   `timestamp` (source day, or extracted time range if present)
*   `entities` (`["Peter","warelay"]`)
*   `content` (the narrative fact)
*   `source` (`memory/2025-11-27.md#L12` etc)

### Reflect: produce stable pages + update beliefs

Reflection is a scheduled job (daily or heartbeat `ultrathink`) that:

*   updates `bank/entities/*.md` from recent facts (entity summaries)
*   updates `bank/opinions.md` confidence based on reinforcement/contradiction
*   optionally proposes edits to `memory.md` (“core-ish” durable facts)

Opinion evolution (simple, explainable):

*   each opinion has:
    *   statement
    *   confidence `c ∈ [0,1]`
    *   last\_updated
    *   evidence links (supporting + contradicting fact IDs)
*   when new facts arrive:
    *   find candidate opinions by entity overlap + similarity (FTS first, embeddings later)
    *   update confidence by small deltas; big jumps require strong contradiction + repeated evidence

## CLI integration: standalone vs deep integration

Recommendation: **deep integration in OpenClaw**, but keep a separable core library.

### Why integrate into OpenClaw?

*   OpenClaw already knows:
    *   the workspace path (`agents.defaults.workspace`)
    *   the session model + heartbeats
    *   logging + troubleshooting patterns
*   You want the agent itself to call the tools:
    *   `openclaw memory recall "…" --k 25 --since 30d`
    *   `openclaw memory reflect --since 7d`

### Why still split a library?

*   keep memory logic testable without gateway/runtime
*   reuse from other contexts (local scripts, future desktop app, etc.)

Shape: The memory tooling is intended to be a small CLI + library layer, but this is exploratory only.

## “S-Collide” / SuCo: when to use it (research)

If “S-Collide” refers to **SuCo (Subspace Collision)**: it’s an ANN retrieval approach that targets strong recall/latency tradeoffs by using learned/structured collisions in subspaces (paper: arXiv 2411.14754, 2024). Pragmatic take for `~/.openclaw/workspace`:

*   **don’t start** with SuCo.
*   start with SQLite FTS + (optional) simple embeddings; you’ll get most UX wins immediately.
*   consider SuCo/HNSW/ScaNN-class solutions only once:
    *   corpus is big (tens/hundreds of thousands of chunks)
    *   brute-force embedding search becomes too slow
    *   recall quality is meaningfully bottlenecked by lexical search

Offline-friendly alternatives (in increasing complexity):

*   SQLite FTS5 + metadata filters (zero ML)
*   Embeddings + brute force (works surprisingly far if chunk count is low)
*   HNSW index (common, robust; needs a library binding)
*   SuCo (research-grade; attractive if there’s a solid implementation you can embed)

Open question:

*   what’s the **best** offline embedding model for “personal assistant memory” on your machines (laptop + desktop)?
    *   if you already have Ollama: embed with a local model; otherwise ship a small embedding model in the toolchain.

## Smallest useful pilot

If you want a minimal, still-useful version:

*   Add `bank/` entity pages and a `## Retain` section in daily logs.
*   Use SQLite FTS for recall with citations (path + line numbers).
*   Add embeddings only if recall quality or scale demands it.

## References

*   Letta / MemGPT concepts: “core memory blocks” + “archival memory” + tool-driven self-editing memory.
*   Hindsight Technical Report: “retain / recall / reflect”, four-network memory, narrative fact extraction, opinion confidence evolution.
*   SuCo: arXiv 2411.14754 (2024): “Subspace Collision” approximate nearest neighbor retrieval.

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/plans/session-binding-channel-agnostic -->

# Session Binding Channel Agnostic Plan

## Overview

This document defines the long term channel agnostic session binding model and the concrete scope for the next implementation iteration. Goal:

*   make subagent bound session routing a core capability
*   keep channel specific behavior in adapters
*   avoid regressions in normal Discord behavior

## Why this exists

Current behavior mixes:

*   completion content policy
*   destination routing policy
*   Discord specific details

This caused edge cases such as:

*   duplicate main and thread delivery under concurrent runs
*   stale token usage on reused binding managers
*   missing activity accounting for webhook sends

## Iteration 1 scope

This iteration is intentionally limited.

### 1\. Add channel agnostic core interfaces

Add core types and service interfaces for bindings and routing. Proposed core types:

```
export type BindingTargetKind = "subagent" | "session";
export type BindingStatus = "active" | "ending" | "ended";

export type ConversationRef = {
  channel: string;
  accountId: string;
  conversationId: string;
  parentConversationId?: string;
};

export type SessionBindingRecord = {
  bindingId: string;
  targetSessionKey: string;
  targetKind: BindingTargetKind;
  conversation: ConversationRef;
  status: BindingStatus;
  boundAt: number;
  expiresAt?: number;
  metadata?: Record<string, unknown>;
};
```

Core service contract:

```
export interface SessionBindingService {
  bind(input: {
    targetSessionKey: string;
    targetKind: BindingTargetKind;
    conversation: ConversationRef;
    metadata?: Record<string, unknown>;
    ttlMs?: number;
  }): Promise<SessionBindingRecord>;

  listBySession(targetSessionKey: string): SessionBindingRecord[];
  resolveByConversation(ref: ConversationRef): SessionBindingRecord | null;
  touch(bindingId: string, at?: number): void;
  unbind(input: {
    bindingId?: string;
    targetSessionKey?: string;
    reason: string;
  }): Promise<SessionBindingRecord[]>;
}
```

### 2\. Add one core delivery router for subagent completions

Add a single destination resolution path for completion events. Router contract:

```
export interface BoundDeliveryRouter {
  resolveDestination(input: {
    eventKind: "task_completion";
    targetSessionKey: string;
    requester?: ConversationRef;
    failClosed: boolean;
  }): {
    binding: SessionBindingRecord | null;
    mode: "bound" | "fallback";
    reason: string;
  };
}
```

For this iteration:

*   only `task_completion` is routed through this new path
*   existing paths for other event kinds remain as-is

### 3\. Keep Discord as adapter

Discord remains the first adapter implementation. Adapter responsibilities:

*   create/reuse thread conversations
*   send bound messages via webhook or channel send
*   validate thread state (archived/deleted)
*   map adapter metadata (webhook identity, thread ids)

### 4\. Fix currently known correctness issues

Required in this iteration:

*   refresh token usage when reusing existing thread binding manager
*   record outbound activity for webhook based Discord sends
*   stop implicit main channel fallback when a bound thread destination is selected for session mode completion

### 5\. Preserve current runtime safety defaults

No behavior change for users with thread bound spawn disabled. Defaults stay:

*   `channels.discord.threadBindings.spawnSubagentSessions = false`

Result:

*   normal Discord users stay on current behavior
*   new core path affects only bound session completion routing where enabled

## Not in iteration 1

Explicitly deferred:

*   ACP binding targets (`targetKind: "acp"`)
*   new channel adapters beyond Discord
*   global replacement of all delivery paths (`spawn_ack`, future `subagent_message`)
*   protocol level changes
*   store migration/versioning redesign for all binding persistence

Notes on ACP:

*   interface design keeps room for ACP
*   ACP implementation is not started in this iteration

## Routing invariants

These invariants are mandatory for iteration 1.

*   destination selection and content generation are separate steps
*   if session mode completion resolves to an active bound destination, delivery must target that destination
*   no hidden reroute from bound destination to main channel
*   fallback behavior must be explicit and observable

## Compatibility and rollout

Compatibility target:

*   no regression for users with thread bound spawning off
*   no change to non-Discord channels in this iteration

Rollout:

1.  Land interfaces and router behind current feature gates.
2.  Route Discord completion mode bound deliveries through router.
3.  Keep legacy path for non-bound flows.
4.  Verify with targeted tests and canary runtime logs.

## Tests required in iteration 1

Unit and integration coverage required:

*   manager token rotation uses latest token after manager reuse
*   webhook sends update channel activity timestamps
*   two active bound sessions in same requester channel do not duplicate to main channel
*   completion for bound session mode run resolves to thread destination only
*   disabled spawn flag keeps legacy behavior unchanged

## Proposed implementation files

Core:

*   `src/infra/outbound/session-binding-service.ts` (new)
*   `src/infra/outbound/bound-delivery-router.ts` (new)
*   `src/agents/subagent-announce.ts` (completion destination resolution integration)

Discord adapter and runtime:

*   `src/discord/monitor/thread-bindings.manager.ts`
*   `src/discord/monitor/reply-delivery.ts`
*   `src/discord/send.outbound.ts`

Tests:

*   `src/discord/monitor/provider*.test.ts`
*   `src/discord/monitor/reply-delivery.test.ts`
*   `src/agents/subagent-announce.format.test.ts`

## Done criteria for iteration 1

*   core interfaces exist and are wired for completion routing
*   correctness fixes above are merged with tests
*   no main and thread duplicate completion delivery in session mode bound runs
*   no behavior change for disabled bound spawn deployments
*   ACP remains explicitly deferred

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/plans/acp-thread-bound-agents -->

# ACP Thread Bound Agents - OpenClaw

## Overview

This plan defines how OpenClaw should support ACP coding agents in thread-capable channels (Discord first) with production-level lifecycle and recovery. Related document:

*   [Unified Runtime Streaming Refactor Plan](https://docs.openclaw.ai/experiments/plans/acp-unified-streaming-refactor)

Target user experience:

*   a user spawns or focuses an ACP session into a thread
*   user messages in that thread route to the bound ACP session
*   agent output streams back to the same thread persona
*   session can be persistent or one shot with explicit cleanup controls

## Decision summary

Long term recommendation is a hybrid architecture:

*   OpenClaw core owns ACP control plane concerns
    *   session identity and metadata
    *   thread binding and routing decisions
    *   delivery invariants and duplicate suppression
    *   lifecycle cleanup and recovery semantics
*   ACP runtime backend is pluggable
    *   first backend is an acpx-backed plugin service
    *   runtime does ACP transport, queueing, cancel, reconnect

OpenClaw should not reimplement ACP transport internals in core. OpenClaw should not rely on a pure plugin-only interception path for routing.

## North-star architecture (holy grail)

Treat ACP as a first-class control plane in OpenClaw, with pluggable runtime adapters. Non-negotiable invariants:

*   every ACP thread binding references a valid ACP session record
*   every ACP session has explicit lifecycle state (`creating`, `idle`, `running`, `cancelling`, `closed`, `error`)
*   every ACP run has explicit run state (`queued`, `running`, `completed`, `failed`, `cancelled`)
*   spawn, bind, and initial enqueue are atomic
*   command retries are idempotent (no duplicate runs or duplicate Discord outputs)
*   bound-thread channel output is a projection of ACP run events, never ad-hoc side effects

Long-term ownership model:

*   `AcpSessionManager` is the single ACP writer and orchestrator
*   manager lives in gateway process first; can be moved to a dedicated sidecar later behind the same interface
*   per ACP session key, manager owns one in-memory actor (serialized command execution)
*   adapters (`acpx`, future backends) are transport/runtime implementations only

Long-term persistence model:

*   move ACP control-plane state to a dedicated SQLite store (WAL mode) under OpenClaw state dir
*   keep `SessionEntry.acp` as compatibility projection during migration, not source-of-truth
*   store ACP events append-only to support replay, crash recovery, and deterministic delivery

### Delivery strategy (bridge to holy-grail)

*   short-term bridge
    *   keep current thread binding mechanics and existing ACP config surface
    *   fix metadata-gap bugs and route ACP turns through a single core ACP branch
    *   add idempotency keys and fail-closed routing checks immediately
*   long-term cutover
    *   move ACP source-of-truth to control-plane DB + actors
    *   make bound-thread delivery purely event-projection based
    *   remove legacy fallback behavior that depends on opportunistic session-entry metadata

## Why not pure plugin only

Current plugin hooks are not sufficient for end to end ACP session routing without core changes.

*   inbound routing from thread binding resolves to a session key in core dispatch first
*   message hooks are fire-and-forget and cannot short-circuit the main reply path
*   plugin commands are good for control operations but not for replacing core per-turn dispatch flow

Result:

*   ACP runtime can be pluginized
*   ACP routing branch must exist in core

## Existing foundation to reuse

Already implemented and should remain canonical:

*   thread binding target supports `subagent` and `acp`
*   inbound thread routing override resolves by binding before normal dispatch
*   outbound thread identity via webhook in reply delivery
*   `/focus` and `/unfocus` flow with ACP target compatibility
*   persistent binding store with restore on startup
*   unbind lifecycle on archive, delete, unfocus, reset, and delete

This plan extends that foundation rather than replacing it.

## Architecture

### Boundary model

Core (must be in OpenClaw core):

*   ACP session-mode dispatch branch in the reply pipeline
*   delivery arbitration to avoid parent plus thread duplication
*   ACP control-plane persistence (with `SessionEntry.acp` compatibility projection during migration)
*   lifecycle unbind and runtime detach semantics tied to session reset/delete

Plugin backend (acpx implementation):

*   ACP runtime worker supervision
*   acpx process invocation and event parsing
*   ACP command handlers (`/acp ...`) and operator UX
*   backend-specific config defaults and diagnostics

### Runtime ownership model

*   one gateway process owns ACP orchestration state
*   ACP execution runs in supervised child processes via acpx backend
*   process strategy is long lived per active ACP session key, not per message

This avoids startup cost on every prompt and keeps cancel and reconnect semantics reliable.

### Core runtime contract

Add a core ACP runtime contract so routing code does not depend on CLI details and can switch backends without changing dispatch logic:

```
export type AcpRuntimePromptMode = "prompt" | "steer";

export type AcpRuntimeHandle = {
  sessionKey: string;
  backend: string;
  runtimeSessionName: string;
};

export type AcpRuntimeEvent =
  | { type: "text_delta"; stream: "output" | "thought"; text: string }
  | { type: "tool_call"; name: string; argumentsText: string }
  | { type: "done"; usage?: Record<string, number> }
  | { type: "error"; code: string; message: string; retryable?: boolean };

export interface AcpRuntime {
  ensureSession(input: {
    sessionKey: string;
    agent: string;
    mode: "persistent" | "oneshot";
    cwd?: string;
    env?: Record<string, string>;
    idempotencyKey: string;
  }): Promise<AcpRuntimeHandle>;

  submit(input: {
    handle: AcpRuntimeHandle;
    text: string;
    mode: AcpRuntimePromptMode;
    idempotencyKey: string;
  }): Promise<{ runtimeRunId: string }>;

  stream(input: {
    handle: AcpRuntimeHandle;
    runtimeRunId: string;
    onEvent: (event: AcpRuntimeEvent) => Promise<void> | void;
    signal?: AbortSignal;
  }): Promise<void>;

  cancel(input: {
    handle: AcpRuntimeHandle;
    runtimeRunId?: string;
    reason?: string;
    idempotencyKey: string;
  }): Promise<void>;

  close(input: { handle: AcpRuntimeHandle; reason: string; idempotencyKey: string }): Promise<void>;

  health?(): Promise<{ ok: boolean; details?: string }>;
}
```

Implementation detail:

*   first backend: `AcpxRuntime` shipped as a plugin service
*   core resolves runtime via registry and fails with explicit operator error when no ACP runtime backend is available

### Control-plane data model and persistence

Long-term source-of-truth is a dedicated ACP SQLite database (WAL mode), for transactional updates and crash-safe recovery:

*   `acp_sessions`
    *   `session_key` (pk), `backend`, `agent`, `mode`, `cwd`, `state`, `created_at`, `updated_at`, `last_error`
*   `acp_runs`
    *   `run_id` (pk), `session_key` (fk), `state`, `requester_message_id`, `idempotency_key`, `started_at`, `ended_at`, `error_code`, `error_message`
*   `acp_bindings`
    *   `binding_key` (pk), `thread_id`, `channel_id`, `account_id`, `session_key` (fk), `expires_at`, `bound_at`
*   `acp_events`
    *   `event_id` (pk), `run_id` (fk), `seq`, `kind`, `payload_json`, `created_at`
*   `acp_delivery_checkpoint`
    *   `run_id` (pk/fk), `last_event_seq`, `last_discord_message_id`, `updated_at`
*   `acp_idempotency`
    *   `scope`, `idempotency_key`, `result_json`, `created_at`, unique `(scope, idempotency_key)`

```
export type AcpSessionMeta = {
  backend: string;
  agent: string;
  runtimeSessionName: string;
  mode: "persistent" | "oneshot";
  cwd?: string;
  state: "idle" | "running" | "error";
  lastActivityAt: number;
  lastError?: string;
};
```

Storage rules:

*   keep `SessionEntry.acp` as a compatibility projection during migration
*   process ids and sockets stay in memory only
*   durable lifecycle and run status live in ACP DB, not generic session JSON
*   if runtime owner dies, gateway rehydrates from ACP DB and resumes from checkpoints

### Routing and delivery

Inbound:

*   keep current thread binding lookup as first routing step
*   if bound target is ACP session, route to ACP runtime branch instead of `getReplyFromConfig`
*   explicit `/acp steer` command uses `mode: "steer"`

Outbound:

*   ACP event stream is normalized to OpenClaw reply chunks
*   delivery target is resolved through existing bound destination path
*   when a bound thread is active for that session turn, parent channel completion is suppressed

Streaming policy:

*   stream partial output with coalescing window
*   configurable min interval and max chunk bytes to stay under Discord rate limits
*   final message always emitted on completion or failure

### State machines and transaction boundaries

Session state machine:

*   `creating -> idle -> running -> idle`
*   `running -> cancelling -> idle | error`
*   `idle -> closed`
*   `error -> idle | closed`

Run state machine:

*   `queued -> running -> completed`
*   `running -> failed | cancelled`
*   `queued -> cancelled`

Required transaction boundaries:

*   spawn transaction
    *   create ACP session row
    *   create/update ACP thread binding row
    *   enqueue initial run row
*   close transaction
    *   mark session closed
    *   delete/expire binding rows
    *   write final close event
*   cancel transaction
    *   mark target run cancelling/cancelled with idempotency key

No partial success is allowed across these boundaries.

### Per-session actor model

`AcpSessionManager` runs one actor per ACP session key:

*   actor mailbox serializes `submit`, `cancel`, `close`, and `stream` side effects
*   actor owns runtime handle hydration and runtime adapter process lifecycle for that session
*   actor writes run events in-order (`seq`) before any Discord delivery
*   actor updates delivery checkpoints after successful outbound send

This removes cross-turn races and prevents duplicate or out-of-order thread output.

### Idempotency and delivery projection

All external ACP actions must carry idempotency keys:

*   spawn idempotency key
*   prompt/steer idempotency key
*   cancel idempotency key
*   close idempotency key

Delivery rules:

*   Discord messages are derived from `acp_events` plus `acp_delivery_checkpoint`
*   retries resume from checkpoint without re-sending already delivered chunks
*   final reply emission is exactly-once per run from projection logic

### Recovery and self-healing

On gateway start:

*   load non-terminal ACP sessions (`creating`, `idle`, `running`, `cancelling`, `error`)
*   recreate actors lazily on first inbound event or eagerly under configured cap
*   reconcile any `running` runs missing heartbeats and mark `failed` or recover via adapter

On inbound Discord thread message:

*   if binding exists but ACP session is missing, fail closed with explicit stale-binding message
*   optionally auto-unbind stale binding after operator-safe validation
*   never silently route stale ACP bindings to normal LLM path

### Lifecycle and safety

Supported operations:

*   cancel current run: `/acp cancel`
*   unbind thread: `/unfocus`
*   close ACP session: `/acp close`
*   auto close idle sessions by effective TTL

TTL policy:

*   effective TTL is minimum of
    *   global/session TTL
    *   Discord thread binding TTL
    *   ACP runtime owner TTL

Safety controls:

*   allowlist ACP agents by name
*   restrict workspace roots for ACP sessions
*   env allowlist passthrough
*   max concurrent ACP sessions per account and globally
*   bounded restart backoff for runtime crashes

## Config surface

Core keys:

*   `acp.enabled`
*   `acp.dispatch.enabled` (independent ACP routing kill switch)
*   `acp.backend` (default `acpx`)
*   `acp.defaultAgent`
*   `acp.allowedAgents[]`
*   `acp.maxConcurrentSessions`
*   `acp.stream.coalesceIdleMs`
*   `acp.stream.maxChunkChars`
*   `acp.runtime.ttlMinutes`
*   `acp.controlPlane.store` (`sqlite` default)
*   `acp.controlPlane.storePath`
*   `acp.controlPlane.recovery.eagerActors`
*   `acp.controlPlane.recovery.reconcileRunningAfterMs`
*   `acp.controlPlane.checkpoint.flushEveryEvents`
*   `acp.controlPlane.checkpoint.flushEveryMs`
*   `acp.idempotency.ttlHours`
*   `channels.discord.threadBindings.spawnAcpSessions`

Plugin/backend keys (acpx plugin section):

*   backend command/path overrides
*   backend env allowlist
*   backend per-agent presets
*   backend startup/stop timeouts
*   backend max inflight runs per session

## Implementation specification

### Control-plane modules (new)

Add dedicated ACP control-plane modules in core:

*   `src/acp/control-plane/manager.ts`
    *   owns ACP actors, lifecycle transitions, command serialization
*   `src/acp/control-plane/store.ts`
    *   SQLite schema management, transactions, query helpers
*   `src/acp/control-plane/events.ts`
    *   typed ACP event definitions and serialization
*   `src/acp/control-plane/checkpoint.ts`
    *   durable delivery checkpoints and replay cursors
*   `src/acp/control-plane/idempotency.ts`
    *   idempotency key reservation and response replay
*   `src/acp/control-plane/recovery.ts`
    *   boot-time reconciliation and actor rehydrate plan

Compatibility bridge modules:

*   `src/acp/runtime/session-meta.ts`
    *   remains temporarily for projection into `SessionEntry.acp`
    *   must stop being source-of-truth after migration cutover

### Required invariants (must enforce in code)

*   ACP session creation and thread bind are atomic (single transaction)
*   there is at most one active run per ACP session actor at a time
*   event `seq` is strictly increasing per run
*   delivery checkpoint never advances past last committed event
*   idempotency replay returns previous success payload for duplicate command keys
*   stale/missing ACP metadata cannot route into normal non-ACP reply path

### Core touchpoints

Core files to change:

*   `src/auto-reply/reply/dispatch-from-config.ts`
    *   ACP branch calls `AcpSessionManager.submit` and event-projection delivery
    *   remove direct ACP fallback that bypasses control-plane invariants
*   `src/auto-reply/reply/inbound-context.ts` (or nearest normalized context boundary)
    *   expose normalized routing keys and idempotency seeds for ACP control plane
*   `src/config/sessions/types.ts`
    *   keep `SessionEntry.acp` as projection-only compatibility field
*   `src/gateway/server-methods/sessions.ts`
    *   reset/delete/archive must call ACP manager close/unbind transaction path
*   `src/infra/outbound/bound-delivery-router.ts`
    *   enforce fail-closed destination behavior for ACP bound session turns
*   `src/discord/monitor/thread-bindings.ts`
    *   add ACP stale-binding validation helpers wired to control-plane lookups
*   `src/auto-reply/reply/commands-acp.ts`
    *   route spawn/cancel/close/steer through ACP manager APIs
*   `src/agents/acp-spawn.ts`
    *   stop ad-hoc metadata writes; call ACP manager spawn transaction
*   `src/plugin-sdk/**` and plugin runtime bridge
    *   expose ACP backend registration and health semantics cleanly

Core files explicitly not replaced:

*   `src/discord/monitor/message-handler.preflight.ts`
    *   keep thread binding override behavior as the canonical session-key resolver

### ACP runtime registry API

Add a core registry module:

*   `src/acp/runtime/registry.ts`

Required API:

```
export type AcpRuntimeBackend = {
  id: string;
  runtime: AcpRuntime;
  healthy?: () => boolean;
};

export function registerAcpRuntimeBackend(backend: AcpRuntimeBackend): void;
export function unregisterAcpRuntimeBackend(id: string): void;
export function getAcpRuntimeBackend(id?: string): AcpRuntimeBackend | null;
export function requireAcpRuntimeBackend(id?: string): AcpRuntimeBackend;
```

Behavior:

*   `requireAcpRuntimeBackend` throws a typed ACP backend missing error when unavailable
*   plugin service registers backend on `start` and unregisters on `stop`
*   runtime lookups are read-only and process-local

### acpx runtime plugin contract (implementation detail)

For the first production backend (`extensions/acpx`), OpenClaw and acpx are connected with a strict command contract:

*   backend id: `acpx`
*   plugin service id: `acpx-runtime`
*   runtime handle encoding: `runtimeSessionName = acpx:v1:<base64url(json)>`
*   encoded payload fields:
    *   `name` (acpx named session; uses OpenClaw `sessionKey`)
    *   `agent` (acpx agent command)
    *   `cwd` (session workspace root)
    *   `mode` (`persistent | oneshot`)

Command mapping:

*   ensure session:
    *   `acpx --format json --json-strict --cwd <cwd> <agent> sessions ensure --name <name>`
*   prompt turn:
    *   `acpx --format json --json-strict --cwd <cwd> <agent> prompt --session <name> --file -`
*   cancel:
    *   `acpx --format json --json-strict --cwd <cwd> <agent> cancel --session <name>`
*   close:
    *   `acpx --format json --json-strict --cwd <cwd> <agent> sessions close <name>`

Streaming:

*   OpenClaw consumes ndjson events from `acpx --format json --json-strict`
*   `text` => `text_delta/output`
*   `thought` => `text_delta/thought`
*   `tool_call` => `tool_call`
*   `done` => `done`
*   `error` => `error`

### Session schema patch

Patch `SessionEntry` in `src/config/sessions/types.ts`:

```
type SessionAcpMeta = {
  backend: string;
  agent: string;
  runtimeSessionName: string;
  mode: "persistent" | "oneshot";
  cwd?: string;
  state: "idle" | "running" | "error";
  lastActivityAt: number;
  lastError?: string;
};
```

Persisted field:

*   `SessionEntry.acp?: SessionAcpMeta`

Migration rules:

*   phase A: dual-write (`acp` projection + ACP SQLite source-of-truth)
*   phase B: read-primary from ACP SQLite, fallback-read from legacy `SessionEntry.acp`
*   phase C: migration command backfills missing ACP rows from valid legacy entries
*   phase D: remove fallback-read and keep projection optional for UX only
*   legacy fields (`cliSessionIds`, `claudeCliSessionId`) remain untouched

### Error contract

Add stable ACP error codes and user-facing messages:

*   `ACP_BACKEND_MISSING`
    *   message: `ACP runtime backend is not configured. Install and enable the acpx runtime plugin.`
*   `ACP_BACKEND_UNAVAILABLE`
    *   message: `ACP runtime backend is currently unavailable. Try again in a moment.`
*   `ACP_SESSION_INIT_FAILED`
    *   message: `Could not initialize ACP session runtime.`
*   `ACP_TURN_FAILED`
    *   message: `ACP turn failed before completion.`

Rules:

*   return actionable user-safe message in-thread
*   log detailed backend/system error only in runtime logs
*   never silently fall back to normal LLM path when ACP routing was explicitly selected

### Duplicate delivery arbitration

Single routing rule for ACP bound turns:

*   if an active thread binding exists for the target ACP session and requester context, deliver only to that bound thread
*   do not also send to parent channel for the same turn
*   if bound destination selection is ambiguous, fail closed with explicit error (no implicit parent fallback)
*   if no active binding exists, use normal session destination behavior

### Observability and operational readiness

Required metrics:

*   ACP spawn success/failure count by backend and error code
*   ACP run latency percentiles (queue wait, runtime turn time, delivery projection time)
*   ACP actor restart count and restart reason
*   stale-binding detection count
*   idempotency replay hit rate
*   Discord delivery retry and rate-limit counters

Required logs:

*   structured logs keyed by `sessionKey`, `runId`, `backend`, `threadId`, `idempotencyKey`
*   explicit state transition logs for session and run state machines
*   adapter command logs with redaction-safe arguments and exit summary

Required diagnostics:

*   `/acp sessions` includes state, active run, last error, and binding status
*   `/acp doctor` (or equivalent) validates backend registration, store health, and stale bindings

### Config precedence and effective values

ACP enablement precedence:

*   account override: `channels.discord.accounts.<id>.threadBindings.spawnAcpSessions`
*   channel override: `channels.discord.threadBindings.spawnAcpSessions`
*   global ACP gate: `acp.enabled`
*   dispatch gate: `acp.dispatch.enabled`
*   backend availability: registered backend for `acp.backend`

Auto-enable behavior:

*   when ACP is configured (`acp.enabled=true`, `acp.dispatch.enabled=true`, or `acp.backend=acpx`), plugin auto-enable marks `plugins.entries.acpx.enabled=true` unless denylisted or explicitly disabled

TTL effective value:

*   `min(session ttl, discord thread binding ttl, acp runtime ttl)`

### Test map

Unit tests:

*   `src/acp/runtime/registry.test.ts` (new)
*   `src/auto-reply/reply/dispatch-from-config.acp.test.ts` (new)
*   `src/infra/outbound/bound-delivery-router.test.ts` (extend ACP fail-closed cases)
*   `src/config/sessions/types.test.ts` or nearest session-store tests (ACP metadata persistence)

Integration tests:

*   `src/discord/monitor/reply-delivery.test.ts` (bound ACP delivery target behavior)
*   `src/discord/monitor/message-handler.preflight*.test.ts` (bound ACP session-key routing continuity)
*   acpx plugin runtime tests in backend package (service register/start/stop + event normalization)

Gateway e2e tests:

*   `src/gateway/server.sessions.gateway-server-sessions-a.e2e.test.ts` (extend ACP reset/delete lifecycle coverage)
*   ACP thread turn roundtrip e2e for spawn, message, stream, cancel, unfocus, restart recovery

### Rollout guard

Add independent ACP dispatch kill switch:

*   `acp.dispatch.enabled` default `false` for first release
*   when disabled:
    *   ACP spawn/focus control commands may still bind sessions
    *   ACP dispatch path does not activate
    *   user receives explicit message that ACP dispatch is disabled by policy
*   after canary validation, default can be flipped to `true` in a later release

## Command and UX plan

### New commands

*   `/acp spawn <agent-id> [--mode persistent|oneshot] [--thread auto|here|off]`
*   `/acp cancel [session]`
*   `/acp steer <instruction>`
*   `/acp close [session]`
*   `/acp sessions`

### Existing command compatibility

*   `/focus <sessionKey>` continues to support ACP targets
*   `/unfocus` keeps current semantics
*   `/session idle` and `/session max-age` replace the old TTL override

## Phased rollout

### Phase 0 ADR and schema freeze

*   ship ADR for ACP control-plane ownership and adapter boundaries
*   freeze DB schema (`acp_sessions`, `acp_runs`, `acp_bindings`, `acp_events`, `acp_delivery_checkpoint`, `acp_idempotency`)
*   define stable ACP error codes, event contract, and state-transition guards

### Phase 1 Control-plane foundation in core

*   implement `AcpSessionManager` and per-session actor runtime
*   implement ACP SQLite store and transaction helpers
*   implement idempotency store and replay helpers
*   implement event append + delivery checkpoint modules
*   wire spawn/cancel/close APIs to manager with transactional guarantees

### Phase 2 Core routing and lifecycle integration

*   route thread-bound ACP turns from dispatch pipeline into ACP manager
*   enforce fail-closed routing when ACP binding/session invariants fail
*   integrate reset/delete/archive/unfocus lifecycle with ACP close/unbind transactions
*   add stale-binding detection and optional auto-unbind policy

### Phase 3 acpx backend adapter/plugin

*   implement `acpx` adapter against runtime contract (`ensureSession`, `submit`, `stream`, `cancel`, `close`)
*   add backend health checks and startup/teardown registration
*   normalize acpx ndjson events into ACP runtime events
*   enforce backend timeouts, process supervision, and restart/backoff policy

### Phase 4 Delivery projection and channel UX (Discord first)

*   implement event-driven channel projection with checkpoint resume (Discord first)
*   coalesce streaming chunks with rate-limit aware flush policy
*   guarantee exactly-once final completion message per run
*   ship `/acp spawn`, `/acp cancel`, `/acp steer`, `/acp close`, `/acp sessions`

### Phase 5 Migration and cutover

*   introduce dual-write to `SessionEntry.acp` projection plus ACP SQLite source-of-truth
*   add migration utility for legacy ACP metadata rows
*   flip read path to ACP SQLite primary
*   remove legacy fallback routing that depends on missing `SessionEntry.acp`

### Phase 6 Hardening, SLOs, and scale limits

*   enforce concurrency limits (global/account/session), queue policies, and timeout budgets
*   add full telemetry, dashboards, and alert thresholds
*   chaos-test crash recovery and duplicate-delivery suppression
*   publish runbook for backend outage, DB corruption, and stale-binding remediation

### Full implementation checklist

*   core control-plane modules and tests
*   DB migrations and rollback plan
*   ACP manager API integration across dispatch and commands
*   adapter registration interface in plugin runtime bridge
*   acpx adapter implementation and tests
*   thread-capable channel delivery projection logic with checkpoint replay (Discord first)
*   lifecycle hooks for reset/delete/archive/unfocus
*   stale-binding detector and operator-facing diagnostics
*   config validation and precedence tests for all new ACP keys
*   operational docs and troubleshooting runbook

## Test plan

Unit tests:

*   ACP DB transaction boundaries (spawn/bind/enqueue atomicity, cancel, close)
*   ACP state-machine transition guards for sessions and runs
*   idempotency reservation/replay semantics across all ACP commands
*   per-session actor serialization and queue ordering
*   acpx event parser and chunk coalescer
*   runtime supervisor restart and backoff policy
*   config precedence and effective TTL calculation
*   core ACP routing branch selection and fail-closed behavior when backend/session is invalid

Integration tests:

*   fake ACP adapter process for deterministic streaming and cancel behavior
*   ACP manager + dispatch integration with transactional persistence
*   thread-bound inbound routing to ACP session key
*   thread-bound outbound delivery suppresses parent channel duplication
*   checkpoint replay recovers after delivery failure and resumes from last event
*   plugin service registration and teardown of ACP runtime backend

Gateway e2e tests:

*   spawn ACP with thread, exchange multi-turn prompts, unfocus
*   gateway restart with persisted ACP DB and bindings, then continue same session
*   concurrent ACP sessions in multiple threads have no cross-talk
*   duplicate command retries (same idempotency key) do not create duplicate runs or replies
*   stale-binding scenario yields explicit error and optional auto-clean behavior

## Risks and mitigations

*   Duplicate deliveries during transition
    *   Mitigation: single destination resolver and idempotent event checkpoint
*   Runtime process churn under load
    *   Mitigation: long lived per session owners + concurrency caps + backoff
*   Plugin absent or misconfigured
    *   Mitigation: explicit operator-facing error and fail-closed ACP routing (no implicit fallback to normal session path)
*   Config confusion between subagent and ACP gates
    *   Mitigation: explicit ACP keys and command feedback that includes effective policy source
*   Control-plane store corruption or migration bugs
    *   Mitigation: WAL mode, backup/restore hooks, migration smoke tests, and read-only fallback diagnostics
*   Actor deadlocks or mailbox starvation
    *   Mitigation: watchdog timers, actor health probes, and bounded mailbox depth with rejection telemetry

## Acceptance checklist

*   ACP session spawn can create or bind a thread in a supported channel adapter (currently Discord)
*   all thread messages route to bound ACP session only
*   ACP outputs appear in the same thread identity with streaming or batches
*   no duplicate output in parent channel for bound turns
*   spawn+bind+initial enqueue are atomic in persistent store
*   ACP command retries are idempotent and do not duplicate runs or outputs
*   cancel, close, unfocus, archive, reset, and delete perform deterministic cleanup
*   crash restart preserves mapping and resumes multi turn continuity
*   concurrent thread bound ACP sessions work independently
*   ACP backend missing state produces clear actionable error
*   stale bindings are detected and surfaced explicitly (with optional safe auto-clean)
*   control-plane metrics and diagnostics are available for operators
*   new unit, integration, and e2e coverage passes

## Addendum: targeted refactors for current implementation (status)

These are non-blocking follow-ups to keep the ACP path maintainable after the current feature set lands.

### 1) Centralize ACP dispatch policy evaluation (completed)

*   implemented via shared ACP policy helpers in `src/acp/policy.ts`
*   dispatch, ACP command lifecycle handlers, and ACP spawn path now consume shared policy logic

### 2) Split ACP command handler by subcommand domain (completed)

*   `src/auto-reply/reply/commands-acp.ts` is now a thin router
*   subcommand behavior is split into:
    *   `src/auto-reply/reply/commands-acp/lifecycle.ts`
    *   `src/auto-reply/reply/commands-acp/runtime-options.ts`
    *   `src/auto-reply/reply/commands-acp/diagnostics.ts`
    *   shared helpers in `src/auto-reply/reply/commands-acp/shared.ts`

### 3) Split ACP session manager by responsibility (completed)

*   manager is split into:
    *   `src/acp/control-plane/manager.ts` (public facade + singleton)
    *   `src/acp/control-plane/manager.core.ts` (manager implementation)
    *   `src/acp/control-plane/manager.types.ts` (manager types/deps)
    *   `src/acp/control-plane/manager.utils.ts` (normalization + helper functions)

### 4) Optional acpx runtime adapter cleanup

*   `extensions/acpx/src/runtime.ts` can be split into:
*   process execution/supervision
*   ndjson event parsing/normalization
*   runtime API surface (`submit`, `cancel`, `close`, etc.)
*   improves testability and makes backend behavior easier to audit

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/plans/acp-unified-streaming-refactor -->

# Unified Runtime Streaming Refactor Plan

## Objective

Deliver one shared streaming pipeline for `main`, `subagent`, and `acp` so all runtimes get identical coalescing, chunking, delivery ordering, and crash recovery behavior.

## Why this exists

*   Current behavior is split across multiple runtime-specific shaping paths.
*   Formatting/coalescing bugs can be fixed in one path but remain in others.
*   Delivery consistency, duplicate suppression, and recovery semantics are harder to reason about.

## Target architecture

Single pipeline, runtime-specific adapters:

1.  Runtime adapters emit canonical events only.
2.  Shared stream assembler coalesces and finalizes text/tool/status events.
3.  Shared channel projector applies channel-specific chunking/formatting once.
4.  Shared delivery ledger enforces idempotent send/replay semantics.
5.  Outbound channel adapter executes sends and records delivery checkpoints.

Canonical event contract:

*   `turn_started`
*   `text_delta`
*   `block_final`
*   `tool_started`
*   `tool_finished`
*   `status`
*   `turn_completed`
*   `turn_failed`
*   `turn_cancelled`

## Workstreams

### 1) Canonical streaming contract

*   Define strict event schema + validation in core.
*   Add adapter contract tests to guarantee each runtime emits compatible events.
*   Reject malformed runtime events early and surface structured diagnostics.

### 2) Shared stream processor

*   Replace runtime-specific coalescer/projector logic with one processor.
*   Processor owns text delta buffering, idle flush, max-chunk splitting, and completion flush.
*   Move ACP/main/subagent config resolution into one helper to prevent drift.

### 3) Shared channel projection

*   Keep channel adapters dumb: accept finalized blocks and send.
*   Move Discord-specific chunking quirks to channel projector only.
*   Keep pipeline channel-agnostic before projection.

### 4) Delivery ledger + replay

*   Add per-turn/per-chunk delivery IDs.
*   Record checkpoints before and after physical send.
*   On restart, replay pending chunks idempotently and avoid duplicates.

### 5) Migration and cutover

*   Phase 1: shadow mode (new pipeline computes output but old path sends; compare).
*   Phase 2: runtime-by-runtime cutover (`acp`, then `subagent`, then `main` or reverse by risk).
*   Phase 3: delete legacy runtime-specific streaming code.

## Non-goals

*   No changes to ACP policy/permissions model in this refactor.
*   No channel-specific feature expansion outside projection compatibility fixes.
*   No transport/backend redesign (acpx plugin contract remains as-is unless needed for event parity).

## Risks and mitigations

*   Risk: behavioral regressions in existing main/subagent paths. Mitigation: shadow mode diffing + adapter contract tests + channel e2e tests.
*   Risk: duplicate sends during crash recovery. Mitigation: durable delivery IDs + idempotent replay in delivery adapter.
*   Risk: runtime adapters diverge again. Mitigation: required shared contract test suite for all adapters.

## Acceptance criteria

*   All runtimes pass shared streaming contract tests.
*   Discord ACP/main/subagent produce equivalent spacing/chunking behavior for tiny deltas.
*   Crash/restart replay sends no duplicate chunk for the same delivery ID.
*   Legacy ACP projector/coalescer path is removed.
*   Streaming config resolution is shared and runtime-independent.

---

<!-- SOURCE: https://docs.openclaw.ai/design/kilo-gateway-integration -->

# Kilo gateway integration - OpenClaw

## Kilo Gateway Provider Integration Design

## Overview

This document outlines the design for integrating “Kilo Gateway” as a first-class provider in OpenClaw, modeled after the existing OpenRouter implementation. Kilo Gateway uses an OpenAI-compatible completions API with a different base URL.

## Design Decisions

### 1\. Provider Naming

**Recommendation: `kilocode`** Rationale:

*   Matches the user config example provided (`kilocode` provider key)
*   Consistent with existing provider naming patterns (e.g., `openrouter`, `opencode`, `moonshot`)
*   Short and memorable
*   Avoids confusion with generic “kilo” or “gateway” terms

Alternative considered: `kilo-gateway` - rejected because hyphenated names are less common in the codebase and `kilocode` is more concise.

### 2\. Default Model Reference

**Recommendation: `kilocode/anthropic/claude-opus-4.6`** Rationale:

*   Based on user config example
*   Claude Opus 4.5 is a capable default model
*   Explicit model selection avoids reliance on auto-routing

### 3\. Base URL Configuration

**Recommendation: Hardcoded default with config override**

*   **Default Base URL:** `https://api.kilo.ai/api/gateway/`
*   **Configurable:** Yes, via `models.providers.kilocode.baseUrl`

This matches the pattern used by other providers like Moonshot, Venice, and Synthetic.

### 4\. Model Scanning

**Recommendation: No dedicated model scanning endpoint initially** Rationale:

*   Kilo Gateway proxies to OpenRouter, so models are dynamic
*   Users can manually configure models in their config
*   If Kilo Gateway exposes a `/models` endpoint in the future, scanning can be added

### 5\. Special Handling

**Recommendation: Inherit OpenRouter behavior for Anthropic models** Since Kilo Gateway proxies to OpenRouter, the same special handling should apply:

*   Cache TTL eligibility for `anthropic/*` models
*   Extra params (cacheControlTtl) for `anthropic/*` models
*   Transcript policy follows OpenRouter patterns

## Files to Modify

### Core Credential Management

#### 1\. `src/commands/onboard-auth.credentials.ts`

Add:

```
export const KILOCODE_DEFAULT_MODEL_REF = "kilocode/anthropic/claude-opus-4.6";

export async function setKilocodeApiKey(key: string, agentDir?: string) {
  upsertAuthProfile({
    profileId: "kilocode:default",
    credential: {
      type: "api_key",
      provider: "kilocode",
      key,
    },
    agentDir: resolveAuthAgentDir(agentDir),
  });
}
```

#### 2\. `src/agents/model-auth.ts`

Add to `envMap` in `resolveEnvApiKey()`:

```
const envMap: Record<string, string> = {
  // ... existing entries
  kilocode: "KILOCODE_API_KEY",
};
```

#### 3\. `src/config/io.ts`

Add to `SHELL_ENV_EXPECTED_KEYS`:

```
const SHELL_ENV_EXPECTED_KEYS = [
  // ... existing entries
  "KILOCODE_API_KEY",
];
```

### Config Application

#### 4\. `src/commands/onboard-auth.config-core.ts`

Add new functions:

```
export const KILOCODE_BASE_URL = "https://api.kilo.ai/api/gateway/";

export function applyKilocodeProviderConfig(cfg: OpenClawConfig): OpenClawConfig {
  const models = { ...cfg.agents?.defaults?.models };
  models[KILOCODE_DEFAULT_MODEL_REF] = {
    ...models[KILOCODE_DEFAULT_MODEL_REF],
    alias: models[KILOCODE_DEFAULT_MODEL_REF]?.alias ?? "Kilo Gateway",
  };

  const providers = { ...cfg.models?.providers };
  const existingProvider = providers.kilocode;
  const { apiKey: existingApiKey, ...existingProviderRest } = (existingProvider ?? {}) as Record<
    string,
    unknown
  > as { apiKey?: string };
  const resolvedApiKey = typeof existingApiKey === "string" ? existingApiKey : undefined;
  const normalizedApiKey = resolvedApiKey?.trim();

  providers.kilocode = {
    ...existingProviderRest,
    baseUrl: KILOCODE_BASE_URL,
    api: "openai-completions",
    ...(normalizedApiKey ? { apiKey: normalizedApiKey } : {}),
  };

  return {
    ...cfg,
    agents: {
      ...cfg.agents,
      defaults: {
        ...cfg.agents?.defaults,
        models,
      },
    },
    models: {
      mode: cfg.models?.mode ?? "merge",
      providers,
    },
  };
}

export function applyKilocodeConfig(cfg: OpenClawConfig): OpenClawConfig {
  const next = applyKilocodeProviderConfig(cfg);
  const existingModel = next.agents?.defaults?.model;
  return {
    ...next,
    agents: {
      ...next.agents,
      defaults: {
        ...next.agents?.defaults,
        model: {
          ...(existingModel && "fallbacks" in (existingModel as Record<string, unknown>)
            ? {
                fallbacks: (existingModel as { fallbacks?: string[] }).fallbacks,
              }
            : undefined),
          primary: KILOCODE_DEFAULT_MODEL_REF,
        },
      },
    },
  };
}
```

### Auth Choice System

#### 5\. `src/commands/onboard-types.ts`

Add to `AuthChoice` type:

```
export type AuthChoice =
  // ... existing choices
  "kilocode-api-key";
// ...
```

Add to `OnboardOptions`:

```
export type OnboardOptions = {
  // ... existing options
  kilocodeApiKey?: string;
  // ...
};
```

#### 6\. `src/commands/auth-choice-options.ts`

Add to `AuthChoiceGroupId`:

```
export type AuthChoiceGroupId =
  // ... existing groups
  "kilocode";
// ...
```

Add to `AUTH_CHOICE_GROUP_DEFS`:

```
{
  value: "kilocode",
  label: "Kilo Gateway",
  hint: "API key (OpenRouter-compatible)",
  choices: ["kilocode-api-key"],
},
```

Add to `buildAuthChoiceOptions()`:

```
options.push({
  value: "kilocode-api-key",
  label: "Kilo Gateway API key",
  hint: "OpenRouter-compatible gateway",
});
```

#### 7\. `src/commands/auth-choice.preferred-provider.ts`

Add mapping:

```
const PREFERRED_PROVIDER_BY_AUTH_CHOICE: Partial<Record<AuthChoice, string>> = {
  // ... existing mappings
  "kilocode-api-key": "kilocode",
};
```

### Auth Choice Application

#### 8\. `src/commands/auth-choice.apply.api-providers.ts`

Add import:

```
import {
  // ... existing imports
  applyKilocodeConfig,
  applyKilocodeProviderConfig,
  KILOCODE_DEFAULT_MODEL_REF,
  setKilocodeApiKey,
} from "./onboard-auth.js";
```

Add handling for `kilocode-api-key`:

```
if (authChoice === "kilocode-api-key") {
  const store = ensureAuthProfileStore(params.agentDir, {
    allowKeychainPrompt: false,
  });
  const profileOrder = resolveAuthProfileOrder({
    cfg: nextConfig,
    store,
    provider: "kilocode",
  });
  const existingProfileId = profileOrder.find((profileId) => Boolean(store.profiles[profileId]));
  const existingCred = existingProfileId ? store.profiles[existingProfileId] : undefined;
  let profileId = "kilocode:default";
  let mode: "api_key" | "oauth" | "token" = "api_key";
  let hasCredential = false;

  if (existingProfileId && existingCred?.type) {
    profileId = existingProfileId;
    mode =
      existingCred.type === "oauth" ? "oauth" : existingCred.type === "token" ? "token" : "api_key";
    hasCredential = true;
  }

  if (!hasCredential && params.opts?.token && params.opts?.tokenProvider === "kilocode") {
    await setKilocodeApiKey(normalizeApiKeyInput(params.opts.token), params.agentDir);
    hasCredential = true;
  }

  if (!hasCredential) {
    const envKey = resolveEnvApiKey("kilocode");
    if (envKey) {
      const useExisting = await params.prompter.confirm({
        message: `Use existing KILOCODE_API_KEY (${envKey.source}, ${formatApiKeyPreview(envKey.apiKey)})?`,
        initialValue: true,
      });
      if (useExisting) {
        await setKilocodeApiKey(envKey.apiKey, params.agentDir);
        hasCredential = true;
      }
    }
  }

  if (!hasCredential) {
    const key = await params.prompter.text({
      message: "Enter Kilo Gateway API key",
      validate: validateApiKeyInput,
    });
    await setKilocodeApiKey(normalizeApiKeyInput(String(key)), params.agentDir);
    hasCredential = true;
  }

  if (hasCredential) {
    nextConfig = applyAuthProfileConfig(nextConfig, {
      profileId,
      provider: "kilocode",
      mode,
    });
  }
  {
    const applied = await applyDefaultModelChoice({
      config: nextConfig,
      setDefaultModel: params.setDefaultModel,
      defaultModel: KILOCODE_DEFAULT_MODEL_REF,
      applyDefaultConfig: applyKilocodeConfig,
      applyProviderConfig: applyKilocodeProviderConfig,
      noteDefault: KILOCODE_DEFAULT_MODEL_REF,
      noteAgentModel,
      prompter: params.prompter,
    });
    nextConfig = applied.config;
    agentModelOverride = applied.agentModelOverride ?? agentModelOverride;
  }
  return { config: nextConfig, agentModelOverride };
}
```

Also add tokenProvider mapping at the top of the function:

```
if (params.opts.tokenProvider === "kilocode") {
  authChoice = "kilocode-api-key";
}
```

### CLI Registration

#### 9\. `src/cli/program/register.onboard.ts`

Add CLI option:

```
.option("--kilocode-api-key <key>", "Kilo Gateway API key")
```

Add to action handler:

```
kilocodeApiKey: opts.kilocodeApiKey as string | undefined,
```

Update auth-choice help text:

```
.option(
  "--auth-choice <choice>",
  "Auth: setup-token|token|chutes|openai-codex|openai-api-key|openrouter-api-key|kilocode-api-key|ai-gateway-api-key|...",
)
```

### Non-Interactive Onboarding

#### 10\. `src/commands/onboard-non-interactive/local/auth-choice.ts`

Add handling for `kilocode-api-key`:

```
if (authChoice === "kilocode-api-key") {
  const resolved = await resolveNonInteractiveApiKey({
    provider: "kilocode",
    cfg: baseConfig,
    flagValue: opts.kilocodeApiKey,
    flagName: "--kilocode-api-key",
    envVar: "KILOCODE_API_KEY",
  });
  await setKilocodeApiKey(resolved.apiKey, agentDir);
  nextConfig = applyAuthProfileConfig(nextConfig, {
    profileId: "kilocode:default",
    provider: "kilocode",
    mode: "api_key",
  });
  // ... apply default model
}
```

### Export Updates

#### 11\. `src/commands/onboard-auth.ts`

Add exports:

```
export {
  // ... existing exports
  applyKilocodeConfig,
  applyKilocodeProviderConfig,
  KILOCODE_BASE_URL,
} from "./onboard-auth.config-core.js";

export {
  // ... existing exports
  KILOCODE_DEFAULT_MODEL_REF,
  setKilocodeApiKey,
} from "./onboard-auth.credentials.js";
```

### Special Handling (Optional)

#### 12\. `src/agents/pi-embedded-runner/cache-ttl.ts`

Add Kilo Gateway support for Anthropic models:

```
export function isCacheTtlEligibleProvider(provider: string, modelId: string): boolean {
  const normalizedProvider = provider.toLowerCase();
  const normalizedModelId = modelId.toLowerCase();
  if (normalizedProvider === "anthropic") return true;
  if (normalizedProvider === "openrouter" && normalizedModelId.startsWith("anthropic/"))
    return true;
  if (normalizedProvider === "kilocode" && normalizedModelId.startsWith("anthropic/")) return true;
  return false;
}
```

#### 13\. `src/agents/transcript-policy.ts`

Add Kilo Gateway handling (similar to OpenRouter):

```
const isKilocodeGemini = provider === "kilocode" && modelId.toLowerCase().includes("gemini");

// Include in needsNonImageSanitize check
const needsNonImageSanitize =
  isGoogle || isAnthropic || isMistral || isOpenRouterGemini || isKilocodeGemini;
```

## Configuration Structure

### User Config Example

```
{
  "models": {
    "mode": "merge",
    "providers": {
      "kilocode": {
        "baseUrl": "https://api.kilo.ai/api/gateway/",
        "apiKey": "xxxxx",
        "api": "openai-completions",
        "models": [
          {
            "id": "anthropic/claude-opus-4.6",
            "name": "Anthropic: Claude Opus 4.6"
          },
          { "id": "minimax/minimax-m2.5:free", "name": "Minimax: Minimax M2.5" }
        ]
      }
    }
  }
}
```

### Auth Profile Structure

```
{
  "profiles": {
    "kilocode:default": {
      "type": "api_key",
      "provider": "kilocode",
      "key": "xxxxx"
    }
  }
}
```

## Testing Considerations

1.  **Unit Tests:**
    *   Test `setKilocodeApiKey()` writes correct profile
    *   Test `applyKilocodeConfig()` sets correct defaults
    *   Test `resolveEnvApiKey("kilocode")` returns correct env var
2.  **Integration Tests:**
    *   Test onboarding flow with `--auth-choice kilocode-api-key`
    *   Test non-interactive onboarding with `--kilocode-api-key`
    *   Test model selection with `kilocode/` prefix
3.  **E2E Tests:**
    *   Test actual API calls through Kilo Gateway (live tests)

## Migration Notes

*   No migration needed for existing users
*   New users can immediately use `kilocode-api-key` auth choice
*   Existing manual config with `kilocode` provider will continue to work

## Future Considerations

1.  **Model Catalog:** If Kilo Gateway exposes a `/models` endpoint, add scanning support similar to `scanOpenRouterModels()`
2.  **OAuth Support:** If Kilo Gateway adds OAuth, extend the auth system accordingly
3.  **Rate Limiting:** Consider adding rate limit handling specific to Kilo Gateway if needed
4.  **Documentation:** Add docs at `docs/providers/kilocode.md` explaining setup and usage

## Summary of Changes

| File | Change Type | Description |
| --- | --- | --- |
| `src/commands/onboard-auth.credentials.ts` | Add | `KILOCODE_DEFAULT_MODEL_REF`, `setKilocodeApiKey()` |
| `src/agents/model-auth.ts` | Modify | Add `kilocode` to `envMap` |
| `src/config/io.ts` | Modify | Add `KILOCODE_API_KEY` to shell env keys |
| `src/commands/onboard-auth.config-core.ts` | Add | `applyKilocodeProviderConfig()`, `applyKilocodeConfig()` |
| `src/commands/onboard-types.ts` | Modify | Add `kilocode-api-key` to `AuthChoice`, add `kilocodeApiKey` to options |
| `src/commands/auth-choice-options.ts` | Modify | Add `kilocode` group and option |
| `src/commands/auth-choice.preferred-provider.ts` | Modify | Add `kilocode-api-key` mapping |
| `src/commands/auth-choice.apply.api-providers.ts` | Modify | Add `kilocode-api-key` handling |
| `src/cli/program/register.onboard.ts` | Modify | Add `--kilocode-api-key` option |
| `src/commands/onboard-non-interactive/local/auth-choice.ts` | Modify | Add non-interactive handling |
| `src/commands/onboard-auth.ts` | Modify | Export new functions |
| `src/agents/pi-embedded-runner/cache-ttl.ts` | Modify | Add kilocode support |
| `src/agents/transcript-policy.ts` | Modify | Add kilocode Gemini handling |

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/plans/openresponses-gateway -->

# OpenResponses Gateway Plan - OpenClaw

## OpenResponses Gateway Integration Plan

## Context

OpenClaw Gateway currently exposes a minimal OpenAI-compatible Chat Completions endpoint at `/v1/chat/completions` (see [OpenAI Chat Completions](https://docs.openclaw.ai/gateway/openai-http-api)). Open Responses is an open inference standard based on the OpenAI Responses API. It is designed for agentic workflows and uses item-based inputs plus semantic streaming events. The OpenResponses spec defines `/v1/responses`, not `/v1/chat/completions`.

## Goals

*   Add a `/v1/responses` endpoint that adheres to OpenResponses semantics.
*   Keep Chat Completions as a compatibility layer that is easy to disable and eventually remove.
*   Standardize validation and parsing with isolated, reusable schemas.

## Non-goals

*   Full OpenResponses feature parity in the first pass (images, files, hosted tools).
*   Replacing internal agent execution logic or tool orchestration.
*   Changing the existing `/v1/chat/completions` behavior during the first phase.

## Research Summary

Sources: OpenResponses OpenAPI, OpenResponses specification site, and the Hugging Face blog post. Key points extracted:

*   `POST /v1/responses` accepts `CreateResponseBody` fields like `model`, `input` (string or `ItemParam[]`), `instructions`, `tools`, `tool_choice`, `stream`, `max_output_tokens`, and `max_tool_calls`.
*   `ItemParam` is a discriminated union of:
    *   `message` items with roles `system`, `developer`, `user`, `assistant`
    *   `function_call` and `function_call_output`
    *   `reasoning`
    *   `item_reference`
*   Successful responses return a `ResponseResource` with `object: "response"`, `status`, and `output` items.
*   Streaming uses semantic events such as:
    *   `response.created`, `response.in_progress`, `response.completed`, `response.failed`
    *   `response.output_item.added`, `response.output_item.done`
    *   `response.content_part.added`, `response.content_part.done`
    *   `response.output_text.delta`, `response.output_text.done`
*   The spec requires:
    *   `Content-Type: text/event-stream`
    *   `event:` must match the JSON `type` field
    *   terminal event must be literal `[DONE]`
*   Reasoning items may expose `content`, `encrypted_content`, and `summary`.
*   HF examples include `OpenResponses-Version: latest` in requests (optional header).

## Proposed Architecture

*   Add `src/gateway/open-responses.schema.ts` containing Zod schemas only (no gateway imports).
*   Add `src/gateway/openresponses-http.ts` (or `open-responses-http.ts`) for `/v1/responses`.
*   Keep `src/gateway/openai-http.ts` intact as a legacy compatibility adapter.
*   Add config `gateway.http.endpoints.responses.enabled` (default `false`).
*   Keep `gateway.http.endpoints.chatCompletions.enabled` independent; allow both endpoints to be toggled separately.
*   Emit a startup warning when Chat Completions is enabled to signal legacy status.

## Deprecation Path for Chat Completions

*   Maintain strict module boundaries: no shared schema types between responses and chat completions.
*   Make Chat Completions opt-in by config so it can be disabled without code changes.
*   Update docs to label Chat Completions as legacy once `/v1/responses` is stable.
*   Optional future step: map Chat Completions requests to the Responses handler for a simpler removal path.

## Phase 1 Support Subset

*   Accept `input` as string or `ItemParam[]` with message roles and `function_call_output`.
*   Extract system and developer messages into `extraSystemPrompt`.
*   Use the most recent `user` or `function_call_output` as the current message for agent runs.
*   Reject unsupported content parts (image/file) with `invalid_request_error`.
*   Return a single assistant message with `output_text` content.
*   Return `usage` with zeroed values until token accounting is wired.

## Validation Strategy (No SDK)

*   Implement Zod schemas for the supported subset of:
    *   `CreateResponseBody`
    *   `ItemParam` + message content part unions
    *   `ResponseResource`
    *   Streaming event shapes used by the gateway
*   Keep schemas in a single, isolated module to avoid drift and allow future codegen.

## Streaming Implementation (Phase 1)

*   SSE lines with both `event:` and `data:`.
*   Required sequence (minimum viable):
    *   `response.created`
    *   `response.output_item.added`
    *   `response.content_part.added`
    *   `response.output_text.delta` (repeat as needed)
    *   `response.output_text.done`
    *   `response.content_part.done`
    *   `response.completed`
    *   `[DONE]`

## Tests and Verification Plan

*   Add e2e coverage for `/v1/responses`:
    *   Auth required
    *   Non-stream response shape
    *   Stream event ordering and `[DONE]`
    *   Session routing with headers and `user`
*   Keep `src/gateway/openai-http.test.ts` unchanged.
*   Manual: curl to `/v1/responses` with `stream: true` and verify event ordering and terminal `[DONE]`.

## Doc Updates (Follow-up)

*   Add a new docs page for `/v1/responses` usage and examples.
*   Update `/gateway/openai-http-api` with a legacy note and pointer to `/v1/responses`.

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/onboarding-config-protocol -->

# Onboarding and Config Protocol - OpenClaw

Purpose: shared onboarding + config surfaces across CLI, macOS app, and Web UI.

## Components

*   Wizard engine (shared session + prompts + onboarding state).
*   CLI onboarding uses the same wizard flow as the UI clients.
*   Gateway RPC exposes wizard + config schema endpoints.
*   macOS onboarding uses the wizard step model.
*   Web UI renders config forms from JSON Schema + UI hints.

## Gateway RPC

*   `wizard.start` params: `{ mode?: "local"|"remote", workspace?: string }`
*   `wizard.next` params: `{ sessionId, answer?: { stepId, value? } }`
*   `wizard.cancel` params: `{ sessionId }`
*   `wizard.status` params: `{ sessionId }`
*   `config.schema` params: `{}`
*   `config.schema.lookup` params: `{ path }`
    *   `path` accepts standard config segments plus slash-delimited plugin ids, for example `plugins.entries.pack/one.config`.

Responses (shape)

*   Wizard: `{ sessionId, done, step?, status?, error? }`
*   Config schema: `{ schema, uiHints, version, generatedAt }`
*   Config schema lookup: `{ path, schema, hint?, hintPath?, children[] }`

## UI Hints

*   `uiHints` keyed by path; optional metadata (label/help/group/order/advanced/sensitive/placeholder).
*   Sensitive fields render as password inputs; no redaction layer.
*   Unsupported schema nodes fall back to the raw JSON editor.

## Notes

*   This doc is the single place to track protocol refactors for onboarding/config.

---

<!-- SOURCE: https://docs.openclaw.ai/experiments/plans/browser-evaluate-cdp-refactor -->

# Browser Evaluate CDP Refactor - OpenClaw

## Context

`act:evaluate` executes user provided JavaScript in the page. Today it runs via Playwright (`page.evaluate` or `locator.evaluate`). Playwright serializes CDP commands per page, so a stuck or long running evaluate can block the page command queue and make every later action on that tab look “stuck”. PR #13498 adds a pragmatic safety net (bounded evaluate, abort propagation, and best-effort recovery). This document describes a larger refactor that makes `act:evaluate` inherently isolated from Playwright so a stuck evaluate cannot wedge normal Playwright operations.

## Goals

*   `act:evaluate` cannot permanently block later browser actions on the same tab.
*   Timeouts are single source of truth end to end so a caller can rely on a budget.
*   Abort and timeout are treated the same way across HTTP and in-process dispatch.
*   Element targeting for evaluate is supported without switching everything off Playwright.
*   Maintain backward compatibility for existing callers and payloads.

## Non-goals

*   Replace all browser actions (click, type, wait, etc.) with CDP implementations.
*   Remove the existing safety net introduced in PR #13498 (it remains a useful fallback).
*   Introduce new unsafe capabilities beyond the existing `browser.evaluateEnabled` gate.
*   Add process isolation (worker process/thread) for evaluate. If we still see hard to recover stuck states after this refactor, that is a follow-up idea.

## Current Architecture (Why It Gets Stuck)

At a high level:

*   Callers send `act:evaluate` to the browser control service.
*   The route handler calls into Playwright to execute the JavaScript.
*   Playwright serializes page commands, so an evaluate that never finishes blocks the queue.
*   A stuck queue means later click/type/wait operations on the tab can appear to hang.

## Proposed Architecture

### 1\. Deadline Propagation

Introduce a single budget concept and derive everything from it:

*   Caller sets `timeoutMs` (or a deadline in the future).
*   The outer request timeout, route handler logic, and the execution budget inside the page all use the same budget, with small headroom where needed for serialization overhead.
*   Abort is propagated as an `AbortSignal` everywhere so cancellation is consistent.

Implementation direction:

*   Add a small helper (for example `createBudget({ timeoutMs, signal })`) that returns:
    *   `signal`: the linked AbortSignal
    *   `deadlineAtMs`: absolute deadline
    *   `remainingMs()`: remaining budget for child operations
*   Use this helper in:
    *   `src/browser/client-fetch.ts` (HTTP and in-process dispatch)
    *   `src/node-host/runner.ts` (proxy path)
    *   browser action implementations (Playwright and CDP)

### 2\. Separate Evaluate Engine (CDP Path)

Add a CDP based evaluate implementation that does not share Playwright’s per page command queue. The key property is that the evaluate transport is a separate WebSocket connection and a separate CDP session attached to the target. Implementation direction:

*   New module, for example `src/browser/cdp-evaluate.ts`, that:
    *   Connects to the configured CDP endpoint (browser level socket).
    *   Uses `Target.attachToTarget({ targetId, flatten: true })` to get a `sessionId`.
    *   Runs either:
        *   `Runtime.evaluate` for page level evaluate, or
        *   `DOM.resolveNode` plus `Runtime.callFunctionOn` for element evaluate.
    *   On timeout or abort:
        *   Sends `Runtime.terminateExecution` best-effort for the session.
        *   Closes the WebSocket and returns a clear error.

Notes:

*   This still executes JavaScript in the page, so termination can have side effects. The win is that it does not wedge the Playwright queue, and it is cancelable at the transport layer by killing the CDP session.

### 3\. Ref Story (Element Targeting Without A Full Rewrite)

The hard part is element targeting. CDP needs a DOM handle or `backendDOMNodeId`, while today most browser actions use Playwright locators based on refs from snapshots. Recommended approach: keep existing refs, but attach an optional CDP resolvable id.

#### 3.1 Extend Stored Ref Info

Extend the stored role ref metadata to optionally include a CDP id:

*   Today: `{ role, name, nth }`
*   Proposed: `{ role, name, nth, backendDOMNodeId?: number }`

This keeps all existing Playwright based actions working and allows CDP evaluate to accept the same `ref` value when the `backendDOMNodeId` is available.

#### 3.2 Populate backendDOMNodeId At Snapshot Time

When producing a role snapshot:

1.  Generate the existing role ref map as today (role, name, nth).
2.  Fetch the AX tree via CDP (`Accessibility.getFullAXTree`) and compute a parallel map of `(role, name, nth) -> backendDOMNodeId` using the same duplicate handling rules.
3.  Merge the id back into the stored ref info for the current tab.

If mapping fails for a ref, leave `backendDOMNodeId` undefined. This makes the feature best-effort and safe to roll out.

#### 3.3 Evaluate Behavior With Ref

In `act:evaluate`:

*   If `ref` is present and has `backendDOMNodeId`, run element evaluate via CDP.
*   If `ref` is present but has no `backendDOMNodeId`, fall back to the Playwright path (with the safety net).

Optional escape hatch:

*   Extend the request shape to accept `backendDOMNodeId` directly for advanced callers (and for debugging), while keeping `ref` as the primary interface.

### 4\. Keep A Last Resort Recovery Path

Even with CDP evaluate, there are other ways to wedge a tab or a connection. Keep the existing recovery mechanisms (terminate execution + disconnect Playwright) as a last resort for:

*   legacy callers
*   environments where CDP attach is blocked
*   unexpected Playwright edge cases

## Implementation Plan (Single Iteration)

### Deliverables

*   A CDP based evaluate engine that runs outside the Playwright per-page command queue.
*   A single end-to-end timeout/abort budget used consistently by callers and handlers.
*   Ref metadata that can optionally carry `backendDOMNodeId` for element evaluate.
*   `act:evaluate` prefers the CDP engine when possible and falls back to Playwright when not.
*   Tests that prove a stuck evaluate does not wedge later actions.
*   Logs/metrics that make failures and fallbacks visible.

### Implementation Checklist

1.  Add a shared “budget” helper to link `timeoutMs` + upstream `AbortSignal` into:
    *   a single `AbortSignal`
    *   an absolute deadline
    *   a `remainingMs()` helper for downstream operations
2.  Update all caller paths to use that helper so `timeoutMs` means the same thing everywhere:
    *   `src/browser/client-fetch.ts` (HTTP and in-process dispatch)
    *   `src/node-host/runner.ts` (node proxy path)
    *   CLI wrappers that call `/act` (add `--timeout-ms` to `browser evaluate`)
3.  Implement `src/browser/cdp-evaluate.ts`:
    *   connect to the browser-level CDP socket
    *   `Target.attachToTarget` to get a `sessionId`
    *   run `Runtime.evaluate` for page evaluate
    *   run `DOM.resolveNode` + `Runtime.callFunctionOn` for element evaluate
    *   on timeout/abort: best-effort `Runtime.terminateExecution` then close the socket
4.  Extend stored role ref metadata to optionally include `backendDOMNodeId`:
    *   keep existing `{ role, name, nth }` behavior for Playwright actions
    *   add `backendDOMNodeId?: number` for CDP element targeting
5.  Populate `backendDOMNodeId` during snapshot creation (best-effort):
    *   fetch AX tree via CDP (`Accessibility.getFullAXTree`)
    *   compute `(role, name, nth) -> backendDOMNodeId` and merge into the stored ref map
    *   if mapping is ambiguous or missing, leave the id undefined
6.  Update `act:evaluate` routing:
    *   if no `ref`: always use CDP evaluate
    *   if `ref` resolves to a `backendDOMNodeId`: use CDP element evaluate
    *   otherwise: fall back to Playwright evaluate (still bounded and abortable)
7.  Keep the existing “last resort” recovery path as a fallback, not the default path.
8.  Add tests:
    *   stuck evaluate times out within budget and the next click/type succeeds
    *   abort cancels evaluate (client disconnect or timeout) and unblocks subsequent actions
    *   mapping failures cleanly fall back to Playwright
9.  Add observability:
    *   evaluate duration and timeout counters
    *   terminateExecution usage
    *   fallback rate (CDP -> Playwright) and reasons

### Acceptance Criteria

*   A deliberately hung `act:evaluate` returns within the caller budget and does not wedge the tab for later actions.
*   `timeoutMs` behaves consistently across CLI, agent tool, node proxy, and in-process calls.
*   If `ref` can be mapped to `backendDOMNodeId`, element evaluate uses CDP; otherwise the fallback path is still bounded and recoverable.

## Testing Plan

*   Unit tests:
    *   `(role, name, nth)` matching logic between role refs and AX tree nodes.
    *   Budget helper behavior (headroom, remaining time math).
*   Integration tests:
    *   CDP evaluate timeout returns within budget and does not block the next action.
    *   Abort cancels evaluate and triggers termination best-effort.
*   Contract tests:
    *   Ensure `BrowserActRequest` and `BrowserActResponse` remain compatible.

## Risks And Mitigations

*   Mapping is imperfect:
    *   Mitigation: best-effort mapping, fallback to Playwright evaluate, and add debug tooling.
*   `Runtime.terminateExecution` has side effects:
    *   Mitigation: only use on timeout/abort and document the behavior in errors.
*   Extra overhead:
    *   Mitigation: only fetch AX tree when snapshots are requested, cache per target, and keep CDP session short lived.
*   Extension relay limitations:
    *   Mitigation: use browser level attach APIs when per page sockets are not available, and keep the current Playwright path as fallback.

## Open Questions

*   Should the new engine be configurable as `playwright`, `cdp`, or `auto`?
*   Do we want to expose a new “nodeRef” format for advanced users, or keep `ref` only?
*   How should frame snapshots and selector scoped snapshots participate in AX mapping?

