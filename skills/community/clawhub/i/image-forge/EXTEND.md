# Image Forge 扩展指南 (EXTEND.md)

> 本指南说明如何向 image-forge 添加新风格、用途、后端和子技能。
> 核心原则：**只改 YAML，不改 SKILL.md 路由逻辑**。

---

## 当前库状态

| 资产 | 数量 | 质量说明 |
|------|------|---------|
| Signature 风格（YAML） | 10 种 | Sallyn 原创，有完整测试过的 prompt recipe |
| Rendering 风格（inline modifier） | 15 种 | 分类体系来自 YouMind/awesome-gpt-image-2，modifier 内容待进一步验证和丰富 |
| 用途 + references JSON | 11 类 | 来自 nano-banana/YouMind，有实际 prompt 示例 |
| 后端 | 2 个 | GPT Image 2 (CRS) + Gemini (Nano Banana 2) |

**待补充**：
- Rendering modifier 的实际 prompt 案例（从 awesome-gpt-image-2、EvoLinkAI 等 repo 导入）
- 更多 Signature 风格（如霓虹全息、磨砂玻璃、3D 黏土、吉卜力）
- logo/品牌类用途的完整接入

---

## 1. 添加 Rendering 风格（最轻量）

只需在 `styles/index.yaml` 的 `rendering_styles` 块添加一条：

```yaml
  - id: frosted-glass                     # 唯一 id，小写短横线
    category: material-render             # 类别（photo/illustration/3d/fine-art/print-art/minimal/digital-art/material-render）
    aliases: [磨砂玻璃, frosted glass, 毛玻璃, glassmorphism]  # 触发词
    modifier: "frosted glass material, translucent surface, soft blur behind glass, light refraction, clean modern aesthetic, studio lighting"
    preferred_backend: gpt-image-2        # gpt-image-2 / nano-banana-2
    tags: [glass, material, modern]
```

**prompt 来源参考**：
- [awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) — EvoLink 按用例整理的 GPT Image 2 案例
- [awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) — YouMind 1500+ 分类 prompt
- [awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) — Gemini 向 10000+ prompt

选一个代表性 case 的 prompt 精炼为 modifier（去掉主体描述，保留视觉语言部分）。

---

## 2. 添加 Signature 风格（有独立 YAML）

**Step 1**：新建 `styles/<id>.yaml`，参考已有文件格式：

```yaml
# styles/frosted-glass.yaml
id: frosted-glass
name: 磨砂玻璃
category: material-render
description: 磨砂玻璃质感，通透朦胧，现代高级感
prompt: |
  [在此处替换为您想要生成的主体内容]，frosted glass material,
  translucent surface with soft blur, subtle light caustics,
  clean studio background, minimalist composition, 
  photorealistic render, soft ambient lighting
placeholder: "[在此处替换为您想要生成的主体内容]"
aspect_ratio: "1:1"
preferred_backend: gpt-image-2
tags: [glass, material, premium, modern]
test_subject: "a smartphone floating above desk"   # 用于验证的主体
```

**Step 2**：在 `styles/index.yaml` 的 `signature_styles` 块添加条目：

```yaml
  - id: frosted-glass
    file: frosted-glass.yaml
    category: material-render
    aliases: [磨砂玻璃, frosted glass, 毛玻璃, glassmorphism]
    aspect_ratio: "1:1"
    preferred_backend: gpt-image-2
    tags: [glass, material, modern]
    use_case_affinity: [product-marketing, app-web-design, profile-avatar]
    avoid_for: []
```

**Step 3（可选）**：在 `use-cases/index.yaml` 相关用途的 `recommended_signature` 里加上新 id。

**验证**：用 test_subject 实际跑一次，确认 prompt 效果。

---

## 3. 添加用途（Use Case）

**Step 1**：创建 `references/<id>.json`，参考已有格式：

```json
[
  {
    "title": "Brand Logo Showcase — Dark Background",
    "prompt": "professional product showcase, dark studio background, dramatic lighting...",
    "tags": ["logo", "brand", "showcase", "dark"]
  },
  ...
]
```

**Step 2**：在 `use-cases/index.yaml` 添加条目：

