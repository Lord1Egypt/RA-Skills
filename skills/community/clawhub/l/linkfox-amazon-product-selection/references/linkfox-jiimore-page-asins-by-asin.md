---
name: linkfox-jiimore-page-asins-by-asin
description: 根据亚马逊ASIN挖掘同细分市场（Niche）的竞品，支持按转化率、销量、价格和利润等多维度筛选潜力商品。
---

# Jiimore ASIN 细分市场（Page Asins By Asin）

本技能用于根据参考 ASIN 挖掘亚马逊同细分市场（Niche）的竞品列表，并提供点击转化率、销量、价格、毛利率等多维指标，帮助卖家发现潜力竞品与机会。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 给定参考 ASIN，挖掘与之同属细分市场的竞品 ASIN，返回带丰富指标的翻页列表。
- 覆盖美国（US）、日本（JP）、德国（DE）三个站点。
- 支持按价格、FBA 费用、毛利率、评论数、评分、点击量、点击转化率、综合转化率、销量、上架时间、细分市场数、卖家国家等多维筛选与排序。
- 提供商品 90 天趋势、Top3 细分市场、畅销榜排名等上下文信息。

### ❌ 边界与限制

- **支持站点**：仅支持 US、JP、DE，其他站点编码会被拒绝。
- **ASIN 必填**：每次查询必须提供参考 ASIN，否则无结果。
- **分页上限**：每页最多 100 条。
- **百分比值**：所有比率/份额参数取值范围为 0-1（非 0-100），构造筛选时需注意。
- **日期格式**：上架时间参数须使用 `yyyyMMdd000000` 格式。
- **不在范围内**：关键词级细分市场分析（用 Jiimore Niche Info by Keyword）；单个 ASIN 收益或利润预估；ABA 搜索词数据/关键词研究；广告投放与竞价管理；商品评论分析或 Listing 优化；供应商寻源或物流规划。

## 核心概念

给定参考 ASIN，工具会**挖掘与之同属细分市场的竞品 ASIN**，返回带丰富指标的翻页列表：点击转化率、综合转化率、点击量（7天/30天/90天）、销量、价格、FBA 费用、毛利率、评分以及 90 天趋势数据。数据仅覆盖 **US**、**JP**、**DE** 站点。

- **ASIN 必填**：每次查询必须包含参考 `asin`，工具据此查找同细分竞品并返回详细指标。
- **百分比字段**：部分参数使用 0-1 小数表示 0%-100%，展示时需换算为百分比（如 0.15 -> 15%）。
- **日期格式**：上架时间参数使用 `yyyyMMdd000000` 格式（如 `20240101000000` 表示 2024 年 1 月 1 日）。

## 调用方式

- **API 端点**：`POST /jiimore/pageAsinsByAsin`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/jiimore_page_asins_by_asin.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-jiimore-page-asins-by-asin-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 按参考 ASIN 基础竞品查询**
查询某参考 ASIN 在美国市场的竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "US",
  "sortField": "purchasedClicksT360",
  "sortType": "desc"
}
```

**2. 高转化竞品**
查找综合转化率高于 15% 的竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "US",
  "clickConversionRateCompositeMin": 0.15,
  "sortField": "clickConversionRateComposite",
  "sortType": "desc"
}
```

**3. 新品机会**
查找近 3 个月上架且点击增长快的竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "US",
  "launchDateMin": "20240101000000",
  "clickCountGrowthT7Min": 0.1,
  "sortField": "clickCountGrowthT7",
  "sortType": "desc"
}
```

**4. 价格区间筛选**
查找价格在 $20-$50 且毛利率较好的竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "US",
  "priceMin": 20,
  "priceMax": 50,
  "grossProfitMarginMin": 0.3,
  "sortField": "gpm",
  "sortType": "desc"
}
```

**5. 高点击低评论竞品（潜在弱点）**
查找月点击量超过 2000 但评论少于 100 的竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "US",
  "clickCountT30Min": 2000,
  "totalReviewsMax": 100,
  "sortField": "clickCountT30",
  "sortType": "desc"
}
```

**6. 日本市场竞品分析**
按评分查看日本市场的竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "JP",
  "sortField": "customerRating",
  "sortType": "desc"
}
```

