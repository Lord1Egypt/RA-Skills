---
name: risk-assessor
version: 1.0.0
author: 燃冰 + 小蚂蚁
created: 2026-04-07
skill_type: 核心🔴
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [value-analyzer, moat-evaluator, intrinsic-value-calculator, asset-allocator]
tags: [风险评估，波动率，下行风险，集中度，仓位管理]
description: ［何时使用］当用户需要评估投资风险时；当用户询问"这只股票风险有多大"时；当需要计算合理仓位上限时；当需要压力测试投资组合时
---

# Risk Assessor 🛡️

**独立风险评估系统**

**核心功能**：波动率分析、下行风险评估、集中度分析、仓位上限计算

---

## 🎯 核心功能

### 1. 波动率分析

| 指标 | 计算方式 | 风险等级 |
|------|----------|----------|
| **历史波动率** | 过去 60 日收益率标准差×√252 | <20% 低 / 20-40% 中 / >40% 高 |
| **Beta 系数** | 相对大盘的敏感度 | <0.8 防御 / 0.8-1.2 中性 / >1.2 进攻 |
| **最大回撤** | 历史最大峰值到谷底跌幅 | <20% 低 / 20-40% 中 / >40% 高 |

### 2. 下行风险

| 指标 | 计算方式 | 含义 |
|------|----------|------|
| **VaR(95%)** | 95% 置信度下最大日损失 | "95% 情况下日损失不超过 X%" |
| **CVaR** | 超过 VaR 的平均损失 | 极端情况下的平均损失 |
| **下行偏差** | 仅计算负收益的标准差 | 衡量"坏波动" |
| **索提诺比率** | (收益 - 无风险利率)/下行偏差 | 风险调整后收益（只 penalize 下行） |

### 3. 集中度风险

| 维度 | 评估标准 | 风险等级 |
|------|----------|----------|
| **个股集中度** | 单一个股/总资产 | >20% 高 / 10-20% 中 / <10% 低 |
| **行业集中度** | 单一行业/股票组合 | >40% 高 / 25-40% 中 / <25% 低 |
| **相关性风险** | 持仓间平均相关系数 | >0.7 高 / 0.4-0.7 中 / <0.4 低 |

### 4. 仓位上限计算

```
基础仓位 = 风险评分 × 账户总权益

风险评分 = f(波动率，下行风险，集中度，流动性)

最终仓位 = min(基础仓位，流动性限制，单一上限)
```

---

## 📐 输出 Schema（标准化）

```json
{
  "signal": {
    "risk_level": "低 | 中 | 高 | 极高",
    "risk_score": 0-100,
    "position_limit": "建议仓位上限 (%)"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_quality": "数据质量说明"
  },
  "reasoning": {
    "key_findings": ["关键发现 1", "关键发现 2"],
    "risk_factors": [
      {
        "factor": "风险因素名称",
        "severity": "低 | 中 | 高",
        "description": "详细说明"
      }
    ],
    "mitigation": ["风险缓解建议 1", "建议 2"]
  },
  "metrics": {
    "volatility": {
      "historical_60d": "数值 (%)",
      "beta": "数值",
      "max_drawdown": "数值 (%)"
    },
    "downside_risk": {
      "var_95": "数值 (%)",
      "cvar": "数值 (%)",
      "sortino_ratio": "数值"
    },
    "concentration": {
      "single_stock": "数值 (%)",
      "sector": "数值 (%)",
      "correlation": "数值"
    }
  },
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。"
}
```

---

## 🔄 使用流程

### 流程 1：个股风险评估

```
Step 1: 获取历史价格数据（API 调用）
        - 过去 60 日收盘价
        - 对应基准指数（沪深 300）

Step 2: 计算波动率指标
        - 历史波动率
        - Beta 系数
        - 最大回撤

Step 3: 计算下行风险
        - VaR(95%)
        - CVaR
        - 索提诺比率

Step 4: 评估集中度（结合持仓）
        - 个股集中度
        - 行业集中度
        - 相关性分析

Step 5: 计算仓位上限
        - 基础仓位 = (100 - 风险评分) × 2%
        - 应用流动性限制
        - 输出最终建议

Step 6: 生成标准化输出
```