```yaml
  - id: brand-logo
    label: "品牌 Logo / 展示图"
    aliases: [logo, 图标, 品牌, brand, 徽标, icon, 标志]
    references_file: "references/brand-logo.json"
    recommended_signature:
      - high-contrast-industrial
    recommended_rendering:
      - minimalism
      - 3d-render
      - photography
    default_backend: gpt-image-2
    default_size: "1024x1024"
    default_aspect: "1:1"
    special_note: "SVG logo 生成请使用专属 logo-generator skill"
```

---

## 4. 接入新后端（模型）

在 `backends.yaml` 的 `backends` 列表添加条目，设更高 `priority` 即可成为新默认：

```yaml
  - id: flux-ultra
    priority: 15          # 比 gpt-image-2 的 10 更高 → 成为新默认
    enabled: true
    description: "FLUX Ultra，极高写实细节"
    type: api
    endpoint: "https://..."
    auth_header: "Bearer $FLUX_API_KEY"
    default_size: "1024x1024"
    timeout_s: 120
    strong_at_rendering:
      - photography
      - 3d-render
    strong_at_use_cases:
      - product-marketing
      - ecommerce-main-image
```

**后端类型约定**：
- `crs`：通过本地 CRS 代理，用 `CRS_API_KEY`
- `gemini`：用 `generate_image.py` 脚本
- `api`：直接 HTTP，在 SKILL.md 的 Generation 节补充调用代码

---

## 5. 接入垂直子技能

**场景**：Lucien 分享了一个新的专属画图技能（如食品摄影专项、建筑可视化专项）

**接入方式一：用途路由引用**（推荐）

在 `use-cases/index.yaml` 加一条新用途，`special_note` 字段说明有专属技能可用：

```yaml
  - id: food-photography
    label: "食品/美食摄影"
    aliases: [美食, 食品, 菜品, food, 餐饮摄影]
    references_file: "references/food-photography.json"
    recommended_rendering: [photography, 3d-render]
    default_backend: gpt-image-2
    default_size: "1024x1024"
    special_note: "如有 food-photo-skill 则优先加载专属技能"
```

**接入方式二：独立技能保持，image-forge 做意图识别**

image-forge 识别到特定意图时，在回复里推荐切换专属技能：
```
用户说"帮我做一个 App 的 icon"
→ image-forge 可以生成，但如果识别到 logo-generator skill 存在
→ 回复："这个场景有专属的 logo-generator skill，可以生成 SVG 格式并配高端展示图，
        是否切换？或者我直接用 image-forge 画一张栅格图"
```

**接入方式三：Signature 风格 + 独立 references**

把新技能的精华 prompt 提炼为 Signature 风格 YAML 加入 image-forge，
同时保留原技能做深度使用（当用户需要完整工作流时）。

---

## 6. 从高星 Repo 批量导入 Prompt

**推荐流程**：

```bash
# 1. 下载目标 repo 的 JSON
curl -s "https://raw.githubusercontent.com/YouMind-OpenLab/awesome-gpt-image-2/main/..." \
  -o /tmp/source-prompts.json

# 2. 用脚本提炼为 references 格式（去掉主体，保留风格语言）
python3 scripts/import_prompts.py \
  --source /tmp/source-prompts.json \
  --category anime-manga \
  --output references/anime-manga-examples.json

# 3. 在 use-cases/index.yaml 对应条目加 examples_file 字段引用
```

**目前待导入的来源**：
- [ ] [EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) — 人像/海报/UI case
- [ ] [YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) — 15 个 style 分类的实际 prompt
- [ ] [YouMind-OpenLab/awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) — Gemini 向各类 prompt

---

## 快速扩容检查清单

```
新增 Rendering 风格：
  □ styles/index.yaml 加条目（id / aliases / modifier / preferred_backend）
  □ 用实际 prompt 验证 modifier 有效

新增 Signature 风格：
  □ 新建 styles/<id>.yaml
  □ styles/index.yaml 加条目
  □ （可选）相关 use-case 的 recommended_signature 加引用
  □ 实际生成一张验证

新增用途：
  □ references/<id>.json（5-10 条 prompt 示例）
  □ use-cases/index.yaml 加条目（含 recommended_styles + default_backend）

新增后端：
  □ backends.yaml 加条目（priority / endpoint / strong_at）
  □ SKILL.md Generation 节补充调用代码

接入子技能：
  □ use-cases/index.yaml 加引用条目 + special_note
  □ 或把核心 prompt 提炼为 Signature 风格
```
