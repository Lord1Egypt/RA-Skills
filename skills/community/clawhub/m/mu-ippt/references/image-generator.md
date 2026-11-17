# Image_Generator 参考手册

> 本文件是 Image_Generator 角色的精简参考。通用标准（SVG 技术约束、画布格式、后处理流水线等）请参阅 [shared-standards.md](./shared-standards.md)。

## 核心使命

接收 Strategist 输出的"设计规范与内容大纲"中的"图片资源清单"，为每张待生成的图片创建优化 prompt，通过 AI 工具生成图片，并保存到项目的 `images/` 目录。

**触发条件**：需要 AI 图片生成时（独立使用或在流水线中被调用）

| 模式 | 触发方式 | 说明 |
|------|---------|------|
| **独立模式** | 直接描述图片需求 | 生成单张或多张 AI 图片 |
| **流水线模式** | `generate-ppt` 中选择了 AI 图片生成 | 为项目批量生成图片素材 |

> 流水线中的下一步：Executor 生成 SVG

---

## 1. 输入与输出

### 输入

- **设计规范与内容大纲**（来自 Strategist）：项目主题、目标受众、设计风格、配色方案、画布格式
- **图片资源清单**（核心输入）：

  | Filename | Dimensions | Purpose | Type | Status | Generation Description |
  |----------|-----------|---------|------|--------|----------------------|
  | cover_bg.png | 1920x1080 | 封面背景 | Background | Pending | 现代科技感抽象背景，深蓝渐变 |

### 输出

| 交付物 | 路径/说明 | 要求 |
|--------|-----------|------|
| Prompt 文档 | `project/images/image_prompts.md` | **必须**使用文件写入工具保存——不能只在对话中输出 |
| 优化后的 prompt | 每张图片独立 prompt | 可直接用于 AI 图片生成工具；同时用作 alt text |
| 图片文件 | `project/images/` 目录 | 按资源清单中的文件名命名 |
| 更新后的清单 | 状态变更 | "Pending" → "Generated" |

---

## 2. 统一 Prompt 结构

### 2.1 标准输出格式

每张图片必须按以下格式输出：

```markdown
### Image N: {filename}

| Attribute | Value |
| --------- | ----- |
| Purpose   | {用于哪一页 / 什么功能} |
| Type      | {Background / Illustration / Photography / Diagram / Decorative} |
| Dimensions | {width}x{height} ({aspect ratio}) |
| Original description | {用户在清单中提供的描述} |

**Prompt**:
{主体描述}, {风格指令}, {色彩指令}, {构图指令}, {质量指令}

**Negative Prompt**:
{需要排除的元素}

**Alt Text**:
> {用于无障碍访问和图片说明的描述}
```

### 2.2 Prompt 组成部分

| 组成部分 | 说明 | 示例 |
|---------|------|------|
| 主体描述 | 核心内容 | `Abstract geometric shapes`、`Team collaboration scene` |
| 风格指令 | 视觉风格 | `flat design`、`3D isometric`、`watercolor style` |
| 色彩指令 | 配色方案 | `color palette: navy blue (#1E3A5F), gold (#D4AF37)` |
| 构图指令 | 布局比例 | `16:9 aspect ratio`、`centered composition` |
| 质量指令 | 分辨率质量 | `high quality`、`4K resolution`、`sharp details` |
| 反向提示 | 排除元素 | `text, watermark, blurry, low quality` |

### 2.3 风格关键词速查表

| 设计风格 | 推荐图片风格 | 核心关键词 |
|---------|-------------|-----------|
| General Versatile | 现代插画、扁平设计 | `modern`, `flat design`, `gradient`, `vibrant colors` |
| General Consulting | 干净专业、商务风 | `professional`, `clean`, `corporate`, `minimalist` |
| Top Consulting | 高端极简、抽象几何 | `premium`, `sophisticated`, `geometric`, `abstract`, `elegant` |
| Technology / SaaS | 未来感、数字化 | `futuristic`, `digital`, `tech grid`, `circuit pattern`, `neon accents`, `dark background` |
| Education / Training | 友好、教学型 | `friendly`, `instructional`, `whiteboard style`, `pastel colors`, `simple shapes` |
| Marketing / Branding | 大胆、有活力 | `bold`, `energetic`, `dynamic composition`, `vivid colors`, `action-oriented` |
| Healthcare / Medical | 干净、令人安心 | `clean`, `clinical`, `soft blue-green palette`, `organic curves`, `reassuring` |
| Finance / Banking | 稳重、可信赖 | `conservative`, `trustworthy`, `blue-gray palette`, `structured`, `precise` |
| Creative / Design | 艺术感、实验性 | `artistic`, `experimental`, `asymmetric`, `textured`, `hand-crafted feel` |

