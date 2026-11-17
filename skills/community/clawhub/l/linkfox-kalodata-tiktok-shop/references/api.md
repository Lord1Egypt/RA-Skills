# Kalodata-TikTok店铺搜索与详情 API 参考

## 调用规范

- **请求地址（店铺榜单）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/shop/rank`
- **请求地址（店铺详情）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/shop/detail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置，按 SKILL.md 的 **解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

### 店铺榜单：`POST /kalodata/shop/rank`

POST Body（JSON），所有参数均可选：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 否 | 地区/市场编码，例如 `US`。最大长度 1000 |
| dateRange | string | 否 | 时间范围，例如 `last7Day`（近7天）、`last30Day`（近30天）。最大长度 1000 |
| pageNumber | integer | 否 | 页码，取值 1-5（超范围返回 `errcode 501`） |
| pageSize | integer | 否 | 每页数量，取值 5-100 |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US`。最大长度 1000 |
| currency | string | 否 | 货币单位，例如 `USD`。最大长度 1000 |
| category_ids | array<string> | 否 | 类目 ID 列表筛选；指定后返回对应类目下的成交金额 |
| revenue_range | string | 否 | 成交金额 / GMV 范围，左闭右开 |
| shop_type | string | 否 | 店铺类型：`BRAND`（品牌）或 `RETAILER`（零售商） |
| sortField | object | 否 | 排序条件；不排序时传空对象 `{}` 走默认榜单顺序 |

> 默认按 `revenue`（GMV）降序排列，每条记录带 `rank` 位次。可用排序字段以网关实际接受的为准；若传入不支持的排序字段，回退默认排序，不要尝试其它绕过逻辑。

