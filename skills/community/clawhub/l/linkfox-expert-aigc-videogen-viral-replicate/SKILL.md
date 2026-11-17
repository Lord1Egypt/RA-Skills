---
name: linkfox-expert-aigc-videogen-viral-replicate
description: 爆款视频复刻，用参考爆款视频和用户商品素材，拆解原视频分镜与镜头语言，分析商品图，生成高保真替换后的视频 prompt，并委托底层视频生成 skill 产出复刻短视频。覆盖说法：爆款视频复刻、复刻爆款短视频、TikTok 爆款复刻、参考爆款视频做同款、用我的商品复刻这个视频、照着爆款做商品视频、viral video replication、replicate viral product video、clone TikTok ad structure、reference video to product video、remake hot video with my product。即使用户只说“照着这个视频给我的商品做一条”“把这个爆款模板套到我的商品”“做同款带货短视频”，也应触发本 skill；普通图转视频、带货口播方案生成、爆款图片复刻不在本范围。
---

# 爆款视频复刻

用一条参考爆款视频做“结构模板”，把视频里的商品相关内容替换为用户自己的商品，尽量保留原视频的分镜结构、视角、镜头运动、节奏、屏幕文字样式和商品展示逻辑，最终生成一条新的商品短视频。

本 skill 是编排型能力（Tier 2）：只负责输入校验、分镜/商品信息组织、时长适配、prompt 替换和底层 skill 调度。实际文本生成、视频生成、响应落盘和媒体下载必须委托底层能力，**本 skill 不直接调用网关 HTTP 接口、不直接处理网关鉴权**。参考视频直分析失败时，允许使用本 skill 自带的标准抽帧脚本生成帧图，再委托 `linkfox-file-upload` 和 `linkfox-aigc-textgen` 完成兜底分镜分析。

## 兼容性说明

需要可访问的参考视频 URL、商品图片 URL、`linkfox-aigc-textgen`、`linkfox-file-upload`、`linkfox-aigc-videogen-multi`；`linkfox-aigc-textgen.imageUrls` 支持传入图片 URL，运行环境支持视频 URL 时优先走直分析。若视频 URL 分析失败，本 skill 固定使用 `scripts/extract_video_frames.py` 抽帧并用 `GEM_3_FLASH` 分析帧图序列。本 skill 不包含 Step 1b 运营报告。

## 适用场景

| 场景 | 说明 |
|------|------|
| 参考爆款视频换商品 | 用户给一条 TikTok/Reels/Shorts/商品视频和自己的商品图，希望套用原视频结构生成新视频。 |
| 跨境短视频素材复刻 | 用户希望保留原视频的 hook、镜头节奏、运镜、字幕样式，用新商品和目标市场语言生成素材。 |
| Seedance 多商品图复刻 | 用户提供主商品图和可选商品细节图，作为 `linkfox-aigc-videogen-multi` 的参考图生成。 |

## 不适用

- 只把一张图片动起来、没有参考爆款视频：用 `linkfox-aigc-videogen-image-to-video`。
- 带货口播、真人自拍讲解、三套口播方案选择：用 `linkfox-aigc-videogen-sale`。
- 参照亚马逊 listing 图复刻商品图片：用 `linkfox-aigc-imagegen-bestseller-replicate`。
- 只分析爆款原因、只要运营报告：本 skill v1 不做 Step 1b。
- 视频剪辑、字幕后期包装、BGM 混音、片段拼接：需要独立剪辑/HyperFrames 类 skill。

## 输入参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `entry` | string | `viralReplica` | 入口保护字段，必须严格传 `viralReplica`。 |
| `reference_video_url` | string | - | 参考爆款视频 URL，必填；必须是 http(s) 可访问地址。 |
| `product_image_url` | string | - | 用户商品图 URL，必填；用于商品分析和最终视频生成参考图。 |
| `product_name` | string | 空 | 用户补充的商品名，进入商品图分析提示词。 |
| `product_desc` | string | 空 | 商品描述、卖点、使用场景补充。 |
| `usp` | string | 空 | 核心卖点；越具体，替换 prompt 越稳。 |
| `target_duration` | string | `Auto` | 目标视频时长：`Auto` / `5S` / `10S` / `15S`。 |
| `sales_country` | string | 空 | 销售国家/地区，使用下方固定枚举。 |
| `target_language` | string | 空 | 目标语言，使用下方固定枚举；未传则保持原视频语言。 |
| `extra_product_image_urls` | array[string] | `[]` | 额外商品图或商品细节图，按顺序追加到最终 `imageList`；不要放模特图或场景图。 |
| `videoType` | string | `seedance2.0` | 视频生成模型：`seedance2.0` / `seedance2.0fast`，最终分别映射到底层 `SEED` / `SEED_FAST`。 |
| `ratio` | string | `9:16` | 输出比例：`16:9` / `9:16` / `1:1` / `3:4` / `4:3` / `21:9`；最终会映射到 `linkfox-aigc-videogen-multi` 支持的比例。 |
| `resolution` | string | `720p` | 输出分辨率：seedance2.0 支持 `480p` / `720p` / `1080p`；seedance2.0fast 支持 `480p` / `720p`。 |
| `is_pro` | boolean | true | 高质量模式，传给底层多图视频 skill 的 `isPro`。 |
| `generate_audio` | boolean | true | 是否生成音频，传给底层多图视频 skill 的 `voice`。 |
| `video_analysis` | string | - | 可选：上游已完成的参考视频分镜分析文本。若未提供，必须调用 `linkfox-aigc-textgen` 分析 `reference_video_url` 获得。 |