### 流程 2：组合压力测试

```
Step 1: 获取组合所有持仓数据

Step 2: 计算组合整体风险
        - 组合波动率
        - 组合 Beta
        - 组合 VaR

Step 3: 压力测试场景
        - 情景 1：大盘下跌 20%
        - 情景 2：行业下跌 30%
        - 情景 3：流动性危机

Step 4: 识别脆弱点
        - 最大风险来源
        - 最脆弱持仓

Step 5: 生成优化建议
        - 减仓建议
        - 对冲建议
        - 分散化建议
```

---

## 📊 风险评分模型

### 综合风险评分（0-100 分）

```
风险评分 = 
  波动率得分 × 30% +
  下行风险得分 × 30% +
  集中度得分 × 25% +
  流动性得分 × 15%

各维度得分（0-100，越高越危险）：

波动率得分：
- 历史波动率 < 20% → 20 分
- 20% ≤ 波动率 < 40% → 50 分
- 波动率 ≥ 40% → 80 分

下行风险得分：
- 最大回撤 < 20% → 20 分
- 20% ≤ 回撤 < 40% → 50 分
- 回撤 ≥ 40% → 80 分

集中度得分：
- 个股占比 < 10% → 20 分
- 10% ≤ 占比 < 20% → 50 分
- 占比 ≥ 20% → 80 分

流动性得分：
- 日均成交 > 10 亿 → 20 分
- 1 亿 < 成交 < 10 亿 → 50 分
- 成交 < 1 亿 → 80 分
```

### 风险等级划分

| 评分 | 等级 | 仓位上限 | 说明 |
|------|------|----------|------|
| 0-25 | 低风险 | ≤20% | 适合重仓 |
| 26-50 | 中风险 | ≤10% | 适度配置 |
| 51-75 | 高风险 | ≤5% | 轻仓参与 |
| 76-100 | 极高风险 | ≤2% | 观察为主 |

---

## 🧪 使用示例

### 示例 1：贵州茅台风险评估（完整 Schema）

**用户输入**：
```
评估贵州茅台的投资风险
```

