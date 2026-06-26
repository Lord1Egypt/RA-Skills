---
name: ollie-file-processor
description: 通用文件处理技能,用于批量重命名和格式转换。当用户需要批量重命名文件(添加前缀/后缀、替换文本、编号重命名、正则表达式重命名)或转换文件格式(图片格式转换、PDF与图片互转、DOCX转PDF、Markdown转PDF)时使用此技能。
---

# File Processor - 文件处理技能

## 概述

此技能提供文件重命名和格式转换功能,用于批量处理文件的命名和格式。支持批量重命名操作和多种文件格式之间的转换。

## 使用时机

当用户需要以下操作时使用此技能:

**文件重命名**:
- 批量为文件添加前缀或后缀
- 替换文件名中的部分文本
- 按编号规则重命名文件
- 使用正则表达式进行复杂重命名
- 重命名单个文件

**格式转换**:
- 图片格式转换 (JPG/PNG/WebP/BMP/TIFF 互转)
- PDF 转为图片
- 多张图片合并为 PDF
- Word 文档 (DOCX) 转为 PDF
- Markdown 文档转为 PDF

## 工作流程

### 文件重命名流程

1. **确定重命名类型**
   - 添加前缀/后缀: 使用 `add_prefix()` 或 `add_suffix()`
   - 替换文本: 使用 `replace_text()`
   - 编号重命名: 使用 `rename_with_numbering()`
   - 正则表达式: 使用 `rename_with_regex()`

2. **执行重命名**
   - 创建 FileRenamer 实例,指定目录路径
   - 调用相应的重命名方法
   - 执行 execute() 完成重命名

3. **验证结果**
   - 检查文件是否按预期重命名
   - 确认无命名冲突

### 格式转换流程

1. **确定转换类型**
   - 图片格式转换: 使用 `convert_images()`
   - PDF 转图片: 使用 `convert_pdf_to_images()`
   - 图片转 PDF: 使用 `convert_images_to_pdf()`
   - DOCX 转 PDF: 使用 `convert_docx_to_pdf()`
   - Markdown 转 PDF: 使用 `convert_markdown_to_pdf()`

2. **执行转换**
   - 创建 FormatConverter 实例
   - 调用相应的转换方法
   - 执行 execute() 完成转换

3. **验证结果**
   - 检查转换后的文件格式和质量
   - 确认文件完整性

## 使用方法

### 文件重命名

#### 1. 批量添加前缀

```python
from scripts.rename_files import FileRenamer

# 为所有文件添加前缀
renamer = FileRenamer("/path/to/directory")
renamer.add_prefix("new_")
renamer.execute()
```

#### 2. 批量添加后缀

```python
# 为所有文件添加后缀(在扩展名前)
renamer = FileRenamer("/path/to/directory")
renamer.add_suffix("_backup")
renamer.execute()
```

#### 3. 替换文件名中的文本

```python
# 将文件名中的 "old" 替换为 "new"
renamer = FileRenamer("/path/to/directory")
renamer.replace_text("old", "new")
renamer.execute()
```

#### 4. 按编号规则重命名

```python
# 将文件按名称排序,重命名为 photo_001.jpg, photo_002.jpg 等
renamer = FileRenamer("/path/to/directory")
renamer.rename_with_numbering(
    pattern="photo_{}.jpg",
    start_num=1,
    digits=3,
    sort_by="name"  # 也可为 "size" 或 "date"
)
renamer.execute()
```

#### 5. 使用正则表达式重命名

```python
# 使用正则表达式重命名
renamer = FileRenamer("/path/to/directory")
# 例如:将 "IMG_1234.jpg" 改为 "image_1234.jpg"
renamer.rename_with_regex(r"IMG_(\d+)", r"image_\1")
renamer.execute()
```

#### 6. 预览模式(不实际执行)

```python
# 使用 dry_run 模式预览重命名效果
renamer = FileRenamer("/path/to/directory", dry_run=True)
renamer.add_prefix("test_")
renamer.execute()  # 只显示预览,不实际重命名
```

### 格式转换

#### 1. 图片格式转换

```python
from scripts.convert_format import FormatConverter

# 将目录中的所有 JPG 图片转换为 PNG 格式
converter = FormatConverter()
converter.convert_images(
    directory="/path/to/images",
    target_format="png",
    quality=95
)
converter.execute()
```

#### 2. PDF 转图片

