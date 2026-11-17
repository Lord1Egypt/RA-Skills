# TikTok 广告与创意情报 API 参考

## 调用规范

- **请求地址（广告搜索）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/search`
- **请求地址（广告详情）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/detail`
- **请求地址（广告关联商品）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/related-products`
- **请求地址（创意搜索）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/creatives/search`
- **请求地址（创意详情）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/creatives/detail`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，兼容回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

`${LINKFOX_TOOL_GATEWAY}` 未设置时，脚本回退到 `https://tool-gateway.linkfox.com`。

## 入口脚本与端点

| 能力 | 脚本 | 算力/次 |
|---|---|---:|
| 广告搜索 | `chuhaijiang_ad_search.py` | 18 |
| 广告详情 | `chuhaijiang_ad_detail.py` | 9 |
| 广告关联商品 | `chuhaijiang_ad_related_products.py` | 18 |
| 创意搜索 | `chuhaijiang_creative_search.py` | 18 |
| 创意详情 | `chuhaijiang_creative_detail.py` | 9 |

五个业务入口脚本默认缓存成功响应 24 小时。缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离；相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不写入缓存；业务成功的空结果可以缓存。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制发起真实请求，可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

## 公共约定

- 网关请求字段使用 Java/MCP 的 camelCase 名；服务端再映射成上游 snake_case。脚本调用不得直接传 `page_size`、`ad_type`、`has_product` 等 snake_case 字段。
- 普通请求的 `country` 必须是小写：`br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`。
- 搜索和关联商品的 `page` 默认 1、最小 1；`pageSize` 可选且最大 10。
- `sort` 格式为 `field:asc` 或 `field:desc`。Java 层不维护可选字段枚举；不要臆造排序字段，未知时省略并使用上游默认值。
- 金额/GMV/GPM/花费通常为 `{ "unit": string, "value": number }`，但调用方仍应按运行时类型解析。

### 公共成功响应

2026-08-29 使用真实网关链路验证五个端点时，成功响应均为 HTTP 200 且使用以下顶层结构：

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | 200 表示本次业务成功 |
| `errmsg` | string | 成功时为 `ok` |
| `request_id` | string | 请求追踪 ID |
| `data` | object | 端点业务数据，结构见各节 |

入口脚本始终保留完整原始 JSON，不移除未知业务字段。

## 广告搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/search`
- **脚本**：`chuhaijiang_ad_search.py`
- **成功数据**：`data.items[]`；总数为 `data.total_count`

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 支持的小写国家码 |
| `page` | integer | 否 | 1 | 页码，最小 1 |
| `pageSize` | integer | 否 | 上游默认 | 每页数量，最大 10 |
| `keyword` | string | 否 | - | 搜索关键词 |
| `category` | string | 否 | - | 商品分类 |
| `adType` | string | 否 | - | 上游广告类型分类值 |
| `excludeSparkAds` | boolean | 否 | - | 是否排除 Spark Ads |
| `minViews` / `maxViews` | number | 否 | - | 最低/最高播放量 |
| `minGmv` / `maxGmv` | number | 否 | - | 最低/最高 GMV |
| `minDays` / `maxDays` | number | 否 | - | 最低/最高投放天数 |
| `sort` | string | 否 | `gmv:desc` | `field:asc` 或 `field:desc` |

```bash
python scripts/chuhaijiang_ad_search.py '{"country":"us","keyword":"beauty","page":1,"pageSize":3}'
```

### 响应字段

真实非空样本的 `data.items[]` 包含：

- 标识/链接：`id`、`video_id`、`product_id`、`advertiser_id`、`ad_url`、`web_url`、`advertiser_url`
- 文案/主体：`ad_title`、`advertiser_name`、`button_text`、`product_title`
- 时间/投放：`create_time`、`ad_create_time`、`last_update_time`、`duration`、`ad_day_count`
- 表现：`video_play_count`、`video_like_count`、`video_like_rate`、`video_engagement_rate`、`video_popularity`、`total_sc`
- 商业指标：`total_gmv`、`video_gpm_30d`、`ad_maximum_cost`、`ad_roas`
- 分类：`product_l1_category`、`product_l2_category`、`product_l3_category`

后续广告详情和关联商品必须使用本对象的 `id`，不是 `video_id` 或 `product_id`。

