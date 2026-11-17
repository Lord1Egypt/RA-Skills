---
name: linkfox-sorftime-amazon-product-detail
description: 基于Sorftime数据查询亚马逊ASIN详情，涵盖多站点历史销量、价格、BSR及利润趋势。
---

# Sorftime 商品详情（Amazon Product Detail）

本技能按 ASIN 查询亚马逊产品详情与历史趋势数据，帮助卖家分析产品表现、定价策略与竞争格局。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 按 ASIN 查询单个或多个（最多 10 个）亚马逊产品详情，覆盖 14 个站点。
- 提供历史趋势数据（可回溯至 2021 年）：BSR 排名、日/月销量、日/月销售额、售价、划线价、Deal 状态。
- 提供实时利润分析（含 FBA 费用明细）、销量、评分、卖家、变体、促销等结构化字段。

### ❌ 边界与限制

- **单次最多 10 个 ASIN**。
- **趋势计费**：默认返回近 15 天趋势；查询 > 15 天扣费加倍。
- **非结构化数据**：结果不支持通过 `_dataQuery_executeDynamicQuery` 二次分析。
- **销量预估**：非标类目（如 Amazon Renewed）商品销量字段可能返回 -1。
- **不在范围内**：跨类目/品牌/卖家的商品搜索与筛选（用 Sorftime Product Search）；ABA 搜索词排名（用 ABA Data Explorer）；广告/PPC 策略；评论内容分析；专利商标查询。

## 核心概念

Sorftime 商品详情按 ASIN 提供产品级数据，历史趋势可回溯至 2021 年，涵盖销量与销售额走势、价格与促销追踪、多级 BSR 排名历史，以及含 FBA 费用明细的实时利润分析。

**关键区分**：本工具返回单个产品的趋势/时序数据。若需跨类目、品牌或卖家搜索/筛选商品，请改用 Sorftime Product Search 技能。

**数据字段分类**（完整字段见 `references/api.md`）：

- **基础信息**：标题、品牌、ASIN、Listing 链接、图片（主图 + A+）、店铺名、五点描述、产品标志、下架状态、更新时间、重量、尺寸
- **变体**：父 ASIN、变体数、子 ASIN、变体属性
- **价格与利润**：售价、Coupon、平台佣金、FBA 费用（含明细）、FBM 运费、利润额与利润率
- **销量**：官方月销量（亚马逊公布）
- **排名**：BSR 排名、类目树、小类排名、上架时间、上架天数
- **评分**：评分、评分数、星级分布（1-5 星占比）
- **卖家**：Buybox 卖家名称/ID/国籍、FBA 状态、卖家数
- **Listing 特性**：A+ 内容、视频、品牌店、特性评分、产品信息、属性
- **促销**：品牌促销、Deal 类型、关联促销
- **趋势**（时序）：BSR 排名、小类 BSR 排名、日/月销量、日/月销售额、售价、划线价、Deal 状态

## 支持站点

US（美国）、GB（英国）、DE（德国）、FR（法国）、IN（印度）、CA（加拿大）、JP（日本）、ES（西班牙）、IT（意大利）、MX（墨西哥）、AE（阿联酋）、AU（澳大利亚）、BR（巴西）、SA（沙特）。

默认站点为 **US**，用户未指定时使用 `us`。

**注意**：Sorftime 使用小写代码（如 `us`、`gb`、`de`），英国代码为 `gb`（不是 `uk`）。

## 调用方式

- **API 端点**：`POST /sorftime/amazon/productDetail`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/sorftime_product_detail.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-sorftime-amazon-product-detail-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

关键参数为 `asin` 与 `marketplace`（均为必填），另可选趋势日期范围。

**查询构建原则**：
1. **始终指定站点**：使用小写站点代码，如 `us`、`de`、`jp`。
2. **谨慎选择是否含趋势**：默认含趋势（近 15 天）。仅需基础产品信息时设 `includeTrend: 2`，可节省成本并加快响应。
3. **历史分析指定日期范围**：需要超出默认 15 天的趋势时，使用 `queryTrendStartDate` 与 `queryTrendEndDate`（yyyy-MM-dd）。注意此操作扣费加倍。
4. **对比时批量传入 ASIN**：单次最多 10 个 ASIN，英文逗号隔开，用于竞品对比而非逐个调用。

**1. 快速查询（默认 15 天趋势）**
```
asin: B00FLYWNYQ, marketplace: us
```

**2. 长周期趋势分析（指定日期）**
```
asin: B00FLYWNYQ, marketplace: us
queryTrendStartDate: 2025-01-01, queryTrendEndDate: 2025-03-31
```

**3. 批量 ASIN 对比**
```
asin: B0088PUEPK,B00U26V4VQ,B0CVM8TXHP, marketplace: us
```

