# Prompt 撰写规范

> 目的：为商店版 skill 提供唯一的 Prompt schema 约束来源。所有新建的任务拆解 Prompt 和复盘 Prompt，都必须基于本文件和 `meta_prompt.md` 生成与校验。

## 一、任务拆解 Prompt 设计规范

### 1. 输入字段

任务拆解 Prompt 必须基于以下输入字段设计：

- `goal_web`
- `core_goal`
- `core_flow`
- `date`
- `batch_seq`
- `next_batch_guidance`（可选）
- `carry_over_tasks`（可选）
- `user_feedback`（可选）

### 2. 输出结构

任务拆解 Prompt 必须输出一个 JSON 对象，顶层字段必须包含：

- `goal_web`
- `core_goal`
- `core_flow`
- `date`
- `batch_seq`
- `tasks`

`tasks` 数组中的每个任务必须包含：

- `task_id`
- `task`
- `task_description`
- `task_reason`
- `depends_on`
- `task_state`
- `task_result`
- `source`

当 `core_flow` 非空时，每个任务还必须包含：

- `flow_step`

### 3. 默认值要求

- `task_state` 默认 `pending`
- `task_result` 默认 `null`
- `source` 默认 `new`
- `depends_on` 无依赖时必须输出 `[]`

### 4. 可修改范围

- 可修改角色设定
- 可修改平台约束
- 可修改任务优先级逻辑
- 可修改领域分析方式
- 不可删除或重命名上述字段

## 二、复盘 Prompt 设计规范

### 1. 输入变量

复盘 Prompt 必须基于以下三个输入变量：

- `{current_task_json}`
- `{current_run_log}`
- `{past_3_runs_logs}`

### 2. 输出结构

复盘 Prompt 必须输出一个 JSON 对象，顶层字段必须包含：

- `batch_seq`
- `goal_web`
- `core_goal`
- `workflow_status`
- `core_flow`
- `retrospective_context`
- `next_batch_guidance`
- `carry_over_tasks`

`retrospective_context` 必须包含：

- `failed_tasks_summary`
- `historical_patterns`
- `lessons_learned`

`next_batch_guidance` 必须包含：

- `task_breakdown_advice`
- `development_constraints`
- `avoid_pitfalls`
- `blacklist`

`carry_over_tasks` 每个元素必须包含：

- `original_task_id`
- `adjustment_strategy`

### 3. 默认与约束

- `goal_web` 必须透传
- `core_flow` 必须透传；无值时写 `null`
- `workflow_status` 只能使用工作流允许的状态值
- 输出必须是严格 JSON，不得附加解释文本

### 4. 可修改范围

- 可修改角色设定
- 可修改分析维度
- 可修改死循环识别逻辑
- 不可删除或重命名上述字段

## 三、Prompt 生产强制流程

1. 先使用 `references/prompts/meta_prompt.md`
2. 再按本文件校验输入字段和输出结构
3. 写入 `references/prompts/`
4. 最后登记到 `references/prompts/prompt_registry.md`

## 四、上线前检查

- [ ] 已通过 `meta_prompt.md` 生成 Prompt 正文
- [ ] 已按本文件核对输入字段
- [ ] 已按本文件核对输出字段
- [ ] 已确认通用 Prompt 可作为 fallback
- [ ] 已在 `prompt_registry.md` 完成注册