## 广告详情

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/detail`
- **脚本**：`chuhaijiang_ad_detail.py`
- **成功数据**：基础信息 `data.items[]`；请求 `include=core` 时另有 `data.core.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 支持的小写国家码 |
| `id` | string | 是 | 广告搜索返回的 `id` |
| `include` | string | 否 | 可选值 `core`；多个值语法为英文逗号分隔 |

```bash
python scripts/chuhaijiang_ad_detail.py '{"country":"us","id":"7658119807128046879","include":"core"}'
```

### 响应字段

- `data.items[]`：`id`、`ad_title`、`advertiser_id`、`advertiser_name`、`advertiser_avatar`、`ad_cover`、`ad_url`、`web_url`、`button_text`、`duration`、`ad_create_time`、`create_time`、`last_update_time`。
- `data.core.items[]`：`core_creative_id`、`core_ad_type`、`core_ad_day_count`、`core_ad_play_ratio`、`core_ad_gmv_ratio`、`core_ad_maximum_cost`、`core_ad_roas`、`core_total_gmv`、`core_total_sc`、`core_video_play_count`、`core_video_like_count`、`core_video_comment_count`、`core_video_share_count`、`core_video_collect_count`、`core_video_gpm_30d`、`core_video_popularity` 和 `id`。

`ad_cover`、`advertiser_avatar` 及金额字段为嵌套对象；使用前检查对象属性，不要当作纯字符串或数字。

## 广告关联商品

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/related-products`
- **脚本**：`chuhaijiang_ad_related_products.py`
- **成功数据**：`data.items[]`；总数为 `data.total_count`

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 支持的小写国家码 |
| `id` | string | 是 | - | 广告搜索返回的 `id` |
| `page` | integer | 否 | 1 | 页码，最小 1 |
| `pageSize` | integer | 否 | 上游默认 | 每页数量，最大 10 |

```bash
python scripts/chuhaijiang_ad_related_products.py '{"country":"us","id":"7658119807128046879","page":1,"pageSize":3}'
```

### 响应字段

真实样本使用带来源前缀的字段名，禁止擅自去前缀或映射成广告搜索字段：

- 商品标识/基础信息：`tiktok_ads_detail_product_id`、`tiktok_product_detail_product_name`、`tiktok_product_detail_product_images`、`tiktok_product_detail_region`、`tiktok_product_detail_product_status`
- 分类/价格/评分：`tiktok_product_detail_l1_category`、`tiktok_product_detail_l2_category`、`tiktok_product_detail_l3_category`、`tiktok_product_detail_floor_price`、`tiktok_product_detail_ceiling_price`、`tiktok_product_detail_product_rating`
- SKU/佣金：`tiktok_product_detail_product_sku_props`、`tiktok_product_detail_product_skus`、`tiktok_product_detail_commission_rate`
- 销售关系：`tiktok_ads_detail_video_id`、`tiktok_ads_detail_product_total_sold_count`、`tiktok_ads_detail_product_total_gmv`、`tiktok_ads_detail_video_30d_sold_count`、`tiktok_ads_detail_video_30d_gmv`、`tiktok_ads_detail_product_launch_time`、`tiktok_ads_detail_product_country_code`
- `id`：当前关联记录 ID；如要继续查商品详情，优先使用 `tiktok_ads_detail_product_id`

## 创意搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/creatives/search`
- **脚本**：`chuhaijiang_creative_search.py`
- **成功数据**：`data.items[]`；总数为 `data.total_count`

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 支持的小写国家码 |
| `page` | integer | 否 | 1 | 页码，最小 1 |
| `pageSize` | integer | 否 | 上游默认 | 每页数量，最大 10 |
| `keyword` | string | 否 | - | 搜索关键词 |
| `category` | string | 否 | - | 素材分类 |
| `hasProduct` | boolean | 否 | - | 是否关联商品 |
| `isSponsored` | boolean | 否 | - | 是否为赞助内容 |
| `isAigc` | boolean | 否 | - | 是否为 AIGC |
| `sort` | string | 否 | `gmv:desc` | `field:asc` 或 `field:desc` |

```bash
python scripts/chuhaijiang_creative_search.py '{"country":"us","hasProduct":true,"page":1,"pageSize":3}'
```

### 响应字段

真实非空样本的 `data.items[]` 包含：