销售国家/地区枚举：

`US(美国)` / `EU(欧洲)` / `JP(日本)` / `KR(韩国)` / `RU(俄罗斯)` / `UK(英国)` / `MX(墨西哥)` / `SEA(东南亚)` / `ASIA(亚洲)` / `LATAM(拉美)` / `GCC(中东)`

目标语言枚举：

`英语` / `中文` / `日语` / `俄语` / `意大利语` / `法语` / `西班牙语` / `德语` / `韩语` / `泰语` / `葡萄牙语` / `马来语` / `荷兰语` / `波兰语` / `瑞典语` / `土耳其语` / `其他语言`

目标时长枚举：

`Auto` / `5S` / `10S` / `15S`

## 底层能力依赖

| 阶段 | 底层能力 | 状态 | 说明 |
|------|----------|------|------|
| 参考视频分镜分析 | `linkfox-aigc-textgen` | 已有依赖 | `imageUrls` 支持图片 URL 和视频 URL；传 `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO`、`thinkingLevel=low`、Step 1 v10 prompt。 |
| 参考视频抽帧兜底 | `scripts/extract_video_frames.py` + `linkfox-file-upload` + `linkfox-aigc-textgen` | 标准兜底 | 仅当参考视频直分析失败、返回 10005、视频不可读、媒体访问失败或内容为空时触发；抽取 8-10 张有时间戳的 JPG，上传后传 `imageUrls=[frame_image_urls]`、`model=GEM_3_FLASH`、`thinkingLevel=low`、Step 1F prompt。 |
| 商品图分析 | `linkfox-aigc-textgen` | 已有依赖 | 传 `imageUrls=[product_image_url]`、`model=GEM_3_FLASH`、`thinkingLevel=low`。 |
| 替换后视频 prompt 生成 | `linkfox-aigc-textgen` | 已有依赖 | 传完整文本 prompt、`imageUrls=[]`、`model=GEM_3_FLASH`、`thinkingLevel=low`。 |
| 视频生成与媒体转存 | `linkfox-aigc-videogen-multi` | 已有依赖 | 传 `imageList=[product_image_url, ...extra_product_image_urls]`、`videoType=SEED/SEED_FAST`、`videoTime`、`prompt`、`voice`、`isPro`、`aspectRatio`、`resolution`。 |

## 流水线步骤

### 步骤 1：校验输入与准备素材 URL

- **输入**：`entry`、`reference_video_url`、`product_image_url`、`extra_product_image_urls`。
- **操作**：确认 `entry=viralReplica`；确认参考视频和图片都是 http(s) URL。本地文件必须先由前端/上游上传成可访问 URL。
- **输出**：`validated_inputs`、`product_reference_images=[product_image_url, ...extra_product_image_urls]`。
- **用途**：确保后续不会把本地路径或空 URL 传给底层 skill。

### 步骤 2：参考视频分镜分析

- **输入**：`reference_video_url`，或上游传入的 `video_analysis`。
- **操作**：
  1. 若已提供 `video_analysis`，直接进入步骤 3。
  2. 否则调用 skill `linkfox-aigc-textgen`（唯一调用方式，禁止直接调脚本或 HTTP），传入：
     - `imageUrls`: `[reference_video_url]`
     - `model`: `GEM_3_1_PRO`
     - `thinkingLevel`: `low`
     - `prompt`: `references/prompts.md` 的 `Step 1 v10` 提示词
  3. 从返回内容读取参考视频的视角、口播、画面描述、镜头语言、屏幕文字、时间码和运动归因，作为 `video_analysis`。
  4. 若 `linkfox-aigc-textgen` 返回视频 URL 不可读、媒体访问失败、`10005`、内容为空或其它明确的视频输入失败，进入步骤 2F 标准抽帧兜底；不得把视频 URL 只写进 prompt 后要求模型读取，不得试探未文档化字段。
