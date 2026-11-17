# EchoTik-TikTok视频列表 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/listVideo`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| region | string | 是 | - | 区域码。可选值：US（美国）、ID（印度尼西亚）、TH（泰国）、PH（菲律宾）、MY（马来西亚）、VN（越南）、GB（英国）、MX（墨西哥）、SG（新加坡）、SA（沙特阿拉伯）、BR（巴西）、ES（西班牙）、JP（日本）、DE（德国）、IT（意大利）、FR（法国） |
| userId | string | 否 | - | 达人ID筛选。最大长度 1000 |
| productId | string | 否 | - | 视频关联商品ID。最大长度 1000 |
| productCategoryId | string | 否 | - | 关联商品类目ID。最大长度 1000 |
| minTotalViewsCnt | integer | 否 | - | 视频播放量筛选（最小值） |
| maxTotalViewsCnt | integer | 否 | - | 视频播放量筛选（最大值） |
| minDuration | integer | 否 | - | 视频时长范围筛选(秒)-最小值 |
| maxDuration | integer | 否 | - | 视频时长范围筛选(秒)-最大值 |
| minCreateTime | integer | 否 | - | 发布时间范围筛选(秒级时间戳)-最小值 |
| maxCreateTime | integer | 否 | - | 发布时间范围筛选(秒级时间戳)-最大值 |
| salesFlag | integer | 否 | - | 是否带货视频：0=非带货视频、1=带货视频 |
| isAd | integer | 否 | - | 是否投流视频：0=非投流视频、1=投流视频 |
| createdByAi | string | 否 | - | 是否AI视频，字符串 `"true"`=AI视频、`"false"`=非AI视频（正则 `^(true\|false)$`，非布尔型） |
| videoSortField | integer | 否 | 3 | 排序字段：1=total_digg_cnt(点赞数)、2=create_time(发布时间)、3=total_views_cnt(播放量) |
| sortType | integer | 否 | 1 | 排序方式：0=升序(asc)、1=降序(desc) |
| pageNum | integer | 否 | 1 | 分页页码，从1开始 |
| pageSize | integer | 否 | 50 | 每页条数。**须为10的倍数，最大100**；第三方接口单页上限10，内部按10每页多次拉取后合并 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功（详见下方错误码） |
| errmsg | string | 业务状态描述 |
| total | integer | 记录数 |
| data | array | 视频列表（详见下方视频字段） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 视频对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| videoId | string | 视频ID |
| videoDesc | string | 视频描述 |
| officialUrl | string | TikTok官方视频地址 |
| coverUrl | string | 视频封面URL |
| duration | integer | 视频时长(秒) |
| width | string | 视频宽度 |
| height | string | 视频高度 |
| ratio | string | 视频清晰度（分辨率，如 540p/720p） |
| dataSize | string | 视频文件大小 |
| createDate | string | 视频发布日期 |
| userId | string | 达人ID |
| uniqueId | string | TikTok账号ID(unique_id) |
| avatar | string | 达人头像 |
| totalViewsCnt | integer | 总播放量 |
| totalViews1dCnt | integer | 近1天播放量 |
| totalViews7dCnt | integer | 近7天播放量 |
| totalViews30dCnt | integer | 近30天播放量 |
| totalDiggCnt | integer | 总点赞数 |
| totalDigg1dCnt | integer | 近1天点赞数 |
| totalDigg7dCnt | integer | 近7天点赞数 |
| totalDigg30dCnt | integer | 近30天点赞数 |
| totalCommentsCnt | integer | 总评论数 |
| totalSharesCnt | integer | 总分享数 |
| totalFavoritesCnt | integer | 总收藏数 |
| totalVideoSaleCnt | integer | 视频销量(件数) |
| totalVideoSaleGmvAmt | integer | 视频销量GMV(金额) |
| salesFlagText | string | 是否带货视频 |
| isAdText | string | 是否投流视频 |
| createdByAiText | string | 是否AI视频（是/否/未知） |
| productCategoryList | string | 商品分类 |
| videoProducts | string | 视频关联商品 |
| region | string | 区域编码 |
| sourceType | string | 商品来源 |
| sourceTool | string | 来源工具 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errcode 字段区分（errcode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数校验错误 | 参数取值非法（如 `region` 不在支持列表、`createdByAi` 非 `true`/`false`、`pageSize` 非 10 的倍数）。参考 `errmsg` 获取具体字段与合法值集合 |
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

### 基础视频列表（按播放量降序）

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listVideo \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "videoSortField": 3,
    "sortType": 1,
    "pageSize": 20,
    "pageNum": 1
  }'
```

### 筛选带货视频 + 播放量区间

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listVideo \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "salesFlag": 1,
    "minTotalViewsCnt": 100000,
    "videoSortField": 3,
    "sortType": 1,
    "pageSize": 20
  }'
```

### 指定达人 + 按点赞降序

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/listVideo \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region": "US",
    "userId": "7234567890123456789",
    "videoSortField": 1,
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
  "skillName": "linkfox-echotik-list-video",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-echotik-list-video`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
