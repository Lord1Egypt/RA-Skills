# TikTok 视频市场情报 API 参考

## 调用规范

- **协议**：HTTPS `POST`，JSON 请求体
- **请求地址**：
  - `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/search`
  - `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/detail`
  - `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/related-products`
  - `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/reviews`
- **网关变量**：`LINKFOX_TOOL_GATEWAY`；未设置时脚本回退 `https://tool-gateway.linkfox.com`
- **认证**：`Authorization: <api_key>`；api_key 优先读取 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`
- **固定请求头**：`Content-Type: application/json`、`User-Agent: LinkFox-Skill/2.0`
- **透传请求头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`
- **超时**：150 秒
- **运行环境**：Python 3.9+，仅标准库

## 入口脚本与缓存

| 能力 | 脚本 | 网关路径 |
|---|---|---|
| 视频搜索 | `chuhaijiang_video_search.py` | `/chuhaijiang/videos/search` |
| 视频详情 | `chuhaijiang_video_detail.py` | `/chuhaijiang/videos/detail` |
| 视频带货商品 | `chuhaijiang_video_related_products.py` | `/chuhaijiang/videos/related-products` |
| 视频评论 | `chuhaijiang_video_reviews.py` | `/chuhaijiang/videos/reviews` |

四个业务入口脚本默认缓存成功响应 24 小时。缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离；相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不写入缓存；业务成功的空结果可以缓存。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制发起真实请求，可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

## 公共约定

### 通用请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写请求上下文/站点码：`br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`；返回行的 `country_code` 可能不同，必须分别保留 |
| `page` | integer | 搜索/关联/评论可选 | 页码，从 1 开始 |
| `pageSize` | integer | 搜索/关联/评论可选 | 每页数量，最大 10；使用小页验证后再按需扩大 |
| `id` | string | 详情/关联/评论是 | 19 位视频 ID；必须按字符串传递 |

### 公共成功响应

真实调用验证的成功外层为：

```json
{
  "errcode": 200,
  "data": {
    "total_count": 1,
    "items": []
  },
  "errmsg": "ok",
  "request_id": "uuid"
}
```

`data.items` 的行结构由端点决定。`total_count` 可以大于当前页长度。字段可能缺失或为 `null`，不得用零补齐。

