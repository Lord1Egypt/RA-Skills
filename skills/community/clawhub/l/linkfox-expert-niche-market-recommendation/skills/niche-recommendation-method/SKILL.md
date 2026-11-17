---
name: niche-recommendation-method
description: 细分市场推荐法：用极目数据发现关键词下的全部细分市场，按可配置标准评估进入价值，输出推荐清单。S0极目查细分市场→S1硬过滤→S2评分→S3排序输出。当用户提到细分市场推荐、市场进入评估、niche recommendation、sub-market analysis时触发。
---

# 细分市场推荐法

用极目数据发现关键词下的全部细分市场，按可配置标准评估每个市场的进入价值，输出推荐清单。

## 执行编排

L1{S0} → L2{S1} → L3{S2} → L4{S3}

## 流水线总览

| 步骤 | 标题 | 一句话 | 调用 | 依赖 | 用途 | 详情 |
|------|------|--------|------|------|------|------|
| S0 | 查细分市场 | 极目API分页取全量niche | linkfox-jiimore-get-niche-info-by-keyword | - | 细分市场列表 | steps/S0.md |
| S1 | 硬过滤 | 按参数淘汰不符合条件的市场 | 内部逻辑 | S0 | 过滤后的市场池 | steps/S1.md |
| S2 | 评分 | 5维度加权评分(0-100) | 内部逻辑 | S1 | 每个市场的综合得分 | steps/S2.md |
| S3 | 排序输出 | 分级推荐+排序+输出 | 内部逻辑 | S2 | 最终推荐清单 | steps/S3.md |

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| seedKeyword | 是 | - | 种子关键词 |
| marketplace | 否 | US | 站点（极目仅支持US/JP/DE） |
| minSearchVolume | 否 | 500 | 最低周搜索量 |
| monopolyThreshold | 否 | 0.60 | Top5点击占比阈值 |
| minBrands | 否 | 3 | 最低品牌数 |
| maxDeclineRate | 否 | -0.20 | 最大季度跌幅 |
| maxReturnRate | 否 | 0.10 | 最大退货率 |
| minPrice / maxPrice | 否 | null | 价格带 |
| maxCPC | 否 | null | 最高CPC |
| productCountMax | 否 | null | 商品数上限 |
| sortBy | 否 | demand | 排序：demand/growth/score |
| scoreWeights | 否 | 见CLAUDE.md | 评分权重 |
| profile | 否 | null | 预设模板名 |

## 输出字段

| 字段 | 来源 | 说明 |
|------|------|------|
| rank | S3排序 | 排名 |
| nicheTitle | S0 | 细分市场名称（英文） |
| translationZh | S0 | 中文翻译 |
| recommendation | S3 | 推荐等级（强烈推荐/推荐/谨慎考虑/不推荐） |
| score | S2 | 综合评分（0-100） |
| competition | S2 | 竞争度（低/中/高） |
| demand | S0 | 需求量 |
| searchVolumeWeekly | S0 | 周搜索量 |
| unitsSoldWeekly | S0 | 周销量 |
| productCount | S0 | 商品数 |
| brandCount | S0 | 品牌数 |
| top5ClickShare | S0 | Top5点击占比 |
| cpc | S0 | CPC中位数 |
| avgPrice | S0 | 均价 |
| growth | S0 | 季度增长率 |
| successfulLaunches | S0 | 半年新品成功数 |
| eliminationReason | S1 | 淘汰原因（仅被淘汰的市场有值） |

## 数据诚信原则

- 缺字段标注「未返回」，严禁编造
- 被淘汰的市场保留在输出中，标注淘汰原因
- 评分仅基于极目返回的原始字段
