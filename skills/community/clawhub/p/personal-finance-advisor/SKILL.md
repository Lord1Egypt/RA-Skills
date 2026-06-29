---
name: Personal Finance Advisor
slug: personal-finance-advisor
description: AI驱动的个人财务规划师。涵盖收支记账分析、预算规划、投资组合建议、税务优化、退休规划、保险配置六大模块。支持多币种、多账户聚合，让AI帮你管好每一分钱。
version: 1.0.0
author: ai-gaoqian
tags:
  - finance
  - personal-finance
  - budgeting
  - investment
  - tax-planning
metadata:
  openclaw:
    requires: []
    pricing:
      amount: 0.50
      currency: CNY
      interval: per-use
---

# Personal Finance Advisor

个人财务全生命周期管理技能。从月度记账到退休规划，覆盖个人财富管理的全部环节。

## 使用场景

- **收支分析**：导入银行/支付宝/微信账单，自动分类统计，生成可视化报表
- **预算规划**：按 50/30/20 法则或自定义比例设定月预算，超支预警
- **投资组合**：基于风险偏好（保守/稳健/进取）推荐资产配置方案，定期再平衡提醒
- **税务优化**：个税专项附加扣除梳理，年终奖计税方式比较，灵活用工税务建议
- **退休规划**：基于当前年龄、收入、预期支出计算养老金缺口和月储蓄目标
- **保险配置**：分析现有保单覆盖缺口，推荐重疾/医疗/意外/寿险配置优先级

## 数据安全

- 所有财务数据仅本地处理，不上传云端
- 敏感字段（账号、金额）自动脱敏显示
- 支持 CSV/OFX/QIF 格式导入，不直接连接银行 API

## 配置

```yaml
skills:
  personal-finance-advisor:
    currency: CNY
    tax_region: cn
    retirement_age: 60
    risk_profile: moderate
    budget_method: 50-30-20
```

## 示例指令

- "分析我上个月的支出分类占比"
- "我月入2万，想在5年内存够50万首付，每月该存多少？"
- "比较一下年终奖单独计税和合并计税哪个更划算"
- "给我推荐一个适合35岁稳健型投资者的ETF组合"