### 2.4 色彩整合方法

从设计规范中提取颜色，转换为 prompt 指令：

```
Primary: #1E3A5F (Deep Navy)  →  "deep navy blue (#1E3A5F)"
Secondary: #F8F9FA (Light Gray) →  "light gray (#F8F9FA)"
Accent: #D4AF37 (Gold)        →  "gold accent (#D4AF37)"

Full directive: "color palette: deep navy blue (#1E3A5F), light gray (#F8F9FA), gold accent (#D4AF37)"
```

### 2.5 画布格式与宽高比

| 画布格式 | 背景宽高比 | 推荐分辨率 |
|---------|-----------|-----------|
| PPT 16:9 | 16:9 | 1920x1080 或 2560x1440 |
| PPT 4:3 | 4:3 | 1600x1200 |
| 小红书 | 3:4 | 1242x1660 |
| 微信朋友圈 | 1:1 | 1080x1080 |
| Story | 9:16 | 1080x1920 |

> 支持的宽高比：`1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`4:5`、`5:4`、`9:16`、`16:9`、`21:9`（Gemini 还支持 `1:4`、`1:8`、`4:1`、`8:1`）

### 2.6 多图一致性策略

为同一套 PPT 生成多张图片时，视觉一致性至关重要。使用 **Deck Style Anchor**（套件风格锚点）——一段 15-25 词的共享前缀，添加到每张图片的 prompt 前面。

**构建方法**：将风格关键词（2.3 节）+ 色彩指令（2.4 节）+ 质量指令组合成一个可复用的前缀。

**示例**：
```
Deck Style Anchor:
"modern flat design illustration, color palette: deep navy (#1E3A5F), light gray (#F8F9FA), gold accent (#D4AF37), clean minimalist, high quality, 4K"

