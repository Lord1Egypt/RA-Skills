# Retention Rules

## Goal

让短期层真的会变短，而不是只在命名上看起来短。

## Core Principle

不是所有记忆都该永久保留。

状态型和恢复型内容如果不清理，会反过来污染恢复判断。

## Target-Class Lifecycle

### `working_buffer`

定位：

- 极短期恢复线索

默认规则：

- task completes -> clear or distill
- interruption resolved -> prune what no longer helps recovery
- older than 7 days without refresh -> stale by default

允许留下的只有：

- 仍未完成的任务 breadcrumb
- 尚未提炼但明显值得提炼的片段

### `proactive_state`

定位：

- 当前 objective / blocker / next move
- 当前有效的主动性边界

默认规则：

- task state changes -> replace canonical fields
- task completes -> clear task-specific fields
- older than 7 days without refresh -> review for staleness

区分两类内容：

- durable boundary -> may stay
- task-specific state -> must refresh or clear

### `daily_memory`

定位：

- 当日事件与阶段记录

默认规则：

- date-scoped archive
- do not treat it as live current state after the day has passed
- promote important items instead of repeatedly reopening the old note

### `reusable_lessons`

定位：

- distilled reusable lessons

默认规则：

- keep until contradicted, superseded, or proven too local

### `long_term_memory`

定位：

- stable facts and preferences

默认规则：

- keep until invalidated
- update in place when a stable fact changes

## Staleness Signals

以下信号说明内容可能已经 stale：

- 没有最近更新时间
- 指向的任务已经结束
- blocker 已被解决但状态没更新
- next move 已经执行完
- 同主题在更新层出现了更近的 canonical state

## Review Moments

至少在这些时刻检查 retention：

- session startup
- task completion
- meaningful interruption recovery
- promotion review before writing long-term memory