- **输出**：`video_analysis`。
- **用途**：被步骤 4 的时长适配和步骤 5 的产品替换 prompt 消费。

### 步骤 2F：参考视频抽帧兜底分镜分析

- **触发条件**：步骤 2 的视频 URL 直分析失败，且未提供上游 `video_analysis`。
- **操作**：
  1. 使用本 skill 自带脚本 `scripts/extract_video_frames.py` 读取 `reference_video_url`，抽取 8-10 张按时间排序的 JPG 帧，输出 `frame_index_map`。
  2. 调用 `linkfox-file-upload` 上传这些 JPG 帧，得到 `frame_image_urls`；不得上传 MP4 到 `linkfox-file-upload`。
  3. 调用 skill `linkfox-aigc-textgen`，传入：
     - `imageUrls`: `frame_image_urls`，顺序必须和 `frame_index_map` 一致
     - `model`: `GEM_3_FLASH`
     - `thinkingLevel`: `low`
     - `prompt`: `references/prompts.md` 的 `Step 1F Frame Fallback v1` 提示词，填入 `frame_index_map`、帧数量和已知视频时长
  4. 从返回内容读取视角、画面描述、镜头语言、屏幕文字、估算时间码和运动归因，作为 `video_analysis`；同时记录 `video_analysis_source=frame_fallback`。
  5. 若抽帧脚本缺少 `ffmpeg` / `imageio-ffmpeg` 依赖、下载参考视频失败、帧图上传失败或帧序列分析为空，才停止执行并说明具体失败点。
- **输出**：`video_analysis`、`video_analysis_source=frame_fallback`、`frame_image_urls`、`frame_index_map`。
- **用途**：兜底产物必须保持 Step 1 v10 的输出格式，使步骤 4 和步骤 5 可无差别消费。

### 步骤 3：商品图分析

- **输入**：`product_image_url`、`product_name`、`product_desc`、`usp`。
- **操作**：调用 skill `linkfox-aigc-textgen`（唯一调用方式，禁止直接调脚本或 HTTP），传入：
  - `imageUrls`: `[product_image_url]`
  - `model`: `GEM_3_FLASH`
  - `thinkingLevel`: `low`
  - `prompt`: `references/prompts.md` 的 `Step 1.5 Product v1` 提示词，并追加商品名、描述和 USP。
- **输出**：`product_info`。
- **用途**：被步骤 5 替换原视频中的产品词、展示动作和卖点关键词。

### 步骤 4：时长适配决策

- **输入**：`video_analysis`、`target_duration`。
- **操作**：校验 `target_duration`；从 `video_analysis` 的视频时长或最后一个分镜时间码提取原视频时长，并解析 `resolved_duration_seconds`：
  - `5S` / `10S` / `15S` 分别解析为 5 / 10 / 15 秒。
  - `Auto` 根据原视频时长向上贴近 Seedance 档位：`<=5s` 取 5，`<=10s` 取 10，`<=15s` 取 15，`>15s` 取 15。
  - 原视频超出目标时长时，生成压缩或截取指令，避免强行塞入过长口播。
- **输出**：`resolved_duration_seconds`、`duration_strategy`、`duration_directive`。
- **用途**：被步骤 5 和步骤 7 消费。

### 步骤 5：生成高保真替换后的视频 prompt

- **输入**：`video_analysis`、`product_info`、`sales_country`、`target_language`、`duration_directive`。
- **操作**：调用 skill `linkfox-aigc-textgen`（唯一调用方式，禁止直接调脚本或 HTTP），传入：
  - `imageUrls`: `[]`
  - `model`: `GEM_3_FLASH`
  - `thinkingLevel`: `low`
  - `prompt`: `references/prompts.md` 的 `Step 2 v7`，填入视频分析、商品分析、市场语言指令和时长适配指令。
- **输出**：`step2_raw_output`、`video_prompt`。
- **用途**：`video_prompt` 进入步骤 6 检查，并最终提交给底层视频生成 skill。

### 步骤 6：视频 prompt 准备

- **输入**：`video_prompt`、`product_info`、`product_reference_images`。
- **操作**：不注入额外引用头，不改写 Step 2 模板。只做三件事：
  - 从 `product_info` 抽取“一句话产品全称”，检查 `video_prompt` 是否仍有清晰的新商品主体描述。
  - 确认 `product_reference_images` 的第一个元素是 `product_image_url`，后续只允许是同一商品的补充图或细节图。
  - 确认业务语义为参考商品图 + prompt 生成视频，不走首帧合成链路。
