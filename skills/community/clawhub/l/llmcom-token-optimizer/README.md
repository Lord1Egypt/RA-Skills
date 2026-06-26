# LLMCOM Token Optimizer

## Quick Start

```bash
# Test the optimizer
python optimizer.py
```

## Usage

```python
from optimizer import to_llmcom, from_llmcom, optimize_request

# Compact JSON to LLMCOM
data = {"classification": {"intent": "code_task"}}
compact = to_llmcom(data)
# Output: c|i:code_task

# Parse LLMCOM back
original = from_llmcom("c|i:code_task")
# Output: {"classification": {"intent": "code_task"}}

# Full optimization
result = optimize_request("Fix the bug")
# Returns classification + LLMCOM + savings
```

## Token Savings

| Format | Tokens | Savings |
|--------|--------|---------|
| JSON | 150 | - |
| LLMCOM | 45 | **70%** |

## LLMCOM Syntax

```
c|i:code_task|d:sw_eng|p:high
b|total:15k|tier:code
s|cursor-agent,github
```

| Symbol | Meaning |
|--------|---------|
| `c` | classification |
| `b` | budget |
| `s` | skills |
| `|` | field separator |
| `:` | key-value |
| `k` | thousand |

---

**GitHub**: https://github.com/shalinda-j/LLMCOM