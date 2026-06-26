# Nano Banana Prompt Generator Skill

> 版本：1.0.0
> 用途：用户中文描述 → Nano Banana 图片生成的结构化 JSON 参数

---

## 触发词

生成图片提示词、生成 Nano Banana 参数、制作产品图、设计头像、设计 LOGO、生成海报、生成配图

> 只要用户描述了想要生成的图片内容，即触发此 Skill。

---

## 模型背景

**Nano Banana** 是 Google 的 Gemini 图片生成模型（gemini-3.1-flash-image），具有：
- 多模态理解（中英文提示词）
- 精确的文字渲染（支持中英双语）
- 快速生成（Flash 速度）
- 适合产品图、头像、LOGO、海报、社交媒体配图

**API 来源：**
- Google AI Studio：https://aistudio.google.com
- Vertex AI：`imagegeneration@latest`

---

## 工作流程

### Step 1：理解用户意图

从用户描述中提取：

| 字段 | 说明 | 来源 |
|------|------|------|
| `use_case` | 用例类型 | 从描述判断 |
| `subject` | 主体（人物/产品/文字/场景） | 用户描述 |
| `context` | 环境/背景 | 用户描述 |
| `style` | 视觉风格 | 用户指定或推断 |
| `colors` | 主色调 | 用户指定或推断 |
| `text_content` | 文字内容（如有） | 用户描述 |
| `aspect_ratio` | 画布比例 | 根据用例推断 |
| `language` | 文字语言 | 中文/英文/双语 |

### Step 2：分类用例

自动归类为以下四种之一：

| 用例 | 说明 | 默认比例 |
|------|------|---------|
| `product_display` | 产品展示海报 | 1:1 或 4:3 |
| `social_media` | 社交媒体配图 | 16:9 或 9:16 |
| `logo_design` | LOGO 设计 | 1:1 |
| `avatar` | 头像/肖像 | 1:1 |

### Step 3：生成结构化 JSON

输出标准 Nano Banana API 参数：

```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "...",
    "style": "...",
    "composition": "...",
    "lighting": "...",
    "mood": "..."
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "1:1",
    "outputFormat": "png",
    "safetySetting": "block_some",
    "personGeneration": "allow_adult"
  },
  "use_case": "...",
  "language_prompt": "...",
  "notes": "..."
}
```

### Step 4：输出给用户

**语言要求：**
- `prompt.text` → 英文（Nano Banana 英文效果最佳）
- `language_prompt` → 中文原意对照（便于用户理解）
- 如果包含文字，单独标注 `text_content` 字段

---

## 用例详细规范

### 1. 产品展示海报（product_display）

**触发词：** 产品图、产品海报、商品展示、电商主图

**Prompt 要素：**
```
[产品主体描述], on [背景/场景], [光照描述], [风格描述], product photography, high resolution, clean background
```

**默认参数：**
```json
{
  "use_case": "product_display",
  "parameters": {
    "aspectRatio": "1:1",
    "numberOfImages": 1
  }
}
```

---

### 2. 社交媒体配图（social_media）

**触发词：** 微博配图、小红书、Instagram、朋友圈、公众号封面

**Prompt 要素：**
```
[场景/主题描述], [情感氛围], [构图], [风格滤镜], social media photography, mobile wallpaper
```

**比例参考：**
- 微博/公众号封面：16:9
- 小红书/Instagram：1:1 或 4:5
- 朋友圈：9:16 或 1:1

---

### 3. LOGO 设计（logo_design）

**触发词：** LOGO、标志、品牌标识、图标

**Prompt 要素：**
```
[品牌名/概念描述], [行业属性], [风格：minimal/retro/tech/futuristic], [颜色], logo design, vector style, clean, professional
```

**文字处理：**
- 如果 LOGO 包含文字，`text_content` 字段单独输出
- Nano Banana 支持中英文字渲染，可直接写入 prompt

---

### 4. 头像/肖像（avatar）

**触发词：** 头像、个人照片、肖像、证件照

**Prompt 要素：**
```
[人物描述：性别/年龄/发型/表情/姿态], [背景：纯色/渐变/场景], [风格：realistic/cartoon/illustration], [光照], portrait photography, [用途]
```

---

## 风格参考表

| 风格 | 英文关键词 |
|------|-----------|
| 写实摄影 | realistic photography, high fidelity |
| 电影感 | cinematic, film still |
| 扁平插画 | flat illustration, vector art |
| 赛博朋克 | cyberpunk, neon lights |
| 复古 | retro vintage, 80s aesthetic |
| 极简 | minimalism, clean design |
| 油画 | oil painting, impressionist |
| 水彩 | watercolor style |
| 动漫 | anime style, manga |
| 像素 | pixel art, 8-bit |
| 3D 渲染 | 3D render, C4D |
| 中国风 | Chinese ink style, traditional |

---

## 输出格式模板

### 完整 JSON 输出示例

```json
{
  "model": "imagegeneration@latest",
  "prompt": {
    "text": "A minimalist product photography of a ceramic coffee mug on a white marble surface, soft natural lighting from the left, clean background, high resolution, studio quality",
    "style": "product photography, minimalist, clean",
    "composition": "centered product, 2/3 negative space",
    "lighting": "soft natural light, subtle shadow",
    "mood": "calm, modern, premium"
  },
  "parameters": {
    "numberOfImages": 1,
    "aspectRatio": "1:1",
    "outputFormat": "png",
    "safetySetting": "block_some",
    "personGeneration": "allow_adult"
  },
  "use_case": "product_display",
  "text_content": null,
  "language_prompt": "极简风格产品图：白色大理石台面上的陶瓷咖啡杯，左侧柔和自然光，高清干净背景",
  "notes": "建议搭配产品名 LOGO 或文字使用 Nano Banana 的文字渲染功能"
}
```

---

## 注意事项

1. **文字渲染：** Nano Banana 支持中英文文字，直接在 prompt 中写入即可
2. **比例选择：** 默认 1:1，社交媒体配图根据平台选择合适比例
3. **风格融合：** 可以组合多个风格（如 "cyberpunk + minimalist"）
4. **安全设置：** 默认 `block_some`，如需调整需明确说明
5. **输出语言：** prompt.text 始终输出英文，中文原意记录在 `language_prompt` 字段

---

## 参考资源

- Nano Banana API 文档：https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-flash-image
- Google AI Studio：https://aistudio.google.com
- Prompt 示例库：https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts
