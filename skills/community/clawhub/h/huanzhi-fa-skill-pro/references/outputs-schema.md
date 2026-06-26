# 输出格式 JSON Schema

## 融资诊断输出

```json
{
  "version": "2.8.0",
  "score": 62,
  "grade": "B",
  "summary": "建议补强后启动融资",
  "dimensions": {
    "traction": {"score": 8, "max": 15, "rating": "warning"},
    "market": {"score": 12, "max": 15, "rating": "good"},
    "team": {"score": 4, "max": 10, "rating": "weak"},
    "product": {"score": 10, "max": 15, "rating": "good"},
    "story": {"score": 6, "max": 10, "rating": "warning"},
    "unit_economics": {"score": 7, "max": 10, "rating": "warning"},
    "use_of_funds": {"score": 5, "max": 10, "rating": "weak"},
    "timing": {"score": 6, "max": 10, "rating": "warning"}
  },
  "weakness": ["team", "use_of_funds"],
  "suggestions": ["招聘CTO", "明确资金规划"]
}
```

## 条款分析输出

```json
{
  "clause": "Liquidation Preference",
  "verdict": "red_flag",
  "risk": "high",
  "reason": "2x高于行业标准，严重稀释创始人收益",
  "suggestion": "谈判降至1x non-participating",
  "fallback": "若对方不让步，做好放弃准备"
}
```

## 核心约束

- 输出必须通过 `validate_output()` 自检
- 失败则重试 1 次
- 仍失败走 Failure 路径
