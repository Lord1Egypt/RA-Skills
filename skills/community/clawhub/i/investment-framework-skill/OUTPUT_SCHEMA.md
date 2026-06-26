# 投资框架技能标准化输出 Schema ⭐⭐⭐⭐⭐

**版本**：v1.0.0  
**生效日期**：2026-04-07  
**适用范围**：investment-framework 所有子技能（30 个）

---

## 🎯 设计原则

### 1. 一致性
所有技能输出结构统一，便于：
- 跨技能对比分析
- 自动化处理（脚本/仪表盘）
- 用户快速定位关键信息

### 2. 可读性
- 人类可读的 JSON 结构
- 清晰的层级关系
- 明确的字段含义

### 3. 可操作性
- `signal` 字段直接支持决策
- `action_items` 提供明确行动建议
- `confidence` 帮助判断可信度

### 4. 可追溯性
- `reasoning` 记录分析逻辑
- `metrics` 保留原始数据
- `sources` 标注数据来源

---

## 📐 核心 Schema

### 标准输出结构

```json
{
  "signal": {
    "summary": "一句话结论",
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "score": 0-100,
    "level": "低 | 中 | 高 | 极高"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_quality": "数据质量说明",
    "limitations": ["局限性 1", "局限性 2"]
  },
  "reasoning": {
    "key_findings": ["关键发现 1", "关键发现 2", "关键发现 3"],
    "analysis": [
      {
        "dimension": "分析维度",
        "finding": "发现",
        "evidence": "支持证据",
        "impact": "低 | 中 | 高"
      }
    ],
    "assumptions": ["关键假设 1", "假设 2"],
    "risks": ["风险 1", "风险 2"]
  },
  "metrics": {
    "primary": {
      "metric_name": "数值",
      "unit": "单位",
      "benchmark": "基准值",
      "percentile": "历史分位"
    },
    "secondary": {
      "metric_name": "数值"
    }
  },
  "sources": [
    {
      "name": "数据源名称",
      "type": "官方 | 媒体 | 第三方",
      "reliability": "S | A | B | C",
      "url": "原始链接（如有）"
    }
  ],
  "action_items": [
    {
      "priority": "高 | 中 | 低",
      "action": "具体行动",
      "timeline": "时间要求",
      "success_criteria": "成功标准"
    }
  ],
  "next_steps": ["下一步 1", "下一步 2"],
  "related_skills": ["skill-1", "skill-2"],
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。",
  "metadata": {
    "skill_name": "技能名称",
    "skill_version": "版本",
    "generated_at": "ISO8601 时间戳",
    "data_as_of": "数据截止时间",
    "cache_status": "fresh | cached"
  }
}
```

---

## 📋 字段详解

### 1. signal（决策信号）⭐⭐⭐⭐⭐

**用途**：快速决策依据，用户第一眼看到的内容

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `summary` | string | ✅ | 一句话结论（≤50 字） |
| `recommendation` | string | ✅ | 五级推荐：强烈推荐/推荐/观察/谨慎/避免 |
| `score` | number | ✅ | 综合评分（0-100） |
| `level` | string | ✅ | 风险/机会等级：低/中/高/极高 |

**示例**：
```json
"signal": {
  "summary": "贵州茅台护城河强，但当前价格安全边际不足",
  "recommendation": "观察",
  "score": 65,
  "level": "中"
}
```

### 2. confidence（置信度）⭐⭐⭐⭐

**用途**：帮助用户判断结论可信度，避免盲目信任

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `score` | number | ✅ | 置信度评分（0-100） |
| `level` | string | ✅ | 置信度等级：低/中/高 |
| `data_quality` | string | ✅ | 数据质量说明（100 字内） |
| `limitations` | array | ✅ | 分析局限性列表 |

**置信度评分标准**：
| 分数 | 等级 | 说明 |
|------|------|------|
| 80-100 | 高 | 数据完整，多源验证，逻辑严密 |
| 60-79 | 中 | 数据基本完整，部分假设 |
| 0-59 | 低 | 数据不足，依赖强假设 |

**示例**：
```json
"confidence": {
  "score": 82,
  "level": "高",
  "data_quality": "数据完整，60 日交易数据充足，多源交叉验证",
  "limitations": [
    "历史数据不代表未来表现",
    "未考虑突发政策变化"
  ]
}
```

### 3. reasoning（分析推理）⭐⭐⭐⭐⭐

**用途**：记录分析逻辑，支持用户深度理解决策依据

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `key_findings` | array | ✅ | 关键发现（3-5 条） |
| `analysis` | array | ✅ | 详细分析维度 |
| `assumptions` | array | ✅ | 关键假设列表 |
| `risks` | array | ✅ | 主要风险列表 |

**analysis 数组结构**：
```json
{
  "dimension": "分析维度名称",
  "finding": "该维度的发现",
  "evidence": "支持证据（数据/事实）",
  "impact": "影响程度（低/中/高）"
}
```

