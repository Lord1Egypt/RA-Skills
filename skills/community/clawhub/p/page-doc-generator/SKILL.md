---
name: page-doc-generator
description: Generate Word documentation from mini-program/uni-app project screenshots and source code. Use when user wants to document pages with screenshots and code. Triggered by requests like "create page document", "generate project documentation", "document with screenshots and code", "create Word document from project screenshots".
---

# Page Doc Generator

Generate Word (.docx) documentation from mini-program/uni-app projects, embedding screenshots and source code for each page.

## Inputs (Required)

| Input | Description | Example |
|-------|-------------|---------|
| `project_path` | Absolute path to the project root | `D:\Project\myapp` |
| `screenshots_dir` | Absolute path to screenshots directory | `D:\Project\myapp\static\页面截图` |

## Output

Generates two files in the project directory:
- `{project_name}_页面文档.md` - Markdown source
- `{project_name}_页面文档.docx` - Word document

## Workflow

### Step 1: Scan Project Structure

Find all Vue page files in `pages/` directory:

```python
# Pages are in: project_path/pages/{page_name}/{page_name}.vue
pages = find_pages(project_path)
# Returns: [{"name": "index", "path": "...", "dir": "..."}, ...]
```

### Step 2: Scan Screenshots

Find all images in screenshots directory:

```python
screenshots = find_screenshots(screenshots_dir)
# Returns: {"书籍录入02": "D:/Project/.../书籍录入02.png", ...}
```

### Step 3: Generate Markdown

Generate documentation with this structure per page:

```markdown
# 页面：page_name

## 页面截图
![page_name](screenshot_path.png)

## 页面信息
| 项目 | 内容 |
|------|------|
| 路径 | `pages/xxx/xxx.vue` |
| 总行数 | N |

## 源代码
```vue
<!-- Vue code here -->
```
```

### Step 4: Convert to Word

Use pandoc to convert Markdown to DOCX:

```bash
pandoc "markdown_file.md" -o "output.docx" --resource-path="screenshots_dir"
```

## Scripts

### generate_page_doc.py

Main generation script:

```bash
python scripts/generate_page_doc.py <project_path> <screenshots_dir> [output_dir]
```

### convert_to_docx.py

Convert Markdown to Word:

```bash
python scripts/convert_to_docx.py <markdown_file> [output_dir]
```

## Quick Usage

```bash
# Full pipeline
python scripts/generate_page_doc.py "D:\Project\myapp" "D:\Project\myapp\static\截图"
python scripts/convert_to_docx.py "D:\Project\myapp\myapp_页面文档.md"
```

## Screenshot Matching

The script matches pages to screenshots by filename:
- Page `index` → screenshot `index.png` or `index01.png`
- Page `notes` → screenshot `notes.png` or `notes01.png`

If exact match not found, tries common variations (append 01, 02, etc.).

## Notes

- Screenshots should be PNG, JPG, JPEG, GIF, or WebP format
- Very large Vue files (>500 lines) are truncated in docs with a note
- pandoc must be installed and in PATH for DOCX conversion
