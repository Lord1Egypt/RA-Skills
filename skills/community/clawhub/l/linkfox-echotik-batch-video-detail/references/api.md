# EchoTik-批量获取视频详情 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/batchVideoDetail`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| videoIds | array&lt;string&gt; | 否* | - | TikTok视频ID列表，最多1000个。从 `linkfox-echotik-list-video` 等结果获取 |
| videoUrls | array&lt;string&gt; | 否* | - | TikTok视频URL列表（形如 `https://www.tiktok.com/@<unique_id>/video/<videoId>` 或 `https://www.tiktok.com/video/<videoId>`），最多1000个；服务端从每个URL提取末尾 `videoId` 并合并到 `videoIds`，与 `videoIds` 不互斥 |

\* `videoIds` 与 `videoUrls` 至少传一个；两者可同时传入，服务端合并去重后查询。单次合计最多 1000 个。

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 业务状态码，200 表示成功（详见下方错误码） |
| errmsg | string | 业务状态描述 |
| total | integer | 返回的视频条数 |
| columns | array | 渲染列定义（每项含 `field`/`title`/`cellType`/`filterable`/`sortable`） |
| videos | array | 视频详情列表（详见下方视频对象字段） |
| costToken | integer | 消耗token |
| type | string | 渲染样式（如 `tableListWorkbenches`） |

### 视频对象字段

| 字段 | 类型 | 说明 |
|------|------|------|
| videoId | string | 视频ID |
| videoDesc | string | 视频描述/文案 |
| officialUrl | string | TikTok官方视频地址 |
| coverUrl | string | 视频封面URL |
| duration | integer | 视频时长(秒) |
| width | string | 视频宽度(px) |
| height | string | 视频高度(px) |
| ratio | string | 视频清晰度(如 540p/720p) |
| dataSize | string | 视频文件大小 |
| createDate | string | 视频发布日期(yyyy-MM-dd HH:mm:ss) |
| userId | string | 达人ID |
| uniqueId | string | TikTok账号ID(unique_id) |
| avatar | string | 达人头像URL |
| totalViewsCnt | integer | 总播放量 |
| totalViews1dCnt | integer | 最近1天播放量增量 |
| totalViews7dCnt | integer | 最近7天播放量增量 |
| totalViews30dCnt | integer | 最近30天播放量增量 |
| totalDiggCnt | integer | 总点赞数 |
| totalDigg1dCnt | integer | 最近1天点赞增量 |
| totalDigg7dCnt | integer | 最近7天点赞增量 |
| totalDigg30dCnt | integer | 最近30天点赞增量 |
| totalCommentsCnt | integer | 总评论数 |
| totalSharesCnt | integer | 总分享数 |
| totalFavoritesCnt | integer | 总收藏数 |
| totalVideoSaleCnt | integer | 视频销量(件,估算) |
| totalVideoSaleGmvAmt | integer | 视频销售GMV(估算金额) |
| salesFlagText | string | 是否带货视频(是/否) |
| isAdText | string | 是否投流视频(是/否) |
| createdByAiText | string | 是否AI视频(是/否/未知) |
| productCategoryList | string | 关联商品分类(JSON字符串,空为`[]`) |
| videoProducts | string | 视频带货商品(JSON字符串,空为`[]`) |
| region | string | 视频所在区域代码 |
| sourceType | string | 数据来源(如 Tiktok) |
| sourceTool | string | 来源工具(如 EchoTik-视频列表) |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errcode 字段区分（errcode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errcode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 400 | 参数校验错误 | 参数取值非法（如 `videoUrls` 格式不合规）。参考 `errmsg` 获取具体字段与合法值集合 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和算力问题** 处理。|
| 402 | 算力不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和算力问题** 处理。|
| 10000 | 无符合要求的视频 | 传入的视频ID/URL均无匹配数据（如空列表、ID不存在）。核对ID/URL是否正确后重试 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 10000,
    "errmsg": "没有符合要求相关的视频信息"
}
```

## curl 示例

### 按视频ID批量查询

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/batchVideoDetail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "videoIds": ["7030893014180531462", "6768504823336815877", "7425631540178160939"]
  }'
```

### 按视频URL批量查询

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/batchVideoDetail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "videoUrls": [
      "https://www.tiktok.com/@sageandintuition/video/7030893014180531462"
    ]
  }'
```

### ID 与 URL 混合（服务端合并）

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/echotik/batchVideoDetail \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "videoIds": ["7030893014180531462"],
    "videoUrls": ["https://www.tiktok.com/@<unique_id>/video/6768504823336815877"]
  }'
```

---

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-echotik-batch-video-detail",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-echotik-batch-video-detail`)
- `sentiment`: Choose ONE — `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE — `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