**输出**（符合 OUTPUT_SCHEMA.md）：
```json
{
  "signal": {
    "summary": "贵州茅台风险等级中，适合适度配置，仓位上限 10%",
    "recommendation": "推荐",
    "score": 42,
    "risk_level": "中"
  },
  "confidence": {
    "score": 85,
    "level": "高",
    "data_quality": "数据完整，60 日交易数据充足，多源验证",
    "limitations": [
      "历史波动率不代表未来",
      "政策风险难以量化"
    ]
  },
  "reasoning": {
    "key_findings": [
      "波动率 28%，低于白酒行业平均 35%",
      "最大回撤 -32%，处于历史中位",
      "流动性极佳，日均成交>50 亿",
      "行业政策风险中等（消费税传闻）"
    ],
    "analysis": [
      {
        "dimension": "波动率",
        "finding": "28%，低于行业平均",
        "evidence": "60 日历史波动率 28% vs 行业 35%",
        "impact": "低"
      },
      {
        "dimension": "下行风险",
        "finding": "VaR(95%) -3.2%，最大回撤 -32%",
        "evidence": "历史最大回撤 2022 年 -32%",
        "impact": "中"
      },
      {
        "dimension": "流动性",
        "finding": "日均成交 50 亿，流动性极佳",
        "evidence": "近 30 日日均成交额",
        "impact": "低"
      }
    ],
    "risk_factors": [
      {
        "factor": "行业政策风险",
        "severity": "中",
        "description": "白酒行业可能面临消费税调整"
      },
      {
        "factor": "估值风险",
        "severity": "中",
        "description": "当前 PE 35x，高于历史中位数 28x"
      },
      {
        "factor": "集中度风险",
        "severity": "低",
        "description": "假设持仓中白酒行业占比 15%"
      }
    ],
    "assumptions": [
      "宏观经济不出现硬着陆",
      "白酒行业政策无重大变化"
    ],
    "risks": [
      "消费税改革风险",
      "高端酒需求下滑风险",
      "利率上升导致估值承压"
    ]
  },
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
    },
    "concentration": {
      "single_stock": { "value": 8, "unit": "%" },
      "sector": { "value": 15, "unit": "%" },
      "correlation": { "value": 0.45, "unit": "" }
    },
    "liquidity": {
      "avg_volume_30d": { "value": 50, "unit": "亿" }
    }
  },
  "sources": [
    { "name": "东方财富 Choice", "type": "第三方", "reliability": "A", "url": "https://choice.eastmoney.com/" },
    { "name": "贵州茅台年报", "type": "官方", "reliability": "S", "url": "http://www.sse.com.cn/" }
  ],
  "action_items": [
    { "priority": "高", "action": "仓位控制在 10% 以内", "timeline": "立即", "success_criteria": "建仓完成" },
    { "priority": "中", "action": "设定止损位 -15%（¥1800）", "timeline": "买入后立即", "success_criteria": "止损单设置" },
    { "priority": "低", "action": "跟踪消费税政策动向", "timeline": "持续", "success_criteria": "政策出台时及时评估" }
  ],
  "next_steps": [
    "使用 value-analyzer 评估当前价格安全边际",
    "使用 sentiment-analyzer 检查市场情绪"
  ],
  "related_skills": ["value-analyzer", "moat-evaluator", "sentiment-analyzer"],
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。",
  "metadata": {
    "skill_name": "risk-assessor",
    "skill_version": "1.0.0",
    "generated_at": "2026-04-07T08:30:00+08:00",
    "data_as_of": "2026-04-06T15:00:00+08:00",
    "cache_status": "fresh"
  }
}
```

---

### 示例 2：长江电力风险评估

**用户输入**：
```
评估长江电力的投资风险
```

**输出摘要**：
```json
{
  "signal": {
    "summary": "长江电力风险等级低，适合稳健配置，仓位上限 15%",
    "recommendation": "推荐",
    "score": 28,
    "risk_level": "低"
  },
  "metrics": {
    "volatility": { "historical_60d": { "value": 15, "unit": "%" }, "beta": { "value": 0.65 } },
    "downside_risk": { "var_95": { "value": -2.1, "unit": "%" }, "sortino_ratio": { "value": 1.8 } }
  }
}
```

---

### 示例 1（旧版）：贵州茅台风险评估

**用户输入**：
```
评估贵州茅台的投资风险
```

**输出**（简化版）：
```json
{
  "signal": {
    "risk_level": "中",
    "risk_score": 42,
    "position_limit": "10%"
  },
  "confidence": {
    "score": 85,
    "level": "高",
    "data_quality": "数据完整，60 日交易数据充足"
  },
  "reasoning": {
    "key_findings": [
      "波动率适中（28%），低于白酒行业平均（35%）",
      "最大回撤 -32%，处于历史中位",
      "流动性极佳，日均成交>50 亿"
    ],
    "risk_factors": [
      {
        "factor": "行业政策风险",
        "severity": "中",
        "description": "白酒行业可能面临消费税调整"
      },
      {
        "factor": "估值风险",
        "severity": "中",
        "description": "当前 PE 35x，高于历史中位数 28x"
      },
      {
        "factor": "集中度风险",
        "severity": "低",
        "description": "白酒行业占组合 15%，适度"
      }
    ],
    "mitigation": [
      "仓位控制在 10% 以内",
      "设定止损位 -15%",
      "关注消费税政策动向"
    ]
  },
  "metrics": {
    "volatility": {
      "historical_60d": "28%",
      "beta": "0.85",
      "max_drawdown": "-32%"
    },
    "downside_risk": {
      "var_95": "-3.2%",
      "cvar": "-4.8%",
      "sortino_ratio": "1.2"
    },
    "concentration": {
      "single_stock": "8%",
      "sector": "15%",
      "correlation": "0.45"
    }
  },
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。"
}
```

