---
name: planning-validator
description: |
  Planning Validator — Validates agent plans before execution to prevent hallucinated planning failures.
  Use when: (1) validating multi-step plans, (2) checking tool availability, (3) verifying permissions
  and dependencies, (4) ensuring plan feasibility before execution.
triggers:
  - "plan validation"
  - "plan verification"
  - "hallucinated planning"
  - "plan feasibility"
  - "pre-execution check"
author: "Axioma Cluster"
date: "2026-05-17"
version: 1.0.0
tags:
  - planning
  - validation
  - agent-safety
  - pre-execution
  - hallucination-prevention
status: "active"
---

# Planning Validator

Validates agent plans before execution to prevent failures from hallucinated assumptions about capabilities.

## Problem: Hallucinated Planning

```
SYMPTOMS:
├── Theoretically perfect plan
├── Assumes access to tools/APIs without verification
├── Fails at execution (no fallback)
├── Multi-agents not coordinated
└── No validation before execution
```

## Solutions Implemented

### 1. Multi-Agent Validator

```python
class PlanningValidator:
    validation_steps = [
        'CHECK_TOOLS_AVAILABLE',
        'CHECK_PERMISSIONS', 
        'CHECK_DEPENDENCIES',
        'VALIDATE_FEASIBILITY',
        'CONFIRM_WITH_USER'
    ]
    
    def validate_plan(plan):
        for step in validation_steps:
            if not check(step, plan):
                return {'valid': False, 'failed_at': step}
        return {'valid': True}
```

### 2. Explicit Tool Schemas

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

### 3. Constraint Verification

```python
def verify_constraints(plan):
    constraints = {
        'TIME_LIMIT': 300,  # 5 min max
        'RETRY_LIMIT': 3,
        'API_CALLS_MAX': 50,
        'MEMORY_LIMIT_MB': 4096
    }
    
    for constraint, limit in constraints.items():
        if plan.exceeds(constraint, limit):
            return False
    return True
```

### 4. Clarification Before Assumption

```python
def ask_for_clarification(unclear_point):
    """Instead of assuming, ask the user"""
    message = f"I'm not certain about: {unclear_point}. "
    message += "Can you clarify before I continue?"
    send_to_user(message)
    wait_for_response()
```

## Watchdogs

| Watchdog | Role | Threshold |
|----------|------|------------|
| **ICS** | Plan integrity | >0.800 = STOP |
| **CLW** | Lessons learned | Pattern seen before = WARNING |
| **STC** | Tension | >0.500 = WARNING |

## Usage

```python
from planning_validator import PlanningValidator

validator = PlanningValidator()

# Before executing a plan
plan = create_plan(objective)

validation = validator.validate_plan(plan)
if not validation['valid']:
    failed_at = validation['failed_at']
    ask_for_clarification(f"Plan failed at: {failed_at}")
else:
    execute_plan(plan)
```

## Checklist

- [x] Multi-agent validator between steps
- [x] Explicit tool schemas (capabilities + limitations)
- [x] Constraint verification
- [x] Clarification before assumptions
- [x] ICS watchdog reinforced
- [x] CLW watchdog (pattern detection)
- [x] User approval for complex plans

## Files

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