Image 1 prompt: [Deck Style Anchor], abstract technology network showing connected nodes...
Image 2 prompt: [Deck Style Anchor], team of professionals collaborating at a desk...
Image 3 prompt: [Deck Style Anchor], growth chart with upward trending line...
```

**例外**：背景图片可以将风格关键词替换为 `background`、`backdrop`、`negative space for text overlay`，同时保留相同的色彩指令。这样既能确保色彩一致性，又不影响背景的功能性。

**规则**：在 prompt 文档的头部（第 5 节）定义一次 Deck Style Anchor，然后在每个单独的 prompt 中引用它。

---

## 3. 图片类型分类与处理

### 类型判定流程

1. 全页/大面积背景 → **Background**（3.1）
2. 真实场景/人物/产品 → **Photography**（3.2）
3. 扁平/插画/卡通风格 → **Illustration**（3.3）
4. 流程/架构/关系图 → **Diagram**（3.4）
5. 局部装饰/纹理 → **Decorative Pattern**（3.5）

### 3.1 Background（背景）

**识别特征**：封面或章节页的全页背景；必须支持文字叠加

| 要点 | 说明 |
|------|------|
| 强调背景属性 | 添加 `background`、`backdrop` |
| 预留文字区域 | `negative space in center for text overlay` |
| 避免强主体 | 使用抽象、渐变、几何元素 |
| 低对比度细节 | `subtle`、`soft`、`muted` |

**模板**：`Abstract {主题元素} background, {风格} style, {主色} to {辅色} gradient, subtle {装饰元素}, clean negative space in center for text overlay, {宽高比} aspect ratio, high resolution, professional presentation background`

**Negative prompt**：`text, letters, watermark, faces, busy patterns, high contrast details`

### 3.2 Photography（摄影）

**识别特征**：真实场景、人物、产品、建筑——摄影级画质

| 要点 | 说明 |
|------|------|
| 强调真实感 | `photography`、`photorealistic`、`real photo` |
| 灯光效果 | `natural lighting`、`soft shadows`、`studio lighting` |
| 背景处理 | `white background` / `blurred background` / `contextual setting` |
| 人物多样性 | `diverse`、`professional attire` |

**模板**：`{主体描述}, professional photography, {灯光类型} lighting, {背景类型} background, color grading matching {配色方案}, high quality, sharp focus, 8K resolution`

**Negative prompt**：`watermark, text overlay, artificial, CGI, illustration, cartoon, distorted faces`

### 3.3 Illustration（插画）

**识别特征**：扁平设计、矢量风格、卡通、概念图

| 要点 | 说明 |
|------|------|
| 指定风格 | `flat design`、`isometric`、`vector style`、`hand-drawn` |
| 简化细节 | `simplified`、`clean lines`、`minimal details` |
| 统一配色 | 严格使用设计规范中的颜色 |
| 背景选择 | `white background` 或 `transparent background` |

**模板**：`{主体描述}, {插画风格} illustration style, {细节程度} with clean lines, color palette: {颜色列表}, {背景类型} background, professional {用途} illustration`

**Negative prompt**：`realistic, photography, 3D render, complex textures, watermark`

### 3.4 Diagram（图表）

**识别特征**：流程图、架构图、概念关系图、数据可视化

| 要点 | 说明 |
|------|------|
| 结构清晰 | `clear structure`、`organized layout`、`logical flow` |
| 连接表示 | `arrows indicating flow`、`connecting lines` |
| 学术/专业感 | `suitable for academic publication`、`professional diagram` |
| 浅色背景 | `white background` 或 `light gray background` |

**模板**：`{图表类型} diagram showing {内容描述}, {组件描述} connected by {连接方式}, {风格} style with {配色方案}, white background, clear labels, professional technical diagram`

**Negative prompt**：`cluttered, messy, overlapping elements, dark background, realistic, photography`

### 3.5 Decorative Pattern（装饰纹理）

**识别特征**：局部装饰、纹理、边框、分隔元素

| 要点 | 说明 |
|------|------|
| 可重复性 | `seamless`、`tileable`、`repeatable`（如需要） |
| 低调辅助 | `subtle`、`understated`、`supporting element` |
| 适合透明背景 | `transparent background` 或 `isolated element` |
| 小尺寸可读性 | 考虑缩小后的辨识度 |

**模板**：`{纹理类型} decorative pattern, {风格} style, {配色方案}, {背景类型} background, subtle and elegant, suitable for {用途}`

**Negative prompt**：`busy, cluttered, high contrast, distracting, photorealistic`

---

## 4. 图片生成工作流

### 4.1 分析阶段

1. 阅读设计规范，了解项目整体风格
2. 提取配色方案、画布格式、目标受众
3. 逐一分析资源清单中的每张图片
4. 判定每张图片的类型（参考第 3 节）

### 4.2 Prompt 生成阶段

对资源清单中每张 "Pending" 状态的图片：

1. **判定类型** → Background / Photography / Illustration / Diagram / Decorative
2. **理解用途** → 用在哪一页？什么功能？
3. **分析原始描述** → 用户在"Generation description"中提供的信息
4. **应用类型专属要点** → 参考对应类型的要点表
5. **生成优化 prompt** → 使用 2.1 标准输出格式
6. **保存 prompt 文档** → **必须**写入 `project/images/image_prompts.md`

### 4.3 图片生成阶段

> 前提条件：4.2 节必须完成；`images/image_prompts.md` 必须存在

#### 方法一：统一 CLI 工具（推荐）

```bash
python3 scripts/image_gen.py "your prompt" \
  --aspect_ratio 16:9 --image_size 1K \
  --output project/images --filename cover_bg
