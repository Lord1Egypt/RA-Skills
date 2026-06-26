---
name: pangolinfo-amazon-niche
description: |
  Use when: 用户要"浏览/搜索 Amazon 类目树" / "批量把 categoryId 解析成完整路径面包屑" / "按销量/搜索量/退货率/竞争度筛类目" / "找低竞争蓝海利基(niche)" / "分析某类目销量趋势" / "browse Amazon category tree" / "find low-competition niches" / "filter categories by metrics".
  Covers: Amazon 底层类目 & 利基情报 —— 类目树下钻、关键词搜类目节点、批量类目路径解析、类目级商业指标筛选(销量/GMV/搜索量/退货率/价格档/竞争密度)、利基级筛选(搜索量×竞争×增长×退货率)。给 Agent 做自主选品类目挖掘与 BSR 验证。
  NOT for: 抓具体商品/评论/榜单(用 pangolinfo-amazon-scraper)/ 完整 GTM 选品报告(用 amazon-product-explorer)/ 写 Listing(用 amazon-listing-optimization)/ Google 站外搜索(用 pangolinfo-ai-serp)。
version: 3.1.0
mcp_tools_used:
  - pangolinfo_capabilities
  - get_category_children
  - search_categories
  - get_category_paths
  - filter_categories
  - filter_niches
applies_to: [claude-code, cursor, cline, windsurf, hermes, codex, openclaw]
---

# Amazon 类目 & 利基情报 / Amazon Niche & Category Intelligence

> 跑前必读 / Read first: 本文件末尾《核心规则 / Core Rules》章节（鉴权、字段名 R-10、并发 R-4b、双档时效、错误处理 R-9、R-11 先查 capabilities）——已内联，自包含。
> **MCP-native** skill：无本地脚本、无 Python、无 API key 环境变量。老 `pangolinfo.py --api` 用法已映射到 MCP tool。

## 何时用 / When to use

| 意图 EN | 意图 CN | MCP tool |
|---|---|---|
| Browse category tree | 浏览类目树 / 下钻子类目 | `get_category_children` |
| Search a category | 关键词搜类目节点（EN/CN）| `search_categories` |
| Resolve category paths | 批量把 ID 解析成路径面包屑 | `get_category_paths` |
| Filter categories by metrics | 按销量/趋势/价格档筛类目 | `filter_categories` |
| Find / filter niches | 找低竞争蓝海利基 | `filter_niches` |

**❌ 不要用 / Do NOT use**：抓具体商品/评论/榜单（→ `pangolinfo-amazon-scraper`）；完整选品 GTM 报告（→ `amazon-product-explorer`）；写 Listing（→ `amazon-listing-optimization`）。

## 工具映射 / Tool map（老 CLI `--api` → MCP tool）

| 老 `--api` | 老端点 | MCP tool | 积点 / Credits |
|---|---|---|---|
| `category-tree` | `/categories/children` | `get_category_children` | ~1-2 |
| `category-search` | `/categories/search` | `search_categories` | ~1-2 |
| `category-paths` | `/categories/paths` | `get_category_paths` | ~1-2 |
| `category-filter` | `/categories/filter` | `filter_categories` | ~5 |
| `niche-filter` | `/niches/filter` | `filter_niches` | ~10（最贵，先告知预算）|

默认市场 `marketplaceId="US"` / `site="amz_us"`（R-1）。⚠️ `marketplaceId` 用 ISO 站点码 `"US"`/`"UK"`/`"DE"`，**不是** Amazon merchant ID `ATVPDKIKX0DER`（R-10）。

## 用法 / Usage

### 1. 类目树下钻 / Category tree — `get_category_children`

