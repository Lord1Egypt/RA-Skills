---
name: sentiment-analyzer
version: 1.0.0
author: 燃冰 + 小蚂蚁
created: 2026-04-07
skill_type: 核心🔴
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [value-analyzer, risk-assessor, future-forecaster, decision-checklist]
tags: [情绪分析，新闻情绪，社交媒体，分析师评级，市场情绪]
description: ［何时使用］当用户需要了解市场情绪时；当用户询问"市场怎么看这家公司"时；当需要判断情绪是否过度乐观/悲观时；当需要反向投资信号时
---

# Sentiment Analyzer 📊

**市场情绪分析系统**

**核心功能**：新闻情绪分析、社交媒体情绪、分析师评级汇总、情绪评分 + 趋势判断

---

## 🎯 核心功能

### 1. 新闻情绪分析

| 维度 | 数据源 | 分析方法 |
|------|--------|----------|
| **主流媒体** | 财联社/华尔街见闻/Reuters | NLP 情感分析 |
| **官方公告** | 交易所公告/公司财报 | 关键词提取 |
| **行业媒体** | 36 氪/虎嗅/晚点 | 主题聚类 |
| **政策新闻** | 国新办/各部委官网 | 政策影响评估 |

**情绪分类**：
- 🟢 正面（利好）：业绩超预期、产品突破、政策扶持
- 🟡 中性：常规公告、人事变动、行业评论
- 🔴 负面（利空）：业绩不及预期、监管处罚、负面舆情

### 2. 社交媒体情绪

| 平台 | 监测内容 | 权重 |
|------|----------|------|
| **微博** | 热搜话题、大 V 观点 | 15% |
| **雪球** | 个股讨论、投资大 V | 25% |
| **知乎** | 深度分析、行业讨论 | 20% |
| **东方财富股吧** | 散户情绪、热度 | 20% |
| **微信公众号** | 深度文章、机构观点 | 20% |

**情绪指标**：
- 讨论热度（声量）
- 情绪倾向（正面/负面比例）
- 情绪变化（7 日趋势）
- 极端情绪指数（贪婪/恐惧）

### 3. 分析师评级

| 指标 | 计算方式 | 含义 |
|------|----------|------|
| **一致评级** | 买入/增持/中性/减持/卖出 | 分析师平均观点 |
| **评级变化** | 近 30 天上调/下调次数 | 观点边际变化 |
| **目标价空间** | (平均目标价 - 当前价)/当前价 | 预期上涨空间 |
| **覆盖密度** | 覆盖分析师数量 | 市场关注度 |

### 4. 情绪综合评分

```
情绪评分 = 
  新闻情绪 × 35% +
  社交媒体情绪 × 30% +
  分析师评级 × 25% +
  资金流向 × 10%

评分范围：-100（极度悲观）到 +100（极度乐观）
```

---

## 📐 输出 Schema（标准化）

```json
{
  "signal": {
    "sentiment_score": -100 到 +100,
    "sentiment_level": "极度悲观 | 悲观 | 中性 | 乐观 | 极度乐观",
    "trend": "改善 | 稳定 | 恶化",
    "contrarian_signal": "反向投资信号（是/否）"
  },
  "confidence": {
    "score": 0-100,
    "level": "低 | 中 | 高",
    "data_coverage": "数据覆盖说明"
  },
  "reasoning": {
    "key_findings": ["关键发现 1", "关键发现 2"],
    "sentiment_drivers": [
      {
        "factor": "驱动因素",
        "direction": "正面 | 负面",
        "impact": "低 | 中 | 高",
        "description": "详细说明"
      }
    ],
    "risks": ["情绪误判风险", "数据滞后风险"]
  },
  "metrics": {
    "news_sentiment": {
      "score": -100 到 +100,
      "article_count": "文章数量",
      "positive_ratio": "正面比例 (%)"
    },
    "social_sentiment": {
      "score": -100 到 +100,
      "discussion_volume": "讨论量",
      "sentiment_change_7d": "7 日变化"
    },
    "analyst_ratings": {
      "consensus": "买入/增持/中性/减持/卖出",
      "upgrades_30d": "上调次数",
      "downgrades_30d": "下调次数",
      "target_price_upside": "目标价空间 (%)"
    },
    "fund_flow": {
      "northbound_5d": "北向资金 5 日净流入",
      "institutional_flow": "机构资金流向"
    }
  },
  "action_items": [
    "基于情绪的 actionable 建议"
  ],
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。"
}
```

