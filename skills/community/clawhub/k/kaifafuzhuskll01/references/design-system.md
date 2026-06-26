# Design System — PPT Generator

固化设计语言。所有布局模板引用此文档中的 CSS 变量。

---

## v3 母版配置参数

每份 PPT 通过 `master_config.json` 定义母版参数：

```json
{
  "theme_color": "#004D8C",
  "theme_accent": "#009688",
  "header_title": "数据安全合规培训",
  "show_footer": true,
  "footer_text": "内部资料，请勿外传",
  "bg_style": "gradient"
}
```

| 参数 | 说明 | 默认值 |
|------|------|-------|
| `theme_color` | 主色 | `#004D8C` |
| `theme_accent` | 强调色 | `#009688` |
| `header_title` | 母版标题栏文字 | 用户提供 |
| `show_footer` | 是否显示底部栏 | `true` |
| `footer_text` | 底部栏文字（版权等） | `""` |
| `bg_style` | 背景风格 | `"gradient"` |

### 母版 CSS 结构

```
.ppt-master
├── .ppt-master-header   → 标题栏（85px, 左侧蓝色图标方块 + 右侧灰色标题文字）
├── .content-area        → 内容区（flex:1, 每个 slide 注入不同 content-area 模板）
└── .ppt-master-footer   → 底部栏（40px, 页码 + 版权信息）
```

### 母版 CSS 变量

```css
:root {
  --color-primary: #004D8C;
  --color-primary-light: rgba(0,77,140,0.08);
  --color-primary-soft: rgba(0,77,140,0.12);
  --color-primary-mid: rgba(0,77,140,0.20);
  --color-primary-muted: rgba(0,77,140,0.6);
  --color-accent: #009688;
  --color-accent-light: rgba(0,150,136,0.08);
  --color-bg: #FFFFFF;
  --color-bg-alt: #f5f7fa;
  --color-bg-page: #f8f9fa;
  --color-text: #1a1a2e;
  --color-text-secondary: #64748b;
  --color-border: rgba(0,77,140,0.12);
  --font: 'Noto Sans SC', sans-serif;
  --header-height: 85px;
  --slide-width: 1280px;
  --slide-height: 720px;
}
```

以上变量在 `assets/base-template.html` 中定义，所有布局模板使用这些变量，不硬编码颜色。

---

## Content-Area 布局选择指南

### 可用布局

| 布局 | 用途 | 变量 |
|------|------|------|
| `ca-bullets` | 要点罗列，最常用 | `{{title}}`, `{{#each points}}`, `{{icon}}`, `{{#if highlight}}` |
| `ca-bullets-2col` | 双列对比 | `{{title}}`, `{{#each left_points}}`, `{{#each right_points}}` |
| `ca-cards-3` | 三列卡片 | `{{title}}`, `{{#each cards}}` (每卡: `card_title`, `icon`, `items[]`, `badge`, `label`) |
| `ca-cards-4` | 四列网格卡片 | 同上 |
| `ca-image-left` | 左图右文 | `{{title}}`, `{{image_icon}}`, `{{#each points}}`, `{{image_desc}}` |
| `ca-image-right` | 左文右图 | 同上 |
| `ca-architecture` | 架构/流程图 | `{{title}}`, `{{#each nodes}}` (每节点: `title`, `desc`), `{{note}}` |
| `ca-table` | 数据表格 | `{{title}}`, `{{#each headers}}`, `{{#each rows}}`, `{{note}}` |
| `ca-timeline` | 垂直时间线 | `{{title}}`, `{{#each events}}` (每事件: `time`, `title`, `desc`) |

### 选择逻辑

| 页面意图 | 推荐 layout |
|----------|-----------|
| 法规/要点罗列 | ca-bullets |
| 对比/并列 | ca-bullets-2col |
| 3 个方案/类型 | ca-cards-3 |
| 4 个方案/类型 | ca-cards-4 |
| 架构图/流程 | ca-architecture |
| 数据展示 | ca-table |
| 案例/截图说明 | ca-image-left / ca-image-right |
| 步骤/时间 | ca-timeline |

---

## 色彩（完整）

```css
:root {
  --color-primary: #004D8C;
  --color-primary-light: rgba(0, 77, 140, 0.08);
  --color-primary-soft: rgba(0, 77, 140, 0.12);
  --color-primary-mid: rgba(0, 77, 140, 0.20);
  --color-primary-muted: rgba(0, 77, 140, 0.6);
  --color-accent: #009688;
  --color-accent-light: rgba(0, 150, 136, 0.08);
  --color-dim: #3F51B5;
  --color-dim-light: rgba(63, 81, 181, 0.08);
  --color-bg: #FFFFFF;
  --color-bg-alt: #f5f7fa;
  --color-bg-page: #f8f9fa;
  --color-text: #1a1a2e;
  --color-text-secondary: #64748b;
  --color-text-muted: rgba(0, 77, 140, 0.5);
  --color-border: rgba(0, 77, 140, 0.12);
}
```

### 使用规则

