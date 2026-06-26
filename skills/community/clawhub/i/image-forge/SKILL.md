---
name: image-forge
description: |
  画图技能路由中枢（统一入口）。三维路由体系（用途 × 风格 × 主体），双后端调度。
  - Signature 风格：10 种有独立 YAML 的视觉方案（构成主义/克莱因/Risograph/故障艺术等）
  - Rendering 风格：15 种通用渲染技法 modifier（写真/动漫/3D/水彩/赛博朋克等），prompt 源自实战案例
  - Logo 展示背景：12 种专业展示场景（来源 logo-generator，已内化）
  - 用途库：12 类场景 + 全实战 prompt 案例，含推荐风格 + 后端默认
  - 后端调度：GPT Image 2（写实/产品/文字/4K）/ Gemini（动漫/艺术/多参考图）
  - 支持：文生图、风格库生图、参考图风格反推、参考图编辑、多参考图合成、logo 展示图
  Use when: 用户想画图/生图/做海报/插画/风格迁移/图片编辑/logo展示图 — 这是唯一的图像生成入口。
  【铁律】绝对禁止使用 image_generate 工具（configured: no，不可用）。所有画图请求必须走本 skill。
  【注意】SVG logo 代码生成 → 请用专属 logo-generator skill。
---

# Image Forge — 统一画图路由

## 目录结构

```
{baseDir}/
├── SKILL.md                     # 本文件（唯一用户入口）
├── backends.yaml                # 后端注册表 + 优先级 + 调度策略
├── styles/
│   ├── index.yaml               # 风格库（双层：10 Signature + 15 Rendering）
│   └── *.yaml                   # 10 个 Signature Style 独立文件
├── use-cases/
│   └── index.yaml               # 11 个用途 + 推荐风格 + 默认后端
├── references/                  # 用途提示词 JSON（11 个场景）
└── scripts/
    ├── reverse_style.py         # Gemini Vision 15 维风格反推
    └── generate_image.py        # Gemini/Nano Banana 2 生图
```

---

## 三维框架

```
用途（Use Case）× 风格（Style）× 主体（Subject）
      ↓                ↓               ↓
  结构指令          视觉语言         用户描述
 （布局/元素）  （色彩/技法/质感）   （画什么）
```

三者**独立路由**、**组合注入** prompt。用途和风格可以各自单独触发，也可以同时命中。

---

## 风格库：双层结构（读取 `styles/index.yaml`）

### Tier 1: Signature Styles（有独立 YAML，10 种）

高度具体的视觉方案，命中后加载对应 YAML 文件，默认走 `nano-banana-2`。

| 触发词示例 | 风格 id | 擅长用途 |
|-----------|---------|---------|
| 俄国构成主义、苏联海报、几何宣传 | constructivism | 海报、社媒 |
| 故障艺术、错位矩形、glitch | glitch-window-v1 | 头像、社媒 |
| 窗口重叠、数字拼贴 | glitch-window-v2 | 头像、社媒 |
| 混合媒介、线稿摄影 | mixed-media | 头像、海报 |
| 黑蓝红、三色极简剪影 | tri-color | 海报、封面 |
| 半调雕刻、铜版画、etching | engraving-halftone | 海报、头像 |
| risograph、半调杂志、印刷风 | risograph-magazine | 海报、社媒 |
| 波普水墨、pop art、ink splash | pop-ink-splash | 头像、社媒 |
| 克莱因蓝、克莱因秩序、极简仰拍 | klein-blue-order | 头像、社媒 |
| 高对比度工业、电光蓝故障 | high-contrast-industrial | 海报、产品、封面 |

### Tier 2: Rendering Styles（inline modifier，15 种）

通用渲染技法类别，命中后取 `modifier` 字段直接注入 prompt。按 `preferred_backend` 调度。

| 触发词示例 | 风格 id | 推荐后端 |
|-----------|---------|---------|
| 摄影、写真、真实照片 | photography | **GPT Image 2** |
| 电影感、胶片、cinematic | cinematic-film-still | **GPT Image 2** |
| 3D渲染、三维、CGI | 3d-render | **GPT Image 2** |
| 等距视角、isometric、2.5D | isometric | **GPT Image 2** |
| 复古、retro、vintage | retro-vintage | **GPT Image 2** |
| 赛博朋克、霓虹、cyberpunk | cyberpunk-sci-fi | **GPT Image 2** |
| 极简、minimalism、简约 | minimalism | **GPT Image 2** |
| 动漫、二次元、anime | anime-manga | Gemini |
| 插画、手绘插画 | illustration | Gemini |
| 素描、线稿、sketch | sketch-line-art | Gemini |
| Q版、chibi、可爱 | chibi-q-style | Gemini |
| 像素艺术、pixel art、8-bit | pixel-art | Gemini |
| 油画、古典油画 | oil-painting | Gemini |
| 水彩、aquarelle | watercolor | Gemini |
| 水墨、国画、中国画 | ink-chinese-style | Gemini |

---

## 用途库（读取 `use-cases/index.yaml`）

