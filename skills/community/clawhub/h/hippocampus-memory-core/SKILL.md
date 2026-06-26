---
name: hippocampus-memory-core
description: >
  Deterministic external memory for OpenClaw and coding agents using
  S3-Hipokamp. Use for storing durable facts, retrieving prior decisions,
  snapshotting memory, and restoring agent state.
---

# Hippocampus Memory Core

Use this skill when you need long-term memory that survives the current turn.

## Use It For

- storing key decisions and facts that should outlive the current session
- searching past architecture, deployment, or debugging context
- creating snapshots before risky changes
- restoring memory after migration or environment reset

## Preferred Flow

1. Check that Hippocampus configuration is present.
2. Store only high-signal facts, not raw transcript spam.
3. Search memory before repeating costly investigation.
4. Snapshot before major refactors or rollout changes.
5. Restore only into the correct agent or workspace scope.

## Guidance

- Prefer deterministic retrieval over ad hoc summaries.
- Keep memory namespaced by workspace and agent.
- Use metadata to mark project, topic, and task boundaries.
- Treat memory as durable infrastructure, not scratchpad overflow.
- If configuration is missing, send the user to `hippocampus-openclaw-onboarding`
  instead of asking for a raw API key first.

## Related

- `hippocampus-openclaw-onboarding` for first-time setup
- `hippocampus-subagent-memory` for isolated child-agent memory
- `@hippocampus/openclaw-context-engine` for native OpenClaw lifecycle integration
