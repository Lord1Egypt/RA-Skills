---
name: qiu-guolu-investor
version: 2.0.0
description: ［何时使用］当用户需要分析 A 股价值投资机会时；当用户问"邱国鹭怎么看这家公司"时；当需要进行估值/品质/时机分析时；当应用简单投资理念时
author: 燃冰 + 小蚂蚁
created: 2026-03-13
updated: 2026-03-19
skill_type: 核心
allowed-tools: [Read]
related_skills: [simple-investor, value-analyzer, moat-evaluator, stock-picker]
tags: [邱国鹭，简单投资，价值投资中国化，A 股]
---

# 邱国鹭简单投资智慧 📚

**基于《投资中最简单的事》《价值》- 邱国鹭**

---

## 📋 功能描述

基于邱国鹭的价值投资中国化理念分析投资机会。

**适用场景：**
- A 股价值投资分析
- 估值/品质/时机三要素分析
- 行业格局分析
- 简单投资理念应用

**边界条件：**
- 不替代深入研究
- 需配合财报分析
- A 股特色需考虑
- 周期股需特殊处理

---

## 🎯 核心理念

### 邱国鹭投资三要素

**1. 估值（便宜吗？）- 40%**
- PE/PB/PS 估值
- 历史估值比较
- 同业估值比较

**2. 品质（是好公司吗？）- 40%**
- ROE>15%
- 毛利率>30%
- 行业龙头

**3. 时机（现在能买吗？）- 20%**
- 市场情绪
- 行业周期
- 催化剂

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

- `references/qiu-principles.md` - 邱国鹭投资原则详解
- `examples/bank-analysis.md` - 银行股分析示例
- `examples/consumer-analysis.md` - 消费股分析示例
- `templates/simple-investing-template.md` - 简单投资分析模板

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

### 示例：贵州茅台分析

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
PE: 30 vs 历史中位 35 → 低估
PB: 12 vs 行业平均 8 → 合理
估值结论：合理

【品质分析】
ROE: 30% > 15% → 优秀
毛利率：90% > 30% → 优秀
行业地位：第 1 → 优秀
品质结论：优秀

【时机分析】
市场情绪：中性
估值位置：历史 40% 分位
建议：观察

【综合评分】7/10
```

---

## 📚 核心理念

**关键洞察：**
1. 投资就是估值、品质、时机
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

- `templates/simple-investing-template.md` - 简单投资模板
- `examples/analysis-examples.md` - 完整分析示例集
- `references/qiu-principles.md` - 邱国鹭投资原则参考

---

## 更新日志

- v2.0.0 (2026-03-19): 按照 SKILL-STANDARD-v2.md 重构，添加 Front Matter、坑点章节、相关资源 📚
- v1.0.0 (2026-03-13): 初始版本，邱国鹭投资智慧上线 📚

---

*投资中最简单的事：好公司、好价格、好时机。* 📚
---

## 🔧 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 不触发 | description 是否包含触发词？ | 将关键词加入 description |
| 运行失败 | 脚本有执行权限吗？ | `chmod +x scripts/*.py` |
| 数据获取失败 | 网络连接正常吗？ | 检查网络或 API 状态 |
| 数据不足 | Tushare 积分足够吗？ | 签到获取更多积分或使用免费数据源 |
| 输出异常 | 输入格式正确吗？ | 检查股票代码格式（如 600519.SH） |