**7. 同细分的中国卖家**
按卖家国家（中国）筛选高销量竞品：
```json
{
  "asin": "B0GC4RPX79",
  "countryCode": "US",
  "sellerCountry": "CN",
  "salesVolumeT360Min": 1000,
  "sortField": "purchasedClicksT360",
  "sortType": "desc"
}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示查询结果，将小数比率换算为百分比（如 0.25 -> 25%）。
2. **突出关键指标**：始终展示 ASIN、商品标题、价格、评分、综合点击转化率、点击量、评论数、毛利率等主列。
3. **展示细分上下文**：当 `niches` 字段存在时，展示 Top 细分市场标题与需求评分，说明该商品竞争所在的市场细分。
4. **趋势可视化**：当 `trends` 数据可用时，概括点击量、价格等关键指标的 90 天趋势方向（上升/下降/平稳）。
5. **分页提示**：当 `total` 超出当前页大小时，告知用户总数并建议是否翻页。
6. **错误处理**：查询失败时，根据响应消息说明原因，并建议调整筛选条件（如放宽区间或检查 ASIN）。
7. **不做主观建议**：客观呈现数据，不主动添加商业建议；仅当用户明确要求时才提供解读。

## 用户表达与场景速查

**适用** —— 基于参考 ASIN 发现同细分竞品：

| 用户说 | 场景 |
|--------|------|
| "查一下 ASIN B0GC4RPX79 的竞品" | 直接竞品查询 |
| "和这个 ASIN 竞争的商品有哪些" | 同细分竞品探索 |
| "看看同细分市场的相似商品" | 细分竞品发现 |
| "我的商品的高转化竞品" | 按转化率筛选竞品 |
| "我所在细分里的新品" | 新入场者识别 |
| "哪些中国卖家和这个 ASIN 竞争" | 按卖家来源筛选 |
| "找像我这样高点击低评论的商品" | 机会缺口分析 |
| "ASIN XX 的竞品价格分析" | 价格导向竞品分析 |

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

# 极目-亚马逊-产品挖掘（ASIN） API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/jiimore/pageAsinsByAsin`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| asin | string | 是 | 参考 ASIN，用于查询与该 ASIN 同属细分市场（Niche）的竞品列表，最大长度1000字符 |

### 站点与分页

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| countryCode | string | 否 | US | 国家编码，可选值：`US`（美国）、`JP`（日本）、`DE`（德国） |
| page | integer | 否 | 1 | 页码（从1开始） |
| pageSize | integer | 否 | 50 | 每页返回数量（10-100） |
| sortField | string | 否 | purchasedClicksT360 | 排序字段（见下方排序选项） |
| sortType | string | 否 | desc | 排序方式：`desc`（降序）或 `asc`（升序） |

### 筛选参数（均为可选）

**价格与FBA**：

| 参数 | 类型 | 说明 |
|------|------|------|
| priceMin | number | 最低产品价格 |
| priceMax | number | 最高产品价格 |
| fbaFeeMin | number | 最低FBA佣金 |
| fbaFeeMax | number | 最高FBA佣金 |
| grossProfitMarginMin | number | 最低毛利率 |
| grossProfitMarginMax | number | 最高毛利率 |

**评论与评分**：

| 参数 | 类型 | 说明 |
|------|------|------|
| totalReviewsMin | integer | 最少评论数量 |
| totalReviewsMax | integer | 最多评论数量 |
| customerRatingMin | number | 最低评分，取值范围 0.0-5.0 |
| customerRatingMax | number | 最高评分，取值范围 0.0-5.0 |

**点击数据（7天）**：

| 参数 | 类型 | 说明 |
|------|------|------|
| clickCountT7Min | integer | 最低周点击量 |
| clickCountT7Max | integer | 最高周点击量 |
| clickCountGrowthT7Min | number | 最低周点击增长率，取值范围 0-1，例如 0.1 表示 10% |
| clickCountGrowthT7Max | number | 最高周点击增长率，取值范围 0-1，例如 0.1 表示 10% |
| clickConversionRateMin | number | 最低点击转化率，取值范围 0-1，例如 0.1 表示 10% |
| clickConversionRateMax | number | 最高点击转化率，取值范围 0-1，例如 0.1 表示 10% |

**点击数据（30天）**：

| 参数 | 类型 | 说明 |
|------|------|------|
| clickCountT30Min | integer | 最低月点击量 |
| clickCountT30Max | integer | 最高月点击量 |
| clickCountGrowthT30Min | number | 最低月点击增长率，取值范围 0-1，例如 0.1 表示 10% |
| clickCountGrowthT30Max | number | 最高月点击增长率，取值范围 0-1，例如 0.1 表示 10% |

**综合转化率**：

| 参数 | 类型 | 说明 |
|------|------|------|
| clickConversionRateCompositeMin | number | 最低综合点击转化率，取值范围 0-1，例如 0.1 表示 10% |
| clickConversionRateCompositeMax | number | 最高综合点击转化率，取值范围 0-1，例如 0.1 表示 10% |

**销量与上架时间**：

