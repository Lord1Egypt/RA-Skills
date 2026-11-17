---
name: linkfox-amazon-store-operations
display_name: Linkfox 亚马逊店铺运营
display_name_en: LinkFox Amazon Store Operations
description: 亚马逊店铺 SP-API 运营一站式 AI 工具集，整合授权/订单/Listing/定价/Catalog/报告/Feeds/买家反馈/文件上传/A+ Content/External Fulfillment/FBA 等 12 项子能力，覆盖店铺日常运营全链路。
description_zh: 亚马逊店铺 SP-API 运营工具集，整合 12 项子能力：店铺授权与令牌管理、订单查询与发货确认、Listing 刊登与限制、定价与比价（含批量 FOEP/竞争摘要）、Catalog 目录检索、95+ 种后台报告下载、Feeds 批量上传、买家反馈洞察、文件预签名上传、A+ Content 管理、External Fulfillment（location 库存/履约单/面单发票/退货）、FBA（入仓资格/库存/Inbound/MCF）。经 LinkFox 网关调用 SP-API，需先授权取令牌。当用户需要亚马逊店铺运营、订单、Listing、定价、报告、批量上传、A+ 页面、买家反馈分析、External Fulfillment 或 FBA 入仓/库存/MCF 时触发。参数见 references/，脚本见 scripts/。
description_en: One-stop Amazon store SP-API operations toolkit integrating 10 sub-capabilities: store OAuth authorization & token management, order query & shipment confirmation, Listings management (PATCH/PUT/DELETE/restrictions/Product Type definitions), product pricing & comparison (batch FOEP & competitive summary), Catalog retrieval, automated download of 95+ Seller Central report types (request→poll→download→extract), Feeds bulk data upload, customer feedback insights (review topics/trends/return reasons), presigned file upload, and A+ Content management. All routed through the LinkFox gateway POST /spApi/developerProxy to Amazon SP-API; requires prior store authorization to obtain an access token. Triggered when the user needs Amazon store operations, order management, listing, pricing, report download, bulk upload, A+ pages, or customer feedback analysis. Full params per sub-capability in references/, scripts in scripts/.
category: e-commerce
version: 1.0.0
author: LinkFox
---

# Linkfox 亚马逊店铺运营（Amazon Store Operations）

亚马逊店铺 SP-API 运营一站式 AI 工具集，整合 **12 项子能力**，覆盖授权与令牌、订单、Listing 刊登、定价、Catalog 目录、报告、Feeds 批量上传、买家反馈、文件上传、A+ Content、External Fulfillment 与 FBA。各子能力完整参数、响应字段与错误码见 `references/` 下对应文件，可执行脚本见 `scripts/`。

## 能力边界

### ✅ 能力范围

以下能力均经 tool_key `amazon_sp_api`（亚马逊 SP-API 网关 `POST /spApi/developerProxy` 转发上游 SP-API，授权类直连 `POST /spApi/*`）实现，整合 12 项子能力：

