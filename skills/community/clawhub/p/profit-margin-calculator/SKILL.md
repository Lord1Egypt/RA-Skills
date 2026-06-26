---
name: profit-margin-calculator
description: Calculate true ecommerce profit margin after product cost, shipping, platform fees, discounts, and refund drag. Use when teams need a fast profitability reality check.
---

# Profit Margin Calculator

不要只看毛利，要看最后真正剩下多少。

## 先交互，再计算

开始前先确认：
1. 你要看的是 gross margin、contribution margin，还是 net margin？
2. 你们平时利润率口径里，是否包含：
   - 运费 / 包装
   - 平台费 / 支付费
   - 折扣 / 补贴
   - 退款 / 售后损耗
   - 固定成本分摊
3. 你想沿用你们现有算法，还是让我给推荐的电商利润拆解方式？

如果用户没有统一口径，先给推荐框架，再让用户确认。

## Python script guidance

当用户给出结构化数字后：
- 生成 Python 脚本完成利润拆解
- 先列公式与假设
- 再返回毛利 / 净利结果
- 同时返回可复用脚本

如果输入不完整，先追问，不要直接输出看似精确的结果。

## 解决的问题

很多团队说“这个产品利润不错”，其实只算了售价减进货价，没把这些算进去：
- 运费和包装；
- 平台手续费；
- 折扣、券、活动补贴；
- 退款和售后损耗；
- 必要时还要分摊基础运营成本。

这个 skill 的目标是：
**把利润率从一个粗数字，变成一张真正能用于经营判断的 margin 拆解。**

## 何时使用

- 对比多个 SKU 利润健康度；
- 定价前确认是否还有空间；
- 发现营收增长但利润不涨时做排查。

## 输入要求

- 售价
- 商品成本
- 运费 / 包装 / 仓储等履约成本
- 平台费 / 支付费 / 渠道费
- 折扣或优惠
- 退款率 / 售后损耗
- 可选：固定成本分摊

## 工作流

1. 明确用户的 margin 口径。
2. 计算毛利与毛利率。
3. 扣除履约、渠道、折扣、退款影响。
4. 输出净利润与净利率。
5. 标记利润被侵蚀最严重的环节。
6. 返回可复用 Python 脚本。

## 输出格式

1. 成本拆解表
2. 毛利 / 净利结果
3. Margin 风险点
4. 优化建议
5. Python 脚本

## 质量标准

- 不混淆 gross margin 和 net margin。
- 清楚指出利润被谁吃掉。
- 结果可用于 SKU 比较或经营复盘。
- 明确哪些数字是估算值。
- 未确认口径前不要假装精确。

## 资源

参考 `references/output-template.md`。
