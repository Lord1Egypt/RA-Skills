# 生图 Prompt 基础框架

> 每次生成图片时，从这里读取基础框架，
> 然后加载当前风格的 prompt 片段，合并组装后传给 image_synthesize。

## 基础框架模板

```
Create a vertical (1080x1920px) {STYLE_NAME} knowledge card about '{TOPIC}'.

{STYLE_PROMPT_FRAGMENT}

=== LAYOUT (top to bottom) ===

[HEADER - top ~12%]
- Badge pill: '{DATE} · 知识卡片'
- Main title: '{MAIN_TITLE}' (large bold rounded hand-drawn font with white outline)
- Optional subtitle: '{SUBTITLE}'
- Cute cartoon mascot (lobster or relevant character) with stars
- Hand-drawn wavy divider

{CONTENT_BLOCKS}

[FOOTER]
- Decorative wave line
- Small mascot giving thumbs up

=== TECHNICAL REQUIREMENTS ===
- Resolution: 2K (2048px quality)
- Aspect ratio: 9:16
- Format: PNG
- Output file: /workspace/{OUTPUT_FILENAME}.png
```

## 内容区块组装规则

根据草稿内容类型，动态组装以下区块：

### 模块卡片区块
```
[CONTENT BLOCKS - module cards]
{ZONE_LABEL}
- {N} sticker cards in grid/flow layout:
  {CARD_1}
  {CARD_2}
  ...
- Each card: emoji icon + bold title + description + tag pills
- White rounded border, subtle shadow, hand-drawn arrows/connectors
```

### 流程区块
```
[WORKFLOW SECTION]
- Section label: '{WORKFLOW_TITLE}'
- {N} numbered step bubbles in flow pattern:
  {STEP_1} → {STEP_2} → ... → {STEP_N}
- Hand-drawn arrows, cute icons
```

### 特性对比区块
```
[FEATURES / COMPARISON]
- {N} feature cards in {GRID} layout
- Each: emoji + bold title + short description
- Color-coded by category
- Comparison boxes: ❌ vs ✅
```

## 输出流程

1. 读取 `references/draft-template.md` → 确认内容结构
2. 读取 `references/style-guide.md` → 确认当前风格定义
3. 读取 `assets/prompts/base_prompt.md` → 获取基础框架
4. 读取 `assets/prompts/style_prompts/{CURRENT_STYLE}.txt` → 获取风格 prompt
5. 组装完整 prompt → 调用 `image_synthesize` 生成图片
6. 调用 `upload_to_cdn` → 获取公开 URL
7. 调用 `message` (feishu) → 发送图片给用户
