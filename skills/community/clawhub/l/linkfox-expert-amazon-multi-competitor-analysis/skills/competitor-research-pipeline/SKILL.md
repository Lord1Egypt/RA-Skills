---
name: competitor-research-pipeline
description: 竞品调研全流程Tier3 SOP：输入ASIN+站点，端到端完成竞品筛选（三路径算法）→全量数据采集（Keepa+卖家精灵+ABA+VOC四源并行）→交叉分析（首页词归因+ABA TOP3对比+SWOT）→HTML深度报告。当用户提到竞品调研、竞品全景分析、竞品深度报告、竞品全流程、competitor research、竞品对标分析时触发。即使用户没说"全流程"，只要需求是从一个ASIN出发做完整竞品调研并出报告也应触发；单步查询不触发。
---

## 适用与不适用

适用于：从目标ASIN出发，端到端完成竞品筛选+数据采集+分析+报告，产出HTML深度竞品调研报告。不适用：只找竞品不出报告（用competitor-selector）；只查单个ASIN数据（直接调对应skill）；选品调研无对标ASIN（用niche-radar）。

## 输入参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| asin | string | 必填 | 目标ASIN |
| marketplace | string | US | 站点代码 |
| product_type | string | auto | auto/standard/non-standard/mixed |
| max_competitors | int | 10 | 竞品数量上限 |
| enable_voc | bool | true | 是否采集VOC评论（top3竞品）|

## 执行编排

L1{S1} → L2{S2,S3,S4,S5} → L3{S6,S6b,S6c,S7} → L4{S8} → L5{S9}

- L1: 竞品筛选（决策点，需agent判断商品类型和确认竞品名单）
- L2: 四源数据并行采集（确定性链，可打包到run_pipeline.py）
- L3: 交叉分析（决策点，需agent判断分析重点）
- L4: SWOT综合研判（agent判断）
- L5: 报告生成（handoff report-generator）

## 流水线

| 步骤 | 做什么 | 调用 | 依赖 | 用途 | 详情 |
|------|--------|------|------|------|------|
| S1 竞品筛选 | 三路径算法筛选5-10个核心竞品 | competitor-selector + linkfox-sellersprite-traffic-keyword + linkfox-amazon-search + linkfox-keepa-product-request + linkfox-aigc-textgen | 无 | L2全部步骤 | `references/steps/S1.md` |
| S2 Keepa历史 | 批量拉取目标+竞品Keepa数据(history=1) | linkfox-keepa-product-request | S1 | S6,S7,S8 | `references/steps/S2.md` |
| S3 卖家精灵流量词 | 反查全部ASIN流量词(含翻页) | linkfox-sellersprite-traffic-keyword | S1 | S6,S7 | `references/steps/S3.md` |
| S4 ABA反查 | 按ASIN反查ABA TOP3上榜词 | linkfox-aba-intelligent-query | S1 | S7 | `references/steps/S4.md` |
| S5 VOC评论 | 采集目标+TOP3竞品评论 | linkfox-voc-review-analysis | S1 | S8 | `references/steps/S5.md` |
| S6 首页词归因 | 唯一首页词vs重复首页词分析 | `scripts/keyword_overlap_analyzer.py` | S2,S3 | S8 | `references/steps/S6.md` |
| S6b 竞品横向对比 | 8维度横向对比(销量趋势/份额/Deal/稳定性/季节性/BSR动量/弹性/功能参数) | `scripts/competitor_comparison_analyzer.py` | S2,S3,S4 | S8 | `references/steps/S6b.md` |
| S6c A+与商品图分析 | A+模块对比+商品图策略对比+AIGC视觉分析+优化方案 | linkfox-aigc-textgen | S2 | S8 | `references/steps/S6c.md` |
| S7 ABA交叉对比 | ABA TOP3上榜词跨ASIN对比 | `scripts/aba_overlap_analyzer.py` | S3,S4 | S8 | `references/steps/S7.md` |
| S8 SWOT研判 | 综合全部数据做SWOT+行动建议 | agent判断 | S2-S7 | S9 | `references/steps/S8.md` |
| S9 报告生成 | JSON数据→自动生成HTML片段→注入模板 | `scripts/generate_report_fragment.py` + linkfox-report-generator | S2-S8 | 最终交付 | `references/steps/S9.md` |

## 报告章节结构（标准模板）

1. 报告头部 + KPI卡片（目标ASIN核心指标：售价/BSR/评论/月销/转化率/ABA词数）
2. 竞品筛选结果（三模型评分表+入选理由+竞品类型标签）
3. 市场全景（价格分布图/评分分布图/BSR对比图/销量趋势图 — 静态市场画像）
4. 竞品对比矩阵（多ASIN参数级并排大表：价格/BSR/评论/转化率/月销/变体/利润率/FBA费 — 参数级快照对比）
5. 竞品横向对比（8维度动态趋势分析：销量趋势/市场份额变动/Deal冲击波/销量稳定性/季节性/BSR动量/价格弹性/功能参数 — 每维度含ECharts图表）
6. 流量关键词分析（首页词归因：唯一vs重复对比+竞争战场TOP15+核心词排名交叉对比）
7. ABA TOP3分析（上榜词数对比+#1词分布+交叉战场表）
8. A+内容与商品图分析（A+模块对比+商品图策略对比+AIGC视觉分析+优化方案）
9. VOC评论洞察（好评高频卖点+差评痛点分类+未满足需求）
10. SWOT分析（优势/劣势/机会/威胁 — 每条有数据支撑）
11. 核心发现与行动建议（优先级分级：高/中/低 — 每条有数据支撑+可执行）

## 与competitor-selector的关系

competitor-selector是本skill的S1子流程。本skill在筛选基础上增加了：全量数据采集、交叉分析、VOC洞察、HTML报告生成，是完整的端到端SOP。

## 局限性

- 全流程积分消耗较大（预估800-1500积分，取决于竞品数和VOC采集范围）
- ABA反查每个ASIN需单独调用，6个ASIN约消耗40,000积分
- 卖家精灵流量词翻页消耗：首页6×15=90 + 翻页约9×15=135
- 非标品路径的AIGC对比有延迟（GEM_3_FLASH约10秒/批，GEM_3_1_PRO约30秒/次）
- 报告生成时间约30-60秒

## 报告产物

⚠ 生成报告必须先阅读 SKILL `linkfox-report-generator` 并遵循其规范：样式、排版、md/html 导出、元信息块统统由它负责，本 skill 不得复制报告样式或 html 模板。