```

**参数说明**：

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `prompt` | - | 正向提示词（位置参数） | - |
| `--negative_prompt` | `-n` | 反向提示词 | None |
| `--aspect_ratio` | - | 图片宽高比 | `1:1` |
| `--image_size` | - | 尺寸（`1K`/`2K`/`4K`） | `1K` |
| `--output` | `-o` | 输出目录 | 当前目录 |
| `--filename` | `-f` | 输出文件名（不含扩展名） | 自动命名 |
| `--backend` | `-b` | 覆盖后端（`gemini`/`openai`/`stability`/`bfl`/`ideogram`/`qwen`/`zhipu`/`volcengine`/`siliconflow`/`fal`/`replicate`） | None |
| `--model` | `-m` | 模型名称 | 后端默认值 |
| `--list-backends` | - | 打印支持等级并退出 | `false` |

**配置来源**：
- 当前进程的环境变量
- 项目根目录的 `.env` 作为兜底

优先级：
- 当前进程环境变量优先
- `.env` 仅补充缺失的值

| 变量 | 是否必需 | 说明 |
|------|---------|------|
| `IMAGE_BACKEND` | 必需 | `gemini` / `openai` / `stability` / `bfl` / `ideogram` / `qwen` / `zhipu` / `volcengine` / `siliconflow` / `fal` / `replicate` |
| `{PROVIDER}_API_KEY` | 必需 | 服务商专属 API key，如 `GEMINI_API_KEY`、`ZHIPU_API_KEY` |
| `{PROVIDER}_BASE_URL` | 可选 | 服务商自定义端点 |
| `{PROVIDER}_MODEL` | 可选 | 服务商模型覆盖 |

> 仅使用服务商专属命名：`GEMINI_API_KEY`、`OPENAI_API_KEY`、`STABILITY_API_KEY`、`BFL_API_KEY`、`IDEOGRAM_API_KEY`、`QWEN_API_KEY` / `DASHSCOPE_API_KEY`、`ZHIPU_API_KEY` / `BIGMODEL_API_KEY`、`VOLCENGINE_API_KEY` / `ARK_API_KEY`、`SILICONFLOW_API_KEY`、`FAL_KEY` 和 `REPLICATE_API_TOKEN`。

> `IMAGE_API_KEY`、`IMAGE_MODEL` 和 `IMAGE_BASE_URL` 有意不予支持。

> 如果 `.env` 或当前环境中包含多个服务商配置，`IMAGE_BACKEND` 用于明确选择生效的那个。

**支持等级（推荐用法）**：
- 核心：`gemini`、`openai`、`qwen`、`zhipu`、`volcengine`
- 扩展：`stability`、`bfl`、`ideogram`
- 实验性：`siliconflow`、`fal`、`replicate`

**生成节奏控制（强制要求）**：
- 每次只执行一个生成命令；确认文件生成后再执行下一个
- 建议图片之间间隔 2-5 秒，避免并发失败
- 如果出现失败/无输出，暂停队列，检查 `IMAGE_BACKEND`、服务商凭证和输出目录，然后恢复

#### 方法二：自动生成

直接调用图片生成 API，下载并保存到 `project/images/` 目录。

#### 方法三：Gemini 网页端

1. 在 [Gemini](https://gemini.google.com/) 中生成图片
2. 选择 **Download full size** 获取高分辨率版本
3. 去水印：`python3 scripts/gemini_watermark_remover.py <image_path>`
4. 将处理后的图片放入 `project/images/` 目录

#### 方法四：手动生成（其他 AI 平台）

Prompt 已保存在 `images/image_prompts.md` 中；告知用户文件位置。用户在 Midjourney、DALL-E、Stable Diffusion 等平台生成图片，并放入 `project/images/` 目录。

### 4.4 验证阶段

- 确认所有图片已保存到 `images/` 目录
- 检查文件名是否与资源清单一致
- 将图片资源清单状态更新为 "Generated"

---

## 5. Prompt 文档模板

创建 `project/images/image_prompts.md` 时使用以下结构：

```markdown
# Image Generation Prompts

