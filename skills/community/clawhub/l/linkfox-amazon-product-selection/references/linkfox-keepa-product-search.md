---
name: linkfox-keepa-product-search
description: 基于 Keepa 数据的亚马逊高级商品搜索与多维度多条件（如品类、价格、销量、BSR 排名等）选品筛选工具。
---

# Keepa 商品搜索（Keepa Product Search）

本技能基于 Keepa 数据提供亚马逊高级商品搜索与多维度筛选，帮助卖家按品类、价格、月销量、BSR 排名、评论数、评分、包装尺寸、重量、配送方式等条件发现目标商品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于 Keepa 商品数据库进行亚马逊多条件高级搜索，支持品类、价格区间、月销量、BSR 排名、关键词（正负向）、评论数、评分、包装尺寸、重量、配送方式、历史排名等多维筛选。
- 返回商品详细数据：价格、标题、图片、上架时间、材质、重量、最近 12 个月月销量等。
- 支持按销量、价格、评分、上架时间等字段排序，最多 3 条排序规则。

### ❌ 边界与限制

- **结果上限**：每页最多 100 条、最少 50 条。
- **排序上限**：单次查询最多 3 条排序规则。
- **类目上限**：每个类目筛选条件最多 50 个类目 ID 或名称。
- **关键词上限**：`keyword` 参数最多 50 个关键词、最大 1000 字符。
- **历史数据成本**：设置 `history=1` 会显著增大响应体积与 token 消耗。
- **价格单位**：所有价格均以最小货币单位表示（如美元以分为单位，`2599` 表示 `$25.99`），构建查询与展示结果时需换算。
- **不在范围内**：实时亚马逊搜索结果页模拟（用 Amazon Search）；搜索词搜索量与排名趋势分析（用 ABA 数据）；商品评论内容与情感分析；广告投放与竞价优化；Listing 优化与文案建议；库存与供应链数据。

## 核心概念

本工具基于 Keepa 数据提供亚马逊高级商品搜索，区别于简单的亚马逊店面搜索，支持多条件筛选：品类、价格区间、月销量、BSR（Best Sellers Rank）、关键词匹配（正负向）、评论数、评分、包装尺寸、重量、配送方式、历史销售排名等。返回商品详细数据，包括价格、标题、图片、上架时间、材质、重量、最近 12 个月月销量等。

**BSR（Best Sellers Rank）**：`salesRank` 值越小表示销售表现越好。排名 1 表示该类目下最畅销商品。用户说"热销商品"时，期望的是较小的 BSR 值。

**价格单位**：价格以最小货币单位表示（如美元以分为单位）。`$25.99` = `2599`。构建查询与展示结果时务必换算。

**类目名称**：`categoriesIncludeNames` 参数支持用冒号 `:` 或 `>` 字符分隔的多层级类目路径。需将用户输入自动转换为正确格式。

## 调用方式

