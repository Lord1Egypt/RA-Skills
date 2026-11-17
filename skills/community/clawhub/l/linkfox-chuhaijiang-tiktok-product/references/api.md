# TikTok 商品市场情报 API 参考

## 调用规范

- **请求地址（商品搜索）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/search`
- **请求地址（商品详情）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/detail`
- **请求地址（关联达人）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/related-creators`
- **请求地址（关联直播）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/related-lives`
- **请求地址（商品评论）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/reviews`
- **请求地址（关联视频）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/related-videos`
- **请求地址（商品热推榜）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/rankings/most-promoted`
- **请求地址（商品新品榜）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/rankings/new-arrivals`
- **请求地址（商品销量榜）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/rankings/top-selling`
- **请求地址（图片搜索）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/image-search`
- **请求地址（上传预签名）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/upload/presigned-url`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，兼容回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

> `${LINKFOX_TOOL_GATEWAY}` 未设置时，脚本回退到 `https://tool-gateway.linkfox.com`。以上规范只适用于 11 个 LinkFox 网关 POST；图片上传还会向预签名响应的 `data.url` 发送一次外部 HTTP PUT，该请求使用图片 MIME 类型、不携带 LinkFox API Key 或透传头。Feedback API 与 onboarding 链路也不属于上述商品网关规范。

## 入口脚本与算力

| 能力 | 脚本 | 算力/次 |
|---|---|---:|
| 商品搜索 | `chuhaijiang_product_search.py` | 18 |
| 商品详情 | `chuhaijiang_product_detail.py` | 9 |
| 关联达人 | `chuhaijiang_product_related_creators.py` | 18 |
| 关联直播 | `chuhaijiang_product_related_lives.py` | 18 |
| 商品评论 | `chuhaijiang_product_reviews.py` | 18 |
| 关联视频 | `chuhaijiang_product_related_videos.py` | 18 |
| 商品热推榜 | `chuhaijiang_product_rank_most_promoted.py` | 18 |
| 商品新品榜 | `chuhaijiang_product_rank_new_arrivals.py` | 18 |
| 商品销量榜 | `chuhaijiang_product_rank_top_selling.py` | 18 |
| 图片搜索 | `chuhaijiang_product_image_search.py` | 30 |
| 上传预签名 | `upload_image.py` | 0 |

## 公共约定

- 网关/MCP 请求参数使用 camelCase；不要把内部上游的 snake_case 字段用于脚本参数。

### 通用请求参数

除图片搜索和上传预签名外，商品端点使用以下公共字段。各端点只接受其请求表列出的字段。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 小写国家码：`br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn` |
| `page` | integer | 否 | - | 页码，最小 1；详情端点不使用 |
| `pageSize` | integer | 否 | - | 搜索/关联最大 10，榜单为 1–20；详情端点不使用 |

### 公共响应外层

2026-08-29 的完整真实链路验证中，10 个商品业务端点均返回 `errcode=200`，上传预签名后的外部 PUT 返回 HTTP 200；商品详情同时返回 `data.items`、`data.core.items` 与 `data.channel.items`。业务端点成功响应使用以下顶层结构：

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | 200 表示成功 |
| `errmsg` | string | 成功时为 `ok` |
| `request_id` | string | 请求追踪 ID |
| `data` | object | 端点业务数据；形状按端点区分 |

10 个商品业务入口脚本默认缓存成功响应 24 小时。缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离；相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不写入缓存；业务成功的空结果可以缓存。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制发起真实请求，可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。上传预签名和外部 PUT 不使用响应缓存。

### 分页与金额类型

- 搜索和关联端点 `pageSize` 最大为 10；榜单端点为 1–20。
- 金额字段通常为 `{ "unit": "US", "value": 31 }`，但部分榜单字段会直接返回 number。
- 同名 `interval_gmv` 在不同榜单可能分别为 number 或对象。解析前必须检查运行时类型；对象按原始 `unit` 和 `value` 展示，数值按原值展示，不要自行换算。

