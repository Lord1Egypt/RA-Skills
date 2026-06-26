# 合规检查引擎

**版本**: v1.0  
**功能**: 检查金融行业合规要求覆盖情况

---

## 📋 合规检查点清单

### 通用检查点（所有产品）

| ID | 检查点 | 检查内容 | 监管依据 |
|----|--------|---------|---------|
| CC002 | 风险匹配原则 | 是否有风险匹配说明 | 《适当性管理办法》 |
| CC003 | 信息披露 | 是否有信息披露机制 | 《信息披露管理办法》 |
| CC006 | 风险揭示书 | 是否有完整风险揭示 | 《风险揭示书内容与格式指引》 |
| CC010 | 净值化管理 | 是否说明净值化管理 | 《资管新规》 |
| CC015 | 适当性管理 | 是否有适当性管理说明 | 《适当性管理办法》 |

### 私募基金/信托

| ID | 检查点 | 检查内容 | 监管依据 |
|----|--------|---------|---------|
| CC001 | 合格投资者认定 | 是否有合格投资者认定流程 | 《私募投资基金监督管理暂行办法》 |
| CC005 | 冷静期制度 | 是否有冷静期说明 | 《私募投资基金募集行为管理办法》 |
| CC007 | 回访确认 | 是否有回访确认机制 | 《私募投资基金募集行为管理办法》 |

### 开放式基金

| ID | 检查点 | 检查内容 | 监管依据 |
|----|--------|---------|---------|
| CC012 | 巨额赎回管理 | 是否有巨额赎回条款 | 《公开募集证券投资基金运作管理办法》 |
| CC013 | 暂停赎回 | 是否有暂停赎回说明 | 《公开募集证券投资基金运作管理办法》 |

---

## 🔧 检查逻辑

```python
def check_compliance(document_content, product_type='fund'):
    """
    检查合规要求覆盖情况
    
    参数:
        document_content: PRD 文档内容
        product_type: 产品类型 (fund/private/trust)
    
    返回:
        {
            "score": 90,
            "applicable_checks": 10,
            "passed_checks": 9,
            "failed_checks": [
                {
                    "id": "CC001",
                    "name": "合格投资者认定",
                    "severity": "high",
                    "reason": "未找到合格投资者认定流程",
                    "regulation": "《私募投资基金监督管理暂行办法》"
                }
            ],
            "suggestions": []
        }
    """
    
    # 1. 确定适用检查点
    applicable = get_applicable_checks(product_type)
    
    # 2. 逐个检查
    failed = []
    for check in applicable:
        result = check_single(document_content, check)
        if not result['passed']:
            failed.append(result)
    
    # 3. 计算得分
    score = calculate_score(applicable, failed)
    
    return {
        "score": score,
        "applicable_checks": len(applicable),
        "passed_checks": len(applicable) - len(failed),
        "failed_checks": failed,
        "suggestions": generate_suggestions(failed)
    }
```

---

## 📊 评分规则

| 缺失检查点 | 严重程度 | 扣分 | 示例 |
|-----------|---------|------|------|
| P0 级检查点 | 高 | -10 分/个 | CC001 合格投资者认定 |
| P1 级检查点 | 中 | -5 分/个 | CC007 回访确认 |

**基础分**: 100 分  
**最低分**: 0 分

---

## 📝 输出格式

```json
{
  "check_type": "compliance",
  "score": 80,
  "status": "warning",
  "product_type": "private_fund",
  "applicable_checks": 10,
  "passed_checks": 8,
  "failed_checks": [
    {
      "id": "CC001",
      "name": "合格投资者认定",
      "severity": "high",
      "description": "未找到合格投资者认定流程",
      "location": "未找到相关章节",
      "regulation": "《私募投资基金监督管理暂行办法》第 12 条",
      "requirement": "应当穿透核查最终投资者是否为合格投资者",
      "suggestion": "补充合格投资者认定流程，包括资产证明、风险识别能力评估等",
      "template": "## 合格投资者认定\\n\\n1. 资产证明：...\\n2. 风险识别能力：...\\n3. 最低投资额：..."
    }
  ],
  "summary": {
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

---

## 🎯 检查规则

### CC001 合格投资者认定

**检查关键词**:
```python
KEYWORDS = [
    "合格投资者",
    "资产证明",
    "金融资产",
    "年收入",
    "最低投资额",
    "风险识别能力"
]
```

**必需内容**:
- 资产证明要求（金融资产/收入）
- 风险识别能力评估
- 最低投资金额（≥100 万）

---

### CC006 风险揭示书

**检查关键词**:
```python
KEYWORDS = [
    "风险揭示",
    "市场风险",
    "信用风险",
    "流动性风险",
    "最不利情形"
]
```

**必需内容**:
- 至少 5 类风险揭示
- 最不利投资情形说明
- 风险等级标识

---

## ✅ 验收标准

| 测试场景 | 预期结果 | 实际结果 |
|---------|---------|---------|
| 完整合规 PRD | 得分 100，覆盖所有适用检查点 | ⏳ 待测试 |
| 缺失 1 个 P0 检查点 | 得分 90，提示高风险 | ⏳ 待测试 |
| 缺失 2+ 个 P0 检查点 | 得分<80，警告 | ⏳ 待测试 |

---

*合规检查引擎 v1.0*
