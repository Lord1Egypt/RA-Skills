# 选品 skills

**7 个 skill**，覆盖 4 种端到端选品流程（关键词选品 / 潜在爆款预测 / 条件选品 / 对标选品 / 跨平台选品）+ 词库 + 以图找竞品。

**归属 agent（重要）**：本桶 **7 个中有 6 个只挂在专业 agent**（`linkfox-product-selection-agent` 或 `linkfox-market-analysis-agent`），`default` 只有 `linkfox-image-competitor-scout` 一个。

**用什么 agent**：
- 想跑完整选品流程 → **必须** `--model linkfox-product-selection-agent`
- 只是"以图找竞品"这种轻量场景 → `default` 也行（含 `linkfox-image-competitor-scout`）

## Skills

| skill | 用途 | 触发短语（例） | 入参（关键字段） | 返回摘要 | 归属 agent |
|---|---|---|---|---|---|
| `linkfox-image-competitor-scout` | 以图/链接跨平台找同类竞品并出选品表 | "图片找竞品"/"这个链接在别的平台有没有同类"/"以图搜货" | `imageUrl`或`productUrl`, `platform`, `site`, `top_n` | 该平台竞品 Top N：主图·标题·商品ID·价格·销量·销售额·品类·配送 | default / selection |
| `linkfox-keyword-library` | 查用户自建关键词词库列表与词条 | "查词库"/"看我的词库"/"keyword library" | `action`(listLibraries/getWords), `libraryId`或`libraryName`, `name` | 词库清单（名称/类型/词条数）或词条明细（word/标签/渠道/备注） | market |
| `linkfox-keyword-select` | 关键词选品：一个词=一个细分市场 | "关键词选品"/"这个词能做吗"/"哪些词值得做" | `platform`, `site`, `seed`, `candidateLimit`, `topProductLimit` | 候选市场清单：keyword·需求·竞争·价格带·funnelVerdict·代表商品 Top3 | selection |
| `linkfox-viral-predict` | 三维（宏观/中观/微观）预测潜在爆款并评分 | "爆款预测"/"哪些品会爆"/"潜力选品" | `platform`, `site`, `seed`, `operation_mode`, `top_n`, `risk_check_top_k` | 候选清单：asin·主图·价格·viralScore·tier·三维子分·IP风险等级 | selection |
| `linkfox-product-condition-selection` | 按预设模式/阈值供给端正向筛品 | "按条件选品"/"销量飙升榜"/"低价长尾选品" | `platform`, `site`, `category`, `mode`(13预设)或自定义阈值, `top_n` | 候选商品 items[]+mode_info：标题·商品ID·价格·月销·命中依据·季节性提示 | selection |
| `linkfox-benchmark-product-selection` | 以对标竞品为锚扩出竞品面并做价值判断 | "对标选品"/"按ASIN对标"/"找同款竞品" | `platform`, `site`, `productIds`或`productUrl`或`imageUrl`, `top_n`, `sort_by` | 竞品列表：商品ID·主图·价格·销量·评分·竞品来源·相似度·跟进建议四档 | selection |
| `linkfox-cross-platform-product-selection` | 源平台筛品→目标平台图/标题相似匹配→对比报告 | "跨平台选品"/"1688搬到Amazon"/"跨平台搬品" | `sourcePlatform`/`site`, `targetPlatform`/`site`, `category`, `mode`, 相似度阈值 | 源列表+目标列表(带source_product_id·图/标题相似度)+利润/风险/Top3报告 | selection |
