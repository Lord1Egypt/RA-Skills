---
name: linkfox-jiimore-product-discovery
description: 基于转化率、点击量、FBA利润等指标，通过关键词在极目数据中发掘亚马逊的潜力爆品与高增长选品。
---

# Jiimore 商品发现（Jiimore Product Discovery）

本技能通过极目数据的关键词驱动商品发掘引擎，帮助亚马逊卖家基于转化率、点击增长与利润等指标发现潜力爆品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 基于关键词在亚马逊 US/JP/DE 站点发掘符合指定性能指标的商品。
- 支持按价格、评论数、评分、转化率、点击量与增长率、年销量、毛利率、FBA 费用、上架时间、细分市场数量、卖家国家等多维筛选与排序。
- 适用于发现新兴机会、验证产品思路与竞品对标。

### ❌ 边界与限制

- **关键词必填**：每次查询必须提供 `keyword`，不支持无关键词浏览。
- **关键词语言**：关键词须翻译为目标站点语言（US 用英文，JP 用日文，DE 用德文）。
- **站点限制**：当前仅支持 US、JP、DE，默认 US。
- **比率值为小数**：转化率与增长率须以 0-1 的小数传入（如 `0.1` 表示 10%）。
- **上架时间格式**：必须严格使用 `yyyyMMdd000000` 格式（如 `20250101000000`）。
- **分页上限**：单页最多 100 条。
- **不在范围内**：ABA 搜索词与关键词分析（用 ABA 工具）；广告/PPC 管理；评论与 Listing 优化；库存与供应链；含利润/定价策略的综合市场报告。

## 核心概念

极目商品发现是关键词驱动的亚马逊商品挖掘工具。给定搜索关键词，返回符合转化率、点击增长率、毛利率、价格、评论数、上架时长等指标的商品列表。

- **关键词必填**：每次查询须包含 `keyword`，并翻译为目标站点语言。
- **比率为小数**：转化率与增长率以 0-1 小数表示，`0.1` 即 10%。
- **站点支持**：当前支持 US（美国）、JP（日本）、DE（德国），默认 US。

## 调用方式

- **API 端点**：`POST /jiimore/productDiscovery`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/jiimore_product_discovery.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-jiimore-product-discovery-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 美国市场高转化无线充电器**
```json
{
  "keyword": "wireless charger",
  "countryCode": "US",
  "clickConversionRateMin": 0.1,
  "sortField": "clickConversionRate",
  "sortType": "desc"
}
```

**2. 发现快速增长的新品（近 6 个月上架、周点击增长 > 20%）**
```json
{
  "keyword": "desk lamp",
  "countryCode": "US",
  "launchDateMin": "20250901000000",
  "clickCountGrowthT7Min": 0.2,
  "sortField": "clickCountGrowthT7",
  "sortType": "desc"
}
```

**3. 低竞争高毛利的低价商品（评论数少）**
```json
{
  "keyword": "phone stand",
  "countryCode": "US",
  "priceMin": 10,
  "priceMax": 30,
  "totalReviewsMax": 100,
  "grossProfitMarginMin": 0.3,
  "sortField": "gpm",
  "sortType": "desc"
}
```

**4. 德国市场中国卖家的月点击强增长商品**
```json
{
  "keyword": "Handyhuelle",
  "countryCode": "DE",
  "sellerCountry": "CN",
  "clickCountGrowthT30Min": 0.15,
  "sortField": "clickCountGrowthT30",
  "sortType": "desc"
}
```

**5. 日本市场高评分且年销量强的商品**
```json
{
  "keyword": "ワイヤレスイヤホン",
  "countryCode": "JP",
  "customerRatingMin": 4.0,
  "salesVolumeT360Min": 1000,
  "sortField": "purchasedClicksT360",
  "sortType": "desc"
}
```

**6. 高综合转化且多细分市场的蓝海机会**
```json
{
  "keyword": "yoga mat",
  "countryCode": "US",
  "clickConversionRateCompositeMin": 0.15,
  "nicheCountMin": 3,
  "sortField": "clickConversionRateComposite",
  "sortType": "desc"
}
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示商品标题、ASIN、价格、评分、转化率、点击量与增长率。
2. **比率格式**：展示时将比率转为百分比（如 `0.12` 显示为 12%），并提醒用户 API 接受的是 0-1 小数。
3. **图片展示**：返回 `imageUrl` 时展示商品主图，便于直观识别。
4. **分页提示**：结果跨页时告知总数与当前页，并询问是否继续翻页。
5. **关键词翻译提醒**：提醒用户关键词须为目标站点语言（US 英文，JP 日文，DE 德文）。
6. **错误处理**：查询失败时根据响应说明原因，并建议调整查询条件。
7. **不做主观建议**：仅呈现客观商品数据，不做主观商业建议。

## 用户表达与场景速查

**适用** —— 商品发掘与挖掘任务：

| 用户说 | 场景 |
|--------|------|
| "找 XX 关键词的热门商品" | 关键词商品发现 |
| "高转化商品"、"爆款" | 高转化商品筛选 |
| "快速增长的商品"、"趋势品" | 点击增长发掘 |
| "高潜力的新品" | 新品 + 增长筛选 |
| "利润好的商品"、"赚钱的商品" | 毛利率筛选 |
| "低竞争商品"、"评论少" | 低评论机会挖掘 |
| "中国卖家的商品" | 卖家来源筛选 |
| "细分市场机会" | 细分市场数量发掘 |

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

# 极目-亚马逊-产品挖掘 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/jiimore/productDiscovery`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

