# 字段汇总表：爆款视频复刻

## S1 输入校验

| 字段 | 中文 | 方向 | 来源/去向 |
|------|------|------|-----------|
| `entry` | 入口 | 输入 | 前端/调用方，必须为 `viralReplica` |
| `reference_video_url` | 参考爆款视频 | 输入 | 用户上传/URL -> S2 |
| `product_image_url` | 商品图 | 输入 | 用户上传 -> S3/S7 |
| `extra_product_image_urls` | 额外商品图 | 输入 | 商品细节图/多角度图 -> S7 |
| `product_reference_images` | 生成参考图列表 | 输出 | `[product_image_url, ...extra_product_image_urls]` -> S7 |
| `video_analysis` | 已有视频分析 | 可选输入 | 上游已分析时可直接传入，跳过 `linkfox-aigc-textgen` 参考视频分析 |

## S2 视频分镜分析

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| `video_analysis` | 分镜分析文本 | 输出 | `linkfox-aigc-textgen` 输出；传 `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO`，含基本信息、逐镜头口播、画面描述、镜头语言、屏幕文字、时间码 |
| `video_analysis_source` | 分析来源 | 输出 | `direct_video` 或 `frame_fallback`；直分析成功为 `direct_video`，抽帧兜底成功为 `frame_fallback` |
| `frame_image_urls` | 兜底帧图 URL | 兜底输出 | 仅 `frame_fallback` 时产生；由 `linkfox-file-upload` 上传 JPG 帧得到，按时间顺序传给 `linkfox-aigc-textgen` |
| `frame_index_map` | 兜底帧索引 | 兜底输出 | 由 `scripts/extract_video_frames.py` 输出，记录每张帧图的序号、近似时间戳和本地路径/文件名 |
| `original_duration` | 原视频时长 | 派生 | 从 `视频时长` 或最后一段时间码提取 |
| `shots[]` | 分镜段 | 派生 | 被 Step 2 逐段替换 |

## S3 商品图分析

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| `product_info` | 商品分析文本 | 输出 | `linkfox-aigc-textgen` 输出 |
| `product_full_name` | 一句话产品全称 | 派生 | 从第 4 部分抽取，用于 Step 2 替换和最终 prompt 检查 |
| `material_phrase` | 外观材质短语 | 派生 | 用于替换产品外观词 |
| `visual_feature_phrase` | 核心视觉特征短语 | 派生 | 用于替换特写和卖点锚点 |

## S4 时长适配

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| `target_duration` | 目标时长 | 输入 | `Auto` / `5S` / `10S` / `15S`；默认 `Auto` |
| `resolved_duration_seconds` | 解析后时长 | 派生 | 5 / 10 / 15 秒 -> S7 的 `videoTime` |
| `duration_strategy.mode` | 适配模式 | 输出 | `passthrough` / `proportional_compress` / `first_n_truncate` |
| `duration_directive` | Step 2 指令块 | 输出 | 告诉 Step 2 是否压缩时间码与 Voiceover |
| `sales_country` | 销售国家/目标市场 | 输入 | 用户选择 -> S5 |
| `target_language` | 目标语言 | 输入 | 用户选择 -> S5 |
| `market_language_directive` | 市场语言指令 | 派生 | 由 `sales_country` + `target_language` 组装，进入 Step 2 |

## S5 Step 2 prompt 替换

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| `step2_raw_output` | Step 2 原始输出 | 输出 | `linkfox-aigc-textgen` 输出，含替换项表和完整 prompt |
| `replacement_table` | 替换项表 | 派生 | 排查老产品词、字幕词、override 是否替换 |
| `video_prompt` | 视频生成 prompt | 输出 | 从第一个时间码开始抽取 -> S6/S7 |

## S6 prompt 准备

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| `seedance_prompt` | 最终视频 prompt | 输出 | 默认等于 `video_prompt`，仅做主体清晰度和商品参考图顺序检查 |
| `product_reference_images` | 商品参考图列表 | 输入 | 第一个必须为 `product_image_url` |

## S7 生成与交付

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| `imageList` | 底层视频参考图 | 输入 | 传给 `linkfox-aigc-videogen-multi` |
| `videoType` | 底层模型枚举 | 输入 | `SEED` / `SEED_FAST` |
| `videoTime` | 底层时长 | 输入 | 使用 `resolved_duration_seconds`，只能是 5 / 10 / 15 秒 |
| `prompt` | 底层视频提示词 | 输入 | 使用 `seedance_prompt` |
| `aspectRatio` | 输出比例 | 输入 | 来自 `ratio` |
| `resolution` | 输出分辨率 | 输入 | `720p` / `1080p`；默认 `720p` |
| `media_paths` | 本地视频路径 | 输出 | 由 `linkfox-aigc-videogen-multi` 返回并交付用户 |