---

## 🔄 使用流程

### 流程 1：个股情绪分析

```
Step 1: 收集新闻数据（过去 7 天）
        - 主流媒体（财联社/华尔街见闻）
        - 官方公告
        - 行业媒体

Step 2: NLP 情绪分析
        - 正面/负面/中性分类
        - 关键词提取
        - 情感强度评分

Step 3: 社交媒体监测
        - 雪球/微博/知乎讨论
        - 情绪倾向统计
        - 热度变化趋势

Step 4: 分析师评级汇总
        - 一致评级
        - 近 30 天变化
        - 目标价空间

Step 5: 资金流向分析
        - 北向资金
        - 机构资金

Step 6: 综合评分 + 趋势判断
        - 加权计算
        - 7 日/30 日趋势
        - 反向信号识别

Step 7: 生成标准化输出
```

### 流程 2：市场整体情绪

```
Step 1: 大盘情绪指标
        - 涨跌家数比
        - 涨停/跌停家数
        - 成交量变化

Step 2: 情绪极端值识别
        - 贪婪/恐惧指数
        - 历史分位

Step 3: 反向信号判断
        - 极度乐观 → 警惕回调
        - 极度悲观 → 关注机会

Step 4: 生成市场情绪报告
```

---

## 📊 情绪评分模型

### 综合情绪评分（-100 到 +100）

```
情绪评分 = 
  新闻情绪 × 35% +
  社交媒体情绪 × 30% +
  分析师评级 × 25% +
  资金流向 × 10%

各维度计算：

新闻情绪（-100 到 +100）：
= (正面文章数 - 负面文章数) / 总文章数 × 100

社交媒体情绪（-100 到 +100）：
= (正面帖子数 - 负面帖子数) / 总帖子数 × 100
× 热度系数（讨论量越大，权重越高）

分析师评级（-100 到 +100）：
买入=+100, 增持=+50, 中性=0, 减持=-50, 卖出=-100
= 平均评级 × 20

资金流向（-100 到 +100）：
= 标准化后的资金净流入
```

### 情绪等级划分

| 评分 | 等级 | 反向信号 | 操作建议 |
|------|------|----------|----------|
| 80-100 | 极度乐观 | ⚠️ 警惕 | 考虑减仓 |
| 60-79 | 乐观 | - | 持有 |
| 20-59 | 温和乐观 | - | 适度参与 |
| -19-19 | 中性 | - | 观望 |
| -59--20 | 温和悲观 | - | 关注机会 |
| -79--60 | 悲观 | ✅ 关注 | 逐步建仓 |
| -100--80 | 极度悲观 | ✅ 机会 | 重点研究 |

### 趋势判断

```
趋势 = 当前评分 - 7 日前评分

趋势 > +20 → 改善 📈
趋势 -20 到 +20 → 稳定 ➡️
趋势 < -20 → 恶化 📉
```

---

## 🧪 使用示例

### 示例 1：贵州茅台情绪分析（完整 Schema）

**用户输入**：
```
分析贵州茅台的市场情绪
```