11 类场景，每类携带推荐风格和默认后端：

| 触发词 | use-case id | 默认后端 | 推荐 Rendering 风格 |
|--------|------------|---------|------------------|
| 海报、传单、poster | poster-flyer | **GPT Image 2** | cinematic, retro, cyberpunk |
| 头像、肖像、avatar | profile-avatar | Gemini | anime, illustration, photography |
| 产品图、营销图 | product-marketing | **GPT Image 2** | photography, 3d-render, minimalism |
| 电商、主图、白底 | ecommerce-main-image | **GPT Image 2** | photography, 3d-render |
| 视频封面、YouTube | youtube-thumbnail | **GPT Image 2** | cinematic, photography |
| 小红书、社交配图 | social-media-post | **GPT Image 2** | illustration, photography, watercolor |
| UI、App、网页 | app-web-design | **GPT Image 2** | 3d-render, isometric, minimalism |
| 漫画、分镜 | comic-storyboard | Gemini | anime-manga, illustration, sketch |
| 游戏素材、角色 | game-asset | Gemini | 3d-render, pixel-art, illustration |
| 信息图、教育图 | infographic-edu-visual | **GPT Image 2** | illustration, isometric, minimalism |

---

## 路由决策树（6 条路径）

```
用户输入
│
├── 有参考图 + "用这个风格"/"反推"
│   → [Path R] 风格反推：reverse_style.py → 提取风格 → 生成
│
├── 有参考图 + "修改"/"编辑"
│   → [Path E] 参考图编辑
│       1张图 → gpt-image-2 edit endpoint
│       2+张图 → nano-banana-2 多参考图
│
├── 命中 Signature Style aliases（构成主义/glitch/risograph…）
│   → [Path S] 加载 YAML → prompt recipe → nano-banana-2
│
├── 命中 Rendering Style aliases（动漫/写真/3D/水彩…）
│   → [Path R2] 取 modifier → 注入 prompt → 按 preferred_backend 调度
│
├── 命中用途关键词（海报/头像/电商…）
│   → [Path U] 加载 use-cases/index.yaml → 检索 references JSON
│       → 若无指定风格，展示推荐风格（可跳过直接生成）
│       → 按 use-case.default_backend
│
└── 直接描述主体，无信号
    → [Path D] 优化/翻译英文 → gpt-image-2（默认最高 priority）
```

---

## 后端调度决策（读取 `backends.yaml`）

```
1. 用户显式覆盖（最高优先级）
   "用 GPT 画"/"4K高清"/"写实" → gpt-image-2
   "用 Gemini 画"/"动漫"        → nano-banana-2

2. Style preferred_backend
   Signature 风格命中 → nano-banana-2（全部 10 种）
   Rendering 风格命中 → 按各风格的 preferred_backend（见上表）

3. Use-case default_backend
   无风格指定时，按用途默认后端

4. 全局默认
   gpt-image-2（priority 最高）
```

**GPT Image 2 强项**：写实摄影、产品展示、文字渲染、4K 高清、海报、UI  
**Gemini 强项**：动漫/插画/中国风/水彩/素描、多参考图合成、Signature 风格迁移

---

## [Generation] — 后端执行

### GPT Image 2（CRS 路由）

**推荐使用 wrapper 脚本**（支持 generate + edit，多图 edit，自动处理 base64）：
```bash
# 文生图
uv run {baseDir}/scripts/gpt_image2.py generate \
  --prompt "<prompt>" \
  --output /path/out.png \
  --size 1536x1024 \
  --quality high

# 改图（单张参考图）
uv run {baseDir}/scripts/gpt_image2.py edit \
  --prompt "<edit instruction>" \
  -i /path/ref.png \
  --output /path/out.png \
  --size 1024x1536

# 改图（多张参考图，最多 4 张）
uv run {baseDir}/scripts/gpt_image2.py edit \
  --prompt "<instruction>" \
  -i ref1.png -i ref2.png \
  --output /path/out.png
```

> **注意**：edit 接口不支持 `input_fidelity` 参数（已验证 2026-04-25）。

**Python API（内联使用）**：
```python
import os, requests, base64, time

CRS_BASE = os.environ.get('CRS_BASE_URL', 'http://127.0.0.1:8765')
CRS_KEY  = os.environ['CRS_API_KEY']

def gpt_image2_generate(prompt, size='1536x1024', quality='high',
                         output_format='png', filename=None):
    resp = requests.post(
        f'{CRS_BASE}/openai/v1/images/generations',
        headers={'Authorization': f'Bearer {CRS_KEY}'},
        json={'model': 'gpt-image-2', 'prompt': prompt, 'size': size,
              'quality': quality, 'output_format': output_format,
              'response_format': 'b64_json'},
        timeout=180,
    )
    data = resp.json()['data'][0]
    out = filename or f'/tmp/image-forge-{int(time.time())}.{output_format}'
    with open(out, 'wb') as f:
        f.write(base64.b64decode(data['b64_json']))
    return out, data.get('revised_prompt', '')

def gpt_image2_edit(prompt, image_path, size='1536x1024', quality='high',
                    output_format='png', filename=None):
    with open(image_path, 'rb') as f:
        b64_img = base64.b64encode(f.read()).decode()
    resp = requests.post(
        f'{CRS_BASE}/openai/v1/images/edits',
        headers={'Authorization': f'Bearer {CRS_KEY}'},
        json={'model': 'gpt-image-2', 'prompt': prompt,
              'images': [{'image_url': f'data:image/png;base64,{b64_img}'}],
              'size': size, 'quality': quality,
              'output_format': output_format, 'response_format': 'b64_json'},
        timeout=180,
    )
    data = resp.json()['data'][0]
    out = filename or f'/tmp/image-forge-edit-{int(time.time())}.{output_format}'
    with open(out, 'wb') as f:
        f.write(base64.b64decode(data['b64_json']))
    return out, data.get('revised_prompt', '')
```

