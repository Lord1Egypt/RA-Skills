---
name: linkfox-tiktok-selection-and-shoppable-video
display_name: Linkfox Tiktok选品与带货视频
display_name_en: LinkFox TikTok Product Selection and Shoppable Video
description: TikTok 选品与带货视频一站式 AI 工具集，整合 EchoTik/FastMoss 选品数据与 TikTok 官方带货视频 API，覆盖 TikTok Shop 选品、爆品趋势、带货视频分析与可购物视频发布。
description_zh: TikTok 选品与带货视频一站式 AI 工具集，整合 3 类工具、10 项子能力：EchoTik（16 区域市场新品排行、商品搜索、商品详情、带货视频、视频下载）、FastMoss（全球热销榜与商品搜索，日周月多维筛选）、TikTok 官方 API（视频号 OAuth 授权与令牌、可购物视频预检/发布/状态/达人档案/大文件上传/可带货商品查询）。覆盖选品、爆品趋势、销量/GMV/达人带货与带货视频分析及可购物视频发布链路。当用户需 TikTok 选品、爆品/新品排行、商品或带货视频分析、视频号授权与可购物视频发布时触发。参数见 references/，脚本见 scripts/。
description_en: One-stop TikTok product-selection and shoppable-video AI toolkit integrating 10 sub-capabilities across 3 tool families — EchoTik (new-product ranking, product search, product detail, promotional-video query, video download URL across 16 regional markets), FastMoss (global top-selling rankings and product search with day/week/month and category/sales/commission/creator multi-dimensional filters), and the TikTok official shoppable-video API (creator OAuth authorization & token management, shoppable video pre-check/publish/status/creator profile/large-file chunked upload, creator sellable-product query). Covers TikTok Shop product research, bestseller/new-product trends, product sales/GMV/live/influencer analysis, promotional-video performance & download, and the full official shoppable-video publishing chain (authorize → get product_id → pre-check → publish → check status). Triggered when the user needs TikTok product selection, bestseller/new-product rankings, product or promotional-video data analysis, or TikTok video-account authorization and shoppable-video publishing. Full params per sub-capability are in references/, executable scripts in scripts/.
category: e-commerce
version: 1.0.0
author: LinkFox
---

# Linkfox Tiktok选品与带货视频（TikTok Product Selection and Shoppable Video）

TikTok 选品与带货视频一站式 AI 工具集，整合 **3 类底层工具、10 项子能力**，覆盖选品数据（EchoTik 16 区域市场 / FastMoss 全球电商）与官方带货视频发布链路（TikTok 视频号授权 → 可带货商品 → 可购物视频预检/发布）。各子能力完整参数、响应字段与错误码见 `references/` 下对应文件，可执行脚本见 `scripts/`。

## 能力边界

### ✅ 能力范围
- **TikTok 选品数据（`echotik_tiktok`，EchoTik，覆盖 16 个区域市场）**：新品排行发现热销爆品与新兴趋势（`echotik_tiktok` list-new-product-rank）；商品搜索按销量/达人/佣金/评分/评论多维筛选（`echotik_tiktok` list-product）；商品关联带货视频查询播放/互动/视频销量/GMV（`echotik_tiktok` product-video）；批量商品详情含多周期销量与 GMV、直播销量、带货达人数、价格评分与佣金（`echotik_tiktok` batch-product-detail）；解析 TikTok 视频链接返回无水印/含水印下载、播放与封面地址（`echotik_tiktok` get-video-download-url）。
- **TikTok 全球电商热销与选品（`fastmoss_tiktok`，FastMoss）**：按日/周/月维度与类目分析热销商品排行榜与 GMV 排名（`fastmoss_tiktok` product-rank-top-selling）；按类目/销量/佣金率/达人数/店铺类型多维搜索筛选商品（`fastmoss_tiktok` product-search）。
- **TikTok 官方带货视频 API（`tiktok_official_video_api`）**：视频号达人 OAuth 授权、已授权账号列表、令牌查询与 access_token 刷新（`tiktok_official_video_api` linkfox-tiktok-video-auth）；可购物视频内容预检、查预检结果、发布、查发布状态、达人档案查询及大文件分片上传（`tiktok_official_video_api` linkfox-tiktok-video）；达人可带货商品查询（店铺商品与橱窗/直播袋商品），取得 product_id 供可购物视频挂车（`tiktok_official_video_api` linkfox-tiktok-video-products）。
- 覆盖 region/marketplace：EchoTik 16 个 TikTok Shop 区域市场；FastMoss 全球电商（按 region 筛选）；TikTok 官方视频号 region 支持 `global`（默认）/ `us`（美国站）。具体取值见各 references。

