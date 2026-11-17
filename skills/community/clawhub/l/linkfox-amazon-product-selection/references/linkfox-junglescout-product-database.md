---
name: linkfox-junglescout-product-database
description: 利用Jungle Scout产品数据库，通过品类、销量、价格、BSR排名、评论等核心多维条件筛选亚马逊潜力商品。
---

# Jungle Scout 产品数据库查询

本技能通过 LinkFox 工具网关调用 Jungle Scout 产品数据库，对 10 个亚马逊站点的商品进行多维条件筛选，帮助卖家发现潜力选品。完整请求参数、响应字段与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按品类、价格、销量、收入、评论数、评分、重量、BSR 排名、LQS、卖家类型等多维度筛选亚马逊商品。
- 覆盖 10 个站点（us/uk/de/in/ca/fr/it/es/mx/jp），支持关键词包含/排除、排除头部品牌、新品发现等。
- 通过月销量、月收入范围圈定市场规模；以评论数、评分、卖家数量评估竞争度；以 LQS 发现 Listing 优化空间。

### ❌ 边界与限制

- **marketplace 必填**：每次查询必须指定站点，未指定时默认 `us`。
- **品类名需匹配**：`categories` 值必须与对应站点的英文标准主分类名完全一致。
- **关键词限制**：`includeKeywords` / `excludeKeywords` 最多各 100 项，每项最长 50 字符。
- **数据时效**：数据来源于 Jungle Scout 定期更新，非实时数据。
- **评分与重量**：`minRating` / `maxRating` 取值 1.0-5.0；`minWeight` / `maxWeight` 以磅（pounds）为单位。
- **成本约束**：本工具消耗积分；同一会话同一参数组合默认只调用一次，失败/空结果不得自动换关键词、翻页连续试探。
- **不在范围内**：关键词搜索量/趋势分析（用关键词历史搜索量工具）；ABA 搜索词排名（用 ABA 工具）；商品详情页/Listing 内容分析；广告/PPC 投放策略；非亚马逊平台商品数据。

## 核心概念

Jungle Scout 产品数据库是亚马逊商品级别的多维筛选工具，帮助卖家从海量商品中快速锁定目标产品：

- **品类选品**：按亚马逊主分类筛选特定品类下的商品。
- **销量/收入筛选**：通过月销量和月收入范围圈定市场规模合适的产品。
- **竞争度评估**：通过评论数、评分、卖家数量判断竞争激烈程度。
- **Listing 质量评估**：LQS（Listing Quality Score，1-10 分）帮助发现优化空间大的产品。
- **产品类型过滤**：区分 FBA/FBM/AMZ 卖家类型、标准尺寸/超大尺寸。
- **新品发现**：通过上架日期筛选近期上架的新品。

**内部分页**：API 自动处理分页；通过 `needCount` 指定需要的结果总数，后端在内部跨页抓取。

**支持站点**：us（美国）、uk（英国）、de（德国）、in（印度）、ca（加拿大）、fr（法国）、it（意大利）、es（西班牙）、mx（墨西哥）、jp（日本）。未指定时默认 `us`。

## 调用方式

- **API 端点**：`POST /tool-jungle-scout/product-database/query`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/junglescout_product_database.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-junglescout-product-database-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 如何构建查询

仅 `marketplace` 为**必填**，其余均为可选筛选条件，组合使用以缩小结果范围。

### 构建查询的原则

1. **站点映射**：用户说"美国站"→ `us`，"日本站"→ `jp`，"德国站"→ `de`；未指定时默认 `us`。
2. **关键词**：`includeKeywords` 支持逗号分隔多个词（匹配标题或 ASIN），如 `yoga mat,fitness`；`excludeKeywords` 排除含特定词的商品。
3. **品类匹配**：`categories` 必须使用对应站点的英文标准分类名，如美国站 `Sports & Outdoors`、`Home & Kitchen` 等；多个品类逗号分隔。
4. **数值范围**：min/max 成对使用，可只传一端；如只设 `minSales=300` 表示月销量≥300。
5. **排序**：`sort` 字段名前加 `-` 表示降序，如 `-sales` 按销量从高到低；默认按 `name` 升序。
6. **结果数量**：`needCount` 控制返回结果总数，不设则返回默认数量。

### 常见查询场景

**1. 关键词搜索 + 按销量筛选**
```json
{
  "marketplace": "us",
  "includeKeywords": "yoga mat",
  "minSales": 300,
  "maxSales": 5000,
  "sort": "-sales",
  "needCount": 50
}
```

**2. 品类 + 价格区间筛选**
```json
{
  "marketplace": "us",
  "categories": "Home & Kitchen",
  "minPrice": 15,
  "maxPrice": 50,
  "minSales": 100,
  "sort": "-revenue",
  "needCount": 50
}
```