> Project: {project_name}
> Generated: {date}
> Color scheme: Primary {#HEX} | Secondary {#HEX} | Accent {#HEX}

---

## Image List Overview

| # | Filename | Type | Dimensions | Status |
|---|----------|------|-----------|--------|
| 1 | cover_bg.png | Background | 1920x1080 | Pending |

---

## Detailed Prompts

### Image 1: cover_bg.png

| Attribute | Value |
|-----------|-------|
| Purpose | Cover background |
| Type | Background |
| Dimensions | 1920x1080 (16:9) |
| Original description | Modern tech abstract background, deep blue gradient |

**Prompt**:
Abstract futuristic background with flowing digital waves...

**Alt Text**:
> Modern tech abstract background with deep blue gradient, digital waves, and particle effects

---

## Usage Instructions

1. Copy the "Prompt" above into an AI image generation tool
2. Recommended platforms: Midjourney / DALL-E 3 / Gemini / Stable Diffusion
3. Rename generated images to the corresponding filenames
4. Place in the `images/` directory
```

---

## 6. Negative Prompt 速查表

### 按图片类型

| 类型 | 推荐 Negative Prompt |
|------|---------------------|
| Background | `text, letters, watermark, faces, busy patterns, high contrast details` |
| Photography | `watermark, text overlay, artificial, CGI, illustration, cartoon, distorted faces` |
| Illustration | `realistic, photography, 3D render, complex textures, watermark` |
| Diagram | `cluttered, messy, overlapping elements, dark background, realistic` |
| Decorative pattern | `busy, cluttered, high contrast, distracting, photorealistic` |

### 通用 Negative Prompt

- **标准版**：`text, watermark, signature, blurry, distorted, low quality`
- **扩展版**（含人物场景）：`text, watermark, signature, blurry, low quality, distorted, extra fingers, mutated hands, poorly drawn face, bad anatomy, extra limbs, disfigured, deformed`

---

## 7. 常见问题

### 未提供"Generation Description"时的默认推断

| 用途 | 默认推断 |
|------|---------|
| 封面背景 | 抽象渐变背景，预留中央文字区域 |
| 章节页背景 | 简洁几何图案，单色调为主 |
| 团队介绍页 | 团队协作场景插画（扁平风格） |
| 数据展示页 | 简洁几何图案或纯色背景 |
| 产品展示 | 产品摄影风格，白色或渐变背景 |

### 图片效果不满意时

诊断问题类别，针对性修改 prompt：

| 问题 | 诊断 | Prompt 调整方式 |
|------|------|----------------|
| 风格不对 | 期望扁平设计但生成了写实图 | 修改风格指令：将 `photography` 替换为 `flat design illustration` |
| 颜色不对 | 颜色与设计规范不符 | 加强色彩指令：添加明确的 HEX 色值，重复颜色名称 |
| 构图不对 | 主体偏移或布局不适合幻灯片 | 调整构图指令：添加 `centered composition`、`rule of thirds` 或 `wide negative space on left` |
| 主体不对 | 图片描绘的内容与预期不符 | 重写主体描述，使用更具体和详细的描述 |
| 质量不佳 | 图片模糊、有伪影或缺乏细节 | 添加 `highly detailed, sharp focus, professional quality, 8K resolution` |

**变体工作流**：
1. 将原始 prompt 作为 "Variant A" 保留在 `image_prompts.md` 中
2. 根据上表的针对性修改创建 "Variant B"
3. 如有需要，用不同的风格方向创建 "Variant C"
4. 清晰标注所有变体，方便用户对比效果

---

## 8. 角色协作

### 与 Strategist 的交接

| 方向 | 内容 |
|------|------|
| 接收 | 设计规范与内容大纲（含图片资源清单） |
| 触发条件 | 用户在"图片使用方式"中选择了 "C) AI 生成" |
| 关键信息 | 配色方案、设计风格、画布格式 |

### 与 Executor 的交接

| 方向 | 内容 |
|------|------|
| 交付 | 所有图片放入 `project/images/` 目录 |
| Executor 引用方式 | `<image href="../images/xxx.png" .../>` |
| 路径说明 | SVG 在 `svg_output/`，图片在 `images/`；使用相对路径 `../images/` |

---

## 9. 任务完成检查清单

### 必须完成的事项

- [ ] 创建了 prompt 文档 `project/images/image_prompts.md`
- [ ] 每张图片包含：类型判定 + 优化 prompt + negative prompt + Alt Text
- [ ] 使用统一输出格式（2.1 标准格式）
- [ ] 阶段完成确认输出

### 图片就绪（至少满足一项）

- [ ] 所有图片已保存到 `project/images/` 目录
- [ ] 或：已明确告知用户使用 `image_prompts.md` 自行生成

### 流水线流转

- [ ] 提示用户进入下一步（切换到 Executor 角色）

> **关键检查**：如果 `images/image_prompts.md` 未创建，或输出格式不符合 2.1 标准，则任务未完成。

### 完成确认输出格式

```markdown
## Image_Generator 阶段完成

- [x] 创建了 prompt 文档 `project/images/image_prompts.md`
- [x] 为 X 张图片生成了优化 prompt
- [x] 所有图片已保存到 `images/` 目录
- [x] 已更新图片资源清单状态

**图片状态汇总**：

| Filename | Type | Dimensions | Status |
|----------|------|-----------|--------|
| cover_bg.png | Background | 1920x1080 | Generated |

**下一步**：切换到 Executor 角色开始 SVG 生成
```
