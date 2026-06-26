---
name: keplerjai-image-gen
description: 通过 ThinkZone AI 生成图片。当用户说「画图」「生图」「生成图片」「AI 绘图」「做一张图」「图生图」等时使用。支持 3 个图片模型（Gemini/MiniMax/Seedream）。
metadata: {
    "openclaw": {
      "emoji": "🖼️",
      "requires": {"env": ["THINKZONE_API_KEY"]},
      "primaryEnv": "THINKZONE_API_KEY"
    }
  }
---

# ThinkZone Image Generation

使用 ThinkZone AI 平台的 3 个指定模型生成图片。

## ⚠️ 调用流程（必读）

**当用户未指定模型时**，必须先反问用户要用哪个模型，再执行生成。可这样询问：

> 请问要用哪个模型？
> - **图片**：Gemini（多模态/参考图）、MiniMax Image 01（人物主体参考）、Seedream（轻量 2K/3K）

用户明确指定模型后，再调用对应脚本。

**当用户已指定模型**（如「用 Gemini 画」「MiniMax 生成」）时，直接执行，无需反问。

## 🎨 支持的模型（3 个）

### 图片生成模型（3 个）

| 模型 | Model ID | 说明 | 尺寸/分辨率 |
|------|----------|------|------|
| **Gemini 3.1 Flash Image Preview** | `gemini-3.1-flash-image-preview` | Google 多模态图像生成 | 0.5K, 1K, 2K, 4K |
| **MiniMax Image 01** | `image-01` | MiniMax 图片生成 | 自定义 512-2048px |
| **BytePlus Seedream 5.0 Lite** | `doubao-seedream-5-0-260128` | BytePlus 轻量版 | 2K, 3K |

## 🔧 配置

需要设置环境变量：
- `THINKZONE_API_KEY` - API 密钥
- `THINKZONE_BASE_URL` - API 基础 URL（可选，默认 `https://open.thinkzoneai.com`）

## 📸 图片生成使用

### Gemini 3.1 Flash Image Preview

```bash
# 基本用法
python3 {baseDir}/scripts/gen_image.py \
  --prompt "一只穿宇航服的虾" \
  --model "gemini-3.1-flash-image-preview"

# 指定分辨率和宽高比
python3 {baseDir}/scripts/gen_image.py \
  --prompt "科幻城市夜景" \
  --model "gemini-3.1-flash-image-preview" \
  --resolution "2K" \
  --aspect-ratio "16:9"

# 带参考图（支持多张，最多 10 张）
python3 {baseDir}/scripts/gen_image.py \
  --prompt "基于参考图生成" \
  --model "gemini-3.1-flash-image-preview" \
  --images "path/to/image1.jpg" "path/to/image2.jpg" \
  --resolution "1K"
```

**参数说明：**

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `--prompt` | 图像描述文本 | 必填 | - |
| `--model` | 模型名称 | `gemini-3.1-flash-image-preview` | 固定 |
| `--resolution` | 分辨率 | `1K` | `0.5K`, `1K`, `2K`, `4K` |
| `--aspect-ratio` | 宽高比 | `1:1` | `1:1`, `16:9`, `9:16`, `3:2`, `2:3`, `3:4`, `4:3`, `4:5`, `5:4`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1` |
| `--images` | 参考图路径（最多 10 张） | - | 图片路径 |
| `--thinking-level` | 思考等级 | `minimal` | `minimal`, `high` |
| `--output-dir` | 输出目录 | `./tmp/thinkzone-image` | 路径 |

### MiniMax Image 01

```bash
# 基本用法
python3 {baseDir}/scripts/gen_image.py \
  --prompt "一只可爱的猫咪" \
  --model "image-01"

# 指定宽高和数量
python3 {baseDir}/scripts/gen_image.py \
  --prompt "赛博朋克角色" \
  --model "image-01" \
  --width 1024 \
  --height 1024 \
  --n 4

# 图生图（人物主体参考）
python3 {baseDir}/scripts/gen_image.py \
  --prompt "穿古装的女性角色" \
  --model "image-01" \
  --subject-reference "path/to/character.jpg" \
  --aspect-ratio "3:4" \
  --watermark
