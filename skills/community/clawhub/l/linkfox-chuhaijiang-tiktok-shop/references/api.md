# TikTok 店铺情报 API 参考

## 调用规范

- **请求地址（店铺搜索）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/search`
- **请求地址（店铺详情）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/detail`
- **请求地址（关联达人）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/related-creators`
- **请求地址（关联商品）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/related-products`
- **请求地址（关联视频）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/related-videos`
- **请求地址（店铺热推榜）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/rankings/most-promoted`
- **请求地址（店铺销量榜）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/rankings/top-selling`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，兼容回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

`${LINKFOX_TOOL_GATEWAY}` 未设置时，脚本回退到 `https://tool-gateway.linkfox.com`。以上七个端点都是 LinkFox 网关 POST；Feedback API 与 onboarding 链路不属于这些店铺端点。

## 入口脚本

| 能力 | 脚本 | 算力/次 |
|---|---|---:|
| 店铺搜索 | `chuhaijiang_seller_search.py` | 18 |
| 店铺详情 | `chuhaijiang_seller_detail.py` | 9 |
| 关联达人 | `chuhaijiang_seller_related_creators.py` | 18 |
| 关联商品 | `chuhaijiang_seller_related_products.py` | 18 |
| 关联视频 | `chuhaijiang_seller_related_videos.py` | 18 |
| 店铺热推榜 | `chuhaijiang_seller_rank_most_promoted.py` | 18 |
| 店铺销量榜 | `chuhaijiang_seller_rank_top_selling.py` | 18 |

七个业务入口脚本默认缓存成功响应 24 小时。缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离；相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不写入缓存；业务成功的空结果可以缓存。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制发起真实请求，可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

## 公共约定

- 网关/MCP 请求参数使用 camelCase；Java 服务再映射为上游 snake_case。不要向脚本传 `page_size`、`seller_type`、`shop_type` 等内部字段。
- ID 应作为 JSON string 发送和保存，避免 64 位标识在 JavaScript/表格工具中丢失精度。
- 成功数据字段可能缺失、为 `null`，或随上游增加；入口脚本保留完整原始 JSON。
- 金额通常是 `{ "unit": "US", "value": 31 }`。按运行时类型解析，不要自行换算或改写币种。

### 通用请求参数

除详情外，搜索、关联和榜单端点使用分页字段。各端点只接受自身请求表列出的参数。

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 小写国家码：`br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn` |
| `page` | integer | 否 | - | 页码，最小 1 |
| `pageSize` | integer | 否 | - | 搜索/关联最大 10；榜单为 1–20 |

### 公共成功响应

2026-08-29 的七端点真实调用均返回 HTTP 200、`errcode=200` 和非空业务数据。响应外层为：

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | `200` 表示成功 |
| `errmsg` | string | 成功时为 `ok` |
| `request_id` | string | 请求追踪 ID |
| `data` | object | 端点业务数据 |

业务成功时 `data.items[]` 是主列表，`data.total_count` 是总数。详情还可能返回 `data.core` 和 `data.channel`。入口脚本保留完整原始 JSON，不移除未知业务字段。

