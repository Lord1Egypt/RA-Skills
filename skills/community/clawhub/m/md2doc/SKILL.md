---
name: md2doc
description: Markdown 转 Word/PDF/HTML 文档转换器。支持 6 种样式模板（商务蓝、技术灰、简洁白、产品红、学术风、默认），自动生成封面、目录、页眉页脚。当用户需要将 Markdown 转成 Word、PDF 或 HTML，生成带样式的文档，或提到文档导出、格式转换时，使用此技能。
---

# MD2DOC - Markdown 文档转换技能

将 Markdown 文件转换为专业美观的 Word (.docx)、PDF 和 HTML 文档。

## 安装

### 方式一：直接复制
将 `md2doc` 文件夹复制到 OpenClaw 的 skills 目录：
```bash
# Windows
xcopy /E md2doc %USERPROFILE%\.openclaw\skills\

# Linux/Mac
cp -r md2doc ~/.openclaw/skills/
```

### 方式二：安装依赖
```bash
pip install python-docx requests markdown beautifulsoup4 Pillow
```

## 功能特性

- ✅ Markdown 转 Word (.docx)
- ✅ Markdown 转 PDF（需安装 Word 或 LibreOffice）
- ✅ **6 种样式模板**（商务蓝、技术灰、简洁白、产品红、学术风、默认）
- ✅ 图片自动嵌入（支持本地路径和网络图片）
- ✅ 表格自动美化（表头带背景色）
- ✅ 代码块带背景色
- ✅ 标题层级自动处理
- ✅ 中文排版优化
- ✅ 同时输出 Word + PDF

## 使用方法

### OpenClaw 中使用

当用户需要将 Markdown 文件转换为 Word/PDF 时：

1. **确认文件路径** - 获取用户提供的 MD 文件路径
2. **检查依赖** - 确保已安装 python-docx 和 requests
3. **执行转换** - 使用脚本转换文件
4. **返回结果** - 告知用户输出文件位置

```python
# 在 OpenClaw 中调用
import subprocess
result = subprocess.run([
    "python", "skills/md2doc/scripts/md2doc.py", 
    "用户文件.md"
], capture_output=True, text=True)
```

### 命令行使用

```bash
# 转 Word（默认样式）
python scripts/md2doc.py input.md

# 同时转 Word + PDF
python scripts/md2doc.py input.md --pdf

# 指定输出目录
python scripts/md2doc.py input.md --output-dir ./output --pdf

# 使用样式模板
python scripts/md2doc.py input.md --style business
python scripts/md2doc.py input.md --style product --pdf

# 查看所有可用样式
python scripts/md2doc.py --list-styles
```

### 可用样式模板

| 样式 | 说明 | 适用场景 |
|------|------|----------|
| `default` | 标准样式 | 一般文档 |
| `business` | 商务蓝，蓝色主题 | 企业报告、商务文档 |
| `tech` | 技术灰，灰色主题 | 技术文档、API 文档 |
| `minimal` | 简洁白，极简风格 | 轻量文档、笔记 |
| `product` | 产品红，红色强调 | PRD、产品需求文档 |
| `academic` | 学术风，宋体正文 | 论文、学术报告 |

### 支持的 Markdown 语法

- 标题（# ## ### 等）
- 段落和文本格式（**粗体**、*斜体*）
- 列表（有序/无序）
- 图片（本地路径或 URL）
- 表格
- 代码块（行内和块级）
- 引用块
- 分隔线

## 工作流程

1. **检查依赖**：确保 Python 和必要库已安装
2. **读取 MD 文件**：解析 Markdown 内容
3. **处理图片**：下载网络图片，验证本地图片路径
4. **生成 Word**：使用 python-docx 创建 .docx 文件
5. **生成 PDF**（可选）：使用 Word 转 PDF 或 reportlab
6. **返回结果**：告知用户输出文件路径

## 依赖安装

```bash
pip install python-docx markdown beautifulsoup4 requests Pillow
```

## 样式说明

- 标题：微软雅黑，层级递减
- 正文：宋体，11pt
- 代码块：等宽字体，浅灰背景
- 表格：带边框，表头加粗
- 图片：最大宽度 6 英寸，居中

## 注意事项

- 图片路径可以是相对路径（相对于 MD 文件位置）或绝对路径
- 网络图片会自动下载并嵌入
- 不支持的 Markdown 扩展语法会被当作普通文本处理
