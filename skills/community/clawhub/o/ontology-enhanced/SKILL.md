---
name: ontology-causal-enhanced
description: 结构化知识图谱 + 因果推理系统。整合 oswalpalash/ontology 和 oswalpalash/causal-inference。
---

# Ontology + Causal Enhanced

整合版：知识图谱 + 因果推理 + Markdown 输出

基于：
- https://clawhub.ai/oswalpalash/ontology
- https://clawhub.ai/oswalpalash/causal-inference

## 组件

1. **ontology-md** - 知识图谱（实体+关系+约束验证）
2. **causal-md** - 因果推理（动作记录+效果估算+历史回填）

## 触发词

| 组件 | 触发词 |
|------|--------|
| ontology | "记住", "what do I know", "link X to Y", "show dependencies" |
| causal | "记录动作", "做了什么", "why failed", "预测效果" |

## Ontology 功能

### 核心类型
- Person, Organization
- Project, Task, Goal
- Event, Location
- Document, Message, Note
- Account, Device, Credential

### 使用
```bash
# 创建实体
python3 skills/ontology-md/scripts/ontology.py create --type Person --props '{"name":"Alice"}'

# 查询
python3 skills/ontology-md/scripts/ontology.py query --type Task --where '{"status":"open"}'

# 关联
python3 skills/ontology-md/scripts/ontology.py relate --from proj_001 --rel has_task --to task_001

# 验证
python3 skills/ontology-md/scripts/ontology.py validate
```

## Causal 功能

### 使用
```bash
# 记录动作
python3 skills/causal-md/scripts/log_action.py --action send_email --outcome reply_received

# 估算效果
python3 skills/causal-md/scripts/estimate_effect.py --action send_email --context '{"time":"morning"}'

# 回填历史
python3 skills/causal-md/scripts/backfill_email.py /path/to/email.json
```

## 数据目录
```
memory/
├── ontology/
│   ├── graph.jsonl    # 实体+关系
│   ├── schema.yaml    # 约束定义
│   └── entities.md    # 导出（兼容 memory_search）
└── causal/
    └── actions.jsonl  # 动作日志
```
