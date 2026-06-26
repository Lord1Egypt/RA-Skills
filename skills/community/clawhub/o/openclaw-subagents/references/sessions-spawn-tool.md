# sessions_spawn Tool — Parameter Reference

Source: https://docs.openclaw.ai/tools/subagents

---

## Overview

`sessions_spawn` is the tool an agent calls to spawn a subagent programmatically.
It is non-blocking — it returns a run ID immediately, and the subagent announces its result
to the requester channel upon completion.

Return value:
```json
{ "status": "accepted", "runId": "...", "childSessionKey": "agent:<id>:subagent:<uuid>" }
```

---

## Parameters

### Required

| Parameter | Type | Description |
|---|---|---|
| `task` | string | The instruction for the subagent. Be specific and self-contained — the subagent starts fresh with no prior conversation context. |

### Optional

| Parameter | Type | Default | Description |
|---|---|---|---|
| `agentId` | string | caller's agent | Target a different agent configuration. Restricted by `allowAgents` allowlist. |
| `label` | string | — | Human-readable name shown in `/subagents list` |
| `model` | string | `agents.defaults.subagents.model` | Override the model for this run. Invalid values revert to default with a warning. |
| `thinking` | string | `"basic"` | Thinking level: `"none"`, `"basic"`, or `"deep"` |
| `runTimeoutSeconds` | number | 900 | Abort after N seconds. Set to `0` for no timeout. |
| `thread` | boolean | false | Discord only. Bind the subagent to the current thread for follow-up. Requires `mode: "session"`. |
| `mode` | string | `"run"` | `"run"` = one-shot (terminates after task). `"session"` = persistent interactive session (requires `thread: true`). |
| `cleanup` | string | `"keep"` | `"delete"` = archive session immediately after announcing result. `"keep"` = retain for `archiveAfterMinutes`. |
| `sandbox` | string | inherited | `"inherit"` = use caller's sandbox policy. `"require"` = enforce sandbox regardless. |

### Not Supported

These channel-delivery params are NOT available in sessions_spawn:
`target`, `channel`, `to`, `threadId`, `replyTo`, `transport`

---

## Example: Basic One-Shot Subagent

```json
{
  "task": "Search the web for SiteGPT G2 reviews from the last 6 months. Summarize the top 5 complaints and post them as a comment on Mission Control task ID conv_abc123.",
  "label": "g2-research",
  "model": "anthropic/claude-haiku-4-5",
  "thinking": "none",
  "runTimeoutSeconds": 300,
  "cleanup": "delete"
}
```

## Example: Orchestrator Spawning Workers (maxSpawnDepth: 2)

Orchestrator (depth 1) spawns workers (depth 2):

```json
{
  "task": "You are an orchestrator. Spawn 3 worker subagents in parallel: one to research G2 reviews, one to analyze competitor pricing, one to summarize Twitter sentiment. Synthesize all findings and post to task #42.",
  "label": "research-orchestrator",
  "model": "anthropic/claude-sonnet-4-5",
  "thinking": "basic",
  "runTimeoutSeconds": 1800
}
```

## Example: Persistent Session with Discord Thread Binding

```json
{
  "task": "You are Friday, the developer agent. Stay active and respond to follow-up messages in this thread about the API refactor task.",
  "mode": "session",
  "thread": true,
  "label": "friday-dev-session",
  "model": "anthropic/claude-sonnet-4-5"
}
```

---

## Slash Command Equivalent

To spawn from chat directly (without agent calling the tool):

```
/subagents spawn <agentId> <task description>
/subagents spawn researcher "Analyze G2 reviews for SiteGPT competitors"
```

With model/thinking flags:

```
/subagents spawn researcher "..." --model claude-haiku-4-5 --thinking none
```

---

## Announce Chain (How Results Are Returned)

Depth-2 worker completes
  -> Announces to depth-1 orchestrator
  -> Orchestrator synthesizes
  -> Announces to depth-0 main agent
  -> Main agent delivers to user

Each level only receives announces from its direct children.

The announce includes:
- Result text (assistant response or latest tool result)
- Status: `completed successfully` | `failed` | `timed out` | `unknown`
- Runtime and token usage statistics

---

## Cascade Stop Behavior

- `/stop` in main chat -> kills all depth-1 subagents -> cascades to their depth-2 children
- `/subagents kill <id>` -> stops specific subagent and all its children
- `/subagents kill all` -> stops all subagents for the current requester

---

## Limitations

- Announce is best-effort: lost if gateway restarts before announce is delivered
- Non-blocking: the tool returns immediately; do not wait for a direct response
- Context injected: only `AGENTS.md` + `TOOLS.md` (no SOUL.md, IDENTITY.md, or conversation history)
- Max nesting depth: 5 (recommended: 2)
- `maxChildrenPerAgent` hard cap: 20
