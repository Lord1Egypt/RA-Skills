# module-library.md — hug-html 组件式模块库 v3.0

## 架构总览

```
骨架 (Skeleton) — N×M 网格 + 3级约束(fill/fit/clip)
  └─ 单元格 (Cell) — 放置组件组合
       ├─ 组件 (Component) — 8种原子类型
       │    ├─ text     纯文本（title/body/caption）
       │    ├─ image    图片（fit/cover/clip）
       │    ├─ icon     图标（FontAwesome/SVG）
       │    ├─ qrcode   二维码
       │    ├─ table    数据表格
       │    ├─ divider  分割线
       │    ├─ spacer   空白占位
       │    └─ group    组合容器（递归）
       └─ 约束系统 — fill/fit/clip 递归应用
```

**核心变化**（v2 → v3）：
- 旧：14 个预置复合模块，每个固定 HTML 结构 → 硬编码，难以定制
- 新：8 个原子组件 + 声明式组合 → 自由搭配，无限可能

---

## 组件类型

### text — 纯文本

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"text"` |
| `content` | string | ✅ | 文本内容 |
| `variant` | string | ❌ | `title`(标题) / `body`(正文) / `caption`(注释)，默认 `body` |
| `style` | object | ❌ | 覆盖样式（font_size, font_weight, color 等） |

**变体默认样式：**

| 变体 | font_size | font_weight | color |
|------|-----------|-------------|-------|
| title | 18px | 700 | #1a1a2e |
| body | 14px | 400 | #4a4a6a |
| caption | 12px | 300 | #8888aa |

### image — 图片

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"image"` |
| `src` | string | ✅ | 图片URL |
| `alt` | string | ❌ | 替代文字 |
| `constraint` | string | ❌ | `fit`(默认) / `cover` / `fill` |
| `aspect` | string | ❌ | 宽高比，如 `"1/1"`、`"16/9"` |
| `style` | object | ❌ | 额外CSS |

### icon — 图标

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"icon"` |
| `name` | string | ✅ | 图标名（如 `star`、`heart`） |
| `family` | string | ❌ | `fa`(FontAwesome) / `svg`(内联)，默认 `fa` |
| `size` | string | ❌ | 尺寸，如 `"24px"`，默认 `24px` |
| `color` | string | ❌ | 颜色，默认 `#1a1a2e` |

### qrcode — 二维码

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"qrcode"` |
| `content` | string | ✅ | 二维码内容（URL/文本） |
| `size` | string | ❌ | 尺寸如 `"120px"`，默认 `120px` |
| `label` | string | ❌ | 二维码下方标注文字 |

### table — 数据表格

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"table"` |
| `headers` | string[] | ✅ | 表头数组 |
| `rows` | string[][] | ✅ | 数据行二维数组 |
| `style` | object | ❌ | 额外CSS |

### divider — 分割线

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"divider"` |
| `height` | string | ❌ | 线粗，默认 `"1px"` |
| `color` | string | ❌ | 颜色，默认 `"#e0e0e0"` |
| `style_type` | string | ❌ | `solid` / `dashed` / `dotted`，默认 `solid` |

### spacer — 空白占位

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"spacer"` |
| `width` | string | ❌ | 宽度，默认 `"100%"` |
| `height` | string | ❌ | 高度，默认 `"auto"` |

### group — 组合容器（递归）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | `"group"` |
| `direction` | string | ❌ | `"row"`(默认) / `"column"` |
| `align` | string | ❌ | 主轴对齐：`left` / `center` / `right` / `top` / `bottom` |
| `cross_align` | string | ❌ | 交叉轴对齐：`stretch`(默认) / `center` / `flex-start` / `flex-end` |
| `ratios` | number[] | ❌ | 子组件flex比例，如 `[1, 2]` 表示1/3和2/3 |
| `children` | array | ✅ | 子组件列表 |
| `style` | object | ❌ | 容器额外CSS |

---

## 约束系统

三种约束模式递归应用于：**骨架 → 模块 → 组件**

| 模式 | 枚举值 | CSS 行为 | 适用场景 |
|------|--------|----------|---------|
| 完全贴合 | `fill` | `width/height:100%` 拉伸填充 | 背景图、全宽文字 |
| 等比缩放 | `fit` | `max-width/max-height:100%` + `object-fit:contain` | 图标、Logo |
| 裁剪遮挡 | `clip` | `position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);overflow:hidden` | 头像、封面图 |

约束在 Spec 中的配置位置：

```json
// 骨架对模块的约束（cell级别）
{"row": 0, "constraint": "fit", ...}

// 组件级别的约束
{"type": "image", "constraint": "clip", "aspect": "1/1", ...}
```

---

## Grid Spec 完整示例

```json
{
  "name": "图文卡片",
  "card_style": {
    "max_width": "400px",
    "bg": "rgba(255,255,255,0.85)",
    "backdrop": "blur(20px)",
    "border_radius": "24px",
    "shadow": "0 12px 40px rgba(0,0,0,0.12)",
    "padding": "20px"
  },
  "grid": {
    "rows": 3, "cols": 3, "gap": "12px",
    "cells": [
      {
        "id": "hero", "row": 0, "col": 0, "rowspan": 2, "colspan": 2,
        "constraint": "fill",
        "padding": "8px",
        "components": [
          {
            "type": "image",
            "src": "https://picsum.photos/200",
            "constraint": "cover",
            "style": {"border_radius": "12px"}
          }
        ]
      },
      {
        "id": "info", "row": 0, "col": 2, "rowspan": 2,
        "direction": "column",
        "ratios": [1, 2, 1],
        "components": [
          {"type": "icon", "name": "star", "size": "28px", "color": "#ffd700"},
          {"type": "group", "direction": "column", "children": [
            {"type": "text", "variant": "title", "content": "卡片标题"},
            {"type": "text", "variant": "body", "content": "这里是正文描述，展示组件式组合的效果。"}
          ]},
          {"type": "text", "variant": "caption", "content": "¥ 99.00"}
        ]
      },
      {"id": "div", "row": 2, "col": 0, "colspan": 3,
       "components": [{"type": "divider"}]}
    ]
  }
}
```

---

## 命令行

```bash
# 列出所有组件类型
python scripts/module_assembler.py --list-components

# 导出接口定义JSON
python scripts/module_assembler.py --export-interfaces interfaces.json

# 生成组件系统演示HTML
python scripts/module_assembler.py --demo

# 旧模块系统（向后兼容）
python scripts/grid_builder.py --list-modules
python scripts/grid_builder.py --spec <spec> -o <output.html>
```

---

## 从旧格式迁移

旧版 `"module": "composite:xxx"` 格式仍然支持，但建议迁移到组件式格式。

**迁移示例：text-img-right（左文右图）**

旧格式：
```json
{"module": "composite:text-img-right"}
```

新格式：
```json
{
  "direction": "row",
  "ratios": [1, 1],
  "components": [
    {"type": "text", "variant": "title", "content": "标题"},
    {"type": "image", "src": "https://...", "constraint": "fit", "aspect": "1/1"}
  ]
}
```
