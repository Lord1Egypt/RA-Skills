---
name: nano-banana-2
description: 使用 Nano Banana 2（Gemini 3.1 Flash Image）生成/编辑图片。支持文生图 + 图生图；512/1K/2K/4K 分辨率；14 种宽高比；最多 14 张输入图片；思考级别控制；使用 --input-image 编辑已有图片。
---

# Nano Banana 2 图片生成与编辑

使用 Google Nano Banana 2 API（Gemini 3.1 Flash Image Preview）生成新图片或编辑已有图片。

## 使用方法

使用绝对路径运行脚本（不要先 cd 到 skill 目录）：

**生成新图片：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "图片描述" --filename "output.png" [--model MODEL] [--resolution 512|1K|2K|4K] [--aspect-ratio RATIO] [--thinking-level minimal|high] [--image-only] [--api-key KEY]
```

**编辑已有图片：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "编辑指令" --filename "output.png" --input-image "path/to/input.png" [--model MODEL] [--resolution 512|1K|2K|4K] [--aspect-ratio RATIO] [--api-key KEY]
```

**多张输入图片（最多 14 张）：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "组合这些元素" --filename "output.png" --input-image "img1.png" "img2.png" "img3.png" [--model MODEL] [--resolution 2K] [--api-key KEY]
```

**重要：** 始终从用户当前工作目录运行，确保图片保存在用户工作的位置，而非 skill 目录。

## 默认工作流（草稿 → 迭代 → 定稿）

目标：快速迭代，在 prompt 确定之前不浪费时间在 4K 上。

- 草稿（1K）：快速反馈
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<草稿 prompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- 迭代：小幅调整 prompt；每次运行使用新文件名
  - 编辑模式下：每次迭代保持相同的 `--input-image`，直到满意为止。
- 定稿（4K）：仅在 prompt 确定后使用
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<最终 prompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## 模型选择

使用 `--model` 指定 Gemini 模型。默认值：`gemini-3.1-flash-image-preview`。

可用模型：

| 模型 ID | 别名 | 分辨率 | 宽高比 | 多图输入 | Thinking | Google Search Grounding | 特点 |
|---|---|---|---|---|---|---|---|
| `gemini-3.1-flash-image-preview` | Nano Banana 2 | 512 / 1K / 2K / 4K | 14 种（含 1:4, 4:1, 1:8, 8:1） | 最多 14 张（10 物体 + 4 角色） | minimal / high | Web Search + Image Search | 速度/质量/成本最佳平衡，默认推荐 |
| `gemini-3-pro-image-preview` | Nano Banana Pro | 1K / 2K / 4K | 10 种 | 最多 11 张（6 物体 + 5 角色） | 默认开启（不可关闭） | Web Search | 专业素材制作，高级推理，高保真文字渲染 |
| `gemini-2.5-flash-image` | Nano Banana | 仅 1K（1024px） | 9 种 | 最多 3 张 | 不支持 | 不支持 | 最快最便宜，适合高并发低延迟场景 |

用户请求映射：
- 默认 / 无偏好 → `gemini-3.1-flash-image-preview`
- "专业"、"最佳质量"、"pro" → `gemini-3-pro-image-preview`
- "快速"、"便宜"、"基础" → `gemini-2.5-flash-image`

## 分辨率选项

Gemini 3.1 Flash Image 支持四种分辨率（必须大写 K，512 除外）：

- **512**（0.5K）- 约 512px（最快，成本最低）
- **1K**（默认）- 约 1024px
- **2K** - 约 2048px
- **4K** - 约 4096px

用户请求与 API 参数映射：
- 未提及分辨率 → `1K`
- "缩略图"、"预览"、"0.5K"、"512" → `512`
- "低分辨率"、"1080"、"1080p"、"1K" → `1K`
- "2K"、"2048"、"普通"、"中等分辨率" → `2K`
- "高分辨率"、"高清"、"4K"、"超清" → `4K`

## 宽高比选项

支持 14 种宽高比，使用 `--aspect-ratio` 设置：

- **1:1** - 正方形（默认，无输入图片时）
- **1:4**、**4:1** - 极端竖版 / 横版（3.1 Flash 新增）
- **1:8**、**8:1** - 超极端竖版 / 横版（3.1 Flash 新增）
- **2:3**、**3:2** - 经典竖版 / 横版
- **3:4**、**4:3** - 标准照片竖版 / 横版
- **4:5**、**5:4** - Instagram 风格竖版 / 横版
- **9:16**、**16:9** - 手机竖屏 / 宽屏
- **21:9** - 超宽屏 / 电影画幅

用户请求映射：
- "正方形" → `1:1`
- "竖版"、"竖屏" → `3:4` 或 `9:16`
- "横版"、"横屏" → `4:3` 或 `16:9`
- "宽屏"、"电影画幅" → `16:9` 或 `21:9`
- "手机"、"故事"、"短视频" → `9:16`
- "横幅"、"超宽" → `21:9`
- "竖幅"、"竖条幅" → `1:4` 或 `1:8`
- "横条幅" → `4:1` 或 `8:1`

未指定 `--aspect-ratio` 时，模型默认匹配输入图片的宽高比，或文生图时使用 1:1。

## 思考级别

使用 `--thinking-level` 控制模型推理深度：

- **minimal**（默认）- 最快响应，最低延迟
- **high** - 最佳质量，模型对构图进行更深入的推理

复杂场景、精细构图或质量优先于速度时使用 `high`。模型内部始终会进行一定程度的思考，`minimal` 只是减少思考量。

## 多张输入图片

Nano Banana 2 单次请求最多支持 14 张参考图片：
- 最多 10 张物体图片（高保真度）
- 最多 4 张角色图片（保持角色一致性）

使用场景：
- **角色一致性**：提供角色参考图，生成不同姿势/角度
- **图片合成**：将多张图片的元素组合到一个场景中
- **风格迁移**：提供风格参考图 + 内容图
- **产品模型**：将产品放置在不同背景上
- **360° 视图**：通过提供之前的输出生成角色的不同角度

示例：
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "An office group photo of these people, they are making funny faces" \
  --input-image person1.png person2.png person3.png person4.png \
  --filename "2026-03-24-10-00-00-group-photo.png" \
  --resolution 2K --aspect-ratio 5:4
```

