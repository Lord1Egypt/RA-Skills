---
name: orgx-power
description: Power-user OrgX skill for OpenClaw. Use when you explicitly need the full mutation surface for entity CRUD, run control, checkpoints, stream reassignment, or agent-config policy changes.
version: 1.0.0
user-invocable: true
tags:
  - orchestration
  - orgx
  - power-user
  - openclaw
---

# OrgX Power (OpenClaw)

Use this skill only when the caller explicitly needs the **full mutation surface** exposed by the OrgX OpenClaw plugin. This is the elevated counterpart to the default-safe `orgx` skill.

> Use `orgx` by default. Use `orgx-power` when you need admin or orchestration operations that change entity state directly.

## When to use this skill

- creating or updating OrgX entities directly
- reassigning streams or changing execution ownership
- pausing, resuming, cancelling, or rolling back runs
- listing or restoring checkpoints
- inspecting or updating managed agent config policy
- working against the unscoped `/orgx/mcp` endpoint rather than a domain-scoped safe surface

## Elevated tool surface

These tools are part of the plugin registry, but are elevated and should be used intentionally:

- `orgx_apply_changeset`
- `orgx_create_entity`
- `orgx_update_entity`
- `orgx_list_entities`
- `orgx_reassign_stream`
- `orgx_reassign_streams`
- `orgx_delegation_preflight`
- `orgx_run_action`
- `orgx_checkpoints_list`
- `orgx_checkpoint_restore`
- `orgx_agent_sessions`
- `orgx_resume_agent_session`
- `orgx_clear_agent_session`
- `update_agent_config`
- `orgx_sentinel_catalog`

The default-safe reporting tools still apply and should usually wrap elevated work:

- `orgx_emit_activity`
- `orgx_request_decision`
- `orgx_register_artifact`
- `orgx_spawn_check`
- `orgx_proof_status`
- `orgx_verify_completion`

## Operating discipline

1. Announce intent with `orgx_emit_activity` before making mutations.
2. Prefer `orgx_request_decision` before irreversible or org-wide changes.
3. Use `orgx_apply_changeset` when you need idempotent batched state updates.
4. Register artifacts for anything another operator would need to inspect later.
5. Verify completion and proof state after major mutations.

## Examples

### Batched entity mutation

```js
orgx_apply_changeset({
  initiative_id: "aa6d16dc-d450-417f-8a17-fd89bd597195",
  idempotency_key: "run_abc_turn_7_commit_1",
  operations: [
    { op: "task.update", task_id: "task_uuid", status: "in_progress" },
    { op: "decision.create", title: "Use SSE for live updates", urgency: "medium" }
  ]
})
```

### Reassign a stream

```js
orgx_reassign_stream({
  initiative_id: "aa6d16dc-d450-417f-8a17-fd89bd597195",
  workstream_id: "7f8e2f61-...",
  domain: "operations",
  role: "reliability"
})
```

### Run control

```js
orgx_run_action({
  runId: "9d5c8b2b-...",
  action: "pause",
  reason: "Waiting for approval on production cutover"
})
```

## Safety note

This skill assumes the runtime actually exposes the elevated tools. In the managed OrgX agent suite, many domain-scoped surfaces intentionally hide them. If a tool is unavailable, fall back to the safe `orgx` skill and request the necessary human decision or orchestration context.
