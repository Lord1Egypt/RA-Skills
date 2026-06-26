# Stateful Targets

## Goal

有些 target class 不是“越写越多越好”，而是必须保持当前真相。

这份文档定义：

- 哪些 target class 是状态型
- 它们该用 append、replace 还是 merge
- 多个 skill 一起写时，什么算 canonical state

## Classification

### Append-Oriented

这些更像日志或档案：

- `daily_memory`
- `reusable_lessons`
- `project_facts` 中的历史记录部分

默认行为：

- append
- 允许按主题整理
- 不要求始终只有一个“当前值”

### State-Oriented

这些更像当前状态槽位：

- `proactive_state`
- `working_buffer`

默认行为：

- 优先维护“当前真相”
- 不应无限 append 成流水账
- 必须能快速看出最新状态

## Canonical Write Semantics

### `proactive_state`

`proactive_state` 是一个 state family，不一定只对应一个文件。

宿主可以有两种实现：

- combined file
- split adapter: durable boundary slice + current task state slice

默认写语义：

- replace for canonical fields
- append only for very short change notes if the host explicitly wants them

最小推荐字段：

- `updated_at`
- `current_objective`
- `current_blocker`
- `next_move`
- optional `durable_boundaries`
- `owner` or `source_skill` when multiple writers exist

规则：

- 新状态覆盖旧状态，不要把每次变化都当历史日志
- 如果 adapter 是 split implementation，`session-state` slice 负责当前任务真相，boundary slice 负责 durable proactive boundaries
- 如果多个 skill 都会写，宿主必须定义 canonical writer 或 merge policy
- 没有明确 merge policy 时，latest valid update wins

### `working_buffer`

默认写语义：

- append for short-lived breadcrumbs
- prune aggressively

最小推荐字段：

- `updated_at`
- `task_ref` if available
- `breadcrumb`
- optional `source_skill`

规则：

- 一条 breadcrumb 只服务当前恢复，不要把它写成长期说明
- 完成恢复后，删除、合并或提炼
- 同一 task 下重复 breadcrumb 应合并，不应无限重复

## Multi-Writer Rule

如果多个 skill 会写同一个 stateful target：

1. host should define a canonical writer if possible
2. if not, require `updated_at`
3. if not, require `source_skill`
4. conflicts resolve to the newest valid state unless the host defines stronger precedence

不要把“谁先写进去”当成权威。

## Multi-Agent Writer Rule

OpenClaw 2026.6.1 的 Workboard 让多个 agent 协作。多 agent 共享记忆时，写入治理要从 skill 级再往上抬一层到 agent 级。

默认规则：

1. 如果多个 agent 会写同一个 stateful target，host 应为该 target 指定一个 canonical agent writer
2. 如果无法指定，每条写入必须带 `owner` / `source_agent`，而不只是 `source_skill`
3. 跨 agent 的当前真相冲突，默认以 newest valid update 为准，除非 host 声明了更强的 precedence
4. 协作型 agent 之间不应各自把对方还没确认的中间状态固化成 canonical

per-agent namespace 建议：

- 如果宿主支持，给每个 agent 一个独立的 `working_buffer` 和当前任务 `proactive_state` 命名空间
- `long_term_memory`、`reusable_lessons`、`system_rules` 这类共享层应保持单一 canonical 副本，由 canonical writer 维护
- 不要让每个 agent 各自维护一份全局规则副本，否则会产生规则 drift

一句话：

- skill 级 multi-writer 解决“多个 skill 抢写”
- agent 级 multi-writer 解决“多个协作 agent 抢写 + 各自固化中间态”
- 两层都应有 canonical writer 或 `owner` 字段，不能只靠“谁先写”

## Anti-Patterns

- 把 `proactive_state` 写成操作日志
- 把 `working_buffer` 写成永久草稿箱
- 多个 skill 同时 append 当前状态，没人负责覆盖旧值
- 没有时间戳也没有 source，就宣称这份状态是“当前真相”
- 多个协作 agent 各自把未确认的中间状态固化成 canonical task state
- 每个 agent 各持一份全局规则副本，导致 `system_rules` 长期 drift
