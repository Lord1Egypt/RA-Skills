---
name: md-converter
description: |-
  Convert Markdown (.md) files to Word (.docx), PDF, and styled HTML in one shot.
  Use when the user asks to: "md 转 Word", "Markdown 转 PDF", "md 转 HTML",
  "Markdown 生成文档", "把 md 文件转成 docx/pdf/html", or wants to convert
  a Markdown file to a viewable/shared document format.
  Supports Chinese (CJK) text with PingFang/SimHei fonts.
version: 1.1.0
agent_created: true
allowed-tools: Bash
---

# Markdown Converter

Convert a Markdown (.md) file to Word (.docx), PDF, and/or styled HTML.

## 安装与设置（分享给朋友时的重要说明）

在使用本 skill 前，需要先安装 Python 依赖：

### macOS / Linux

```bash
python3 -m pip install python-docx reportlab
```

### Windows

```bash
python -m pip install python-docx reportlab
```

如果遇到权限问题，加 `--user`：`python3 -m pip install --user python-docx reportlab`

> **注意：** PDF 脚本使用 reportlab，首次安装可能耗时 10-30 秒。HTML 脚本无外部依赖，可直接运行。

### 验证安装

```bash
python3 -c "import docx, reportlab; print('OK')"
```

输出 `OK` 表示依赖已就绪。

---

## Capabilities

- **HTML** — Generates a responsive, card-layout HTML page with embedded CSS（无额外依赖）
- **DOCX** — Creates a formatted Word document with headings, tables, lists, code blocks（需 `python-docx`）
- **PDF** — Generates a PDF via reportlab with proper Chinese font support（需 `reportlab`）
- **Batch** — `convert_all.py` runs all three formats at once

## Workflow

### Step 1: Auto-detect Python

Refer to the system's available Python runtimes. Prefer `python3` — it works on macOS/Linux.
On Windows, use `python` if `python3` is unavailable.

### Step 2: Ensure dependencies

If the user reports errors, install dependencies as described in the **安装与设置** section above.

### Step 3: Convert

Choose the appropriate script based on what the user wants:

| User says | Run |
|-----------|-----|
| "转成 HTML" / "只需要网页版" | `python3 scripts/md_to_html.py <input.md>` |
| "转成 Word" / "生成 docx" | `python3 scripts/md_to_docx.py <input.md>` |
| "转成 PDF" | `python3 scripts/md_to_pdf.py <input.md>` |
| "全转" / "都要" / 没说具体格式 | `python3 scripts/convert_all.py <input.md>` |

Each script accepts an optional second argument for the output path:

```bash
python3 scripts/md_to_html.py input.md output.html
python3 scripts/md_to_docx.py input.md output.docx
python3 scripts/md_to_pdf.py input.md output.pdf
python3 scripts/convert_all.py input.md /path/to/output/dir/
```

### Step 4: Verify & present

After conversion:
1. Check that the output files exist and have reasonable file sizes
2. Read the generated HTML for preview if needed
3. Use `deliver_attachments` to send all generated files to the user
4. Summarize the output briefly — file paths, sizes, formats

## Supported Markdown Features

| Feature | HTML | DOCX | PDF |
|---------|------|------|-----|
| Headings (h1-h4) | ✓ | ✓ | ✓ |
| Bold / Italic | ✓ | ✓ | ✓ |
| Inline code | ✓ | ✓ | ✓ |
| Code blocks | ✓ | ✓ | ✓ |
| Unordered lists | ✓ | ✓ | ✓ |
| Ordered lists | ✓ | ✓ | ✓ |
| Tables | ✓ | ✓ | ✓ |
| Links | ✓ | ✓ | ✓ |
| Horizontal rules | ✓ | ✓ | ✓ |
| Blockquotes | ✓ | ✗ | ✗ |

## Notes

- HTML output includes responsive CSS suitable for desktop and mobile viewing
- PDF uses PingFang (macOS) or SimHei (Windows) for Chinese text — falls back to Helvetica if neither is found
- DOCX uses python-docx; table styling includes header row coloring and zebra striping
- For Chinese text with special characters (quotes, dashes), prefer using ASCII equivalents or ensure the input file is UTF-8 encoded

## 常见问题

**Q: 报错 "No module named 'docx'"**
→ 运行 `python3 -m pip install python-docx`

**Q: PDF 中文显示为方块**
→ 脚本会自动检测系统字体。macOS 用 PingFang，Windows 用 SimHei。如果字体缺失，安装对应中文字体即可。

**Q: Windows 上 python3 不存在**
→ 用 `python` 代替 `python3`。确认已安装 Python 3.7+ 并加入 PATH。