### 示例 2：组合压力测试

**用户输入**：
```
对我的持仓进行压力测试：
- 贵州茅台 20%
- 宁德时代 15%
- 招商银行 15%
- 沪深 300ETF 30%
- 国债 ETF 20%
```

**输出**：
```json
{
  "signal": {
    "risk_level": "中",
    "risk_score": 48,
    "position_limit": "当前仓位合理"
  },
  "confidence": {
    "score": 80,
    "level": "高",
    "data_quality": "组合数据完整"
  },
  "reasoning": {
    "key_findings": [
      "组合波动率 18%，低于股票型组合平均（22%）",
      "组合 Beta 0.92，略低于大盘",
      "行业分散度良好（白酒/新能源/金融/宽基/债券）"
    ],
    "risk_factors": [
      {
        "factor": "个股集中度",
        "severity": "中",
        "description": "茅台占比 20%，达到单一上限"
      },
      {
        "factor": "相关性上升",
        "severity": "低",
        "description": "市场下跌时相关性可能上升至 0.7+"
      }
    ],
    "mitigation": [
      "茅台仓位不再增加",
      "考虑增加海外资产分散风险",
      "保持国债 ETF 20% 作为缓冲"
    ]
  },
  "stress_test": {
    "scenarios": [
      {
        "name": "大盘下跌 20%",
        "组合损失": "-16%",
        "最大回撤持仓": "宁德时代 (-28%)"
      },
      {
        "name": "白酒行业下跌 30%",
        "组合损失": "-8%",
        "说明": "茅台拖累，但其他持仓对冲"
      },
      {
        "name": "流动性危机",
        "组合损失": "-22%",
        "说明": "国债 ETF 提供流动性缓冲"
      }
    ]
  },
  "metrics": {
    "portfolio_volatility": "18%",
    "portfolio_beta": "0.92",
    "portfolio_var_95": "-2.8%",
    "diversification_ratio": "1.3"
  },
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。"
}
```

---

## 🔧 数据源

### 推荐 API

| 数据 | 来源 | 频率 |
|------|------|------|
| 历史价格 | 东方财富/新浪财经 | 实时 |
| 财务数据 | 东方财富 Choice | 季报 |
| 行业数据 | 申万宏源 | 月度 |
| 宏观数据 | 国家统计局 | 月度 |

### 缓存策略

```
- 价格数据：缓存 1 小时
- 波动率计算：缓存 24 小时
- 财务数据：缓存 7 天
- 行业数据：缓存 7 天
```

---

## ⚠️ 注意事项

### 1. 数据质量

- ✅ 优先使用官方数据源（交易所、统计局）
- ✅ 交叉验证（至少 2 个来源）
- ❌ 避免单一自媒体来源
- ❌ 避免使用超过 30 天的财务数据

### 2. 模型局限

- 历史波动率不代表未来
- VaR 假设正态分布（实际有肥尾）
- 相关性在危机时可能失效
- 黑天鹅事件无法量化

### 3. 使用建议

- ✅ 定期更新（至少每周）
- ✅ 结合定性分析
- ✅ 设置止损纪律
- ❌ 不机械套用模型
- ❌ 不忽视基本面变化

---

## 🔗 相关技能

- `value-analyzer` - 价值分析（风险 - 收益平衡）
- `moat-evaluator` - 护城河评估（长期风险）
- `intrinsic-value-calculator` - 内在价值（安全边际）
- `asset-allocator` - 资产配置（组合风险）
- `sentiment-analyzer` - 情绪分析（市场风险）

---

*风险控制的本质不是避免风险，而是理解风险、定价风险、管理风险。* 🛡️
