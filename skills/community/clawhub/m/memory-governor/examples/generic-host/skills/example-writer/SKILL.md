---
name: example-writer
description: 一个 generic host 中的示例 skill。展示普通 skill 如何在不依赖 OpenClaw 的情况下接入 memory-governor。
---

# Example Writer

这个 skill 会产出三类信息：

- 当天关键进展
- 可复用经验
- 临时恢复线索

## Memory Contract

This skill follows `memory-governor`.

### Produced Memory Types

- key progress update
- reusable lesson
- recovery hint

### Capability Declaration

```toml
[capabilities]
families = ["writer"]
```

### Target Class Routing

- key progress update -> `daily_memory`
- reusable lesson -> `reusable_lessons`
- recovery hint -> `working_buffer`

### Adapter Assumption

这个 skill 不直接写死 OpenClaw 路径。

它只假设宿主会提供自己的 adapter map。

在这个 generic host 示例里：

- `daily_memory` -> `notes/daily/YYYY-MM-DD.md`
- `proactive_state` -> `memory/proactive-state.md`
- `reusable_lessons` -> `memory/reusable-lessons.md`
- `working_buffer` -> `memory/working-buffer.md`

### Fallback Behavior

如果没有更强的宿主 adapter：

- `proactive_state` 使用本地 `memory/proactive-state.md`
- `reusable_lessons` 使用本地 `memory/reusable-lessons.md`
- `working_buffer` 使用本地 `memory/working-buffer.md`

### Exclusions

不应写入：

- secret
- 原始大段日志
- 无法复用的闲聊噪声
- 两周内必然过期的短期运行态