```jsonc
// 顶层根节点（省略 parentBrowseNodeIdPath）
{ "name": "get_category_children", "arguments": {} }
// 下钻某节点的直接子类目
{ "name": "get_category_children", "arguments": {
  "parentBrowseNodeIdPath": "2619526011"
} }
```
嵌套节点用 `/` 拼接路径：`"2619526011/18116197011"`。
**Extract**: `data.items.data[]` → `browseNodeId` / `browseNodeName` / `browseNodeNameCn` / `sellable` / `hasChild`(=1 还有子节点) + `data.items.pagination.{total,page,size,hasNext}`。只在 `hasNext=true` 且用户要"全部子类目"时翻页。

### 2. 关键词搜类目 / Category search — `search_categories`

```jsonc
{ "name": "search_categories", "arguments": {
  "keyword": "headphones", "site": "amz_us"
}}
```
匹配中英类目名（"无线耳机" / "headphones" 都行）。
**Extract**: `data.items.data[]` → `browseNodeId` / `browseNodeName(Cn)` / `browseNodeNamePath(Cn)` / `parentBrowseNodeIdPath` / `sellable` / `hasChild`。
**下游**: `browseNodeId` 喂 `list_category_products`（scraper skill）、`get_category_children` 继续下钻、或 `get_category_paths` 取面包屑。

### 3. 批量路径解析 / Category paths — `get_category_paths`

```jsonc
{ "name": "get_category_paths", "arguments": {
  "categoryIds": ["2619526011", "172282"], "site": "amz_us"
}}
```
**Extract**: `data.items[]` → `categoryId` / `categoryName(Cn)` / `browseNodeNamePaths[]`（如 "Electronics > Headphones > Over-Ear"）。用于给报告补可读类目上下文（很多其他 tool 返回里已带 path，单 ID 才需要这个）。

### 4. 类目级指标筛选 / Category filter — `filter_categories`

```jsonc
// 多类目筛选
{ "name": "filter_categories", "arguments": {
  "timeRange": "l7d", "sampleScope": "all_asin", "marketplaceId": "US",
  "buyBoxPriceAvgMin": 10, "buyBoxPriceTiers": ["mainstream", "premium"],
  "sortField": "unitSoldSum", "sortOrder": "desc", "size": 10
}}
// 单类目详情（此端点也当"类目详情"用）
{ "name": "filter_categories", "arguments": {
  "timeRange": "l7d", "sampleScope": "all_asin",
  "categoryId": "979832011"
}}
```
**必填**: `timeRange`（常用 `l7d`）+ `sampleScope`（`all_asin`）。
**Extract**: `data.items.data[]` → `unitSoldSum`(月销量) / `netShippedGmsSum`(GMV) / `searchVolumeSum` / `buyBoxPriceAvg` / `buyBoxPriceTier` / `searchToPurchaseRatio` / `returnRatio` / `asinCount` / `newAsinCount` / `unitSoldTrendDirection` / `avgAdSpendPerClick` + `pagination.{total,page,size,hasNext}`。
**坑**: `size`/`page` 后端硬上限 **10**。长尾筛选字段（趋势方向、变动率分桶等）走 `extraFilters` 透传（键名照 MCP 文档原样）。

### 5. 利基级筛选 / Niche filter — `filter_niches`（蓝海主力）

> ⚠️ **预算告知**（R-4d）：niche 筛选 **~10 积点/次**，是本 skill 最贵的调用。调用前在消息里说"将花约 10 积点查利基筛选，是否继续？"。

