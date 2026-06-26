---
name: health-reasoner
description: "Health Reasoner — 日常习惯健康小工具。基于生活习惯（睡眠/饮食/运动/压力/烟酒）输出评分与改善建议。纯规则驱动，纯 Python 标准库。不提供医疗诊断。"
---

# Health Reasoner (日常习惯健康小工具)

纯规则驱动的日常习惯评分工具。**零外部依赖**。**非医疗用途**。

## Quick Start

```python
from health_reasoner import HealthReasoner

hr = HealthReasoner()
result = hr.assess({
    "age": 28,
    "gender": "male",
    "sleep_hours": 6.5,
    "sleep_quality": "fair",
    "diet_type": "high_fat",
    "exercise_frequency": "weekly",
    "stress_level": "high",
})
print(result.score)
print(result.suggestions)
```

## 特性

- **零外部依赖** — 纯 Python 标准库
- **历史记录可选** — 不传 `--history` 不留痕
- **规则透明** — 每条建议可溯源
