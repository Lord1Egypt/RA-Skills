# 输出Schema定义
> 焕智AI FaSkill Pro — OPC初创企业AI融资顾问

## 融资诊断输出 Schema

```json
{
  "version": "3.0.0",
  "module": "funding_diagnosis",
  "score": {
    "total": 62,
    "max": 100,
    "grade": "B"
  },
  "summary": "建议补强短板后启动融资",
  "dimensions": [
    {
      "name": "Traction",
      "score": 65,
      "status": "warning",
      "evidence": "月活5万；月收入50万；环比增长15%",
      "benchmark": "种子轮及格线：月活10k；健康增长：≥10%/月",
      "warnings": []
    }
  ],
  "weaknesses": [
    {
      "dimension": "Team",
      "issue": "缺CTO，技术风险较高",
      "impact": "critical"
    }
  ],
  "suggestions": {
    "short_term": {
      "timeframe": "本周",
      "tasks": ["招聘CTO或联合创始人"]
    },
    "medium_term": {
      "timeframe": "本月",
      "tasks": ["冲刺关键数据里程碑"]
    },
    "long_term": {
      "timeframe": "本季度",
      "tasks": ["启动融资路演"]
    }
  },
  "capital_eq_note": ""
}
```

## 政策匹配输出 Schema

```json
{
  "version": "3.0.0",
  "module": "policy_matcher",
  "user_profile": {
    "district": "徐汇区",
    "sector": "AI智能体",
    "stage": "刚注册"
  },
  "matched_policies": [
    {
      "name": "徐汇区OPC创业启动金",
      "type": "cash_grant",
      "amount": {"min": 50000, "max": 100000},
      "match_score": "high",
      "action": "准备材料，提交至徐汇区科创委"
    }
  ],
  "total_estimated": {
    "min": 50000,
    "max": 2100000,
    "note": "估算值，以实际审批为准"
  },
  "recommended_community": {
    "name": "模速空间",
    "district": "徐汇区",
    "benefits": ["首年全免"]
  },
  "action_plan": {
    "short_term": {
      "timeframe": "本周",
      "tasks": ["准备入驻材料"]
    }
  }
}
```

## 专精特新评估输出 Schema

```json
{
  "version": "3.0.0",
  "module": "zhuanjingtexin_assessment",
  "assessment": {
    "current_tier": "none",
    "next_tier": "innovative_sme",
    "next_tier_name": "创新型中小企业",
    "innovative_sme": {
      "tier": "innovative_sme",
      "score": 45,
      "achievable": false,
      "gaps": [{"indicator": "研发投入占比", "priority": 2}]
    }
  },
  "roadmap": {
    "target_tier": "innovative_sme",
    "estimated_timeline": "2-3个月",
    "milestones": []
  }
}
```

## 响应格式规范

所有输出必须遵循：
1. 使用中文输出（专业术语保留英文）
2. 结构化格式（结论→依据→建议）
3. 明确标注红旗条款
4. 每个建议附带时间标签
5. 关键建议附加免责声明