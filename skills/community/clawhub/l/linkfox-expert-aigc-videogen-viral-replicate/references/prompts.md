# Prompt 契约：爆款视频复刻

本文件记录当前 skill 使用的提示词契约。当前版本固定使用 `step1-v10`、`step1f-frame-fallback-v1`、`step15-v1`、`step2-v7`；维护者更新工程提示词时，应同步更新本文件后再发布 skill。

## 目录

- [Step 1 v10：参考视频分镜分析](#step-1-v10参考视频分镜分析)
- [Step 1F Frame Fallback v1：抽帧兜底分镜分析](#step-1f-frame-fallback-v1抽帧兜底分镜分析)
- [Step 1.5 Product v1：商品图分析](#step-15-product-v1商品图分析)
- [Step 2 v7：高保真替换 Prompt](#step-2-v7高保真替换-prompt)
- [Seedance 2.0 R2V 提交前约束](#seedance-20-r2v-提交前约束)

## Step 1 v10：参考视频分镜分析

使用方式：调用 `linkfox-aigc-textgen`，传 `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO`、`thinkingLevel=low`。`imageUrls` 支持图片 URL 和视频 URL；不要把视频 URL 只写进 prompt，也不要改用未文档化字段。

角色：专业电商短视频分析师。

目标：对上传的视频做逐镜头拆解，输出用于 Seedance 2.0 / Seedance 2.0 Fast R2V 生成的结构化分镜脚本。只输出生成所需的客观视觉信息，不做营销逻辑或爆款原因分析。

核心规则：

1. 先识别整条视频视角：`first-person POV`、`selfie overhead`、`third-person observer`、`over-shoulder`。
2. 视角判定必须依据画面实际可见内容：看得到躯干/腿/穿搭但看不到脸的高角度自拍，是 `selfie overhead`，不是 first-person POV。
3. 分镜按场景切换、镜头运动、人物动作、口播主题、产品展示角度、屏幕文字变化切割；一镜到底也按动作/口播/字幕变化拆。
4. 每个分镜输出：口播原文、中文翻译、英文画面描述、中文画面描述、镜头语言、屏幕文字、时间。
5. 屏幕文字只提取后期覆盖字幕/营销文案，不提取产品包装、招牌、T 恤印字等场景固有文字。
6. third-person / over-shoulder 且看得到脸时，画面描述必须写嘴部状态；有口播就写 speaking，无口播才写 silent/smiling。
7. 运动归因必须明确：相机动、主体动、两者都动、两者都不动。不要把“相机绕静止主体”写成“主体旋转”。
8. 输出中不要写营销分析、爆款原因、建议、评分、生成模型参数。

输出格式：

```markdown
# 视频分镜脚本

## 基本信息
- 视频时长：
- 产品类型：
- **视频视角：first-person POV / selfie overhead / third-person observer / over-the-shoulder**
- 分镜数量：

---

# 01

**口播原文：**
> ...

**中文翻译：**
> ...

**画面描述：**
> ...

**画面描述（中文）：**
> ...

**镜头语言：**
> 视角：... / 镜头类型：... / 运镜：... / 机位：...

**屏幕文字：**
> - 有无：yes / no
> - 文本原文：...
> - 文本中译：...
> - 屏幕位置：...
> - 视觉样式：...
> - 出现时段：full shot 或 MM:SS-MM:SS

**时间：** MM:SS~MM:SS
```

## Step 1F Frame Fallback v1：抽帧兜底分镜分析

使用方式：仅当 Step 1 v10 的参考视频 URL 直分析失败、返回 `10005`、视频不可读、媒体访问失败或内容为空时使用。先用 `scripts/extract_video_frames.py` 抽取 8-10 张按时间排序的 JPG 帧，再用 `linkfox-file-upload` 上传帧图。调用 `linkfox-aigc-textgen` 时传 `imageUrls=[frame_image_urls]`、`model=GEM_3_FLASH`、`thinkingLevel=low`。`imageUrls` 顺序必须与 `frame_index_map` 顺序一致。

角色：专业电商短视频帧序列分析师。

目标：你收到的是同一条参考视频按时间顺序抽取的关键帧图片，不是互不相关的商品图。请根据这些帧近似还原视频的分镜结构、视角、镜头运动、人物/手部动作、商品展示逻辑、屏幕文字和节奏，输出与 Step 1 v10 完全兼容的结构化分镜脚本，供 Seedance 2.0 / Seedance 2.0 Fast R2V 生成使用。

输入补充信息：

```text
帧数量：{frame_count}
已知视频时长：{source_video_duration}
帧索引与时间戳：
{frame_index_map}
```

核心规则：

1. 必须按 `imageUrls` 的顺序理解时间推进；不要把这些帧当成独立参考图。
2. 先识别整条视频视角：`first-person POV`、`selfie overhead`、`third-person observer`、`over-shoulder`。视角判定依据画面实际可见内容。
3. 分镜按明显的场景变化、人物/手部动作变化、商品展示角度变化、镜头距离变化、屏幕文字变化来切割；帧不足时以动作阶段切割，不要强行过度细分。
4. 每个分镜都要输出：口播原文、中文翻译、英文画面描述、中文画面描述、镜头语言、屏幕文字、时间。
5. 你不能听到音频。只有当画面中有可见字幕、可读口型内容或帧信息足以确认口播时，才写具体口播；否则口播原文写 `无可确认口播（frame fallback cannot hear audio）`，中文翻译写 `无可确认口播`。
6. 屏幕文字只提取后期覆盖字幕/营销文案，不提取产品包装、招牌、T 恤印字等场景固有文字。看不清时写可辨识部分并标注 `partially legible`。
7. 镜头运动必须基于相邻帧的构图变化推断，并明确运动归因：相机动、主体动、两者都动、两者都不动。证据不足时使用 `likely` / `可能`，不得把“相机绕静止主体”写成“主体旋转”。
8. 时间码按 `frame_index_map` 和已知视频时长估算。可以使用近似区间，但必须保持单调递增，不得编造超出视频时长的时间。
9. 输出中不要写营销分析、爆款原因、建议、评分、生成模型参数，也不要提到“我无法分析视频”。

输出格式必须与 Step 1 v10 一致：

```markdown
# 视频分镜脚本

## 基本信息
- 视频时长：
- 产品类型：
- **视频视角：first-person POV / selfie overhead / third-person observer / over-the-shoulder**
- 分镜数量：
- 分析来源：frame_fallback

---

# 01

**口播原文：**
> ...

**中文翻译：**
> ...

**画面描述：**
> ...

**画面描述（中文）：**
> ...

**镜头语言：**
> 视角：... / 镜头类型：... / 运镜：... / 机位：...

**屏幕文字：**
> - 有无：yes / no
> - 文本原文：...
> - 文本中译：...
> - 屏幕位置：...
> - 视觉样式：...
> - 出现时段：full shot 或 MM:SS-MM:SS

**时间：** MM:SS~MM:SS
```

## Step 1.5 Product v1：商品图分析

角色：电商产品视觉分析专家。

目标：根据商品图和用户补充信息，提取用于替换视频 prompt 中产品描述的字段。

输出结构：

```markdown
### 1. 基础信息
- **产品类型**：
- **品牌名称**：

### 2. 外观描述（用于替换视频 prompt 中的产品外观词）
- **整体颜色方案**：
- **外表面材质和质感**：
- **品牌标识描述**：
- **产品结构和形状**：
- **尺寸感**：
- **整体风格印象**：

### 3. 细节特征（用于替换功能演示镜头中的细节描述词）
- **顶部/正面特征**：
- **底部/背面特征**：
- **内部可见特征**：
- **独特视觉亮点**：

### 4. 英文描述短语（直接可用于 prompt 替换）
- **一句话产品全称**：
- **外观材质短语**：
- **核心视觉特征短语**：
- **内部特征短语**：
- **整体印象短语**：
```

第 4 部分最重要，Step 2 会优先消费这些短语，Seedance 提交前也用它检查新商品主体是否清晰。

## Step 2 v7：高保真替换 Prompt

角色：视频脚本适配专家。

任务：将原视频分镜脚本中的产品信息替换为新产品，同时最大程度保留原文；根据销售国家和目标语言做口播/字幕的市场语言适配；根据时长适配指令调整时间码和 Voiceover；把屏幕文字完整传递给生成模型。

核心原则：

1. 非产品相关句子必须逐词照抄 Step 1 原文，不改写、不压缩、不合并、不省略。包括视角/POV 起手句、镜头语言、背景、光线、动作节奏、非新产品物品、人物外貌。
2. 产品相关部分替换为新产品信息：产品名称、颜色、品牌、材质、外观特征、卖点关键词、细节特征。
3. 原视频展示动作不适合新产品时，替换为新产品的等价展示动作，保持描述丰富度和句式风格。
4. 口播必须与原视频对齐：原 Shot 无真实口播时，不输出 `Voiceover` 字段。
5. 产品类别/位置守恒：只替换与新产品同身体位置、同类别的物品。
6. 屏幕覆盖字幕必须传递；字幕里的品牌名、产品名、颜色、材质、卖点关键词也必须替换。非产品内容、位置、样式、出现时段保持原样。

销售国家与目标语言：

- `target_language`：所有有口播的 Shot 改写为目标语言；屏幕文字先替换产品词，再翻译；画面描述语言保持当前链路语言。
- `sales_country`：作为目标市场语境，影响口播措辞、计量/货币/CTA 语气；不要因此改变镜头骨架、人物动作或场景结构。
- 未提供 `target_language` 时，保持原视频语言；未提供 `sales_country` 时，保持原视频市场语境。
- `sales_country` 只使用固定枚举：`US(美国)` / `EU(欧洲)` / `JP(日本)` / `KR(韩国)` / `RU(俄罗斯)` / `UK(英国)` / `MX(墨西哥)` / `SEA(东南亚)` / `ASIA(亚洲)` / `LATAM(拉美)` / `GCC(中东)`。
- `target_language` 只使用固定枚举：`英语` / `中文` / `日语` / `俄语` / `意大利语` / `法语` / `西班牙语` / `德语` / `韩语` / `泰语` / `葡萄牙语` / `马来语` / `荷兰语` / `波兰语` / `瑞典语` / `土耳其语` / `其他语言`。

时长适配：

- 外部 `target_duration` 只能是 `Auto` / `5S` / `10S` / `15S`；Step 2 只接收上游解析后的 `duration_directive`。
- `passthrough`：时间码和 Voiceover 保持输入原样。
- `proportional_compress`：时间码按压缩比缩放；Voiceover 删减 filler、重复修饰和过渡赘语，保留 hook、核心卖点、CTA。
- `first_n_truncate`：后端先截 Step 1 分镜，Step 2 按 passthrough 处理。

输入插槽：

```text
原视频分镜分析：
{video_analysis}

新产品信息：
{product_info}

销售国家与目标语言：
{market_language_directive}

时长适配指令：
{duration_directive}
```

输出格式：

```markdown
### 第一步：列出所有替换项

| 原文 | 替换为 | 类型 |
|------|--------|------|

### 第二步：输出替换后的完整 prompt

[X-Ys] [替换后的画面描述]. Voiceover: "[目标语言口播]". A [style] caption at the [position] reads: "[已做产品替换的字幕文字]".
```

类型取值包括：`产品词`、`展示动作`、`卖点关键词`、`target-language`、`target-market`、`voiceover-compress`、`caption-product-replace`、`caption-translate`。

## Seedance 2.0 R2V 提交前约束

Step 2 输出的完整 prompt 原样作为 `seedance_prompt`。不要为了多参考图额外注入 `Reference`、`@Image1`、`Element` 等模型专属引用头。

提交前只做校验：

- `seedance_prompt` 中应包含新商品的一句话产品全称或等价清晰描述。
- `referenceImages` 的第一个元素必须是 `product_image_url`，其余元素只能是同一商品的补充图或细节图。
- 业务语义固定为 R2V；如果网关 schema 需要 `generationMode=multimodal`，它只是内部字段名。
- 不走首帧合成，不提交 `image2video`。