**3. 高评分低竞争选品（评论少但评分高）**
```json
{
  "marketplace": "us",
  "categories": "Beauty & Personal Care",
  "minRating": 4.0,
  "maxReviews": 200,
  "minSales": 100,
  "sort": "-sales",
  "needCount": 50
}
```

**4. 仅 FBA 产品筛选**
```json
{
  "marketplace": "us",
  "includeKeywords": "phone stand",
  "sellerTypes": "fba",
  "productTiers": "standard",
  "minSales": 200,
  "sort": "-sales",
  "needCount": 50
}
```

**5. 排除头部品牌 + 发现蓝海机会**
```json
{
  "marketplace": "us",
  "categories": "Sports & Outdoors",
  "excludeTopBrands": true,
  "minSales": 300,
  "maxReviews": 500,
  "minRating": 4.0,
  "sort": "-sales",
  "needCount": 50
}
```

**6. 按上架日期发现新品**
```json
{
  "marketplace": "us",
  "categories": "Electronics",
  "minUpdatedAt": "2026-01-01",
  "minSales": 50,
  "sort": "-sales",
  "needCount": 50
}
```

## 展示规则

1. **表格呈现**：以结构化表格展示关键列：商品标题、品牌、价格、月销量、月收入、BSR 排名、评论数、评分、LQS。
2. **排序说明**：提醒用户当前应用的排序方式及返回结果数量。
3. **亮点标注**：标记评论少但销量高的产品（潜在机会），或 LQS 评分较高的产品。
4. **费用明细**：当用户询问盈利情况时，展示 `feeBreakdown` 详情（FBA 费用、推荐费、总费用）。
5. **图片链接**：展示单个商品详情时附 `imageUrl`。
6. **错误处理**：查询失败时根据错误响应说明原因，并建议调整参数。

## 用户表达与场景速查

**适用** —— 亚马逊商品多条件筛选与发现：

| 用户说 | 场景 |
|--------|------|
| "帮我找月销量500以上的瑜伽垫" | 关键词 + 销量筛选 |
| "美国站厨房品类30美金以下有什么好产品" | 品类 + 价格筛选 |
| "评论少但评分高的蓝海产品" | 高评分低竞争选品 |
| "找FBA标准尺寸的手机支架" | 卖家类型 + 产品尺寸筛选 |
| "排除大品牌的运动品类机会" | 排除头部品牌 |
| "最近新上架的电子产品有哪些卖得好" | 新品发现 |
| "BSR排名1万以内的家居产品" | BSR排名筛选 |
| "LQS低于5分的高销量产品" | Listing优化机会 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# Jungle Scout 产品数据库查询 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/tool-jungle-scout/product-database/query`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| marketplace | string | 是 | 目标市场代码。可选值：`us`、`uk`、`de`、`in`、`ca`、`fr`、`it`、`es`、`mx`、`jp` |

### 关键词筛选

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| includeKeywords | string | 否 | 标题/ASIN包含关键词，逗号分隔，最多100项，每项最长50字符 |
| excludeKeywords | string | 否 | 标题/ASIN排除关键词，逗号分隔，最多100项，每项最长50字符 |

### 品类筛选

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| categories | string | 否 | 主分类名称，逗号分隔，需匹配对应站点的标准分类名。美国站示例：Appliances, Arts Crafts & Sewing, Automotive, Baby, Beauty & Personal Care, Books, CDs & Vinyl, Cell Phones & Accessories, Clothing Shoes & Jewelry, Collectibles & Fine Art, Computers, Digital Music, Electronics, Garden & Outdoor, Grocery & Gourmet Food, Handmade, Health Household & Baby Care, Home & Kitchen, Industrial & Scientific, Kindle Store, Kitchen & Dining, Movies & TV, Musical Instruments, Office Products, Pet Supplies, Sports & Outdoors, Tools & Home Improvement, Toys & Games, Video Games 等。其他站点（uk, de, fr, it, es, mx, jp, ca, in）有对应的本地分类名 |

### 价格 / 销量 / 收入

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minPrice | number | 否 | 最低价格 |
| maxPrice | number | 否 | 最高价格 |
| minSales | integer | 否 | 最低月销量 |
| maxSales | integer | 否 | 最高月销量 |
| minRevenue | number | 否 | 最低月收入 |
| maxRevenue | number | 否 | 最高月收入 |

### 评论 / 评分

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minReviews | integer | 否 | 最低评论数 |
| maxReviews | integer | 否 | 最高评论数 |
| minRating | number | 否 | 最低评分（1.0-5.0） |
| maxRating | number | 否 | 最高评分（1.0-5.0） |