- **输出**：`seedance_prompt`、`product_reference_images`。
- **用途**：被步骤 7 传给 `linkfox-aigc-videogen-multi`。

### 步骤 7：调用底层多参考图视频 skill

- **输入**：`seedance_prompt`、`product_reference_images`、`resolved_duration_seconds`、`ratio`、`resolution`、`is_pro`、`generate_audio`。
- **操作**：调用 skill `linkfox-aigc-videogen-multi`（唯一调用方式，禁止直接调脚本、HTTP 或其它视频 skill），传入：
  - `imageList`: `product_reference_images`
  - `videoType`: `SEED` / `SEED_FAST`
  - `videoTime`: `resolved_duration_seconds`
  - `prompt`: `seedance_prompt`
  - `voice`: `generate_audio`
  - `isPro`: `is_pro`
  - `aspectRatio`: `ratio`；若底层只支持 `16:9` / `9:16`，则不支持的比例需先让用户重选。
  - `resolution`: `resolution`
- **输出**：底层 skill stdout；成功通常包含 `Saved full response: ["...mp4"]`，失败可能包含 `Saved full response: xxx.json` 或错误说明。
- **用途**：底层 skill 自行完成网关调用、响应落盘和视频下载，本 skill 不做二次包装、不截取、不重新输出。

### 步骤 8：交付

- **输入**：步骤 7 的底层 skill stdout。
- **操作**：成功时收集 `Saved full response:` 后的本地视频路径；失败时读取底层能力落盘 JSON 中的 `errcode` / `errmsg` / `error` / `status` / `errorMsg` 并做用户可读说明。若响应出现 `status=FAILED`，视为当前任务终态，不自动重试、不换模型、不重建任务；其中 `errorMsg` 为“图片审核不通过”或其它审核、侵权、人脸、明星/名人肖像相关失败时，立即停止；不得进入抽帧兜底、重新上传同一素材、换模型、换底层 skill、改 prompt 或继续调用工具绕过。
- **输出**：`media_paths` 或失败原因。
- **用途**：最终只展示本地 MP4 路径，不展示网关临时 URL。

## 输出规则

- 只展示 `media_paths` 中的本地视频路径。
- 不读取或输出 MP4/base64。
- 不把原始临时视频 URL 直接发给用户。
- 如果参考视频直分析失败，必须先按步骤 2F 使用标准抽帧兜底；只有标准兜底也失败时，才说明具体失败点。
- 图片审核不通过是最终视频生成阶段的终止型业务失败；只提示用户更换有授权、无明星/名人肖像或侵权风险的合规商品图。

## Prompt 与参考

- `references/prompts.md`：Step 1、Step 1.5、Step 2 的提示词契约。
- `references/api.md`：底层 skill 参数映射、已知能力缺口与已知局限。
- `references/workflow.md`：业务流程详述和关键取舍。
- `references/data-fields.md`：运行时字段来源、去向和下游消费关系。
- `scripts/extract_video_frames.py`：参考视频直分析失败时的标准抽帧工具。
- `examples/trial-prompts.md`：核心 / 边界 / 欠触发试跑提示词。
- `examples/test-cases.md`：正常用例、错误用例、覆盖点。

## 执行自检

每次流程结束前确认：

- [ ] 没有执行 Step 1b；本 skill 只做生成链路。
- [ ] `reference_video_url` 和 `product_image_url` 都是可访问 URL。
- [ ] 没有直接 HTTP 调网关；抽帧只使用 `scripts/extract_video_frames.py`，不临时写脚本。
- [ ] 若未提供 `video_analysis`，已先调用 `linkfox-aigc-textgen`，且 `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO`、`thinkingLevel=low`。
- [ ] 若视频 URL 直分析失败，已按步骤 2F 抽帧、上传帧图，并用 `GEM_3_FLASH` 分析 `frame_image_urls`。
- [ ] 没有通过 prompt 内嵌 MP4 URL、模型切换或未文档化字段探测视频理解。
- [ ] 商品图分析和 Step 2 prompt 替换均调用 `linkfox-aigc-textgen`。
- [ ] 最终视频生成调用 `linkfox-aigc-videogen-multi`，且 `videoType=SEED` 或 `SEED_FAST`。
- [ ] 参考图顺序为主商品图、额外商品图。
- [ ] 图片审核不通过时立即停止，并返回用户可读的合规换图提示；服务器繁忙等 `FAILED` 也不重试、不绕路。
- [ ] 成功结果由底层 skill 下载到会话 `media/`，用户只看到本地 MP4 路径。
