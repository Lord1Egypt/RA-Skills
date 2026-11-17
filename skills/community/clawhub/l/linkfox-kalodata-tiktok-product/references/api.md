# Kalodata-TikTok商品搜索与详情 API 参考

## 调用规范

- **请求地址（商品榜单）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/product/rank`
- **请求地址（商品详情）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/product/detail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置，按 SKILL.md 的 **解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

### 商品榜单：`POST /kalodata/product/rank`

POST Body（JSON），所有参数均可选：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 否 | TikTok Shop 市场区域代码，例如 `US`。未指定时默认按服务端缺省（通常 US） |
| dateRange | string | 否 | 相对日期范围，例如 `last7Day`、`last30Day` |
| currency | string | 否 | 货币代码，例如 `USD` |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US` |
| category_ids | array<string> | 否 | 类目 ID 列表筛选 |
| shop_id | string | 否 | 店铺 ID 筛选 |
| creator_id | string | 否 | 达人 ID 筛选 |
| video_id | string | 否 | 返回指定视频关联的商品 |
| livestream_id | string | 否 | 返回指定直播关联的商品 |
| revenue_range | string | 否 | 成交金额 / GMV 范围，左闭右开 |
| is_affiliate | string | 否 | 是否联盟商品：`PUBLIC_PLAN`（是）或 `NON_AFFILIATE`（否） |
| commission_rate | number | 否 | 联盟商品佣金率，例如 `0.15` |
| is_tts_product | integer | 否 | 是否全托管商品：`1`（全托管）或 `0`（非全托管） |
| unit_price_range | string | 否 | 商品价格范围，左闭右开 |
| sortField | object | 否 | 排序规格对象，省略时使用默认排行 |
| pageNumber | integer | 否 | 页码，范围 1–5 |
| pageSize | integer | 否 | 每页条数，范围 5–100 |

> 该接口用于浏览商品榜单，不支持关键词搜索。`sortField` 的可用排序字段以网关实际接受的为准；若传入不支持的排序字段，按服务端 `errmsg` 处理，不要臆造字段名或尝试绕过逻辑。