```python
# 将 PDF 转换为 PNG 图片
converter = FormatConverter()
converter.convert_pdf_to_images(
    pdf_path="/path/to/file.pdf",
    output_dir="/path/to/output",
    format="png",
    dpi=300
)
converter.execute()
```

#### 3. 图片转 PDF

```python
# 将目录中的图片合并为一个 PDF
converter = FormatConverter()
converter.convert_images_to_pdf(
    directory="/path/to/images",
    output_pdf="/path/to/output.pdf",
    sort=True  # 按名称排序
)
converter.execute()
```

#### 4. DOCX 转 PDF

```python
# 将 Word 文档转换为 PDF
converter = FormatConverter()
converter.convert_docx_to_pdf(
    docx_path="/path/to/document.docx",
    output_pdf="/path/to/output.pdf"
)
converter.execute()
```

#### 5. Markdown 转 PDF

```python
# 将 Markdown 文档转换为 PDF
converter = FormatConverter()
converter.convert_markdown_to_pdf(
    md_path="/path/to/document.md",
    output_pdf="/path/to/output.pdf"
)
converter.execute()
```

## 脚本使用说明

### rename_files.py

文件重命名工具,提供以下命令行功能:

```bash
# 添加前缀
python rename_files.py /path/to/directory prefix "new_prefix"

# 添加后缀
python rename_files.py /path/to/directory suffix "_backup"

# 替换文本
python rename_files.py /path/to/directory replace "old" "new"

# 编号重命名
python rename_files.py /path/to/directory numbering "photo_{}.jpg" --start 1 --digits 3 --sort name

# 正则表达式重命名
python rename_files.py /path/to/directory regex "IMG_(\d+)" "image_\1"

# 预览模式(不实际执行)
python rename_files.py /path/to/directory prefix "test_" --dry-run
```

### convert_format.py

文件格式转换工具,提供以下命令行功能:

```bash
# 图片格式转换
python convert_format.py images /path/to/images png --quality 95

# PDF 转图片
python convert_format.py pdf-to-images /path/to/file.pdf /path/to/output --format png --dpi 300

# 图片转 PDF
python convert_format.py images-to-pdf /path/to/images /path/to/output.pdf

# DOCX 转 PDF
python convert_format.py docx-to-pdf /path/to/document.docx /path/to/output.pdf

# Markdown 转 PDF
python convert_format.py md-to-pdf /path/to/document.md /path/to/output.pdf

# 预览模式
python convert_format.py images /path/to/images png --dry-run
```

## 依赖要求

**文件重命名**:
- Python 3.6+
- 无额外依赖(仅使用标准库)

**格式转换**:
- Python 3.6+
- Pillow: 图片处理 (`pip install Pillow`)
- pdf2image: PDF 转图片 (`pip install pdf2image`)
- docx2pdf: DOCX 转 PDF (`pip install docx2pdf`)
- markdown + weasyprint: Markdown 转 PDF (`pip install markdown weasyprint`)

**注意**: pdf2image 需要 Poppler 库在 Windows 上。可以从 https://github.com/oschwartz10612/poppler-windows/releases/ 下载并安装。

## 最佳实践

1. **使用预览模式**: 在执行批量操作前,先使用 `dry_run=True` 预览结果
2. **备份重要文件**: 执行批量重命名或转换前,先备份重要文件
3. **检查依赖**: 执行格式转换前,确保已安装所需的 Python 库
4. **验证结果**: 执行完成后,检查文件是否符合预期
5. **处理冲突**: 脚本会自动跳过会产生命名冲突的重命名操作

## 常见问题

**Q: 重命名操作可以撤销吗?**
A: 重命名操作是不可逆的。建议先使用 `dry_run=True` 预览,确认无误后再执行。

**Q: 如何处理嵌套目录中的文件?**
A: 当前脚本仅处理指定目录中的文件,不递归处理子目录。如需处理子目录,需要手动遍历。

**Q: 图片转换会保持原质量吗?**
A: 可以通过 `quality` 参数控制图片质量(1-100),默认为 95。

**Q: PDF 转图片需要安装什么?**
A: 需要安装 `pdf2image` 库和 Poppler 库。Poppler 在 Windows 上需要单独下载安装。

**Q: 支持哪些图片格式?**
A: 支持 JPG、JPEG、PNG、WebP、BMP、TIFF 等常见格式。

## 资源

此技能包含以下可执行脚本:

- `scripts/rename_files.py`: 文件重命名工具
- `scripts/convert_format.py`: 文件格式转换工具

这些脚本可以直接作为 Python 模块导入使用,也可以通过命令行调用。