- 主色 `.color-primary` 用于：标题文字、重要元素、强调色块、卡片标题
- 浅底 `.color-primary-light` 用于：卡片背景、标签背景、图标容器、高亮区域
- 边框 `.color-border` 用于：卡片边框、分割线、header/footer 边界
- 次级文字 `.color-text-secondary` 用于：辅助说明、描述文本、footer 文字、header title
- 强调色 `.color-accent` 用于：第二列标题 (ca-bullets-2col)、装饰元素
- **不要自行创造新颜色**。需要第二/第三强调色时用 accent

---

## 字体

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

:root {
  --font: 'Noto Sans SC', sans-serif;
}
```

### 层级

| 用途 | font-size | font-weight | 备注 |
|------|-----------|-------------|------|
| 页标题 | 40px | 700 | Header 左侧 |
| 英文副标题 | 24px | 300 | Header 右侧，opacity 0.6 |
| 章节大号 | 96px | 700 | 章节封面编号 |
| 段落标题 | 26px | 600 | 内容区 section title |
| 卡片标题 | 20px | 600 | 卡片内标题 |
| 正文 | 16px | 400 | 要点列表、段落 |
| 辅助文字 | 14-15px | 400 | 标签、脚注、来源 |
| 页码 | 14px | 400 | 底部页码 |

---

## 容器与间距

```css
.ppt-slide {
  width: 1280px;
  min-height: 720px;
  box-sizing: border-box;
  position: relative;
  background: var(--color-bg);
}

.ppt-header {
  height: 85px;
  display: flex;
  align-items: center;
  padding: 0 80px;
  border-bottom: 2px solid var(--color-primary-light);
  flex-shrink: 0;
}

.ppt-content {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 40px 80px;
}

.ppt-footer {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 80px;
  font-size: 14px;
  color: var(--color-primary-muted);
}
```

### 间距

- 页面左右 padding: 80px
- 内容区上下 padding: 40px
- 卡片间距: 24-32px (gap)
- 段落间距: 20-24px

---

## 卡片

```css
.ppt-card {
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: 16px;
  padding: 32px;
}

.ppt-card.featured {
  border: 3px solid var(--color-primary);
  position: relative;
}
```

---

## 标签 / Badge

```css
.ppt-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 16px;
  border-radius: 9999px;
  background: var(--color-primary-light);
  color: var(--color-primary);
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.ppt-badge.recommended {
  background: var(--color-primary);
  color: #fff;
}
```

---

## 图标

使用内嵌 SVG sprite，通过 `<svg><use href="icons.svg#icon-name"/></svg>` 引用。
图标容器为圆形：

```css
.ppt-icon-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--color-primary-light);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ppt-icon-circle svg {
  width: 28px;
  height: 28px;
  color: var(--color-primary);
}
```

---

## 推荐标签（章节封面/三栏卡片用）

```css
.ppt-recommend-badge {
  position: absolute;
  top: -12px;
  left: 24px;
  padding: 4px 16px;
  border-radius: 9999px;
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}
```

---

## 图表数据格式（给 Developer 子 agent 的输入）

### 雷达图
```json
{
  "labels": ["维度1", "维度2", "维度3", "维度4", "维度5"],
  "datasets": [
    { "label": "方案A", "data": [60, 85, 50, 55, 80], "color": "#004D8C" }
  ]
}
```

### 柱状图/进度条
```json
{
  "labels": ["Q1", "Q2", "Q3", "Q4"],
  "values": [65, 80, 55, 90],
  "color": "#004D8C",
  "label": "完成率 (%)"
}
```

---

## PPTX 排版参数

### 画布

| 参数 | 值 | 说明 |
|------|-----|------|
| slide_width | 13.333 inch | 16:9 宽屏 |
| slide_height | 7.5 inch | 16:9 宽屏 |
| margin | 0.8 inch | 页边距 |

### 字体

| 参数 | 值 | 说明 |
|------|-----|------|
| title_font_size | 32pt | 标题 |
| subtitle_font_size | 18pt | 副标题 |
| body_font_size | 14pt | 正文 |
| bullet_font_size | 12pt | 要点列表 |
| font_name | Noto Sans SC | 回退到 Microsoft YaHei |

### 颜色映射

| HTML 变量 | PPTX RGB |
|----------|---------|
| `--color-primary` (#004D8C) | RGB(0, 77, 140) |
| `--color-accent` (#009688) | RGB(0, 150, 136) |
| `--color-bg` (#FFFFFF) | RGB(255, 255, 255) |
| `--color-bg-alt` (#f5f7fa) | RGB(245, 247, 250) |
| `--color-text` (#1a1a2e) | RGB(26, 26, 46) |
| `--color-text-secondary` (#64748b) | RGB(100, 116, 139) |
| `--color-border` (rgba(0,77,140,0.12)) | RGB(0, 77, 140) 12% opacity |

### 图表说明

v1 阶段 PPTX 图表（chart-radar / chart-bar）暂用表格展示数据，v2 支持 python-pptx 原生图表。
