---
name: task_weight_manager
description: Use when a user wants OpenClaw to manage several interleaved conversation threads inside one chat, keep a primary mission in focus, classify side topics, assign weights or priorities, reduce distraction, and periodically steer attention back to the main task. Also fits the Chinese concept "任务权重管理器".
version: 1.0.1
metadata:
  openclaw:
    emoji: "🎯"
    homepage: "https://github.com/LucasZH7/openclaw-task-weight-manager"
    os:
      - macos
      - linux
      - windows
    requires:
      anyBins:
        - python3
---

# Task Weight Manager

Use this skill when one conversation contains multiple strands of intent and the user wants the agent to stay oriented instead of drifting.

## What this skill does

- Splits recent conversation into named threads.
- Assigns each thread a weight based on priority, urgency, dependency, and user intent.
- Chooses a `mainline` thread and protects it from casual drift.
- Captures interruptions into a parking lot instead of losing them.
- Periodically re-checks whether the current work still matches the highest-value thread.

## Default operating model

Treat the conversation as a weighted queue of threads, not as one flat transcript.

Each thread should have:

- `id`: short label such as `A`, `B`, `F`
- `title`: one-line meaning
- `goal`: desired outcome
- `weight`: `1-100`
- `state`: `mainline`, `active`, `parked`, `blocked`, or `done`
- `evidence`: the latest user turns that justify the classification
- `next_action`: smallest useful next step

## Weighting rules

Start from the user's explicit intent, then adjust using these signals:

- `+40` if the user says this is the main task, primary goal, or highest priority
- `+25` if other work depends on it
- `+20` if it is time-sensitive
- `+15` if the user has already invested significant context into it
- `-15` if it is merely exploratory or nice-to-have
- `-20` if it is blocked by missing inputs

Use relative judgment, not rigid math. The purpose is stable prioritization, not fake precision.

## Focus lock

If one thread clearly dominates, mark it as `mainline` and behave as follows:

1. Continue work inside that thread unless a higher-priority interruption appears.
2. When the user introduces a side topic, classify it, acknowledge it briefly, and park it.
3. Return to the `mainline` in the same response unless the user explicitly switched.

Do not silently abandon the `mainline` because of an interesting tangent.

## Interrupt handling

When a new topic appears during focused work:

1. Decide whether it is `urgent`, `important but not now`, or `background noise`.
2. If not urgent, store it as a separate thread.
3. Tell the user where it was parked.
4. Resume the `mainline`.

Good phrasing pattern:

`我把这个记到线程 B（技能体系）里，当前先继续线程 F（主线任务）。`

## Reflection loop

Whenever the user asks for re-prioritization, or when periodic automation wakes the agent:

1. Re-read the latest turns plus the saved thread board.
2. Merge duplicates.
3. Re-score each thread.
4. Check whether the current work still matches the highest-weight thread.
5. If drift happened, explain the drift in one sentence and steer back.

## Response contract

When this skill is active, prefer compact status blocks like:

```md
主线: F - 完成任务权重管理器 MVP
当前排序: F(92) > B(61) > D(38)
本轮动作: 继续完成 F 的下一步，并把新话题先停放到 B
```

Then continue the actual work.

## State persistence

If the workspace allows files, maintain a small board at:

- `task-weight-manager/threads.md`

Keep it human-readable. Update only when the thread model materially changes.

Suggested section layout:

- `Mainline`
- `Weighted Threads`
- `Parking Lot`
- `Blocked`
- `Done`

## Guardrails

- Do not create too many threads for tiny wording variations.
- Do not keep stale threads alive just because they once existed.
- Do not override a direct user switch of priority.
- Do not use weighting language to avoid answering the user's current explicit request.
- If two threads are truly tied, say so and ask for a priority decision only if needed.

## When to read more

Read [references/integration.md](references/integration.md) when the user wants this behavior to work with OpenClaw features such as `HEARTBEAT.md`, `cron`, `memory`, or `session` isolation.

Read [references/usage-patterns.md](references/usage-patterns.md) when the user wants examples, Chinese command phrases, or recommended operating patterns.