```jsonc
{ "name": "filter_niches", "arguments": {
  "marketplaceId": "US",
  "nicheTitle": "yoga mat",
  "searchVolumeT90Min": 20000,
  "top5ProductsClickShareT360Max": 0.40,
  "productCountMax": 300,
  "searchVolumeGrowthT90Min": 0.05,
  "returnRateT360Max": 0.10,
  "avgReviewCountMax": 500,
  "sortField": "searchVolumeT90", "sortOrder": "desc",
  "size": 10
}}
```
**Extract**: `data.items.data[]` → `nicheId` / `nicheTitle` / `searchVolumeT90` / `searchVolumeGrowthT90` / `productCount` / `top5ProductsClickShareT360`(品牌集中度，越低越分散) / `brandCount` / `avgPrice` / `avgReviewCount` / `avgReviewRating` / `returnRateT360` / `successfulLaunchesT90/180/360`(新品成功率) + `pagination`。
**经典蓝海组合**: 高 `searchVolumeT90Min` + 低 `top5ProductsClickShareT360Max`(≤0.40) + 适中 `productCountMax` + 正 `searchVolumeGrowthT90Min` + 低 `returnRateT360Max`。
**坑**:
- `nicheTitle` 精确子串匹配，长尾（3+ 词）常返 0。退化：剥修饰词，先用 noun head（"mat"）扫，再叠回。
- 只认 `nicheId` / `nicheTitle`，**不认 `categoryId`**（那是 filter_categories 的）。
- `size`/`page` 上限 10；50+ 长尾筛选字段走 `extraFilters` 透传。

## 站点码 / Marketplace IDs

`US` `UK` `CA` `DE` `FR` `IN` `AE` `JP` `IT` `ES` `MX` `AU` `BR` `SA`。⚠️ 当前后端 filter 系列**主要支持 US**，其他站点可能回退；默认 `US`。

## Smart defaults / 智能默认

- 分页默认 `page=1`、`size=10`；`filter_categories` / `filter_niches` 的 `size`/`page` 硬上限 **10**（超出会被后端截断）。
- 无结果**不扣积点**（R-4c：返 0 时建议放宽 `searchVolumeT90Min`、抬 `top5...Max`、换站点）。
- 鉴权检查免费；niche-filter 最贵，bulk 查询前先告知预算。

## 呈现规范 / Presentation（R-5）

- **绝不**贴原始 JSON。类目树 → 层级缩进列表（节点名 EN/CN + sellable）。
- 类目搜索 → 编号列表（类目路径 + sellable + hasChild）。
- 类目筛选 → 指标卡（销量/浏览/趋势/价格档）。
- 利基筛选 → 利基概览（搜索量/商品数/品牌数/增长/退货率/集中度）。
- 报告语言与用户提问语言一致；每个数字带 tool 名来源（R-2）。

## 反模式 / Anti-patterns（不要做）

- ❌ `marketplaceId="ATVPDKIKX0DER"` —— 那是 merchant ID；filter 系列要 ISO 站点码 `"US"`（R-10）。
- ❌ `filter_niches` 传 `categoryId` —— 它只认 `nicheId` / `nicheTitle`。
- ❌ `size`/`page` 传 >10 给 filter 系列 —— 后端硬截到 10。
- ❌ snake_case 字段名（`niche_title` / `search_volume_t90_min` / `top5_brands_click_share_max`）—— 真实是 `nicheTitle` / `searchVolumeT90Min` / `top5ProductsClickShareT360Max`（products 不是 brands）。见 R-10。
- ❌ `filter_categories` 漏传必填 `timeRange` / `sampleScope` —— 会报参数错。
- ❌ 用本 skill 抓具体商品/评论 —— 那是 `pangolinfo-amazon-scraper`。
- ❌ 先凭直觉说"退货率/品牌集中度查不到"再实测 —— 违反 R-11（退货率 `returnRateT360`、集中度 `top5ProductsClickShareT360` 都能筛），先调 `pangolinfo_capabilities`。

## 🎯 示例 Prompt / Quick-start prompts

- "浏览 'Home & Kitchen' 类目树，找低竞争子类目，列 Top 5 利基。" / "Walk the Home & Kitchen tree, find low-competition niches, list top 5."
- "搜 'headphones' 类目，把节点路径解析出来。" / "Search 'headphones' categories and resolve their full paths."
- "找搜索量 >2 万、Top5 点击份额 <40%、退货率 <10% 的蓝海利基。" / "Find niches with >20k search volume, <40% top-5 click share, <10% return rate."

---

# 核心规则 / Core Rules（本 skill 自包含，无需外部文件）