- **授权与令牌管理（linkfox-amazon-store-auth）**：生成亚马逊店铺 OAuth 授权链接、查询已授权店铺列表、刷新令牌、查询指定店铺访问令牌；是所有下游 SP-API 操作的前置依赖（取 `accessToken`）。
- **订单管理（linkfox-amazon-store-orders）**：订单列表检索、单笔订单详情、买家信息、收货地址、订单行项目、管制订单核验信息查询，以及发货状态更新、确认发货、管制订单核验状态更新（SP-API Orders）。
- **Listing 刊登管理（linkfox-amazon-store-listings）**：单条/列表检索刊登、PATCH 部分更新、PUT 创建/全量更新、DELETE 删除刊登，查询 ASIN 刊登限制（是否可售）、Product Type 列表搜索与 JSON Schema 定义查询（SP-API Listings & Definitions）。
- **商品定价与比价（linkfox-amazon-store-pricing）**：单条/批量获取 ASIN/SKU 定价、竞争性报价、Listing/Item 报价、购物车预期价（FOEP）与竞争摘要（SP-API Product Pricing，含 batch 接口）。
- **Catalog 目录检索（linkfox-amazon-store-catalog）**：按 ASIN 获取商品目录详情、按关键词/标识符检索商品目录、查询商品所属类目节点，返回摘要/图片/销售排名等（SP-API Catalog Items）。
- **报告自动化（linkfox-amazon-store-report）**：95+ 种卖家后台报告（库存/订单/销售流量/财务结算/FBA/Brand Analytics 等）的端到端获取——请求→轮询→下载→解压，并生成限时本机 HTTP 下载链接（SP-API Reports）。
- **Feeds 批量数据上传（linkfox-amazon-store-feeds）**：库存或 Listing 批量文件的 Feed 文档创建、文件上传、Feed 任务创建、状态轮询、列表查询、取消与结果文档下载（SP-API Feeds）。
- **买家反馈洞察（linkfox-amazon-store-customer-feedback）**：按 ASIN 或类目节点分析评论主题、评价趋势、退货原因与星级影响（MENTIONS / STAR_RATING_IMPACT）（SP-API Customer Feedback）。
- **文件预签名上传（linkfox-amazon-store-uploads）**：创建上传目的地生成预签名 URL，再向该 URL 上传文件，供 A+ Content、Messaging 等下游 API 使用（SP-API Uploads）。
- **A+ Content 管理（linkfox-amazon-store-aplus-content）**：A+ 文档检索、创建、获取、更新、ASIN 关联校验/全量替换、发布记录查询、审核提交与暂停展示（SP-API A+ Content Management）。
- **External Fulfillment（linkfox-amazon-store-external-fulfillment）**：location 级库存 batchInventory、履约单 get/process/packages/面单发票、EF 退货 list/get（SP-API External Fulfillment Inventory / Shipping / Returns v2024-09-11）。
- **FBA（linkfox-amazon-store-fba）**：入仓资格 getItemEligibilityPreview、FBA Inventory、Fulfillment Inbound（v2024-03-20 + v0）、Fulfillment Outbound/MCF 2020-07-01。
- 覆盖美国、英国、德国、日本、法国、意大利、西班牙等站点（`marketplaceIds`/`marketplaceId` 指定，`region` 取 `NA`/`EU`/`FE` 且须与授权区域一致）。

### ❌ 边界与限制

- **API Key 必需**：所有工具均需环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）；各子能力独立计费、独立限频。
- **授权前置**：除 `linkfox-amazon-store-auth` 外，其余 11 项子能力均依赖店铺已授权——须先用 `linkfox-amazon-store-auth`（`store_tokens.py` / `POST /spApi/storeTokens`）取得 `accessToken`，并通过 `check_auth_dependency.py` 本地探测依赖是否就绪（未就绪以 exit 42 + `DEPENDENCY_MISSING:` 信号提示安装 `linkfox-amazon-store-auth`）。
- **计费约束**：同一会话同一参数组合默认只调用一次（脚本带本地缓存）；失败或空结果不得自动改参数、翻页或连续试探；需继续检索时先向用户说明会产生额外消耗（各工具计费规则见 `skills-version.json` 对应条目与 references 内 api.md 的 `costToken` 字段）。
- **不在范围内**：选品/关键词/竞品/评论挖掘等选品调研（用 `linkfox-amazon-product-selection` 系列）；广告投放与管理（用 Amazon Ads 系列）；前台实时搜索/商品详情/前台评论（用 amazon_search / amazon_product_detail / amazon_reviews 系列）；物流与供应链规划、1688 找货源、其他平台运营、与平台或卖家的直接沟通、实时库存与订单的自动决策。
- **数据时效**：SP-API 返回为亚马逊后台当前状态；报告类为按 `dataStartTime`/`dataEndTime` 拉取的历史快照；`accessToken` 约 1 小时过期，过期需 `refresh_token.py` 刷新或重新 `store_tokens.py` 获取。

## 工具选择指南

按需求在下表定到子能力，再跳到【业务需求路由速查】查端点/脚本/references 取参执行。

