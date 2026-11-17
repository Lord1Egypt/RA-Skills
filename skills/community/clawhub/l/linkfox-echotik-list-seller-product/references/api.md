# EchoTik-TikTok店铺商品列表 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/listSellerProduct`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sellerId | string | 是 | - | 店铺ID（TikTok Shop 小店ID）。最大长度 1000。从「EchoTik TikTok 店铺搜索」或「EchoTik TikTok 店铺详情」技能的返回结果获取 |
| sellerProductSortField | integer | 否 | 1 | 列表排序字段：1=总销量(total_sale_cnt)、2=总销售额(total_sale_gmv_amt)、3=SPU平均价格(spu_avg_price)、4=7天销量(total_sale_7d_cnt)、5=7天销售额(total_sale_gmv_7d_amt) |
| sortType | integer | 否 | 1 | 排序顺序：0=升序(asc)、1=降序(desc) |
| pageSize | integer | 否 | 50 | 每页条数。**须为10的倍数，最大100**；官方接口单页上限10，内部按10每页多次拉取后合并 |
| pageNum | integer | 否 | 1 | 分页页码，从1开始 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功（详见下方错误码） |
| errmsg | string | 业务状态描述 |
| total | integer | 记录数 |
| products | array | 店铺商品列表（详见下方商品字段） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 商品对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| productId | string | 商品唯一标识ID |
| asin | string | 产品ID（同 productId） |
| title / productName | string | 商品名称 |
| imageUrl | string | 商品图片URL |
| coverUrl | string | 封面图URL |
| productImageUrls | array | 商品图片URL列表 |
| price | number | 商品价格 |
| spuAvgPrice | number | SPU平均价格 |
| minPrice | number | 最低价格 |
| maxPrice | number | 最高价格 |
| currency | string | 货币 |
| totalSaleCnt | integer | 总销量 |
| totalSale1dCnt | integer | 1天内总销量(增量) |
| totalSale7dCnt | integer | 7天内总销量(增量) |
| totalSale15dCnt | integer | 15天内总销量(增量) |
| totalSale30dCnt | integer | 30天内总销量(增量) |
| totalSale60dCnt | integer | 60天内总销量(增量) |
| totalSale90dCnt | integer | 90天内总销量(增量) |
| monthlySalesUnits | integer | 月销量 |
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv1dAmt | number | 1天内总销售额(增量) |
| totalSaleGmv7dAmt | number | 7天内总销售额(增量) |
| totalSaleGmv15dAmt | number | 15天内总销售额(增量) |
| totalSaleGmv30dAmt | number | 30天内总销售额(增量) |
| totalSaleGmv60dAmt | number | 60天内总销售额(增量) |
| totalSaleGmv90dAmt | number | 90天内总销售额(增量) |
| productRating | number | 商品评分 |
| ratings | integer | 评论数 |
| reviewCount | integer | 评论数量 |
| productCommissionRate | number | 商品佣金比例（小数，如 0.05 表示 5%） |
| categoryName | string | 商品品类名称 |
| categoryIds | array | 商品品类ID列表 |
| salesFlagText | string | 带货方式 |
| salesTrendFlagText | string | 销售趋势标记 |
| firstCrawlDt | integer | 上架日期（yyyyMMdd 格式，如 20240504） |
| availableDate | string | 上架时间(时间戳/日期) |
| discount | string | 折扣信息 |
| offMarkText | string | 是否有优惠标记 |
| freeShippingText | string | 是否包邮 |
| isSShopText | string | 是否S店 |
| salePropsInfo | array | 销售属性信息（含 propId/propName/salePropValues[propValueId/propValue/image]） |
| region | string | 区域代码 |
| sourceTool | string | 来源工具 |
| sourceType | string | 商品来源 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errcode 字段区分（errcode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数校验错误 | 参数取值非法（如 `sellerId` 为空、`pageSize` 非10倍数）。参考 `errmsg` 获取具体字段与合法值集合 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和算力问题** 处理。|
| 402 | 算力不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和算力问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

### 基础店铺商品列表（按总销量降序）

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSellerProduct \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "sellerId": "7495514739648989419",
    "sellerProductSortField": 1,
    "sortType": 1,
    "pageSize": 20,
    "pageNum": 1
  }'
```

### 按7天销售额排序（近7天动销）

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSellerProduct \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "sellerId": "7495514739648989419",
    "sellerProductSortField": 5,
    "sortType": 1
  }'
```

### 按价格升序（店铺最低价商品）

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSellerProduct \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "sellerId": "7495514739648989419",
    "sellerProductSortField": 3,
    "sortType": 0
  }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-echotik-list-seller-product",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-echotik-list-seller-product`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
