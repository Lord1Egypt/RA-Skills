# Shopee 商品详情 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/shopee/product/detail`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传请求头**：`SESSION_ID`、`MODE_ID`、`APP_NAME`（均从同名环境变量读取，未配置时为空字符串）
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| productUrl | string | 是 | - | Shopee HTTPS 商品链接；host 必须是支持的 8 个站点之一，端口须省略或为 443，路径须以 `-i.<数字shopId>.<数字itemId>` 结尾 |

支持的 host：`shopee.sg`、`shopee.co.id`、`shopee.com.my`、`shopee.ph`、`shopee.co.th`、`shopee.tw`、`shopee.vn`、`shopee.com.br`。

仅接受上表中的公共请求参数。工具内部固定使用 URL 自动识别模式，并根据 URL host 推导站点；搜索、分类、排序、抓取数量和延迟参数不对外开放。每次调用仅查询一个商品；若上游返回的有效商品数量不是 1，或返回 ID 与链接中的 shopId/itemId 不一致，接口返回业务错误。

最小请求：

```json
{
  "productUrl": "https://shopee.sg/%28LENECT-OFFICIAL-STORE%29-Flash-I-Aurora-Dual-Highlighter-7.2g-COCOMO-i.9641401.29691169956"
}
```

## 响应结构

成功响应为 LinkFox 统一包装：

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码；`200` 表示成功 |
| errmsg | string | 业务状态消息；成功时为 `ok` |
| data | array | Shopee 商品数组；成功时固定 1 条 |
| total | integer | 成功时固定为 `1` |
| costToken | integer | 消耗 token |
| type | string | 固定为 `tableListWorkbenches` |
| columns | array | 根据常用商品字段生成的渲染列 |

### 商品对象

常用字段：

| 分组 | 字段 |
|------|------|
| 标识 | `itemId`、`shopId`、`url`、`name`、`brand`、`categoryId`、`categoryBreadcrumb` |
| 图片视频 | `image`、`images`、`videos` |
| 价格 | `price`、`priceBeforeDiscount`、`priceMin`、`priceMax`、`discountPercent`、`currency` |
| 销售评价 | `sold`、`soldDisplayed`、`rating`、`ratingCount`、`ratingDistribution`、`likedCount` |
| 库存变体 | `stock`、`tierVariations`、`models` |
| 店铺 | `shopName`、`shopRating`、`shopLocation`、`isMall`、`isOfficialShop`、`isShopeeVerified` 及嵌套 `shop` 数据 |
| 内容 | `description`、`attributes`、类目、可售状态和商品条件等来源可用字段 |

来源新增或低频顶层字段会保留在商品对象根级。字段可能为 `null`；不同站点可能只返回标题、价格、主图、评分、销量和店铺等轻量字段。

示例（节选）：

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "data": [
    {
      "itemId": "29691169956",
      "shopId": "9641401",
      "url": "https://shopee.sg/%28LENECT-OFFICIAL-STORE%29-Flash-I-Aurora-Dual-Highlighter-7.2g-COCOMO-i.9641401.29691169956",
      "name": "Le'nect Aurora Dual Highlighter",
      "price": 36,
      "discountPercent": 23,
      "currency": "SGD",
      "rating": 5,
      "images": ["https://down-sg.img.susercontent.com/file/example"],
      "models": [
        {"name": "(BUY 1) AURORA HGLTR", "model_id": 281458233416}
      ],
      "shopName": "COCOMO Official Store",
      "shopLocation": "SG"
    }
  ],
  "total": 1,
  "costToken": 70000,
  "type": "tableListWorkbenches",
  "columns": [
    {"field": "itemId", "title": "商品 ID", "cellType": "text"}
  ]
}
```

## 错误码与边界

| 情况 | 表现 | 处理建议 |
|------|------|----------|
| 成功 | HTTP 200 且返回上述统一包装 | 按 `data` 解析 |
| productUrl 为空或格式非法 | 网关业务错误 | 传支持站点且路径含 `-i.<shopId>.<itemId>` 的 HTTPS 商品链接 |
| 商品无效、已移除或站点不匹配 | 网关业务错误 | 核对链接；不要自动换站点重复查询 |
| 上游 warning/error row 或缺少 itemId/shopId | 网关业务错误 | 视为无有效商品，不计入成功数据 |
| 上游商品 ID 与请求 URL 不一致 | 网关业务错误 | 不返回错误商品，核对链接后重试 |
| 上游返回多个有效商品 | 网关业务错误 | 视为上游结果异常；本接口不截断、不返回批量结果 |
| 401 | 鉴权失败 | 按 SKILL.md 的「解决认证和算力问题」处理 |
| 402 | 算力不足 | 按 SKILL.md 的「解决认证和算力问题」处理 |
| 超时或上游异常 | 连接错误、5xx 或业务错误 | 告知用户；不要连续自动重试产生额外费用 |

## curl 示例

```bash
API_KEY="${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}"
curl -X POST "${LINKFOX_TOOL_GATEWAY:-https://tool-gateway.linkfox.com}/shopee/product/detail" \
  -H "Authorization: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID:-}" \
  -H "MODE_ID: ${MODE_ID:-}" \
  -H "APP_NAME: ${APP_NAME:-}" \
  -d '{
    "productUrl": "https://shopee.sg/%28LENECT-OFFICIAL-STORE%29-Flash-I-Aurora-Dual-Highlighter-7.2g-COCOMO-i.9641401.29691169956"
  }'
```

---

## Feedback API

> 此端点与上方工具 API 分离，不要混用 Base URL。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**：`application/json`

```json
{
  "skillName": "linkfox-shopee-product-detail",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "The returned Shopee listing matched the requested product."
}
```

- `skillName`：固定使用本 Skill frontmatter 的 `name`
- `sentiment`：`POSITIVE`、`NEUTRAL`、`NEGATIVE` 三选一
- `category`：`BUG`、`COMPLAINT`、`SUGGESTION`、`OTHER` 四选一
- `content`：简述用户意图、实际表现以及问题或表扬原因
