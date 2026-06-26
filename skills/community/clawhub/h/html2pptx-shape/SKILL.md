---
name: html2pptx-shape
description: HTML 转 PPTX 形状转换器 — 将 HTML 幻灯片转换为完全可编辑的 PPTX，自动内嵌外部 CSS，保留 CSS 样式、布局，映射为 PPTX 原生形状（矩形/文本框/图片等）
metadata:
  openclaw:
    version: 3.0
    requires:
      pip:
        - python-pptx
        - beautifulsoup4
        - pillow
        - requests
        - cssutils
        - premailer
        - playwright
---

# html2pptx-shape — HTML 转 PPTX 形状转换器

将 HTML 幻灯片转换为 **完全可编辑的 PPTX**，核心特性：

- **自动内嵌外部 CSS** — 将 `<link>` 引用的 CSS 文件嵌入到 `<style>` 标签
- **CSS 样式完整保留** — 颜色、字体、渐变、阴影、边框、圆角
- **布局精确还原** — 元素位置、尺寸、层级关系
- **PPTX 原生形状映射** — div→矩形，p/h→文本框，img→图片，svg→形状
- **16:9 标准比例** — 宽屏演示文稿 (13.333" × 7.5")

## 快速开始

### 安装依赖

```bash
cd /Users/panda/.openclaw/workspace/skills/html2pptx-shape
pip3 install -r requirements.txt
playwright install chromium
```

### 基本使用

```bash
# 转换 HTML 文件（自动内嵌外部 CSS）
python3 index.py <input.html> [output.pptx]

# 示例
python3 index.py examples/demo.html
python3 index.py my-presentation.html my-output.pptx
```

### 输出

| 项目 | 说明 |
|------|------|
| 文件名 | `<input>_converted.pptx`（默认）或指定名称 |
| 格式 | PPTX (Office Open XML) |
| 比例 | 16:9 widescreen |
| 可编辑性 | ✅ 所有文字/形状可编辑 |

---

## 功能特性

### ✅ 自动 CSS 内嵌

自动将外部 CSS 文件嵌入到 HTML 的 `<style>` 标签中：

```html
<!-- 转换前 -->
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="theme.css">

<!-- 转换后 -->
<style>
/* styles.css 内容 */
/* theme.css 内容 */
</style>
```

支持：
- ✅ 多个 `<link>` 标签
- ✅ 相对路径 CSS 文件
- ✅ CSS 变量（`:root` 和任何选择器中的定义）
- ⚠️ 自动跳过远程 CSS（http/https 开头）

### ✅ CSS 样式支持

| CSS 属性 | PPTX 映射 | 支持度 |
|----------|-----------|--------|
| `color` | 文字颜色 | ✅ |
| `background-color` | 填充颜色 | ✅ |
| `background` (gradient) | 渐变填充 | ⚠️ 转为纯色 |
| `font-family` | 字体 | ✅ |
| `font-size` | 字号 | ✅ |
| `font-weight` | 字重 | ✅ |
| `text-align` | 对齐方式 | ✅ |
| `border` | 边框 | ✅ |
| `border-radius` | 圆角矩形 | ✅ |
| `box-shadow` | 阴影 | ✅ |
| `opacity` | 透明度 | ✅ |
| `width/height` | 尺寸 | ✅ |
| `position: absolute` | 绝对定位 | ✅ |

### ✅ 元素映射

| HTML 元素 | PPTX 形状 | 说明 |
|-----------|-----------|------|
| `<div>` | Rectangle | 矩形背景/容器 |
| `<p>`, `<h1>`-`<h6>` | TextBox | 文本框，保留字体/颜色/对齐 |
| `<img>` | Picture | 图片，支持 base64/URL/本地文件 |
| `<svg>` | Freeform | SVG 路径转 PPTX 自由形状（简化） |
| `<span>` | (内联) | 文本格式化，不创建独立形状 |
| `<ul>`, `<ol>` | TextBox | 列表文本框，保留项目符号 |

---

## 技术实现

1. **CSS 嵌入** — 自动将外部 CSS 文件嵌入到 HTML `<style>` 标签
2. **CSS 变量解析** — 收集所有 CSS 变量定义（支持任何选择器）
3. **CSS 内联** — 使用 cssutils 解析并应用样式到每个元素
4. **HTML 解析** — BeautifulSoup4 解析 DOM 结构
5. **布局计算** — 遍历 DOM 树，计算每个元素的绝对位置
6. **形状创建** — python-pptx 创建对应形状
7. **样式应用** — 将 CSS 属性映射到 PPTX 形状属性
8. **分页处理** — 遍历 `section.slide`，每页创建一张幻灯片

---

## 使用场景

- 将 `html-ppt` 生成的 HTML 演示文稿转为可编辑 PPTX
- 网页内容存档为 PPTX 格式
- 需要后期编辑的 HTML→PPTX 转换
- 自包含 HTML 文件（无外部依赖）的 PPTX 转换