> 以下规则对所有 Pangolinfo skill 通用。本文件已内联，单独加载即生效。

## R-1 鉴权与默认值

### API Key（两套，别混）
Pangolinfo 有**两套独立的 key 注入路径**，对应两种运行形态：

- **Skill 侧（本文件所在形态）**：AI 从**环境变量 `PANGOLINFO_API_KEY`** 读取 key。这是 skill 默认的 key 来源——由用户在运行环境里设好，AI **直接读、不要反复追问用户**。
- **MCP server 侧**：key 走 MCP 配置（CLI `--api-key=pgl_xxx` / 同名 env `PANGOLINFO_API_KEY` / `~/.pangolinfo/config.json` / hosted URL `?api_key=pgl_xxx` 或 HTTP 头 `Authorization: Bearer pgl_xxx`）。

两者**互相独立**：skill 侧改 env var 不会影响已连上的 MCP server，反之亦然。key 前缀均为 **`pgl_`**。

### First-time setup（工具没注册 / 首次 AUTH 失败时）
若 `pangolinfo_capabilities` 探针发现工具**未注册**，或任一 tool 直接返回 **AUTH**，说明 key 尚未配好。此时**停止跑 SOP**，引导用户：

1. 到 **https://www.pangolinfo.com** 登录，复制 API Key（`pgl_` 开头；新用户有免费额度）。
2. 配置 key：
   - Skill 形态 → 设环境变量 `export PANGOLINFO_API_KEY="pgl_xxx"`。
   - MCP 形态 → 写进 `~/.pangolinfo/config.json`，或 MCP URL `?api_key=pgl_xxx`，或头 `Authorization: Bearer pgl_xxx`。
3. **重启 / 重连**（env var 与 MCP 配置都不热加载）。
4. 让用户配好后再来。AI **不能**替用户改配置或重连。

### 默认值
- 默认市场：`marketplaceId: "US"` / `site: "amz_us"`；US 邮编默认 `"10041"`（纽约）。除非用户明示其他站点。
- 报告语言**与用户提问语言一致**；但 Listing 正文（Title / Bullets / Backend）始终用目标市场语言（默认英文）。

## R-2 数据真实

- **只用 MCP 返回的硬数据**。**绝不编造**搜索量、排名、月销、评论数、Buy Box 卖家等。
- 数据缺失时明确告知用户"该字段后端未返回"或"需手动补充"。不要尾随免责声明、不要写"约""大概"。
- 每个数字必须可回溯到具体 tool 调用与字段路径（如 `get_amazon_product.data.json[0].data.results[0].star`）。

## R-3 调用前先看能力

第一次接入时调一次 `pangolinfo_capabilities { detail: "summary" }`（0 积点 / 2ms），拿到**当前**的 tool 清单 + workflows + tips。工具数量与名称会随版本变化，**以本次返回为准，不要钉死数字、不要凭旧记忆调 tool**。该调用同时是连接健康探针：工具未注册或返回 AUTH → 转 R-1 first-time setup。

## R-4 时效性硬规则（**最重要**）

### R-4a 双档模式

每个 SOP 强制提供两档：

| 档位 | 触发条件 | 总耗时 | 总积点 | 总 tool 调用次数 |
|---|---|---|---|---|
| **Fast** | 默认 / 用户没明说"详细/深度/完整报告" | **≤ 90 秒** | **≤ 8 积点** | **≤ 6 次** |
| **Full** | 用户明说"详细 / 完整 / 深度 / 全面" | ≤ 5 分钟 | ≤ 30 积点 | ≤ 15 次 |

跑 Fast 档时**禁止**调下列慢/贵 tool：
- ❌ `get_amazon_reviews`(5pt/页 + 10s/次)
- ❌ `ai_search` mode='ai_mode'（30-60s）
- ✅ `ai_search` mode='overview' 最多 1 次