### 重量 / 尺寸 / BSR

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minWeight | number | 否 | 最低重量（磅） |
| maxWeight | number | 否 | 最高重量（磅） |
| minRank | integer | 否 | 最低BSR排名 |
| maxRank | integer | 否 | 最高BSR排名 |
| minLqs | integer | 否 | 最低LQS评分（1-10） |
| maxLqs | integer | 否 | 最高LQS评分（1-10） |

### 卖家 / 产品类型

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minSellers | integer | 否 | 最少卖家数 |
| maxSellers | integer | 否 | 最多卖家数 |
| minNet | number | 否 | 最低净利润 |
| maxNet | number | 否 | 最高净利润 |
| sellerTypes | string | 否 | 卖家类型，逗号分隔。可选值：`amz`（亚马逊自营）、`fba`、`fbm` |
| productTiers | string | 否 | 产品尺寸层级，逗号分隔。可选值：`oversize`、`standard` |
| excludeTopBrands | boolean | 否 | 是否排除头部品牌 |
| excludeUnavailableProducts | boolean | 否 | 是否排除不可购买的商品 |

### 日期 / 分页 / 排序

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minUpdatedAt | string | 否 | 数据更新起始日期（YYYY-MM-DD） |
| maxUpdatedAt | string | 否 | 数据更新截止日期（YYYY-MM-DD） |
| needCount | integer | 否 | 需要返回的结果总数，API内部自动分页 |
| sort | string | 否 | 排序字段。可选值：`name`, `-name`, `category`, `-category`, `revenue`, `-revenue`, `sales`, `-sales`, `price`, `-price`, `rank`, `-rank`, `reviews`, `-reviews`, `lqs`, `-lqs`, `sellers`, `-sellers`。前缀 `-` 表示降序。默认：`name` |

### 站点映射

| 站点 | marketplace 值 |
|------|---------------|
| 美国 | us |
| 英国 | uk |
| 德国 | de |
| 印度 | in |
| 加拿大 | ca |
| 法国 | fr |
| 意大利 | it |
| 西班牙 | es |
| 墨西哥 | mx |
| 日本 | jp |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| costToken | integer | 消耗 token 数 |
| productDatabaseList | array | 产品数据列表 |

### productDatabaseList 数组中每个对象

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 产品唯一标识 |
| title | string | 产品标题 |
| brand | string | 品牌名称 |
| category | string | 主分类 |
| breadcrumbPath | string | 完整分类路径 |
| price | number | 当前售价 (USD) |
| approximate30DayUnitsSold | integer | 近30天预估销量 |
| approximate30DayRevenue | number | 近30天预估收入 (USD) |
| productRank | integer | BSR排名 |
| reviews | integer | 评论总数 |
| rating | number | 平均评分 (1.0-5.0) |
| listingQualityScore | integer | Listing质量评分 (LQS, 1-10) |
| numberOfSellers | integer | 在售卖家数 |
| sellerType | string | 卖家类型 (amz/fba/fbm) |
| imageUrl | string | 商品主图URL |
| dateFirstAvailable | string | 首次上架日期 |
| weightValue | number | 产品重量 |
| weightUnit | string | 重量单位 |
| lengthValue | number | 长度 |
| widthValue | number | 宽度 |
| heightValue | number | 高度 |
| dimensionsUnit | string | 尺寸单位 |
| parentAsin | string | 父体ASIN |
| isParent | boolean | 是否为父体 |
| isVariant | boolean | 是否为变体 |
| isStandalone | boolean | 是否为独立产品 |
| isAvailable | boolean | 是否可购买 |
| buyBoxOwner | string | Buy Box 持有卖家名 |
| buyBoxOwnerSellerId | string | Buy Box 持有卖家ID |
| updatedAt | string | 数据更新时间 |
| feeBreakdown | object | 费用明细：`fbaFee`（FBA费用）、`referralFee`（推荐费）、`variableClosingFee`（可变结算费）、`totalFees`（总费用） |
| subcategoryRanks | array | 子分类BSR排名列表，每项含 `subcategory`、`rank`、`id` |
| type | string | 资源类型 |
| variants | array | 变体列表 |
| upcList | array | UPC码列表 |
| eanList | array | EAN码列表 |
| isbnList | array | ISBN码列表 |
| gtinList | array | GTIN码列表 |
| dateFirstAvailableIsEstimated | boolean | 上架日期是否为估算值 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `productDatabaseList` |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/tool-jungle-scout/product-database/query \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "marketplace": "us",
    "includeKeywords": "yoga mat",
    "minSales": 300,
    "maxPrice": 50,
    "minRating": 4.0,
    "sort": "-sales",
    "needCount": 20
  }'
```