**示例**：
```json
"reasoning": {
  "key_findings": [
    "护城河强（18/25 分），网络效应和转换成本是核心优势",
    "当前价格对应安全边际 15%，不足 30% 买入标准",
    "管理层稳定，过去 5 年核心高管无重大变动"
  ],
  "analysis": [
    {
      "dimension": "护城河",
      "finding": "强（18/25 分）",
      "evidence": "网络效应 5/5，转换成本 5/5，品牌 4/5",
      "impact": "高"
    },
    {
      "dimension": "估值",
      "finding": "合理偏高",
      "evidence": "PE 35x vs 历史中位数 28x",
      "impact": "中"
    }
  ],
  "assumptions": [
    "宏观经济不出现硬着陆",
    "白酒行业政策无重大变化"
  ],
  "risks": [
    "消费税改革风险",
    "高端酒需求下滑风险"
  ]
}
```

### 4. metrics（量化指标）⭐⭐⭐⭐

**用途**：提供原始数据，支持用户独立验证

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `primary` | object | ✅ | 核心指标（3-5 个） |
| `secondary` | object | ⭕ | 辅助指标 |

**primary 指标结构**：
```json
{
  "metric_name": {
    "value": "数值",
    "unit": "单位（%，x，倍等）",
    "benchmark": "基准值/行业平均",
    "percentile": "历史分位（0-100）"
  }
}
```

**示例**：
```json
"metrics": {
  "primary": {
    "pe_ratio": {
      "value": 35.2,
      "unit": "x",
      "benchmark": 28.0,
      "percentile": 72
    },
    "roe": {
      "value": 28.5,
      "unit": "%",
      "benchmark": 15.0,
      "percentile": 88
    }
  }
}
```

### 5. sources（数据来源）⭐⭐⭐⭐

**用途**：标注数据来源，支持可信度评估和追溯

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 数据源名称 |
| `type` | string | ✅ | 来源类型：官方/媒体/第三方 |
| `reliability` | string | ✅ | 可靠性等级：S/A/B/C |
| `url` | string | ⭕ | 原始链接 |

**可靠性等级**（参考 MEMORY.md 信源分级）：
| 等级 | 标识 | 来源类型 | 使用方式 |
|------|------|---------|---------|
| S | 🟢 | 官方文档、GitHub、学术期刊、监管机构 | 直接引用 |
| A | 🟡 | 权威媒体、知名开发者博客、上市公司财报 | 交叉验证后使用 |
| B | 🟠 | 技术社区、自媒体、行业分析机构 | 多源印证或标注不确定性 |
| C | 🔴 | 匿名论坛、单一来源爆料 | 仅作线索，标注「待核实」 |

**示例**：
```json
"sources": [
  {
    "name": "东方财富 Choice",
    "type": "第三方",
    "reliability": "A",
    "url": "https://choice.eastmoney.com/"
  },
  {
    "name": "贵州茅台 2024 年年报",
    "type": "官方",
    "reliability": "S",
    "url": "http://www.sse.com.cn/"
  }
]
```

### 6. action_items（行动建议）⭐⭐⭐⭐⭐

**用途**：提供明确可执行的行动建议

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `priority` | string | ✅ | 优先级：高/中/低 |
| `action` | string | ✅ | 具体行动（动词开头） |
| `timeline` | string | ✅ | 时间要求 |
| `success_criteria` | string | ✅ | 成功标准 |

**示例**：
```json
"action_items": [
  {
    "priority": "高",
    "action": "将贵州茅台加入观察列表",
    "timeline": "立即",
    "success_criteria": "设定价格提醒（目标价<¥1500）"
  },
  {
    "priority": "中",
    "action": "跟踪 Q2 财报，关注营收增速",
    "timeline": "2024 年 Q2 财报发布后",
    "success_criteria": "营收增速>15% 则重新评估"
  }
]
```

### 7. next_steps（后续步骤）⭐⭐⭐

**用途**：建议后续分析方向

**示例**：
```json
"next_steps": [
  "使用 risk-assessor 评估下行风险",
  "使用 sentiment-analyzer 检查市场情绪",
  "使用 decision-checklist 进行最终决策检查"
]
```

### 8. related_skills（相关技能）⭐⭐⭐

**用途**：推荐关联技能，支持组合使用

**示例**：
```json
"related_skills": [
  "value-analyzer",
  "moat-evaluator",
  "risk-assessor"
]
```

### 9. metadata（元数据）⭐⭐⭐