```

**参数说明：**

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `--prompt` | 图像描述文本 | 必填 | - |
| `--model` | 模型名称 | `image-01` | 固定 |
| `--width` | 宽度像素 | `1024` | 512-2048（8 的倍数） |
| `--height` | 高度像素 | `1024` | 512-2048（8 的倍数） |
| `--aspect-ratio` | 宽高比 | `1:1` | `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `2:3`, `3:2` |
| `--n` | 生成数量 | `1` | 1-9 |
| `--subject-reference` | 人物主体参考图 | - | 图片路径 |
| `--watermark` | 是否添加水印 | `false` | `true`, `false` |

### BytePlus Seedream 5.0 Lite

```bash
# 基本用法
python3 {baseDir}/scripts/gen_image.py \
  --prompt "中国风山水画" \
  --model "doubao-seedream-5-0-260128"

# 指定尺寸和格式
python3 {baseDir}/scripts/gen_image.py \
  --prompt "高质量产品渲染图" \
  --model "doubao-seedream-5-0-260128" \
  --size "3K" \
  --output-format "png"

# 批量生成（最多 15 张）+ 参考图（最多 14 张）
python3 {baseDir}/scripts/gen_image.py \
  --prompt "基于参考图变体" \
  --model "doubao-seedream-5-0-260128" \
  --images "ref1.jpg" "ref2.jpg" \
  --size "2K" \
  --max-images 4 \
  --no-watermark
```

**参数说明：**

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `--prompt` | 图像描述文本 | 必填 | - |
| `--model` | 模型名称 | `seedream-5-0-260128` | 固定 |
| `--size` | 输出尺寸 | `2K` | `2K`, `3K` |
| `--output-format` | 输出格式 | `jpeg` | `jpeg`, `png` |
| `--max-images` | 最大生成数量 | `1` | 1-15 |
| `--images` | 参考图路径（最多 14 张） | - | 图片路径 |
| `--watermark` | 是否添加水印 | `false` | `true`, `false` |
| `--stream` | 流式输出 | `false` | `true`, `false` |

---

## 📋 前端调用参考（Vue 3）

参考 `campus-amags/tenant/src/views/workbench` 组件的调用方式：

### 图片生成调用示例

```typescript
import { 
  postImageGeneration,      // MiniMax Image 01
  postV3ImageGenerations,   // BytePlus Seedream
  postGeminiGenerateContent // Gemini 3.1 Flash
} from './api/image'

// MiniMax Image 01
const minimaxPayload = {
  model: 'image-01',
  prompt: '你的提示词',
  width: 1024,
  height: 1024,
  aspect_ratio: '1:1',
  n: 1,
  aigc_watermark: false,
  subject_reference: [{ type: 'character', image_file: 'base64_or_url' }]
}
const result = await postImageGeneration(minimaxPayload)

// BytePlus Seedream 5.0 Lite
const seedreamPayload = {
  model: 'doubao-seedream-5-0-260128',
  prompt: '你的提示词',
  size: '2K',
  output_format: 'jpeg',
  watermark: false,
  image: ['url1', 'url2'],  // 参考图
  sequential_image_generation: 'auto',
  sequential_image_generation_options: { max_images: 4 }
}
const result = await postV3ImageGenerations(seedreamPayload)

// Gemini 3.1 Flash Image Preview
const geminiPayload = {
  contents: [
    { parts: [{ text: '你的提示词' }] },
    { parts: selectedImages.map(img => ({ inlineData: { mimeType: 'image/jpeg', data: img.base64 } })) }
  ],
  generationConfig: {
    responseModalities: ['IMAGE'],
    imageConfig: {
      aspectRatio: '16:9',
      imageSize: '2K'
    },
    thinkingConfig: {
      thinkingLevel: 'minimal',
      includeThoughts: false
    }
  }
}
const result = await postGeminiGenerateContent(geminiPayload)
```

---

## ⚠️ 注意事项

1. **账户余额**：确保 ThinkZone AI 账户有足够余额
2. **图片尺寸限制**：
   - Gemini：分辨率 0.5K/1K/2K/4K
   - MiniMax：512-2048px（8 的倍数）
   - Seedream：2K/3K
3. **参考图限制**：
   - Gemini：最多 10 张
   - MiniMax：1 张（人物主体）
   - Seedream：最多 14 张
4. **超时处理**：图片生成建议预留约 120 秒

---

## 🔗 相关链接

- ThinkZone AI 平台：https://open.thinkzoneai.com
- 前端参考实现：`C:\Users\Linsihuan\Desktop\campus-amags\tenant\src\views\workbench`

---

*最后更新：2026-04-17*
