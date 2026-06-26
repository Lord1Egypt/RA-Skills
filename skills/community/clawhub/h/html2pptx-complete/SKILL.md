---
name: html2pptx-complete
description: HTML 转 PPTX 完整工作流 — 自动内嵌外部 CSS，使用 pptxgenjs 解析 HTML 结构，生成可编辑 PPTX，保留文字、布局、样式
metadata:
  openclaw:
    version: 3.0
    requires:
      pip:
        - beautifulsoup4
        - cssutils
        - requests
      npm:
        - pptxgenjs
        - cheerio
---

# html2pptx-complete — HTML 转 PPTX 完整工作流

## 三步流程

```
HTML (带外部 CSS)
    ↓ [步骤 1: CSS 内嵌]
HTML (内嵌 CSS)
    ↓ [步骤 2: pptxgenjs 解析]
PPTX (可编辑)
    ↓ [步骤 3: 导出]
最终文件
```

---

## 快速开始

### 安装依赖

```bash
cd /Users/panda/.openclaw/workspace/skills/html2pptx-complete

# Python 依赖（CSS 内嵌）
pip3 install -r requirements-python.txt

# Node.js 依赖（PPTX 生成）
npm install
```

### 基本使用

```bash
# 一键转换
node scripts/convert.js input.html output.pptx

# 或分步执行
# 步骤 1: CSS 内嵌
python3 scripts/embed-css.py input.html embedded.html

# 步骤 2: PPTX 生成
node scripts/generate-pptx.js embedded.html output.pptx
```

---

## 步骤 1: CSS 内嵌

### 功能

- 🔍 查找所有 `<link rel="stylesheet">` 标签
- 📄 读取 CSS 文件内容
- 🔗 替换为 `<style>CSS 内容</style>`
- 🗑️ 移除外部 CSS 引用
- ✅ 保证 HTML 可独立运行

### 支持的 CSS

| 类型 | 支持度 | 说明 |
|------|--------|------|
| 本地相对路径 | ✅ | `href="style.css"` |
| 本地绝对路径 | ✅ | `href="/path/to/style.css"` |
| 远程 URL | ⚠️ 跳过 | `href="https://..."` |
| CSS 变量 | ✅ | 完整解析 |
| 渐变/动画 | ✅ | 保留原始代码 |

### 示例

**转换前:**
```html
<head>
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="theme.css">
</head>
```

**转换后:**
```html
<head>
  <style>
/* style.css 内容 */
/* theme.css 内容 */
  </style>
</head>
```

---

## 步骤 2: pptxgenjs 解析

### 解析规则

| HTML 结构 | PPTX 映射 | 说明 |
|-----------|-----------|------|
| `section.slide` | 新幻灯片 | 每张 slide 一页 |
| `<h1>` | 标题文本框 | 幻灯片标题 |
| `<h2>`-`<h6>` | 小标题 | 层级递减字号 |
| `<p>` | 正文文本框 | 保留段落 |
| `<ul>`, `<ol>` | 列表 | 保留项目符号 |
| `<img>` | 图片 | 支持路径/URL/Base64 |
| `<div>` | 容器/文本框 | 根据内容判断 |
| CSS 样式 | PPTX 属性 | 颜色/字体/大小/对齐 |

### 样式转换

| CSS 属性 | PPTX 映射 | 支持度 |
|----------|-----------|--------|
| `color` | 文字颜色 | ✅ |
| `background-color` | 填充色 | ✅ |
| `font-size` | 字号 | ✅ px→pt |
| `font-weight: bold` | 粗体 | ✅ |
| `font-style: italic` | 斜体 | ✅ |
| `text-align` | 对齐方式 | ✅ |
| `border` | 边框 | ⚠️ 简化 |
| `border-radius` | 圆角 | ⚠️ 部分 |
| `box-shadow` | 阴影 | ❌ |
| `linear-gradient` | 渐变填充 | ⚠️ 简化 |

### 分页规则

**优先级:**
1. `section.slide` 结构（最高优先级）
2. `<h1>` 标题（备选方案）
3. 整个文档作为单页（无上述结构时）

---

## 步骤 3: 导出

### 输出格式

| 属性 | 值 |
|------|-----|
| 格式 | PPTX (Office Open XML) |
| 比例 | 16:9 宽屏 |
| 可编辑性 | ✅ 文字/形状可编辑 |
| 文件大小 | 50-200KB（取决于内容） |

### 兼容性

- ✅ PowerPoint 2010+
- ✅ Keynote
- ✅ Google Slides
- ✅ LibreOffice Impress

---

## 使用示例

### 示例 1: html-ppt 生成的 HTML

```bash
# 输入：html-ppt 生成的多页 HTML
node scripts/convert.js my-deck/index.html my-deck.pptx

# 输出：包含所有 slide 的 PPTX
```

