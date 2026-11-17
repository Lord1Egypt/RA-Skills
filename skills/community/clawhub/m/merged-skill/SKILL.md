---
name: merged-social-poster-skill
description: Generate professional social cards and magazine-style posters. Combines Guizang's Editorial/Swiss visual systems with magazine-poster templates. Use for 小红书图文, 公众号封面, magazine posters, social cards, carousel images, or any visual content needing high-quality rendering.
---

# Merged Social + Poster Skill

A combined skill merging **guizang-social-card** (Playwright rendering, 28 layouts, 10 themes) with **magazine-poster** (article illustrations, magazine-style HTML).

## Capabilities

| Feature | Source | Description |
|---------|--------|-------------|
| Playwright → PNG | guizang | 1080×1440 / 1080×1080 / 2100×900 |
| 28 Layout Recipes | guizang | Editorial M01-M16 + Swiss S01-S12 |
| 10 Theme Presets | guizang | 6 Editorial + 4 Swiss |
| Magazine Templates | magazine-poster | Article illustration system |
| Validation | guizang | 6-rule QA checklist |

## Workflow

1. **Intake** — platform, style, content, images
2. **Style Selection** — Editorial or Swiss, pick theme
3. **Layout** — Choose from 28 recipes or magazine templates
4. **Asset Prep** — Source images (Unsplash/Pexels/user)
5. **Compose** — HTML + CSS in single file
6. **Render** — `node render.mjs` → PNG
7. **QA** — Run `validate-social-deck.mjs` (optional)

## Quick Start

```
帮我基于这篇文章做一套瑞士风小红书图文，5张，IKB蓝。
```

```
做一个西安文旅的杂志风海报，森林墨主题。
```

```
把这篇产品测评做成公众号封面对：21:9 + 1:1。
```

## Theme Presets

### Editorial (6)
- **Ink Classic** `#0a0a0b` / `#f1efea` — 通用默认
- **Indigo Porcelain** `#0a1f3d` / `#f1f3f5` — 科技/AI
- **Forest Ink** `#1a2e1f` / `#f5f1e8` — 自然/户外
- **Kraft Paper** `#2a1e13` / `#eedfc7` — 怀旧/人文
- **Dune** `#1f1a14` / `#f0e6d2` — 艺术/设计
- **Midnight Ink** `#0e0d0c` / `#ece2cf` — 暗色/游戏

### Swiss (4)
- **IKB Klein Blue** — 科技/产品
- **Lemon** — 数据/教程
- **Lemon Green** — 健康/运动
- **Safety Orange** — 警示/活力

## File Structure

```
merged-skill/
├── SKILL.md                    # This file
├── assets/
│   ├── template-editorial-card.html
│   ├── template-swiss-card.html
│   └── magazine-templates/     # From magazine-poster
├── references/
│   ├── layout-recipes.md
│   ├── theme-presets.md
│   ├── style-system.md
│   └── ...
├── render.mjs                  # Playwright renderer
└── validate-social-deck.mjs    # QA validator
```

## Rendering

```bash
node render.mjs path/to/task-dir
```

Outputs PNG files to `output/` directory.

## Validation

```bash
node validate-social-deck.mjs path/to/task-dir
```

6 rules: overflow, type caps, footer collision, 4-band density, frame overflow, Swiss identity.