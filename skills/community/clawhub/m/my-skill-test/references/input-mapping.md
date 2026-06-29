# 创意列表查询入参映射表

本文档根据《ZingAPI 对接文档》中“创意列表查询”的请求体字段整理，用于指导 agent 将用户的自然语言描述转换为接口入参。

使用原则：

- 若字段已有脚本参数，优先使用脚本参数。
- 若字段没有脚本参数，生成 JSON 请求体，并通过 `python scripts/creative_list.py --body '@request.json'` 调用。
- 表中的“用户表达”用于意图识别，不要求完全匹配；后续可根据实际使用继续补充同义词。
- 字典型字段的具体 code 以附录字典值为准。

## 通用检索与分页

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 查询游戏广告、游戏创意、游戏素材 | `app_type` | `1` |
| 查询工具广告、工具类 APP 创意 | `app_type` | `2` |
| 查询电商广告、电商创意 | `app_type` | `3` |
| 第 N 页、翻到第 N 页 | `page` | 取用户指定页码；默认 `1`，最大 `500`。 |
| 返回 N 条、查 N 条、给我 N 个结果 | `page_size` 或分页 | 单页最大 `20`；超过 `20` 时应拆分页查询或使用后续封装的 `limit` 逻辑。 |
| 查最近 N 天、近一周、近一个月 | `seen_begin`、`seen_end` | 转换为时间戳范围；未指定时默认最近 7 天。 |
| 从某天到某天、投放发现时间在某段时间 | `seen_begin`、`seen_end` | 转换为 Unix 时间戳。 |
| 查新广告、只看新创意 | `new_ads_flag` | `1`。 |
| 全部广告、在投广告 | `new_ads_flag` | `0`。 |
| 首次发现时间、首次投放时间、新上架创意 | `first_seen_begin`、`first_seen_end` | 转换为 Unix 时间戳范围；用于新广告查询。 |
| 关键词搜索、包含某词、搜索某品牌/玩法/文案 | `keyword` | 字符串或数组；最多 7 个关键词生效。 |
| 排除某词、不包含某词 | `exclude_keyword` | 字符串数组；最多 7 个关键词生效。 |
| 精确搜索、精准匹配 | `search_type` | `1`。 |
| 默认搜索、模糊搜索 | `search_type` | `0`。 |
| 搜综合、全局搜索 | `position` | `0`。 |
| 搜广告文案、搜文案内容 | `position` | `1`。 |
| 搜广告主、按广告主搜索 | `position` | `2`。 |
| 搜投放主页、搜主页 | `position` | `4`。 |
| 搜落地页域名、搜域名 | `position` | `6`。 |

## 渠道、地区、语言与系统

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| Facebook、FB、脸书渠道 | `platform` | `["facebook"]`。 |
| Instagram、Ins | `platform` | `["instagram"]`。 |
| YouTube | `platform` | `["youtube"]`。 |
| TikTok | `platform` | `["tiktok"]`。 |
| Admob、UnityAds、AppLovin、Vungle/Liftoff 等渠道 | `platform` | 转换为附录渠道 code。 |
| FB 系渠道合并、合并 Facebook 系投放 | `fb_merge` | `true`。 |
| 国家、地区、投放国家、投放在某国 | `geo` | 转换为三位国家/地区 code，如日本 `JPN`、美国 `USA`。 |
| 仅在某些国家投放、只投这些国家 | `complete_country_match` | 与 `geo` 联用，设为 `true`。 |
| 排除某国家、不看某地区 | `exclude_geo` | 转换为三位国家/地区 code 数组。 |
| 文案语言、语言为日语/英语/中文 | `language` | 转换为语言 code，具体 code 以附录为准。 |
| iOS、Android、系统、设备系统 | `os` | 转换为系统 code，具体 code 以附录为准。 |

## 素材类型与素材规格

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 图片广告、图片素材 | `ads_type` | `[1]`。 |
| 视频广告、视频素材 | `ads_type` | `[2]`。 |
| 轮播广告、轮播素材 | `ads_type` | `[3]`。 |
| HTML 广告、HTML 素材 | `ads_type` | `[4]`。 |
| 试玩广告、可玩广告 | `ads_type` | `[7]`。 |
| 图片和视频都要 | `ads_type` | `[1, 2]`。 |
| 版式比例、竖版、横版、方形、9:16、16:9、1:1 | `ads_format` | 转换为附录“版式比例”code，例如 `9:16`、`16:9`、`1:1`。 |
| 高清素材、高清画质 | `ads_size` | `["hd"]`。 |
| 标清素材、标清画质 | `ads_size` | `["sd"]`。 |
| 分辨率、素材尺寸、1920 x 1080、1080 x 1920 | `material_size` | 字符串数组，注意格式为 `"宽 x 高"`，例如 `["1920 x 1080"]`。 |
| 视频时长大于 N 秒、视频时长最少 N 秒 | `video_duration_begin` | 秒数。 |
| 视频时长小于 N 秒、视频时长最多 N 秒 | `video_duration_end` | 秒数。 |
| 有结束卡片、结束卡片广告 | `end_card` | `1`。 |
| 不限制结束卡片、全部结束卡片 | `end_card` | `0`。 |
| 动态广告、动态创意 | `is_dynamic` | `1`。 |
| 原帖广告、广告原帖 | `original_flag` | `1`。 |
| 查看违规广告、违规素材 | `view_illegal` | `true`；目前主要支持 FB 渠道。 |
| 试玩广告有关联视频、有试玩关联视频 | `related_video` | `1`。 |