## 店铺搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/search`
- **脚本**：`chuhaijiang_seller_search.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

继承 `country`、`page`、`pageSize`，并支持：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `keyword` | string | 否 | 店铺搜索关键词 |
| `category` | string | 否 | 商品分类 ID |
| `sellerType` | string | 否 | 卖家类型；使用服务支持的类型值 |
| `minRating` / `maxRating` | number | 否 | 店铺评分范围 |
| `minSold7d` / `maxSold7d` | number | 否 | 7 天销量范围 |
| `minGmv7d` / `maxGmv7d` | number | 否 | 7 天 GMV 范围 |
| `sort` | string | 否 | `field:asc` 或 `field:desc`；服务默认 `gmv_7d:desc`，真实调用已验证该值 |

```bash
python scripts/chuhaijiang_seller_search.py '{"country":"us","keyword":"beauty","minRating":4,"page":1,"pageSize":3,"sort":"gmv_7d:desc"}'
```

### 响应字段

以下字段来自真实结果；不同店铺可能省略趋势或业务主体等字段。

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 店铺 ID，可传给详情和三个关联端点 |
| `shop_name` | string | 店铺名称 |
| `region` | string | 店铺市场 |
| `shop_rating` | number | 店铺评分 |
| `shop_main_category` | string | 主营分类 ID |
| `shop_product_count` | integer | 商品数 |
| `shop_total_sold_count` | number | 累计销量 |
| `shop_total_gmv` | object | 累计 GMV，含 `unit`、`value` |
| `shop_sold_count_for_last_7_days` | number | 近 7 天销量 |
| `shop_gmv_for_last_7_days` | object | 近 7 天 GMV |
| `total_related_creator_count` | number | 累计关联达人数 |
| `seller_business_info` | array<string> | 商家主体信息 |
| `sold_count_trend` | array<object> | 销量趋势点，含 `timestamp`、`value` |

## 店铺详情

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/detail`
- **脚本**：`chuhaijiang_seller_detail.py`
- **基础数据**：`data.items[]`
- **可选核心数据**：`data.core.items[]`
- **可选渠道数据**：`data.channel.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 店铺 ID |
| `include` | string | 否 | `core`、`channel`，或二者用英文逗号组合：`core,channel` / `channel,core` |

```bash
python scripts/chuhaijiang_seller_detail.py '{"country":"us","id":"7495205878591949358","include":"core,channel"}'
```

### 基础详情 `data.items[]`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` / `seller_id` | string | 店铺 ID |
| `shop_name` / `region` | string | 店铺名称和市场 |
| `shop_rating` | number | 店铺评分 |
| `shop_total_gmv` | object | 累计 GMV |
| `shop_main_category` | string | 主营分类 ID |
| `business_info` | array<string> | 商家主体 |
| `seller_avatar` | object | `thumb_url`、`url` |
| `create_time` / `last_update_time` | integer | 毫秒时间戳 |
| `creator_user_id` / `creator_user_name` / `creator_nickname` | string | 店铺关联账号身份 |
| `creator_role` | integer | 账号角色值 |

### 核心详情 `data.core.items[]`

`data.core.total_count` 是核心详情记录数，真实单店响应为 1。

真实响应包括：`id`、`core_seller_id`、`core_region`、`core_seller_shop_product_count`、`core_seller_shop_total_product_count`、`core_shop_total_sold_count`、`core_seller_shop_total_gmv`、`core_seller_sold_count_for_last_30_days`、`core_seller_gmv_for_last_30_days`、`core_seller_total_related_creator_count`、`core_seller_total_related_live_creator_count`、`core_seller_total_related_video_creator_count`、`core_seller_total_related_shop_creator_count`。

### 渠道详情 `data.channel.items[]`

`data.channel.total_count` 是渠道详情记录数，真实单店响应为 1。

真实响应包括：`id`、`channel_seller_id`、`channel_seller_sold_count_for_last_30_days`、`channel_seller_gmv_for_last_30_days`、`channel_video_30d_sold_count`、`channel_video_30d_gmv`、`channel_live_30d_sold_count`、`channel_live_30d_gmv`、`channel_product_card_30d_sold_count`、`channel_product_card_30d_gmv`、`channel_personal_creator_30d_sold_count`、`channel_personal_creator_30d_gmv`、`channel_seller_creator_30d_sold_count`、`channel_seller_creator_30d_gmv`。

## 店铺关联数据

### 共享请求字段

关联达人、关联商品、关联视频共享：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 店铺 ID |
| `page` | integer | 否 | 最小 1 |
| `pageSize` | integer | 否 | 最大 10 |

