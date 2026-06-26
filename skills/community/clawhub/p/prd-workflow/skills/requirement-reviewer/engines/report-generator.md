# 评审报告生成器

**版本**: v1.0  
**功能**: 整合所有检查结果，生成完整评审报告

---

## 🔧 报告生成逻辑

```python
def generate_review_report(document_content, product_type='fund'):
    """
    生成完整评审报告
    
    流程:
    1. 执行完整性检查
    2. 执行一致性检查
    3. 执行合规检查
    4. 执行术语检查
    5. 执行风险检查
    6. 计算总体评分
    7. 生成评审结论
    8. 输出报告
    """
    
    # 1. 执行各项检查
    completeness = check_completeness(document_content)
    consistency = check_consistency(document_content)
    compliance = check_compliance(document_content, product_type)
    terminology = check_terminology(document_content)
    risk = check_risk_disclosure(document_content)
    
    # 2. 计算总体评分
    overall_score = calculate_overall_score([
        completeness, consistency, compliance, terminology, risk
    ])
    
    # 3. 生成评审结论
    conclusion = generate_conclusion(overall_score)
    
    # 4. 生成报告
    report = {
        "document_name": extract_document_name(document_content),
        "review_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "reviewer": "Requirement Reviewer v1.0",
        "product_type": product_type,
        "overall_score": overall_score,
        "conclusion": conclusion,
        "checks": {
            "completeness": completeness,
            "consistency": consistency,
            "compliance": compliance,
            "terminology": terminology,
            "risk": risk
        },
        "summary": generate_summary([
            completeness, consistency, compliance, terminology, risk
        ]),
        "suggestions": generate_all_suggestions([
            completeness, consistency, compliance, terminology, risk
        ])
    }
    
    return report
```

---

## 📊 总体评分计算

```python
def calculate_overall_score(checks):
    """
    计算总体评分
    
    权重:
    - 完整性：30%
    - 一致性：25%
    - 合规性：25%
    - 术语准确性：10%
    - 风险揭示：10%
    """
    
    weights = {
        'completeness': 0.30,
        'consistency': 0.25,
        'compliance': 0.25,
        'terminology': 0.10,
        'risk': 0.10
    }
    
    score = 0
    for check_name, check_result in checks.items():
        score += check_result['score'] * weights[check_name]
    
    return round(score, 1)
```

---

## 🎯 评审结论

```python
def generate_conclusion(score):
    """
    生成评审结论
    
    评分等级:
    - 90-100: 优秀 - 通过，可提交
    - 80-89: 良好 - 需改进，改进后复审
    - 70-79: 合格 - 需改进，改进后复审
    - 60-69: 需改进 - 不通过，需重大修改
    - <60: 不通过 - 不通过，需重大修改
    """
    
    if score >= 90:
        return {
            "level": "优秀",
            "status": "pass",
            "text": "✅ 通过，可提交",
            "color": "green"
        }
    elif score >= 80:
        return {
            "level": "良好",
            "status": "warning",
            "text": "⚠️ 需改进，改进后复审",
            "color": "yellow"
        }
    elif score >= 70:
        return {
            "level": "合格",
            "status": "warning",
            "text": "⚠️ 需改进，改进后复审",
            "color": "orange"
        }
    else:
        return {
            "level": "不通过",
            "status": "fail",
            "text": "❌ 不通过，需重大修改",
            "color": "red"
        }
```

---

## 📝 Markdown 报告模板

```markdown
# PRD 评审报告

**文档名称**: {{document_name}}  
**评审时间**: {{review_time}}  
**评审人**: {{reviewer}}  
**产品类型**: {{product_type}}  

---

## 📊 评审概览

| 指标 | 得分 | 状态 |
|-----|------|------|
| **总体评分** | **{{overall_score}}/100** | {{conclusion.icon}} |
| 完整性 | {{completeness.score}}/100 | {{completeness.status}} |
| 一致性 | {{consistency.score}}/100 | {{consistency.status}} |
| 合规性 | {{compliance.score}}/100 | {{compliance.status}} |
| 术语准确性 | {{terminology.score}}/100 | {{terminology.status}} |
| 风险揭示 | {{risk.score}}/100 | {{risk.status}} |

**评审结论**: {{conclusion.text}}

---

## ✅ 通过项

{% for item in passed_items %}
- [x] {{item}}
{% endfor %}

---

## ⚠️ 待改进项

### 1. 完整性问题

{% for issue in completeness.issues %}
- [ ] **{{issue.description}}**
  - 位置：{{issue.location}}
  - 建议：{{issue.suggestion}}
{% endfor %}

### 2. 一致性问题

{% for issue in consistency.issues %}
- [ ] **{{issue.description}}** ({{issue.severity}})
  - 位置 1: {{issue.location1}} - "{{issue.value1}}"
  - 位置 2: {{issue.location2}} - "{{issue.value2}}"
  - 建议：{{issue.suggestion}}
{% endfor %}

### 3. 合规问题

{% for issue in compliance.failed_checks %}
- [ ] **{{issue.name}}** ({{issue.severity}})
  - 监管依据：{{issue.regulation}}
  - 问题：{{issue.description}}
  - 建议：{{issue.suggestion}}
{% endfor %}

### 4. 术语问题

{% for issue in terminology.issues %}
- [ ] **{{issue.description}}**
  - 错误：{{issue.wrong_term}}
  - 正确：{{issue.correct_term}}
{% endfor %}

### 5. 风险揭示问题

{% for issue in risk.issues %}
- [ ] **{{issue.description}}**
  - 建议：{{issue.suggestion}}
{% endfor %}

---

## 📈 改进建议

### 优先修复（P0）
{% for suggestion in suggestions.p0 %}
1. {{suggestion}}
{% endfor %}

### 建议补充（P1）
{% for suggestion in suggestions.p1 %}
1. {{suggestion}}
{% endfor %}

### 可选优化（P2）
{% for suggestion in suggestions.p2 %}
1. {{suggestion}}
{% endfor %}

---

## 🎯 评审结论

{{conclusion.text}}

{% if conclusion.status == 'warning' %}
**复审要求**: 修复所有 P0 问题后，可申请复审
{% elif conclusion.status == 'fail' %}
**复审要求**: 重大修改后，需重新评审
{% endif %}

---

*评审报告由 Requirement Reviewer v1.0 自动生成*
```

---

## 📋 JSON 输出格式

```json
{
  "document_name": "XX 稳健增长混合型证券投资基金 PRD",
  "review_time": "2026-02-26 22:45:00",
  "reviewer": "Requirement Reviewer v1.0",
  "product_type": "fund",
  "overall_score": 85.5,
  "conclusion": {
    "level": "良好",
    "status": "warning",
    "text": "⚠️ 需改进，改进后复审",
    "color": "yellow"
  },
  "checks": {
    "completeness": {...},
    "consistency": {...},
    "compliance": {...},
    "terminology": {...},
    "risk": {...}
  },
  "summary": {
    "total_issues": 5,
    "high_severity": 1,
    "medium_severity": 2,
    "low_severity": 2
  },
  "suggestions": {
    "p0": ["统一风险等级为 R3"],
    "p1": ["补充数据需求章节", "补充技术风险揭示"],
    "p2": ["优化验收标准格式"]
  }
}
```

---

*评审报告生成器 v1.0*