## 广告主、主页与落地页

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 指定广告主、查某个广告主 domain | `advertiser_key` | 字符串数组；最多前 20 个生效。 |
| 排除广告主、不看某广告主 | `exclude_advertiser_key` | 字符串数组；最多前 20 个生效。 |
| 指定创意 ID、指定 ad_key | `ad_key_list` | 字符串数组；最大长度 20。 |
| 包含主页信息、有主页信息 | `account_flag` | `true`。 |
| 落地页类型、APP 落地页 | `ads_promote_type` | `1`。 |
| 游戏/工具网站落地页、Web 落地页 | `ads_promote_type` | `2`。 |
| W2S | `ads_promote_type` | `2-1`。 |
| W2APK | `ads_promote_type` | `2-2`。 |
| 社交账号落地页 | `ads_promote_type` | `3`。 |
| 预约广告 | `is_preorder` | `1`。 |
| 非预约广告 | `is_preorder` | `2`。 |
| 不限制预约广告 | `is_preorder` | `0`。 |
| 有落地页快照、预约广告带落地页快照 | `landing_page` | `1`。 |
| 链接类型、重定向链接 | `redirect_filter_type` | `1`。 |
| DSP 平台链接、流量平台链接 | `redirect_filter_type` | `2`。 |
| 全部链接类型 | `redirect_filter_type` | `0`。 |
| 营销目标、CTA 类型、按钮类型 | `cta_type` | 转换为附录“营销目标”code。 |
| 广告版位、资源位、插屏、横幅、原生、激励视频等 | `ad_positions` | 转换为附录“广告版位”code。 |

## 去重、排序与 Top 创意

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 广告去重、按广告维度去重、默认去重 | `duplicate_removal` | `0`。 |
| 素材去重、按素材去重、智能去重 | `duplicate_removal` | `1`。 |
| 广告主去重、按广告主去重 | `duplicate_removal` | `2`。 |
| 按相关性排序、最相关 | `sort_field` | `-correlation`。 |
| 按展示估值排序、曝光最高、展现最高 | `sort_field` | `-impression`。 |
| 最新创意、按首次发现倒序 | `sort_field` | `-first_seen`。 |
| 最后看见、最近还在投 | `sort_field` | `-last_seen`。 |
| 投放天数最长 | `sort_field` | `-days`。 |
| 关联广告数最多 | `sort_field` | `-related_ads_count`。 |
| 热度最高、最热 | `sort_field` | `-heat_degree`。 |
| 点赞最多 | `sort_field` | `-like_count`。 |
| 评论最多 | `sort_field` | `-comment_count`。 |
| 分享最多 | `sort_field` | `-share_count`。 |
| 人气值 Top 1%、Top1% 创意、最头部创意 | `popularity_tag` | `[1]`。 |
| 人气值 Top 10%、Top10% 创意 | `popularity_tag` | `[10]`。 |
| 同时看 Top1% 和 Top10% | `popularity_tag` | `[1, 10]`。 |

## 互动、花费与受众画像

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 点赞数至少 N、点赞大于 N | `like_begin` | 整数。 |
| 点赞数最多 N、点赞小于 N | `like_end` | 整数。 |
| 评论数至少 N、评论大于 N | `comment_begin` | 整数。 |
| 评论数最多 N、评论小于 N | `comment_end` | 整数。 |
| 分享数至少 N、分享大于 N | `share_begin` | 整数。 |
| 分享数最多 N、分享小于 N | `share_end` | 整数。 |
| 广告花费至少 N 美元、FB 花费大于 N | `cost_begin` | 整数。 |
| 广告花费最多 N 美元、FB 花费小于 N | `cost_end` | 整数。 |
| 男性受众、男性占比、男 ≥50%、男 ≥75%、男 100% | `audience_sex` | `1`、`2`、`3` 分别表示男 ≥50%、男 ≥75%、男 100%。 |
| 女性受众、女性占比、女 ≥50%、女 ≥75%、女 100% | `audience_sex` | `4`、`5`、`6` 分别表示女 ≥50%、女 ≥75%、女 100%。 |
| 13-17 岁受众 | `audience_age` | `[1]`。 |
| 18-24 岁受众 | `audience_age` | `[2]`。 |
| 25-34 岁受众 | `audience_age` | `[3]`。 |
| 35-44 岁受众 | `audience_age` | `[4]`。 |
| 45-54 岁受众 | `audience_age` | `[5]`。 |
| 55-64 岁受众 | `audience_age` | `[6]`。 |
| 65 岁以上受众 | `audience_age` | `[7]`。 |

