# Health Reasoner API 规范

## 核心类：`HealthReasoner`

### `assess(data: dict) -> HealthAssessment`

输入格式（`UserHealthProfile` JSON）：

```json
{
  "age": 28,
  "gender": "male",
  "sleep_hours": 6.5,
  "sleep_quality": "fair",
  "diet_type": "balanced",
  "exercise_frequency": "weekly",
  "stress_level": "moderate",
  "smoking_status": "never",
  "alcohol_use": "light",
  "symptoms": ["偶尔头痛"],
  "medical_history": []
}
```

**字段校验规则：**

| 字段 | 类型 | 允许值 |
|------|------|--------|
| age | int | 0-120 |
| gender | str | male, female |
| sleep_hours | float | 0.0-24.0 |
| sleep_quality | str | good, fair, poor |
| diet_type | str | balanced, high_fat, high_sugar, high_salt, vegetarian |
| exercise_frequency | str | daily, weekly, rarely, sedentary |
| stress_level | str | low, moderate, high |
| smoking_status | str | never, past, current |
| alcohol_use | str | none, light, moderate, heavy |
| symptoms | list[str] | 可选 |
| medical_history | list[str] | 可选 |

### 输出：`HealthAssessment`

```json
{
  "score": 68,
  "risk_level": "medium",
  "suggestions": [
    {"priority": 1, "category": "sleep", "rule_id": "SLEEP-001", "message": "建议将睡眠延长至7-8小时"},
    {"priority": 2, "category": "stress", "rule_id": "STRESS-002", "message": "每天安排15分钟深呼吸练习"}
  ],
  "risk_factors": ["睡眠不足", "高压力"],
  "details": {
    "sleep_score": 60,
    "diet_score": 75,
    "exercise_score": 50,
    "stress_score": 40,
    "substance_score": 85
  }
}
```

**错误码：**

| 错误 | HTTP 等效 | 说明 |
|------|-----------|------|
| ValueError | 400 | 输入校验失败 |
| TypeError | 400 | 字段类型错误 |
| 其他异常 | 500 | 内部错误 |

## 额外函数

### `batch_assess(profiles: List[dict]) -> List[HealthAssessment]`

批量评估多个健康档案。每个元素与 `assess()` 输入格式相同。`assess()` 的调用者负责错误处理。

### `trend_analysis(history: List[dict]) -> TrendReport`

从历史 `UserHealthProfile` 列表（按日期排序）生成趋势分析报告：

```json
{
  "score_trend": "stable",
  "sleep_trend": "improving",
  "changes": [
    {"field": "sleep_hours", "change": "+0.5", "duration": "7d"}
  ]
}
```