## 视频搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/search`
- **脚本**：`chuhaijiang_video_search.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

网关请求使用 camelCase；Java 服务再映射为出海匠上游的 snake_case。请求字段如下：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `keyword` | string | 否 | 视频描述或相关关键词 |
| `category` | string | 否 | 视频分类；Java 契约未提供可用值枚举，只能使用供应商认可的分类值 |
| `isCommercial` | boolean | 否 | 是否带货 |
| `minViews` / `maxViews` | number | 否 | 播放量范围 |
| `minLikes` / `maxLikes` | number | 否 | 点赞量范围 |
| `minGmv30d` / `maxGmv30d` | number | 否 | 30 天 GMV 范围 |
| `minEngagement` / `maxEngagement` | number | 否 | 互动率范围；Java 契约未声明单位或范围，保持供应商原始口径，不自行做百分比换算 |
| `accountType` | integer | 否 | 账号类型，只允许 `0`、`3`、`4` |
| `sort` | string | 否 | `field:asc` 或 `field:desc`；默认 `views:desc` |
| `country` | string | 是 | 请求上下文/站点码 |
| `page` | integer | 否 | 页码，从 1 开始 |
| `pageSize` | integer | 否 | 每页数量，最大 10 |

上述字段的上游别名分别为 `is_commercial`、`min_views`、`max_views`、`min_likes`、`max_likes`、`min_gmv_30d`、`max_gmv_30d`、`min_engagement`、`max_engagement`、`account_type` 和 `page_size`。Skill 调用网关时应使用表中的 camelCase 名称。

Java 侧没有定义 `category` 枚举、`accountType` 的业务名称或除 `views` 外的完整排序字段枚举。实测随意使用 `beauty` 或返回行的作者分类标签作为 `category` 时，网关返回 `errcode=501`，错误消息显示上游 HTTP 502 / `BACKEND_ERROR`；不要猜测分类值或自动换值重试。

只发送用户明确要求的筛选字段。不要为了空结果自动放宽范围、换关键词或翻页。

真实差分验证已覆盖 `isCommercial`、播放/点赞/30 天 GMV/互动率的最小与最大值、`accountType=0` 和 `sort=views:desc` 的组合请求；`isCommercial=true` 的独立请求返回了商品、30 天销量和 GMV 字段。

### 真实响应关键字段

| 字段 | 说明 |
|---|---|
| `id` | 视频 ID |
| `video_desc` / `share_url` | 文案与公开链接 |
| `video_launch_time` / `video_duration` | 发布时间戳与时长 |
| `author_id` / `author_unique_id` / `author_nickname` | 作者身份 |
| `country_code` / `account_type` | 返回行的地区与账号类型 |
| `video_play_count` / `video_like_count` | 播放与点赞 |
| `video_comment_count` / `video_share_count` / `video_collect_count` | 互动计数 |
| `video_engagement_rate` | 十进制互动率 |
| `video_total_like_count_to_follower_count_ratio` | 点赞与粉丝比率 |
| `video_30d_gpm` | `{unit,value}` 结构的 30 天 GPM |
| `is_ad` / `is_aigc_video` | 广告和 AIGC 标记，字段可能缺失 |

```bash
python scripts/chuhaijiang_video_search.py '{"country":"us","keyword":"beauty","isCommercial":true,"sort":"views:desc","page":1,"pageSize":3}'
```

## 视频详情

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/detail`
- **脚本**：`chuhaijiang_video_detail.py`
- **成功数据**：`data.items[]`；`include=core` 时另有 `data.core.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写站点码 |
| `id` | string | 是 | 视频 ID |
| `include` | string | 否 | 使用 `core` 取得标准化核心表现字段 |

真实验证的 `data.items[0]` 包含 `video_cover`、`user_avatar`、`video_duration`、`unique_id`、`nickname`、`follower_count`、`had_product`、`has_comment`、`share_url`、`video_count`、`video_avg_play_count`、`video_avg_like_count` 与 `author_avg_engagement_rate` 等字段。

`data.core.items[0]` 包含 `core_video_play_count`、`core_video_like_count`、`core_video_comment_count`、`core_video_share_count`、`core_video_collect_count`、`core_video_engagement_rate`、`core_video_like_play_ratio`、`core_video_30d_gpm` 与 `core_country_code`。

```bash
python scripts/chuhaijiang_video_detail.py '{"country":"us","id":"6788833646091504902","include":"core"}'
```

## 视频带货商品

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/related-products`
- **脚本**：`chuhaijiang_video_related_products.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

继承 `country`、`id`、`page`、`pageSize`。普通非带货视频返回 `errcode=200`、`total_count=0` 和空 `items`，这是有效结果。

真实非空响应包含：

- 商品：`tiktok_video_detail_product_id`、`tiktok_product_detail_product_name`、`tiktok_product_detail_product_rating`、类目、图片、SKU、库存与状态。
- 价格：`tiktok_product_detail_floor_price` / `ceiling_price`，均保留 `{unit,value}`。
- 商务：`tiktok_product_detail_commission_rate`、`tiktok_video_detail_product_total_sold_count`、`tiktok_video_detail_product_total_gmv`。
- 视频归因：`tiktok_video_detail_video_id`、`tiktok_video_detail_video_30d_sold_count`、`tiktok_video_detail_video_30d_gmv`。

```bash
python scripts/chuhaijiang_video_related_products.py '{"country":"us","id":"7672655263672864013","page":1,"pageSize":3}'
```

## 视频评论

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/reviews`
- **脚本**：`chuhaijiang_video_reviews.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

继承 `country`、`id`、`page`、`pageSize`。

| 字段 | 说明 |
|---|---|
| `tiktok_video_detail_comment_id` | 评论 ID |
| `tiktok_video_detail_comment_text` | 评论文本 |
| `tiktok_video_detail_comment_create_time` | 创建时间戳 |
| `tiktok_video_detail_comment_like_count` | 点赞数 |
| `tiktok_video_detail_comment_reply_count` | 回复数 |
| `tiktok_video_detail_comment_unique_id` | 评论者 handle |
| `tiktok_video_detail_comment_nickname` | 评论者昵称 |
| `tiktok_video_detail_comment_user_avatar` | `{thumb_url,url}` 头像对象 |
| `tiktok_video_detail_video_id` | 所属视频 ID |

```bash
python scripts/chuhaijiang_video_reviews.py '{"country":"us","id":"6788833646091504902","page":1,"pageSize":3}'
```

## 错误与失败判定

| 情况 | 处理 |
|---|---|
| HTTP 401 或 `errcode=401` | 检查双 env key；读取 `onboarding.md`，不要绕过鉴权 |
| `errcode=402` 或余额/算力不足 | 按 onboarding 的 billing 流程处理，不自动重试 |
| HTTP/业务 403 | 无权限；不归入普通 auth/billing 自动处理 |
| HTTP 4xx | 回显网关 JSON，检查 `country`、`id`、分页和字段类型 |
| HTTP 5xx / 超时 | 保留错误并停止；不得自动连续重试付费请求 |
| 分类值导致网关 `errcode=501`，错误消息显示上游 HTTP 502 / `BACKEND_ERROR` | 分类枚举未公开；停止并要求用户提供供应商认可的分类值 |
| `errcode=200` 且 `items=[]` | 有效空结果，不得伪装为错误或自动换条件 |

成功判定必须同时检查 HTTP 请求完成、`errcode=200`、`errmsg=ok`，且不存在顶层 `error`。脚本会把网关错误作为 JSON 回显，不打印 Python 堆栈。

## 算力消耗规则

| 能力 | 算力/次 |
|---|---:|
| 视频搜索 | 18 |
| 视频详情 | 9 |
| 视频带货商品 | 18 |
| 视频评论 | 18 |

## curl 示例

```bash
curl --request POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/search" \
  --header "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  --header "Content-Type: application/json" \
  --header "User-Agent: LinkFox-Skill/2.0" \
  --data '{"country":"us","keyword":"beauty","isCommercial":true,"sort":"views:desc","page":1,"pageSize":3}' \
  --max-time 150
```

```bash
curl --request POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/videos/detail" \
  --header "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  --header "Content-Type: application/json" \
  --header "User-Agent: LinkFox-Skill/2.0" \
  --data '{"country":"us","id":"6788833646091504902","include":"core"}' \
  --max-time 150
```

---

## Feedback API

- **地址**：`https://skill-api.linkfox.com/api/v1/public/feedback`
- 仅在用户明确要求提交反馈，或发现问题后用户明确授权时调用。
- 建议字段：`skillName`、`endpoint`、`category`、`summary`、`requestId`。
- 自动检测可列举：字段缺失、类型变化、分页异常、空结果与筛选不符、网关错误。
- 提交前必须脱敏；禁止包含 API Key、验证码、手机号、支付信息、签名 URL、原始完整请求/响应或无关上下文。
