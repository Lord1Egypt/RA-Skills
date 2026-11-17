# EchoTik-TikTok店铺详情 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/sellerDetail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| sellerId | string | 是 | - | TikTok Shop 店铺ID。可从「EchoTik TikTok 店铺搜索」技能（`linkfox-echotik-list-seller`）的结果中获取，或使用已知店铺链接中的 ID。最大长度 1000 |

## 响应结构

成功时响应体为一个扁平对象：顶层携带业务状态字段与该店铺的全部详情字段（与店铺搜索返回的单个店铺对象同构），另含 `columns`、`type` 两个渲染元数据字段。**注意：本接口无 `total`、无 `sellers` 列表**，店铺字段直接位于顶层。

### 状态与渲染字段

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功（详见下方错误码） |
| errmsg | string | 业务状态描述 |
| costToken | integer | 消耗 token |
| columns | array | 渲染的列定义（展示元数据） |
| type | string | 渲染的样式（如 `tableListWorkbenches`） |

### 店铺详情字段

| 字段 | 类型 | 说明 |
|------|------|------|
| sellerId | string | 小店ID |
| sellerName | string | 小店名称 |
| sellerLink | string | 小店链接 |
| coverUrl | string | 店铺封面地址 |
| region | string | 地区 |
| categoryId | string | 一级分类ID |
| categoryL2Id | string | 二级分类ID |
| categoryL3Id | string | 三级分类ID |
| totalSaleCnt | integer | 总销量 |
| totalSale1dCnt | integer | 最近1天销量(增量) |
| totalSale7dCnt | integer | 最近7天销量(增量) |
| totalSale30dCnt | integer | 最近30天销量(增量) |
| totalSale90dCnt | integer | 最近90天销量(增量) |
| totalSaleGmvAmt | number | 总销售额 |
| totalSaleGmv1dAmt | number | 最近1天销售额(增量) |
| totalSaleGmv7dAmt | number | 最近7天销售额(增量) |
| totalSaleGmv30dAmt | number | 最近30天销售额(增量) |
| totalSaleGmv90dAmt | number | 最近90天销售额(增量) |
| followersCount | integer | 粉丝数 |
| rating | number | 评分 |
| reviewCount | integer | 评价数 |
| positiveFeedbackRate | number | 好评率 |
| responseRate | number | 回复率 |
| deliveryRate | integer | 送达率 |
| totalProductCnt | integer | 历史在店商品数(含下架) |
| totalCrawlProductCnt | integer | 在店商品数 |
| spuAvgPrice | number | 店铺内商品SKU均价 |
| minPrice | integer | 最低价格 |
| maxPrice | integer | 最高价格 |
| totalIflCnt | integer | 总带货达人数 |
| totalVideoCnt | integer | 总带货视频数 |
| totalLiveCnt | integer | 总直播数 |
| salesFlagText | string | 主要带货方式（视频带货 / 直播带货） |
| salesTrendFlagText | string | 销售趋势（上升 / 下降 / 平稳） |
| shopIdentityLabel | string | 店铺标识（如 OFFICIAL SHOP） |
| shopTypeText | string | 是否品牌店铺（是 / 否） |
| fromFlagText | string | 跨境标识（本土 / 跨境） |
| productCategoryList | string | 商品分类（JSON 字符串，含 category_name / category_id） |
| mostProductCategoryList | string | TOP1商品分类（JSON 字符串） |
| firstCrawlDt | integer | 预估上架时间，yyyyMMdd 格式（如 20240504 代表 2024-05-04） |
| userId | string | 达人UID |
| sourceType | string | 商品来源（如 Tiktok） |
| sourceTool | string | 来源工具（如 EchoTik-店铺详情） |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errcode 字段区分（errcode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数校验错误 | 参数取值非法（如 `sellerId` 为空或不存在）。参考 `errmsg` 获取具体原因 |
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

### 查询单个店铺详情

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/sellerDetail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "sellerId": "7495514739648989419"
  }'
```

### 结合店铺搜索使用

先用店铺搜索列出某区域的店铺，取其 `sellerId`，再调用本接口：

```bash
# 1) 列出美国 GMV 前列店铺（见 linkfox-echotik-list-seller）
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSeller \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{ "region": "US", "sellerSortField": 2, "sortType": 1, "pageSize": 10 }'

# 2) 用返回的 sellerId 查看该店铺完整详情
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/sellerDetail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{ "sellerId": "<上一步返回的 sellerId>" }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-echotik-seller-detail",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-echotik-seller-detail`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
