# EchoTik-TikTok店铺列表 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/listSeller`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| region | string | 是 | - | 区域。可选值：US（美国）、ID（印度尼西亚）、TH（泰国）、PH（菲律宾）、MY（马来西亚）、VN（越南）、GB（英国）、MX（墨西哥）、SG（新加坡）、SA（沙特阿拉伯）、BR（巴西）、ES（西班牙）、JP（日本）、DE（德国）、IT（意大利）、FR（法国） |
| categoryId | string | 否 | - | 店铺一级分类ID。最大长度 1000 |
| categoryL2Id | string | 否 | - | 店铺二级分类ID。最大长度 1000 |
| categoryL3Id | string | 否 | - | 店铺三级分类ID。最大长度 1000 |
| minTotalSaleGmv30dAmt | number | 否 | - | 近30日GMV筛选（最小值） |
| maxTotalSaleGmv30dAmt | number | 否 | - | 近30日GMV筛选（最大值） |
| salesTrendFlag | integer | 否 | - | 近7日销售趋势：0=平稳、1=上升、2=下降 |
| fromFlag | integer | 否 | - | 店铺来源：1=本土店铺、2=跨境店铺 |
| salesFlag | integer | 否 | - | 主要带货方式：1=视频、2=直播 |
| minFirstCrawlDt | integer | 否 | - | 预估上架时间筛选（最小值），yyyyMMdd 格式（例如 20240101 代表 2024-01-01） |
| maxFirstCrawlDt | integer | 否 | - | 预估上架时间筛选（最大值），yyyyMMdd 格式 |
| sellerSortField | integer | 否 | 2 | 排序字段：1=总销量（total_sale_cnt）、2=总销售额（total_sale_gmv_amt）、3=店铺内商品SKU均价（spu_avg_price） |
| sortType | integer | 否 | 1 | 排序方式：0=升序（asc）、1=降序（desc） |
| pageNum | integer | 否 | 1 | 分页页码，从1开始 |
| pageSize | integer | 否 | 50 | 每页条数。**须为10的倍数，最大100**；官方接口单页上限10，内部按10每页多次拉取后合并 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功（详见下方错误码） |
| errmsg | string | 业务状态描述 |
| total | integer | 记录数 |
| sellers | array | 店铺列表（详见下方店铺字段） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 店铺对象字段

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
| salesFlagText | string | 主要带货方式 |
| salesTrendFlagText | string | 销售趋势 |
| shopIdentityLabel | string | 店铺标识 |
| shopTypeText | string | 是否品牌店铺 |
| fromFlagText | string | 跨境标识 |
| productCategoryList | string | 商品分类 |
| mostProductCategoryList | string | TOP1商品分类 |
| firstCrawlDt | integer | 预估上架时间 |
| userId | string | 达人UID |
| sourceTool | string | 来源工具 |
| sourceType | string | 商品来源 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errcode 字段区分（errcode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数校验错误 | 参数取值非法（如 `region` 不在支持列表）。参考 `errmsg` 获取具体字段与合法值集合 |
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

### 基础店铺列表（按总销售额降序）

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSeller \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "sellerSortField": 2,
    "sortType": 1,
    "pageSize": 20,
    "pageNum": 1
  }'
```

### 筛选跨境店铺 + 30日GMV + 上升趋势

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSeller \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "ID",
    "fromFlag": 2,
    "salesTrendFlag": 1,
    "minTotalSaleGmv30dAmt": 50000,
    "sellerSortField": 2,
    "sortType": 1,
    "pageSize": 20
  }'
```

### 直播带货 + 近期上架

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listSeller \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "GB",
    "salesFlag": 2,
    "minFirstCrawlDt": 20250101,
    "sellerSortField": 1,
    "sortType": 1
  }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-echotik-list-seller",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-echotik-list-seller`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