- 标识/作者：`id`、`video_id`、`product_id`、`author_uid`、`author_unique_id`、`author_nickname`、`user_avatar`、`follower_cnt`
- 内容：`video_desc`、`content_tag_v2`、`content_intent`、`platform`、`country_code`、`is_aigc_video`
- 时间/时长：`video_date`、`video_launch_time`、`video_duration`
- 表现：`video_play_count`、`video_like_count`、`video_comment_count`、`video_share_count`、`video_collect_count`、`video_engagement_rate`
- 商业指标：`video_30d_gmv`、`video_total_gmv`、`video_30d_gpm`

创意详情必须使用本对象的 `id`，不是 `video_id` 或 `product_id`。

## 创意详情

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/creatives/detail`
- **脚本**：`chuhaijiang_creative_detail.py`
- **成功数据**：基础信息 `data.items[]`；按 `include` 返回 `data.analysis.items[]` 和/或 `data.embedding.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 支持的小写国家码 |
| `id` | string | 是 | 创意搜索返回的 `id` |
| `include` | string | 否 | `analysis`、`embedding`；多个值用英文逗号分隔 |

```bash
python scripts/chuhaijiang_creative_detail.py '{"country":"us","id":"7668708053428047118","include":"analysis,embedding"}'
```

### 响应字段

- `data.items[]`：创意/作者/商品/表现组合数据，包括 `id`、`video_id`、`uid`、`unique_id`、`nickname`、`follower_count`、`share_url`、`product_id`、`product_name`、`product_images`、类目、价格、评分、佣金、状态、销量/GMV，以及视频播放/互动/30 天销售指标。
- `data.analysis.items[]`：`id`、`video_id`、`video_uri`、`video_cover`、`country_code`、`platform`、`is_aigc_video`、`hook_type`、`hook_subtype`、`formula_type`、`formula_subtype`、`angle_type`、`angle_subtype`、`transcription_with_structure`、`storyboards`。
- `data.embedding.items[]`：`id`、`video_id`、`video_uri`、`video_cover`、`country_code`、`platform`、`extracted_content`、`matched_tags`、`embedding`。

`embedding` 是数值数组，可能显著增大响应；只有明确需要相似度或下游模型输入时才请求。用户可见答复应总结分析字段，不要内联完整向量。

## 错误码与失败处理

| `errcode` / HTTP | 含义 | 处理建议 |
|---|---|---|
| 200 | 成功 | 按端点数据路径解析 |
| 400 | 必填参数缺失等请求错误 | 根据 `errmsg` 补齐或修正参数；不得原样重试 |
| 401 | 认证失败 | 按 `SKILL.md` 的“解决认证和算力问题”处理 |
| 402 | 算力/余额不足 | 停止重试并引导授权或充值 |
| 501 | 参数校验或上游调用失败 | 回显 `errmsg` 并停止，不得自动重试；如需重试，先向用户说明会产生额外算力消耗 |
| 其他非 200 | 业务异常 | 回显错误，不得自动连续试探付费端点 |

网关可能以 HTTP 200 包装业务错误，因此必须同时检查 `errcode` 和 `errmsg`。真实测试中，创意搜索带一组过滤条件时曾收到 `BACKEND_ERROR`，缩减为合法最小请求后成功；不要把一次 5xx 当成字段枚举依据。

## curl 示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/ads/search" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"country":"us","keyword":"beauty","page":1,"pageSize":3}'
```

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/ad-creative/creatives/detail" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{"country":"us","id":"7668708053428047118","include":"analysis,embedding"}'
```

---

## Feedback API

此端点独立于工具网关。仅在用户明确要求提交反馈，或发现问题后明确授权提交时调用。提交前应概括并脱敏，不得发送原始用户消息、无关任务上下文、手机号或任何凭证。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**：`application/json`

```json
{
  "skillName": "linkfox-chuhaijiang-tiktok-ads",
  "sentiment": "NEUTRAL",
  "category": "SUGGESTION",
  "content": "Describe the user intent, actual behavior, and improvement clearly."
}
```

`sentiment` 取 `POSITIVE`、`NEUTRAL` 或 `NEGATIVE`；`category` 取 `BUG`、`COMPLAINT`、`SUGGESTION` 或 `OTHER`。不得在反馈内容中包含 API Key。
