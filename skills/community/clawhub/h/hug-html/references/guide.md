# guide.md — hug-html 完整使用教程 (v2 网格架构)

HTML 网格化模块生成技能，支持可配置的 N×M 网格布局、单元格合并、双层模块体系。

---

## 快速开始

### 1. 查看所有可用基础模块

```bash
python "scripts/grid_builder.py" --list-modules
```

### 2. 查看所有内置模板

```bash
python "scripts/grid_builder.py" --list-templates
```

### 3. 从内置模板生成 HTML

```bash
# App 推广卡片
python "scripts/template_generator.py" --type harmony-app -o "data/output/my-card.html"

# 双端推广卡片
python "scripts/template_generator.py" --type harmony-dual -o "data/output/dual-card.html"

# 周历仪表板
python "scripts/template_generator.py" --type calendar-dashboard -o "data/output/calendar.html"
```

### 4. 从自定义 Grid Spec 生成

```bash
python "scripts/grid_builder.py" --spec "data/templates/3x3-merge.json" -o "data/output/3x3.html"
```

### 5. 生成可视化编辑界面

```bash
python "scripts/visual_editor.py" --template "data/output/my-card.html" -o "data/output/editor.html"
# 或用内置模板直接生成
python "scripts/visual_editor.py" --type harmony-app -o "data/output/editor.html"
# 打开后按 Ctrl+E 进入编辑模式
```

### 6. 内容填充

```bash
# 自动填充示例内容
python "scripts/content_filler.py" auto --template "data/output/template.html" --output "data/output/filled.html"

# 用 JSON 文件填充
python "scripts/content_filler.py" fill --template "data/output/template.html" --content "data/config/content.json" --output "data/output/final.html"
```

---

## 核心架构

### 四层体系

```
骨架 (Skeleton)
├── 骨架结构 — N×M 网格、行列数、单元格合并(rowspan/colspan)、gap间距
└── 骨架样式 — 底板背景/渐变/透明度、外阴影、外边框、圆角、内外边距

模块 (Modules)  ← 模块模板 = {模块结构 + 模块样式} 预置组合
├── 模块结构 — 复合模块的 HTML 骨架
└── 模块样式 — 模块级的视觉样式（由 base 模块提供）

基础 (Base/Primitives)
└── 基础样式 — 作用于具体文字/元素的 CSS 原语
```

### 两层级模块体系

```
基础模块 (base)      →    复合模块 (composite)     →    放入网格格子
CSS 原语                  可复用 HTML 组件
─────────────────────────────────────────────────────
font-size-xl               header-entity
color-dark                 main-title
bg-glass                   qr-card / qr-dual
radius-xl                  feature-panel
shadow-glass               comms-panel
img-circle                 footer-caption
flex-center                text-block / text-img-right
...                        param-panel / data-table / stat-card
```

### Grid Spec 格式

```json
{
  "name": "模板名称",
  "desc": "描述",
  "card_style": {
    "max_width": "400px",
    "bg": "rgba(255,255,255,0.82)",
    "border_radius": "36px",
    "padding": "24px 20px"
  },
  "grid": {
    "rows": 6,
    "cols": 1,
    "gap": "0",
    "cells": [
      {"id": "header", "row": 0, "col": 0, "module": "composite:header-entity"},
      {"id": "merged", "row": 1, "col": 0, "colspan": 2, "rowspan": 2,
       "module": "composite:feature-panel", "style": {"background": "#f5f5f5"}},
      {"id": "custom", "row": 2, "col": 0, "colspan": 3,
       "html": "<div data-field='custom'>自定义HTML内容</div>"}
    ]
  }
}
```

### 单元格合并

通过 `colspan` 和 `rowspan` 实现合并效果：
- `colspan: 2` — 跨 2 列
- `rowspan: 2` — 跨 2 行
- 两者同时使用 — 跨 2 列 2 行

---

## 内置模板列表

| 模板名 | 来源 | 网格 | 说明 |
|--------|------|------|------|
| `harmony-app` | 刻在石头上 | 6×1 | App 推广毛玻璃卡片 |
| `harmony-dual` | 灯球色盘 | 6×1 | 双端（应用+元服务）推广卡片 |
| `calendar-dashboard` | 智能周历 | 5×3 | **完全交互式仪表板**：年份控制、周末规则、假日区间CRUD、补班管理、每周日历视图、总工日统计 |
| `promo` | 原 promo 模板 | 3×3 | 活动宣传面板（卡片网格） |
| `3x3-merge` | — | 3×3 | 单元格合并演示 |
| `4x2-app-card` | — | 4×2 | 应用推广卡（左右分栏） |
| `3x3-mixed-styles` | — | 3×3 | 每格不同样式演示 |

---

## 基础模块 (Base Modules)

```
# 字体大小: font-size-xxl / xl / lg / md / sm / xs / xxs
# 字体颜色: color-dark / mid / light / white / primary / gradient-text
# 背景: bg-white / transparent / light-blue / glass / dark / gradient-*
# 圆角: radius-sm / md / lg / xl / full / pill
# 间距: pad-xs / sm / md / lg / xl
# 阴影: shadow-sm / md / lg / glass
# 边框: border-glass / light / bottom / divider-*
# 图片: img-circle / cover / contain / logo
# 布局: flex-center / between / col / text-center / text-left / gap-*
# 透明度: opacity-100 / 90 / 70 / 50
# 动画: anim-fade / slide / hover-scale
```

---

## 复合模块 (Composite Modules)

| 模块名 | 用途 | 槽位 (data-field) |
|--------|------|-------------------|
| `header-entity` | 单实体头部（图标+名称+标签） | entity-name, entity-badge |
| `header-dual` | 双实体头部（左应用+右元服务） | app-name, app-badge, service-name, service-badge |
| `main-title` | 渐变文字主标题+副标题+底边线 | main-title, main-sub |
| `qr-card` | 单张二维码卡片 | qr-image, qr-label, qr-hint |
| `qr-dual` | 双二维码并排 | qr-image-left/right, qr-label-left/right |
| `feature-panel` | 特性面板（多行图标+文字） | feature-icon-N, feature-text-N |
| `comms-panel` | 多端通信面板（设备标签+协议） | 设备标签内容 |
| `footer-caption` | 底部分隔线+标签组 | footer-tag-1/2/3 |
| `small-note` | 极小注释文字 | note-text |
| `text-block` | 纯文本块（标题+多行正文） | tb-title, tb-body, tb-body-2 |
| `text-img-right` | 左文右图组合 | ti-title, ti-desc |
| `param-panel` | 参数配置面板 | param-title, param-1/2 |
| `data-table` | 数据表格（表头+行） | th-1/2, td-row*-col* |
| `stat-card` | 数据统计卡片 | stat-label, stat-value |

---

## 可视化编辑器功能

- **Ctrl+E** — 进入/退出编辑模式
- **格子选择** — 点击格子 → 弹出属性面板
- **字段编辑** — 点击带 data-field 的文字区域直接编辑
- **工具栏** — 加粗/斜体/下划线、字色、背景色、字号、透明度
- **网格概览** — 点击"📋 网格"按钮查看所有格子
- **格子属性** — 右下角面板可调整底板颜色和内边距
- **Ctrl+S** — 导出最终 HTML
