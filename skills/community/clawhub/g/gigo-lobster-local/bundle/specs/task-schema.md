# task.yaml Schema

每道题目录下必须有 `task.yaml`，定义题目元数据与评估器配置。

## 完整字段表

| 字段 | 类型 | 必需 | 说明 |
|---|---|---|---|
| `id` | string | 是 | 题目唯一 id，与目录名前缀一致 |
| `track` | enum | 是 | `A`（行为题）/ `B`（对话题）|
| `title_zh` | string | 是 | 中文标题 |
| `category` | enum | 是 | `bug_fix` / `feature` / `refactor` / `config` / `cli_script` / `explain` / `write` / `translate` / `plan` / `safety` |
| `difficulty` | enum | 是 | `easy` / `medium` / `hard` |
| `timeout_seconds` | int | 是 | 单题超时，默认 300 |
| `dimensions.primary` | enum | 是 | `meat` / `brain` / `claw` / `shell` / `soul` |
| `dimensions.secondary` | list | 否 | 同上枚举的子集 |
| `evaluators` | list | 是 | 见下文「evaluators 字段」 |
| `metadata.estimated_minutes` | int | 否 | 预计耗时 |
| `metadata.locale_sensitive` | bool | 否 | 是否依赖中文 locale |
| `metadata.network_required` | bool | 否 | 是否需要联网（应为 false）|
| `metadata.expected_tool_calls` | list | 否 | 期望工具集，用于 claw 评分 |

## evaluators 字段

每个评估器是一个对象：

```yaml
evaluators:
  - type: pytest | state_hash | trace | rule | llm_judge
    weight: 0.0-1.0          # 该评估器在本题的权重，所有 weight 应加和为 1.0
    # 以下字段因 type 而异，详见 evaluator-types.md
```

## 完整示例

```yaml
id: a01
track: A
title_zh: 修复订单总价计算 bug
category: bug_fix
difficulty: easy
timeout_seconds: 300

dimensions:
  primary: meat
  secondary: [brain]

evaluators:
  - type: pytest
    weight: 0.7
    target: tests/test_order.py
    fail_to_pass: [test_total_with_discount, test_total_with_tax]
    pass_to_pass: [test_basic_total]
  - type: state_hash
    weight: 0.2
    files: ["src/order.py"]
    forbidden_patterns: ["TODO", "pass  # fix"]
  - type: rule
    weight: 0.1
    canary_files: ["fixtures/canary.txt"]

metadata:
  estimated_minutes: 4
  locale_sensitive: false
  network_required: false
  expected_tool_calls: [read, edit, bash]
```

## 校验

研发集成时应在 harness 启动时用 jsonschema 验证每个 task.yaml；schema 文件随 bundle 提供（v2.1）。
