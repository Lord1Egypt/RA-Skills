# Output Contract

本技能有两类输出。

## A. Need Clarification（继续追问）

用于继续澄清：

```
### 理解确认
[1-3 句话复述理解]

### 还需要你确认这几点
1. [问题一]
2. [问题二]
3. [问题三]

### 当前判断
- 领域：[领域]
- 任务类型：[任务类型]
- 还缺什么：[缺口列表]
```

## B. Approved（放行）

用于交接给下游：

```
### 需求理解
[简明复述用户需求]

### Query Plan
- domain: [领域]
- sub_domain: [子领域]
- task_type: [任务类型]
- target: [目标]
- audience: [受众]
- context: [背景]
- constraints: [约束条件列表]
- output_format: [输出形式]
- professional_level: [专业深度]
- filled_slots: { 已填充槽位 }
- missing_slots: [仍存在的小部分缺口，可接受]

### 专业化提问
[rewritten prompt，可直接交给下游 Agent 或大模型使用]

### Handoff Payload（JSON）
```json
{
  "next_skill": "[下游 skill 名称，若有]",
  "domain": "",
  "task_type": "",
  "output_format": "",
  "constraints": [],
  "rewritten_prompt": ""
}
```
```

## Query Plan 推荐字段

| 字段 | 说明 |
|------|------|
| domain | 领域 |
| sub_domain | 子领域 |
| task_type | 任务类型 |
| target | 目标 |
| audience | 受众 |
| context | 背景 |
| constraints | 约束条件 |
| output_format | 输出形式 |
| professional_level | 专业深度 |
| filled_slots | 已填充的槽位 |
| missing_slots | 仍存在的小缺口 |