| 需求 / 用户说 | 默认推荐（子能力） | 何时换用其他 |
|---|---|---|
| 授权/绑定亚马逊店铺、查已授权店铺、令牌过期 | `linkfox-amazon-store-auth` | — |
| 查订单列表 / 单笔订单详情 / 买家信息 / 收货地址 / 订单行 | `linkfox-amazon-store-orders` | 要批量下载历史订单报告用 `linkfox-amazon-store-report`（reportType 订单类） |
| 确认发货 / 标记已发货 / 更新发货状态 | `linkfox-amazon-store-orders`（confirm_shipment / update_shipment_status） | — |
| 单条 Listing 改标题/价格/属性、新建/全量更新/删除刊登 | `linkfox-amazon-store-listings`（PATCH/PUT/DELETE） | 要批量上传/修改多条 Listing 文件用 `linkfox-amazon-store-feeds`（feedType=Listing 类） |
| 查 ASIN 能不能卖 / 刊登限制 | `linkfox-amazon-store-listings`（get_listings_restrictions） | — |
| Product Type 有哪些 / 某类型的字段 Schema | `linkfox-amazon-store-listings`（search/get_definitions_product_type） | — |
| 查商品定价 / 这个 ASIN 多少钱 / 比价 | `linkfox-amazon-store-pricing`（get_pricing / get_competitive_pricing） | 要批量（≤20 ASIN/SKU）报价用 `post_item_offers_batch` / `post_listing_offers_batch`；要购物车预期价用 `post_featured_offer_expected_price_batch`；要竞争摘要用 `post_competitive_summary_batch` |
| 批量查报价（多个 ASIN/SKU） | `linkfox-amazon-store-pricing`（post_item_offers_batch / post_listing_offers_batch） | 仅 1 个用单条 `get_item_offers` / `get_listing_offers` |
| 查商品目录 / 按 ASIN 查商品信息 / 关键词搜目录 / 类目节点 | `linkfox-amazon-store-catalog` | 要前台实时搜索结果（非店铺目录）用 amazon_search 系列（选品 skill） |
| 下载卖家后台报告（库存/订单/销售流量/财务/FBA/Brand Analytics） | `linkfox-amazon-store-report`（get_report ⭐端到端） | 要逐条查订单用 `linkfox-amazon-store-orders` |
| 批量上传库存 / 批量改 Listing（Feed 文件） | `linkfox-amazon-store-feeds`（create_feed_document→upload→create_feed→get_feed） | 单条 Listing 改用 `linkfox-amazon-store-listings` |
| 查 Feed 处理状态 / 取消 Feed / 下载 Feed 结果 | `linkfox-amazon-store-feeds`（get_feed / cancel_feed / get_feed_document） | — |
| 这个 ASIN 评论主题/差评痛点/星级影响 | `linkfox-amazon-store-customer-feedback`（get_item_review_topics，sortBy=STAR_RATING_IMPACT 看星级影响） | 要前台逐条评论文本用 amazon_reviews 系列（选品 skill）；要类目级反馈用 `get_browse_node_review_topics` |
| 这个 ASIN 评价趋势 / 类目评论趋势 | `linkfox-amazon-store-customer-feedback`（get_item_review_trends / get_browse_node_review_trends） | — |
| 退货原因 / 类目退货主题趋势 | `linkfox-amazon-store-customer-feedback`（get_browse_node_return_topics / trends） | — |
| 上传 A+ 图片 / Messaging 附件 / 生成预签名上传 URL | `linkfox-amazon-store-uploads`（create_upload_destination_for_resource→upload_to_destination） | — |
| A+ 页面检索/创建/获取/更新 | `linkfox-amazon-store-aplus-content` | 需先上传图片用 `linkfox-amazon-store-uploads` 取得 URL |
| A+ 关联 ASIN / 校验 ASIN / 审核提交 / 暂停展示 / 发布记录 | `linkfox-amazon-store-aplus-content` | — |
| External Fulfillment location 库存查写 / Seller Flex Easy Ship 履约单 / 面单发票 / EF 退货 | `linkfox-amazon-store-external-fulfillment` | 普通订单用 `linkfox-amazon-store-orders`；Feed 批量库存用 `linkfox-amazon-store-feeds` |
| FBA 入仓资格 / FBA 库存摘要 / Inbound Plan 入仓 / MCF 多渠道履约 | `linkfox-amazon-store-fba` | External Fulfillment 用 `linkfox-amazon-store-external-fulfillment`；普通订单用 orders |

### 工具选择思路