| 参数 | 类型 | 说明 |
|------|------|------|
| salesVolumeT360Min | integer | 最低年销量 |
| salesVolumeT360Max | integer | 最高年销量 |
| launchDateMin | string | 最早上架时间，格式为 yyyyMMdd000000 |
| launchDateMax | string | 最晚上架时间，格式为 yyyyMMdd000000 |

**细分市场与卖家**：

| 参数 | 类型 | 说明 |
|------|------|------|
| nicheCountMin | integer | 最少细分市场数量 |
| nicheCountMax | integer | 最多细分市场数量 |
| sellerCountry | string | 卖家国家的国家码，选择多个国家的用英文逗号隔开，如：CN,US |

### 排序选项

| 值 | 说明 |
|------|------|
| purchasedClicksT360 | 360天购买点击（默认） |
| totalReviews | 评论数量 |
| price | 价格 |
| launchDate | 上架时间 |
| clickCountT30 | 30天点击量 |
| clickCountT90 | 90天点击量 |
| clickCountT7 | 7天点击量 |
| clickConversionRate | 点击转化率(原7天点击转化率) |
| clickConversionRateComposite | 综合点击转化率 |
| customerRating | 评分 |
| clickCountGrowthT7 | 周点击增长率 |
| clickCountGrowthT30 | 月点击增长率 |
| currentPrice | 当前价格 |
| fbaFee | FBA佣金 |
| shippingFee | FBA运费 |
| gpm | 毛利率 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总记录数 |
| pages | integer | 总页数 |
| page | integer | 当前页 |
| pageSize | integer | 每页大小 |
| data | array | ASIN 产品列表（见下方产品对象字段） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 产品对象字段（`data` 数组内）

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | 亚马逊产品ASIN |
| parentAsin | string | 亚马逊产品父ASIN |
| title | string | 产品标题 |
| brand | string | 品牌 |
| price | number | 价格 |
| currentPrice | number | 当前价格 |
| currency | string | 币种 |
| customerRating | number | 评分 |
| totalReviews | integer | 评论数 |
| launchDate | string | 上架时间 |
| link | string | ASIN链接 |
| imagesUrl | string | 产品主图 |
| sellerName | string | 卖家名称 |
| sellerId | string | 卖家ID |
| fbaFee | number | FBA佣金 |
| shippingFee | number | FBA运费 |
| gpm | number | 毛利率 |
| clickConversionRate | number | 点击转化率(原7天点击转化率) |
| clickConversionRateComposite | number | 综合点击转化率 |
| clickConversionRateType | string | 转化率计算类型 |
| clickConversionRateCompositeType | string | 综合转化率计算类型 |
| clickCountT7 | integer | 7天点击量 |
| clickCountT30 | integer | 30天点击量 |
| clickCountT90 | integer | 90天点击量 |
| clickCountGrowthT7 | number | 周点击增长率 |
| clickCountGrowthT30 | number | 月点击增长率 |
| purchasedClicksT360 | integer | 360天购买点击 |
| salesVolumeT360 | integer | 年销量 |
| nicheCount | integer | 所属细分市场数 |
| sameNicheTitle | string | 同细分市场（Niche）标题 |
| involvedNum | integer | 涉及的关键词数量 |
| involvedFrequency | integer | 涉及的关键词频次 |
| categoryNames | array | 类目信息 |
| hasMetric | boolean | 标识是否有指标 |
| searchValueType | string | 搜索类型: exact(精准匹配), sameNiche(与参考 ASIN 同属细分市场), category(类目) |
| niches | array | top3细分市场，包含: nicheId, nicheTitle, demand(市场评分), image, marketplaceId |
| bestSellersRanking | array | 畅销榜排名，包含: rank(排名), category(类目名称) |
| trends | array | 90天趋势数据，包含: day(日期), clickCountT7(周点击量), reviewCount(评论数), reviewRating(评分), bestSellerRanking(BSR排名), averagePriceT7(周平均价格), totalOfferDepthT7(7天新增offer) |
| lastUpdateTime | string | 最后更新时间 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 余额不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
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
curl -X POST https://tool-gateway.linkfox.com/jiimore/pageAsinsByAsin \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B0GC4RPX79",
    "countryCode": "US",
    "sortField": "purchasedClicksT360",
    "sortType": "desc",
    "page": 1,
    "pageSize": 50
  }'
```

### 带筛选条件的查询示例

```bash
curl -X POST https://tool-gateway.linkfox.com/jiimore/pageAsinsByAsin \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B0GC4RPX79",
    "countryCode": "US",
    "clickConversionRateCompositeMin": 0.15,
    "clickCountT30Min": 2000,
    "totalReviewsMax": 100,
    "sortField": "clickConversionRateComposite",
    "sortType": "desc",
    "page": 1,
    "pageSize": 50
  }'
```