### 示例 2: 带外部 CSS 的 HTML

```bash
# 输入：引用多个 CSS 文件的 HTML
node scripts/convert.js presentation.html presentation.pptx

# 自动：
# 1. 嵌入 style.css, theme.css
# 2. 解析 slide 结构
# 3. 生成可编辑 PPTX
```

### 示例 3: 单页 HTML 文档

```bash
# 输入：普通 HTML 文档
node scripts/convert.js document.html document.pptx

# 输出：按 h1 标题分页的 PPTX
```

---

## 核心脚本

### scripts/embed-css.py (步骤 1)

```python
#!/usr/bin/env python3
"""CSS 内嵌脚本"""

import re
from pathlib import Path
from bs4 import BeautifulSoup

def embed_css(html_path, output_path=None):
    # 读取 HTML
    # 查找 <link> 标签
    # 读取 CSS 文件
    # 替换为 <style>
    # 保存
    pass
```

### scripts/generate-pptx.js (步骤 2-3)

```javascript
#!/usr/bin/env node
/**
 * PPTX 生成脚本
 * 使用 pptxgenjs 解析 HTML 并生成 PPTX
 */

const PptxGenJS = require('pptxgenjs');
const cheerio = require('cheerio');

async function generate(htmlPath, outputPath) {
  // 读取 HTML
  // 解析 slide 结构
  // 应用 CSS 样式
  // 创建 PPTX
  // 导出文件
}
```

### scripts/convert.js (一键执行)

```javascript
#!/usr/bin/env node
/**
 * 完整工作流脚本
 * 步骤 1: CSS 内嵌 (Python)
 * 步骤 2: PPTX 生成 (Node.js)
 * 步骤 3: 导出文件
 */

async function convert(htmlPath, outputPath) {
  // 调用 embed-css.py
  // 调用 generate-pptx.js
  // 清理临时文件
}
```

---

## 文件结构

```
html2pptx-complete/
├── SKILL.md                  (本文档)
├── README.md                 (快速入门)
├── package.json              (Node.js 依赖)
├── requirements-python.txt   (Python 依赖)
├── scripts/
│   ├── convert.js            (一键转换)
│   ├── embed-css.py          (CSS 内嵌)
│   └── generate-pptx.js      (PPTX 生成)
├── refs/
│   └── pptxgenjs-mapping.md  (样式映射表)
└── examples/
    ├── demo.html             (示例 HTML)
    ├── demo.css              (示例 CSS)
    └── demo_converted.pptx   (输出示例)
```

---

## 与现有技能对比

| 特性 | html2pptx-complete | html2pptx-shape |
|------|-------------------|-----------------|
| CSS 内嵌 | ✅ 自动 | ✅ 自动 |
| 核心库 | pptxgenjs (JS) | python-pptx |
| 环境 | Node.js + Python | Python |
| 样式保留 | ⚠️ 基础 + 部分 CSS | ✅ 完整 CSS |
| 布局还原 | ⚠️ 简化 | ✅ 精确 |
| 分页规则 | section.slide / h1 | section.slide |
| 适用场景 | 通用 HTML | html-ppt 生成 |

---

## 适用场景

### ✅ 推荐

- 📄 html-ppt 生成的 HTML 转 PPTX
- 📊 带外部 CSS 的 HTML 文档
- 📝 需要快速转换的通用 HTML
- 🎨 对样式要求不极端的场景

### ⚠️ 不推荐

- 🖼️ 复杂渐变/阴影效果（用 html-to-pptx 截图版）
- 🎭 精确像素级还原（用 html2pptx-shape）
- 📐 CSS Grid/Flex 复杂布局（可能简化）

---

## 依赖安装

```bash
# Python 依赖
pip3 install beautifulsoup4 cssutils requests

# Node.js 依赖
npm install pptxgenjs cheerio
```

---

## 常见问题

### Q1: CSS 文件找不到？

**检查:**
- 路径是否正确（相对/绝对）
- 文件是否存在
- 权限是否允许读取

**解决:**
- 使用绝对路径
- 或将 CSS 文件放到 HTML 同目录

### Q2: 样式丢失？

**原因:**
- pptxgenjs 不支持某些 CSS 属性
- 复杂选择器未解析

**解决:**
- 使用内联样式 `style="..."`
- 或简化 CSS 选择器

### Q3: 图片无法显示？

**检查:**
- 图片路径是否正确
- 网络 URL 是否可访问
- Base64 格式是否正确

---

## 更新日志

### v1.0.0 (2026-04-17)
- ✅ 初始版本
- ✅ CSS 自动内嵌
- ✅ pptxgenjs 解析
- ✅ section.slide/h1 分页
- ✅ 基础样式映射

---

## License

MIT

## Author

老 6 🎯