**用途**：记录分析上下文，支持审计和追溯

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skill_name` | string | ✅ | 技能名称 |
| `skill_version` | string | ✅ | 技能版本 |
| `generated_at` | string | ✅ | ISO8601 时间戳 |
| `data_as_of` | string | ✅ | 数据截止时间 |
| `cache_status` | string | ✅ | fresh（实时）/ cached（缓存） |

**示例**：
```json
"metadata": {
  "skill_name": "value-analyzer",
  "skill_version": "3.2.0",
  "generated_at": "2026-04-07T10:30:00+08:00",
  "data_as_of": "2026-04-06T15:00:00+08:00",
  "cache_status": "fresh"
}
```

---

## 📊 技能特定 Schema 扩展

### value-analyzer 扩展

```json
"metrics": {
  "primary": {
    "pe_ratio": { "value": 35.2, "unit": "x", "benchmark": 28.0, "percentile": 72 },
    "pb_ratio": { "value": 8.5, "unit": "x", "benchmark": 6.0, "percentile": 68 },
    "roe": { "value": 28.5, "unit": "%", "benchmark": 15.0, "percentile": 88 },
    "debt_to_equity": { "value": 0.15, "unit": "", "benchmark": 0.5, "percentile": 15 }
  },
  "graham_criteria": {
    "size": { "pass": true, "value": "1000 亿+", "threshold": ">100 亿" },
    "financial_strength": { "pass": true, "value": "流动比率 3.5", "threshold": ">2" },
    "earnings_stability": { "pass": true, "value": "连续 10 年盈利", "threshold": "10 年" },
    "dividend_record": { "pass": true, "value": "连续 8 年分红", "threshold": "5 年" },
    "growth": { "pass": true, "value": "10 年 CAGR 15%", "threshold": ">7%" },
    "moderate_pe": { "pass": false, "value": 35.2, "threshold": "<15" },
    "moderate_pb": { "pass": false, "value": 8.5, "threshold": "<1.5" }
  }
}
```

### moat-evaluator 扩展

```json
"metrics": {
  "moat_score": {
    "total": 18,
    "max": 25,
    "level": "强"
  },
  "moat_types": {
    "brand": { "score": 4, "max": 5, "evidence": "高端品牌心智" },
    "network_effect": { "score": 5, "max": 5, "evidence": "用户越多价值越大" },
    "switching_cost": { "score": 5, "max": 5, "evidence": "高转换成本" },
    "scale_advantage": { "score": 2, "max": 5, "evidence": "规模优势一般" },
    "franchise": { "score": 2, "max": 5, "evidence": "无特许经营权" }
  },
  "moat_trend": "稳定 | 增强 | 减弱"
}
```

### risk-assessor 扩展

```json
"metrics": {
  "volatility": {
    "historical_60d": { "value": 28, "unit": "%", "benchmark": 35, "percentile": 42 },
    "beta": { "value": 0.85, "unit": "", "benchmark": 1.0, "percentile": 35 },
    "max_drawdown": { "value": -32, "unit": "%", "benchmark": -45, "percentile": 28 }
  },
  "downside_risk": {
    "var_95": { "value": -3.2, "unit": "%" },
    "cvar": { "value": -4.8, "unit": "%" },
    "sortino_ratio": { "value": 1.2, "unit": "" }
  }
}
```

### sentiment-analyzer 扩展

```json
"metrics": {
  "news_sentiment": {
    "score": 62,
    "article_count": 78,
    "positive_ratio": 68,
    "unit": "%"
  },
  "social_sentiment": {
    "score": 28,
    "discussion_volume": 2340,
    "sentiment_change_7d": 5
  },
  "analyst_ratings": {
    "consensus": "买入",
    "upgrades_30d": 5,
    "downgrades_30d": 1,
    "target_price_upside": 15,
    "unit": "%"
  }
}
```

---

## 🔄 版本管理

### Schema 版本规则

- **主版本**（v1.x.x）：破坏性变更（字段删除/类型变更）
- **次版本**（vx.1.x）：向后兼容的新增字段
- **修订版**（vx.x.1）：文档/示例更新

### 变更流程

1. 提出变更需求（GitHub Issue）
2. 评估影响范围（破坏性/兼容性）
3. 更新 Schema 文档
4. 更新所有受影响技能
5. 更新版本号

---

## ✅ 验收标准

### 技能输出合规检查清单

- [ ] 包含所有必填字段（signal, confidence, reasoning, metrics, sources, action_items, metadata）
- [ ] `signal.recommendation` 使用五级标准（强烈推荐/推荐/观察/谨慎/避免）
- [ ] `confidence.score` 0-100 范围
- [ ] `reasoning.key_findings` 3-5 条
- [ ] `metrics.primary` 3-5 个核心指标
- [ ] `sources` 至少 2 个数据源
- [ ] `action_items` 至少 1 个可执行建议
- [ ] `metadata` 包含完整时间戳
- [ ] 包含免责声明
- [ ] JSON 格式有效

---

## 📚 实施计划

### Phase 1（2026-04-07）
- ✅ 创建 risk-assessor 技能（使用新 Schema）
- ✅ 创建 sentiment-analyzer 技能（使用新 Schema）
- ✅ 创建 OUTPUT_SCHEMA.md 文档

### Phase 2（2026-04-14）
- [ ] 更新现有 10 个技能适配新 Schema
- [ ] 创建 Schema 验证脚本
- [ ] 更新技能文档

### Phase 3（2026-04-21）
- [ ] 所有 30 个技能完成迁移
- [ ] 创建示例输出库
- [ ] 用户文档更新

---

## 🔗 相关文档

- `SKILL.md` - 投资框架主文档
- `SKILLS-INVENTORY.md` - 技能清单
- `risk-assessor/SKILL.md` - 风险评估技能
- `sentiment-analyzer/SKILL.md` - 情绪分析技能

---

*标准化不是束缚，而是为了让分析更可靠、决策更清晰、协作更高效。* 📐