- **重要**：多个子能力满足需求时，要依据需求深入分析子能力的功能、用途、出入参，从中调研出最合适的子能力，并推荐用户，让用户自己决定。
- 满足程度同等的前提下，向用户推荐"默认推荐子能力"。
- **单条 vs 批量**：单条写操作优先 `linkfox-amazon-store-listings`；批量文件操作优先 `linkfox-amazon-store-feeds`。
- **店铺目录 vs 前台搜索**：查自己店铺后台可售商品/类目用 `linkfox-amazon-store-catalog`；查前台实时 SERP/竞品用选品 skill 的 amazon_search 系列。

## 业务需求路由速查

按【工具选择指南】定到子能力后，下表查端点、脚本与 references 文件取参执行。所有 SP-API 业务调用统一经 `POST ${LINKFOX_TOOL_GATEWAY}/spApi/developerProxy`，请求体含 `region` + `path`（SP-API 相对路径，无前导 `/`）+ `method` + `amzAccessToken`（来自 `linkfox-amazon-store-auth` 的 `store_tokens.py`）+ 可选 `queryString`/`body`/`contentType`；授权类直连 `POST /spApi/*`。

### 子能力 ↔ references 文件 ↔ 端点 ↔ 脚本（10 项）

**amazon_sp_api**

| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-amazon-store-auth | references/linkfox-amazon-store-auth.md | POST /spApi/authorizeUrl、/spApi/authorizedStores、/spApi/refreshToken、/spApi/storeTokens | authorize_url.py、authorized_stores.py、refresh_token.py、store_tokens.py |
| linkfox-amazon-store-orders | references/linkfox-amazon-store-orders.md | POST /spApi/developerProxy（orders/2026-01-01/*、orders/v0/*） | search_orders.py、get_order.py、get_order_address.py、get_order_buyer_info.py、get_order_items.py、get_order_items_buyer_info.py、get_order_regulated_info.py、update_shipment_status.py、update_verification_status.py、confirm_shipment.py |
| linkfox-amazon-store-listings | references/linkfox-amazon-store-listings.md | POST /spApi/developerProxy（listings/2021-08-01/*、definitions/2020-09-01/*） | get_listings_item.py、search_listings_items.py、patch_listings_item.py、put_listings_item.py、delete_listings_item.py、get_listings_restrictions.py、search_definitions_product_types.py、get_definitions_product_type.py |
| linkfox-amazon-store-pricing | references/linkfox-amazon-store-pricing.md | POST /spApi/developerProxy（products/pricing/v0/*、batches/products/pricing/*） | get_pricing.py、get_competitive_pricing.py、get_listing_offers.py、get_item_offers.py、post_item_offers_batch.py、post_listing_offers_batch.py、post_featured_offer_expected_price_batch.py、post_competitive_summary_batch.py |
| linkfox-amazon-store-catalog | references/linkfox-amazon-store-catalog.md | POST /spApi/developerProxy（catalog/2022-04-01/*、catalog/v0/*） | get_catalog_item.py、list_catalog_categories.py、search_catalog_items.py |
| linkfox-amazon-store-report | references/linkfox-amazon-store-report.md | POST /spApi/developerProxy（reports/2021-06-30/reports、/reports/{reportId}、/documents/{reportDocumentId}） | get_report.py（⭐端到端）、merge_report_type_values_from_cache.py（辅助） |
| linkfox-amazon-store-feeds | references/linkfox-amazon-store-feeds.md | POST /spApi/developerProxy（feeds/2021-06-30/documents、/feeds、/feeds/{feedId}）+ PUT 预签名 URL | create_feed_document.py、upload_feed_document.py、create_feed.py、get_feed.py、get_feeds.py、get_feed_document.py、cancel_feed.py |
| linkfox-amazon-store-customer-feedback | references/linkfox-amazon-store-customer-feedback.md | POST /spApi/developerProxy（customerFeedback/2024-06-01/items/{asin}/*、/browseNodes/{browseNodeId}/*） | get_item_review_topics.py、get_item_review_trends.py、get_item_browse_node.py、get_browse_node_review_topics.py、get_browse_node_review_trends.py、get_browse_node_return_topics.py、get_browse_node_return_trends.py |
| linkfox-amazon-store-uploads | references/linkfox-amazon-store-uploads.md | POST /spApi/developerProxy（uploads/2020-11-01/uploadDestinations/{resource}）+ PUT 预签名 URL | create_upload_destination_for_resource.py、upload_to_destination.py |
| linkfox-amazon-store-aplus-content | references/linkfox-amazon-store-aplus-content.md | POST /spApi/developerProxy（aplus/2020-11-01/contentDocuments/*、/contentPublishRecords、/contentAsinValidations） | search_content_documents.py、create_content_document.py、get_content_document.py、update_content_document.py、list_content_document_asin_relations.py、post_content_document_asin_relations.py、validate_content_document_asin_relations.py、search_content_publish_records.py、post_content_document_approval_submission.py、post_content_document_suspend_submission.py |
| linkfox-amazon-store-external-fulfillment | references/linkfox-amazon-store-external-fulfillment.md | POST /spApi/developerProxy（externalFulfillment/inventory/2024-09-11/*、externalFulfillment/2024-09-11/shipments/*、externalFulfillment/2024-09-11/returns/*） | post_batch_inventory.py、get_shipments.py、get_shipment.py、process_shipment.py、create_packages.py、update_package.py、update_package_status.py、retrieve_shipping_options.py、generate_invoice.py、retrieve_invoice.py、generate_ship_labels.py、list_returns.py、get_return.py |
| linkfox-amazon-store-fba | references/linkfox-amazon-store-fba.md | POST /spApi/developerProxy（fba/inbound/v1/*、fba/inventory/v1/*、fba/inbound/v0/*、inbound/fba/2024-03-20/*、fba/outbound/2020-07-01/*） | fba_api.py（统一入口）及 70 个 operation 脚本，见 capabilities |

> 各子能力脚本目录下另有共享模块（`_spapi_<域>_common.py` / `_lf_output.py`）与依赖检查脚本 `check_auth_dependency.py`，由业务脚本内部调用，不作为独立 CLI 使用。

## 调用方式

- **网关**：`${LINKFOX_TOOL_GATEWAY}/<端点>`（默认 `https://tool-gateway.linkfox.com`，可用 `LINKFOX_TOOL_GATEWAY` 覆盖，兼容旧名 `STORE_API_BASE_URL`/`SPAPI_BASE_URL`），请求方式 POST、Content-Type `application/json`，认证 Header `Authorization: <api_key>`（api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取；未配置按下方【解决认证和积分问题】处理）。各端点路径见上方【业务需求路由速查】与对应 references 文件。
- **SP-API 请求体**：业务接口统一 `POST /spApi/developerProxy`，JSON 体含 `region`（`NA`/`EU`/`FE`）、`path`（SP-API 相对路径，无前导 `/`）、`method`（`GET`/`POST`/`PATCH`/`PUT`/`DELETE`）、`amzAccessToken`（访问令牌）、可选 `queryString`/`body`/`contentType`；授权类直连 `POST /spApi/authorizeUrl` 等专用端点。
- **授权前置**：首次或令牌过期时，先跑 `linkfox-amazon-store-auth` 的 `store_tokens.py '{"region":"NA","sellerId":"A1..."}'` 取 `amzAccessToken`，再传给下游业务脚本；业务脚本启动时会本地探测 `check_auth_dependency.py`，依赖缺失时以 exit 42 + `DEPENDENCY_MISSING:` 提示先安装 `linkfox-amazon-store-auth`。
- **Python 脚本**：每项子能力对应 `scripts/<脚本名>.py '<JSON 参数>' [--inline]`（脚本名与端点见路由速查表）。脚本内部完成网关调用、鉴权与落盘。
- **输出策略（脚本默认行为）**：始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill>-<timestamp>.json`（`<cwd>` 为脚本执行时工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）；响应体 ≤ 8 KB 落盘后完整打印到 stdout，> 8 KB 仅打印摘要（顶层字段、常见计数、最大列表长度 + 前 3 条样本）；加 `--inline` 强制全量打印（同样落盘）。
- **读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 PowerShell `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。
- **完整参数**：每个子能力的请求参数、响应字段、错误码、curl 示例见 `references/<源skill>.md`（文件内含该子能力 SKILL.md 正文与 api.md 全文）。

## 使用示例

以下按运营模块给出代表性子能力的出入参示例；其余子能力参数见对应 references 文件。`region` 取 `NA`/`EU`/`FE`（须与授权区域一致），`marketplaceIds`/`marketplaceId` 为站点 ID（美国 `ATVPDKIKX0DER`），`sellerId` 为卖家标识，`amzAccessToken` 由 `linkfox-amazon-store-auth` 的 `store_tokens.py` 取得。

### 授权层

**1. 生成授权链接 / 取访问令牌（amazon_sp_api → authorize_url.py / store_tokens.py）**
```json
{"region": "NA", "sellerName": "My Store"}
```
出参：`authorizeUrl`（Amazon 授权链接）；`store_tokens.py` 出参 `accessToken`（约 1 小时过期）、`refreshToken`、`tokenType`、`expiresIn`、`authRecordId`。`sellerName` 必填，用于在已授权列表中识别账号。

### 订单层

**2. 订单列表检索（amazon_sp_api → search_orders.py）**
```json
{"sellerId": "A1EC6SZ7XAMURH", "region": "NA", "marketplaceIds": ["ATVPDKIKX0DER"], "lastUpdatedAfter": "2026-05-01T00:00:00Z"}
```
出参：`searchOrders`（订单列表，含 AmazonOrderId/PurchaseDate/OrderStatus/OrderTotal/FulfillmentChannel 等）、`paginationToken`、developerProxy 的 `errcode`/`httpStatus`/`body`。`lastUpdatedAfter`/`createdAfter` 二选一，`marketplaceIds` ≤50。

### Listing 刊登层

**3. 创建/全量更新刊登（amazon_sp_api → put_listings_item.py）**
```json
{"sellerId": "A1BCDEFGHIJK2", "region": "NA", "sku": "My-Seller-SKU-001", "marketplaceIds": ["ATVPDKIKX0DER"], "productType": "LUGGAGE", "requirements": "LISTING", "attributes": {"item_name": [{"value": "Example Title", "marketplace_id": "ATVPDKIKX0DER"}]}}
```
出参：`putResult`（Amazon 返回的提交结果，含 `sku`/`status`/`submissionId`/`issues`）、`httpStatus`、`errcode`。`marketplaceIds` 官方约束 ≤1，`requirements` 必填（`LISTING`/`LISTING_PRODUCT_ONLY`/`LISTING_OFFER_ONLY`）。

### 定价层

**4. 单条定价/比价（amazon_sp_api → get_pricing.py）**
```json
{"sellerId": "A1...", "region": "NA", "asin": "B08N5WRWNW", "marketplaceId": "ATVPDKIKX0DER", "itemType": "Asin", "asins": ["B08N5WRWNW"], "itemCondition": "New"}
```
出参：`pricing`（含 `Identifier`/`Summary`/`Product`，价格、竞品数、Buy Box 价等）、`errcode`/`httpStatus`/`body`。批量 ≤20 用 `post_item_offers_batch.py`；购物车预期价用 `post_featured_offer_expected_price_batch.py`（≤40）。

### Catalog 目录层

**5. 按 ASIN 查商品目录（amazon_sp_api → get_catalog_item.py）**
```json
{"sellerId": "A1...", "region": "NA", "asin": "B08N5WRWNW", "marketplaceIds": ["ATVPDKIKX0DER"], "includedData": ["summaries", "images"]}
```
出参：`catalogItem`（含 `asin`/`summaries`/`images`/`attributes`/`salesRanks` 等）、`errcode`/`httpStatus`/`body`。`includedData` 可选 `summaries`/`images`/`attributes`/`salesRanks` 等。

### 报告层

**6. 端到端获取报告（amazon_sp_api → get_report.py ⭐）**
```json
{"sellerId": "A1EC6SZ7XAMURH", "region": "NA", "reportType": "GET_MERCHANT_LISTINGS_ALL_DATA", "marketplaceIds": ["ATVPDKIKX0DER"]}
```
出参：`reportId`、`processingStatus`（IN_QUEUE/IN_PROGRESS/DONE/FATAL/CANCELLED）、`reportDocumentId`、`downloadPath`（解压后本地绝对路径）、`extractedFileHttpUrl`（限时本机 HTTP 直链，默认 300s）。支持 95+ 报告类型，详见 `references/report-types.md` 与 `references/report-requests/`。

### Feeds 批量上传层

**7. 创建 Feed 任务（amazon_sp_api → create_feed.py，需先 create_feed_document.py+upload_feed_document.py 上传文件）**
```json
{"sellerId": "A1EC6SZ7XAMURH", "region": "NA", "feedType": "POST_FLAT_FILE_INVLOADER_DATA", "marketplaceIds": ["ATVPDKIKX0DER"], "inputFeedDocumentId": "amzn1.tdoc.1.1.xxx"}
```
出参：`feedId`、`processingStatus`（IN_QUEUE/IN_PROGRESS/DONE/FATAL/CANCELLED）、`resultFeedDocumentId`、`errcode`/`httpStatus`。流程：`create_feed_document` 取 `url` → `upload_feed_document` PUT 上传 → `create_feed` 建任务 → `get_feed` 轮询 → `get_feed_document` 取结果。

### 买家反馈层

**8. ASIN 评论主题（amazon_sp_api → get_item_review_topics.py）**
```json
{"sellerId": "A1...", "region": "NA", "asin": "B0...", "marketplaceId": "ATVPDKIKX0DER", "sortBy": "MENTIONS"}
```
出参：`itemReviewTopics`（评论主题及频次/星级影响）、`errcode`/`httpStatus`/`body`。`sortBy` 必填 `MENTIONS`（提及量）或 `STAR_RATING_IMPACT`（星级影响）；要趋势用 `get_item_review_trends.py`，类目级用 `get_browse_node_review_topics.py`（需先 `get_item_browse_node.py` 反查 `browseNodeId`）。

### 文件上传层

**9. 创建上传目的地（amazon_sp_api → create_upload_destination_for_resource.py → upload_to_destination.py）**
```json
{"sellerId": "A1...", "region": "NA", "resource": "aplus/2020-11-01/contentDocuments", "marketplaceId": "ATVPDKIKX0DER", "filePath": "/path/to/banner.jpg", "contentType": "image/jpeg"}
```
出参：`uploadDestination`（含 `uploadDestinationId`/`url`/`headers`）、`errcode`/`httpStatus`。`contentMD5` 可由 `filePath`/`content`/`contentBase64` 自动计算；步骤 2 `upload_to_destination.py` 向返回的预签名 `url` PUT 文件（带 `headers`）。

### A+ Content 层

**10. 获取 A+ 文档详情（amazon_sp_api → get_content_document.py）**
```json
{"sellerId": "A1...", "region": "NA", "marketplaceId": "ATVPDKIKX0DER", "contentReferenceKey": "YOUR_KEY", "includedDataSet": ["CONTENTS", "METADATA"]}
```
出参：`contentDocument`（文档内容与元数据）、`contentReferenceKey`、`warnings`、`errcode`/`httpStatus`/`body`。`includedDataSet` 必填 ≥1（`CONTENTS`/`METADATA`）；创建/更新用 `create_content_document.py`/`update_content_document.py`，提交审核用 `post_content_document_approval_submission.py`。

## 展示规则

1. **客观呈现数据**：以清晰表格展示查询/操作结果，不做主观商业建议（除非用户主动要求）；展示价格/金额时务必提示币种与站点（响应字段标明本地币种与 marketplace）。
2. **来源标注**：展示数据时说明来自哪个 SP-API 模块（Orders/Listings/Pricing/Catalog/Reports/Feeds/Customer Feedback/Uploads/A+ Content/Auth）。
3. **不可用数据**：值为 `0`/`-1`/`null` 的字段表示数据不可用，标注"N/A"或省略，不作实际值展示。
4. **写操作确认**：Listing/Feeds/A+/订单发货等写操作（PATCH/PUT/POST/DELETE）执行前向用户确认关键参数（sellerId、sku、ASIN、marketplaceIds、reportType、feedType 等），避免误改误删；写操作多为异步，展示 `submissionId`/`feedId`/`reportId`/`processingStatus` 并提示需轮询确认最终结果。
5. **错误处理与协同**：查询失败时根据响应 `errcode`/`errmsg`/`httpStatus` 说明原因并建议修正（ASIN/SKU 格式、`region` 与授权区不一致、`path` 白名单未放行 `1005`、参数越界、令牌过期需刷新等）；连续使用多模块时将各结果汇总为连贯分析，标注数据来源与时间窗。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

**注意**：你是workbuddy，并且渠道是workbuddy，使用 onboarding 引导登录注册时 channel **必须**为 workbuddy。这非常重要！

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。
