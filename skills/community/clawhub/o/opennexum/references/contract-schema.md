# Contract Schema Reference

本文档以 `packages/core/src/types.ts` 和 `packages/core/src/contract.ts` 为准。

## Overview

Contract 是任务静态语义的单一事实来源。运行时不会要求手工维护第二份静态登记表；`nexum sync` 会把 contract 同步到 `nexum/active-tasks.json`。

## Required Fields

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | string | Yes | 唯一任务 ID |
| `name` | string | Yes | 人类可读任务名 |
| `type` | `coding | task` | No | 默认 `coding` |
| `scope` | object | Yes | 文件范围、边界、冲突声明 |
| `deliverables` | array | Yes | 交付物列表 |
| `eval_strategy` | object | Yes | 评审策略和 criteria |
| `generator` / `agent.generator` | string | Yes | generator 逻辑 agent |
| `evaluator` / `agent.evaluator` | string | Yes | evaluator 逻辑 agent |
| `max_iterations` | number | Yes | fail 后最多重试次数 |
| `depends_on` | string[] | No | 上游依赖，默认 `[]` |

## Optional Fields

| Field | Type | Notes |
| --- | --- | --- |
| `created_at` | string | ISO 时间戳元数据 |
| `batch` | string | 批次名 |
| `description` | string | 任务补充说明 |

## `scope`

```yaml
scope:
  files:
    - src/feature.ts
  boundaries:
    - packages/core/
  conflicts_with:
    - TASK-002
```

- `files`: 本任务应直接修改或交付的文件
- `boundaries`: 明确禁止扩散的区域
- `conflicts_with`: 与当前任务互斥的 task ID

`conflicts_with` 不是注释字段。它会进入 spawn payload 的 `constraints.conflictsWith`，并且 `runSpawn()` 会拒绝与活跃冲突任务并发执行。

## `deliverables`

推荐对象数组：

```yaml
deliverables:
  - path: src/feature.ts
    description: "Feature implementation"
```

兼容旧格式：

```yaml
deliverables:
  - "src/feature.ts: Feature implementation"
```

字符串会被归一化成 `{ description: "<string>" }`。

## `eval_strategy`

```yaml
eval_strategy:
  type: review
  criteria:
    - id: C1
      desc: "feature works as contracted"
      method: review
      threshold: pass
      weight: 2
```

### `type`

允许值：

- `unit`
- `integration`
- `review`
- `e2e`
- `composite`

### `criteria`

每项字段：

| Field | Type | Required |
| --- | --- | --- |
| `id` | string | Yes |
| `desc` | string | Yes |
| `method` | string | No |
| `threshold` | string | No |
| `weight` | number | No |

## `generator` / `evaluator`

两种写法都支持：

```yaml
generator: codex-gen-01
evaluator: claude-eval-01
```

或者：

```yaml
agent:
  generator: codex-gen-01
  evaluator: claude-eval-01
```

运行时会优先读 `agent.*`，再回退到顶层字段。

## `max_iterations`

`nexum complete` 的语义：

- `pass`: 进入 `done`
- `fail` 且未到上限: 进入 retry，状态回到 `pending`
- `fail` 且达到上限: 进入 `escalated`
- `escalated`: 直接进入 `escalated`

当前系统不再把“超限失败”写成 `failed`；需要人工介入时统一用 `escalated`。

## `depends_on`

`depends_on` 会同时影响两层：

- `nexum sync`: 依赖未满足时注册为 `blocked`
- `spawn payload`: 输出到 `constraints.dependsOn`

因此它是调度真相，不只是文档备注。

## Example

```yaml
id: TASK-001
name: "implement feature X"
type: coding
created_at: "2026-03-31T00:00:00Z"
batch: batch-1

agent:
  generator: auto
  evaluator: auto

scope:
  files:
    - src/feature.ts
    - src/feature.test.ts
  boundaries: []
  conflicts_with: []

deliverables:
  - path: src/feature.ts
    description: "feature implementation"

eval_strategy:
  type: review
  criteria:
    - id: C1
      desc: "feature works as contracted"
      method: review
      threshold: pass

max_iterations: 3
depends_on: []
```

## Authoring Notes

- `scope.files` 要窄，不要偷懒写整个目录
- `depends_on` 和 `conflicts_with` 要按调度约束写，而不是按“可能相关”写
- 逻辑 agent 建议使用标准前缀 `codex-*` / `claude-*`
- 如果用了自定义逻辑 agent，必须在 `nexum/config.json` 里显式配置
