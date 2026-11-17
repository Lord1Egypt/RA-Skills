---
name: competitor-selector
description: 竞品筛选算法Skill：输入ASIN+站点，自动判定商品类型（标品/非标品/混合），经核心流量词提取→候选池生成→价格过滤→重合度过滤→三模型评分（直接竞品6维/上升潜力股5维/标杆头部5维），最终锁定5-10个核心竞品。当用户提到找竞品、竞品筛选、竞品选择、选竞品、competitor selection、竞品调研第一步、自动找竞品时触发。即使用户没说"算法"，只要需求是从一个ASIN出发找到对其竞品也应触发；一次性手动查竞品不触发。
---

## 适用与不适用

适用于：从目标ASIN出发，通过算法自动筛选出5-10个核心竞品（直接竞品+标杆头部+上升潜力股），可重复执行，产出结构化竞品列表。不适用：手动指定竞品做深度分析（直接用竞品调研skill）；一次性查某个ASIN的相似商品（用linkfox-sellersprite-competitor-lookup）；纯选品调研无对标ASIN。

## 输入参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| asin | string | 必填 | 目标ASIN |
| marketplace | string | US | 站点代码 |
| product_type | string | auto | auto(自动判定) / standard(标品) / non-standard(非标品) / mixed(混合) |
| price_tolerance | float | 0.2 | 价格浮动比例，默认±20% |
| overlap_threshold | float | 0.8 | 功能/外观重合度阈值 |
| max_competitors | int | 10 | 最终竞品数量上限 |

## 执行编排

L1{S1, S2} → L2{S3} → L3{S4} → L4{S5} → L5{S6}

S1和S2可并行：S1反查流量词的同时，S2拉取目标ASIN详情和主图用于后续判定。

## 流水线

| 步骤 | 做什么 | 调用 | 依赖 | 用途 | 详情 |
|------|--------|------|------|------|------|
| S0 商品类型判定 | 判定标品/非标品/混合 | linkfox-amazon-product-detail | 无 | 决定S2-S4路径 | `references/steps/S0.md` |
| S1 识别核心流量词 | 反查流量词，搜索量×流量占比加权取TOP8 | linkfox-sellersprite-traffic-keyword | 无 | S2标品/混合路径候选池 | `references/steps/S1.md` |
| S2 生成候选池 | 标品:前台搜索 / 非标品:以图搜图 / 混合:双路并行 | linkfox-amazon-search + linkfox-amazon-search-by-image | S0,S1 | S3价格过滤 | `references/steps/S2.md` |
| S3 价格+Keepa过滤 | Keepa实时价±tolerance，拉取历史数据 | linkfox-keepa-product-request | S2 | S4重合度过滤 | `references/steps/S3.md` |
| S4 重合度过滤 | 标品:AIGC功能对比 / 非标品:AIGC外观对比 / 混合:交叉比对 | linkfox-aigc-textgen + linkfox-amazon-product-detail | S3 | S4b/S5评分 | `references/steps/S4.md` |
| S4b ABA反查 | 对核心候选反查ABA TOP3上榜词 | linkfox-aba-intelligent-query | S4 | S5标杆评分 | `references/steps/S4b.md` |
| S5 三模型评分 | 直接竞品6维+潜力股5维+标杆5维 | `scripts/competitor_selector.py` | S4,S4b | S6最终选择 | `references/steps/S5.md` |
| S6 锁定输出 | 按类型和评分排序，锁定5-10个 | agent判断 | S5 | 最终交付 | `references/steps/S6.md` |

## 评分模型概要

完整规则见 `references/scoring-model.md`。

**直接竞品6维**（可达性模型）：BSR差距20% + 评论数差距15% + 转化率差距15% + 价格竞争力10% + 功能重合度25% + 上架时间10%。总分≥3.5入选。S4 AIGC重合度≥0.80为硬性前置条件。转化率从卖家精灵purchaseRate按流量占比加权聚合。

**上升潜力股5维**（增长性模型）：销量增长趋势35% + 评论成长空间20% + BSR改善20% + 转化率表现15% + 上架时间10%。总分≥3.5入选。硬性排除：当月销量=0、Deal尖峰、上架<3月、BSR>50000。转化率从卖家精灵聚合。

**标杆头部5维**（领先度模型）：BSR领先度25% + 评论壁垒20% + 销量规模20% + ABA统治力20% + 价格相关性15%。总分≥3.5入选。硬性门槛：至少1维显著领先目标。

## 商品类型判定规则

| 类型 | 判定依据 | S2路径 | S4路径 |
|------|----------|--------|--------|
| 标品 | 有明确规格参数(容量/尺寸/版本/功率)，功能可量化对比 | 关键词搜索 | AIGC功能对比 |
| 非标品 | 外观/设计是主要差异化，规格模糊 | 以图搜图 | AIGC外观对比 |
| 混合 | 既有规格参数又有强外观属性 | 双路并行 | 交叉比对 |

## 输出

最终交付JSON文件，包含三类竞品：
```json
{
  "target_asin": "B0XXXXX",
  "product_type": "standard",
  "direct_competitors": [{"asin":"...","brand":"...","score":4.2,...}],
  "rising_stars": [{"asin":"...","brand":"...","score":3.8,...}],
  "benchmarks": [{"asin":"...","brand":"...","score":4.0,...}],
  "summary": {"total": 7, "direct": 4, "rising": 1, "benchmark": 2}
}
```

## 局限性

- ABA反查需调用linkfox-aba-intelligent-query（按ASIN反查上榜词），积分消耗较大
- AIGC多模态对比每次最多9张图（1目标+9候选），候选超9个需分批
- 非标品路径的以图搜图仅支持8个站点（US/UK/DE/FR/IT/ES/JP/IN）
- 商品类型自动判定基于规格表字段数量+标题关键词，准确率约80%，建议用户确认

## 报告产物

如需生成竞品筛选报告，handoff给linkfox-report-generator。

⚠ 生成报告必须先阅读 SKILL `linkfox-report-generator` 并遵循其规范：样式、排版、md/html 导出、元信息块统统由它负责，本 skill 不得复制报告样式或 html 模板。
