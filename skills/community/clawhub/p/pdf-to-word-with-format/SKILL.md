---
name: pdf-to-word-with-format
description: PDF带格式精确转换成Word Skill。将PDF文档精确转换为Word文档，完整保留原始字体名称、字号(pt)、段落格式（行间距1.5倍、段前段后间距、首行缩进2字符）、文本对齐方式（居中/两端对齐）、文本格式（粗体、斜体、下划线、颜色）、表格和图片等。支持中文字体智能映射（宋体→宋体、黑体→黑体、楷体→楷体等）。触发场景：用户说"PDF转Word"、"PDF转Word保留格式"、"PDF精准转Word"、"PDF format to Word"、"Convert PDF with formatting"等。
---

# PDF带格式精确转换成Word (PDF to Word with Format)

## 概述

本 skill 提供**高精度**PDF转Word转换服务，最大程度保留原始文档的所有格式信息。

### 核心功能

1. **精确字体映射**
   - 智能识别PDF字体名称
   - 映射到Word可用中英文字体
   - 支持：宋体、黑体、楷体、仿宋_GB2312、Times New Roman、Arial等

2. **字号精确转换**
   - 精确保留原始字号（pt）
   - 标题22pt、二号16pt、三号14pt等

3. **段落格式保留**
   - 行间距：1.5倍行距
   - 首行缩进：2字符（0.74cm）
   - 段前段后间距

4. **文本对齐**
   - 左对齐、居中、右对齐、两端对齐

5. **文本格式**
   - 粗体（Bold）
   - 斜体（Italic）
   - 下划线（Underline）
   - 文本颜色

6. **表格支持**
   - 完整表格结构
   - 单元格内容

7. **图片支持**
   - 提取并保留图片位置
   - 自动调整图片大小

---

## 使用方式

### 基本转换

```bash
python convert.py <输入PDF> --output <输出Word>
```

### 批量转换

```bash
python convert.py <PDF文件夹> --batch --output <输出文件夹>
```

### 转换指定页面

```bash
python convert.py 文档.pdf --pages 0-5 --output 文档.docx
```

---

## 依赖安装

首次使用需安装依赖：

```bash
pip install pymupdf python-docx
```

---

## 示例

```bash
# 基本转换
python convert.py 报告.pdf --output 报告.docx

# 批量转换文件夹中所有PDF
python convert.py ./pdfs/ --batch --output ./words/

# 转换前10页
python convert.py 文档.pdf --pages 0-9 --output 文档.docx

# 指定起始页和结束页
python convert.py 长文档.pdf --start 5 --end 15 --output 部分.docx
```

---

## 输出说明

- 输出文件为 `.docx` 格式，可用 Microsoft Word 或 WPS 打开
- 转换后的文档保留了大部分原始格式
- 特殊布局的PDF转换效果可能略有差异

---

## 技术原理

本 skill 基于以下技术实现：

1. **PyMuPDF (fitz)** - 提取PDF内容和格式信息
2. **python-docx** - 构建Word文档

提取的格式信息包括：
- 字体名称、字号
- 文本对齐方式
- 粗体、斜体、下划线标志
- 文本颜色（RGB）
- 段落位置坐标

---

## 字体映射表

| PDF字体 | Word字体 |
|--------|---------|
| 宋体, SimSun | 宋体 |
| 黑体, SimHei | 黑体 |
| 楷体, SimKai | 楷体_GB2312 |
| 仿宋, SimFang | 仿宋_GB2312 |
| Times New Roman | Times New Roman |
| Arial, Helvetica | Arial |
| 微软雅黑, Microsoft YaHei | 微软雅黑 |