## 纯图片模式

使用 `--image-only` 抑制响应中的文本，仅返回生成的图片。不需要模型文本评论时使用。

```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "日落" --filename "sunset.png" --image-only
```

## API 密钥

脚本按以下顺序检查 API 密钥：
1. `--api-key` 参数（用户在聊天中提供的密钥）
2. `GEMINI_API_KEY` 环境变量

如果两者都不可用，脚本将报错退出。

## 预检 + 常见故障（快速修复）

- 预检：
  - `command -v uv`（必须存在）
  - `test -n "$GEMINI_API_KEY"`（或传入 `--api-key`）
  - 编辑模式下：`test -f "path/to/input.png"`

- 常见故障：
  - `Error: No API key provided.` → 设置 `GEMINI_API_KEY` 或传入 `--api-key`
  - `Error loading input image:` → 路径错误 / 文件不可读；确认 `--input-image` 指向真实图片
  - `Maximum 14 input images supported.` → 减少输入图片数量
  - "quota/permission/403" 类 API 错误 → 密钥错误、无权限或配额用尽；尝试其他密钥/账号

## 文件名生成

文件名格式：`yyyy-mm-dd-hh-mm-ss-name.png`

**格式：** `{时间戳}-{描述性名称}.png`
- 时间戳：当前日期时间，格式 `yyyy-mm-dd-hh-mm-ss`（24 小时制）
- 名称：小写英文描述，用连字符分隔
- 描述部分保持简洁（通常 1-5 个词）
- 根据用户 prompt 或对话上下文命名
- 不明确时使用随机标识符（如 `x9k2`、`a7b3`）

