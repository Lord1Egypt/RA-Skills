# 通用工具 skills

**15 个 skill**，覆盖文件上传 / 报告落盘 / 定时任务 / skill 创建 / SuperAgent 编排 / 网页爬取 / Google 趋势 / AI 搜索 / 飞书表格 / 商品库变体 CRUD。

**归属 agent**：大部分挂在 `default`。少数例外：
- `lark-base` 只在 `linkfox-listing-agent`
- `linkfox-skill-creator` 只在 `linkfox-market-analysis-agent`

**不确定用哪个 agent？** → 用 `default`（覆盖本桶 12/15 个 skill）。要用飞书表格 → `linkfox-listing-agent`；要用通用 skill 生成器 → `linkfox-market-analysis-agent`。

## Skills

| skill | 类型 | 用途 | 入参（关键字段） | 返回摘要 | 归属 agent |
|---|---|---|---|---|---|
| `lark-base` | 飞书 | 读写飞书多维表格 schema 与记录 | `app_id`+`app_secret`/`tenant_access_token`, `base_url`/`app_token`, `table_id`, `record_id`, `fields` | JSON：tables/fields/records；`ok:false` 时含错误原因 | listing |
| `linkfox-ai-mode-google-search` | AI 搜索 | 用 Google AI Overview 抓单关键词深度调研 | `keyword`(必填) | Markdown 全文 + citations，落盘 JSON，超 8KB 只回摘要 | default / market / selection |
| `linkfox-ecommerce-skill-creator` | skill 创建 | 电商 Tier2/3 多步业务流程 skill 生成器 | mode(新建/复刻/微调), skill 名, 业务流程访谈信息 | 生成产物目录+`SKILL.md`+scripts+references，走六环验收 | default / listing / market / selection |
| `linkfox-file-upload` | 文件上传 | 本地文件上传 OSS 换 HTTPS URL | `local_path`(必填，可多个) | JSON 数组：`url`/`path`/`name`/`size`/`ext`，失败带 `error` | default / image / listing / market / selection / video |
| `linkfox-google-trend-get-trend-by-keys` | Google 趋势 | 按关键词查 Google Trends 搜索热度 | `keyword`(必填), `region`, `dayRangeStart`, `dayRangeEnd` | JSON 0-100 归一化趋势曲线，落盘 + 摘要，超 8KB 只回摘要 | default / market / selection |
| `linkfox-google-trend-get-trend-by-time` | Google 趋势 | 按时间窗查区域实时热搜话题 | `days`(默认7), `region`(默认US) | JSON：query/searchVolume/increasePercentage 列表，落盘 | default / market / selection |
| `linkfox-plugin-web-data-crawler` | 网页爬取 | 浏览器插件采集商品详情页字段 | `--site`, `--url`(或 ASIN), `--category`, `--reuse-tab` | JSON：标题/价/图/评分/五点/规格，落盘 + `[Saved]` 路径 | default |
| `linkfox-product-center-variant-create` | 商品库 CRUD | 商品库创建 SPU/SKU 变体+原图 | `productName`/`productId`, `images`(必填), `offerSource`, `videos` | JSON：`productId`+`skuId`，含 `duplicate` 幂等标记 | default / image / listing / market / selection |
| `linkfox-product-center-variant-detail` | 商品库 CRUD | 按 skuId 查变体完整业务档案 | `skuId`(必填), `offerSource` | JSON：基础/卖点/服装字段/状态/原图列表，大响应落盘 | default / image / listing / market / selection |
| `linkfox-product-center-variant-listings` | 商品库 CRUD | 按 skuId 分页列变体下所有链接卡片 | `skuId`(必填), `platform`, `marketplace`, `isReference`, `status`, `pageNum` | JSON：listing 卡片列表+total+hasMore，大响应落盘 | default / image / listing / market / selection |
| `linkfox-product-center-variant-update` | 商品库 CRUD | 按 skuId PATCH 更新变体字段/追加媒体 | `skuId`(必填), `offerSource`, `skuName`/`sellingPoints`/`appendImages` 等按需 | JSON：`{code, msg, traceId}`，data 一般为 null | default / image / listing / market / selection |
| `linkfox-report-generator` | 报告落盘 | 生成 HTML 分析报告（>400 字唯一出口） | `--content-file`(HTML 片段), `--language`(zh/en/ja/ko), `--title` | JSON：`path`/`bytes`/`language`/`title`，`Saved full response:` 落盘 | default / listing / market / selection |
| `linkfox-skill-creator` | skill 创建 | 通用 skill / API wrapper 脚手架与合规校验 | `--slug`, `--api-path`, `--title`, `--dest` | 生成 SKILL.md+scripts 骨架+`_meta.json`；validate 输出 finding | market |
| `linkfox-superagent-orchestration` | 编排调度 | SuperAgent 主/子 Agent handoff 合同 | `targetAgent`(5 种), handoff 上下文, write-back proposal | 结构化 handoff intent（非 skill 调用，供前端渲染卡片） | default |
| `linkfox-task-scheduler` | 定时任务 | 增删改查定时任务+N 分钟后一次性提醒 | `action`(create/update/update-status/delete/list/remind), `execType`, `execPoint`, `execTime`, `promptContent`, `noticeList` | JSON：任务 id/调度/状态；list 回分页列表，落盘 | default |
