# Session Patterns

## Default builder spawn

Use a persistent ACP Claude Code session for real coding work:

```json
{
  "task": "Implement the feature from shared/specs/x.md and write outputs under shared/artifacts/x/",
  "label": "x-builder",
  "runtime": "acp",
  "agentId": "claude",
  "thread": true,
  "mode": "session",
  "timeoutSeconds": 1200,
  "runTimeoutSeconds": 1200
}
```

## Reviewer spawn

```json
{
  "task": "Review the implementation in shared/artifacts/x/ against shared/specs/x.md. Return concrete deltas only.",
  "label": "x-reviewer",
  "runtime": "acp",
  "agentId": "claude",
  "thread": true,
  "mode": "session",
  "timeoutSeconds": 1200,
  "runTimeoutSeconds": 1200
}
```

## Targeted fixer spawn with Codex

```json
{
  "task": "Apply only the reviewer deltas listed in shared/reviews/x-round1.md. Keep the patch minimal.",
  "label": "x-fixer",
  "runtime": "acp",
  "agentId": "codex",
  "thread": true,
  "mode": "session",
  "timeoutSeconds": 1200,
  "runTimeoutSeconds": 1200
}
```

## Rule of thumb

- **Claude Code**: default builder/reviewer
- **Codex**: narrow fixer / patch worker
- **OpenClaw**: routing, state, summaries, human checkpoints
