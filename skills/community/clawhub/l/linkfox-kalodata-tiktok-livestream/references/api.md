# Kalodata-TikTok直播搜索与详情 API 参考

## 调用规范

- **请求地址（直播榜单）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/livestream/rank`
- **请求地址（直播详情）**：`${LINKFOX_TOOL_GATEWAY}/kalodata/livestream/detail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置，按 SKILL.md 的 **解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

### 直播榜单：`POST /kalodata/livestream/rank`

POST Body（JSON），所有参数均可选：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 否 | 地区/市场编码，例如 `US`。最大长度 1000 |
| dateRange | string | 否 | 时间范围，例如 `last7Day`（近7天）、`last30Day`（近30天）。最大长度 1000 |
| pageNumber | integer | 否 | 页码，取值 1–5（超范围返回 `errcode 501`） |
| pageSize | integer | 否 | 每页数量，取值 5–100 |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US`。最大长度 1000 |
| currency | string | 否 | 货币单位，例如 `USD`。最大长度 1000 |
| category_id | string | 否 | 类目 ID 筛选 |
| shop_id | string | 否 | 店铺 ID 筛选 |
| creator_id | string | 否 | 达人 ID 筛选 |
| product_id | string | 否 | 商品 ID 筛选 |
| followers_range | string | 否 | 达人粉丝数范围筛选 |
| sortField | object | 否 | 排序条件，结构由网关定义；不排序时传空对象 `{}` 走默认榜单顺序 |

> 该接口用于浏览直播榜单，不支持关键词搜索。`sortField` 在 `inputSchema` 中声明为对象（`properties` 为空）；默认按 `revenue`（GMV）降序排列，传入空对象 `{}` 走默认排序。可用的排序字段以网关实际接受的为准；若传入不被支持的排序字段，网关会返回业务错误，此时应回退为默认排序，不要尝试其它绕过逻辑。

### 直播详情：`POST /kalodata/livestream/detail`

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| livestreamId | string | 是 | 目标直播的唯一 ID（camelCase），例如 `7661409374878878494`。通常来自直播榜单接口的 `livestream_id`。最大长度 1000 |
| region | string | 否 | 地区/市场编码，例如 `US`。最大长度 1000 |
| dateRange | string | 否 | 时间范围，例如 `last7Day`（近7天）、`last30Day`（近30天）。最大长度 1000 |
| language | string | 否 | 返回语言，例如 `zh-CN`、`en-US`。最大长度 1000 |
| currency | string | 否 | 货币单位，例如 `USD`。最大长度 1000 |

> `livestreamId` 为必填，其余参数可选；不传时网关按默认值处理。本接口为单实体详情接口，不支持按关键词/标题搜索直播，也无 `pageNumber`/`pageSize`/`sortField` 等分页或排序参数；需先用直播榜单接口发现直播并获取 `livestream_id`，再用 `livestreamId` 查询详情。

## 响应结构

### 共有顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功 |
| data | array | 直播榜单列表或直播详情数据 |
| costToken | integer | 本次调用扣费 token，固定 14000 |
| errmsg | string | 状态消息，成功时为 `ok` |

> ⚠️ 两个接口的响应都**不包含 `total`**，也没有总页数等分页元数据。直播榜单需翻页时持续请求下一页，直到某页返回条数少于 `pageSize` 或达到第 5 页；直播详情的 `data` 成功时恒为 1 元素数组。

### 直播榜单字段（`data` 数组中的每个元素）

| 字段 | 类型 | 说明 |
|------|------|------|
| livestream_start_time | integer | 直播开始时间（epoch 毫秒） |
| livestream_end_time | integer | 直播结束时间（epoch 毫秒） |
| livestream_duration | integer | 直播时长（秒） |
| livestream_title | string | 直播标题 |
| livestream_id | string | 直播唯一 ID（字符串，避免大整数精度丢失）；可用作详情接口的 `livestreamId` |
| creator_id | string | 达人唯一 ID（字符串，避免大整数精度丢失） |
| creator_handle | string | 达人账号 handle |
| revenue | string | 总销售额 / GMV（按请求的 `currency` 货币；**返回为字符串**，如 `"185590.52"`） |
| unit_price | string | 件单价（按请求的 `currency` 货币；**返回为字符串**，如 `"265.89"`） |
| views | integer | 观看数 |
| record_type | string | 记录类型（如 `SHORT`） |

> **货币字段为字符串**：榜单接口的 `revenue` 与 `unit_price` 返回的是字符串（如 `"185590.52"`），不是数字，使用前需转换为数值类型（`float()` / `Number()` / `ConvertFrom-Json`）。默认按 `revenue`（GMV）降序排列。

### 直播详情字段（`data` 固定为 1 元素数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| livestream_id | string | 直播唯一 ID（与请求的 `livestreamId` 一致） |
| livestream_title | string | 直播标题（如 `24 HOUR STREAM`） |
| creator_id | string | 达人唯一 ID（字符串，避免大整数精度丢失） |
| creator_handle | string | 达人用户名/handle（如 `pokepiglt`） |
| livestream_start_time | integer | 直播开始时间，epoch 毫秒（如 `1783810950000`） |
| livestream_end_time | integer | 直播结束时间，epoch 毫秒（如 `1783898407000`） |
| livestream_duration | integer | 直播时长，单位**秒**（如 `87457`） |
| record_type | string | 记录类型（如 `SHORT`） |
| viewers | integer | 观看人数（注意：DETAIL 用 `viewers`，RANK 用 `views`） |
| revenue | number | 直播销售额 / GMV，**数字**类型，按请求的 `currency` 货币（如 `185590.52`）——注意：在直播 RANK 接口中 `revenue` 是字符串，此处为数字 |
| gpm | number | GMV per mille（每千次展示 GMV），数字类型——DETAIL 独有，RANK 接口无此字段 |
| product_number | integer | 直播带货商品数 |

> **与 RANK 接口的字段名/类型差异**：直播 DETAIL 接口使用 `viewers`（RANK 接口使用 `views`）；DETAIL 的 `revenue` 是**数字**（RANK 的 `revenue` 是**字符串**）；DETAIL 有 `gpm`（RANK 无），DETAIL 无 `unit_price`（RANK 有）。用 `jq`/`ConvertFrom-Json` 抽取时务必使用上方对应接口的字段名。

## 真实响应示例

### 直播榜单

`region=US, dateRange=last7Day, pageSize=5, pageNumber=1`（节选前 2 条）：

```json
{
  "errcode": 200,
  "data": [
    {
      "livestream_start_time": 1783810950000,
      "livestream_duration": 87457,
      "revenue": "185590.52",
      "livestream_title": "24 HOUR STREAM",
      "creator_id": "7446971784983921710",
      "livestream_id": "7661409374878878494",
      "creator_handle": "pokepiglt",
      "unit_price": "265.89",
      "livestream_end_time": 1783898407000,
      "views": 205348,
      "record_type": "SHORT"
    },
    {
      "livestream_start_time": 1783213207000,
      "livestream_duration": 4306,
      "revenue": "149304.17",
      "livestream_title": "DEALS FOR YOU - Live Now!",
      "creator_id": "7153432386608251946",
      "livestream_id": "7658842218676947743",
      "creator_handle": "based",
      "unit_price": "25.26",
      "livestream_end_time": 1783217513000,
      "views": 51765,
      "record_type": "SHORT"
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

### 直播详情

`livestreamId=7661409374878878494`：

```json
{
  "errcode": 200,
  "data": [
    {
      "livestream_start_time": 1783810950000,
      "livestream_duration": 87457,
      "viewers": 205348,
      "revenue": 185590.52,
      "livestream_title": "24 HOUR STREAM",
      "gpm": 903.79,
      "creator_id": "7446971784983921710",
      "livestream_id": "7661409374878878494",
      "creator_handle": "pokepiglt",
      "livestream_end_time": 1783898407000,
      "record_type": "SHORT",
      "product_number": 68
    }
  ],
  "costToken": 14000,
  "errmsg": "ok"
}
```

> 脚本落盘的完整 JSON 包含全部字段，建议用 `jq` 或 `ConvertFrom-Json` 按需抽取。

## 错误码

正常情况下，接口 HTTP 状态码为 200，业务成功与否通过响应体中的 `errcode` 字段区分。当遇到未授权等情况时，HTTP 状态码为 401，且对应 `errcode` 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error；按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 402 | 算力不足 | HTTP 402：按 SKILL.md 的 **解决认证和算力问题** 处理 |
| 501 | 上游调用失败 / 参数无效 | 多种形态：①`errmsg` 形如 `调用 Kalodata 接口失败: Kalodata API HTTP 554: `（上游 Kalodata 瞬时错误），用相同参数重试 1-2 次，不要改参数；持续失败联系网关侧确认 Kalodata 上游配置。②`errmsg` 形如 `page_number 范围为 1-5，当前: 999`（榜单页码越界），修正参数后重试。③详情接口缺少必填 `livestreamId` 时也会返回 501，核对 ID 是否来自榜单结果 |
| 其他非 200 值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
  "errcode": 501,
  "errmsg": "page_number 范围为 1-5，当前: 999"
}
```

## curl 示例

### 直播榜单

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/livestream/rank \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "dateRange": "last7Day",
    "pageSize": 5,
    "pageNumber": 1
  }'
```

### 直播详情

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/kalodata/livestream/detail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "livestreamId": "7661409374878878494",
    "region": "US",
    "dateRange": "last7Day"
  }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-kalodata-tiktok-livestream",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-kalodata-tiktok-livestream`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
