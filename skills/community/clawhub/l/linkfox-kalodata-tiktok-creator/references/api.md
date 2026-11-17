# Kalodata-TikTok达人搜索与详情 API 参考

## 调用规范

- **请求地址（达人榜单）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/creator/rank`
- **请求地址（达人详情）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/creator/detail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置，按 SKILL.md 的 **解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

### 达人榜单：`POST /kalodata/creator/rank`

POST Body（JSON），所有参数均可选：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 否 | 地区/市场编码，例如 `US` |
| dateRange | string | 否 | 时间范围，例如 `last7Day`、`last30Day` |
| pageNumber | integer | 否 | 页码，取值 1-5 |
| pageSize | integer | 否 | 每页数量，取值 5-100 |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US` |
| currency | string | 否 | 货币单位，例如 `USD` |
| category_ids | array<integer> | 否 | 类目 ID 列表筛选 |
| shop_id | string | 否 | 店铺 ID 筛选 |
| revenue_range | string | 否 | 成交金额 / GMV 范围筛选 |
| creator_type | string | 否 | 达人类型筛选 |
| followers_range | string | 否 | 粉丝数范围筛选 |
| engagement_rate | string | 否 | 互动率筛选 |
| sortField | object | 否 | 排序条件；不排序时传空对象 `{}` 走默认榜单顺序 |

> 默认按 `revenue`（GMV）降序排列。可用排序字段以网关实际接受的为准；若传入不支持的排序字段，回退默认排序，不要尝试其它绕过逻辑。

### 达人详情：`POST /kalodata/creator/detail`

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| creatorId | string | 是 | 达人唯一 ID，例如 `7153432386608251946`，可从达人榜单响应的 `creator_id` 获取 |
| shop_id | string | 否 | 店铺 ID 筛选 |
| category_ids | array<integer> | 否 | 类目 ID 列表筛选 |
| region | string | 否 | 地区/市场编码，例如 `US` |
| dateRange | string | 否 | 时间范围，例如 `last7Day`、`last30Day` |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US` |
| currency | string | 否 | 货币单位，例如 `USD` |

> `creatorId` 为必填。本接口不支持按关键词/昵称搜索达人；需先用达人榜单接口发现达人并获取 `creator_id`，再用 `creatorId` 查询详情。

## 响应结构

### 共有顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功 |
| data | array | 榜单或详情数据 |
| costToken | integer | 本次调用扣费 token，通常为 14000 |
| errmsg | string | 状态消息，成功时为 `ok` |

### 达人榜单字段（`data` 数组中的每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| creator_nickname | string | 达人昵称 |
| creator_handle | string | TikTok 主页名，例如 `@based` |
| creator_id | string | 达人唯一 ID，字符串格式以避免大整数精度丢失 |
| creator_followers | string | 粉丝数，以字符串返回 |
| content_views | string | 内容总观看数，以字符串返回 |
| sales_volumn | integer | 销量，字段拼写为 `volumn` |
| revenue | number | 总销售额 / GMV，按请求的 `currency` 返回 |
| video_revenue | number | 短视频带货销售额 |
| live_revenue | number | 直播带货销售额 |
| revenue_growth_rate | number | 销售额增长率（%），可正可负 |

> `outputSchema` 可能声明 `total` 字段，但真实响应不包含 `total`，也没有总页数等分页元数据。需要翻页时持续请求下一页，直到某页返回条数少于 `pageSize`。

### 达人详情字段（`data` 固定为 1 元素数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| creator_id | string | 达人唯一 ID |
| creator_nickname | string | 达人昵称 |
| creator_handle | string | 达人 handle |
| creator_region | string | 达人地区 |
| creator_status | string | 达人状态 |
| creator_bio | string | 达人简介 |
| creator_belonged_shop_id | string | 所属店铺 ID |
| creator_followers | string | 粉丝总数，以字符串返回 |
| new_followers | integer | `dateRange` 窗口内新增粉丝 |
| revenue | number | 总销售额 / GMV |
| video_revenue | number | 视频销售额 |
| live_revenue | number | 直播销售额 |
| sales_volumn | integer | 销量，字段拼写为 `volumn` |
| unit_price | number | 件单价 |
| video_number | integer | 窗口内视频数 |
| video_views | integer | 视频总播放量 |
| video_gpm | number | 视频 GPM |
| live_number | integer | 窗口内直播数 |
| live_views | integer | 直播总观看量 |
| live_gpm | number | 直播 GPM |
| product_number | integer | 关联商品数 |
| shop_number | integer | 关联店铺数 |
| creator_contact_email | string | 联系邮箱 |
| creator_contact_ins | string | Instagram 联系方式 |
| creator_contact_whatsapp | string | WhatsApp 联系方式 |
| creator_contact_facebook | string | Facebook 联系方式 |
| creator_contact_tiktok | string | TikTok 联系方式 |
| creator_contact_zalo | string | Zalo 联系方式 |
| creator_contact_line | string | Line 联系方式 |

> `data` 对于有效 `creatorId` 通常为 1 元素数组。详情响应不包含 `total` 字段。

## 真实响应示例

### 达人榜单

```json
{
  "errcode": 200,
  "data": [
    {
      "revenue_growth_rate": 1.36,
      "revenue": 389817.79,
      "video_revenue": 238900.7,
      "sales_volumn": 14781,
      "content_views": "79192665",
      "creator_followers": "3700000",
      "creator_id": "7153432386608251946",
      "creator_handle": "@based",
      "creator_nickname": "BASED",
      "live_revenue": 150857.09
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

### 达人详情

```json
{
  "errcode": 200,
  "data": [
    {
      "creator_contact_line": "",
      "video_revenue": 238900.7,
      "sales_volumn": 14781,
      "video_number": 222,
      "creator_contact_email": "",
      "product_number": 51,
      "creator_bio": "based.com/tt",
      "revenue": 389817.79,
      "live_gpm": 29.32,
      "video_views": 74047861,
      "video_gpm": 3.23,
      "creator_handle": "@based",
      "creator_nickname": "BASED",
      "live_views": 5144804,
      "creator_followers": "3700000",
      "creator_region": "us",
      "unit_price": 26.37,
      "new_followers": 100000,
      "creator_belonged_shop_id": "7495079418085345590",
      "creator_status": "BELONGED_TO_SELLER",
      "creator_contact_tiktok": "based",
      "creator_id": "7153432386608251946",
      "shop_number": 1,
      "live_number": 2,
      "live_revenue": 150857.09
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
| 501 | 上游调用失败 / 参数无效 | 若 `errmsg` 包含 Kalodata HTTP 554，用相同参数重试 1-2 次；若因 `creatorId` 缺失或无效，核对 ID 是否来自榜单结果 |
| 其他非 200 值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
  "errcode": 401,
  "errmsg": "authorized error"
}
```

## curl 示例

### 达人榜单

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/creator/rank \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "dateRange": "last7Day",
    "pageSize": 10,
    "pageNumber": 1,
    "currency": "USD"
  }'
```

### 达人详情

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/creator/detail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "creatorId": "7153432386608251946",
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
  "skillName": "linkfox-kalodata-tiktok-creator",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-kalodata-tiktok-creator`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
