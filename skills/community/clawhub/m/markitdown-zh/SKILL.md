---
name: markitdown-zh
description: 使用微软 markitdown 库将多种文档格式（PDF、DOCX、PPTX、XLSX、XLS、CSV、JSON、TXT、EPUB、HTML等）转换为 Markdown。支持批量转换、保留格式、图片提取等功能。使用场景：(1) "把这个 PDF 转成 Markdown"，(2) "把这个 word 文档转成 Markdown"，(3) "批量转换这个文件夹里的文档"，(4) "提取文档中的图片"。
---
# tags
"文档转换", "markitdown", ".docx .xlsx .pptx", "OCR"

# MarkItDown 文档转换技能

使用微软的 markitdown 库将各种文档格式转换为 Markdown。

## 支持的格式

- PDF (.pdf)
- Word 文档 (.docx)
- PowerPoint 演示文稿 (.pptx)
- Excel 电子表格 (.xlsx .xls)
- HTML 文件 (.html, .htm)
- 纯文本文件 (.txt, .rtf, .xml, .csv, .json)
- 电子书 (.epub)
- 等等...

## 快速开始

### 单个文件转换

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

### 使用提供的脚本

```bash
# 转换单个文件
python3 scripts/convert.py input.pdf output.md

# 批量转换文件夹
python3 scripts/batch_convert.py input_folder/ output_folder/

# 提取文档中的图片
python3 scripts/extract_images.py document.pdf images_folder/
```

## 详细用法

### 单个文件转换

使用 `scripts/convert.py`：

```bash
python3 scripts/convert.py <input_file> [output_file]
```

如果不指定输出文件，会自动生成 `.md` 文件。

### 批量转换

使用 `scripts/batch_convert.py`：

```bash
python3 scripts/batch_convert.py <input_directory> <output_directory>
```

会递归处理目录中的所有支持的文件。

### 图片提取

使用 `scripts/extract_images.py`：

```bash
python3 scripts/extract_images.py <input_file> <output_directory>
```

从文档中提取所有图片并保存到指定目录。

## 脚本说明

- `scripts/convert.py` - 单个文件转换脚本
- `scripts/batch_convert.py` - 批量转换脚本
- `scripts/extract_images.py` - 图片提取脚本

每个脚本都有 `--help` 选项查看详细参数。

## 安装依赖

### Python 版本要求

markitdown 需要 Python 3.10 或更高版本。

检查 Python 版本：
```bash
python3.12 --version  # 或 python3.11, python3.13
```

### 安装 markitdown

使用 Python 3.10+ 安装：

```bash
# 使用 Python 3.12（推荐）
# 使用虚拟环境（适用于非root用户，如node用户）
python3.12 -m venv markitdown-env
source markitdown-env/bin/activate
pip install "markitdown[all]"

# 或安装pipx包管理应用，通过pipx安装markitdown
sudo apt-get install pipx
# 使用pipx安装markitdown包 all表示支持所有格式
pipx install 'markitdown[all]'
# 将通过pipx安装的包路径放入当前变量PATH内
pipx ensurepath
```

### 可选：系统依赖

某些格式转换可能需要额外的系统依赖：

- **PDF 处理**: `brew install poppler` (macOS) 或 `sudo apt-get install poppler-utils` (Linux)
- **OCR**: `brew install tesseract` (macOS) 或 `sudo apt-get install tesseract-ocr` (Linux)

## 验证安装

```bash
python3.12 -c "from markitdown import MarkItDown; print('安装成功!')"
```

## 使用脚本

所有脚本都支持使用特定 Python 版本运行：

```bash
# 使用 Python 3.12 运行
python3.12 scripts/convert.py input.pdf output.md
python3.12 scripts/batch_convert.py input_folder/ output_folder/
python3.12 scripts/extract_images.py document.pdf images_folder/
```

## 另请参阅

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - 上游库