### ❌ 边界与限制
- **API Key 必需**：所有工具均需环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）；各工具独立计费、独立限频，数据时效与区域覆盖随数据源而异。
- **计费约束**：同一会话同一参数组合默认只调用一次（脚本带本地缓存）；失败或空结果不得自动换关键词、翻页或改区域连续试探；需继续检索时先向用户说明会产生额外消耗（计费规则见 `skills-version.json` 与 references 内 api.md 的 `costToken` 字段：EchoTik 5 项 fixed≈4.5/9000 token，FastMoss 2 项 fixed≈10.5/21000 token，TikTok 官方 3 项免费）。
- **TikTok 官方模块隔离**：`linkfox-tiktok-video` / `linkfox-tiktok-video-products` 仅走 `/tiktokVideo/developerProxy`，path 须以 `affiliate_creator` / `video` / `creator` 开头（否则 errcode 1005）；不可用于 `/tiktokShop/*`（TikTok Shop 卖家模块用 `linkfox-tiktok-shop-auth`）。令牌 `ttsAccessToken` 由 `linkfox-tiktok-video-auth` 授权后经 `/tiktokVideo/accountTokens` 取得，固定 creator 达人端。
- **TikTok 官方依赖链**：可购物视频发布需先 `linkfox-tiktok-video-auth` 授权取令牌，再 `linkfox-tiktok-video-products` 取 `product_id`，最后 `linkfox-tiktok-video` 预检/发布；`check_auth_dependency.py` 探测 `linkfox-tiktok-video-auth` 是否安装（exit 42=未安装/未授权，需先完成授权）。
- **大文件上传限制**：≤10MB 走 `upload_shoppable_video_file`（multipart，网关暂不支持）；>10MB 走大文件分片三步（Initialize → PUT 分片 → Bind，详见 `references/large-file-upload.md`，Step 1/3 可经 proxy，Step 2 分片 PUT 不经网关）。
- **不在范围内**：TikTok Shop 小店 ERP（商品/订单/财务，用 `linkfox-tiktok-shop-auth` + 业务 skill）、TikTok Shop 可购物视频（`/tiktokShop/developerProxy`，用 `linkfox-tiktok-creator`）、TikTok 广告投放、物流与供应链、非电商任务、与平台或卖家的直接沟通。

## 工具选择指南

按需求在下表定到子能力，再跳到【业务需求路由速查】查端点/脚本/references 取参执行。

