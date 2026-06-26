# Phased Rollout Plan for First-Class GrayMatter Adoption

This plan sequences implementation so we do not duplicate durability or resilience logic across the skill, plugin, and MCP surfaces.

## Goal

Make GrayMatter the shared memory platform through one client core, one tool contract, and multiple thin integration surfaces.

## Phase 1: Shared GrayMatter client extraction and hardening

### Entry criteria
- Current scripts and wrappers can authenticate and perform read/write/query operations.
- Existing fallback spool behavior is documented.

### Exit criteria
- A shared client module owns auth, retries, timeout policy, and error normalization.
- Durable memory operations (`MemoryEntry`, `GrayMatter`, `SwarmOps`) route through the shared client.
- Existing script-level callers are converted to the shared client or thin wrappers over it.

### Deliverables
- Shared client package in-repo with stable function signatures.
- Contract tests for success, auth-failure, transient failure, and fallback enqueue paths.

## Phase 2: MCP tool contract definition

### Entry criteria
- Shared client from Phase 1 is available and tested.

### Exit criteria
- Contract defines tool names, inputs, outputs, and error envelopes for memory/graph operations.
- Contract distinguishes durable memory writes from strategic/KPI/business-record writes.
- Contract includes idempotency and pagination conventions.

### Deliverables
- Versioned MCP contract document and schema examples.
- Compatibility notes for Codex and other ACP callers.

## Phase 3: MCP server on shared client

### Entry criteria
- MCP contract is finalized and versioned.

### Exit criteria
- MCP server implements contract using only shared client calls.
- Server surfaces normalized errors and health/status telemetry.
- Replay path for queued writes is available via server operation.

### Deliverables
- MCP server implementation.
- Integration tests covering read/write/query/graph and fallback replay behavior.

## Phase 4: OpenClaw plugin build or hardening

### Entry criteria
- Shared client and MCP server are stable.

### Exit criteria
- Plugin hooks read/write through shared client, without re-implementing retry/spool logic.
- Plugin status endpoint exposes auth, cache, and spool/replay health.
- Graceful fallback to local queue is preserved when API access degrades.

### Deliverables
- OpenClaw plugin implementation or hardening patch set.
- Hook-level tests for normal and degraded-path flows.

## Phase 5: Skill as thin usage guide layer

### Entry criteria
- Client, MCP server, and plugin surfaces are in place.

### Exit criteria
- Skill focuses on operator guidance, usage patterns, and examples.
- Skill no longer contains duplicated transport/resilience logic.
- Migration guidance from direct skill scripts to shared client + MCP/plugin flows is complete.

### Deliverables
- Updated `SKILL.md` and examples.
- Deprecation guidance for legacy direct-call paths.

## Compatibility and migration notes

### Current direct skill usage
- Keep existing script entrypoints functional during migration.
- Route scripts through shared client internals as phases progress.
- Maintain fallback spool format stability until replay migration is complete.

### Codex and ACP integrations
- Prefer MCP contract calls once Phase 3 ships.
- During transition, support both direct scripts and MCP with clear precedence:
  1. MCP server (preferred)
  2. Shared client wrappers
  3. Legacy script path (temporary)

## Anti-duplication guardrails

- No new retry or fallback logic may be added outside the shared client.
- All external surfaces (scripts, MCP, plugin) must consume shared error envelopes.
- Any new memory feature must include where it belongs in the five-phase model before merge.
