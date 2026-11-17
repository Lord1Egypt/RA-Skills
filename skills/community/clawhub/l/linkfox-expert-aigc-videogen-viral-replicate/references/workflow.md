# 业务流程详述：爆款视频复刻

## 业务目标

跨境电商运营给一条参考爆款视频和自己的商品素材，系统拆解参考视频的客观结构，再把产品相关内容替换成用户商品，生成一条保留原视频镜头骨架与节奏的新商品短视频。

本流程只做生成链路，不包含 Step 1b 运营深度报告。

## 核心公式

```text
爆款视频复刻 = 参考视频的分镜结构 / 视角 / 运镜 / 节奏 / 屏幕文字样式
             + 用户商品图 / 商品细节图与商品卖点
             + 销售国家与目标语言
             + 底层多参考图视频生成
```

“复刻”不是逐像素复制，而是保留已验证的镜头骨架和展示方式，替换商品、产品词、卖点，并按销售国家与目标语言改写口播和屏幕文字。

## 步骤拆解

| 编号 | 动作 | 上游 | 下游 | 调用能力 |
|------|------|------|------|----------|
| S1 | 校验入口与 URL | 用户输入 | S2/S3/S7 | 本 skill 编排逻辑 |
| S2 | 参考视频分镜分析 | S1 或上游 `video_analysis` | S4/S5 | `linkfox-aigc-textgen`，`imageUrls=[reference_video_url]`，`model=GEM_3_1_PRO` |
| S2F | 抽帧兜底分镜分析 | S2 失败 | S4/S5 | `extract_video_frames.py` -> `linkfox-file-upload` -> `linkfox-aigc-textgen`，`imageUrls=[frame_image_urls]`，`model=GEM_3_FLASH` |
| S3 | 商品图分析 | S1 | S5/S6/S7 | `linkfox-aigc-textgen` |
| S4 | 时长适配决策 | S2 + `target_duration` | S5/S7 | 本 skill 编排逻辑 |
| S5 | 高保真替换 prompt | S2/S3/S4 + 市场语言 | S6/S7 | `linkfox-aigc-textgen` |
| S6 | 视频 prompt 准备 | S5 + S3 | S7 | 本 skill 编排逻辑 |
| S7 | 多参考图视频生成 | S6 + 商品参考图列表 | 用户 | `linkfox-aigc-videogen-multi` |

## 主链路决策

### Step 1b 移除

Step 1b 是给运营看的爆款原因分析报告，不进入生成链。当前 skill 目标是生成复刻视频，因此不执行 Step 1b，也不把报告内容混入 Step 2。

### 视频理解调用契约

当前业务 skill 不直接调用视频理解 HTTP 接口。维护方已确认 `linkfox-aigc-textgen.imageUrls` 支持图片 URL 和视频 URL，因此参考视频分镜分析优先由 `linkfox-aigc-textgen` 直分析完成：

- `imageUrls=[reference_video_url]`
- `model=GEM_3_1_PRO`
- `thinkingLevel=low`
- `prompt=references/prompts.md#Step 1 v10`

若 textgen 返回视频不可读、媒体访问失败、`10005`、内容为空或其它明确的视频输入失败，必须进入标准抽帧兜底；不得将 MP4 URL 仅写入 prompt 后要求模型读取，不得通过模型切换做试探性重试，不得使用未文档化字段试探，例如 `videoUrl`、`videoUrls`、`referenceVideoUrl`。

### 抽帧兜底契约

抽帧兜底是正式链路的一部分，不是临时补洞。只允许使用本 skill 自带脚本 `scripts/extract_video_frames.py`：

1. 输入 `reference_video_url`，抽取 8-10 张按时间排序的 JPG 帧。
2. 保留脚本输出的 `frame_index_map`，其中包含每帧的序号、近似时间戳和本地路径。
3. 调用 `linkfox-file-upload` 上传这些 JPG 帧，得到 `frame_image_urls`。不要把 MP4 传给 `linkfox-file-upload`。
4. 调用 `linkfox-aigc-textgen`：
   - `imageUrls=[frame_image_urls]`
   - `model=GEM_3_FLASH`
   - `thinkingLevel=low`
   - `prompt=references/prompts.md#Step 1F Frame Fallback v1`
5. Step 1F 必须输出与 Step 1 v10 兼容的 `# 视频分镜脚本`，下游 S4/S5 不需要分支处理。

帧兜底不能听音频，因此口播只能来自可见字幕/OCR或画面可确定信息；无法确认时必须显式写“无可确认口播（frame fallback cannot hear audio）”，不能编造口播原文。

### 商品参考图策略

`product_image_url` 是主商品图，进入商品图分析和最终视频生成。`extra_product_image_urls` 只能放同一商品的补充图、细节图、不同角度图，默认不单独分析，只作为最终 `imageList` 的补充参考。模特图、人物图、场景图不进入本 skill。

### 最终视频生成策略

最终统一调用 `linkfox-aigc-videogen-multi`：

- `videoType=SEED` / `SEED_FAST`
- `imageList=[product_image_url, ...extra_product_image_urls]`
- `videoTime=resolved_duration_seconds`
- `prompt=seedance_prompt`
- `voice=generate_audio`
- `isPro=is_pro`
- `aspectRatio=ratio`
- `resolution=resolution`

如果用户要求切换为其它模型，说明本复刻链路当前只保留 Seedance/SEED 与 Seedance Fast/SEED_FAST 多参考图生成主路，不在本 skill 内保留其它分支。

## 已知局限

- 不解析社媒 URL，不下载无水印视频。
- 不做 Step 1b 报告。
- 不做模特图、人物图、场景图识别或分析；若上游有混合素材，必须先筛出商品图。
- 不直接调用网关 HTTP；参考视频直分析失败时只能使用标准抽帧兜底，而不是临时补实现。