| 需求 / 用户说 | 默认推荐（子能力） | 何时换用其他 |
|---|---|---|
| TikTok 选品 / 搜商品（"TikTok 上什么好卖"） | `linkfox-echotik-list-product`（16 区域市场，销量/达人/佣金/评分多维） | 要全球电商+日/周/月维度+范围筛选（达人数/佣金率 range）用 `linkfox-fastmoss-product-search` |
| TikTok 新品 / 新兴趋势（"最近有什么新品爆"） | `linkfox-echotik-list-new-product-rank`（新品排行） | 要热销榜（非新品）用 `linkfox-fastmoss-product-rank-top-selling` |
| TikTok 热销榜 / 爆品排行 / GMV 排名 | `linkfox-fastmoss-product-rank-top-selling`（日/周/月+类目） | 要"新品"趋势用 `linkfox-echotik-list-new-product-rank` |
| 商品详情 / 多周期销量 GMV（"这个 productId 卖得怎么样"） | `linkfox-echotik-batch-product-detail`（1d/7d/15d/30d/60d/90d/累计+直播+达人） | — |
| 商品带货视频（"这个商品有哪些带货视频 / 视频销量"） | `linkfox-echotik-product-video`（播放/互动/视频销量/GMV） | — |
| 视频下载 / 去水印（"下载这个 TikTok 视频"） | `linkfox-echotik-get-video-download-url`（无水印/含水印/播放/封面） | — |
| 视频号授权 / 绑定视频号 / 刷新令牌 | `linkfox-tiktok-video-auth`（OAuth+令牌） | TikTok Shop 卖家授权用 `linkfox-tiktok-shop-auth`（不互通） |
| 达人能带什么货 / 橱窗商品 / 取 product_id | `linkfox-tiktok-video-products`（店铺商品+橱窗/直播袋） | — |
| 发布可购物视频 / 视频挂车（"发一个带商品的 TikTok 视频"） | `linkfox-tiktok-video`（预检→发布→查状态） | 需先 `linkfox-tiktok-video-auth` 授权 + `linkfox-tiktok-video-products` 取 product_id |
| 达人主页 / 档案 | `linkfox-tiktok-video`（get_creator_profile，独立功能） | — |
| 大文件分片上传视频（>10MB） | `linkfox-tiktok-video`（large_file_upload_init/bind + 分片 PUT） | ≤10MB 走 `upload_shoppable_video_file`（网关暂不支持 multipart） |

### 工具选择思路
- **重要**：多个子能力满足需求时，要依据需求深入分析子能力的功能、用途、出入参、从中调研出最合适的子能力，并推荐用户，让用户自己决定。
- 满足程度同等的前提下，向用户推荐"默认推荐子能力"。

## 业务需求路由速查

按【工具选择指南】定到子能力 后，下表查端点、脚本与 references 文件取参执行：

### 子能力 ↔ references 文件 ↔ 端点 ↔ 脚本（10 项）

**echotik_tiktok**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-echotik-list-new-product-rank | references/linkfox-echotik-list-new-product-rank.md | POST /echotik/listNewProductRank | echotik_list_new_product_rank.py |
| linkfox-echotik-list-product | references/linkfox-echotik-list-product.md | POST /echotik/listProduct | echotik_list_product.py |
| linkfox-echotik-product-video | references/linkfox-echotik-product-video.md | POST /echotik/listProductVideo | echotik_list_product_video.py |
| linkfox-echotik-batch-product-detail | references/linkfox-echotik-batch-product-detail.md | POST /echotik/batchProductDetail | echotik_batch_product_detail.py |
| linkfox-echotik-get-video-download-url | references/linkfox-echotik-get-video-download-url.md | POST /echotik/getVideoDownloadUrl | echotik_get_video_download_url.py |

**fastmoss_tiktok**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-fastmoss-product-rank-top-selling | references/linkfox-fastmoss-product-rank-top-selling.md | POST /fastmoss/productRankTopSelling | fastmoss_product_rank_top_selling.py |
| linkfox-fastmoss-product-search | references/linkfox-fastmoss-product-search.md | POST /fastmoss/productSearch | fastmoss_product_search.py |

**tiktok_official_video_api**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-tiktok-video-auth | references/linkfox-tiktok-video-auth.md | POST /tiktokVideo/authorizeUrl、/authorizedAccounts、/accountTokens、/refreshToken | authorize_url.py、authorized_accounts.py、account_tokens.py、refresh_token.py |
| linkfox-tiktok-video | references/linkfox-tiktok-video.md | POST /tiktokVideo/developerProxy | video_api.py、video_proxy.py、get_creator_profile.py、precheck_shoppable_video.py、get_shoppable_video_precheck_result.py、post_shoppable_video.py、get_shoppable_video_status.py、upload_shoppable_video_file.py、large_file_upload_init.py、large_file_upload_bind.py |
| linkfox-tiktok-video-products | references/linkfox-tiktok-video-products.md | POST /tiktokVideo/developerProxy | get_shop_products.py、get_showcase_products.py、products_api.py |

