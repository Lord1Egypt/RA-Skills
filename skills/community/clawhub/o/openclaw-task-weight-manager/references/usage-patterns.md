# Usage Patterns

Use this reference when the user wants the skill to feel consistent, disciplined, and easy to steer in daily work.

## Recommended commands

These commands are short enough to use in ordinary chat:

- `开始主线任务：F`
- `锁定主线 30 分钟`
- `列出所有线程`
- `把刚才那段归到 B`
- `重新加权`
- `只告诉我当前主线`
- `恢复被打断的主线`
- `把低优先级都停到停车场`

## Recommended response style

When the conversation is noisy, answer in this order:

1. State the current `mainline`.
2. Mention any new thread classifications.
3. Resume the mainline or explain why it changed.

Good compact pattern:

```md
主线: F - 完成发布版 skill
新增分类: B = 想法整理, C = 后续自动化
处理策略: B/C 先停放，继续推进 F
```

## Example thread taxonomy

Useful thread types for this skill:

- `Mainline`: the thing we are trying to finish now
- `Support`: material that helps the mainline
- `Reflection`: self-improvement, postmortem, strategy
- `Research`: exploratory questions or comparisons
- `Parking Lot`: valid but deferred ideas

## Promotion and demotion rules

Promote a parked thread when:

- the user explicitly says it is now the main task
- the current mainline is blocked and the parked thread unblocks it
- new urgency appears

Demote an active thread when:

- it no longer helps the current mission
- it keeps consuming attention without producing progress
- it has become speculative

## Drift diagnosis

If the agent drifted, explain the reason in one sentence using one of these patterns:

- `我被一个相关但次优先的话题带偏了，现在回到主线。`
- `这个支线本来是辅助信息，但已经开始占用主线注意力，所以先停放。`
- `当前主线被阻塞，因此临时提升了能解锁它的线程。`

## Good fit

This skill works especially well when the user:

- likes one chat window instead of many tabs
- thinks out loud in fragments
- mixes strategy, execution, and reflection in one stream
- wants the agent to preserve focus rather than merely remember facts