### 店铺详情：`POST /kalodata/shop/detail`

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| shopId | string | 是 | TikTok 店铺唯一 ID（字符串，避免大整数精度丢失），例如 `7495514739648989419`。可从店铺榜单响应的 `shop_id` 字段获取 |
| category_id | string | 否 | 类目 ID，可进一步限定返回的类目维度 |
| region | string | 否 | 地区/市场编码，例如 `US`。最大长度 1000 |
| dateRange | string | 否 | 时间范围，例如 `last7Day`、`last30Day`。最大长度 1000 |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US`。最大长度 1000 |
| currency | string | 否 | 货币单位，例如 `USD`。最大长度 1000 |

> `shopId` 为必填，缺省时无法返回有效结果。本接口不支持按关键词/店铺名搜索；需先用店铺榜单接口发现店铺并获取 `shop_id`，再用 `shopId` 查询详情。本接口无分页，响应 `data` 固定为 1 个元素的数组（单店铺详情）。

## 响应结构

### 共有顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功 |
| data | array | 店铺榜单列表（rank）或 1 元素详情数组（detail） |
| costToken | integer | 本次调用扣费 token，固定 14000 |
| errmsg | string | 状态消息，成功时为 `ok` |

> ⚠️ `outputSchema` 可能声明 `total` 字段，但**真实响应不包含 `total`**，也没有总页数等分页元数据。需翻页时持续请求下一页，直到某页返回条数少于 `pageSize`。详情响应 `data` 恒为 1 个元素的数组。

> ⚠️ **详情字段名与店铺 RANK 接口不同**：详情用 `self_account_revenue`（RANK 用 `self_promotion_revenue`）、`shoppingmall_revenue`（`shopping` 与 `mall` 之间**无下划线**，RANK 用 `shopping_mall_revenue`）、`seller_type`（RANK 用 `shop_type`）。详情还返回 `creator_number`/`video_number`/`live_number`/`product_number`（RANK 不返回），且不返回 `rank`/`revenue_growth_rate`/`on_sell_product_count`。抽取数据时务必使用对应接口的确切字段名。

### 店铺榜单字段（`data` 数组中的每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| rank | integer | 排名位次（1 为最高） |
| shop_name | string | 店铺名称 |
| shop_id | string | 店铺唯一 ID（字符串，避免大整数精度丢失） |
| shop_type | string | 店铺类型（如 `BRAND`） |
| revenue | number | 总销售额 / GMV（按请求的 `currency` 货币） |
| sales_volumn | integer | 销量（注意字段拼写为 `volumn`） |
| on_sell_product_count | integer | 在售商品数 |
| unit_price | number | 件单价（按请求的 `currency` 货币） |
| revenue_growth_rate | number | 销售额增长率（%，可正可负） |
| self_promotion_revenue | number | 自营/自推广销售额 |
| affiliate_revenue | number | 达人分销销售额 |
| shopping_mall_revenue | number | 商城销售额 |

> **收入渠道拆分（榜单）**：`revenue` = `self_promotion_revenue` + `affiliate_revenue` + `shopping_mall_revenue`。

### 店铺详情字段（`data` 固定为 1 元素数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| shop_id | string | 店铺唯一 ID（字符串，避免大整数精度丢失） |
| shop_name | string | 店铺名称 |
| seller_type | string | 店铺/卖家类型（如 `BRAND`）——详情用 `seller_type`，非 `shop_type` |
| region | string | 地区/市场（如 `US`） |
| revenue | number | 总销售额 / GMV（按请求的 `currency` 货币） |
| sales_volumn | integer | 销量（注意字段拼写为 `volumn`） |
| product_number | integer | 在售商品数 |
| unit_price | number | 件单价（按请求的 `currency` 货币） |
| self_account_revenue | number | 自营/自播自推销售额——详情用 `self_account_revenue`，非 `self_promotion_revenue` |
| affiliate_revenue | number | 达人分销销售额 |
| shoppingmall_revenue | number | 商城销售额（注意：`shopping` 与 `mall` 之间**无下划线**） |
| creator_number | integer | 达人合作数 |
| video_number | integer | 关联视频数 |
| live_number | integer | 关联直播数 |

> **收入渠道拆分（详情）**：`revenue` ≈ `self_account_revenue` + `affiliate_revenue` + `shoppingmall_revenue`。各分项可能独立四舍五入（如 `shoppingmall_revenue` 在详情接口返回 `10431.0`，而榜单接口为 `10431.39`），故三者之和可能与 `revenue` 存在微小差异，不要当作精确恒等式。

## 真实响应示例

### 店铺榜单（`region=US, dateRange=last7Day, pageSize=5`，节选前 2 条）

```json
{
  "errcode": 200,
  "data": [
    {
      "shop_id": "7495514739648989419",
      "revenue_growth_rate": 16.98,
      "revenue": 4036424.77,
      "sales_volumn": 142080,
      "on_sell_product_count": 146,
      "self_promotion_revenue": 133774.9,
      "affiliate_revenue": 3892218.48,
      "shop_type": "BRAND",
      "rank": 1,
      "shop_name": "medicube US Store",
      "unit_price": 28.41,
      "shopping_mall_revenue": 10431.39
    },
    {
      "shop_id": "7495830785034323995",
      "revenue_growth_rate": -4.78,
      "revenue": 2487949.36,
      "sales_volumn": 88156,
      "on_sell_product_count": 147,
      "self_promotion_revenue": 92771.54,
      "affiliate_revenue": 2383899.26,
      "shop_type": "BRAND",
      "rank": 2,
      "shop_name": "Dr.Melaxin",
      "unit_price": 28.22,
      "shopping_mall_revenue": 11278.56
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

### 店铺详情（`shopId=7495514739648989419, region=US, dateRange=last7Day`）

```json
{
  "errcode": 200,
  "data": [
    {
      "self_account_revenue": 133774.9,
      "creator_number": 25367,
      "sales_volumn": 142080,
      "affiliate_revenue": 3892218.48,
      "video_number": 66199,
      "shop_name": "medicube US Store",
      "unit_price": 28.41,
      "shoppingmall_revenue": 10431.0,
      "product_number": 158,
      "shop_id": "7495514739648989419",
      "revenue": 4036424.77,
      "seller_type": "BRAND",
      "live_number": 8433,
      "region": "US"
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

> 脚本落盘的完整 JSON 包含全部字段，建议用 `jq` 或 `ConvertFrom-Json` 按需抽取。

## 错误码

正常情况下，接口 HTTP 状态码为 200，业务成功与否通过响应体中的 `errcode` 字段区分。未授权等情况可能返回 HTTP 401，且对应 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数缺失/非法 | 如详情缺 `shopId` 时返回 `errmsg: shopId 为必填参数`；按 `errmsg` 修正后重试 |
| 401 | 认证失败 | HTTP 401 或 authorized error；按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 402 | 算力不足 | 按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 501 | 上游调用失败 / 参数越界 | 两种形态：①`errmsg` 形如 `调用 Kalodata 接口失败: Kalodata API HTTP 554: `（上游 Kalodata 瞬时错误），用相同参数重试 1-2 次，不要改参数。②`errmsg` 形如 `page_number 范围为 1-5，当前: 999`（榜单参数越界），修正参数后重试 |
| 其他非 200 值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
  "errcode": 501,
  "errmsg": "page_number 范围为 1-5，当前: 999"
}
```

## curl 示例

### 店铺榜单

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/shop/rank \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "dateRange": "last7Day",
    "pageSize": 10,
    "pageNumber": 1
  }'
```

### 店铺详情

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/shop/detail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "shopId": "7495514739648989419",
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
  "skillName": "linkfox-kalodata-tiktok-shop",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-kalodata-tiktok-shop`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
