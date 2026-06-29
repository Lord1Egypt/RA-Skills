# ZingAPI 创意列表查询参数说明

本文档说明 `scripts/creative_list.py` 支持的常用参数、字段映射和输出模式。

## 接口信息

请求地址：

`POST https://openapi.dataideaglobal.com/zingapi/v1/creative/list/{customer_name}`

固定请求头：

`x-zf-action: creative-list`

生产环境地址已内置，不需要配置接口域名。

## 鉴权配置

必须配置以下环境变量：

| 环境变量 | 说明 |
| --- | --- |
| `ZINGAPI_ACCESS_KEY_ID` | 接入方 Access Key ID |
| `ZINGAPI_ACCESS_KEY_SECRET` | 接入方 Access Key Secret |
| `ZINGAPI_CUSTOMER_NAME` | 请求路径中的客户名称 |

当前线上服务使用以下签名约定：

- `Authorization` 算法标识：`zf3-HMAC-SHA256`
- 随机数请求头：`x-zf-nonce`
- 请求体哈希请求头：`x-zf-content-sha256`

## 常用脚本参数

| 脚本参数 | ZingAPI 字段 | 支持值 |
| --- | --- | --- |
| `--app-type 游戏` | `app_type` | `1` |
| `--app-type 工具` | `app_type` | `2` |
| `--app-type 电商` | `app_type` | `3` |
| `--creative-type 图片` | `ads_type` | `1` |
| `--creative-type 视频` | `ads_type` | `2` |
| `--creative-type 轮播` | `ads_type` | `3` |
| `--creative-type HTML` | `ads_type` | `4` |
| `--creative-type 试玩` | `ads_type` | `7` |
| `--sort 最新` | `sort_field` | `-first_seen` |
| `--sort 展现` | `sort_field` | `-impression` |
| `--sort 热度` | `sort_field` | `-heat_degree` |
| `--sort 最后发现` | `sort_field` | `-last_seen` |
| `--sort 投放天数` | `sort_field` | `-days` |
| `--dedupe 广告去重` | `duplicate_removal` | `0` |
| `--dedupe 素材去重` | `duplicate_removal` | `1` |
| `--dedupe 广告主去重` | `duplicate_removal` | `2` |

脚本同时兼容英文参数值，例如 `game`、`video`、`latest`、`material`。

## 常用请求字段

使用 `--body '@request.json'` 时，可直接传入 ZingAPI 原始请求体。

完整自然语言入参映射见 `references/input-mapping.md`。若用户需求涉及该映射表中的字段，但脚本没有专用参数，应构造 JSON 请求体并通过 `--body` 调用。

| 字段 | 说明 |
| --- | --- |
| `app_type` | 必填。`1` 游戏，`2` 工具，`3` 电商。 |
| `page` | 页码，默认 `1`，范围 `1-500`。 |
| `page_size` | 每页数量，默认 `20`，最大 `20`。 |
| `platform` | 渠道列表，例如 `["facebook", "instagram", "youtube", "tiktok"]`。 |
| `geo` | 国家/地区编码列表，例如 `["USA", "JPN", "GBR"]`。 |
| `keyword` | 搜索关键词，可传字符串或数组，最多 7 个关键词生效。 |
| `exclude_keyword` | 排除关键词，最多 7 个关键词生效。 |
| `ads_type` | 素材类型。`1` 图片，`2` 视频，`3` 轮播，`4` HTML，`7` 试玩。 |
| `seen_begin`、`seen_end` | 创意发现时间范围，Unix 时间戳。 |
| `first_seen_begin`、`first_seen_end` | 首次发现时间范围，用于查询新创意。 |
| `include_ai_tags` | 是否返回 AI 标签摘要。 |
| `max_ai_tags_per_type` | 每类 AI 标签最大返回数量，默认 `5`。 |
| `ai_tag_search` | 游戏素材内容属性筛选，例如 `{"theme_ids":[50,236]}`。 |
| `game_play`、`game_theme`、`game_ip`、`game_core_track` | 游戏类专属筛选字段。 |
| `tag_ids` | 游戏/工具分类标签。 |
| `popularity_tag` | Top 创意筛选，`1` 表示 Top 1%，`10` 表示 Top 10%。 |
| `like_begin/end`、`comment_begin/end`、`share_begin/end` | 社媒互动指标范围。 |
| `cost_begin/end` | Facebook 广告花费范围。 |

## 输出模式

| 参数 | 说明 |
| --- | --- |
| `--output summary` | 默认模式。按业务含义分组输出摘要字段。 |
| `--output raw` | 输出接口原始响应。 |
| `--dry-run` | 只输出请求地址、请求头摘要和请求体，不发送真实请求。 |

如需后续查询创意详情，应保留 `ad_key`、`app_type` 和 `search_flag`。

出参字段含义见 `references/response-fields.md`。其中“人气值”对应 `all_exposure_value` 或 `new_week_exposure_value`，`heat` 仅表示热度值。
