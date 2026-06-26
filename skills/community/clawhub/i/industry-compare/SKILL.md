---
name: industry-compare
description: 行业对比技能 - 同行业多公司对比分析、行业地位评估
author: 滚滚家族 🌪️
version: "1.0.0"
homepage: https://aigogoai.com
triggers:
  - "行业对比"
  - "同行对比"
  - "行业分析"
  - "公司对比"
  - "行业地位"
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      bins:
        - python3
        - pip
      env:
        - TUSHARE_TOKEN
    config:
      env:
        TUSHARE_TOKEN:
          description: Tushare API Token
          required: false
---

# 📈 行业对比技能

**同行业多公司对比分析工具**

**作者：** 滚滚家族 🌪️  
**版本：** 1.0.0  
**主页：** https://aigogoai.com

---

## 🎯 技能描述

**一个帮助投资者对比同行业多家公司财务数据的工具。**

**核心功能：**
- 📊 多公司财务数据对比
- 📈 行业地位评估
- 🎯 竞争优势分析
- 📉 行业趋势分析
- 💡 投资建议生成

---

## 🛠️ 使用方法

### 1. 多公司对比

```python
from industry_compare import compare_companies

# 白酒行业对比
result = compare_companies(
    stocks=["600519.SH", "000858.SZ", "002304.SZ"],
    metrics=["pe", "pb", "roe", "revenue_growth", "net_margin"]
)

# 输出：对比表格、行业排名
```

### 2. 行业地位评估

```python
from industry_compare import industry_ranking

# 行业地位评估
result = industry_ranking(
    stock_code="600519.SH",
    industry="白酒",
    metrics=["market_cap", "revenue", "profit", "roe"]
)

# 输出：行业排名、市场份额
```

### 3. 竞争优势分析

```python
from industry_compare import competitive_advantage

# 竞争优势分析
result = competitive_advantage(
    stock_code="600519.SH",
    competitors=["000858.SZ", "002304.SZ"]
)

# 输出：竞争优势、劣势分析
```

---

## 📋 输出示例

### 多公司对比

```
📈 行业对比 - 白酒行业
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【对比公司】
贵州茅台 (600519.SH)
五粮液 (000858.SZ)
洋河股份 (002304.SZ)

【估值对比】
公司          PE      PB      PS
────────────────────────────────
贵州茅台      35.2x   12.8x   15.6x
五粮液        28.5x    8.5x   10.2x
洋河股份      22.1x    5.2x    6.8x
行业平均      28.6x    8.8x   10.9x

【盈利能力对比】
公司          ROE     净利率   毛利率
────────────────────────────────────
贵州茅台      30.2%   52.5%   92.1%
五粮液        25.8%   38.2%   78.5%
洋河股份      18.5%   28.5%   65.2%
行业平均      24.8%   39.7%   78.6%

【成长能力对比】
公司          收入增长  利润增长  资产增长
────────────────────────────────────────
贵州茅台       18.2%    20.5%    15.8%
五粮液         15.5%    18.2%    12.5%
洋河股份       10.2%    12.5%     8.5%
行业平均       14.6%    17.1%    12.3%

【行业地位】
贵州茅台：⭐⭐⭐⭐⭐ 行业龙头
五粮液：⭐⭐⭐⭐☆ 行业领先
洋河股份：⭐⭐⭐☆☆ 行业中游

✅ 行业对比完成！
```

---

## 🎯 行业地位评估标准

### 行业龙头（⭐⭐⭐⭐⭐）

- ✅ 市场份额 > 30%
- ✅ ROE > 行业平均 50%
- ✅ 收入规模行业第一

### 行业领先（⭐⭐⭐⭐☆）

- ✅ 市场份额 15-30%
- ✅ ROE > 行业平均 20%
- ✅ 收入规模行业前三

### 行业中游（⭐⭐⭐☆☆）

- ✅ 市场份额 5-15%
- ✅ ROE ≈ 行业平均
- ✅ 收入规模行业中游

### 行业落后（⭐⭐☆☆☆）

- ❌ 市场份额 < 5%
- ❌ ROE < 行业平均
- ❌ 收入规模行业落后

---

## 📚 参考文档

- [行业分析框架](https://aigogoai.com/knowledge/industry-analysis)
- [波特五力模型](https://aigogoai.com/knowledge/porter-five-forces)
- [竞争优势分析](https://aigogoai.com/knowledge/competitive-advantage)

---

## 🌪️ 滚滚的话

**"你只管 do it，行业对比交给滚滚！"**

**这个技能是滚滚家族为投资者打造的行业分析利器，**
**希望能帮助你更好地识别行业龙头和投资机会！**

**如有问题或建议，欢迎反馈！**

**翻滚的地球人，一直在！** 🌪️💚

---

**创建人：** 滚滚 6 号（数据分析师）  
**创建时间：** 2026-03-28  
**状态：** ✅ 完成