### 关联达人

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/related-creators`
- **脚本**：`chuhaijiang_seller_related_creators.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_seller_related_creators.py '{"country":"us","id":"7495205878591949358","page":1,"pageSize":10}'
```

真实达人行包含以下字段：

- 身份：`id`、`tiktok_seller_detail_creator_user_id`、`tiktok_seller_detail_creator_unique_id`、`tiktok_seller_detail_creator_nickname`、`tiktok_seller_detail_creator_country_code`、`tiktok_seller_detail_creator_account_type`、`tiktok_seller_detail_creator_category_label`、`tiktok_seller_detail_creator_user_avatar`、`tiktok_seller_detail_creator_seller_id`、`tiktok_seller_detail_creator_youtube_channel_id`。
- 受众和互动：`tiktok_seller_detail_creator_follower_count`、`tiktok_seller_detail_creator_total_favorited`、`tiktok_seller_detail_creator_video_count`、`tiktok_seller_detail_creator_related_total_video`、`tiktok_seller_detail_creator_author_avg_like_cnt`、`tiktok_seller_detail_creator_author_avg_play_cnt`、`tiktok_seller_detail_creator_author_total_play_cnt`、`tiktok_seller_detail_creator_author_avg_engagement_rate`。
- 带货渠道：`tiktok_seller_detail_creator_by_live`、`tiktok_seller_detail_creator_by_shop`、`tiktok_seller_detail_creator_by_video`。
- GMV：`tiktok_seller_detail_creator_video_7d_gmv`、`tiktok_seller_detail_creator_video_30d_gmv`、`tiktok_seller_detail_live_7d_gmv`、`tiktok_seller_detail_creator_live_30d_gmv`、`tiktok_seller_detail_total_video_live_7d_gmv`、`tiktok_seller_detail_creator_total_video_live_30d_gmv`。
- 联系方式：`tiktok_seller_detail_creator_bio_email`，可能为空或缺失。

### 关联商品

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/related-products`
- **脚本**：`chuhaijiang_seller_related_products.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_seller_related_products.py '{"country":"us","id":"7495205878591949358","page":1,"pageSize":10}'
```

商品行包含：

- 身份和链接：`id`、`tiktok_seller_product_product_id`、`tiktok_seller_product_product_name`、`tiktok_seller_detail_product_link`、`tiktok_seller_detail_product_detail_link`、`tiktok_seller_product_region`。
- 分类和状态：`tiktok_seller_product_l1_category`、`tiktok_seller_product_l2_category`、`tiktok_seller_product_l3_category`、`tiktok_seller_product_product_status`、`tiktok_seller_product_create_time`。
- 表现：`tiktok_seller_product_product_sold_count`、`tiktok_seller_product_product_sold_count_for_last_7_days`、`tiktok_seller_product_product_gmv`、`tiktok_seller_product_product_gmv_for_last_7_days`、`tiktok_seller_product_product_rating`、`tiktok_seller_product_review_count`、`tiktok_seller_product_commission_rate`、`tiktok_seller_product_total_related_creator_count`、`tiktok_seller_product_total_related_video_count`。
- 价格和媒体：`tiktok_seller_product_floor_price`、`tiktok_seller_product_ceiling_price`、`tiktok_seller_product_product_images[]`（`thumb_url`、`url`）。
- SKU：`tiktok_seller_product_product_skus[]` 含 `sku_id`、`price`、`sku_sale_props[]`、`stock`、`sale_prop_value_ids`、`status`；`price` 含 `original_price`、`original_price_value`、`real_price`、`discount`、`unit_price_desc`。
- 规格：`tiktok_seller_product_product_sku_props[]` 含 `prop_id`、`prop_name`、`has_image`、`sale_prop_values[]`；规格值含 `prop_value_id`、`prop_value`、`image`。