**4. 仅查产品信息，不含趋势**
```
asin: B0088PUEPK, marketplace: us, includeTrend: 2
```

**5. BSR 排名历史（德国站）**
```
asin: B00FLYWNYQ, marketplace: de
queryTrendStartDate: 2024-06-01, queryTrendEndDate: 2025-01-01
```

## 趋势数据解读

趋势数组采用交错格式：偶数下标为日期，奇数下标为对应值。

```
[20250101, 150, 20250102, 180, 20250103, 165, ...]
 ^date     ^val ^date     ^val ^date     ^val
```

- **销量/销售额趋势**：值 `-1` 表示"无法预估"（如类目变为 Amazon Renewed）。
- **价格趋势**：单位为当地货币最小单位（美元为美分）；`-1` 表示该日无可用价格。
- **BSR 排名趋势**：`bsrRankTrend` 格式为 `[{NodeId: xxx, Rank: [date, rank, ...]}]`，按小类返回。
- **Deal 趋势**：值 `1` 表示当日有 Deal，`0` 表示无 Deal。

## 展示规则

1. **只呈现数据**：以清晰表格展示查询结果，不做主观商业建议。
2. **排名说明**：展示排名数据时提醒用户，数值越小排名越靠前。
3. **价格单位**：趋势数据使用货币最小单位（美元为美分），展示时换算为标准货币。
4. **销量预估说明**：销量/销售额字段为 `-1` 表示"无法预估"，应向用户说明而非直接展示 -1。
5. **趋势可视化**：展示趋势数据时以可读表格呈现关键数据点，而非堆砌原始数组。
6. **下架处理**：`offSale` 为 true 时明确告知用户该产品当前不可售/已下架。
7. **错误处理**：查询失败时根据 `msg` 字段说明原因，并建议调整查询条件。

## 用户表达与场景速查

**适用** —— 按 ASIN 查询产品详情与趋势：

| 用户说 | 场景 |
|--------|------|
| "查一下这个ASIN的销量走势" | 销量趋势 |
| "这个产品最近价格变化如何" | 价格历史 |
| "帮我看看这个产品的利润空间" | 利润分析 |
| "这个ASIN的BSR排名趋势" | 排名历史 |
| "对比一下这几个ASIN的数据" | 多 ASIN 对比 |
| "这个产品的FBA费用是多少" | FBA 费用明细 |
| "产品上架多久了，评分怎么样" | 基础产品信息 |
| "这个产品还在售吗" | 下架状态核查 |
| "这个产品有没有Deal促销记录" | Deal 历史 |
| "看看这个产品的变体信息" | 变体详情 |

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

# Sorftime 产品详情(含趋势) API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/sorftime/amazon/productDetail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | 亚马逊标准识别号（ASIN），支持多个（最多10个），以英文逗号隔开。示例：`B0088PUEPK` 或 `B0088PUEPK,B00U26V4VQ` |
| marketplace | string | 是 | 亚马逊站点代码：us、gb、de、fr、in、ca、jp、es、it、mx、ae、au、br、sa |
| includeTrend | integer | 否 | 是否包含趋势数据。`1`：包含（默认）；`2`：不包含 |
| queryTrendStartDate | string | 否 | 趋势开始日期，格式 `yyyy-MM-dd`。默认仅返回近15天，查询天数>15天时扣费加倍 |
| queryTrendEndDate | string | 否 | 趋势截止日期，格式 `yyyy-MM-dd` |

## 响应结构

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| code | integer | 响应码（200表示成功） |
| msg | string | 响应消息 |
| total | integer | 结果总数 |
| costTime | integer | 耗时（ms） |
| costToken | integer | 消耗Token数量 |
| requestConsumed | integer | 消耗的请求数 |
| sourceType | string | 来源类型：sorftime |
| type | string | 渲染的样式 |
| columns | array | 渲染的列 |
| products | array | 产品详情列表（详见下方） |

### 商品对象字段（products 数组元素）