**GPT Image 2 尺寸**：`1024x1024` / `1536x1024` / `1024x1536` / `2048x2048` / `3840x2160` (4K横) / `2160x3840` (4K竖)

### Gemini / Nano Banana 2

```bash
# 文生图
uv run {baseDir}/scripts/generate_image.py \
  --prompt "<optimized_english_prompt>" \
  --filename "~/.openclaw/workspace/tmp/image-forge/$(date +%Y-%m-%d-%H-%M-%S)-<slug>.png" \
  --aspect-ratio "<1:1|3:4|4:3|9:16|16:9>"

# 改图 / 多参考图合成（已实测 2026-04-25）
# Gemini 会在参考图基础上按 prompt 修改，多图合成/风格迁移尤其适合
uv run {baseDir}/scripts/generate_image.py \
  --prompt "<e.g.: keep character, change background to warm sunset>" \
  --filename "~/.openclaw/workspace/tmp/image-forge/$(date +%Y-%m-%d-%H-%M-%S)-<slug>.png" \
  -i "/path/to/ref1.jpg" -i "/path/to/ref2.jpg" \
  --aspect-ratio "3:4"
```

> **Gemini edit vs GPT Image 2 edit**
> - Gemini：多图合成、风格迁移更自由，但对原图布局保留能力较弱
> - GPT Image 2：保留原图布局/文字/边框精确修改时更强，推荐用于卡牌、产品展示图的约束性编辑

---

## Prompt 组合逻辑

```
Final Prompt =
  [Rendering Style modifier（如有）]
+ [Signature Style prompt（如有，替换主体后）]
+ [Use-case 结构指令（如有，从 references JSON 取）]
+ [用户主体描述（中→英翻译优化）]
+ [技术参数（lighting / composition / quality）]
```

- 中文输入全部翻译为英文后发给两个后端
- Signature Style prompt 已含完整视觉语言，Rendering modifier 作补充层
- 两者同时命中时：Signature 优先（更具体），Rendering 作辅助修饰

---

## 输出交付

- 保存目录：`~/.openclaw/workspace/tmp/image-forge/`
- 文件名：`YYYY-MM-DD-HH-MM-SS-<slug>.png`
- 回复：说明所选路径 + 后端 + 关键 prompt 要点，不读取二进制

### 渠道交付规则

| 渠道 | 交付方式 |
|------|--------|
| **飞书** | `message` tool + `filePath`（发送原生飞书图片消息） |
| Discord / 其他渠道 | `MEDIA: /absolute/path` （自动 inline） |

飞书交付示例：
```
message action=send filePath=/abs/path/to/image.png
```
【注意】一次生成多张图时，分次发送每张图片。

---

## 典型示例

```
# [Path D] 默认 GPT Image 2
"画一只在宇宙中游泳的猫"
→ gpt-image-2，size=1536x1024

# [Path S] Signature 风格 + Gemini
"帮我画一张俄国构成主义风格的 AI 机器人海报"
→ constructivism.yaml → nano-banana-2，aspect=3:4

# [Path R2] Rendering 风格 → 自动按强项调度
"帮我画一张动漫风格的城市夜景"
→ anime-manga modifier → nano-banana-2
"帮我画一张赛博朋克风城市"
→ cyberpunk-sci-fi modifier → gpt-image-2

# [Path U] 用途路由 + 推荐风格
"帮我做一张 YouTube 视频封面，科技感"
→ youtube-thumbnail.json → 推荐 cinematic/photography → gpt-image-2

# [Path U + R2] 用途 + 风格同时命中
"帮我做一张水彩风格的社交配图，主题是咖啡和阅读"
→ social-media-post + watercolor → nano-banana-2，aspect=1:1

# [Path E] 参考图编辑
1张图 + "改成极简风格" → gpt-image-2 edit endpoint
2张图 + "合成一张"    → nano-banana-2 (-i ref1 -i ref2)

# [Path R] 风格反推
1张图 + "用这个风格给我画一只猫" → reverse_style.py → gpt-image-2

# 显式后端覆盖
"用 Gemini 画一张产品图" → nano-banana-2（覆盖用途默认）
"4K高清画一张产品海报"  → gpt-image-2，size=3840x2160
```
