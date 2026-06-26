---
name: planning-validator-zh
description: |
  计划验证器 — 在执行前验证代理计划，防止虚假计划失败。
  使用场景：(1) 验证多步计划，(2) 检查工具可用性，(3) 验证权限和依赖，(4) 确保计划执行前的可行性。
triggers:
  - "计划验证"
  - "计划检查"
  - "虚假计划"
  - "计划可行性"
  - "执行前检查"
author: "Axioma Cluster"
date: "2026-05-17"
version: 1.0.0
tags:
  - 计划
  - 验证
  - 代理安全
  - 执行前
  - 虚假预防
status: "active"
---

# 计划验证器

在执行前验证代理计划，防止因对能力的不切实际假设而导致的失败。

## 问题：虚假计划

```
症状：
├── 理论上完美的计划
├── 假设可以访问未经验证的工具/API
├── 执行时失败（无回退）
├── 多代理未协调
└── 执行前无验证
```

## 解决方案

### 1. 多代理验证器

```python
class PlanningValidator:
    validation_steps = [
        '检查工具可用性',
        '检查权限', 
        '检查依赖',
        '验证可行性',
        '确认用户'
    ]
    
    def validate_plan(plan):
        for step in validation_steps:
            if not check(step, plan):
                return {'valid': False, 'failed_at': step}
        return {'valid': True}
```

### 2. 明确的工具模式

```python
tool_schemas = {
    'telegram_send': {
        'capabilities': ['send_text', 'send_audio', 'send_document'],
        'limitations': ['no_video_call', 'max_10MB'],
        'required_auth': ['bot_token']
    },
    'qdrant_query': {
        'capabilities': ['search', 'insert', 'delete'],
        'limitations': ['no_update'],
        'required_auth': ['qdrant_key']
    }
}

def verify_tool_capabilities(tool, required_action):
    if required_action not in tool_schemas[tool]['capabilities']:
        return False
    return True
```

### 3. 约束验证

```python
def verify_constraints(plan):
    constraints = {
        '时间限制': 300,  # 最多5分钟
        '重试限制': 3,
        '最大API调用': 50,
        '内存限制_MB': 4096
    }
    
    for constraint, limit in constraints.items():
        if plan.exceeds(constraint, limit):
            return False
    return True
```

### 4. 假设前澄清

```python
def ask_for_clarification(unclear_point):
    """不假设，而是询问用户"""
    message = f"我不确定: {unclear_point}。 "
    message += "你能在继续之前澄清吗？"
    send_to_user(message)
    wait_for_response()
```

## 看门狗

| 看门狗 | 角色 | 阈值 |
|--------|------|------|
| **ICS** | 计划完整性 | >0.800 = 停止 |
| **CLW** | 经验教训 | 见过模式 = 警告 |
| **STC** | 紧张度 | >0.500 = 警告 |

## 使用方法

```python
from planning_validator import PlanningValidator

validator = PlanningValidator()

# 在执行计划之前
plan = create_plan(objective)

validation = validator.validate_plan(plan)
if not validation['valid']:
    failed_at = validation['failed_at']
    ask_for_clarification(f"计划在 {failed_at} 失败")
else:
    execute_plan(plan)
```

## 检查清单

- [x] 步骤之间的多代理验证器
- [x] 明确的工具模式（能力 + 限制）
- [x] 约束验证
- [x] 假设前澄清
- [x] ICS 看门狗加强
- [x] CLW 看门狗（模式检测）
- [x] 复杂计划需要用户审批

## 文件结构

```
planning-validator/
├── SKILL.md
├── scripts/
│   ├── planning_validator.py
│   ├── utils.py
│   └── main.py
├── data/
├── models/
└── tests/
```