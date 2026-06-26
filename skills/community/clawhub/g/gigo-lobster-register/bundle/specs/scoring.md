# 评分聚合

## 题目分

```python
task_score = sum(ev.score * ev.weight for ev in task.evaluators)
# ev.score 来自 check.py（pytest/state_hash/trace/rule）或 /judge（llm_judge）
```

## 维度分

每题对维度的贡献：

```python
def task_contrib(task, dim):
    if dim == task.dimensions.primary:
        return (task_score, 1.0)
    if dim in task.dimensions.secondary:
        return (task_score * 0.65, 0.65)
    return None
```

聚合：

```python
def dimension_score(dim):
    contribs = [task_contrib(t, dim) for t in completed_tasks]
    contribs = [c for c in contribs if c]
    if not contribs:
        return None  # N/A
    weighted_sum = sum(s for s, w in contribs)
    weight_sum   = sum(w for s, w in contribs)
    return clamp(0, 100, weighted_sum / weight_sum)
```

## cost / speed 全局

```python
total_tokens = sum(t.tokens.prompt + t.tokens.completion for t in completed_tasks)
total_ms     = sum(t.elapsed_ms for t in completed_tasks)

# v2.0 经验值，第一批 10 次评测后校准
BASELINE_TOKENS = 30000
SCALE_TOKENS    = 50000
BASELINE_MS     = 600000      # 10 分钟
SCALE_MS        = 1800000     # 30 分钟

cost_score  = clamp(0, 100, 100 - (total_tokens - BASELINE_TOKENS) / SCALE_TOKENS * 100)
speed_score = clamp(0, 100, 100 - (total_ms     - BASELINE_MS)     / SCALE_MS     * 100)
```

## 总分

```python
DIM_WEIGHT = {
    "meat": 0.30, "brain": 0.20, "claw": 0.15, "shell": 0.15,
    "soul": 0.10, "cost": 0.05, "speed": 0.05,
}

total_score = sum(dim_score[d] * DIM_WEIGHT[d] for d in DIM_WEIGHT if dim_score[d] is not None)
# 若某维度 N/A（如业务 agent 跳过 Track A），权重重新归一化
```

## tier 映射（沿用 v1 tasting_config.json）

| min | max | tier |
|---|---|---|
| 0 | 30 | street_stall |
| 31 | 45 | night_market |
| 46 | 55 | restaurant |
| 56 | 65 | star_grade |
| 66 | 75 | michelin |
| 76 | 84 | royal |
| 85 | 91 | legendary |
| 92 | 100 | god_tier |
