---
name: simple-investor
version: 2.0.0
description: ［何时使用］当用户需要分析 A 股公司时；当用户问"这家公司便宜吗"时；当进行价值投资分析时；当需要选股三要素分析时
author: 燃冰 + 小蚂蚁
created: 2026-03-13
updated: 2026-03-19
skill_type: 全球配置
allowed-tools: [Bash, Read, Exec]
related_skills: [value-analyzer, stock-picker, moat-evaluator, decision-checklist]
tags: [价值投资，A 股，邱国鹭，选股三要素]
---

# 简单投资者 📈

**基于《投资中最简单的事》- 邱国鹭**

---

## 📋 功能描述

价值投资中国化，选股三要素分析（估值、品质、时机）。

**适用场景：**
- A 股公司分析
- 估值分析
- 品质分析
- 时机判断

**边界条件：**
- 不替代深入研究
- 需配合财报分析
- A 股特色需考虑
- 周期股需特殊处理

---

## 🎯 核心功能

### 功能 1：估值分析（便宜吗？）

**4 大估值指标：**

| 指标 | 当前 | 历史中位 | 评估 |
|------|------|---------|------|
| PE | X | Y | 低估/合理/高估 |
| PB | X | Y | 低估/合理/高估 |
| PS | X | Y | 低估/合理/高估 |
| 股息率 | X% | Y% | 低估/合理/高估 |

**估值结论：** 便宜/合理/贵

### 功能 2：品质分析（好公司吗？）

**4 大品质指标：**

| 指标 | 当前 | 标准 | 评估 |
|------|------|------|------|
| ROE | X% | >15% | 优秀/良好/一般/差 |
| 毛利率 | X% | >30% | 优秀/良好/一般/差 |
| 净利率 | X% | >10% | 优秀/良好/一般/差 |
| 行业地位 | 前 X | 前 3 | 优秀/良好/一般/差 |

**品质结论：** 优秀/良好/一般/差

### 功能 3：时机分析（现在能买吗？）

**时机判断：**
- 市场情绪：贪婪/恐惧
- 估值位置：历史百分位
- 行业周期：上行/下行
- 催化剂：有/无

**投资建议：** 买入/观察/回避

---

## ⚠️ 常见错误

**错误 1：只看估值不看品质**
```
问题：
• 买便宜烂公司
• 忽视 ROE 和毛利率
• 价值陷阱

解决：
✓ 估值 + 品质结合
✓ ROE>15% 是底线
✓ 避免价值陷阱
```

**错误 2：忽视 A 股特色**
```
问题：
• 用美股标准看 A 股
• 忽视政策影响
• 忽视散户情绪

解决：
✓ 考虑 A 股估值体系
✓ 关注政策导向
✓ 利用散户情绪
```

**错误 3：周期股误判**
```
问题：
• 周期股用 PE 估值
• 高点买入周期股
• 低点卖出周期股

解决：
✓ 周期股用 PB 估值
✓ 低 PE 时卖出
✓ 高 PE 时买入
```

**错误 4：忽视行业格局**
```
问题：
• 忽视行业集中度
• 忽视竞争格局
• 忽视进入壁垒

解决：
✓ 关注行业前 3 名
✓ 选择龙头公司
✓ 关注进入壁垒
```

**错误 5：时机判断错误**
```
问题：
• 高位追涨
• 低位割肉
• 忽视市场情绪

解决：
✓ 逆向投资
✓ 别人贪婪我恐惧
✓ 别人恐惧我贪婪
```

---

## 🔗 相关资源

- `references/value-investing-china.md` - 价值投资中国化详解
- `examples/bank-analysis.md` - 银行股分析示例
- `examples/consumer-analysis.md` - 消费股分析示例
- `templates/stock-analysis-template.md` - A 股分析模板

---

## 📊 输入参数

