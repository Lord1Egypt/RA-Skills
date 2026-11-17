# Kalodata-TikTok视频搜索与详情 API 参考

## 调用规范

- **请求地址（视频榜单）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/video/rank`
- **请求地址（视频详情）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/video/detail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置，按 SKILL.md 的 **解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

### 视频榜单：`POST /kalodata/video/rank`

POST Body（JSON），所有参数均可选：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 否 | 地区/市场编码，例如 `US` |
| dateRange | string | 否 | 时间范围，例如 `last7Day`、`last30Day` |
| pageNumber | integer | 否 | 页码，取值 1-5 |
| pageSize | integer | 否 | 每页数量，取值 5-100 |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US` |
| currency | string | 否 | 货币单位，例如 `USD` |
| category_id | string | 否 | 类目 ID 筛选 |
| shop_id | string | 否 | 店铺 ID 筛选 |
| creator_id | string | 否 | 达人 ID 筛选 |
| product_id | string | 否 | 商品 ID 筛选 |
| revenue_range | string | 否 | GMV 范围；响应中的 `revenue` 即 GMV，例如 `1-100`、`>1000`、`<100` |
| followers_range | string | 否 | 达人粉丝数范围筛选 |
| ads_roas | number | 否 | 广告 ROAS 筛选 |
| sortField | object | 否 | GMV 排序条件，例如 `{"field":"revenue","type":"DESC"}` |

> 该接口用于浏览视频榜单，不支持关键词搜索。后端支持用 `revenue_range` 过滤 GMV。

### 视频详情：`POST /kalodata/video/detail`

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| videoId | string | 是 | TikTok 视频 ID，例如 `7659161409279806734`，可从视频榜单响应的 `video_id` 获取 |
| region | string | 否 | 地区/市场编码，例如 `US` |
| dateRange | string | 否 | 时间范围，例如 `last7Day`、`last30Day` |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US` |
| currency | string | 否 | 货币单位，例如 `USD` |

> `videoId` 为必填。本接口不支持按关键词/标题搜索视频；需先用视频榜单接口发现视频并获取 `video_id`，再用 `videoId` 查询详情。

## 响应结构

### 共有顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功 |
| data | array | 榜单或详情数据 |
| costToken | integer | 本次调用扣费 token，通常为 14000 |
| errmsg | string | 状态消息，成功时为 `ok` |

### 视频榜单字段（`data` 数组中的每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| video_id | string | 视频 ID，字符串格式以避免大整数精度丢失 |
| video_title | string | 视频标题 / 文案 |
| views | integer | 播放量 |
| digg_count | integer | 点赞数 |
| comment_count | integer | 评论数 |
| share_count | integer | 分享数 |
| revenue | number | 总销售额 / GMV，按请求的 `currency` 返回 |
| revenue_growth_rate | number | 销售额增长率（%），可正可负 |
| ad | integer | 是否广告/带货视频标识（1=是） |
| ad_view_ratio | number | 广告播放占比（%） |
| ad_revenue_ratio | number | 广告带来的销售额占比（%） |
| ads_roas | number | 广告 ROAS |
| belonged_creator_id | string | 所属达人 ID |
| belonged_creator_handle | string | 所属达人用户名 |
| creator_debut | string | 达人入驻日期（`YYYY-MM-DD`） |

> 真实响应不包含 `total`，也没有总页数等分页元数据。需要翻页时持续请求下一页，直到某页返回条数少于 `pageSize` 或达到第 5 页。

### 视频详情字段（`data` 固定为 1 元素数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| video_id | string | 视频 ID，字符串格式以避免大整数精度丢失 |
| video_title | string | 视频标题 / 文案 |
| video_region | string | 视频地区，可能为空字符串 |
| belonged_creator_id | string | 归属达人 ID |
| belonged_creator_handle | string | 归属达人用户名 |
| views | integer | 播放量 |
| digg_count | integer | 点赞数 |
| comment_count | integer | 评论数 |
| share_count | integer | 分享数 |
| revenue | number | 总销售额 / GMV |
| sales_volumn | integer | 销量，字段拼写为 `volumn` |
| video_gpm | number | 视频 GPM（每千次播放 GMV） |
| ad | integer | 是否投放广告（1=有广告，0=无广告） |
| ads_views | integer | 广告播放数 |
| ads_roas | number | 广告 ROAS |
| ad_cpa | number | 广告 CPA |
| ad_view_ratio | number | 广告播放占比（%） |
| ads_period | integer | 广告投放周期（天） |
| duration | number | 视频时长（秒） |
| product_number | integer | 视频关联商品数 |

> `data` 对于有效 `videoId` 通常为 1 元素数组。详情响应不包含 `total` 字段。

## 真实响应示例

### 视频榜单

```json
{
  "errcode": 200,
  "data": [
    {
      "video_id": "7659161409279806734",
      "video_title": "Ashley always getting me into trouble...",
      "views": 8935253,
      "digg_count": 183512,
      "comment_count": 2668,
      "share_count": 29847,
      "revenue": 180245.0,
      "revenue_growth_rate": 0,
      "ad": 1,
      "ad_view_ratio": 6.494768530896663,
      "ad_revenue_ratio": 0,
      "ads_roas": 4.24,
      "belonged_creator_id": "7565796510165943309",
      "belonged_creator_handle": "kimkrecs"
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

### 视频详情

```json
{
  "errcode": 200,
  "data": [
    {
      "comment_count": 2668,
      "video_region": "",
      "ads_views": 7901839,
      "ad": 1,
      "sales_volumn": 3835,
      "ad_cpa": 6.518341651222737,
      "ad_view_ratio": 6.494768530896663,
      "product_number": 1,
      "belonged_creator_id": "7565796510165943309",
      "ads_roas": 4.24,
      "share_count": 29847,
      "duration": 105.1,
      "belonged_creator_handle": "kimkrecs",
      "revenue": 180245.0,
      "video_title": "Ashley always getting me into trouble ...",
      "digg_count": 183512,
      "video_gpm": 20.17,
      "ads_period": 3,
      "views": 8935253,
      "video_id": "7659161409279806734"
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

## 错误码

正常情况下，接口 HTTP 状态码为 200，业务成功与否通过响应体中的 `errcode` 字段区分。未授权等情况可能返回 HTTP 401，且对应 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error；按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 402 | 算力不足 | 按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 501 | 上游调用失败 / 参数无效 | 若 `errmsg` 包含 Kalodata HTTP 554，用相同参数重试 1-2 次；若因 `videoId` 缺失或无效，核对 ID 是否来自榜单结果 |
| 其他非 200 值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
  "errcode": 401,
  "errmsg": "authorized error"
}
```

## curl 示例

### 视频榜单

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/video/rank \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "dateRange": "last7Day",
    "revenue_range": "1-100",
    "sortField": {
      "field": "revenue",
      "type": "DESC"
    },
    "pageSize": 10,
    "pageNumber": 1,
    "currency": "USD"
  }'
```

### 视频详情

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/video/detail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "videoId": "7659161409279806734",
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
  "skillName": "linkfox-kalodata-tiktok-video",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-kalodata-tiktok-video`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
