# TikTok 达人市场情报 API 参考

## 调用规范

- **网关**：`${LINKFOX_TOOL_GATEWAY}`，未设置时脚本回退 `https://tool-gateway.linkfox.com`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；优先读取 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s
- **参数命名**：网关/MCP 使用 camelCase；不要把内部上游的 snake_case 字段用于脚本参数

## 入口脚本与算力

| 能力 | 请求地址 | 脚本 | 算力/次 |
|---|---|---|---:|
| 达人搜索 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/search` | `chuhaijiang_creator_search.py` | 18 |
| 达人详情 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/detail` | `chuhaijiang_creator_detail.py` | 9 |
| 关联直播 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/related-lives` | `chuhaijiang_creator_related_lives.py` | 18 |
| 带货商品 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/related-products` | `chuhaijiang_creator_related_products.py` | 18 |
| 关联视频 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/related-videos` | `chuhaijiang_creator_related_videos.py` | 18 |
| 达人机构榜 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/rankings/agencies` | `chuhaijiang_creator_rank_agencies.py` | 18 |
| 带货达人榜 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/rankings/commercial` | `chuhaijiang_creator_rank_commercial.py` | 18 |
| 达人涨粉榜 | `${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/rankings/growth` | `chuhaijiang_creator_rank_growth.py` | 18 |

八个业务入口脚本默认缓存成功响应 24 小时。缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离；相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不写入缓存；业务成功的空结果可以缓存。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制发起真实请求，可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

## 公共约定

### 通用请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 小写国家码：`br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn` |
| `page` | integer | 否 | - | 页码，最小 1；详情端点不使用 |
| `pageSize` | integer | 否 | - | 搜索/关联最大 10，榜单为 1–20；详情端点不使用 |

### 公共响应外层

网关成功响应使用以下顶层结构；业务字段位于 `data`：

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | 200 表示成功 |
| `errmsg` | string | 成功时通常为 `ok` |
| `request_id` | string | 请求追踪 ID |
| `data` | object | 端点业务数据，形状按端点区分 |

缓存命中时脚本输出 `Cache hit` 提示，但返回和落盘的 JSON 仍保持原始响应结构，不注入本地缓存字段。

### 分页与金额类型

- 搜索和关联端点 `pageSize` 最大为 10；榜单端点为 1–20。
- 金额字段可能是 number，也可能是包含 `unit`、`value` 的对象。解析前必须检查运行时类型并保留原始单位，不要自行换算。

## 达人搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/search`
- **脚本**：`chuhaijiang_creator_search.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

继承公共字段 `country`、`page`、`pageSize`，并支持：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `keyword` | string | 否 | 搜索关键词 |
| `category` | string | 否 | 达人分类 |
| `minFollowers` / `maxFollowers` | number | 否 | 粉丝数范围 |
| `minGmv30d` / `maxGmv30d` | number | 否 | 30 天 GMV 范围 |
| `minAvgViews` / `maxAvgViews` | number | 否 | 平均播放量范围 |
| `minEngagement` / `maxEngagement` | number | 否 | 互动率范围 |
| `hasContact` | boolean | 否 | 是否有联系方式 |
| `sort` | string | 否 | `field:asc` 或 `field:desc`；默认 `gmv_30d:desc` |

### 调用示例

```bash
python scripts/chuhaijiang_creator_search.py '{"country":"us","keyword":"beauty","page":1,"pageSize":5}'
```

## 达人详情

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/detail`
- **脚本**：`chuhaijiang_creator_detail.py`
- **算力**：9 算力/次
- **成功数据**：基础信息为 `data.items[]`；可选指标为 `data.core.items[]`、`data.channel.items[]` 和 `data.portrait.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 达人 ID |
| `include` | string | 否 | `channel`、`core` 或 `portrait`；多个值用英文逗号分隔 |

### 调用示例

```bash
python scripts/chuhaijiang_creator_detail.py '{"country":"us","id":"7302162228386776110","include":"channel,core,portrait"}'
```

## 达人关联数据

### 共享请求字段

关联直播、带货商品和关联视频共享以下请求结构：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 达人 ID |
| `page` | integer | 否 | 最小 1 |
| `pageSize` | integer | 否 | 最大 10 |

### 关联直播

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/related-lives`
- **脚本**：`chuhaijiang_creator_related_lives.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_creator_related_lives.py '{"country":"us","id":"7302162228386776110","page":1,"pageSize":5}'
```

### 带货商品

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/related-products`
- **脚本**：`chuhaijiang_creator_related_products.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_creator_related_products.py '{"country":"us","id":"7302162228386776110","page":1,"pageSize":5}'
```

### 关联视频

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/related-videos`
- **脚本**：`chuhaijiang_creator_related_videos.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_creator_related_videos.py '{"country":"us","id":"7302162228386776110","page":1,"pageSize":5}'
```

## 达人榜单

### 共享请求字段

三个榜单都使用公共字段 `country`、`page`、`pageSize`；`pageSize` 为 1–20。

### 达人机构榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/rankings/agencies`
- **脚本**：`chuhaijiang_creator_rank_agencies.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `category` | string | 否 | 机构分类 |
| `sort` | string | 否 | 排序；默认 `gmv_30d:desc` |

```bash
python scripts/chuhaijiang_creator_rank_agencies.py '{"country":"us","page":1,"pageSize":10}'
```

### 带货达人榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/rankings/commercial`
- **脚本**：`chuhaijiang_creator_rank_commercial.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `date` | string | 是 | `YYYYMMDD` |
| `granularity` | string | 是 | `daily`、`weekly`、`monthly`、`0`、`1` 或 `2` |
| `creatorCategory` | string | 否 | 达人分类 |
| `productCategory` | string | 否 | 商品分类 |
| `sort` | string | 否 | 排序；默认 `total_gmv:desc` |

```bash
python scripts/chuhaijiang_creator_rank_commercial.py '{"country":"us","date":"20260828","granularity":"daily","pageSize":10}'
```

### 达人涨粉榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/rankings/growth`
- **脚本**：`chuhaijiang_creator_rank_growth.py`
- **算力**：18 算力/次
- **成功数据**：`data.items[]`，总数为 `data.total_count`

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `date` | string | 是 | `YYYYMMDD` |
| `granularity` | string | 是 | `daily`、`weekly`、`monthly`、`0`、`1` 或 `2` |
| `creatorCategory` | string | 否 | 达人分类 |
| `productCategory` | string | 否 | 商品分类 |
| `sort` | string | 否 | 排序；默认 `new_follower_count:desc` |

```bash
python scripts/chuhaijiang_creator_rank_growth.py '{"country":"us","date":"20260828","granularity":"daily","pageSize":10}'
```

## 响应结构与关键字段

以下字段来自 2026-08-29 的真实生产响应。搜索、关联和榜单使用 `data.items[]`，总数位于 `data.total_count`；详情扩展分别位于 `data.core.items[]`、`data.channel.items[]` 和 `data.portrait.items[]`。

### 达人搜索响应字段

- **列表项字段**：`account_type`, `author_avg_engagement_rate`, `bio_email`, `category_label`, `country_code`, `ecom_video_avg_play_count`, `facebook_url`, `follower_count`, `follower_count_growth_for_last_7_days`, `has_live_product`, `has_shop_product`, `has_video_product`, `id`, `ins_id`, `live_30d_gmv`, `live_30d_gpm`, `nickname`, `product_category_label_list`, `total_favorited`, `total_video_live_30d_gmv`, `unique_id`, `user_avatar`, `user_sell_product_l3_category`, `video_30d_gmv`, `video_30d_gpm`, `video_avg_like_count`, `video_avg_play_count`, `video_total_like_count_to_follower_count_ratio`, `youtube_channel_id`

`bio_email` 和外部社交账号字段只用于判断公开资料可用性；除非用户有明确、合规的业务需求，否则不要在结果中主动展示或汇总联系方式。

### 达人详情响应字段

- **基础资料 `data.items[]`**：`bio_email`, `bio_url`, `category_label`, `enterprise_verify_reason`, `facebook_url`, `has_live_product`, `has_shop_product`, `has_video_product`, `id`, `ins_id`, `last_update_time`, `nickname`, `partnered_brand`, `product_category_label_list`, `signature`, `unique_id`, `user_avatar`, `youtube_channel_id`
- **核心指标 `data.core.items[]`**：`core_author_avg_engagement_rate`, `core_follower_count`, `core_product_count`, `core_total_favorited`, `core_uid`, `core_video_total_like_count_to_follower_count`, `id`, `tioktok_creator_detail_core_ec_video_count`, `tioktok_creator_detail_core_ecom_video_avg_play_count`, `tioktok_creator_detail_core_med_commission_rate`
- **渠道指标 `data.channel.items[]`**：`channel_country_code`, `channel_ec_video_30d_avg_engagement_rate`, `channel_ec_video_30d_avg_play_count`, `channel_live_30d_gmv`, `channel_live_30d_gpm`, `channel_total_video_live_30d_gmv`, `channel_uid`, `channel_video_30d_gmv`, `channel_video_30d_gpm`, `id`
- **受众画像 `data.portrait.items[]`**：`id`, `portrait_age_distribution`, `portrait_follower_count`, `portrait_gender_distribution`, `portrait_region_distribution`, `portrait_uid`

上游真实字段中存在 `tioktok_*` 拼写，必须按响应原样读取，不要擅自改成 `tiktok_*`。

### 关联直播响应字段

- **列表项字段**：`id`, `tiktok_creator_detail_live_country_code`, `tiktok_creator_detail_live_cover`, `tiktok_creator_detail_live_end_time`, `tiktok_creator_detail_live_gmv`, `tiktok_creator_detail_live_gpm`, `tiktok_creator_detail_live_max_user_count`, `tiktok_creator_detail_live_most_product_category_label`, `tiktok_creator_detail_live_new_follow_count`, `tiktok_creator_detail_live_opm`, `tiktok_creator_detail_live_product_count`, `tiktok_creator_detail_live_room_id`, `tiktok_creator_detail_live_room_link`, `tiktok_creator_detail_live_start_time`, `tiktok_creator_detail_live_title`, `tiktok_creator_detail_live_total_sold_count`, `tiktok_creator_detail_live_total_user`, `tiktok_creator_detail_live_user_follower_count`

### 带货商品响应字段

- **列表项字段**：`id`, `tiktok_creator_detail_by_live`, `tiktok_creator_detail_by_shop`, `tiktok_creator_detail_by_video`, `tiktok_creator_detail_live_30d_gmv`, `tiktok_creator_detail_live_30d_sold_count`, `tiktok_creator_detail_product_country_code`, `tiktok_creator_detail_product_id`, `tiktok_creator_detail_product_launch_time`, `tiktok_creator_detail_total_video_live_30d_gmv`, `tiktok_creator_detail_total_video_live_30d_sold_count`, `tiktok_creator_detail_user_id`, `tiktok_creator_detail_video_30d_gmv`, `tiktok_creator_detail_video_30d_sold_count`, `tiktok_product_detail_ceiling_price`, `tiktok_product_detail_commission_rate`, `tiktok_product_detail_floor_price`, `tiktok_product_detail_l1_category`, `tiktok_product_detail_l2_category`, `tiktok_product_detail_l3_category`, `tiktok_product_detail_product_images`, `tiktok_product_detail_product_name`, `tiktok_product_detail_product_rating`, `tiktok_product_detail_product_sku_props`, `tiktok_product_detail_product_skus`, `tiktok_product_detail_product_status`, `tiktok_product_detail_region`

### 关联视频响应字段

- **列表项字段**：`id`, `tiktok_creator_detail_is_ad`, `tiktok_creator_detail_is_aigc_video`, `tiktok_creator_detail_video_30d_gmv`, `tiktok_creator_detail_video_30d_sold_count`, `tiktok_creator_detail_video_ad_source`, `tiktok_creator_detail_video_author_category_label`, `tiktok_creator_detail_video_author_nickname`, `tiktok_creator_detail_video_author_uid`, `tiktok_creator_detail_video_author_unique_id`, `tiktok_creator_detail_video_collect_count`, `tiktok_creator_detail_video_comment_count`, `tiktok_creator_detail_video_country_code`, `tiktok_creator_detail_video_cover`, `tiktok_creator_detail_video_desc`, `tiktok_creator_detail_video_duration`, `tiktok_creator_detail_video_engagement_rate`, `tiktok_creator_detail_video_id`, `tiktok_creator_detail_video_launch_time`, `tiktok_creator_detail_video_like_count`, `tiktok_creator_detail_video_play_count`, `tiktok_creator_detail_video_product_id`, `tiktok_creator_detail_video_product_images`, `tiktok_creator_detail_video_product_l1_category`, `tiktok_creator_detail_video_product_l2_category`, `tiktok_creator_detail_video_product_l3_category`, `tiktok_creator_detail_video_product_title`, `tiktok_creator_detail_video_share_count`, `tiktok_creator_detail_video_share_url`, `tiktok_creator_detail_video_total_like_count_to_follower_count_ratio`, `tiktok_creator_detail_video_user_avatar`

### 达人机构榜响应字段

- **列表项字段**：`avg_commission_rate`, `follower_count`, `has_email_address`, `has_phone`, `has_whats_app`, `id`, `partner_icon`, `partner_id`, `partner_name`, `partner_top3_category`, `partner_top3_category_list`, `total_30d_video_live_gmv`, `total_30d_video_live_sold_count`, `total_related_creator_count`, `total_related_product_count`, `total_related_seller_count`, `video_count`

### 带货达人榜响应字段

- **列表项字段**：`bio_email`, `category_label`, `country_code`, `creator_oecuid`, `follower_count`, `handle`, `id`, `interval_ecom_video_play_count_growth`, `interval_live_user`, `interval_new_follower`, `l1_category_aggregated_live_gmv`, `l1_category_aggregated_total_gmv`, `l1_category_aggregated_video_gmv`, `nickname`, `product_count`, `titkok_creator_commercial_interval_live_gmv`, `titkok_creator_commercial_interval_total_video_live_gmv`, `titkok_creator_commercial_interval_video_gmv`, `uid`, `unique_id`, `user_avatar`, `user_sell_product_l1_category`

### 达人涨粉榜响应字段

- **列表项字段**：`bio_email`, `category_label`, `channel_id`, `creator_oecuid`, `follower_count`, `handle`, `id`, `interval_new_follower`, `nickname`, `tioktok_creator_growth_interval_new_follower_ratio`, `uid`, `unique_id`, `user_avatar`, `user_sell_product_l1_category`, `video_count`

比率、时间和窗口指标按原值呈现，不自行改写为百分比或另一个周期。

## 错误码

| `errcode` / HTTP | 含义 | 处理建议 |
|---|---|---|
| 200 | 成功 | 按对应端点结构解析 `data` |
| 401 | 认证失败 | 按 `SKILL.md` 的认证引导处理 |
| 402 | 算力或余额不足 | 停止重试并引导授权或充值 |
| 403 | 无权限 | 停止调用并联系网关侧确认工具是否启用 |
| 501 | 参数校验失败 | 根据 `errmsg` 修正参数 |
| 其他非 200 | 业务异常 | 回显错误信息，不自动连续重试付费接口 |

## curl 示例

### 达人搜索

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/creators/search" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"country":"us","keyword":"beauty","page":1,"pageSize":5}'
```

---

## Feedback API

此端点独立于工具网关：

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**：`application/json`

```json
{
  "skillName": "linkfox-chuhaijiang-tiktok-creator",
  "sentiment": "NEUTRAL",
  "category": "SUGGESTION",
  "content": "Describe the user intent, actual behavior, and improvement clearly."
}
```

`sentiment` 取 `POSITIVE`、`NEUTRAL` 或 `NEGATIVE`；`category` 取 `BUG`、`COMPLAINT`、`SUGGESTION` 或 `OTHER`。反馈内容不得包含 API Key 或达人私人联系方式。

仅当用户明确要求提交反馈，或发现问题后用户明确授权时调用；提交前概括并脱敏，不发送原始用户消息或无关上下文。
