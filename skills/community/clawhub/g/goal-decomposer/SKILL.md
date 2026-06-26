---
name: goal-decomposer
version: "1.0.0"
description: |
  将高层自然语言目标拆解为可执行的多层级任务列表。
  触发场景：用户给出模糊目标需要具体执行步骤、复杂任务需要拆解、需要生成任务树。
metadata:
  author: 筱龙虾
  created: 2026-04-25
---

# Goal Decomposer Skill

## 核心能力

将用户自然语言描述的目标，自动拆解为结构化的任务树：

```
用户目标："我想做个产品调研"
    ↓
任务树：
├─ Task 1: 确定调研范围
│  ├─ 1.1 明确产品类别
│  └─ 1.2 确定目标市场
├─ Task 2: 收集数据
│  ├─ 2.1 搜索竞品信息
│  └─ 2.2 整理市场数据
└─ Task 3: 生成报告
   ├─ 3.1 分析优劣势
   └─ 3.2 输出结论
```

## 设计原则

1. **MECE原则**：任务互斥完全穷尽
2. **可执行性**：每个子任务可独立执行
3. **层级清晰**：不超过3层深度
4. **优先级排序**：标注P0/P1/P2

## 输入格式

```json
{
  "goal": "用户自然语言目标",
  "context": "背景信息（可选）",
  "constraints": ["约束条件（可选）"]
}
```

## 输出格式

```json
{
  "root_goal": "原目标",
  "tasks": [
    {
      "id": "T1",
      "title": "任务标题",
      "priority": "P0",
      "children": [
        {"id": "T1.1", "title": "子任务", "priority": "P0"}
      ],
      "spawn_hint": "建议spawn方式（可选）"
    }
  ],
  "execution_order": ["T1", "T2", "T3"]
}
```

## 使用方式

```python
# 方式1：直接调用
import json
result = decompose_goal("做个产品调研")

# 方式2：通过sessions_spawn
sessions_spawn(agentId="goal-decomposer", task="拆解目标：做个产品调研")
```

## 与现有能力集成

| 能力 | 集成方式 |
|------|----------|
| RESOLVER | 任务生成后路由到对应skill |
| sessions_spawn | 子任务可独立spawn执行 |
| AUTO-FIX | 拆解失败触发修复 |
| web-access | 调研类任务联网获取数据 |

## 实现脚本

见 `scripts/decompose.py`


---
## ⚠️ 常见坑

| 症状 | 原因 | 解决办法 |
|------|------|----------|
| 拆解层级不清 | 目标表述模糊 | 明确"做什么+为什么做" |
| 任务过于碎片 | 缺少MECE检查 | 启用MECE验证开关 |
| 依赖关系缺失 | 未标注前提任务 | 检查是否需要前置条件 |
| 执行顺序混乱 | 依赖标注遗漏 | 补充"depends_on"字段 |