示例：
- Prompt "宁静的日式花园" → `2025-11-23-14-23-05-japanese-garden.png`
- Prompt "山上的日落" → `2025-11-23-15-30-12-sunset-mountains.png`
- Prompt "画一个机器人" → `2025-11-23-16-45-33-robot.png`
- 上下文不明确 → `2025-11-23-17-12-48-x9k2.png`

## 图片编辑

当用户想修改已有图片时：
1. 检查用户是否提供了图片路径或引用了当前目录中的图片
2. 使用 `--input-image` 参数指定图片路径
3. prompt 应包含编辑指令（如"让天空更有戏剧性"、"移除人物"、"改为卡通风格"）
4. 常见编辑任务：添加/移除元素、更改风格、调整颜色、模糊背景、语义修复（inpainting）、风格迁移、草图转照片等

## Prompt 处理

**生成模式：** 将用户的图片描述原样传入 `--prompt`。仅在明显不足时才重新组织。

**编辑模式：** 将编辑指令传入 `--prompt`（如"在天空中加一道彩虹"、"改成水彩画风格"）

两种模式下都要保留用户的创意意图。

## Prompt 模板（高命中率）

当用户描述模糊或编辑需要精确时使用模板。

- 生成模板：
  - "Create an image of: <主题>. Style: <风格>. Composition: <构图/镜头>. Lighting: <光线>. Background: <背景>. Color palette: <色调>. Avoid: <排除项>."

- 编辑模板（保留其他所有内容）：
  - "Change ONLY: <单一修改>. Keep identical: subject, composition/crop, pose, lighting, color palette, background, text, and overall style. Do not add new objects. If text exists, keep it unchanged."

- 写实模板：
  - "A photorealistic [镜头类型] of [主题], [动作或表情], set in [环境]. The scene is illuminated by [光线描述], creating a [氛围] atmosphere. Captured with a [相机/镜头细节], emphasizing [关键纹理和细节]."

- 语义修复模板（Inpainting）：
  - "Using the provided image, change only the [特定元素] to [新元素/描述]. Keep everything else in the image exactly the same, preserving the original style, lighting, and composition."

- 风格迁移模板：
  - "Transform the provided photograph of [主题] into the artistic style of [艺术家/艺术风格]. Preserve the original composition but render it with [风格元素描述]."

- 多图合成模板：
  - "Create a new image by combining the elements from the provided images. Take the [图1元素] and place it with/on the [图2元素]. The final image should be a [最终场景描述]."

## 输出

- 将 PNG 保存到当前目录（如果文件名包含目录则保存到指定路径）
- 脚本输出生成图片的完整路径
- **不要回读图片** - 只需告知用户保存路径
- 所有生成的图片都包含 SynthID 水印

## 示例

**生成新图片：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "宁静的日式花园，樱花盛开" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**编辑已有图片：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```

**宽屏电影画幅：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "悬崖上的史诗奇幻城堡，日落时分" --filename "2025-11-23-15-00-00-castle.png" --resolution 4K --aspect-ratio 21:9
```

**高质量深度思考：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "一张详细的信息图，将光合作用解释为一道食谱" --filename "2025-11-23-15-30-00-infographic.png" --resolution 2K --aspect-ratio 3:4 --thinking-level high
```

**组合多张图片：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "Create a professional e-commerce fashion photo. Put the dress from the first image on the model from the second image" --filename "2025-11-23-16-00-00-fashion.png" --input-image dress.png model.png --resolution 2K
```

**快速缩略图预览：**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "咖啡店 Logo，名为 The Daily Grind" --filename "2025-11-23-16-30-00-logo.png" --resolution 512 --aspect-ratio 1:1 --image-only
```
