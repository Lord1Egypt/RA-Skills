---
name: pptx-add-slides
description: 在已有 PPT 中新增幻灯片并保持风格一致。核心策略：从原 PPT 提取典型页面的完整 slide XML 作为模板，仅替换文字内容，零手工拼样式。
  Use when user asks to 在 PPT 里加几页、新增幻灯片、补充内容页、插入页面、扩展 PPT、给 PPT 增加章节.
  不适用于从头创建新 PPT、仅修改现有页面文字、或不需要保持风格一致的场景.
---

## 概述

在已有 PPTX 文件中新增幻灯片，并确保新页面与原 PPT 的风格（母版、版式、背景、字体、配色、卡片底板、装饰元素等）完全一致。

**核心原则：零手工拼 XML。** 从原 PPT 中提取已有页面的完整 XML 作为模板，仅替换 `<a:t>` 文本节点，其余所有样式属性原样保留。这从根本上避免了手工拼 XML 导致的字号偏差、颜色错误、背景丢失等问题。

### 功能范围

- 解析原 PPTX，识别母版和版式（slide layout）
- 从原 PPT 中选取典型页面（正文内容页 / 章节分隔页）作为模板
- 基于模板 XML 创建新幻灯片，仅替换文字内容
- 支持多种页面类型：正文页、分隔页、封面页
- 插入到指定位置（开头、结尾或任意页码之间）
- 通过操作 PPTX zip 内 XML 结构确保一致性

### 为什么不用 python-pptx 的 add_slide + 手工填属性

python-pptx 的 `add_slide(layout)` 仅复制版式骨架（占位符位置），不会复制背景图、主题色覆盖、自定义形状、透明度遮罩等实际渲染出来的样式。手工逐属性赋值极易遗漏细微参数（如阴影、渐变、线宽、文本框内边距），导致视觉不一致。唯一可靠的方式是克隆已有 slide 的完整 XML，然后替换文本。

---

## 使用

### 脚本位置

核心脚本文位于 `scripts/add_slides.py`。

### 场景 1：新增正文内容页

```bash
python3 scripts/add_slides.py \
  --source "原PPT路径.pptx" \
  --output "输出PPT路径.pptx" \
  --template-page 5 \
  --insert-after 1 \
  --pages '[{"title": "新页面标题", "subtitle": "副标题文字", "content": ["要点一", "要点二", "要点三"], "footer": "底部总结文字"}]'
```

- `--template-page`：原 PPT 中作为模板的页码（从 1 开始），选排版最典型的正文页
- `--insert-after`：新页面插入到第几页之后
- `--pages`：JSON 数组，每项对应一页的内容

### 场景 2：新增章节分隔页

```bash
python3 scripts/add_slides.py \
  --source "原PPT路径.pptx" \
  --output "输出PPT路径.pptx" \
  --template-page 20 \
  --insert-after 4 \
  --page-type "section" \
  --pages '[{"section_number": "05", "title": "考核与评估机制", "desc": "构建科学的人才评价体系"}]'
```

### 场景 3：同时新增多种类型页面（混合插入）

```bash
python3 scripts/add_slides.py \
  --source "原PPT路径.pptx" \
  --output "输出PPT路径.pptx" \
  --pages-config '[{"template": 5, "insert_after": 3, "type": "content", "data": {"title": "...", "content": ["..."]}}, {"template": 20, "insert_after": 10, "type": "section", "data": {"section_number": "02", "title": "...", "desc": "..."}}]'
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `--source` | 原 PPTX 文件路径 |
| `--output` | 输出 PPTX 文件路径 |
| `--template-page` | 模板页码（1-based），选取排版最典型的页面 |
| `--insert-after` | 插入位置（在指定页码之后） |
| `--page-type` | 页面类型：`content`（默认）/ `section` / `cover` |
| `--pages` | 页面内容 JSON 数组 |
| `--pages-config` | 混合类型的完整配置 JSON 数组 |

---

## 补充说明

### 模板页选择原则

- **正文内容页**：选原 PPT 中排版元素最全的一页（有标题、副标题、正文要点、底部栏、卡片底板等）
- **章节分隔页**：选原 PPT 中已有的章节分隔页，确保数字样式、标题位置等一致
- **避免选封面或目录页**：这些页面通常有特殊排版，不适合作为通用模板
- 如果原 PPT 没有章节分隔页，选择排版最简单的正文页并手动将内容区的文本块全部清空，只保留背景和标题区域

### 依赖安装

```bash
pip install python-pptx lxml
```

### 常见问题

**Q：脚本执行后新页面背景图丢失？**
A：检查原 PPT 中模板页的背景图是否嵌在 slide XML 的关系链中。如果背景图通过 slide layout 的关系引用，需要在复制 slide XML 时同时复制 `slideX.xml.rels` 中的图片关系。

**Q：替换文字后样式变了？**
A：确保只替换 `<a:t>` 标签内的文本，不要触碰 `<a:rPr>` 等样式标签。本脚本使用 lxml 精确定位文本节点。

**Q：内容结构不匹配导致文本溢出或留白？**
A：模板页有几个文本区域就填充几个。如果内容比模板的文本区域多，多余内容会被截断；如果少，对应区域保持空白。选择文本区域数量足够的页面作为模板。

**Q：新页面的超链接/动画丢失？**
A：slide XML 模板复制会保留超链接（`<a:hlinkClick>`），但动画（`<p:anim>`）和切换效果需要从 `slideX.xml` 的 timing 部分额外处理。简单场景下动画可以忽略。

### 已知坑点

1. **不要用 `slide.background` 属性覆盖** — python-pptx 的 background API 只能设置纯色，无法处理图片背景。背景图通过 `p:bg` 元素在 XML 中定义，模板复制方式天然保留。
2. **主题色引用** — 如果模板页使用了主题色（如 `val="accent1"`），复制后主题色引用自动生效，无需手动计算 RGB 值。这是模板方案相比手工拼 XML 的核心优势之一。
3. **关系 ID 冲突** — 从 zip 内复制 slide XML 时，新 slide 的关系 ID（rId）可能与已有 slide 冲突。脚本会自动重新编号。
4. **内容类型声明** — 新增 slide 后需要更新 `[Content_Types].xml` 中的 Override 声明，脚本会自动处理。