- **API 端点**：`POST /keepa/productSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/keepa_product_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-keepa-product-search-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

根据用户意图构建请求参数：

1. **确定站点**：将用户目标国家映射为正确的 `domain` ID（默认 `1` 即美国站）。
2. **设置关键词筛选**：用 `keyword` 进行基于标题的筛选，支持正负向词。
3. **设置类目范围**：用 `categoriesIncludeNames` 或 `rootCategoryNames` 按类目限定，将用户输入转换为正确的类目路径格式。
4. **应用数值筛选**：将销量、价格、BSR、评论、评分等需求映射到对应的 Gte/Lte 参数。
5. **设置排序**：若用户要求按销量、价格或评分排序，配置 `sort` 数组。
6. **启用历史数据**：若用户需要月销量趋势或价格历史，将 `history` 设为 `1`。

**1. 美国站月销量超 1000 的电子产品**
```json
{"domain": "1", "rootCategoryNames": ["Electronics"], "monthlySoldGte": 1000}
```

**2. 价格区间内高评分商品**
```json
{"domain": "1", "currentBuyBoxShippingGte": 1500, "currentBuyBoxShippingLte": 5000, "currentRatingGte": 4.0, "keyword": "wireless charger"}
```

**3. 近 6 个月上架且评论数少的新品**
```json
{"domain": "1", "availableDateGte": "2025-10-01", "currentCountReviewsLte": 50, "monthlySoldGte": 500}
```

**4. BSR 排名筛选用于竞品分析**
```json
{"domain": "1", "categoriesIncludeNames": ["Home & Kitchen"], "currentSalesLte": 5000, "sort": [{"fieldName": "monthlySold", "sortDirection": "desc"}]}
```

**5. 非 Amazon 自营但 FBA 配送且销量好的商品**
```json
{"domain": "1", "buyBoxIsAmazon": false, "buyBoxIsFBA": true, "monthlySoldGte": 300, "currentRatingGte": 4.0}
```

**6. 轻小便于运输的商品**
```json
{"domain": "1", "packageWeightLte": 500, "packageLengthLte": 200, "packageWidthLte": 150, "packageHeightLte": 100, "monthlySoldGte": 200}
```

**7. 日本站带历史数据的搜索**
```json
{"domain": "5", "keyword": "USB charger", "history": 1, "monthlySoldGte": 100}
```

**8. 指定品牌并排除危险品**
```json
{"domain": "1", "brand": ["Anker", "UGREEN"], "isHazMat": false, "sort": [{"fieldName": "monthlySold", "sortDirection": "desc"}]}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示关键字段：ASIN、标题、价格、BSR、月销量、评分、评论数、品牌。
2. **价格换算**：将价格从最小货币单位换算为标准格式（如 `2599` → `$25.99`）。
3. **BSR 说明**：展示 BSR 数据时提醒用户，数值越小表示销售排名越好。
4. **月销量历史**：包含历史数据时，清晰呈现 12 个月销量趋势。
5. **分页提示**：告知总结果数，必要时建议获取后续页。
6. **图片链接**：若有图片 URL，提及但不尝试内联渲染，除非用户要求。
7. **错误处理**：查询失败时说明原因，并建议调整筛选条件。

## 用户表达与场景速查

**适用** —— 多条件亚马逊商品搜索与筛选：