趋势数组均采用交错格式：偶数下标为日期（yyyyMMdd），奇数下标为对应值。

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | ASIN |
| title | string | 商品标题 |
| brand | string | 品牌 |
| asinUrl | string | 商品链接，亚马逊Listing详情页URL |
| imageUrl | string | 主图URL |
| productImageUrls | array | 主图列表（所有商品图片URL） |
| ebcPhoto | array | A+图片列表 |
| storeName | string | 店铺名称 |
| description | string | 五点描述 |
| productBadge | array | 产品标志，如Amazon Choice、Best Seller、New Release等 |
| lastUpdate | string | 更新时间，ASIN数据最近采集时间（格式yyyy-MM-dd） |
| offSale | boolean | 是否下架。true=不可售，false=可售 |
| productType | string | 分类，亚马逊产品类目节点名称 |
| weight | string | 重量，单位g |
| size | array | 尺寸，外包装[最长边,第二长边,最短边]，单位cm |
| parentAsin | string | 父ASIN，有子体时为父级ASIN，无子体时为null |
| variationNum | integer | 变体数 |
| variationASIN | array | 子体ASIN列表，无子体时为空 |
| attribute | array | 产品属性，有子体时表示子体属性。每项包含 asin（子体ASIN）、name（属性名）、value（属性值） |
| price | number | 销售价，扣除Coupon后的实际售价，单位为当地货币(如美元) |
| coupon | integer | Coupon政策。值>=0为抵扣金额(如500=$5)，值<0为折扣百分比(如-10=10%折扣) |
| platformFee | number | 平台佣金，单位为当地货币(如美元) |
| fbaFees | number | FBA费用，单位为当地货币(如美元) |
| fbaDetail | array | FBA明细。首项为配送费，后续为月份:仓储费，如[475,"1-9:5","10-12:15"] |
| shipCost | number | FBM配送费，单位为当地货币(如美元) |
| shipsFrom | string | 发货方 |
| profitAmount | number | 利润，到手价-FBA费-佣金，单位为当地货币(如美元) |
| profitRate | number | 利润率，例25.83表示25.83% |
| monthlySalesUnits | integer | 官方月销量，亚马逊公布的ASIN月销量，取近7个自然日最新值，无则为0 |
| salesRank | integer | BSR排名，大类排名 |
| category | array | 大类，[大类名称, NodeId] |
| bsrCategory | array | 小类排名列表，每项包含 nodeId（节点ID）、name（类目名称）、rank（排名）、date（日期，格式yyyyMMdd） |
| availableDate | string | 上架时间，格式yyyy-MM-dd |
| onlineDays | integer | 上架天数 |
| rating | number | 当前评分（0.0-5.0，如4.70） |
| ratings | integer | 评分数量 |
| fiveStarRatings | number | 5星占比，例57.7表示57.7% |
| fourStarRatings | number | 4星占比 |
| threeStarRatings | number | 3星占比 |
| twoStarRatings | number | 2星占比 |
| oneStarRatings | number | 1星占比 |
| buyboxSeller | string | Buybox卖家名称 |
| buyBoxSellerId | string | Buybox卖家ID |
| buyboxSellerAddress | string | 卖家所在地，Buybox卖家国籍(二字码如CN、US)，亚马逊自营时为null |
| isFBA | boolean | 是否FBA，Buybox卖家是否使用FBA物流 |
| sellerNum | integer | 卖家数 |
| aPlus | boolean | 有A+ |
| hasVideo | boolean | 有视频 |
| hasBrandStore | boolean | 有品牌店 |
| feature | object | 产品特性星级，亚马逊为此产品统计的特性及每个特性的星级，如{"Battery life":4.0} |
| productInfo | object | 产品信息，Listing中部Product Information结构化数据 |
| property | object | 属性列表，含变体属性及Bullet Points上方说明 |
| brandPromotion | string | 品牌促销 |
| dealType | string | Deal标签 |
| extraSavings | array | 关联促销，如[{Asin:xxx, Text:"Save 5%..."}] |
| rankTrend | array | BSR趋势，大类排名变化历史，交错格式[日期,排名,...] |
| bsrRankTrend | array | 小类排名趋势，JSON格式[{NodeId:xxx, Rank:[日期,排名,...]}] |
| listingSalesVolumeOfDailyTrend | array | 日销量趋势，值为-1表示无法预估 |
| listingSalesOfDailyTrend | array | 日销售额趋势，单位为当地货币最小单位(如美分)，值为-1表示无法预估 |
| listingSalesVolumeOfMonthTrend | array | 月销量趋势(近30日)，值为-1表示无法预估 |
| listingSalesOfMonthTrend | array | 月销售额趋势，单位为当地货币最小单位(如美分) |
| priceTrend | array | 售价趋势，未扣Coupon，单位为当地货币最小单位，-1表示该日无可用价格 |
| listPriceTrend | array | 原价趋势（划线价历史），单位为当地货币最小单位，-1表示该日无可用价格 |
| dealTrend | array | Deal趋势，值1=有Deal，0=无Deal |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 code 字段区分（code = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析 `products` 等业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `msg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productDetail \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B00FLYWNYQ", "marketplace": "us"}'
```

```bash
curl -X POST https://tool-gateway.linkfox.com/sorftime/amazon/productDetail \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asin": "B00FLYWNYQ", "marketplace": "us", "includeTrend": 1, "queryTrendStartDate": "2025-01-01", "queryTrendEndDate": "2025-03-01"}'
```