**输出**（符合 OUTPUT_SCHEMA.md）：
```json
{
  "signal": {
    "summary": "贵州茅台情绪温和乐观（32 分），无反向信号，适合持有",
    "sentiment_score": 32,
    "sentiment_level": "温和乐观",
    "trend": "稳定",
    "contrarian_signal": "否"
  },
  "confidence": {
    "score": 78,
    "level": "中",
    "data_coverage": "新闻 45 篇，社交帖子 1200 条，分析师 18 人覆盖",
    "limitations": [
      "社交媒体数据覆盖有限",
      "部分分析师评级更新滞后"
    ]
  },
  "reasoning": {
    "key_findings": [
      "新闻情绪正面（55 分），季报超预期驱动",
      "社交媒体情绪中性（25 分），散户讨论热度一般",
      "分析师一致'增持'，目标价空间 +12%",
      "北向资金近 5 日净流入 3.2 亿"
    ],
    "sentiment_drivers": [
      {
        "factor": "季报超预期",
        "direction": "正面",
        "impact": "高",
        "description": "Q1 发电量 +8%，营收 +6%，超市场预期"
      },
      {
        "factor": "来水改善预期",
        "direction": "正面",
        "impact": "中",
        "description": "气象预测显示二季度来水偏丰"
      },
      {
        "factor": "利率环境",
        "direction": "负面",
        "impact": "低",
        "description": "市场担忧利率上行压制高股息资产估值"
      }
    ],
    "risks": [
      "情绪数据可能已反映在股价中",
      "来水预测存在不确定性"
    ]
  },
  "metrics": {
    "news_sentiment": { "score": 55, "article_count": 45, "positive_ratio": 62, "unit": "%" },
    "social_sentiment": { "score": 25, "discussion_volume": 1200, "sentiment_change_7d": 3 },
    "analyst_ratings": { "consensus": "增持", "upgrades_30d": 3, "downgrades_30d": 0, "target_price_upside": 12, "unit": "%" },
    "fund_flow": { "northbound_5d": { "value": 3.2, "unit": "亿" }, "institutional_flow": "净流入" }
  },
  "sources": [
    { "name": "财联社", "type": "媒体", "reliability": "A", "url": "https://www.cls.cn/" },
    { "name": "雪球", "type": "第三方", "reliability": "B", "url": "https://xueqiu.com/" },
    { "name": "东方财富 Choice", "type": "第三方", "reliability": "A", "url": "https://choice.eastmoney.com/" }
  ],
  "action_items": [
    { "priority": "中", "action": "情绪温和乐观，维持现有仓位", "timeline": "持续持有", "success_criteria": "仓位保持在 10-15%" },
    { "priority": "低", "action": "若情绪升至 80+（极度乐观），考虑减仓", "timeline": "监控中", "success_criteria": "设定情绪预警" },
    { "priority": "低", "action": "若情绪降至 -60 以下（极度悲观），重点研究加仓机会", "timeline": "监控中", "success_criteria": "设定情绪预警" }
  ],
  "next_steps": [
    "使用 risk-assessor 评估下行风险",
    "使用 value-analyzer 计算安全边际",
    "使用 decision-checklist 进行最终决策检查"
  ],
  "related_skills": ["risk-assessor", "value-analyzer", "decision-checklist"],
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。",
  "metadata": {
    "skill_name": "sentiment-analyzer",
    "skill_version": "1.0.0",
    "generated_at": "2026-04-07T08:30:00+08:00",
    "data_as_of": "2026-04-06T15:00:00+08:00",
    "cache_status": "fresh"
  }
}
```

---

### 示例 2：A 股市场整体情绪

**用户输入**：
```
当前 A 股市场情绪如何
```

**输出摘要**：
```json
{
  "signal": {
    "summary": "A 股市场情绪温和悲观（-35 分），接近反向信号区间",
    "sentiment_score": -35,
    "sentiment_level": "温和悲观",
    "trend": "恶化",
    "contrarian_signal": "否（接近反向信号区间）"
  },
  "metrics": {
    "market_breadth": { "advance_decline_ratio": "1:3", "limit_up_count": 25, "limit_down_count": 89 },
    "sentiment_indicators": { "fear_greed_index": 32, "historical_percentile": "25%" }
  }
}
```

---

### 示例 1（旧版）：贵州茅台情绪分析

**用户输入**：
```
分析贵州茅台的市场情绪
```

**输出**（简化版）：
```json
{
  "signal": {
    "sentiment_score": 45,
    "sentiment_level": "温和乐观",
    "trend": "稳定",
    "contrarian_signal": "否"
  },
  "confidence": {
    "score": 82,
    "level": "高",
    "data_coverage": "新闻 78 篇，社交帖子 2340 条，分析师 25 人覆盖"
  },
  "reasoning": {
    "key_findings": [
      "新闻情绪正面（62 分），主要受季报超预期驱动",
      "社交媒体情绪中性（28 分），散户分歧较大",
      "分析师一致'买入'，目标价空间 +15%"
    ],
    "sentiment_drivers": [
      {
        "factor": "季报超预期",
        "direction": "正面",
        "impact": "高",
        "description": "Q1 营收 +18%，净利 +20%，超市场预期"
      },
      {
        "factor": "白酒消费税传闻",
        "direction": "负面",
        "impact": "中",
        "description": "市场担忧消费税改革，但暂无实质进展"
      },
      {
        "factor": "北向资金流入",
        "direction": "正面",
        "impact": "中",
        "description": "近 5 日净流入 12 亿"
      }
    ],
    "risks": [
      "情绪数据滞后，可能已反映在股价中",
      "社交媒体情绪易受短期事件影响"
    ]
  },
  "metrics": {
    "news_sentiment": {
      "score": 62,
      "article_count": 78,
      "positive_ratio": "68%"
    },
    "social_sentiment": {
      "score": 28,
      "discussion_volume": 2340,
      "sentiment_change_7d": "+5"
    },
    "analyst_ratings": {
      "consensus": "买入",
      "upgrades_30d": 5,
      "downgrades_30d": 1,
      "target_price_upside": "15%"
    },
    "fund_flow": {
      "northbound_5d": "+12 亿",
      "institutional_flow": "净流入"
    }
  },
  "action_items": [
    "情绪温和乐观，无极端信号",
    "关注消费税政策动向",
    "若情绪降至 -60 以下（极度悲观），重点研究买入机会"
  ],
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。"
}
```