| 用户说 | 场景 |
|--------|------|
| "找月销量超 X 的商品" | 销量筛选 |
| "在 XX 类目里搜商品" | 按类目发现商品 |
| "BSR 低于 X 的商品" | 销售排名筛选 |
| "近 N 个月上架的新品" | 新品发现 |
| "价格在 $X 到 $Y 之间的商品" | 价格区间筛选 |
| "评分好的 FBA 商品" | 配送 + 评分筛选 |
| "X 克以下的轻量商品" | 包装尺寸筛选 |
| "XX 品牌的商品" | 指定品牌搜索 |
| "看 XX 的历史销量数据" | 历史销量分析 |
| "高级选品"、"商品筛选" | 多条件选品调研 |
| "小众商品挖掘"、"找低竞争商品" | 竞争空白分析 |
| "BSR 趋势"、"销售排名历史" | 历史排名筛选 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# Keepa-亚马逊-商品搜索 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/keepa/productSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| domain | string | 是 | Amazon域名ID：1=美国, 2=英国, 3=德国, 4=法国, 5=日本, 6=加拿大, 8=意大利, 9=西班牙, 10=印度, 11=墨西哥 |
| keyword | string | 否 | 标题关键词（大小写不敏感；空格表示分词AND；关键词本身包含空格时用双引号包裹；支持前缀-排除；如果含有 & 符号会被替换为空格；最多50个关键词，最大1000字符） |
| rootCategory | array[int] | 否 | 根类目ID（最多50），仅包含列在这些根类别中的产品 |
| rootCategoryNames | array[string] | 否 | 根类目名称（最多50），当rootCategory为空时使用，系统会自动查找对应的类目ID |
| categoriesInclude | array[int] | 否 | 仅包含的子类目ID（最多50），仅包含直接列在这些子类别中的产品 |
| categoriesIncludeNames | array[string] | 否 | 包含的子类目名称（最多50），当categoriesInclude为空时使用，系统会自动查找对应的类目ID。支持传入完整类目路径（用 `:` 或 `›` 分隔），结果更准确 |
| categoriesExclude | array[int] | 否 | 排除的子类目ID（最多50） |
| categoriesExcludeNames | array[string] | 否 | 排除的子类目名称（最多50），当categoriesExclude为空时使用，系统会自动查找对应的类目ID。支持传入完整类目路径（用 `:` 或 `›` 分隔），结果更准确 |
| currentSalesGte / currentSalesLte | integer | 否 | 当前销售排名范围（数值越小排名越好） |
| avg90SalesGte / avg90SalesLte | integer | 否 | 90天平均销售排名范围 |
| deltaPercent90SalesGte / deltaPercent90SalesLte | integer | 否 | 90天销售排名变化百分比范围 |
| monthlySoldGte / monthlySoldLte | integer | 否 | 销量/月销量范围 |
| srAvgGte / srAvgLte | integer | 否 | 历史销售排名范围（正整数，数值越小排名越好，用于srAvgMonth指定月份） |
| srAvgMonth | string | 否 | 历史销售排名-选择月份（格式：YYYYMM，如202511表示2025年11月，最近36个月内） |
| currentNewGte / currentNewLte | integer | 否 | 当前新品价格范围（最小货币单位） |
| currentBuyBoxShippingGte / currentBuyBoxShippingLte | integer | 否 | 当前购买按钮含运费价格范围（最小货币单位） |
| currentCountReviewsGte / currentCountReviewsLte | integer | 否 | 当前评论数量范围 |
| currentRatingGte / currentRatingLte | number | 否 | 当前评分范围（0.0-5.0） |
| packageLengthGte / packageLengthLte | integer | 否 | 包装长度范围（毫米） |
| packageWidthGte / packageWidthLte | integer | 否 | 包装宽度范围（毫米） |
| packageHeightGte / packageHeightLte | integer | 否 | 包装高度范围（毫米） |
| packageWeightGte / packageWeightLte | integer | 否 | 包装重量范围（克） |
| brand | array[string] | 否 | 品牌（OR匹配） |
| color | array[string] | 否 | 颜色（OR匹配），筛选指定颜色的产品 |
| size | array[string] | 否 | 尺码（OR匹配），筛选指定尺码的产品 |
| availableDateGte / availableDateLte | string | 否 | 产品上架时间范围（日期格式：yyyy-MM-dd） |
| buyBoxIsAmazon | boolean | 否 | 购买按钮卖家是否为亚马逊 |
| buyBoxIsFBA | boolean | 否 | 购买按钮是否为FBA |
| isHazMat | boolean | 否 | 是否为危险品 |
| variationCountGte / variationCountLte | integer | 否 | 变体数量范围 |
| currentCountNewGte / currentCountNewLte | integer | 否 | 当前新品报价数量范围 |
| outOfStockPercentage90Gte / outOfStockPercentage90Lte | integer | 否 | 90天缺货百分比范围 |
| singleVariation | boolean | 否 | 仅返回一个变体，当设为true时，多变体产品只返回一个变体 |
| productType | array[int] | 否 | 产品类型筛选（默认[0,1,2]）：0=标准产品, 1=可下载产品, 2=电子书, 5=变体父ASIN |
| history | integer | 否 | 返回值是否包含历史数据/历史销量（1=获取, 0=不获取，默认0） |
| rating | integer | 否 | 是否获取评分信息（1=获取, 0=不获取，默认1） |
| page | integer | 否 | 页码（从1开始，默认1） |
| perPage | integer | 否 | 每页返回的最大结果数（最小50，最大100，默认50） |
| sort | array[object] | 否 | 排序（最多3）：对象数组，每项包含 `{"fieldName": "...", "sortDirection": "asc\|desc"}`。可排序字段：availableDate(上架时间)、currentSales(当前销售排名)、monthlySold(销量/月销量)、currentRating(当前评分)、currentCountReviews(当前评论数)、currentBuyBoxShipping(当前购买按钮含运费价格)、currentNew(当前新品价格) |

