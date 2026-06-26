# OpenClaw Integration Notes

Use this reference when the user wants the skill to behave more like an always-on coordination layer.

## Best fit with official OpenClaw features

### `HEARTBEAT.md`

Use heartbeat for lightweight periodic self-checks. Keep the checklist short so it can safely run often.

Suggested heartbeat checklist:

```md
# Heartbeat checklist
- Reclassify the last active conversation turns into threads.
- Confirm whether the current mainline still has the highest weight.
- If drift is detected, capture the distraction into Parking Lot and steer back.
- If a parked thread becomes urgent, promote it and explain why.
```

### `cron`

Use cron when the user wants a stronger periodic loop than normal chat behavior.

Recommended starting intervals:

- Every `10-15` minutes for active execution sessions
- Every `30-60` minutes for lower-cost maintenance

Use cron to trigger a short system event such as:

- `Re-score current threads and return to the highest-weight mainline.`

Avoid very short intervals unless the user accepts the token cost.

### `memory`

Store stable task structure in files instead of hoping the whole transcript remains salient.

Recommended files:

- `task-weight-manager/threads.md`
- `task-weight-manager/decisions.md`

Use memory for:

- long-running goals
- why a thread is important
- switch history
- blocked reasons

Do not dump full chat logs into memory files.

### `session`

Session isolation is useful when one agent handles many different contexts.

Good pattern:

- one session for the project's main execution lane
- separate sessions for research, experiments, or reflective coaching

If the user insists on a single chat window, use the weighted-thread board to simulate sub-contexts inside that one session.

## Practical MVP vs full automation

### MVP

This skill alone can already:

- classify threads during normal chat
- keep a visible mainline
- park distractions
- support manual re-weighting

### Full automation

To match the user's stronger concept, add a small helper layer outside the skill:

1. Periodically fetch recent transcript slices.
2. Call an LLM to classify messages into thread IDs.
3. Update `task-weight-manager/threads.md`.
4. If the mainline changed, trigger a short reminder or system event.

That helper could be implemented later as:

- a cron-driven script
- a gateway extension
- an external service calling an OpenAI-compatible endpoint

## Suggested user commands

These phrases work well with the skill:

- `开始主线任务：F`
- `重新加权`
- `把刚才那个想法归到 B`
- `锁定主线 30 分钟`
- `列出现在所有线程`
- `为什么你刚才偏题了`

## Design intent

The main idea is not merely task management. It is attention management for an AI agent operating inside a noisy, single-threaded conversation surface.