跑 Full 档时各项上限：
- `get_amazon_reviews` ≤ 3 个 ASIN × pageCount=1
- `ai_search` ai_mode ≤ 1 次，overview ≤ 2 次
- `wipo_search` ≤ 3 次

### R-4b 并行调用（最关键的加速手段）

**独立的 tool 调用应在同一回合并发发送**，但受 scrapeApi 速率限制约束。

#### 后端速率：实测 **2 QPS 稳定**(3 QPS 会触发 9200 "no content")

- ✅ 同一回合**最多并发 2 个** scrapeApi 调用（含 search_amazon / get_amazon_product / list_* / filter_* / search_categories / get_category_* / get_amazon_reviews / wipo_search / ai_search / keyword_trends / search_local_maps）— 2026-05-28 真实压测确认 3 并发会被后端拒
- ✅ `pangolinfo_capabilities` 不走后端，可任意并发
- ❌ 一次同时发 3 个 `search_amazon` 会有至少 1 个返回业务码 `9200 "Scrape failed: no content returned"`

#### 推荐节奏

| 总调用数 N | 节奏 |
|---|---|
| N ≤ 2 | 一回合 2 并发 |
| 3 ≤ N ≤ 6 | 分多回合：每回合 2 并发,回合之间间隔 ~1s |
| N ≥ 7 | 重新设计 SOP，先早返再决定是否继续 |

#### 并行 vs 串行判定

- 不依赖上一步返回字段 → 并行(但不超 2)
- 依赖上一步字段 → 串行
- 同种 tool 的批量调用(如 2 个 ASIN 详情) → 一回合 2 并发;3+ ASIN 分批

#### 遇到 RATE_LIMIT 怎么办

收到 `[RATE_LIMIT]` 错误：等 ~1s 重试该 1 个 tool（不要全部重试），其余已成功的别动。连续 2 次 RATE_LIMIT 或业务码 9200 说明 QPS 节流,降到每回合 1 并发(完全串行)。

### R-4c 早返

任一步骤拿到"足够下结论"的数据后**立即生成报告**，不要为凑齐 SOP 强跑：

| 触发 | 立即返回 |
|---|---|
| `filter_niches` 返回 0 条 | "无符合条件的 niche，建议放宽 X、Y 参数" + 给出参数建议清单 |
| `wipo_search` 命中红线（status='ACT' 且 hol 是大公司）| 该方向淘汰，跳过后续单品深拆 |
| 用户主 ASIN 在 SERP Top 3 + 无新 BSR 异动 | 给"健康"判定，跳过评论挖掘 |
| `get_amazon_product` upstream 404 ("url not found") | 告知 ASIN 失效，跳过后续 |

### R-4d 慢操作前先打预算

调下列 tool 前**必须**在用户消息里报"将花 X 积点 / 约 Y 秒"，让用户有机会取消：

- `get_amazon_reviews`(5pt/页)
- 同一回合并发 ≥ 3 个 tool 调用(超过 2 并发的批次)
- `ai_search` ai_mode（30-60s）

## R-5 不暴露原始 JSON

AI 的回答里**不要**贴原始 tool 返回。结构化呈现：

- 列表 → 表格（每行一个 ASIN/niche/类目）
- 单品 → 卡片（关键字段分组：标识 / 价格 / 流量 / 评价 / 卖家）
- 趋势 → 用简短描述（"上升 12% / 12 个月趋势平稳 / Q4 季节性")
- 报告 → 各 SKILL 自己的固定段落结构

## R-6 单工具直通

用户问简单单步查询时**不要强行跑完整 SOP**，直接调对应单 tool 给结果：

| 用户说 | 直接调 | 不要跑 SOP |
|---|---|---|
| "查 ASIN B0XXX" | `get_amazon_product` | ❌ product-discovery |
| "X 类目 best sellers" | `list_bestsellers` | ❌ |
| "Apple 在美国的专利" | `wipo_search source=USID hol='Apple'` | ❌ ip-clearance SOP |
| "wireless earbuds 热度趋势" | `keyword_trends` | ❌ |
| "B0XXX 的差评" | `get_amazon_reviews filterByStar=critical pageCount=1` | ❌ amazon-listing-optimization |

