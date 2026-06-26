---
name: hippocampus-subagent-memory
description: >
  Isolate and coordinate sub-agent memory in OpenClaw with Hippocampus using
  scoped IDs, bounded merge-back, and explicit cross-agent imports.
---

# Hippocampus Subagent Memory

Use this skill when OpenClaw spawns sub-agents that need their own memory
without contaminating the parent agent context.

## Use It For

- creating isolated sub-agent memory namespaces
- preventing accidental memory leakage across siblings
- returning only bounded summaries or artifacts to the parent
- coordinating explicit import from child to parent

## Preferred Flow

1. Spawn a child with a scoped `HIPOKAMP_SUBAGENT_ID`.
2. Let the child write only into its own namespace.
3. Return a bounded result package at the end of the task.
4. Import back to parent only what is explicitly approved.

## Guidance

- Default to isolation.
- Do not flatten full child memory into the parent.
- Prefer summary, artifacts, and references over transcript copy.
- Tag child memory with session and parent linkage metadata.
- Root-agent bootstrap should happen once in the portal; child agents should
  inherit scope automatically and should not require separate portal signup.

## Related

- `hippocampus-memory-core` for core memory operations
- `hippocampus-openclaw-onboarding` for base config
- `@hippocampus/openclaw-context-engine` for automated spawn/end lifecycle hooks
