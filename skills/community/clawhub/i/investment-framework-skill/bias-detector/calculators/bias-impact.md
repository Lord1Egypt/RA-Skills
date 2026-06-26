# 认知偏差影响计算

> 基于偏差数量和严重程度评估决策风险

---

## 核心公式

### 偏差评分
```
偏差评分 = Σ(偏差数量 × 严重程度 × 风险权重)

严重程度：
- 高：3 分
- 中：2 分
- 低：1 分

风险权重：
- 损失厌恶：1.5
- 确认偏误：1.5
- 过度自信：1.6
- 从众心理：1.4
- 处置效应：1.3
- 锚定效应：1.2
- 代表性偏差：1.2
- 可得性偏差：1.1
```

### 风险等级
```
偏差百分比 = 偏差评分 / 最大可能评分 × 100%

风险等级：
- ≥60%：高风险 → 建议暂停决策，深入反思
- 30-60%：中风险 → 需要警惕，使用清单检查
- <30%：低风险 → 决策较客观，保持警惕
```

---

## 计算示例

### 示例 1：高风险决策

**检测到的偏差**：
- 损失厌恶（高）
- 确认偏误（高）
- 过度自信（中）
- 从众心理（中）

**计算**：
```
损失厌恶：3 × 1.5 = 4.5
确认偏误：3 × 1.5 = 4.5
过度自信：2 × 1.6 = 3.2
从众心理：2 × 1.4 = 2.8

总分：15.0
最大分：(3×1.5 + 3×1.5 + 3×1.6 + 3×1.4) = 18.0

百分比：15.0 / 18.0 = 83.3%
风险等级：高风险
建议：暂停决策，深入反思偏差
```

---

### 示例 2：中风险决策

**检测到的偏差**：
- 锚定效应（中）
- 可得性偏差（低）

**计算**：
```
锚定效应：2 × 1.2 = 2.4
可得性偏差：1 × 1.1 = 1.1

总分：3.5
最大分：(3×1.2 + 3×1.1) = 6.9

百分比：3.5 / 6.9 = 50.7%
风险等级：中风险
建议：需要警惕，使用清单检查
```

---

### 示例 3：低风险决策

**检测到的偏差**：
- 代表性偏差（低）

**计算**：
```
代表性偏差：1 × 1.2 = 1.2

总分：1.2
最大分：3×1.2 = 3.6

百分比：1.2 / 3.6 = 33.3%
风险等级：低风险
建议：决策较客观，保持警惕
```

---

## Python 计算脚本

```python
def calculate_bias_impact(biases, severities):
    """
    计算偏差影响
    
    Args:
        biases: list, 偏差列表
        severities: list, 严重程度列表
    
    Returns:
        dict: 评分结果
    """
    weights = {
        'loss_aversion': 1.5,
        'confirmation': 1.5,
        'overconfidence': 1.6,
        'herding': 1.4,
        'disposition': 1.3,
        'anchoring': 1.2,
        'representativeness': 1.2,
        'availability': 1.1
    }
    
    severity_map = {'high': 3, 'medium': 2, 'low': 1}
    
    total_score = 0
    max_score = 0
    
    for bias, severity in zip(biases, severities):
        weight = weights.get(bias, 1.0)
        score = severity_map.get(severity, 1) * weight
        total_score += score
        max_score += 3 * weight
    
    percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    if percentage >= 60:
        risk_level = '高'
        recommendation = '建议暂停决策，深入反思偏差'
    elif percentage >= 30:
        risk_level = '中'
        recommendation = '需要警惕偏差影响，使用清单检查'
    else:
        risk_level = '低'
        recommendation = '决策较客观，保持警惕'
    
    return {
        'total_score': round(total_score, 2),
        'max_score': round(max_score, 2),
        'percentage': round(percentage, 1),
        'risk_level': risk_level,
        'recommendation': recommendation
    }
```

---

## Excel 公式

### 偏差评分
```excel
=SUMPRODUCT(偏差数量单元格，严重程度单元格，风险权重单元格)
```

### 风险等级
```excel
=IF(偏差百分比>=60%, "高", IF(偏差百分比>=30%, "中", "低"))
```

---

## 使用建议

1. **每次决策前检查**：识别存在的偏差
2. **评分后行动**：
   - 高风险：暂停决策，找人讨论
   - 中风险：使用清单强制检查
   - 低风险：继续但保持警惕
3. **持续练习**：形成习惯，减少偏差

---

*认知偏差是投资的最大敌人。承认偏差，持续检查，理性决策。*
