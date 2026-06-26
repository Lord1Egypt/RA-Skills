---
slug: llmcom-token-optimizer
name: LLMCOM Token Optimizer
version: 1.0.1
author: shalinda-j
tags: [token-optimization, llmcom, context-management, cost-saving]
description: Token-efficient context format using LLMCOM specification - reduces token usage by 70-80% through compact object notation.
---

# LLMCOM Token Optimizer

> **70-80% Token Savings** using LLMCOM compact format

## What is LLMCOM?

LLMCOM (LLM Compact Object Notation) is a token-efficient format for structured data exchange with LLMs. It replaces verbose JSON with compact notation.

## Token Savings Comparison

### Before (JSON - Verbose)

```json
{
  "classification": {
    "intent": "code_task",
    "domain": "software_engineering",
    "priority": "high"
  },
  "budget": {
    "total": 15000,
    "tier": "code"
  },
  "skills": ["cursor-agent", "github"]
}
```
**~150 tokens**

### After (LLMCOM - Compact)

```
c|i:code_task|d:software_engineering|p:high
b|t:15000|tier:code
s|cursor-agent,github
```
**~45 tokens**

**Savings: 70%**

## Usage

### Format Data

```python
from optimizer import to_llmcom, from_llmcom

# Convert JSON to LLMCOM
data = {"classification": {"intent": "code_task"}}
compact = to_llmcom(data)  # c|i:code_task

# Parse LLMCOM back
original = from_llmcom("c|i:code_task")
```

### CLI Commands

| Command | Purpose |
|---------|---------|
| `/llmcom-pack` | Compress context to LLMCOM |
| `/llmcom-unpack` | Expand LLMCOM to JSON |
| `/llmcom-stats` | Show token savings |

## LLMCOM Syntax

| Symbol | Meaning |
|--------|---------|
| `|` | Field separator |
| `:` | Key-value separator |
| `,` | List separator |
| `c` | Classification block |
| `b` | Budget block |
| `s` | Skills block |

## Examples

### Classification
```
c|i:code_task|d:sw_eng|p:high|conf:0.9
```

### Budget
```
b|total:15k|tier:code|model:med
```

### Skills
```
s|cursor-agent,github,vercel|load:on_demand
```

## Integration

Works with:
- OpenClaw agents
- Claude Code
- Any LLM context

## Source

GitHub: https://github.com/shalinda-j/LLMCOM

---

*Created by Jeni (AGI Agent)*