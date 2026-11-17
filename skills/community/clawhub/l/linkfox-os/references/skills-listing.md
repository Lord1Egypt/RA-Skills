# Listing skills

**25 个 skill**，覆盖亚马逊 Listing 生成 pipeline 全阶段：L1 规则/输入 → L2 采集 → L3 关键词 / 差异化 / 合规 → L4 写作 → L5 质量门 → 编排 / 导出 / 商品库 CRUD。

**归属 agent（重要）**：本桶 **25 个中有 22 个只在 `linkfox-listing-agent`**。默认 agent 只有 3 个商品库 CRUD skill + 一个 `linkfox-listing-master-test`。

**用什么 agent**：
- 要产出完整 Listing（对标 / 诊断 / 新建 / 批量 / 打分）→ **必须** `--model linkfox-listing-agent`
- 只要商品库 CRUD → `default` 就行

## Skills

| skill | 阶段/角色 | 用途 | 入参（关键字段） | 返回摘要 | 归属 agent |
|---|---|---|---|---|---|
| `agent-listing-result-html-skill` | 导出/渲染 | 把结构化 Listing 结果渲染为固定样式三页 tab HTML | 结构化 JSON 绝对路径, `--hide-primary-tabs`, `--variant-index` | 单文件 HTML + `Saved full response:` JSON + XLSX/MD artifact 路径 | listing |
| `linkfox-listing-master-test` | 编排模式（旧版全能） | 竞品 ASIN → Listing 文案 + A+ 长图双线并行 | `asins`, `marketplace`, 模式, 商品图 URL, 相似度/分辨率 | Markdown 报告（标题/五点/描述/后台词 + A+ 图路径 + 合规/一致性） | default |
| `linkfox-product-center-listing-create` | 商品库 CRUD | 为已有 SKU 或新建商品创建上架链接 | `skuId` 或 `productName`+`productImages`, `platform`, `marketplace`, `isReference`, `offerSource` | `listingId`/`skuId`/`productId` JSON | default / image / listing / market / selection |
| `linkfox-product-center-listing-detail` | 商品库 CRUD | 按 listingId 查链接完整业务档案 | `listingId`, `offerSource` | Listing 完整字段 JSON（大响应落盘），含主副图/A+/状态码 | default / image / listing / market / selection |
| `linkfox-product-center-listing-update` | 商品库 CRUD | PATCH 更新 listing 文案或追加图片 | `listingId`, `title`, `bulletPoints`, `keywords`, `appendImages`, `imageType`, `offerSource` | 更新结果 code/msg JSON | default / image / listing / market / selection |
| `listing-asin-batch-ingest` | L1 采集入口 | 解析 ASIN 批次（文本/CSV/Excel/ZIP）标准化 | `raw_text` 或 `file_id`, `batch_id`, `dedupe_against`, `max_batch_size` | 标准化 ASINContext 列表 + IngestStats + 校验失败行 | listing |
| `listing-asin-deep-fetch` | L2 采集 | 并发拉竞品详情 + Keepa 销售历史 | `batch_id`, `row_indices`, `region`, `fetch_options` | 写回 target_detail/target_keepa，返回 fetched_count/failed_rows | listing |
| `listing-batch-replicate` | 编排模式（批量） | 多目标商品批量完整 Listing 编排 + 反聚类 | ASIN/CSV/Excel/飞书链接, `mode`, `marketplace`, `output_language` | 批量报告 JSON（每项完整 Listing + 反聚类/合规汇总） | listing |
| `listing-benchmark` | 编排模式 | 对标复刻：竞品 → 关键词布局 → 差异化文案 | `asin`(s), `marketplace`, `output_language` | 完整 Listing HTML + assemble JSON + L3 md 路径 | listing |
| `listing-bullet-writer` | L4 写作 | 生成/重写 5 条 BAF 五点描述 | `batch_id`, `row_index`, `generation_mode`, `title_already_generated`, `item_highlights_already_generated` | bullets[5] + 覆盖率/结构 meta 落盘 JSON | listing |
| `listing-competitor-cluster` | L3 批量差异化 | 对 ASIN 集合按图+标题语义聚类做 anti-cluster | `batch_id`, `row_indices`, `similarity_threshold`, `clustering_dimensions` | cluster_id 分配 + cluster_summary（含差异化提示） | listing |
| `listing-compliance-scan` | L3 质量门 | 扫对标内容风险（专利/商标/极限词/品类） | `batch_id`, `row_indices`, `scan_depth`, `scan_assets` | ComplianceReport（risk 等级 + 命中项）写回 context | listing |
| `listing-compliance-validator` | L5 质量门 | 对 writer 产出做合规终检 | `batch_id`, `row_index`, `validation_depth`, `fields_to_validate` | compliance_pass + violations[] + requires_human_review | listing |
| `listing-create` | 编排模式 | 新建：产品信息（图/规格）从零生成 Listing | 图片/规格文本/品牌/类目, `marketplace`, 可选竞品 ASIN | 完整 Listing HTML + 忠实性核查表 + 待卖家确认清单 | listing |
| `listing-description-writer` | L4 写作 | 生成/重写产品长描述 | `batch_id`, `row_index`, `format_style`(narrative/listicle/qa/scenario) | description + 段落/覆盖率 meta 落盘 JSON | listing |
| `listing-diff-meter` | L5 质量门 | 量化生成 vs 对标相似度，防抄袭 | `batch_id`, `row_index`, `fields_to_check`, `comparison_targets` | DiffReport（分字段分数 + 冲突片段 + recycle_advice） | listing |
| `listing-export-flat-file` | 导出 | 批量导出 Amazon Flat File（XLSX） | `batch_id`, `template_id`, `amazon_region`, `include_only_passed`, `sku_strategy` | Amazon inventory XLSX file_id + row_count + skipped_rows | listing |
| `listing-flow-batch-replicate` | 编排 Playbook | L1-L5 声明式批量流水线主入口 | `batch_id`, `rule_version`, `mode`(single_preview/full_batch/resume_failed), `concurrency` | BatchResultsSummary（done/failed/flagged + 阶段耗时/成本） | listing |
| `listing-keyword-matrix-build` | L3 关键词 | ASIN-SIF/SellerSprite 或 category_seed 构建 scored_table | `asin` 或 `category_node`+`product_facts`+`seed_keywords`, `region`, `time_window`, `top_n` | scored_table JSON + coverage_warning，`Saved full response:` 落盘 | listing |
| `listing-quality-scorer` | L5 质量门（评分） | 独立评分 8 维 + hard gates，生成 scorePanel | `listing`, `product_facts`, `keyword_matrix`, `compliance_report`, `diff_report`, `scoring_mode` | scorePanel JSON（overall/grade/items/topIssues/quickFixes） | listing |
| `listing-review-mine` | L2/L3 采集（可选） | 抓取竞品评论并聚类为购买洞察 | `batch_id`, `reviews_per_star`, `focus`, `include_quotes` | 赞点/槽点/未满足需求/场景/人群 JSON 写回 context | listing |
| `listing-rewrite` | 编排模式 | 诊断优化：自有 ASIN/文案 → 评分 → 优化 + diff | 目标 ASIN 或粘贴文本, 可选竞品 ASIN, `marketplace` | 完整 HTML + 新旧 scorePanel 对比 + 关键词变更 + diff | listing |
| `listing-rule-resolver` | L1 规则解析 | 多模态规则输入归一化为 ResolvedRule | `template_id`, `form_fields`, `nl_description`, `sample_listing_ids` | ResolvedRule + rule_version(hash) + ambiguities | listing |
| `listing-search-terms-writer` | L4 写作 | 生成 ≤250 字节后台搜索词，前台自动去重 | `batch_id`, `row_index`, `strategy`, `include_typos`, `include_competitor_brand_terms` | search_terms 字符串 + meta 落盘 JSON | listing |
| `listing-title-writer` | L4 写作 | 生成 Title(≤75c) + Item Highlights(≤125c) | `batch_id`, `row_index`, `source_mode`(generate/split_legacy), `legacy_title`, `title_split_hints` | title + item_highlights + migration_map 落盘 JSON（含批量 fast path 输出 XLSX） | listing |