```json
{
  "company_name": {
    "type": "string",
    "required": true,
    "description": "公司名称"
  },
  "pe_ratio": {
    "type": "number",
    "required": true,
    "description": "市盈率"
  },
  "pb_ratio": {
    "type": "number",
    "required": true,
    "description": "市净率"
  },
  "roe": {
    "type": "number",
    "required": true,
    "description": "净资产收益率（%）"
  },
  "industry_position": {
    "type": "string",
    "required": true,
    "description": "行业地位"
  },
  "historical_pe_range": {
    "type": "object",
    "properties": {
      "min": {"type": "number"},
      "max": {"type": "number"},
      "median": {"type": "number"}
    },
    "required": false
  }
}
```

---

## 📤 输出格式

```json
{
  "status": "success",
  "data": {
    "valuation_analysis": {
      "pe_assessment": "低估 | 合理 | 高估",
      "pb_assessment": "低估 | 合理 | 高估",
      "conclusion": "便宜 | 合理 | 贵"
    },
    "quality_analysis": {
      "roe_assessment": "优秀 | 良好 | 一般 | 差",
      "margin_assessment": "优秀 | 良好 | 一般 | 差",
      "position_assessment": "优秀 | 良好 | 一般 | 差",
      "conclusion": "优秀 | 良好 | 一般 | 差"
    },
    "timing_analysis": {
      "market_sentiment": "贪婪 | 恐惧",
      "valuation_percentile": 0,
      "recommendation": "买入 | 观察 | 回避"
    },
    "investment_score": 0,
    "max_score": 10
  }
}
```

---

## 🧪 使用示例

### 示例 1：贵州茅台分析

**输入：**
```
公司名称：贵州茅台
市盈率：30
市净率：12
ROE: 30%
行业地位：第 1
历史 PE 范围：20-50，中位 35
```

**输出：**
```
【估值分析】

| 指标 | 当前 | 历史中位 | 评估 |
|------|------|---------|------|
| PE | 30 | 35 | 低估 |
| PB | 12 | 10 | 合理 |
| 股息率 | 1.5% | 1.5% | 合理 |

估值结论：合理

【品质分析】

| 指标 | 当前 | 标准 | 评估 |
|------|------|------|------|
| ROE | 30% | >15% | 优秀 |
| 毛利率 | 90% | >30% | 优秀 |
| 净利率 | 50% | >10% | 优秀 |
| 行业地位 | 第 1 | 前 3 | 优秀 |

品质结论：优秀

【时机分析】

市场情绪：中性
估值位置：历史 40% 分位
行业周期：稳定

【投资建议】

建议：观察
理由：
1. 估值合理，不便宜
2. 品质优秀
3. 等待更好价格
4. 长期持有价值高

风险：
- 估值风险
- 政策风险
- 增长放缓
```

---

## 📚 核心理念

**关键洞察：**
1. 估值 + 品质 + 时机三要素
2. 好公司 + 好价格=好投资
3. A 股有自身估值体系
4. 周期股逆向操作
5. 别人恐惧我贪婪

**健康公式：**
```
好投资 = 好公司 × 好价格 × 好时机
```

---

## 🔗 相关文件

- `templates/stock-analysis-template.md` - A 股分析模板
- `examples/analysis-examples.md` - 完整分析示例集
- `references/value-investing-china.md` - 价值投资中国化参考

---

## 更新日志

- v2.0.0 (2026-03-19): 按照 SKILL-STANDARD-v2.md 重构，添加 Front Matter、坑点章节、相关资源 📈
- v1.0.0 (2026-03-13): 初始版本，简单投资者上线 📈

---

*投资中最简单的事：好公司、好价格、好时机。* 📈
---

## 🔧 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 不触发 | description 是否包含触发词？ | 将关键词加入 description |
| 运行失败 | 脚本有执行权限吗？ | `chmod +x scripts/*.py` |
| 数据获取失败 | 网络连接正常吗？ | 检查网络或 API 状态 |
| 数据不足 | Tushare 积分足够吗？ | 签到获取更多积分或使用免费数据源 |
| 输出异常 | 输入格式正确吗？ | 检查股票代码格式（如 600519.SH） |