## 商品搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/search`
- **脚本**：`chuhaijiang_product_search.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

继承公共字段 `country`、`page`、`pageSize`，并支持：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `keyword` | string | 否 | 搜索关键词 |
| `category` | string | 否 | 商品分类 ID |
| `sellerType` | string | 否 | `1`=海外非品牌、`2`=本地、`3`=品牌、`4`=非品牌 |
| `minPrice` / `maxPrice` | number | 否 | 最低/最高价格（美元） |
| `minRating` / `maxRating` | number | 否 | 评分范围，0–5 |
| `minSold7d` / `maxSold7d` | number | 否 | 7 天销量范围 |
| `minSold30d` / `maxSold30d` | number | 否 | 30 天销量范围 |
| `freeShipping` | boolean | 否 | 是否包邮 |
| `sort` | string | 否 | `field:asc` 或 `field:desc`；字段为 `daily_sold`、`gmv_30d`、`gmv_7d`、`price`、`rating`、`sold_30d`、`sold_7d`；默认 `gmv_7d:desc` |

### 调用示例

```bash
python scripts/chuhaijiang_product_search.py '{"country":"us","keyword":"beauty","minRating":4,"freeShipping":true,"pageSize":5}'
```

## 商品详情

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/detail`
- **脚本**：`chuhaijiang_product_detail.py`
- **算力**：9 算力/次
- **成功数据**：基础信息为 `data.items[]`；可选指标为 `data.core.items[]` 和 `data.channel.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 商品 ID |
| `include` | string | 否 | `channel` 或 `core`；多个值用英文逗号分隔 |

### 调用示例

```bash
python scripts/chuhaijiang_product_detail.py '{"country":"us","id":"1732052189676081387","include":"core,channel"}'
```

## 商品关联数据

### 共享请求字段

关联达人、关联直播、商品评论和关联视频共享以下请求结构：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 商品 ID |
| `page` | integer | 否 | 最小 1 |
| `pageSize` | integer | 否 | 最大 10 |

### 关联达人

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/related-creators`
- **脚本**：`chuhaijiang_product_related_creators.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_product_related_creators.py '{"country":"us","id":"1732052189676081387","page":1,"pageSize":10}'
```

### 关联直播

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/related-lives`
- **脚本**：`chuhaijiang_product_related_lives.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_product_related_lives.py '{"country":"us","id":"1732052189676081387","page":1,"pageSize":10}'
```

### 商品评论

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/reviews`
- **脚本**：`chuhaijiang_product_reviews.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_product_reviews.py '{"country":"us","id":"1732052189676081387","page":1,"pageSize":10}'
```