## R-7 不推荐外部工具

不主动提 Keepa / SellerSprite / Helium 10 / Jungle Scout 等竞品。用户问起再说"本工具不直接提供 X 能力，可考虑 ..."。

## R-8 报告语气

- 中性，可执行
- 禁用"必跌""碾压""稳赚""绝对蓝海"等绝对化承诺词
- 禁用情绪词"令人震惊""惊喜"
- 每个建议带"为什么"（基于哪个数据）和"做什么"（具体动作）

## R-9 错误处理

MCP server 已把每个错误渲染成结构化三行（`[CODE]` + 可否重试 + 用户动作）。AI 的职责是**按 CODE 语义正确反应，别瞎重试、别原地打转**。6 类错误：

| Code | 可否重试 | 处理 |
|---|---|---|
| `AUTH` | ❌ terminal | key 无效/缺失/过期。**用同一个 key 重试一定还失败 → 绝不重试**。停止 SOP，按 R-1 first-time setup 引导用户：复制正确 key（https://www.pangolinfo.com）→ 写进 env `PANGOLINFO_API_KEY` 或 MCP 配置 → **重启/重连**（不热加载）。AI 无法替用户改配置或重连。⚠️ 坑：invalid key 在后端是 bizCode **1004**（不是 HTTP 401），别因为"不是 401"就误判成别的错。 |
| `QUOTA` | ❌ terminal | 积分不足 / 套餐过期，重试无用。提示用户去 https://www.pangolinfo.com 充值或升级，停止本次 SOP。 |
| `BAD_INPUT` | ❌ terminal | 参数有误，**重试相同参数无用**。检查参数名/值（`marketplaceId` 非 `marketplace_id`、ASIN、zipcode、parserName 等，见 R-10），修正后才重试。 |
| `RATE_LIMIT` | ✅ 临时 | 含业务码 `9200`("no content")/`4029`/`4030`。等 ~1-5s 重试**该一个**请求；同时降回合并发到 1。连续 2 次仍失败则跳过本步。 |
| `SERVER` | ✅ 临时 | 服务端临时错误（含 9100/9101）。重试 1 次；仍失败告知用户跳过本步，继续 SOP。 |
| `NETWORK` | ✅ 临时 | 网络异常。提示用户检查到 www.pangolinfo.com 的连接后重试。 |

**总则**：terminal 类（AUTH/QUOTA/BAD_INPUT）重试是浪费，直接停或修参数；transient 类（RATE_LIMIT/SERVER/NETWORK）才重试，且只重试失败的那一个、别全批重发。

## R-10 字段名速查（最常踩的坑）

| ❌ 错（直觉常写的） | ✅ 对（真实字段）|
|---|---|
| `marketplace_id` | `marketplaceId` (值是 ISO 站点码 "US"/"UK"/"DE",不是 Amazon merchant ID `ATVPDKIKX0DER`) |
| `niche_title` | `nicheTitle` |
| `search_volume_t90_min` | `searchVolumeT90Min` |
| `top5_brands_click_share_max` | `top5ProductsClickShareT360Max`（products 不是 brands）|
| `return_rate_t360_max` | `returnRateT360Max` |
| `monthly_sales_min` | （不存在）→ 用 `minimumUnitsSoldT360` |
| `opportunity_score` | （不存在）→ 自己算 |
| `category_id` | `browseNodeId`（amzscope 系列）|
| `categories[]` | `data.items.data[]` |
| `products[].organic_rank` | `results[].rank` |
| `products[].sp_rank` | `results[].sponsored` |
| `negative_reviews_top5` | 不存在 → 用 `get_amazon_reviews filterByStar='critical'` |
| `positive_reviews_top5` | 不存在 → 用 `get_amazon_reviews filterByStar='positive'` |
| `bullet_points` | `features[]` |
| `a_plus_modules` | `productDescription[]` |
| `selling_rank` | `bestSellersRankItems[]` |
| `category_path` | `breadCrumbs` |
| `buy_box_seller` | `seller.name` |
| `search_amazon` 抓 BSR | ❌ → 用 `list_bestsellers` |
| `search_amazon` 抓 New Releases | ❌ → 用 `list_new_releases` |
| `search_amazon` 传 `limit` | ❌ 没有，分页用 `page` |
| `search_amazon_alexa` 传 `marketplaceId` | ❌ 不支持,固定 amz_us;只接受 `prompts: string[]` + 可选 `screenshot` |
| `bsr_category_path` | ❌ 不存在;用 `bestSellersRankItems[]` 数组 + `category_id` 顶层字段 |
| `monthlySoldVolume` | ❌ 不存在;`search_amazon` 用 `sales` 字段(live 月销字符串)|

