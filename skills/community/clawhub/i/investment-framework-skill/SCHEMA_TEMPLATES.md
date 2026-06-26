# 技能 Schema 模板库 📐

**用途**：为各技能提供标准化输出 Schema 模板，快速适配 OUTPUT_SCHEMA.md

---

## moat-evaluator 模板

```json
{
  "signal": {
    "summary": "护城河评估结论（≤50 字）",
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "score": 0-100,
    "moat_level": "强 | 中 | 弱 | 无"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_quality": "数据质量说明",
    "limitations": ["护城河评估主观性较强", "行业变化可能影响护城河持续性"]
  },
  "reasoning": {
    "key_findings": ["护城河类型 1+ 强度", "护城河类型 2+ 强度", "趋势判断"],
    "analysis": [
      {
        "dimension": "护城河类型（品牌/网络效应/转换成本/规模/特许）",
        "finding": "评分（0-5）",
        "evidence": "具体证据",
        "impact": "高 | 中 | 低"
      }
    ],
    "moat_types": {
      "brand": { "score": 0-5, "max": 5, "evidence": "证据" },
      "network_effect": { "score": 0-5, "max": 5, "evidence": "证据" },
      "switching_cost": { "score": 0-5, "max": 5, "evidence": "证据" },
      "scale_advantage": { "score": 0-5, "max": 5, "evidence": "证据" },
      "franchise": { "score": 0-5, "max": 5, "evidence": "证据" }
    },
    "moat_trend": "增强 | 稳定 | 减弱",
    "assumptions": ["假设 1", "假设 2"],
    "risks": ["护城河被侵蚀风险", "技术颠覆风险"]
  },
  "metrics": {
    "moat_score": {
      "total": 0-25,
      "max": 25,
      "level": "强 | 中 | 弱"
    },
    "moat_types": {
      "brand": { "score": 0-5, "max": 5 },
      "network_effect": { "score": 0-5, "max": 5 },
      "switching_cost": { "score": 0-5, "max": 5 },
      "scale_advantage": { "score": 0-5, "max": 5 },
      "franchise": { "score": 0-5, "max": 5 }
    }
  },
  "sources": [{ "name": "数据源", "type": "官方 | 媒体 | 第三方", "reliability": "S|A|B|C" }],
  "action_items": [{ "priority": "高 | 中 | 低", "action": "行动", "timeline": "时间", "success_criteria": "标准" }],
  "next_steps": ["使用 value-analyzer 评估价值", "使用 intrinsic-value-calculator 计算内在价值"],
  "related_skills": ["value-analyzer", "intrinsic-value-calculator", "market-patent-evaluator"],
  "disclaimer": "⚠️ 市场有风险，投资需谨慎。",
  "metadata": { "skill_name": "moat-evaluator", "skill_version": "4.0.0", "generated_at": "ISO8601", "data_as_of": "ISO8601", "cache_status": "fresh|cached" }
}
```

---

## intrinsic-value-calculator 模板

```json
{
  "signal": {
    "summary": "内在价值和安全边际结论（≤50 字）",
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "score": 0-100,
    "margin_of_safety": "安全边际%"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_quality": "数据质量说明",
    "limitations": ["DCF 模型依赖假设", "预测存在不确定性"]
  },
  "reasoning": {
    "key_findings": ["DCF 估值结果", "相对估值结果", "安全边际判断"],
    "analysis": [
      {
        "dimension": "估值方法（DCF/PE/PB/股息折现）",
        "finding": "估值结果",
        "evidence": "关键假设（增长率/折现率/终值）",
        "impact": "高 | 中 | 低"
      }
    ],
    "valuation_methods": {
      "dcf": { "value": 数值，"assumptions": "假设说明" },
      "pe_relative": { "value": 数值，"assumptions": "假设说明" },
      "pb_relative": { "value": 数值，"assumptions": "假设说明" },
      "dividend_discount": { "value": 数值，"assumptions": "假设说明" }
    },
    "assumptions": ["增长率假设", "折现率假设", "终值假设"],
    "risks": ["假设过于乐观风险", "宏观环境变化风险"]
  },
  "metrics": {
    "valuation_summary": {
      "dcf_value": { "value": 数值，"unit": "元" },
      "pe_relative_value": { "value": 数值，"unit": "元" },
      "pb_relative_value": { "value": 数值，"unit": "元" },
      "average_intrinsic_value": { "value": 数值，"unit": "元" },
      "current_price": { "value": 数值，"unit": "元" },
      "margin_of_safety": { "value": 数值，"unit": "%" }
    }
  },
  "sources": [{ "name": "数据源", "type": "官方 | 媒体 | 第三方", "reliability": "S|A|B|C" }],
  "action_items": [{ "priority": "高 | 中 | 低", "action": "行动", "timeline": "时间", "success_criteria": "标准" }],
  "next_steps": ["使用 decision-checklist 进行最终决策检查", "使用 risk-assessor 评估下行风险"],
  "related_skills": ["value-analyzer", "moat-evaluator", "risk-assessor"],
  "disclaimer": "⚠️ 市场有风险，投资需谨慎。",
  "metadata": { "skill_name": "intrinsic-value-calculator", "skill_version": "4.0.0", "generated_at": "ISO8601", "data_as_of": "ISO8601", "cache_status": "fresh|cached" }
}
```

