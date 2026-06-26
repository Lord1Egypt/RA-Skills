# Shared Routing Group Schema

Use this reference when a project does **not** own an entire Telegram group by itself, but instead participates in a shared routing group with multiple topics and potentially multiple projects.

Read this file when:

- the user says a project shares a Telegram group with another project
- one group contains multiple operational topics with different owners
- topic ownership must be made explicit
- the scaffold should emit schema stubs without changing runtime bindings

## Required Model

Every shared routing group should declare:

- routing group metadata
- topic ownership
- project scope
- workflow scope
- router-only vs answering mode

## Minimal Topic Ownership Stub

```json
{
  "topicOwnership": {
    "1": {
      "topicKey": "general",
      "ownerAgent": "main",
      "projectScope": "shared-cluster",
      "workflowScope": "router",
      "mode": "router-only"
    },
    "2": {
      "topicKey": "report",
      "ownerAgent": "<project-or-topic-agent>",
      "projectScope": "<project-id>",
      "workflowScope": "<workflow-surface>",
      "mode": "answering"
    }
  }
}
```

## Scaffold Behavior

For shared-routing-group mode, the scaffold should:

- not assume one project equals one group
- not overwrite an existing stable shared runtime binding automatically
- emit a reviewable schema stub first
- require explicit confirmation before touching live topic ownership

## Review Heuristic

If the current runtime is stable:

- prefer documentation/schema extraction first
- defer runtime mutation

If a topic has an owner agent but no explicit project/workflow scope:

- treat this as a schema gap, not necessarily a runtime bug


## Related System Review Checklist

See [SHARED_ROUTING_GROUP_REVIEW_CHECKLIST.md](/Users/ck/Documents/openclaw/openclaw-workspace/docs/SHARED_ROUTING_GROUP_REVIEW_CHECKLIST.md) before proposing runtime changes to a stable shared group.