> TikTok 官方三子能力共享 helper：`response_io.py`（落盘/摘要）、`check_auth_dependency.py`（探测 `linkfox-tiktok-video-auth`）；`linkfox-tiktok-video` 另有 `_video_api_runner.py` / `_video_endpoints.py` / `_tiktok_video_common.py`，`linkfox-tiktok-video-products` 另有 `_products_api_runner.py` / `_products_endpoints.py` / `_tiktok_video_products_common.py`，均与本入口脚本同目录、随调随用。

## 调用方式

- **网关**：`${LINKFOX_TOOL_GATEWAY}/<端点>`（默认 `https://tool-gateway.linkfox.com`），请求方式 POST、Content-Type `application/json`，认证 Header `Authorization: <api_key>`（api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取；未配置按下方【解决认证和积分问题】处理）。各端点路径见上方【业务需求路由速查】与对应 references 文件。
- **TikTok 官方带货视频链路**：`linkfox-tiktok-video` / `linkfox-tiktok-video-products` 经 `POST /tiktokVideo/developerProxy` 转发至紫鸟 `tiktok-proxy/creator/{region}/{path}`；调用方传 `path` / `method` / `ttsAccessToken`（= creator `access_token`，上游请求头 `x-tts-access-token`）/ `region`（`global` 默认 / `us`）；`app_key` / `timestamp` / `sign` 由紫鸟代理自动注入。具名脚本（`video_api.py` / `products_api.py` / 各 `get_*.py` / `post_*.py`）只需传 `{"api": "...", "openId": "..."}`，脚本内部自动调 `/tiktokVideo/accountTokens` 取 `ttsAccessToken` 再调 developerProxy。
- **Python 脚本**：每项子能力对应 `scripts/<脚本名>.py '<JSON 参数>' [--inline]`（脚本名与端点见路由速查表）。脚本内部完成网关调用、鉴权与落盘。
- **输出策略（脚本默认行为）**：始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill>-<timestamp>.json`（`<cwd>` 为脚本执行时工作目录；`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）；响应体 ≤ 8 KB 落盘后完整打印到 stdout，> 8 KB 仅打印摘要（顶层字段、常见计数、最大列表长度 + 前 3 条样本）；加 `--inline` 强制全量打印（同样落盘）。
- **读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 PowerShell `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。
- **完整参数**：每个子能力的请求参数、响应字段、错误码、curl 示例见 `references/<子能力>.md`（文件内含该子能力 SKILL.md 正文与 api.md 全文）；`linkfox-tiktok-video` 另含 `references/large-file-upload.md`（大文件分片上传详解）。

## 使用示例

以下按数据层给出代表性子能力的出入参示例；其余子能力参数见对应 references 文件。

### 选品与数据层（EchoTik / FastMoss）

**1. TikTok 新品排行（echotik_tiktok → echotik_list_new_product_rank.py）**
```json
{"date": "2025-06-15", "region": "US", "pageNum": 1, "pageSize": 50}
```
出参：`products[]`（title/asin/price/minPrice/maxPrice/currency/totalSaleCnt/totalSaleGmvAmt/salesTrendFlagText/totalVideoCnt/totalLiveCnt/totalIflCnt 达人数/productCommissionRate/productRating/reviewCount/categoryId/imageUrl）、`total`、`columns`、`costToken`。

**2. TikTok 商品搜索（echotik_tiktok → echotik_list_product.py）**
```json
{"keyword": "phone case", "region": "US", "minTotalSale30dCnt": 1000, "productSortField": 5, "sortType": 1, "pageSize": 20}
```
出参：`products[]`（productId/productName/title/price/spuAvgPrice/productRating/reviewCount/ratings/productCommissionRate/totalSaleCnt/monthlySalesUnits/totalSaleGmvAmt/totalIflCnt 达人数/categoryName/firstCrawlDt/salesTrendFlagText）、`total`、`columns`、`costToken`。

**3. TikTok 热销榜（fastmoss_tiktok → fastmoss_product_rank_top_selling.py）**
```json
{"region": "US", "dateInfo": {"type": "day", "value": "2026-04-15"}, "page": 1, "pageSize": 10}
```
出参：`products[]`（title/productId/price/minPrice/maxPrice/currency/totalSaleCnt/totalSaleGmvAmt/growthRate/shopName/shopTotalUnitsSold/categoryName/productCommissionRate/imageUrl/offShelvesText）、`total`、`columns`、`costToken`。`dateInfo.type` 支持 `day` / `week` / `month`。

**4. TikTok 商品搜索（fastmoss_tiktok → fastmoss_product_search.py）**
```json
{"keyword": "phone case", "region": "US", "orderField": "day7_units_sold", "pageSize": 10}
```
带范围筛选：`{"keyword": "beauty", "region": "US", "commissionRateRange": {"min": 0.10}, "creatorCountRange": {"min": 50}, "orderField": "commission_rate", "pageSize": 10}`
出参：`products[]`（title/productId/price/totalSaleCnt/totalSaleGmvAmt/totalVideoCnt/totalLiveCnt/totalIflCnt 达人数/productCommissionRate/productRating/reviewCount/skuCount/shopName/isCrossBorder/tiktokUrl/fastmossUrl/imageUrl）、`total`、`columns`、`costToken`。

**5. 批量商品详情（echotik_tiktok → echotik_batch_product_detail.py）**
```json
{"productIds": ["1729382310407603945", "1729382310407603946"]}
```
出参：`products[]`（productId/productName/region/sellerId/minPrice/maxPrice/spuAvgPrice/productRating/reviewCount/productCommissionRate/totalSaleCnt/totalSaleGmvAmt/totalLiveCnt/totalVideoCnt/totalIflCnt 达人数/totalViewsCnt/discount/freeShipping/salesTrendFlag/firstCrawlDt）、`total`、`columns`、`costToken`。也可用 `productUrls` 传 TikTok Shop 商品 URL。

**6. 商品带货视频（echotik_tiktok → echotik_list_product_video.py）**
```json
{"productId": "1729382310407603945", "productVideoSortField": 1, "sortType": 1, "pageSize": 20}
```
出参：`data[]`（videoId/productId/userId/videoDesc/officialUrl/covet 封面/totalFavoritesCnt 点赞/totalVideoSaleCnt/totalVideoSaleGmvAmt/hashTag/createDate/region）、`total`、`columns`、`costToken`。

**7. 视频下载地址（echotik_tiktok → echotik_get_video_download_url.py）**
```json
{"url": "https://www.tiktok.com/@user/video/1234567890"}
```
出参：`downloadUrl`（无水印）、`playUrl`、`coverUrl`、`dynamicCoverUrl`、`videoId`、`costToken`、`errmsg`。

### 带货视频发布层（TikTok 官方）

> 完整链路：`linkfox-tiktok-video-auth` 授权取 `ttsAccessToken` → `linkfox-tiktok-video-products` 取 `product_id` → `linkfox-tiktok-video` 上传 `file_id` →（可选）预检 → 发布 → 查状态。

**8. 视频号授权与令牌（tiktok_official_video_api → authorize_url.py / authorized_accounts.py / account_tokens.py / refresh_token.py）**
```json
// POST /tiktokVideo/authorizeUrl
{"displayName": "My Channel", "region": "global"}
// → {"authorizeUrl": "https://services.tiktokshop.com/open/authorize?service_id=xxx&state=abc123"}（约 1 小时失效）
// POST /tiktokVideo/authorizedAccounts  {}   → accounts[](openId/displayName/region/userType)、total
// POST /tiktokVideo/accountTokens       {"openId": "<creator_open_id>"}
//   → accessToken/refreshToken/accessTokenExpireIn/refreshTokenExpireIn（accessToken 即下游 ttsAccessToken）
// POST /tiktokVideo/refreshToken        {"openId": "<creator_open_id>"}   → 续签并回写
```

**9. 视频号可带货商品（tiktok_official_video_api → get_shop_products.py / get_showcase_products.py）**
```json
// 店铺商品（get_shop_products，GET affiliate_creator/202509/shop_products）
{"openId": "...", "title_keyword": "apple", "sort_field": "PRICE", "sort_order": "DESC", "page_size": 20}
// 橱窗/直播袋商品（get_showcase_products，GET affiliate_creator/202405/showcases/products）
{"openId": "...", "page_size": 20, "origin": "SHOWCASE"}   // origin: SHOWCASE（默认）/ LIVE
```
出参：商品列表含 **`product_id`**（供 `linkfox-tiktok-video` 预检/发布挂车）、`data.next_page_token`（翻页）。`page_size` 必填 1~20。

**10. 发布可购物视频（tiktok_official_video_api → precheck_shoppable_video.py / get_shoppable_video_precheck_result.py / post_shoppable_video.py / get_shoppable_video_status.py）**
```json
// 内容预检（precheck_shoppable_video，POST affiliate_creator/202511/videos/precheck_task）
{"openId": "...", "video_info": {"file_id": "..."}, "product_link_info": {"product_id": "...", "title": "Product anchor"}}
// → data.precheck.task_id
// 查预检结果（GET affiliate_creator/202511/videos/precheck_tasks/{task_id}）
{"openId": "...", "task_id": "1123123123"}
// → result（SUCCESS/FAIL/PROCESSING）；FAIL 时看 issues[] 整改
// 发布可购物视频（post_shoppable_video，POST affiliate_creator/202603/videos）
{"openId": "...", "video_info": {"file_id": "...", "title": "My shoppable video"}, "product_link_info": {"product_id": "...", "title": "Product anchor"}}
// → data.video.id
// 查发布状态（get_shoppable_video_status，GET affiliate_creator/202509/videos/{video_id}/status）
{"openId": "...", "video_id": "7548431509997292816"}
// → post_status（SUCCESS/FAIL/PROCESSING）、post_time
```
> 上传视频文件取 `file_id`：≤10MB 走 `upload_shoppable_video_file`（multipart，网关暂不支持）；>10MB 走大文件分片（`large_file_upload_init` → PUT 分片 → `large_file_upload_bind`，详见 `references/large-file-upload.md`）。

## 展示规则

1. **客观呈现数据**：以清晰表格展示查询结果，不做主观商业建议（除非用户主动要求）；不同区域币种不同，展示价格/收入时务必提示币种（响应 `currency` 字段标明本地币种）。
2. **来源标注**：展示数据时说明来自哪个工具/数据源（EchoTik / FastMoss / TikTok 官方）。
3. **令牌安全**：不向用户明文输出完整 `ttsAccessToken` / `accessToken` / `refreshToken`，仅展示前 10 字符等掩码形式。
4. **不可用数据**：值为 `0` 或 `-1` 的字段表示数据不可用，标注"N/A"或省略，不作实际值展示；`salesTrendFlagText`/`salesTrendFlag` 为 0=平稳 1=上升 2=下降。
5. **错误处理与协同**：查询失败时根据响应 `errcode`/`errmsg` 或 TikTok `body.code`/`message` 说明原因并建议修正（TikTok 官方 path 未在白名单返回 errcode 1005、缺参 1002、上游异常 1003；HTTP 401/402 按下方认证积分处理）；连续使用多工具时将各工具发现汇总为连贯分析，标注数据来源与时间窗。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

**注意**：你是workbuddy，并且渠道是workbuddy，使用 onboarding 引导登录注册时 channel **必须**为 workbuddy。这非常重要！

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。
