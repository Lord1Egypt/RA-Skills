# FastMoss-TikTok热销榜单 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/fastmoss/productRankTopSelling`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 是 | 市场区域代码。可选值：US（美国）、GB（英国）、MX（墨西哥）、ES（西班牙）、DE（德国）、IT（意大利）、FR（法国）、ID（印度尼西亚）、VN（越南）、MY（马来西亚）、TH（泰国）、PH（菲律宾）、BR（巴西）、JP（日本）、SG（新加坡） |
| dateInfo | object | 是 | 日期规格对象，包含 `type` 和 `value` 两个字段 |
| dateInfo.type | string | 是 | 时间粒度：`day`（日）、`week`（周）、`month`（月） |
| dateInfo.value | string | 是 | 日期值：day 格式 `YYYY-MM-DD`，week 格式 `YYYY-周数`（如 `2025-18`），month 格式 `YYYY-MM` |
| category | string | 否 | 商品类目名称（英文），会匹配到 TikTok 类目 ID。非英文输入需先翻译为英文 |
| orderby | object | 否 | 排序规则对象，包含 `field` 和 `order` 两个字段 |
| orderby.field | string | 否 | 排序字段：`units_sold`（销量）、`gmv`（销售额）、`total_units_sold`（总销量）、`total_gmv`（总销售额）、`growth_rate`（增长率） |
| orderby.order | string | 否 | 排序方向：`desc`（降序）、`asc`（升序），默认 `desc` |
| page | integer | 否 | 页码，默认 `1` |
| pageSize | integer | 否 | 每页条数，最大 `10`，默认 `10` |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，`200` 表示成功 |
| errmsg | string | 业务状态说明 |
| page | integer | 当前页码 |
| pageSize | integer | 当前每页条数 |
| total | integer | 记录数 |
| products | array | 热销商品列表（见下方商品对象） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costTime | integer | 接口耗时（毫秒） |
| costToken | integer | 消耗 token；部分响应可能省略 |
| matchedCategoryIdPath | string | 匹配到的类目 ID 路径；传入 `category` 时可能返回 |
| matchedCategoryNamePath | string | 匹配到的类目名称路径；传入 `category` 时可能返回 |

### 商品对象

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 商品名称 |
| productId | string | 商品 ID |
| region | string | 区域代码 |
| price | number | 商品价格 |
| minPrice | number | 最低价格；仅价格区间商品返回 |
| maxPrice | number | 最高价格；仅价格区间商品返回 |
| currency | string | 货币符号或标识 |
| totalSaleCnt | integer | 总销量 |
| totalSale1dCnt | integer | 近1天销量（dateType=day 时返回） |
| totalSale7dCnt | integer | 近7天销量（dateType=week 时返回） |
| totalSale30dCnt | integer | 近30天销量（dateType=month 时返回） |
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv1dAmt | number | 近1天销售额（dateType=day 时返回） |
| totalSaleGmv7dAmt | number | 近7天销售额（dateType=week 时返回） |
| totalSaleGmv30dAmt | number | 近30天销售额（dateType=month 时返回） |
| growthRate | number | 增长率（百分比） |
| shopName | string | 店铺名称 |
| shopTotalUnitsSold | integer | 店铺总销量 |
| shopSellerId | string | 店铺卖家 ID |
| categoryName | string | 商品类目 |
| categoryIds | array | 商品类目 ID 路径（一级至三级） |
| productCommissionRate | number | 商品佣金比例（基点，1000=10%） |
| imageUrl | string | 商品图片 URL |
| coverUrl | array | 商品封面图 URL 列表 |
| shopAvatar | string | 店铺头像 URL |
| sourceTool | string | 来源工具标识 |
| sourceType | string | 商品来源类型 |
| offShelvesText | string | 是否下架（"是"=已下架，"否"=在售） |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 `errcode` 字段区分（`errcode = 200` 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
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

```bash
curl -X POST https://tool-gateway.linkfox.com/fastmoss/productRankTopSelling \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"region": "US", "dateInfo": {"type": "day", "value": "2026-04-15"}, "page": 1, "pageSize": 10}'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-fastmoss-top-selling",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
