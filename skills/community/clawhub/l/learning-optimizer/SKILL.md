---
name: learning-optimizer
description: Learning optimizer - analyze study patterns, identify inefficiencies, suggest optimizations for better learning outcomes
version: 1.1.0
---

# Learning Optimizer

Analyze and optimize learning patterns for better efficiency.

## Features
- Study pattern analysis
- Efficiency identification
- Time allocation suggestions
- Focus improvement tips

## Input
- Study schedule/history
- Current time allocation
- Distraction factors
- Performance data (optional)

## Output
- Efficiency analysis
- Optimization suggestions
- Time reallocation plan
- Focus improvement tips

## Constraints
- ❌ No performance guarantees
- ❌ No one-size-fits-all solutions
- ❌ No external data collection

## Usage
```bash
python3 scripts/main.py analyze --schedule "每天2小时" --subjects "数学,英语"
python3 scripts/main.py optimize --problem "容易分心" --current "长时间连续学习"
python3 scripts/main.py allocate --total 120 --priorities "数学高,英语中"
python3 scripts/main.py data
```

## Storage

Logs are local-first and stored under `~/.learning-optimizer/` by default.
Set `LEARNING_OPTIMIZER_HOME` for tests, demos, or shared machines:

```bash
LEARNING_OPTIMIZER_HOME=/tmp/learning-demo python3 scripts/main.py analyze --schedule "每天2小时" --subjects "数学,英语"
```

The skill writes JSONL logs:
- `analysis_log.jsonl`
- `optimization_log.jsonl`
- `allocation_log.jsonl`

## Verification

```bash
python3 -m py_compile scripts/main.py scripts/verify.py
python3 scripts/verify.py
```