### 关联视频

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/related-videos`
- **脚本**：`chuhaijiang_seller_related_videos.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_seller_related_videos.py '{"country":"us","id":"7495205878591949358","page":1,"pageSize":10}'
```

视频行真实字段：`id`、`tiktok_seller_detail_video_id`、`tiktok_seller_detail_video_seller_id`、`tiktok_seller_detail_video_desc`、`tiktok_seller_detail_video_launch_time`、`tiktok_seller_detail_video_duration`、`tiktok_seller_detail_cover_url`、`tiktok_seller_detail_share_url`、`tiktok_seller_detail_video_play_count`、`tiktok_seller_detail_video_30d_play_count`、`tiktok_seller_detail_video_like_count`、`tiktok_seller_detail_video_comment_count`、`tiktok_seller_detail_video_engagement_rate`、`tiktok_seller_detail_video_30d_sold_count`、`tiktok_seller_detail_video_30d_gmv`、`tiktok_seller_detail_is_ad`、`tiktok_seller_detail_video_ad_source`、`tiktok_seller_detail_is_aigc_video`、`tiktok_seller_detail_user_id`、`tiktok_seller_detail_user_unique_id`、`tiktok_seller_detail_user_nickname`、`tiktok_seller_detail_user_avatar`、`tiktok_seller_detail_follower_count`。

## 店铺榜单

### 共享请求字段

两个榜单都使用 `country`、`date`、`granularity`、`page`、`pageSize`，其中 `pageSize` 为 1–20。

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `date` | string | 是 | `YYYYMMDD` |
| `granularity` | string | 是 | `daily`、`weekly`、`monthly`、`0`、`1` 或 `2` |
| `category` | string | 否 | 商品分类 ID |
| `shopType` | string | 否 | 店铺类型：`1`、`2`、`3` 或 `4` |
| `sort` | string | 否 | `field:asc` 或 `field:desc`，各端点默认值见下文 |

### 店铺热推榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/rankings/most-promoted`
- **脚本**：`chuhaijiang_seller_rank_most_promoted.py`
- **默认排序**：`related_creator_count:desc`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_seller_rank_most_promoted.py '{"country":"us","date":"20260824","granularity":"daily","page":1,"pageSize":10}'
```

真实行字段：`id`、`seller_id`、`shop_name`、`region`、`shop_rating`、`shop_product_count`、`seller_main_category`、`seller_business_info`、`seller_avatar`、`biz_type`、`interval_related_creator_count`、`interval_total_related_creator_count`、`interval_total_related_video_creator_count`、`interval_total_related_shop_creator_count`、`interval_total_related_videos_count`。

### 店铺销量榜

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/rankings/top-selling`
- **脚本**：`chuhaijiang_seller_rank_top_selling.py`
- **默认排序**：`interval_sold_count:desc`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

```bash
python scripts/chuhaijiang_seller_rank_top_selling.py '{"country":"us","date":"20260824","granularity":"daily","page":1,"pageSize":10}'
```

真实行字段：`id`、`seller_id`、`shop_name`、`region`、`shop_rating`、`shop_product_count`、`seller_main_category`、`seller_business_info`、`seller_avatar`、`biz_type`、`interval_sold_count`、`interval_total_sold_count`、`interval_sold_count_growth_rate`、`interval_gmv`、`interval_total_gmv`、`interval_gmv_pop_growth_rate`、`interval_related_creator_count`、`interval_total_related_creator_count`。

## 错误码

| `errcode` / HTTP | 含义 | 处理建议 |
|---|---|---|
| 200 | 成功 | 按端点的 `data` 结构解析 |
| 401 | 认证失败 | 按 `SKILL.md` 的“解决认证和算力问题”处理 |
| 402 | 算力/余额不足 | 停止重试并引导授权或充值 |
| 501 | 参数校验失败 | 根据 `errmsg` 修正参数；非法国家码真实返回此码 |
| 其他非 200 | 业务异常 | 回显 `errmsg`，不得自动连续重试付费接口 |

入口脚本会把 HTTP 错误或业务错误保存并回显，不会缓存失败结果。参数错误不会自动改条件重试。

## curl 示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/sellers/search" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"country":"us","keyword":"beauty","minRating":4,"pageSize":3,"sort":"gmv_7d:desc"}'
```

---

## Feedback API

此端点独立于工具网关。仅在用户明确要求提交反馈，或发现问题后明确授权提交时调用。提交前应概括并脱敏，不得发送原始用户消息、无关任务上下文、手机号或任何凭证。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**：`application/json`

```json
{
  "skillName": "linkfox-chuhaijiang-tiktok-shop",
  "sentiment": "NEUTRAL",
  "category": "SUGGESTION",
  "content": "Describe the user intent, actual behavior, and improvement clearly."
}
```

`sentiment` 取 `POSITIVE`、`NEUTRAL` 或 `NEGATIVE`；`category` 取 `BUG`、`COMPLAINT`、`SUGGESTION` 或 `OTHER`。不得在反馈内容中包含 API Key、手机号或带签名参数的临时 URL。