### 关联视频

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/related-videos`
- **脚本**：`chuhaijiang_product_related_videos.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_product_related_videos.py '{"country":"us","id":"1732052189676081387","page":1,"pageSize":10}'
```

## 商品榜单

### 共享请求字段

三个榜单都使用公共字段 `country`、`page`、`pageSize`，其中 `pageSize` 为 1–20。`sellerType` 接受 `1`、`2`、`3` 或 `4`。

### 商品热推榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/rankings/most-promoted`
- **脚本**：`chuhaijiang_product_rank_most_promoted.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `date` | string | 是 | `YYYYMMDD` |
| `granularity` | string | 是 | `daily`、`weekly`、`monthly`、`0`、`1` 或 `2` |
| `category` | string | 否 | 商品分类 |
| `sellerType` | string | 否 | `1`、`2`、`3` 或 `4` |
| `sort` | string | 否 | `interval_gmv`、`interval_sold_count`、`live_count`、`live_user_count`、`related_creator_count`、`video_play_count`；格式为 `field:asc` 或 `field:desc`，默认 `related_creator_count:desc` |

```bash
python scripts/chuhaijiang_product_rank_most_promoted.py '{"country":"us","date":"20260824","granularity":"daily","pageSize":10}'
```

### 商品新品榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/rankings/new-arrivals`
- **脚本**：`chuhaijiang_product_rank_new_arrivals.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `category` | string | 否 | 商品分类 |
| `sellerType` | string | 否 | `1`、`2`、`3` 或 `4` |
| `listedFrom` / `listedTo` | string | 否 | 上架日期范围，`YYYYMMDD` |
| `productStatus` | string | 否 | `1`、`2`、`3` 或 `4` |
| `sort` | string | 否 | `gmv_3d`、`sold_count_3d`、`total_gmv`、`total_sold_count`；格式为 `field:asc` 或 `field:desc`，默认 `gmv_3d:desc` |

```bash
python scripts/chuhaijiang_product_rank_new_arrivals.py '{"country":"us","page":1,"pageSize":10}'
```

### 商品销量榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/rankings/top-selling`
- **脚本**：`chuhaijiang_product_rank_top_selling.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `date` | string | 是 | `YYYYMMDD` |
| `granularity` | string | 是 | `daily`、`weekly`、`monthly`、`0`、`1` 或 `2` |
| `category` | string | 否 | 商品分类 |
| `sellerType` | string | 否 | `1`、`2`、`3` 或 `4` |
| `sort` | string | 否 | `gmv_growth_rate`、`interval_gmv`、`interval_sold_count`、`sold_count_growth_rate`、`total_gmv`、`total_sold_count`；格式为 `field:asc` 或 `field:desc`，默认 `interval_sold_count:desc` |

```bash
python scripts/chuhaijiang_product_rank_top_selling.py '{"country":"us","date":"20260824","granularity":"daily","pageSize":10}'
```

## 图片搜索工作流

### 上传预签名

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/upload/presigned-url`
- **脚本**：`upload_image.py`
- **算力**：0 算力/次
- **成功数据**：`data.url`、`data.os_key`、`data.os_bucket`、`data.signed_url`

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `fileName` | string | 是 | 带扩展名的文件名；辅助脚本支持 JPG/JPEG/PNG |

该 LinkFox 路由映射到出海匠加速版 `POST /open/v1/upload/presigned-url`。辅助脚本会请求预签名并继续完成 PUT：

```bash
python scripts/upload_image.py /path/to/product.jpg
```

### 外部 HTTP PUT

只向预签名响应的 `data.url` 发送 HTTP PUT，body 为图片字节，`Content-Type` 与图片格式一致。此 PUT 不经过 `${LINKFOX_TOOL_GATEWAY}`，不计入 11 个 endpoint，也不携带 LinkFox API Key。HTTP 200、201 或 204 表示上传成功；不得把 `signed_url` 当作上传地址备用。

`upload_image.py` 成功时仅输出安全元数据：`osKey`、`osBucket`、`fileName`、`contentType`、`fileSize`、`uploadStatus`、`requestId`、`errcode`、`errmsg` 和 `presignDataFields`，不会输出两个签名 URL。