---

## decision-checklist 模板

```json
{
  "signal": {
    "summary": "决策逻辑检查结论（≤50 字）",
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "score": 0-100,
    "logic_quality": "强 | 中 | 弱"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_quality": "数据质量说明",
    "limitations": ["认知偏差识别主观性", "无法覆盖所有偏差"]
  },
  "reasoning": {
    "key_findings": ["能力圈评估结果", "认知偏差检查结果", "逻辑完整性评估"],
    "analysis": [
      {
        "dimension": "检查维度（能力圈/认知偏差/逻辑完整性）",
        "finding": "评分/结果",
        "evidence": "具体检查项",
        "impact": "高 | 中 | 低"
      }
    ],
    "capability_circle": {
      "score": 0-20,
      "assessment": "能力圈内 | 边界 | 圈外"
    },
    "cognitive_biases": {
      "detected": ["偏差 1", "偏差 2"],
      "severity": "高 | 中 | 低"
    },
    "logic_completeness": {
      "score": 0-5,
      "assessment": "完整 | 基本完整 | 不完整"
    },
    "assumptions": ["假设 1", "假设 2"],
    "risks": ["认知偏差风险", "逻辑漏洞风险"]
  },
  "metrics": {
    "capability_circle_score": 0-20,
    "cognitive_bias_count": 0-8,
    "logic_completeness_score": 0-5,
    "investment_ten_commandments": {
      "violated": ["违反的诫命"],
      "score": 0-10
    }
  },
  "sources": [{ "name": "数据源", "type": "官方 | 媒体 | 第三方", "reliability": "S|A|B|C" }],
  "action_items": [{ "priority": "高 | 中 | 低", "action": "行动", "timeline": "时间", "success_criteria": "标准" }],
  "next_steps": ["若通过检查，执行投资", "若未通过，重新分析"],
  "related_skills": ["value-analyzer", "moat-evaluator", "risk-assessor"],
  "disclaimer": "⚠️ 市场有风险，投资需谨慎。",
  "metadata": { "skill_name": "decision-checklist", "skill_version": "4.0.0", "generated_at": "ISO8601", "data_as_of": "ISO8601", "cache_status": "fresh|cached" }
}
```

---

## asset-allocator 模板

```json
{
  "signal": {
    "summary": "资产配置方案结论（≤50 字）",
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "score": 0-100,
    "allocation_type": "保守 | 平衡 | 积极"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_quality": "数据质量说明",
    "limitations": ["市场预测存在不确定性", "历史数据不代表未来"]
  },
  "reasoning": {
    "key_findings": ["风险承受评估结果", "配置比例建议", "再平衡策略"],
    "analysis": [
      {
        "dimension": "分析维度（年龄/风险偏好/投资目标/约束）",
        "finding": "评估结果",
        "evidence": "具体数据",
        "impact": "高 | 中 | 低"
      }
    ],
    "risk_profile": {
      "risk_tolerance": "低 | 中 | 高",
      "risk_capacity": "低 | 中 | 高",
      "time_horizon": "短期 | 中期 | 长期"
    },
    "assumptions": ["市场长期回报假设", "通胀率假设"],
    "risks": ["市场风险", "利率风险", "通胀风险"]
  },
  "metrics": {
    "allocation": {
      "stocks": { "percentage": 0-100, "sub_allocation": "国内/国际" },
      "bonds": { "percentage": 0-100, "sub_allocation": "国债/企业债" },
      "cash": { "percentage": 0-100 },
      "alternatives": { "percentage": 0-100, "sub_allocation": "黄金/REITs 等" }
    },
    "expected_return": { "value": 数值，"unit": "%" },
    "expected_volatility": { "value": 数值，"unit": "%" }
  },
  "sources": [{ "name": "数据源", "type": "官方 | 媒体 | 第三方", "reliability": "S|A|B|C" }],
  "action_items": [{ "priority": "高 | 中 | 低", "action": "行动", "timeline": "时间", "success_criteria": "标准" }],
  "next_steps": ["使用 value-analyzer 选择具体标的", "定期再平衡"],
  "related_skills": ["value-analyzer", "risk-assessor", "future-forecaster"],
  "disclaimer": "⚠️ 市场有风险，投资需谨慎。",
  "metadata": { "skill_name": "asset-allocator", "skill_version": "4.0.0", "generated_at": "ISO8601", "data_as_of": "ISO8601", "cache_status": "fresh|cached" }
}
```

---

*使用模板快速适配各技能，确保一致性和合规性。*