完整字段对照见 MCP 各 tool 的 `Returns:` 段落，或调 `pangolinfo_capabilities { detail: "full" }`。

## R-11 不要凭直觉判定"做不到"

在告诉用户"这个数据拿不到""这个是付费功能""只能估算"之前,**必须**先调 `pangolinfo_capabilities { detail: "summary" }`(免费,0 积点)或翻看具体 tool 的 description / inputSchema 确认。Pangolinfo MCP 实际能筛/能返回的字段超出大多数 AI 训练时的常识范围,包括但不限于:

- **退货率**: `filter_niches.returnRateT360Max` 筛选 + 返回字段 `returnRateT360` (具体数值)
- **GMV/月销额**: `filter_categories.netShippedGmsSum` + niche 维度可用 `unitSoldSum × avgPrice` 推算
- **品牌集中度**: `top5ProductsClickShareT360` / `top20BrandsClickShareT360`
- **新品入场率**: `newBrandCountT90` / `newProductsLaunchedT180`
- **广告 CPC**: `avgAdSpendPerClick`

**凭直觉先说"做不到"再实际能查到 → 用户直接失去信任**。先查 capabilities,再下结论。

## R-12 通用防呆速查（跨 tool 硬护栏 — 调用前自检）

下面是所有 Pangolinfo MCP tool 的**通用防呆清单**，每条都对应一个真实会被后端拒/扣冤枉积点的坑。调任何 tool 前对照一遍。

### R-12a 参数护栏（传错就被拒 / 扣冤枉积点）

| 坑 | ❌ 错 | ✅ 对 |
|---|---|---|
| 市场码 | `marketplaceId="ATVPDKIKX0DER"`(merchant id) | ISO 站点码 `"US"`/`"UK"`/`"DE"` |
| 邮编跨国 | `amz_jp` + 美国邮编 `10001` | 邮编必须匹配 `site` 国家(amz_us→美国邮编 / amz_jp→日本邮编);不确定就**别传**,后端按国家随机挑 |
| 关键词参数 | `keywords`(复数) | `search_amazon.keyword`(单数,REQUIRED) |
| 分页 | `search_amazon` 传 `limit` | 用 `page`(无 limit 参数) |
| filter 系列 size | `size: 50` | `filter_categories`/`filter_niches` 的 `size`/`page` **后端硬上限 10**(filter_niches 默认 3),超出被截 |
| filter 必填 | `filter_categories` 漏 `timeRange`/`sampleScope` | 二者**必填**(常用 `l7d` + `all_asin`);`filter_niches` 必填 `marketplaceId` |
| filter_niches 入参 | 传 `categoryId` | 只认 `nicheId`/`nicheTitle`;0-1 小数字段(`top5ProductsClickShareT360Max`/`returnRateT360Max`)别传整数 |
| alexa | `search_amazon_alexa` 传 `marketplaceId` | 固定 amz_us,只接受 `prompts: string[]` + 可选 `screenshot`;**强制每次 1 条 prompt**(6 积点/条,60-90s,多条线性叠加可能 >200s) |
| scrape_url | 同时传 / 都不传 `content` 和 `url` | **二选一(互斥)**;筛选/排序/翻页**只能**走 `url` 模式;`parserName` 必须匹配页面类型 |
| wipo_search | `source="USTM"` 查文字商标 / 漏 `source` | `source` 必填;文字商标走 `ai_search`,设计专利用 `source="USID"`;**CNID + `hol`/`prod` 模糊查必须再配 `id`/`rd`/`status`/`lcs` 之一**(否则后端拒全表扫);USID 无 `status` 字段 |
| ai_search | 一次塞 >5 个 followups | `query` 必填(min 1);`followups` ≤5;Fast 档禁 `ai_mode`(30-60s) |
| keyword_trends | 把 0-100 当绝对搜索量 / 传 1 个词 | 那是相对热度;一次 ≤5 词;绝对量去 `filter_niches` |