### 图片搜索

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/image-search`
- **脚本**：`chuhaijiang_product_image_search.py`
- **算力**：30 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `osKey` | string | 是 | - | 上传返回的 `os_key`，网关参数使用 camelCase |
| `country` | string | 否 | `US` | 大写两位国家码 |

```bash
python scripts/chuhaijiang_product_image_search.py '{"osKey":"returned-key","country":"US"}'
```

## 响应结构与关键字段

除商品详情和上传预签名外，成功业务数据通常位于 `data.items[]`，总数位于 `data.total_count`。业务对象字段可能缺失、为 `null` 或随上游增加；脚本会保留完整原始 JSON，调用方不应丢弃未知字段。

| 端点 | 数据路径 | 解析和链式调用所需的关键字段 |
|---|---|---|
| 商品搜索 | `data.items[]` | `id`（详情及关联接口使用）、`product_name`、`product_images`、`floor_price`、`ceiling_price`、`product_rating`、`product_sold_count`、`product_gmv`、`seller_id`、`shop_name` |
| 商品详情 | `data.items[]` | `id`、`product_id`、`product_name`、`product_images`、价格、评分、SKU、规格、店铺和卖家信息 |
| 商品详情核心指标 | `data.core.items[]` | `product_gmv`、`product_sold_count`、近 30 天指标、广告指标、视频指标及关联达人/直播/视频数量 |
| 商品详情渠道指标 | `data.channel.items[]` | 视频、直播、商品卡、个人达人和卖家达人渠道的近 30 天 GMV 与销量 |
| 关联达人 | `data.items[]` | 达人 `user_id`/`uid`/`unique_id`、昵称、粉丝数、互动和播放指标、视频/直播 GMV；联系方式字段可能缺失 |
| 关联直播 | `data.items[]` | `room_id`、标题、直播链接、达人 ID、开播/结束时间、GMV、销量和观众指标 |
| 商品评论 | `data.items[]` | `review_id`、内容、评分、发布时间、图片/媒体及 SKU 信息 |
| 关联视频 | `data.items[]` | `video_id`、描述、封面、分享链接、达人 ID、播放/点赞/互动指标及近 30 天 GMV/销量 |
| 商品热推榜 | `data.items[]` | `id`/`product_id`、商品与店铺信息、区间 GMV/销量、直播数、关联达人数和视频播放量 |
| 商品新品榜 | `data.items[]` | `id`/`product_id`、商品与店铺信息、累计及近 3/7 天 GMV/销量、商品状态和销量趋势 |
| 商品销量榜 | `data.items[]` | `id`/`product_id`、商品与店铺信息、区间/累计 GMV 与销量及其增长率 |
| 图片搜索 | `data.items[]` | `id`、`product_name`、`product_images`、价格、GMV、销量、类目和地区 |
| 上传预签名 | `data` | `url` 仅用于外部 PUT；`os_key` 用于图搜；`os_bucket` 为存储桶；`signed_url` 仅用于临时读取 |

商品详情不要只读取 `data.items`：请求 `include=core,channel` 时还应分别解析 `data.core.items` 与 `data.channel.items`。上传返回的 `data.url` 和 `data.signed_url` 不得打印、写入日志或持久化。解析嵌套对象和数组前应检查实际 JSON 类型。

## 错误码

| `errcode` / HTTP | 含义 | 处理建议 |
|---|---|---|
| 200 | 成功 | 按上方端点结构解析 `data`；详情不要只读取 `data.items` |
| 401 | 认证失败 | 按 `SKILL.md` 的“解决认证和算力问题”处理 |
| 402 | 算力/余额不足 | 停止重试并引导授权或充值 |
| 501 | 参数校验失败 | 根据 `errmsg` 修正参数；真实非法国家码会返回此码 |
| 其他非 200 | 业务异常 | 回显 `errmsg`，不得自动连续重试付费接口 |

## curl 示例

### 商品搜索

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/search" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"country":"us","keyword":"beauty","minRating":4,"pageSize":5}'
```

### 商品详情

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/products/detail" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"country":"us","id":"1732052189676081387"}'
```

### 图片搜索

优先使用 `python scripts/upload_image.py <local-image>`，避免预签名 URL 出现在终端历史。脚本返回 `osKey` 后：

```bash
python scripts/chuhaijiang_product_image_search.py '{"osKey":"returned-key","country":"US"}'
```

---

## Feedback API

此端点独立于工具网关：

仅在用户明确要求提交反馈，或发现问题后明确授权提交时调用。提交前应概括并脱敏，不得发送原始用户消息、无关任务上下文、手机号或任何凭证。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**：`application/json`

```json
{
  "skillName": "linkfox-chuhaijiang-tiktok-product",
  "sentiment": "NEUTRAL",
  "category": "SUGGESTION",
  "content": "Describe the user intent, actual behavior, and improvement clearly."
}
```

`sentiment` 取 `POSITIVE`、`NEUTRAL` 或 `NEGATIVE`；`category` 取 `BUG`、`COMPLAINT`、`SUGGESTION` 或 `OTHER`。不得在反馈内容中包含 API Key 或预签名 URL。