### 商品详情：`POST /kalodata/product/detail`

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | string | 是 | TikTok 商品 ID，例如 `1729508370969629931`（字符串，避免大整数精度丢失），可从商品榜单响应的 `product_id` 获取 |
| region | string | 否 | 地区/市场编码，例如 `US` |
| dateRange | string | 否 | 时间范围，例如 `last7Day`（近7天）、`last30Day`（近30天） |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US` |
| currency | string | 否 | 货币单位，例如 `USD` |

> `productId` 为必填，缺失时网关返回业务错误。其余参数可选，省略时网关按默认处理。`region`/`dateRange`/`currency` 决定货币字段（`revenue`、`unit_price`、`min_price`、`max_price` 及渠道收入拆分）的口径与单位。本接口不支持按关键词/标题搜索商品；需先用榜单接口发现商品并获取 `product_id`，再用 `productId` 查询详情。

## 响应结构

### 共有顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功 |
| data | array | 榜单或详情数据 |
| costToken | integer | 本次调用扣费 token，通常为 14000 |
| errmsg | string | 状态消息，成功时为 `ok` |

> 顶层字段为 `errcode` / `data` / `costToken` / `errmsg`。**真实响应不返回 `total`**（也没有总页数等分页元数据），商品列表在 `data` 数组中。详情的 `data` 固定为 1 元素数组。

### 商品榜单字段（`data` 数组中的每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| product_id | string | 商品 ID（字符串格式，避免大整数精度丢失）；作为 `productId` 查询详情 |
| product_name | string | 商品标题 |
| unit_price | number | 单价（货币随 `region`，如 `US` 为 USD） |
| sales_volumn | integer | 销量（件数）。注意接口字段名为 `sales_volumn`（原样拼写，非 `volume`），用 `jq`/`ConvertFrom-Json` 取值时须用此名 |
| revenue | number | 总销售额（GMV），= `video_revenue` + `live_revenue` + `showcase_revenue` |
| video_revenue | number | 视频渠道销售额 |
| live_revenue | number | 直播渠道销售额 |
| showcase_revenue | number | 橱窗/展示渠道销售额 |
| revenue_growth_rate | number | 销售额增长率（百分比，如 `27.94` 表示 27.94%） |
| commission_rate | number | 佣金率（百分比，如 `25.0` 表示 25%；**非基点**） |
| launch_date | string | 上架日期（`YYYY-MM-DD`） |

> 真实响应不包含 `total`，也没有总页数等分页元数据。需要翻页时持续请求下一页，直到某页返回条数少于 `pageSize` 或达到第 5 页。

### 商品详情字段（`data` 固定为 1 元素数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| product_id | string | 商品唯一 ID（字符串，避免大整数精度丢失） |
| product_name | string | 商品名称 |
| product_region | string | 商品所在地区/市场（如 `us`） |
| product_shop_id | string | 所属店铺 ID |
| pri_cate_id | string | 一级类目 ID |
| sec_cate_id | string | 二级类目 ID |
| ter_cate_id | string | 三级类目 ID |
| unit_price | number | 件单价（按请求的 `currency` 货币） |
| min_price | number | 最低价（按请求的 `currency` 货币） |
| max_price | number | 最高价（按请求的 `currency` 货币） |
| revenue | number | 总销售额 / GMV（按请求的 `currency` 货币） |
| sales_volumn | integer | 销量（注意字段拼写为 `volumn`） |
| commission_rate | number | 佣金率，**直接百分比**（25.0 表示 25%） |
| product_review_count | integer | 商品评论数 |
| launch_date | string | 上架日期（`YYYY-MM-DD`） |
| delivery_type | string | 配送方式（如 `local`） |
| video_number | integer | 关联视频数 |
| video_revenue | number | 视频带来的销售额（按请求的 `currency` 货币） |
| live_number | integer | 关联直播数 |
| live_revenue | number | 直播带来的销售额（按请求的 `currency` 货币） |
| shopping_mall_revenue | number | 商城销售额（按请求的 `currency` 货币） |
| creator_number | integer | 关联达人数 |

> **收入渠道拆分**：详情 `revenue` = `video_revenue` + `live_revenue` + `shopping_mall_revenue`。
> **字段拼写注意**：`sales_volumn` 拼写为 `volumn`（非 `volume`），用 `jq` / `ConvertFrom-Json` 抽取时需使用准确字段名；`commission_rate` 为直接百分比（25.0 = 25%）。

## 真实响应示例

### 商品榜单

```json
{
  "errcode": 200,
  "data": [
    {
      "revenue_growth_rate": 27.94,
      "revenue": 620518.0,
      "video_revenue": 592599.0,
      "sales_volumn": 33872,
      "product_id": "1729508370969629931",
      "showcase_revenue": 311.0,
      "commission_rate": 15.0,
      "launch_date": "2026-03-18",
      "unit_price": 18.32,
      "product_name": "[NEW] [medicube] PDRN Pink Collagen Volume Multi Balm | All In One Volufiline, PDRN, NAD Stick for Youthful-Looking, Helping Look of Fine Lines, Firming Care, Anti-Aging Care | For Under-Eyes, Neck, Forehead, Smile Lines, Lip Care | Korean Skincare",
      "live_revenue": 27608.0
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

### 商品详情

```json
{
  "errcode": 200,
  "data": [
    {
      "sec_cate_id": "848776",
      "product_region": "us",
      "creator_number": 4164,
      "video_revenue": 592599.0,
      "sales_volumn": 33872,
      "video_number": 8271,
      "ter_cate_id": "601611",
      "unit_price": 18.32,
      "product_name": "[NEW] [medicube] PDRN Pink Collagen Volume Multi Balm | All In One Volufiline, PDRN, NAD Stick for Youthful-Looking, Helping Look of Fine Lines, Firming Care, Anti-Aging Care | For Under-Eyes, Neck, Forehead, Smile Lines, Lip Care | Korean Skincare",
      "revenue": 620518.0,
      "max_price": 19.0,
      "min_price": 19.0,
      "delivery_type": "local",
      "product_review_count": 42277,
      "product_id": "1729508370969629931",
      "pri_cate_id": "601450",
      "live_number": 2053,
      "commission_rate": 15.0,
      "launch_date": "2026-03-18",
      "shopping_mall_revenue": 311.0,
      "product_shop_id": "7495514739648989419",
      "live_revenue": 27608.0
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

> 上例中 `revenue` (620518.0) = `video_revenue` (592599.0) + `live_revenue` (27608.0) + `shopping_mall_revenue` (311.0)，渠道拆分自洽。脚本落盘的完整 JSON 包含全部字段，建议用 `jq` 或 `ConvertFrom-Json` 按需抽取。

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务成功与否通过响应体中的 `errcode` 字段区分（errcode = 200 表示成功，其他值表示业务错误）。未授权等情况可能返回 HTTP 401，且对应 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段。注意：合法但无数据的请求（如不支持的 `region`）可能返回 200 但响应中**不含 `data` 字段**（空结果），且仍会扣费 |
| 401 | 认证失败 | HTTP 401 或 authorized error；按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 402 | 算力不足 | HTTP 402：按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 501 | 上游调用失败 / 参数错误 | 两种形态：①`errmsg` 形如 `调用 Kalodata 接口失败: Kalodata API HTTP 5xx: `（如 522/554，上游 Kalodata 瞬时错误），用相同参数重试 1-2 次，不要改参数；持续失败联系网关侧确认 Kalodata 上游配置（如服务端 `KALODATA_SECRET_KEY` 是否配置）。②`errmsg` 形如参数校验错误（如 `page_number 范围为 1-5`、`productId` 缺失或非法），修正参数后重试 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例（认证失败）：

```json
{
  "errcode": 401,
  "errmsg": "authorized error"
}
```

上游瞬时错误示例（重试同参即可，不扣额外配置项）：

```json
{
  "errcode": 501,
  "errmsg": "调用 Kalodata 接口失败: Kalodata API HTTP 522: "
}
```

参数越界示例（校验在计费前，不扣费）：

```json
{
  "errcode": 501,
  "errmsg": "page_number 范围为 1-5，当前: 99"
}
```

## curl 示例

### 商品榜单

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/product/rank \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "dateRange": "last7Day",
    "pageSize": 20,
    "pageNumber": 1,
    "currency": "USD"
  }'
```

### 商品详情

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/product/detail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "productId": "1729508370969629931",
    "region": "US",
    "dateRange": "last7Day",
    "currency": "USD"
  }'
```

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-kalodata-tiktok-product",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-kalodata-tiktok-product`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