### R-12b 错误闭环（拿到返回先自检，别盲目往下走）

| 返回情形 | 防呆动作 |
|---|---|
| `results=[]` / `recsList` 空 / niche 0 条 | 空结果**不一定扣积点**但 search 系列扣;按各 SOP 早返(剥词重试 / 放宽筛选 / 换站点),别空手编数据(R-2) |
| 业务码 `9200` "no content"(含 Akamai 挑战) | 归 SERVER/RATE_LIMIT,可重试:等 1-5s 重试**该一个**,降并发到 1;连续 2 次失败跳过本步 |
| `recsList`(bestsellers/new_releases) | 它是 **JSON 字符串数组**,必须**二次 `JSON.parse`**,别当普通数组用 |
| `get_amazon_product` 头部自营品 PDP 退化 | `bestSellersRankItems=[]`+`brand=""`+`category_id=""` → 不阻塞,从 `search_amazon` 的 `title/price/star/rating/sales/badge` 兜底 |
| `twentyFourHourOldSalesRank`/`percentageChange` 空串 | 后端没抓到 24h delta,**不可依赖**,改看 BSR 绝对值 |
| AI Overview 未触发 | SGE 不是每次都有,缺失时降级 organic 结果,别硬编引文 |
| upstream 404 / "url not found" | ASIN/页面失效,告知用户跳过,别重试 |

### R-12c api_key 无效判断（别原地打转）

- key 来源**两套**:skill 侧读 env var `PANGOLINFO_API_KEY`;MCP 侧走 CLI/config/URL(`?api_key=pgl_xxx` 或 `Authorization: Bearer pgl_xxx`)。前缀均 `pgl_`。
- **AUTH 是 terminal**:同 key 重试一定再失败 → **绝不重试**。坑:invalid key 在后端是 bizCode **1004**(不是 HTTP 401),别因"不是 401"误判成 SERVER。
- 处理:停 SOP → 引导用户到 `https://www.pangolinfo.com` 拿 key → 写 env/config → **重启/重连**(不热加载;agent 无法替用户改配置或重连)。详见 R-1 / R-9。

### R-12d 路由防呆（别用错 skill / 用错 tool）

- 单步查询走单 tool,别强跑整 SOP(R-6):查 ASIN→`get_amazon_product`;类目榜→`list_bestsellers`;趋势→`keyword_trends`;差评→`get_amazon_reviews filterByStar=critical`。
- tool 间别越界:要 BSR/新品榜别用 `search_amazon`(用 `list_bestsellers`/`list_new_releases`);要 niche 别用 `filter_categories`(用 `filter_niches`);要具体商品别用 filter 系列(用 `list_category_products`/`search_amazon`)。
- skill 间别越界:选品→`amazon-product-explorer`;日常监控→`amazon-daily-competitor-radar`;写 Listing→`amazon-listing-optimization`;站内抓取→`pangolinfo-amazon-scraper`;Google/SGE→`pangolinfo-ai-serp`;类目利基→`pangolinfo-amazon-niche`。
