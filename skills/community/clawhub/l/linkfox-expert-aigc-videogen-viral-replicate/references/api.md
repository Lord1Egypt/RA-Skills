# 爆款视频复刻底层能力映射

本页只描述 `linkfox-aigc-videogen-viral-replicate` 的编排参数与底层 skill 调用关系。实际鉴权、HTTP 请求、响应落盘、媒体下载由底层能力维护；本业务 skill 不直接调用网关。参考视频直分析失败时，本业务 skill 仅使用自带标准抽帧脚本做帧图兜底。

## 能力依赖

| 阶段 | 底层能力 | 入参要点 | 输出 |
|------|----------|----------|------|
| 参考视频分镜分析 | `linkfox-aigc-textgen` | `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO`、`thinkingLevel=low`、Step 1 v10 prompt | `video_analysis` |
| 参考视频抽帧兜底 | `scripts/extract_video_frames.py` + `linkfox-file-upload` + `linkfox-aigc-textgen` | 抽取 8-10 张 JPG；上传帧图；`imageUrls=[frame_image_urls]`、`model=GEM_3_FLASH`、`thinkingLevel=low`、Step 1F prompt | `video_analysis`、`frame_image_urls`、`frame_index_map` |
| 商品图分析 | `linkfox-aigc-textgen` | `imageUrls=[product_image_url]`、`model=GEM_3_FLASH`、`thinkingLevel=low`、Step 1.5 prompt | `product_info` |
| 替换后视频 prompt | `linkfox-aigc-textgen` | `imageUrls=[]`、`model=GEM_3_FLASH`、`thinkingLevel=low`、Step 2 prompt | `video_prompt` |
| 视频生成 | `linkfox-aigc-videogen-multi` | `videoType=SEED/SEED_FAST`、`imageList`、`videoTime`、`prompt` 等 | 本地 MP4 路径 |

## 视频理解调用契约

维护方已确认：`linkfox-aigc-textgen.imageUrls` 支持传递图片 URL 和视频 URL。参考视频分镜分析直接使用 `linkfox-aigc-textgen`：

- `imageUrls`: `[reference_video_url]`
- `model`: `GEM_3_1_PRO`
- `thinkingLevel`: `low`
- `prompt`: `references/prompts.md` 中 Step 1 v10

若该调用返回视频不可读、媒体访问失败、`10005`、内容为空或其它明确的视频输入失败，进入标准抽帧兜底；禁止在本业务 skill 中临时直连视频理解 HTTP 接口，或尝试未文档化字段，例如 `videoUrl`、`videoUrls`、`referenceVideoUrl`。

## `linkfox-aigc-textgen` 调用

### 参考视频分镜分析

传入：

- `imageUrls`: `[reference_video_url]`
- `model`: `GEM_3_1_PRO`
- `thinkingLevel`: `low`
- `prompt`: `references/prompts.md` 中 Step 1 v10

### 参考视频抽帧兜底分镜分析

触发：参考视频分镜分析返回视频输入失败、`10005`、媒体不可读或内容为空。

抽帧：

```bash
python scripts/extract_video_frames.py \
  --video "$reference_video_url" \
  --out-dir "$workspace_dir/data/reference_frames" \
  --frames 9
```

上传：调用 `linkfox-file-upload` 上传抽出的 JPG 帧，得到 `frame_image_urls`。只上传帧图，不上传 MP4。

textgen 传入：

- `imageUrls`: `frame_image_urls`
- `model`: `GEM_3_FLASH`
- `thinkingLevel`: `low`
- `prompt`: `references/prompts.md` 中 Step 1F Frame Fallback v1，填入：
  - `frame_count`
  - `source_video_duration`
  - `frame_index_map`

### 商品图分析

传入：

- `imageUrls`: `[product_image_url]`
- `model`: `GEM_3_FLASH`
- `thinkingLevel`: `low`
- `prompt`: `references/prompts.md` 中 Step 1.5 Product v1，并追加 `product_name`、`product_desc`、`usp`

### Prompt 替换

传入：

- `imageUrls`: `[]`
- `model`: `GEM_3_FLASH`
- `thinkingLevel`: `low`
- `prompt`: `references/prompts.md` 中 Step 2 v7，填入 `video_analysis`、`product_info`、`duration_directive`、`market_language_directive`

## `linkfox-aigc-videogen-multi` 调用

传入：

- `imageList`: `[product_image_url, ...extra_product_image_urls]`
- `videoType`: `SEED` / `SEED_FAST`
- `videoTime`: `resolved_duration_seconds`，只能是 `5` / `10` / `15`
- `prompt`: `seedance_prompt`
- `promptOptimizer`: `false`
- `isPro`: `is_pro`
- `voice`: `generate_audio`
- `aspectRatio`: `ratio`
- `resolution`: `resolution`

## 输出判定

- 成功：底层 `linkfox-aigc-videogen-multi` stdout 含 `Saved full response: ["...mp4"]`，本 skill 只展示本地视频路径。
- 失败：底层 stdout 含 `Saved full response: xxx.json` 或错误说明，按 `errcode` / `errmsg` / `error` 做用户可读解释。
- 禁止读取或输出 MP4/base64。
- 禁止把底层 API 临时 URL 直接给用户。

## 已知局限

- 参考视频直分析依赖运行环境对视频 URL 的支持；若不支持，走标准抽帧兜底。帧兜底无法听取音频，只能从画面、可见字幕和连续帧变化近似还原口播与节奏。
- `linkfox-aigc-videogen-multi` 当前公开参数不是原 Seedance R2V 网关的 `referenceImages/generationMode` schema，而是多参考图视频 skill 的 `imageList/videoType=SEED/SEED_FAST` schema。
- 本 skill 不接收模特图、人物图或场景图；若上游混传多张图，应先筛出商品图后再调用本 skill。
- 本 skill 不做 Step 1b 运营分析报告，也不做 MOS 打分。
- 本 skill 不负责下载 TikTok/Instagram/YouTube 链接；解析失败时应让用户上传视频文件或提供 CDN URL。
