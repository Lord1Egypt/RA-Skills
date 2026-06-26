---
name: duan-yongping-investor
version: 2.0.0
description: ［何时使用］当用户需要分析企业文化和商业模式时；当用户问"段永平怎么看这家公司"时；当需要进行本分/能力圈/长期主义分析时
author: 燃冰 + 小蚂蚁
created: 2026-03-13
updated: 2026-03-19
skill_type: 核心
allowed-tools: [Read]
related_skills: [moat-evaluator, value-analyzer, decision-checklist, stock-picker]
tags: [段永平，本分，能力圈，长期主义，价值投资]
---

# 段永平投资智慧 🧘

**基于段永平（步步高、OPPO、vivo 创始人）投资理念**

---

## 📋 功能描述

基于段永平投资理念分析企业，强调"本分"、"能力圈"、"长期主义"。

**适用场景：**
- 企业文化分析
- 商业模式评估
- 能力圈检查
- 长期投资价值判断

**边界条件：**
- 不替代深入研究
- 需配合财务分析
- 文化分析主观性强
- 需长期跟踪验证

---

## 🎯 核心理念

### 段永平投资三原则

**1. 本分（40%）**
- 做对的事情
- 把事情做对
- 诚信为本

**2. 能力圈（30%）**
- 只投资自己懂的公司
- 不懂不投
- 持续学习扩大能力圈

**3. 长期主义（30%）**
- 买入并持有 10 年+
- 忽视短期波动
- 关注长期价值

---

## ⚠️ 常见错误

**错误 1：忽视企业文化**
```
问题：
• 只看财务数据
• 忽视企业文化
• 忽视管理层诚信

解决：
✓ 企业文化是核心
✓ 关注"本分"程度
✓ 长期跟踪验证
```

**错误 2：能力圈外投资**
```
问题：
• 投资不懂的公司
• 盲目跟风
• 忽视能力圈边界

解决：
✓ 只投懂的公司
✓ 持续学习
✓ 承认无知
```

**错误 3：短期思维**
```
问题：
• 频繁交易
• 忽视长期价值
• 被短期波动影响

解决：
✓ 长期持有 10 年+
✓ 忽视短期波动
✓ 关注基本面
```

**错误 4：忽视商业模式**
```
问题：
• 忽视商业模式质量
• 投资辛苦赚钱的公司
• 忽视现金流

解决：
✓ 选择容易赚钱的生意
✓ 关注现金流
✓ 选择轻资产模式
```

**错误 5：价格与价值混淆**
```
问题：
• 只看价格不看价值
• 好公司也要好价格
• 忽视安全边际

解决：
✓ 价值优先
✓ 等待好价格
✓ 保持耐心
```

---

## 🔗 相关资源

- `references/duan-principles.md` - 段永平投资原则详解
- `examples/apple-analysis.md` - 苹果案例分析
- `examples/kweichow-analysis.md` - 茅台案例分析
- `templates/culture-analysis-template.md` - 企业文化分析模板

---

## 📊 输入参数

```json
{
  "company_name": {
    "type": "string",
    "required": true,
    "description": "公司名称"
  },
  "business_model": {
    "type": "string",
    "required": true,
    "description": "商业模式描述"
  },
  "culture_examples": {
    "type": "array",
    "items": {"type": "string"},
    "required": false,
    "description": "企业文化案例列表"
  },
  "competitive_advantage": {
    "type": "string",
    "required": true,
    "description": "竞争优势"
  },
  "pe_ratio": {
    "type": "number",
    "required": false,
    "description": "市盈率"
  }
}
```

---

## 📤 输出格式

```json
{
  "status": "success",
  "data": {
    "business_model_analysis": {
      "score": 0,
      "max_score": 5,
      "assessment": ""
    },
    "culture_analysis": {
      "benfen_score": 0,
      "max_score": 5,
      "assessment": ""
    },
    "moat_analysis": {
      "exists": true,
      "type": "",
      "strength": 0
    },
    "valuation_analysis": {
      "pe_assessment": "低估 | 合理 | 高估",
      "recommendation": ""
    },
    "investment_score": 0,
    "max_score": 10
  }
}
```

---

## 🧪 使用示例

### 示例：苹果公司分析

**输入：**
```
公司名称：苹果
商业模式：硬件 + 软件 + 服务生态
企业文化案例：
- 用户隐私保护
- 产品极致体验
- 长期研发投入
竞争优势：品牌 + 生态 + 技术
市盈率：25
```

**输出：**
```
【商业模式分析】
评分：5/5
理由：
- 赚钱容易（高毛利）
- 现金流充沛
- 轻资产模式
- 强定价权

【企业文化分析（本分检查）】
评分：5/5
理由：
- 用户隐私保护（本分）
- 产品极致体验（把事情做对）
- 长期研发投入（长期主义）

【护城河分析】
存在：是
类型：品牌 + 网络效应 + 转换成本
强度：5/5

【估值分析】
PE: 25 vs 历史平均 20 → 合理
建议：观察

【综合评分】9/10
```

---

## 📚 核心理念

**关键洞察：**
1. 本分是企业文化核心
2. 只投懂的公司
3. 长期持有 10 年+
4. 好生意赚钱容易
5. 价格围绕价值波动

**健康公式：**
```
好投资 = 本分 × 能力圈 × 长期主义
```

---

## 🔗 相关文件

- `templates/culture-analysis-template.md` - 企业文化分析模板
- `examples/culture-examples.md` - 完整文化分析示例集
- `references/duan-principles.md` - 段永平投资原则参考

---

## 更新日志

- v2.0.0 (2026-03-19): 按照 SKILL-STANDARD-v2.md 重构，添加 Front Matter、坑点章节、相关资源 🧘
- v1.0.0 (2026-03-13): 初始版本，段永平投资智慧上线 🧘

---

*本分是做对的事情，把事情做对。只投懂的公司，长期持有 10 年+。* 🧘
---

## 🔧 故障排查

| 问题 | 检查项 | 解决方案 |
|------|--------|---------|
| 不触发 | description 是否包含触发词？ | 将关键词加入 description |
| 运行失败 | 脚本有执行权限吗？ | `chmod +x scripts/*.py` |
| 数据获取失败 | 网络连接正常吗？ | 检查网络或 API 状态 |
| 数据不足 | Tushare 积分足够吗？ | 签到获取更多积分或使用免费数据源 |
| 输出异常 | 输入格式正确吗？ | 检查股票代码格式（如 600519.SH） |