---

## 示例

### 示例 1：转换 html-ppt 生成的 HTML

```bash
python3 index.py examples/demo.html
# 输出：examples/demo_converted.pptx
```

### 示例 2：转换带有外部 CSS 的 HTML

```bash
python3 index.py my-presentation.html
# 自动嵌入 style.css, theme.css 等外部文件
# 输出：my-presentation_converted.pptx
```

### 示例 3：指定输出文件名

```bash
python3 index.py input.html output.pptx
```

### 示例 4：在 Python 中调用

```python
from index import run
result = run(["./examples/demo.html"])
print(f"Generated: {result['output_file']}")
print(f"Slides: {result['slides_count']}")
```

---

## 文件结构

```
html2pptx-shape/
├── SKILL.md                 (本文档)
├── README.md                (快速入门)
├── index.py                 (核心转换逻辑)
├── requirements.txt         (Python 依赖)
├── scripts/
│   ├── embed-css.py         (独立 CSS 嵌入工具)
│   ├── debug-convert.py     (调试脚本)
│   ├── check-inline.py      (样式检查脚本)
│   └── debug-vars.py        (变量调试脚本)
└── examples/
    ├── demo.html            (示例 HTML - 4 页)
    ├── demo_converted.pptx  (生成的 PPTX)
    ├── external-css.html    (外部 CSS 测试)
    ├── external-css_converted.pptx
    ├── styles.css
    └── theme.css
```

---

## 完整工作流

### 从 html-ppt 到 PPTX

```bash
# 1. 用 html-ppt 生成 HTML 演示文稿
# (使用 html-ppt skill 创建 HTML)

# 2. 转换为可编辑 PPTX
python3 index.py my-deck/index.html

# 3. 在 PowerPoint 中打开并编辑
open my-deck/index_converted.pptx
```

### 处理外部 CSS

```bash
# 情况 A: HTML 引用外部 CSS
# index.html 中有：<link rel="stylesheet" href="style.css">

# 直接转换，自动嵌入 CSS
python3 index.py index.html

# 情况 B: 想先内嵌 CSS 再转换
python3 scripts/embed-css.py index.html
python3 index.py index_embedded.html
```

---

## 限制与已知问题

| 限制 | 说明 | 建议 |
|------|------|------|
| CSS 动画 | 不支持（转换为静态） | 使用截图版保留视觉效果 |
| CSS Grid/Flex | 简化为绝对定位 | 检查布局是否正确 |
| 外部字体 | 回退到系统字体 | 确保系统有相应字体 |
| `::before`/`::after` | PPTX 不支持伪元素 | 忽略警告 |
| `background-clip: text` | 渐变文字转纯色 | 手动在 PPTX 中添加渐变 |
| 复杂 SVG | 降级为占位符 | 简化 SVG 或转为图片 |

---

## 依赖安装

```bash
# Python 依赖
pip3 install python-pptx beautifulsoup4 pillow requests cssutils premailer

# Playwright 浏览器（用于截图功能）
playwright install chromium
```

---

## 故障排除

### 问题：CSS 文件未找到

```
⚠️  CSS file not found: xxx.css
```

**原因：** 相对路径无法解析

**解决：**
1. 将 CSS 文件移动到正确位置
2. 或使用 `scripts/embed-css.py` 先内嵌 CSS
3. 或直接将 CSS 内容复制到 `<style>` 标签中

### 问题：样式未应用

**原因：** CSS 选择器太复杂或使用了不支持的属性

**解决：**
1. 检查 HTML 元素的 class 是否正确
2. 使用内联样式 `style="..."` 替代
3. 查看转换日志中的 selector error 警告

### 问题：布局错乱

**原因：** CSS Grid/Flex 布局被简化

**解决：**
1. 使用绝对定位 `position: absolute` 替代
2. 或在 PPTX 中手动调整位置

---

## 与 html-to-pptx 的对比

| 特性 | html2pptx-shape | html-to-pptx |
|------|-----------------|--------------|
| CSS 内嵌 | ✅ 自动 | ⚠️ 需要预处理器 |
| CSS 变量解析 | ✅ 完整支持 | ⚠️ 部分支持 |
| 形状映射 | ✅ 原生 PPTX 形状 | ⚠️ 简化文本框 |
| 可编辑性 | ✅ 完全可编辑 | ✅ 完全可编辑 |
| 文件大小 | 小 (30-50KB) | 小 (30-50KB) |
| 截图高保真 | ❌ | ✅ 支持 |

---

## 更新日志

### v1.0.0 (2026-04-17)
- ✅ 初始版本
- ✅ 自动内嵌外部 CSS
- ✅ CSS 变量完整解析（支持任何选择器）
- ✅ CSS 样式手动内联（使用 cssutils）
- ✅ PPTX 原生形状映射
- ✅ 16:9 标准比例

---

## License

MIT

## Author

老 6 🎯