## 游戏类筛选

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 游戏分类、游戏标签、二级分类 | `tag_ids` | 转换为附录“分类/二级分类”code。 |
| 游戏玩法、玩法标签、解谜、战斗、收集等 | `game_play` | 转换为附录“游戏玩法”code。 |
| 游戏主题、题材、魔法、科幻、中世纪等 | `game_theme` | 转换为附录“游戏主题”code。 |
| 游戏 IP、宝可梦、迪士尼、火影等 | `game_ip` | 转换为附录“游戏 IP”code。 |
| 游戏核心赛道、超休闲、轻度、中度、重度 | `game_core_track` | 转换为附录“游戏核心赛道”code。 |
| 图片智能分析、旧版图片 AI 标签 | `ai_image_tag` | 已废弃；优先使用 `ai_tag_search`。 |
| 视频智能分析、旧版视频 AI 标签 | `ai_video_tag` | 已废弃；优先使用 `ai_tag_search`。 |
| 素材内容属性、AI 标签搜索、广告主题、人物信息、美术风格、营销卖点、玩家心理 | `ai_tag_search` | 转换为附录“素材内容属性”的 key 和标签 ID。 |
| 返回 AI 分析标签、带 AI 标签 | `include_ai_tags` | `true`。 |
| 每类 AI 标签返回 N 个 | `max_ai_tags_per_type` | 整数；仅 `include_ai_tags=true` 时生效。 |

## 工具类筛选

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 工具分类、工具标签、应用分类 | `tag_ids` | 转换为附录“分类/二级分类”code。 |
| AI APP、人工智能应用 | `is_ai_app` | `1`。 |
| 非 AI APP 或不限制 AI APP | `is_ai_app` | `0`。 |
| 短剧创意、短剧广告 | `is_theater` | `1`。 |
| 非短剧或不限制短剧 | `is_theater` | `0`。 |

## 电商类筛选

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 独立站、Shopify、WooCommerce、WordPress 等 | `independent_website` | 转换为附录“网站类型-独立网站”code。 |
| 电商平台、Amazon、Shopee、TikTok Shop、AliExpress 等 | `ecommerce_platform` | 转换为附录“网站类型-电商平台”code。 |
| 社交账号、Facebook 账号、Instagram 账号等 | `social_account` | 转换为附录“网站类型-社交账号”code。 |
| 货到付款、COD | `cod_flag` | `1`。 |
| 不限制货到付款 | `cod_flag` | `0`。 |
| 购物类落地页 | `landing_type` | `1`。 |
| 社交通讯类落地页 | `landing_type` | `2`。 |
| 不限制电商落地页类型 | `landing_type` | `0`。 |
| 搜索套利、套利类创意 | `search_arbitrage_flag` | `1`。 |
| 不限制搜索套利 | `search_arbitrage_flag` | `0`。 |

## 变现、CPI 与重投

| 用户表达/含义 | ZingAPI 字段 | 建议转换规则 |
| --- | --- | --- |
| 内购应用、IAP | `monetization_model` | `1`。 |
| 非内购应用、非 IAP | `monetization_model` | `2`。 |
| 不限制内购 | `monetization_model` | `0`。 |
| CPI 低于 0.5 | `cpi_price_amount` | `[1]`。 |
| CPI 在 0.5 到 1 之间 | `cpi_price_amount` | `[2]`。 |
| CPI 大于 1 | `cpi_price_amount` | `[3]`。 |
| CPI 币种美元 | `cpi_price_currency` | `["USD"]`。 |
| CPI 币种人民币 | `cpi_price_currency` | `["CNY"]`。 |
| 初次投放、首次投放 | `resume_or_new_ads` | `1`。 |
| 重复投放、重投广告 | `resume_or_new_ads` | `2`。 |
| 不限制重投 | `resume_or_new_ads` | `0`。 |

## 组合规则示例

| 用户表达 | 推荐请求体片段 |
| --- | --- |
| 查人气值 Top1% 的日本游戏视频创意 | `{"app_type":1,"geo":["JPN"],"ads_type":[2],"popularity_tag":[1]}` |
| 查 1920 x 1080 的视频素材 | `{"ads_type":[2],"material_size":["1920 x 1080"]}` |
| 查只投放日本的游戏素材 | `{"app_type":1,"geo":["JPN"],"complete_country_match":true}` |
| 查 Facebook 上女性 75% 以上的素材 | `{"platform":["facebook"],"audience_sex":[5]}` |
| 查有结束卡片的视频广告 | `{"ads_type":[2],"end_card":1}` |