- 请求参数 `categoriesIncludeNames` 类目名称支持多层级，层级之间用英文冒号 `:` 或 `›` 分隔，需根据用户输入自动转换

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总行数 |
| perPage | integer | 每页数量 |
| currentPage | integer | 当前页码 |
| totalCount | integer | 总数量 |
| sourceType | string | 来源类型：keepa |
| type | string | 渲染的样式 |
| columns | array | 渲染的列 |
| costToken | integer | 消耗token |
| products | array | 商品列表（详见下方） |

### 商品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| title | string | 商品标题 |
| brand | string | 品牌 |
| manufacturer | string | 制造商 |
| model | string | 型号 |
| price | number | 当前价格（单位：元，如美元/欧元等） |
| primePrice | number | Prime价格 |
| currency | string | 币种 |
| salesRank | integer | 销售排名 |
| salesRank30 | integer | 近30天平均销售排名 |
| salesRank90 | integer | 近90天平均销售排名 |
| salesRank180 | integer | 近180天平均销售排名 |
| monthlySalesUnits | integer | 月销量 |
| monthlySalesRevenue | number | 月销售额 |
| monthlySalesUnits1MonthAgo .. monthlySalesUnits12MonthsAgo | integer | 最近12个月每月的月销量 |
| rating | number | 当前评分（0.0-5.0） |
| ratings | integer | 评分数量 |
| reviewCount | integer | 评论数量 |
| availableDate | string | 上架时间（yyyy-MM-dd HH:mm:ss） |
| lastUpdate | string | 最后更新时间（yyyy-MM-dd HH:mm:ss） |
| imageUrl | string | 图片URL（请求地址） |
| productImageUrls | array | 商品图片列表 |
| asinUrl | string | 亚马逊ASIN的详情网址 |
| categoryTree | string | 类目树 |
| categoryTreeId | string | 类目树ID |
| rootCategory | integer | 根类目ID |
| subcategories | array | 子类目列表，包含 code(类目ID)、rank(排名)、label(类目名称) |
| fulfillment | string | 配送方式（AMZ, FBA, FBM） |
| buyBoxSellerId | string | 购买按钮卖家ID |
| sellerNum | integer | 卖家数 |
| parentAsin | string | 父ASIN |
| variationNum | integer | 变体数量 |
| color | string | 颜色 |
| dimension | string | 尺寸 |
| dimensionsType | string | 尺寸类型 |
| material | string | 产品的材质，指其构造中使用的主要材料 |
| weight | string | 重量（克） |
| packageWeight | string | 包装重量（克） |
| packageLength | integer | 包装长度（毫米） |
| packageWidth | integer | 包装宽度（毫米） |
| packageHeight | integer | 包装高度（毫米） |
| packageDimensions | string | 包装尺寸 |
| packageQuantity | integer | 包装中商品的数量，不可用时为0或-1 |
| itemLength | integer | 商品长度（毫米），不可用时为0或-1 |
| itemWidth | integer | 商品宽度（毫米），不可用时为0或-1 |
| itemHeight | integer | 商品高度（毫米），不可用时为0或-1 |
| isAdultProduct | boolean | 是否为成人产品 |
| isHazmat | boolean | 是否为危险品 |
| referralFeePercentage | number | 推荐费百分比 |
| fbaFees | number | FBA配送费（单位：元） |
| profit | number | 利润率（百分比，如25.5表示25.5%） |
| urlSlug | string | URL Slug |
| sourceType | string | 来源类型：keepa |
| sourceTool | string | 来源工具 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | - | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
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
curl -X POST https://tool-gateway.linkfox.com/keepa/productSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain": "1", "keyword": "wireless charger", "monthlySoldGte": 500, "currentRatingGte": 4.0}'
```