### 示例 2：市场整体情绪

**用户输入**：
```
当前 A 股市场情绪如何
```

**输出**：
```json
{
  "signal": {
    "sentiment_score": -35,
    "sentiment_level": "温和悲观",
    "trend": "恶化",
    "contrarian_signal": "否（接近反向信号区间）"
  },
  "confidence": {
    "score": 75,
    "level": "中",
    "data_coverage": "全市场数据，3000+ 股票"
  },
  "reasoning": {
    "key_findings": [
      "市场情绪持续走弱，7 日下降 18 分",
      "涨跌家数比 1:3，跌停家数增加",
      "但未达到极度悲观（-60 以下），反向信号未触发"
    ],
    "sentiment_drivers": [
      {
        "factor": "经济数据不及预期",
        "direction": "负面",
        "impact": "高",
        "description": "PMI 49.2，低于荣枯线"
      },
      {
        "factor": "政策预期落空",
        "direction": "负面",
        "impact": "中",
        "description": "市场期待的刺激政策未出台"
      },
      {
        "factor": "外资流出",
        "direction": "负面",
        "impact": "中",
        "description": "北向资金连续 3 日净流出"
      }
    ],
    "risks": [
      "情绪可能继续恶化",
      "外部风险（美联储政策）"
    ]
  },
  "metrics": {
    "market_breadth": {
      "advance_decline_ratio": "1:3",
      "limit_up_count": 25,
      "limit_down_count": 89
    },
    "sentiment_indicators": {
      "fear_greed_index": 32,
      "historical_percentile": "25%"
    }
  },
  "action_items": [
    "市场情绪温和悲观，接近反向信号区间",
    "若继续恶化至 -60 以下，启动逆向研究",
    "当前保持适度仓位，等待明确信号"
  ],
  "disclaimer": "⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。"
}
```

---

## 🔧 数据源

### 推荐 API

| 数据 | 来源 | 频率 |
|------|------|------|
| 新闻 | 财联社/华尔街见闻 API | 实时 |
| 社交媒体 | 雪球/微博（爬虫） | 每小时 |
| 分析师评级 | 东方财富 Choice | 日度 |
| 资金流向 | 港交所/东方财富 | 实时 |

### 缓存策略

```
- 新闻数据：缓存 1 小时
- 社交媒体：缓存 30 分钟
- 分析师评级：缓存 24 小时
- 资金流向：缓存 15 分钟
```

---

## ⚠️ 注意事项

### 1. 情绪陷阱

- ✅ 情绪是反向指标（极端时才有价值）
- ✅ 结合基本面分析
- ❌ 不单纯依赖情绪交易
- ❌ 不追逐热门情绪

### 2. 数据质量

- ✅ 多源交叉验证
- ✅ 识别水军/机器人帖子
- ❌ 避免单一平台数据
- ❌ 避免使用过时数据

### 3. 使用建议

- ✅ 情绪极端时重点关注
- ✅ 情绪与基本面背离时深入研究
- ✅ 定期跟踪情绪变化
- ❌ 不频繁交易（情绪波动快）

---

## 🔗 相关技能

- `risk-assessor` - 风险评估（情绪风险）
- `value-analyzer` - 价值分析（情绪 vs 价值）
- `decision-checklist` - 决策检查（情绪偏差）
- `future-forecaster` - 趋势预测（情绪周期）

---

*市场短期是投票机（情绪），长期是称重机（价值）。聪明的投资者利用情绪，而非被情绪利用。* 📊
