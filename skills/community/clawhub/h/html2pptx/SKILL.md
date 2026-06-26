---
name: html2pptx
version: 3.0.0
description: 将HTML演示文稿转换为PowerPoint(PPTX)格式。支持frontend-slides生成的HTML，保留结构、样式和内容。触发词：html转pptx、html2pptx、转换ppt、生成pptx
author: Claude
license: MIT
tags: [presentation, conversion, html, powerpoint, pptx]
category: productivity
requirements:
  - python: ">=3.9"
---

# HTML to PPTX 转换器

将HTML演示文稿（特别是frontend-slides生成的）转换为原生PowerPoint(.pptx)文件。

## 使用场景

- 将frontend-slides生成的HTML演示文稿转换为可编辑的PPT
- 保留幻灯片结构、文字内容和基本样式
- 批量转换多个HTML文件

## 使用方法

### 基本用法

```bash
python src/convert.py <input.html> [output.pptx]
```

### 示例

```bash
# 转换单个文件
python src/convert.py presentation.html

# 指定输出路径
python src/convert.py presentation.html ~/Documents/output.pptx
```

## 支持的内容

| HTML元素 | PPTX转换 |
|---------|---------|
| `<section class="slide">` | 幻灯片页 |
| `<h1>`, `<h2>` | 标题 |
| `<p>` | 段落文本 |
| `<ul>`, `<ol>`, `<li>` | 列表 |
| `<div class="card">` | 文本框分组 |
| `<img>` | 图片（保留路径） |
| CSS颜色 | 尝试匹配主题色 |

## 转换流程

1. **解析HTML** - 使用BeautifulSoup提取slide结构
2. **分析样式** - 提取CSS颜色、字体信息
3. **创建PPTX** - 使用python-pptx生成幻灯片
4. **映射内容** - 将HTML元素映射到PPTX形状
5. **保存文件** - 输出.pptx文件

## 限制说明

- 复杂CSS动画无法转换
- 渐变背景转为纯色
- 自定义字体可能丢失
- 绝对定位元素需要手动调整

## 依赖安装

```bash
pip install python-pptx beautifulsoup4 lxml
```

## 文件结构

```
html2pptx/
├── SKILL.md          # 本文件
├── src/
│   └── convert.py    # 主转换脚本
└── examples/         # 示例文件
```