### 必填参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 关键词（必填，并根据所选国家，翻译关键词为对应国家的语言） |

### 筛选参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| countryCode | string | 否 | 国家，使用国家简称。默认 `US`。可选值：`US`、`JP`、`DE` |
| priceMin | number | 否 | 最低商品价格 |
| priceMax | number | 否 | 最高商品价格 |
| totalReviewsMin | integer | 否 | 最低评论数 |
| totalReviewsMax | integer | 否 | 最高评论数 |
| customerRatingMin | number | 否 | 最低评分 |
| customerRatingMax | number | 否 | 最高评分 |
| clickConversionRateMin | number | 否 | 最低点击购买转化率，数值范围为0-1，0.1表示10% |
| clickConversionRateMax | number | 否 | 最高点击购买转化率，数值范围为0-1，0.1表示10% |
| clickConversionRateCompositeMin | number | 否 | 最低综合转化率，数值范围为0-1，0.1表示10% |
| clickConversionRateCompositeMax | number | 否 | 最高综合转化率，数值范围为0-1，0.1表示10% |
| clickCountT7Min | integer | 否 | 最低周点击量 |
| clickCountT7Max | integer | 否 | 最高周点击量 |
| clickCountT30Min | integer | 否 | 最低月点击量 |
| clickCountT30Max | integer | 否 | 最高月点击量 |
| clickCountGrowthT7Min | number | 否 | 最低周点击增长率，数值范围为0-1，0.1表示10% |
| clickCountGrowthT7Max | number | 否 | 最高周点击增长率，数值范围为0-1，0.1表示10% |
| clickCountGrowthT30Min | number | 否 | 最低月点击增长率，数值范围为0-1，0.1表示10% |
| clickCountGrowthT30Max | number | 否 | 最高月点击增长率，数值范围为0-1，0.1表示10% |
| salesVolumeT360Min | integer | 否 | 最低年销售量 |
| salesVolumeT360Max | integer | 否 | 最高年销售量 |
| grossProfitMarginMin | number | 否 | 最低毛利率 |
| grossProfitMarginMax | number | 否 | 最高毛利率 |
| fbaFeeMin | number | 否 | 最低FBA佣金 |
| fbaFeeMax | number | 否 | 最高FBA佣金 |
| launchDateMin | string | 否 | 最小上架时间，格式为：`yyyyMMdd000000` |
| launchDateMax | string | 否 | 最大上架时间，格式为：`yyyyMMdd000000` |
| nicheCountMin | integer | 否 | 最低细分市场数量 |
| nicheCountMax | integer | 否 | 最高细分市场数量 |
| sellerCountry | string | 否 | 卖家国家地区编码，选择多个的情况下用逗号隔开，如：`CN,US` |

### 排序与分页

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sortField | string | 否 | 排序字段。默认 `purchasedClicksT360`。可选值：`totalReviews`（总评论数）、`price`（价格）、`launchDate`（上架时间）、`clickCountT7`（7天点击量）、`clickCountT30`（30天点击量）、`clickCountT90`（90天点击量）、`clickConversionRate`（点击购买转化率）、`clickConversionRateComposite`（综合点击购买转化率）、`customerRating`（评分）、`purchasedClicksT360`（360天购买量）、`clickCountGrowthT7`（周点击增长率）、`clickCountGrowthT30`（月点击增长率）、`currentPrice`（当前价格）、`fbaFee`（FBA佣金）、`shippingFee`（FBA运费）、`gpm`（毛利率） |
| sortType | string | 否 | 排序方式。默认 `desc`。可选值：`desc`（降序）、`asc`（升序） |
| page | integer | 否 | 页码。默认 `1` |
| pageSize | integer | 否 | 每页数量（10-100）。默认 `50` |


## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 总数 |
| sourceTool | string | 工具类型：`jiimore` |
| sourceType | string | 来源类型：`amazon` |
| type | string | 渲染的样式 |
| title | string | 标题 |
| costToken | integer | 消耗token |
| columns | array | 渲染的列 |
| products | array | 产品列表（详见下方） |

### 产品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| asin | string | 亚马逊商品ASIN |
| parentAsin | string | 亚马逊商品父ASIN |
| title | string | 产品标题 |
| brand | string | 品牌 |
| price | number | 价格 |
| imageUrl | string | 产品主图 |
| productImageUrls | array | 产品图片链接列表 |
| asinUrl | string | ASIN链接 |
| ratings | integer | 评论数 |
| availableDate | string | 上架时间（时间戳） |
| availableDateString | string | 上架日期（字符串） |
| categoryNames | array | 类目信息 |
| marketplaceId | string | 站点ID |
| clickCountT7 | integer | 周点击量 |
| clickCountT30 | integer | 月点击量 |
| clickCountT90 | integer | 季度点击量 |
| clickConversionRate | number | 点击购买转化率 |
| clickConversionRateComposite | number | 综合转化率 |
| grossProfitMargin | number | 毛利率 |
| fbaFee | number | 亚马逊佣金 |
| shippingFee | number | FBA运费 |
| sourceTool | string | 工具类型：`jiimore` |
| sourceType | string | 来源类型：`amazon` |

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
curl -X POST https://tool-gateway.linkfox.com/jiimore/productDiscovery \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "wireless charger",
    "countryCode": "US",
    "clickConversionRateMin": 0.1,
    "priceMin": 10,
    "priceMax": 50,
    "sortField": "clickConversionRate",
    "sortType": "desc",
    "page": 1,
    "pageSize": 20
  }'
```
