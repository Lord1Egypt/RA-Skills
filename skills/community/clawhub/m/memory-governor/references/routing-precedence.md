# Routing Precedence

## Goal

解决 capture 阶段最容易出现的歧义路由。

不要把“这条信息好像两个地方都能放”留给不同 skill 自由发挥。

## General Rule

当一条信息同时像两个 target class 时：

1. 先选作用域更窄的层
2. 先选语义更临时的层
3. 先 capture 到低承诺层，再按 promotion rules 升格

一句话：

**先局部，后全局。先短存，后长期。**

## Canonical Tie-Breakers

### `daily_memory` vs `long_term_memory`

默认先写 `daily_memory`。

只有在信息已经明显是长期稳定事实或长期稳定偏好时，才直接进入 `long_term_memory`。

### `learning_candidates` vs `reusable_lessons`

默认先写 `learning_candidates`。

只有当经验已经明显跨任务成立，或者用户已经明确把它升格为长期规则时，才直接进入 `reusable_lessons`。

一句话：

- 单次纠错，先候选
- 重复验证后，再复用

### `project_facts` vs `reusable_lessons`

默认先写 `project_facts`。

只有当一条规则已经明确跨项目可复用，才进入 `reusable_lessons`。

判定顺序：

1. 这条内容是否只对当前项目成立？
2. 如果项目变了，它还成立吗？
3. 是否已经在多个项目或任务里重复验证？

如果前两条偏“项目局部”，先写 `project_facts`。

### `proactive_state` vs `working_buffer`

默认分工：

- 当前 objective / blocker / next move -> `proactive_state`
- 临时 breadcrumb / partial finding / resume hint -> `working_buffer`

不要把“当前任务状态”塞进 `working_buffer` 里长期漂着。

### `reusable_lessons` vs `system_rules`

默认先写 `reusable_lessons`。

只有当它已经明确改变全局启动流程、协作边界、默认行为时，才升到 `system_rules`。

### `reusable_lessons` vs `tool_rules`

如果主要约束的是工具、命令、平台格式、配置，进入 `tool_rules`。

否则先留在 `reusable_lessons`。

## Escalation Rule

遇到仍然无法判断的边界项时：

- 不要直接升到全局规则
- 先 capture 到较低承诺层
- 等更多证据出现后再 promotion

这比误把局部规则写成全局真理安全得多。
